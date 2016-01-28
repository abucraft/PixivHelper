# -*- coding:utf-8 -*-
from pixivpy3 import PixivAPI
from pixivpy3 import PixivError
from datetime import datetime
import re
import json
import os
class Worker:
    writes = 0
    api = PixivAPI()
    root_dir = "image"
    size = "large"
    latest_time = "2000-01-18 23:41:35"
    def login(self,username,password):
        self.token = self.api.login(username,password)

    #循环检查路径是否存在
    def check_root_dir(self,path_list):
        if not os.path.exists(self.root_dir):
            os.mkdir(self.root_dir)
        cur_path = self.root_dir
        for path in path_list:
            cur_path = os.path.join(cur_path,path)
            if not os.path.exists(cur_path):
                os.mkdir(cur_path)

    def check_result(self,result,filepath):
        if cmp(result["status"],"success") != 0:
            file(filepath,"w").write(json.dumps(result))
            raise PixivError(json.dumps(result))

    def pull_following_works(self,time,nums=10,
        flt={
        'illustration':True,
        'manga':True,
        'ugoira':True
        }):
        result = self.api.me_following_works();
        self.check_root_dir(["following"])
        curpg = 1
        per_pg = 30
        self.check_result(result,os.path.join(self.root_dir,"following","error.json"))
        file(os.path.join(self.root_dir,"following","metadata.json"),"w").write(json.dumps(result))
        total = result["pagination"]["total"]
        nums = (nums < total and [nums] or [total])[0]
        for i in range(0,nums):
            if curpg < i/per_pg + 1:
                curpg+=1
                result = self.api.me_following_works(page=curpg)
                self.check_result(result,os.path.join(self.root_dir,"following","error.json"))

            idx = i%per_pg
            info_json = result["response"][idx]
            reup_time = info_json["reuploaded_time"]
            #过滤掉不想要的图片
            if not flt[info_json["type"]]:
                continue
            #这个方法在抓取排行时不可取
            #在上次扒取的时间点之前的图片就放弃
            #if datetime.strptime(reup_time,"%Y-%m-%d %H:%M:%S") < time:
            #    continue
            self.save_work(info_json,os.path.join(self.root_dir,"following"))
            if datetime.strptime(self.latest_time,"%Y-%m-%d %H:%M:%S") < datetime.strptime(reup_time,"%Y-%m-%d %H:%M:%S"):
                self.latest_time = reup_time
        return result

    def pull_ranking_works(self,time,nums=10,work_type="all",rank_type = "daily",
        flt={
        'illustration':True,
        'manga':True,
        'ugoira':True
        }):
        self.check_root_dir([work_type,rank_type])
        result = self.api.ranking(ranking_type = work_type,mode = rank_type)
        curpg = 1
        per_pg = 50

        self.check_result(result,os.path.join(self.root_dir,work_type,rank_type,"error.json"))

        file(os.path.join(self.root_dir,work_type,rank_type,"metadata.json"),"w").write(json.dumps(result))
        total = result["pagination"]["total"]
        nums = (nums < total and [nums] or [total])[0]
        for i in range(0,nums):
            if curpg < i/per_pg + 1:
                curpg+=1
                result = self.api.me_following_works(page=curpg,ranking_type=rank_type,mode = work_type)
                self.check_result(result,os.path.join(self.root_dir,work_type,rank_type,"error.json"))

                file(os.path.join(self.root_dir,work_type,rank_type,"metadata.json"),"w").write(json.dumps(result))
            idx = i%per_pg
            info_json = result["response"][0]["works"][idx]["work"]
            reup_time = info_json["reuploaded_time"]
            #过滤掉不想要的图片
            if not flt[info_json["type"]]:
                continue
            #在上次扒取的时间点之前的图片就放弃
            #if datetime.strptime(reup_time,"%Y-%m-%d %H:%M:%S") < time:
            #    continue
            self.save_work(info_json,os.path.join(self.root_dir,work_type,rank_type))
            if datetime.strptime(self.latest_time,"%Y-%m-%d %H:%M:%S") < datetime.strptime(reup_time,"%Y-%m-%d %H:%M:%S"):
                self.latest_time = reup_time
        return result

    def save_work(self,info_json,path):
        #过滤不想保存的作品
        if cmp(info_json["type"],"ugoira") == 0:
            self.save_ugoira(info_json,path)
        if cmp(info_json["type"],"illustration") == 0:
            self.save_image(info_json,path)
        if cmp(info_json["type"],"manga") == 0:
            self.save_image(info_json,path)
        return

    def save_ugoira(self,info_json,path):
        full_info = self.api.works(info_json["id"])
        urls = full_info["response"][0]["metadata"]["zip_urls"]

        first_url = None
        for item in urls:
            first_url = urls[item]
            break
        file_name = first_url[first_url.rfind("/")+1:]
        if os.path.exists(os.path.join(path,file_name)):
            #print u"文件已存在:跳过"
            return first_url
        file(os.path.join(path,"%s.json" % (file_name)),"w").write(json.dumps(full_info))
        res = self.api.auth_requests_call("GET",first_url)
        data = res.content
        file(os.path.join(path,file_name),"wb").write(data)
        self.writes += int(res.headers["content-length"])
        #not finish
        print first_url
        print res.headers["content-length"]
        return first_url

    def save_image(self,info_json,path):
        page_count = info_json["page_count"]
        #如果是漫画，也就是多幅图片就存在id文件夹下面
        if page_count != 1:
            cur_path = os.path.join(path,"%d"%info_json["id"])
            if not os.path.exists(cur_path):
                os.mkdir(cur_path)
        else:
            cur_path = path

        for i in range(0,page_count):
            origin_url = info_json["image_urls"][self.size]
            p_idx = origin_url.rfind("_p")
            if cmp(self.size,"large") == 0:
                r_idx = origin_url.rfind(".")
            else:
                r_idx = origin_url.rfind("_")

            img_url = "%s_p%d%s" % (origin_url[:p_idx],i,origin_url[r_idx:])
            file_name = img_url[img_url.rfind("/")+1:]
            if os.path.exists(os.path.join(cur_path,file_name)):
                #print u"文件已存在:跳过"
                continue
            res = self.api.auth_requests_call("GET",img_url)
            data = res.content
            file(os.path.join(cur_path, file_name), "wb").write(data)
            self.writes += int(res.headers["content-length"])
            print os.path.join(cur_path,file_name)
            print res.headers["content-length"]
