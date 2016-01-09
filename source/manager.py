# -*- coding:utf-8 -*-
from worker import Worker
from datetime import datetime
from pixivpy3 import PixivError
import wx
import os
import copy
import json
import logging
import sys
import _winreg

exepath,exename = os.path.split(sys.argv[0])
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=os.path.join(exepath,"log.txt"),
                filemode='w')
def get_path_size(str_path):
    if not os.path.exists(str_path):
        return 0
    if os.path.isfile(str_path):
        return os.path.getsize(str_path)
    total_size = 0
    for str_root, ls_dirs, ls_files in os.walk(str_path):
        #get child directory size
        #for str_dir in ls_dirs:
        #    total_size = total_size + get_path_size(os.path.join(str_root, str_dir));

        #for child file size
        for str_file in ls_files:
            total_size = total_size + os.path.getsize(os.path.join(str_root, str_file));
    return total_size

class Manager:
    #设置log
    worker = Worker()
    cur_size = 0
    settings = {
        "runnable": False,
        "crawl_setting":{
            "spotlight":{
                "todo":False
            },
            "following":{
                "todo":True,
                "nums":10,
                "filter_setting":{
                    "illustration":True,
                    "manga":True,
                    "ugoira":True
                }
            },
            "ranking":{
                "all":{
                    "type":{
                        "daily":{
                            "todo":True,
                            "nums":10
                        },
                        "weekly":{
                            "todo":False,
                            "nums":10
                        },
                        "monthly":{
                            "todo":False,
                            "nums":10
                        },
                        "rookie":{
                            "todo":False,
                            "nums":10
                        },
                        "original":{
                            "todo":False,
                            "nums":10
                        },
                        "male":{
                            "todo":False,
                            "nums":10
                        },
                        "female":{
                            "todo":False,
                            "nums":10
                        },
                        "daily_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "weekly_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "male_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "female_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "r18g":{
                            "todo":False,
                            "nums":10
                        }
                    },
                    "filter_setting":{
                        "illustration":True,
                        "manga":True,
                        "ugoira":True
                    }
                },
                "illust":{
                    "type":{
                        "daily":{
                            "todo":True,
                            "nums":10
                        },
                        "weekly":{
                            "todo":False,
                            "nums":10
                        },
                        "monthly":{
                            "todo":False,
                            "nums":10
                        },
                        "rookie":{
                            "todo":False,
                            "nums":10
                        },
                        "daily_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "weekly_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "r18g":{
                            "todo":False,
                            "nums":10
                        }
                    },
                    "filter_setting":{
                        "illustration":True,
                        "manga":True,
                        "ugoira":True
                    }
                },
                "manga":{
                    "type":{
                        "daily":{
                            "todo":False,
                            "nums":10
                        },
                        "weekly":{
                            "todo":False,
                            "nums":10
                        },
                        "monthly":{
                            "todo":False,
                            "nums":10
                        },
                        "rookie":{
                            "todo":False,
                            "nums":10
                        },
                        "daily_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "weekly_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "r18g":{
                            "todo":False,
                            "nums":10
                        }
                    },
                    "filter_setting":{
                        "illustration":True,
                        "manga":True,
                        "ugoira":True
                    }
                },
                "ugoira":{
                    "type":{
                        "daily":{
                            "todo":False,
                            "nums":10
                        },
                        "weekly":{
                            "todo":False,
                            "nums":10
                        },
                        "daily_r18":{
                            "todo":False,
                            "nums":10
                        },
                        "weekly_r18":{
                            "todo":False,
                            "nums":10
                        }
                    },
                    "filter_setting":{
                        "illustration":True,
                        "manga":True,
                        "ugoira":True
                    }
                }
            }
        },
        "auto_boot":True,
        "disk_setting":{
            "root_dir":"image",
            "max_size": 4096000000
        },
        "image_size":"large",
        "time_setting":{
            "from":"00:00:00",
            "to":"23:59:59",
            "span_mili_second":60000
        },
        "user_info":{
            "username":"",
            "password":""
        },
        "last_crawl_time":"2000-01-18 23:41:35"
    }
    is_working = False
    def load_setting(self):
        if not os.path.exists(os.path.join(exepath,"settings.json")):
            self.settings["disk_setting"]["root_dir"] = os.path.join(os.getcwd(),exepath,"image")
            self.worker.root_dir = self.settings["disk_setting"]["root_dir"]
            try:
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",0,_winreg.KEY_WRITE)
                _winreg.SetValueEx(key,"PixivHelper",0,os.path.join(exepath,_winreg.REG_SZ,sys.argv[0]))
                file(os.path.join(exepath,"settings.json"),"w").write(json.dumps(self.settings))
            except Exception as e:
                print e
        else:
            self.settings = json.load(file(os.path.join(exepath,"settings.json"),"r"))
            self.worker.root_dir = self.settings["disk_setting"]["root_dir"]
            try:
                if self.settings["auto_boot"]:
                    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",0,_winreg.KEY_WRITE)
                    _winreg.SetValueEx(key,"PixivHelper",1,_winreg.REG_SZ,os.path.join(os.getcwd(),sys.argv[0]))
                else:
                    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",0,_winreg.KEY_WOW64_64KEY + _winreg.KEY_ALL_ACCESS)
                    _winreg.DeleteValue(key,"PixivHelper")
            except Exception as e:
                logging.error(e)

    def __init__(self):
        self.load_setting()
        self.cur_size = get_path_size(self.settings["disk_setting"]["root_dir"])
        print "目录大小为 : %d" % self.cur_size

    def apply_settings(self):
        if not self.settings["runnable"]:
            self.settings["runnable"] = True
        file(os.path.join(exepath,"settings.json"),"w").write(json.dumps(self.settings))
        self.worker.root_dir = self.settings["disk_setting"]["root_dir"]
        try:
            if self.settings["auto_boot"]:
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",0,_winreg.KEY_WRITE)
                _winreg.SetValueEx(key,"PixivHelper",1,_winreg.REG_SZ,os.path.join(os.getcwd(),sys.argv[0]))
            else:
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",0,_winreg.KEY_WOW64_64KEY + _winreg.KEY_ALL_ACCESS)
                _winreg.DeleteValue(key,r"PixivHelper")
        except Exception as e:
            logging.error(e)

    def crawl(self):
        self.worker.size = self.settings["image_size"]
        if self.cur_size > self.settings["disk_setting"]["max_size"]:
            logging.info("total images size out of range %d" % self.cur_size)
        else:
            if self.settings["crawl_setting"]["following"]["todo"]:
                self.worker.pull_following_works(datetime.strptime(self.settings["last_crawl_time"],"%Y-%m-%d %H:%M:%S"),
                    self.settings["crawl_setting"]["following"]["nums"],
                    self.settings["crawl_setting"]["following"]["filter_setting"])
            rankings = self.settings["crawl_setting"]["ranking"]
            for work_type in rankings:
                for rank_type in rankings[work_type]["type"]:
                    if rankings[work_type]["type"][rank_type]["todo"]:
                        self.worker.pull_ranking_works(datetime.strptime(self.settings["last_crawl_time"],"%Y-%m-%d %H:%M:%S"),
                        rankings[work_type]["type"][rank_type]["nums"],work_type,rank_type,rankings[work_type]["filter_setting"])
            self.cur_size += self.worker.writes
            self.worker.writes = 0
            self.settings["last_crawl_time"] = self.worker.latest_time
            file(os.path.join(exepath,"settings.json"),"w").write(json.dumps(self.settings))

    def work(self):
        if self.is_working:
            return
        self.is_working = True
        try:
            self.crawl()
        except PixivError as perror:
            try:
                self.worker.login(self.settings["user_info"]["username"],self.settings["user_info"]["password"])
                self.crawl()
            except Exception as e:
                logging.error(e)
                logging.error(u"可能是登录出错了，请检查一下用户名和密码")
                logging.error(u"也有可能是pixiv用户设置里的相关选项没打开")
                logging.error(u"具体参考报错信息以及相关目录下的metadata.json")
                wx.MessageBox(u"可能是登录出错也可能是其他错误，请检查log.txt",u"出错了",wx.OK|wx.ICON_ERROR)
        finally:
            self.is_working = False

    def test(self):
        self.work()

#C:\Users\ok\AppData\Local\VirtualStore\Windows\SysWOW64u
