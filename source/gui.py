#-*- coding:utf-8 –*-
import wx
import os
import thread
import sys
import win32com.client
from manager import Manager
from datetime import time
from datetime import datetime
TRAY_TOOLTIP = 'Pixiv Helper'
TRAY_ICON = 'icon.ico'

import wx.lib.buttons as buttons
import wx.lib.masked as masked

username = "username"
password = "password"
starttime = '12:00:00'
endtime = '12:00:00'
picsize = 0 # 0-原图 1-中等 2-缩略图
picdir = "D:\\"
limitroom = 1024
timeinterval = 5
autoboot = False

guanzhu_chahua = True
guanzhu_manhua = False
guanzhu_dongtu = False
guanzhu_shuliang = 10

zonghe_chahua = False
zonghe_manhua = False
zonghe_dongtu = False
zonghe_jinri = False
zonghe_benzhou = False
zonghe_benyue = False
zonghe_xinren = False
zonghe_nanxing = False
zonghe_nvxing = False
zonghe_r18_nanxing = False
zonghe_r18_nvxing = False
zonghe_r18_meiri = False
zonghe_r18_meizhou = False
zonghe_r18g = False
zonghe_yuanchuang = False
zonghe_shuliang = 10

chahua_jinri = False
chahua_benzhou = False
chahua_benyue = False
chahua_xinren = False
chahua_r18_meiri = False
chahua_r18_meizhou = False
chahua_r18g = False
chahua_shuliang = 10

manhua_jinri = False
manhua_benzhou = False
manhua_benyue = False
manhua_xinren = False
manhua_r18_meiri = False
manhua_r18_meizhou = False
manhua_r18g = False
manhua_shuliang = 10

dongtu_jinri = False
dongtu_benzhou = False
dongtu_r18_meiri = False
dongtu_r18_meizhou = False
dongtu_shuliang = 10

class TestDialog1(wx.Dialog):
  def __init__(
        self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
        style=wx.DEFAULT_DIALOG_STYLE,
        ):
    pre = wx.PreDialog()
    pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
    pre.Create(parent, ID, title, pos, size, style)
    self.PostCreate(pre)
    box = wx.StaticBox(self,-1,u'抓取类型')
    sizer = wx.StaticBoxSizer(box,wx.VERTICAL)
    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb1 = wx.CheckBox(self, -1, u"插画")
    self.cb1.SetValue(guanzhu_chahua)
    box.Add(self.cb1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    self.cb2 = wx.CheckBox(self, -1, u"漫画")
    self.cb2.SetValue(guanzhu_manhua)
    box.Add(self.cb2, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    self.cb3 = wx.CheckBox(self, -1, u"动图")
    self.cb3.SetValue(guanzhu_dongtu)
    box.Add(self.cb3, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(box, 0, wx.ALL, 5)

    spinsizer = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText(self, wx.ID_ANY, u"每次扫描数量:", wx.DefaultPosition, wx.DefaultSize, 0 )

    self.sc = wx.SpinCtrl(self, -1, "", size=(70, 25))
    self.sc.SetRange(1,2048)
    self.sc.SetValue(guanzhu_shuliang)

    spinsizer.Add((7,10))
    spinsizer.Add(text1, 0, wx.ALL, 3)
    spinsizer.Add(self.sc, 0, wx.ALL, 0)

    btnsizer = wx.StdDialogButtonSizer()

    btn = wx.Button(self, wx.ID_OK, label=u'确定')
    btn.SetDefault()
    btnsizer.AddButton(btn)

    btn = wx.Button(self, wx.ID_CANCEL, label=u'取消')
    btnsizer.AddButton(btn)
    btnsizer.Realize()


    globalsizer = wx.BoxSizer(wx.VERTICAL)
    globalsizer.Add(sizer,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(spinsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    self.SetSizer(globalsizer)
    globalsizer.Fit(self)

class TestDialog2(wx.Dialog):
  def __init__(
        self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
        style=wx.DEFAULT_DIALOG_STYLE,
        ):
    pre = wx.PreDialog()
    pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
    pre.Create(parent, ID, title, pos, size, style)
    self.PostCreate(pre)
    box = wx.StaticBox(self,-1,u'抓取类型')
    sizer = wx.StaticBoxSizer(box,wx.VERTICAL)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb1 = wx.CheckBox(self, -1, u"插画")
    self.cb1.SetValue(zonghe_chahua)
    box.Add(self.cb1, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer.Add(box, 0, wx.ALL, 0)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb2 = wx.CheckBox(self, -1, u"漫画")
    self.cb2.SetValue(zonghe_manhua)
    box.Add(self.cb2, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb3 = wx.CheckBox(self, -1, u"动图")
    self.cb3.SetValue(zonghe_dongtu)
    box.Add(self.cb3, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)

    box = wx.StaticBox(self,-1,u'排行类型')
    sizer2 = wx.StaticBoxSizer(box,wx.VERTICAL)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb4 = wx.CheckBox(self, -1, u"今日")
    self.cb4.SetValue(zonghe_jinri)
    box.Add(self.cb4, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    box.Add((36,5))
    self.cb5 = wx.CheckBox(self, -1, u"本周")
    self.cb5.SetValue(zonghe_benzhou)
    box.Add(self.cb5, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    box.Add((55,5))
    self.cb6 = wx.CheckBox(self, -1, u"本月")
    self.cb6.SetValue(zonghe_benyue)
    box.Add(self.cb6, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    box.Add((19,5))
    self.cb7 = wx.CheckBox(self, -1, u"新人")
    self.cb7.SetValue(zonghe_xinren)
    box.Add(self.cb7, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer2.Add(box, 0, wx.ALL, 0)

    box = wx.BoxSizer(wx.HORIZONTAL)

    self.cb8 = wx.CheckBox(self, -1, u"受男性欢迎")
    self.cb8.SetValue(zonghe_nanxing)
    box.Add(self.cb8, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb9 = wx.CheckBox(self, -1, u"r18受男性欢迎")
    self.cb9.SetValue(zonghe_r18_nanxing)
    box.Add(self.cb9, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb10 = wx.CheckBox(self, -1, u"r18每日")
    self.cb10.SetValue(zonghe_r18_meiri)
    box.Add(self.cb10, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb11 = wx.CheckBox(self, -1, u"r18每周")
    self.cb11.SetValue(zonghe_r18_meizhou)
    box.Add(self.cb11, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer2.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)

    box = wx.BoxSizer(wx.HORIZONTAL)

    self.cb12 = wx.CheckBox(self, -1, u"受女性欢迎")
    self.cb12.SetValue(zonghe_nvxing)
    box.Add(self.cb12, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb13 = wx.CheckBox(self, -1, u"r18受女性欢迎")
    self.cb13.SetValue(zonghe_r18_nvxing)
    box.Add(self.cb13, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb14 = wx.CheckBox(self, -1, u"r18g")
    self.cb14.SetValue(zonghe_r18g)
    box.Add(self.cb14, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    box.Add((16,5))
    self.cb15 = wx.CheckBox(self, -1, u"原创")
    self.cb15.SetValue(zonghe_yuanchuang)
    box.Add(self.cb15, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer2.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)

    spinsizer = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText(self, wx.ID_ANY, u"每次扫描数量:", wx.DefaultPosition, wx.DefaultSize, 0 )

    self.sc = wx.SpinCtrl(self, -1, "", size=(70, 25))
    self.sc.SetRange(1,2048)
    self.sc.SetValue(zonghe_shuliang)

    spinsizer.Add((7,10))
    spinsizer.Add(text1, 0, wx.ALL, 3)
    spinsizer.Add(self.sc, 0, wx.ALL, 0)

    btnsizer = wx.StdDialogButtonSizer()

    btn = wx.Button(self, wx.ID_OK, label=u'确定')
    btn.SetDefault()
    btnsizer.AddButton(btn)

    btn = wx.Button(self, wx.ID_CANCEL, label=u'取消')
    btnsizer.AddButton(btn)
    btnsizer.Realize()

    globalsizer = wx.BoxSizer(wx.VERTICAL)
    hsizer = wx.BoxSizer(wx.HORIZONTAL)
    hsizer.Add(sizer,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    hsizer.Add(sizer2,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(hsizer,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(spinsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
    self.SetSizer(globalsizer)
    globalsizer.Fit(self)

class TestDialog3(wx.Dialog):
  def __init__(
        self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
        style=wx.DEFAULT_DIALOG_STYLE,
        ):
    pre = wx.PreDialog()
    pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
    pre.Create(parent, ID, title, pos, size, style)
    self.PostCreate(pre)
    box = wx.StaticBox(self,-1,u'排行类型')
    sizer = wx.StaticBoxSizer(box,wx.VERTICAL)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb1 = wx.CheckBox(self, -1, u"今日")
    self.cb1.SetValue(chahua_jinri)
    box.Add(self.cb1, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb2 = wx.CheckBox(self, -1, u"本周")
    self.cb2.SetValue(chahua_benzhou)
    box.Add(self.cb2, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb3 = wx.CheckBox(self, -1, u"本月")
    self.cb3.SetValue(chahua_benyue)
    box.Add(self.cb3, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb4 = wx.CheckBox(self, -1, u"新人")
    self.cb4.SetValue(chahua_xinren)
    box.Add(self.cb4, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer.Add(box, 0, wx.ALL, 5)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb5 = wx.CheckBox(self, -1, u"r18每日")
    self.cb5.SetValue(chahua_r18_meiri)
    box.Add(self.cb5, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
    self.cb6 = wx.CheckBox(self, -1, u"r18每周")
    self.cb6.SetValue(chahua_r18_meizhou)
    box.Add(self.cb6, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
    self.cb7 = wx.CheckBox(self, -1, u"r18g")
    self.cb7.SetValue(chahua_r18g)
    box.Add(self.cb7, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


    spinsizer = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText(self, wx.ID_ANY, u"每次扫描数量:", wx.DefaultPosition, wx.DefaultSize, 0 )

    self.sc = wx.SpinCtrl(self, -1, "", size=(70, 25))
    self.sc.SetRange(1,2048)
    self.sc.SetValue(chahua_shuliang)

    spinsizer.Add((7,10))
    spinsizer.Add(text1, 0, wx.ALL, 3)
    spinsizer.Add(self.sc, 0, wx.ALL, 0)

    btnsizer = wx.StdDialogButtonSizer()

    btn = wx.Button(self, wx.ID_OK, label=u'确定')
    btn.SetDefault()
    btnsizer.AddButton(btn)

    btn = wx.Button(self, wx.ID_CANCEL, label=u'取消')
    btnsizer.AddButton(btn)
    btnsizer.Realize()


    globalsizer = wx.BoxSizer(wx.VERTICAL)
    globalsizer.Add(sizer,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(spinsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    self.SetSizer(globalsizer)
    globalsizer.Fit(self)

class TestDialog4(wx.Dialog):
  def __init__(
        self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
        style=wx.DEFAULT_DIALOG_STYLE,
        ):
    pre = wx.PreDialog()
    pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
    pre.Create(parent, ID, title, pos, size, style)
    self.PostCreate(pre)
    box = wx.StaticBox(self,-1,u'排行类型')
    sizer = wx.StaticBoxSizer(box,wx.VERTICAL)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb1 = wx.CheckBox(self, -1, u"今日")
    self.cb1.SetValue(manhua_jinri)
    box.Add(self.cb1, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb2 = wx.CheckBox(self, -1, u"本周")
    self.cb2.SetValue(manhua_benzhou)
    box.Add(self.cb2, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb3 = wx.CheckBox(self, -1, u"本月")
    self.cb3.SetValue(manhua_benyue)
    box.Add(self.cb3, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    self.cb4 = wx.CheckBox(self, -1, u"新人")
    self.cb4.SetValue(manhua_xinren)
    box.Add(self.cb4, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
    sizer.Add(box, 0, wx.ALL, 5)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb5 = wx.CheckBox(self, -1, u"r18每日")
    self.cb5.SetValue(manhua_r18_meiri)
    box.Add(self.cb5, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
    self.cb6 = wx.CheckBox(self, -1, u"r18每周")
    self.cb6.SetValue(manhua_r18_meizhou)
    box.Add(self.cb6, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
    self.cb7 = wx.CheckBox(self, -1, u"r18g")
    self.cb7.SetValue(manhua_r18g)
    box.Add(self.cb7, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


    spinsizer = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText(self, wx.ID_ANY, u"每次扫描数量:", wx.DefaultPosition, wx.DefaultSize, 0 )

    self.sc = wx.SpinCtrl(self, -1, "", size=(70, 25))
    self.sc.SetRange(1,2048)
    self.sc.SetValue(manhua_shuliang)

    spinsizer.Add((7,10))
    spinsizer.Add(text1, 0, wx.ALL, 3)
    spinsizer.Add(self.sc, 0, wx.ALL, 0)

    btnsizer = wx.StdDialogButtonSizer()

    btn = wx.Button(self, wx.ID_OK, label=u'确定')
    btn.SetDefault()
    btnsizer.AddButton(btn)

    btn = wx.Button(self, wx.ID_CANCEL, label=u'取消')
    btnsizer.AddButton(btn)
    btnsizer.Realize()


    globalsizer = wx.BoxSizer(wx.VERTICAL)
    globalsizer.Add(sizer,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(spinsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    self.SetSizer(globalsizer)
    globalsizer.Fit(self)

class TestDialog5(wx.Dialog):
  def __init__(
        self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
        style=wx.DEFAULT_DIALOG_STYLE,
        ):
    pre = wx.PreDialog()
    pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
    pre.Create(parent, ID, title, pos, size, style)
    self.PostCreate(pre)
    box = wx.StaticBox(self,-1,u'排行类型')
    sizer = wx.StaticBoxSizer(box,wx.VERTICAL)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb1 = wx.CheckBox(self, -1, u"今日")
    self.cb1.SetValue(dongtu_jinri)
    box.Add(self.cb1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    self.cb2 = wx.CheckBox(self, -1, u"r18每日")
    self.cb2.SetValue(dongtu_r18_meiri)
    box.Add(self.cb2, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(box, 0, wx.ALL, 5)

    box = wx.BoxSizer(wx.HORIZONTAL)
    self.cb3 = wx.CheckBox(self, -1, u"本周")
    self.cb3.SetValue(dongtu_benzhou)
    box.Add(self.cb3, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    self.cb4 = wx.CheckBox(self, -1, u"r18每周")
    self.cb4.SetValue(dongtu_r18_meizhou)
    box.Add(self.cb4, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    spinsizer = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText(self, wx.ID_ANY, u"每次扫描数量:", wx.DefaultPosition, wx.DefaultSize, 0 )

    self.sc = wx.SpinCtrl(self, -1, "", size=(70, 25))
    self.sc.SetRange(1,2048)
    self.sc.SetValue(dongtu_shuliang)

    spinsizer.Add((7,10))
    spinsizer.Add(text1, 0, wx.ALL, 3)
    spinsizer.Add(self.sc, 0, wx.ALL, 0)

    btnsizer = wx.StdDialogButtonSizer()

    btn = wx.Button(self, wx.ID_OK, label=u'确定')
    btn.SetDefault()
    btnsizer.AddButton(btn)

    btn = wx.Button(self, wx.ID_CANCEL, label=u'取消')
    btnsizer.AddButton(btn)
    btnsizer.Realize()

    globalsizer = wx.BoxSizer(wx.VERTICAL)
    globalsizer.Add(sizer,0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(spinsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    globalsizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    self.SetSizer(globalsizer)
    globalsizer.Fit(self)

class MainWindow(wx.Frame):

  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title, size=(330, 480))
    self.SetMinSize((330,480))
    self.SetMaxSize((330,480))
    self.setupMenuBar()
    self.setupPanel()
    self.Show(True)

#--
  def setupMenuBar(self):
    self.CreateStatusBar()

    menubar = wx.MenuBar()
    menufile = wx.Menu()

    mnuabout = menufile.Append(wx.ID_ABOUT, '&About', 'about and help')
    mnuexit = menufile.Append(wx.ID_EXIT, 'E&xit', 'close window')

    menubar.Append(menufile, '&File')


    self.Bind(wx.EVT_MENU, self.onAbout, mnuabout)
    self.Bind(wx.EVT_MENU, self.onExit, mnuexit)
    self.Bind(wx.EVT_CLOSE, self.onExit)
    self.SetMenuBar(menubar)
  def setupPanel(self):
#--
    panel = wx.Panel(self, -1,size=(330,480))
    panel.SetBackgroundColour('white')
    #v1
    box = wx.StaticBox(panel,-1,u'抓取设置')
    boxsizerv1 = wx.StaticBoxSizer(box,wx.VERTICAL)
    btnv1 = wx.Button(panel, -1, u'关注用户新作')
    btnv2 = wx.Button(panel, -1, u'综合排行')
    btnv3 = wx.Button(panel, -1, u'插画排行')
    btnv4 = wx.Button(panel, -1, u'漫画排行')
    btnv5 = wx.Button(panel, -1, u'动图排行')

    panel.Bind(wx.EVT_BUTTON, self.OnButton1, btnv1)
    panel.Bind(wx.EVT_BUTTON, self.OnButton2, btnv2)
    panel.Bind(wx.EVT_BUTTON, self.OnButton3, btnv3)
    panel.Bind(wx.EVT_BUTTON, self.OnButton4, btnv4)
    panel.Bind(wx.EVT_BUTTON, self.OnButton5, btnv5)

    boxsizerv1.Add(btnv1, proportion=0, flag=wx.ALL, border=5)
    boxsizerv1.Add(btnv2, proportion=0, flag=wx.ALL, border=5)
    boxsizerv1.Add(btnv3, proportion=0, flag=wx.ALL, border=5)
    boxsizerv1.Add(btnv4, proportion=0, flag=wx.ALL, border=5)
    boxsizerv1.Add(btnv5, proportion=0, flag=wx.ALL, border=5)
    #v2
    boxsizerv2 = wx.BoxSizer(wx.VERTICAL)
    box = wx.StaticBox(panel,-1,u'用户信息')

    boxsizerv3 = wx.StaticBoxSizer(box,wx.VERTICAL)
    boxsizerh2 = wx.BoxSizer(wx.HORIZONTAL)
    boxsizerh3 = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText(panel,-1,u'用户名:')
    self.textfiled1 = wx.TextCtrl(panel, -1, username, size=(76,-1))

    boxsizerh2.Add(text1,proportion=0, flag=wx.ALL, border=5)
    boxsizerh2.Add(self.textfiled1,proportion=0, flag=wx.ALL, border=5)

    text2 = wx.StaticText(panel,-1,u'   密码:')
    self.textfiled2 = wx.TextCtrl(panel, -1, password, style=wx.TE_PASSWORD, size=(76,-1))
    boxsizerh3.Add(text2,proportion=0, flag=wx.ALL, border=5)
    boxsizerh3.Add(self.textfiled2,proportion=0, flag=wx.ALL, border=5)
    boxsizerv3.Add(boxsizerh2)
    boxsizerv3.Add(boxsizerh3)

    box = wx.StaticBox(panel,-1,u'时间设置')
    boxsizerv4 = wx.StaticBoxSizer(box,wx.VERTICAL)

    text1 = wx.StaticText( panel, -1, u'开始时间:')
    self.time1 = masked.TimeCtrl( panel, -1,value=starttime, name="start time",fmt24hr=True, )
    h = self.time1.GetSize().height
    spin1 = wx.SpinButton( panel, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL )
    self.time1.BindSpinButton( spin1 )

    text2 = wx.StaticText( panel, -1, u'结束时间:')
    spin2 = wx.SpinButton( panel, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL )
    self.time2 = masked.TimeCtrl(panel, -1, value=endtime, name="end time", fmt24hr=True,spinButton = spin2)

    grid = wx.FlexGridSizer( cols=2, hgap=10, vgap=5 )
    grid.Add( text1, 0, wx.ALIGN_RIGHT )
    hbox1 = wx.BoxSizer( wx.HORIZONTAL )
    hbox1.Add( self.time1, 0, wx.ALIGN_CENTRE )
    hbox1.Add( spin1, 0, wx.ALIGN_CENTRE )
    grid.Add( hbox1, 0, wx.LEFT )

    grid.Add( text2, 0, wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM )
    hbox2 = wx.BoxSizer( wx.HORIZONTAL )
    hbox2.Add( self.time2, 0, wx.ALIGN_CENTRE )
    hbox2.Add( spin2, 0, wx.ALIGN_CENTRE )
    grid.Add( hbox2, 0, wx.LEFT )
    boxsizerv4.Add(grid)

    box = wx.StaticBox(panel,-1,u'图片大小')
    boxsizerv5 = wx.StaticBoxSizer(box,wx.VERTICAL)
    sampleList = [u'原图', u'中等', u'缩略图']
    self.ch = wx.Choice(panel, -1, size=(135, 27), choices = sampleList)
    self.ch.SetSelection(picsize)
    boxsizerv5.Add(self.ch)


    boxsizerv2.Add(boxsizerv3)
    boxsizerv2.Add(boxsizerv4)
    boxsizerv2.Add(boxsizerv5)


    boxsizerh1 = wx.BoxSizer(wx.HORIZONTAL)
    boxsizerh1.Add((10,20))
    boxsizerh1.Add(boxsizerv1)
    boxsizerh1.Add((40,20))
    boxsizerh1.Add(boxsizerv2)

    text1 = wx.StaticText( panel, wx.ID_ANY, u"图片存放目录:", wx.DefaultPosition, wx.DefaultSize, 0 )

    self.dirPicker = wx.DirPickerCtrl( panel, wx.ID_ANY, picdir, u"选择源文件夹", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
    boxsizerh2 = wx.BoxSizer(wx.HORIZONTAL)
    boxsizerh2.Add(text1, 0, wx.ALL, 10)
    boxsizerh2.Add(self.dirPicker, 0, wx.ALL, 5)

    boxsizerh3 = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText( panel, wx.ID_ANY, u"总大小限制(MB):", wx.DefaultPosition, wx.DefaultSize, 0 )
 #   self.text = wx.TextCtrl(panel, -1, limitroom, (20, 50), (60, -1))

    self.sc = wx.SpinCtrl(panel, -1, "", size=(70, 25))
    self.sc.SetRange(1,2048000000)
    self.sc.SetValue(limitroom)


 #   self.Bind(wx.EVT_SPIN, self.OnSpin, self.spin)
    boxsizerh3.Add((7,10))
    boxsizerh3.Add(text1, 0, wx.ALL, 3)
    boxsizerh3.Add(self.sc, 0, wx.ALL, 0)
#    boxsizerh3.Add(self.spin, 0, wx.ALL, 0)

    text1 = wx.StaticText( panel, wx.ID_ANY, u"开机自动启动:", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.checkbox = wx.CheckBox(panel, -1)
    self.checkbox.SetValue(autoboot)
    boxsizerh3.Add((20,10))
    boxsizerh3.Add(text1, 0, wx.ALL, 3)
    boxsizerh3.Add(self.checkbox, 0, wx.ALL, 4)

    boxsizerh4 = wx.BoxSizer(wx.HORIZONTAL)
    text1 = wx.StaticText( panel, wx.ID_ANY, u"抓取间隔(分):     ", wx.DefaultPosition, wx.DefaultSize, 0 )

    self.sc2 = wx.SpinCtrl(panel, -1, "", size=(70, 25))
    self.sc2.SetRange(1,360)
    self.sc2.SetValue(timeinterval)

    boxsizerh4.Add((7,10))
    boxsizerh4.Add(text1, 0, wx.ALL, 3)
    boxsizerh4.Add(self.sc2, 0, wx.ALL, 0)

    boxsizerh5 = wx.BoxSizer(wx.HORIZONTAL)
    boxsizerh5.Add((20,5))
    btnh0 = wx.Button(panel, -1, u'立刻开始')
    self.Bind(wx.EVT_BUTTON, self.OnButtonBegin, btnh0)
    boxsizerh5.Add(btnh0, proportion=0, flag=wx.ALL, border=5)

    btnh1 = wx.Button(panel, -1, u'确定')
    self.Bind(wx.EVT_BUTTON, self.OnButtonOK, btnh1)
    boxsizerh5.Add(btnh1, proportion=0, flag=wx.ALL, border=5)
    btnh2 = wx.Button(panel, -1, u'取消')
    self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, btnh2)
    boxsizerh5.Add(btnh2, proportion=0, flag=wx.ALL, border=5)


    boxsizerv0 = wx.BoxSizer(wx.VERTICAL)
    boxsizerv0.Add(boxsizerh1)
    boxsizerv0.Add((10,10))
    boxsizerv0.Add(boxsizerh2)
    boxsizerv0.Add((10,10))
    boxsizerv0.Add(boxsizerh3)
    boxsizerv0.Add((10,10))
    boxsizerv0.Add(boxsizerh4)
    boxsizerv0.Add((10,10))
    boxsizerv0.Add(boxsizerh5)


    panel.SetSizer(boxsizerv0)

  def onAbout(self, evt):
      f = open("help.txt", "r")
      msg = f.read()
      f.close()
      dlg = wx.MessageDialog(self, msg, 'About', wx.OK)
      dlg.ShowModal()
      dlg.Destroy()

  def OnButton1(self, evt):
      dlg = TestDialog1(self, -1, u"关注用户", size=(400, 300),
                     style=wx.DEFAULT_DIALOG_STYLE,
                     )

    # this does not return until the dialog is closed.
      val = dlg.ShowModal()
      if val == wx.ID_OK:
          global guanzhu_chahua,guanzhu_manhua,guanzhu_dongtu,guanzhu_shuliang
          guanzhu_chahua = dlg.cb1.IsChecked()
          guanzhu_manhua = dlg.cb2.IsChecked()
          guanzhu_dongtu = dlg.cb3.IsChecked()
          guanzhu_shuliang = dlg.sc.GetValue()

      dlg.Destroy()

  def OnButton2(self, evt):
      dlg = TestDialog2(self, -1, u"综合排行", size=(400, 300),
                     style=wx.DEFAULT_DIALOG_STYLE,
                     )

    # this does not return until the dialog is closed.
      val = dlg.ShowModal()

      if val == wx.ID_OK:
          global zonghe_chahua,zonghe_manhua,zonghe_dongtu,zonghe_jinri,zonghe_benzhou,zonghe_benyue,zonghe_xinren,zonghe_nanxing,zonghe_r18_nanxing,zonghe_r18_meiri,zonghe_r18_meizhou,zonghe_nvxing,zonghe_r18_nvxing,zonghe_r18g,zonghe_yuanchuang,zonghe_shuliang
          zonghe_chahua = dlg.cb1.IsChecked()
          zonghe_manhua = dlg.cb2.IsChecked()
          zonghe_dongtu = dlg.cb3.IsChecked()
          zonghe_jinri = dlg.cb4.IsChecked()
          zonghe_benzhou = dlg.cb5.IsChecked()
          zonghe_benyue = dlg.cb6.IsChecked()
          zonghe_xinren = dlg.cb7.IsChecked()
          zonghe_nanxing = dlg.cb8.IsChecked()
          zonghe_r18_nanxing = dlg.cb9.IsChecked()
          zonghe_r18_meiri = dlg.cb10.IsChecked()
          zonghe_r18_meizhou = dlg.cb11.IsChecked()
          zonghe_nvxing = dlg.cb12.IsChecked()
          zonghe_r18_nvxing = dlg.cb13.IsChecked()
          zonghe_r18g = dlg.cb14.IsChecked()
          zonghe_yuanchuang = dlg.cb15.IsChecked()
          zonghe_shuliang = dlg.sc.GetValue()
      dlg.Destroy()

  def OnButton3(self, evt):
      dlg = TestDialog3(self, -1, u"插画排行", size=(400, 300),
                     style=wx.DEFAULT_DIALOG_STYLE,
                     )

    # this does not return until the dialog is closed.
      val = dlg.ShowModal()

      if val == wx.ID_OK:
          global chahua_jinri,chahua_benzhou,chahua_benyue,chahua_xinren,chahua_r18_meiri,chahua_r18_meizhou,chahua_r18g,chahua_shuliang
          chahua_jinri = dlg.cb1.IsChecked()
          chahua_benzhou = dlg.cb2.IsChecked()
          chahua_benyue = dlg.cb3.IsChecked()
          chahua_xinren = dlg.cb4.IsChecked()
          chahua_r18_meiri = dlg.cb5.IsChecked()
          chahua_r18_meizhou = dlg.cb6.IsChecked()
          chahua_r18g = dlg.cb7.IsChecked()
          chahua_shuliang = dlg.sc.GetValue()
      dlg.Destroy()

  def OnButton4(self, evt):
      dlg = TestDialog4(self, -1, u"漫画排行", size=(400, 300),
                     style=wx.DEFAULT_DIALOG_STYLE,
                     )

    # this does not return until the dialog is closed.
      val = dlg.ShowModal()

      if val == wx.ID_OK:
          global manhua_jinri,manhua_benzhou,manhua_benyue,manhua_xinren,manhua_r18_meiri,manhua_r18_meizhou,manhua_r18g,manhua_shuliang
          manhua_jinri = dlg.cb1.IsChecked()
          manhua_benzhou = dlg.cb2.IsChecked()
          manhua_benyue = dlg.cb3.IsChecked()
          manhua_xinren = dlg.cb4.IsChecked()
          manhua_r18_meiri = dlg.cb5.IsChecked()
          manhua_r18_meizhou = dlg.cb6.IsChecked()
          manhua_r18g = dlg.cb7.IsChecked()
          manhua_shuliang = dlg.sc.GetValue()
      dlg.Destroy()
  def OnButton5(self, evt):
      dlg = TestDialog5(self, -1, u"动图排行", size=(400, 300),
                     style=wx.DEFAULT_DIALOG_STYLE,
                     )

    # this does not return until the dialog is closed.
      val = dlg.ShowModal()

      if val == wx.ID_OK:
          global dongtu_jinri,dongtu_r18_meiri,dongtu_benzhou,dongtu_r18_meizhou,dongtu_shuliang
          dongtu_jinri = dlg.cb1.IsChecked()
          dongtu_r18_meiri = dlg.cb2.IsChecked()
          dongtu_benzhou = dlg.cb3.IsChecked()
          dongtu_r18_meizhou = dlg.cb4.IsChecked()
          dongtu_shuliang = dlg.sc.GetValue()
      dlg.Destroy()

  def OnButtonBegin(self,evt):
      global username,password,starttime,endtime,picsize,picdir,limitroom,timeinterval,autoboot
      username = self.textfiled1.GetValue()
      password = self.textfiled2.GetValue()
      starttime = self.time1.GetValue()
      endtime = self.time2.GetValue()
      picsize = self.ch.GetCurrentSelection()
      picdir = self.dirPicker.GetPath()
      limitroom = self.sc.GetValue()
      timeinterval = self.sc2.GetValue()
      autoboot = self.checkbox.IsChecked()
      apply_global_vars()
      task_bar_ico.begin_work()


  def OnButtonOK(self, evt):
      global username,password,starttime,endtime,picsize,picdir,limitroom,timeinterval,autoboot
      username = self.textfiled1.GetValue()
      password = self.textfiled2.GetValue()
      starttime = self.time1.GetValue()
      endtime = self.time2.GetValue()
      picsize = self.ch.GetCurrentSelection()
      picdir = self.dirPicker.GetPath()
      limitroom = self.sc.GetValue()
      timeinterval = self.sc2.GetValue()
      autoboot = self.checkbox.IsChecked()
      apply_global_vars()
      global showing_frame
      showing_frame = False
      self.Destroy()

  def OnButtonCancel(self, evt):
      global showing_frame
      showing_frame = False
      self.Destroy()

  def onExit(self, evt):
      global showing_frame
      showing_frame = False
      self.Destroy()

showing_frame = False
working_thread_id = 0

def set_global_vars():
    global guanzhu_chahua,guanzhu_manhua,guanzhu_dongtu,guanzhu_shuliang
    global zonghe_chahua,zonghe_manhua,zonghe_dongtu,zonghe_jinri,zonghe_benzhou,zonghe_benyue,zonghe_xinren,zonghe_nanxing,zonghe_r18_nanxing,zonghe_r18_meiri,zonghe_r18_meizhou,zonghe_nvxing,zonghe_r18_nvxing,zonghe_r18g,zonghe_yuanchuang,zonghe_shuliang
    global chahua_jinri,chahua_benzhou,chahua_benyue,chahua_xinren,chahua_r18_meiri,chahua_r18_meizhou,chahua_r18g,chahua_shuliang
    global manhua_jinri,manhua_benzhou,manhua_benyue,manhua_xinren,manhua_r18_meiri,manhua_r18_meizhou,manhua_r18g,manhua_shuliang
    global dongtu_jinri,dongtu_r18_meiri,dongtu_benzhou,dongtu_r18_meizhou,dongtu_shuliang
    global username,password,starttime,endtime,picsize,picdir,limitroom,timeinterval,autoboot
    #全局设置
    username = manager.settings["user_info"]["username"]
    password = manager.settings["user_info"]["password"]
    starttime = manager.settings["time_setting"]["from"]
    endtime = manager.settings["time_setting"]["to"]
    if cmp(manager.settings["image_size"],"large") == 0:
        picsize = 0
    if cmp(manager.settings["image_size"],"px_480mw") == 0:
        picsize = 1
    if cmp(manager.settings["image_size"],"px_128x128") == 0:
        picsize = 2
    picdir = os.path.join(manager.settings["disk_setting"]["root_dir"])
    limitroom = manager.settings["disk_setting"]["max_size"]/(1024*1024)
    timeinterval = manager.settings["time_setting"]["span_mili_second"]/(60000)
    autoboot = manager.settings["auto_boot"]

    #动图设置
    dongtu_shuliang = manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["daily"]["nums"]
    dongtu_jinri = manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["daily"]["todo"]
    dongtu_benzhou = manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["weekly"]["todo"]
    dongtu_r18_meiri = manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["daily_r18"]["todo"]
    dongtu_r18_meizhou = manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["weekly_r18"]["todo"]

    #漫画设置
    manhua_shuliang = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["daily"]["nums"]
    manhua_jinri = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["daily"]["todo"]
    manhua_benzhou = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["weekly"]["todo"]
    manhua_benyue = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["monthly"]["todo"]
    manhua_xinren = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["rookie"]["todo"]
    manhua_r18_meiri = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["daily_r18"]["todo"]
    manhua_r18_meizhou = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["weekly_r18"]["todo"]
    manhua_r18g = manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["r18g"]["todo"]

    #插画设置
    chahua_shuliang = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["daily"]["nums"]
    chahua_jinri = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["daily"]["todo"]
    chahua_benzhou = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["weekly"]["todo"]
    chahua_benyue = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["monthly"]["todo"]
    chahua_xinren = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["rookie"]["todo"]
    chahua_r18_meiri = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["daily_r18"]["todo"]
    chahua_r18_meizhou = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["weekly_r18"]["todo"]
    chahua_r18g = manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["r18g"]["todo"]

    #综合排行设置
    zonghe_shuliang = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["daily"]["nums"]
    zonghe_chahua = manager.settings["crawl_setting"]["ranking"]["all"]["filter_setting"]["illustration"]
    zonghe_manhua = manager.settings["crawl_setting"]["ranking"]["all"]["filter_setting"]["manga"]
    zonghe_dongtu = manager.settings["crawl_setting"]["ranking"]["all"]["filter_setting"]["ugoira"]
    zonghe_jinri = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["daily"]["todo"]
    zonghe_benzhou = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["weekly"]["todo"]
    zonghe_benyue = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["monthly"]["todo"]
    zonghe_xinren = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["rookie"]["todo"]
    zonghe_yuanchuang = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["original"]["todo"]
    zonghe_nanxing = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["male"]["todo"]
    zonghe_nvxing = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["female"]["todo"]
    zonghe_r18_meiri = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["daily_r18"]["todo"]
    zonghe_r18_meizhou = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["weekly_r18"]["todo"]
    zonghe_r18_nanxing = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["male_r18"]["todo"]
    zonghe_r18_nvxing = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["female_r18"]["todo"]
    zonghe_r18g = manager.settings["crawl_setting"]["ranking"]["all"]["type"]["r18g"]["todo"]

    #关注用户设置
    guanzhu_shuliang = manager.settings["crawl_setting"]["following"]["nums"]
    guanzhu_chahua = manager.settings["crawl_setting"]["following"]["filter_setting"]["illustration"]
    guanzhu_manhua = manager.settings["crawl_setting"]["following"]["filter_setting"]["manga"]
    guanzhu_dongtu = manager.settings["crawl_setting"]["following"]["filter_setting"]["ugoira"]

def apply_global_vars():
    global manager
    global guanzhu_chahua,guanzhu_manhua,guanzhu_dongtu,guanzhu_shuliang
    global zonghe_chahua,zonghe_manhua,zonghe_dongtu,zonghe_jinri,zonghe_benzhou,zonghe_benyue,zonghe_xinren,zonghe_nanxing,zonghe_r18_nanxing,zonghe_r18_meiri,zonghe_r18_meizhou,zonghe_nvxing,zonghe_r18_nvxing,zonghe_r18g,zonghe_yuanchuang,zonghe_shuliang
    global chahua_jinri,chahua_benzhou,chahua_benyue,chahua_xinren,chahua_r18_meiri,chahua_r18_meizhou,chahua_r18g,chahua_shuliang
    global manhua_jinri,manhua_benzhou,manhua_benyue,manhua_xinren,manhua_r18_meiri,manhua_r18_meizhou,manhua_r18g,manhua_shuliang
    global dongtu_jinri,dongtu_r18_meiri,dongtu_benzhou,dongtu_r18_meizhou,dongtu_shuliang
    global username,password,starttime,endtime,picsize,picdir,limitroom,timeinterval,autoboot
    #全局设置
    manager.settings["user_info"]["username"] = username
    manager.settings["user_info"]["password"] = password
    manager.settings["time_setting"]["from"] = starttime
    manager.settings["time_setting"]["to"] = endtime
    if picsize == 0:
        manager.settings["image_size"]="large"
    if picsize == 1:
        manager.settings["image_size"]="px_480mw"
    if picsize == 2:
        manager.settings["image_size"]="px_128x128"
    manager.settings["disk_setting"]["root_dir"] = picdir
    manager.settings["disk_setting"]["max_size"] = limitroom*1024*1024
    manager.settings["time_setting"]["span_mili_second"] = timeinterval*60000
    manager.settings["auto_boot"] = autoboot

    #动图设置
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["daily"]["nums"] = dongtu_shuliang
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["daily"]["todo"] = dongtu_jinri
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["weekly"]["nums"] = dongtu_shuliang
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["weekly"]["todo"] = dongtu_benzhou
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["daily_r18"]["nums"] = dongtu_shuliang
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["daily_r18"]["todo"] = dongtu_r18_meiri
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["weekly_r18"]["nums"] = dongtu_shuliang
    manager.settings["crawl_setting"]["ranking"]["ugoira"]["type"]["weekly_r18"]["todo"] = dongtu_r18_meizhou

    #漫画设置
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["daily"]["nums"] = manhua_shuliang
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["daily"]["todo"] = manhua_jinri
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["weekly"]["nums"] = manhua_shuliang
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["weekly"]["todo"] = manhua_benzhou
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["monthly"]["nums"] = manhua_shuliang
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["monthly"]["todo"] = manhua_benyue
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["rookie"]["nums"] = manhua_shuliang
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["rookie"]["todo"] = manhua_xinren
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["daily_r18"]["nums"] = manhua_shuliang
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["daily_r18"]["todo"] = manhua_r18_meiri
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["weekly_r18"]["nums"] = manhua_shuliang
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["weekly_r18"]["todo"] = manhua_r18_meizhou
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["r18g"]["nums"] = manhua_shuliang
    manager.settings["crawl_setting"]["ranking"]["manga"]["type"]["r18g"]["todo"] = manhua_r18g

    #插画设置
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["daily"]["nums"] = chahua_shuliang
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["daily"]["todo"] = chahua_jinri
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["weekly"]["nums"] = chahua_shuliang
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["weekly"]["todo"] = chahua_benzhou
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["monthly"]["nums"] = chahua_shuliang
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["monthly"]["todo"] = chahua_benyue
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["rookie"]["nums"] = chahua_shuliang
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["rookie"]["todo"] = chahua_xinren
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["daily_r18"]["nums"] = chahua_shuliang
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["daily_r18"]["todo"] = chahua_r18_meiri
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["weekly_r18"]["nums"] = chahua_shuliang
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["weekly_r18"]["todo"] = chahua_r18_meizhou
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["r18g"]["nums"] = chahua_shuliang
    manager.settings["crawl_setting"]["ranking"]["illust"]["type"]["r18g"]["todo"] = chahua_r18g

    #综合排行设置
    manager.settings["crawl_setting"]["ranking"]["all"]["filter_setting"]["illustration"] = zonghe_chahua
    manager.settings["crawl_setting"]["ranking"]["all"]["filter_setting"]["manga"] = zonghe_manhua
    manager.settings["crawl_setting"]["ranking"]["all"]["filter_setting"]["ugoira"] = zonghe_dongtu
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["daily"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["daily"]["todo"] = zonghe_jinri
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["weekly"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["weekly"]["todo"] = zonghe_benzhou
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["monthly"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["monthly"]["todo"] = zonghe_benyue
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["rookie"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["rookie"]["todo"] = zonghe_xinren
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["original"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["original"]["todo"] = zonghe_yuanchuang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["male"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["male"]["todo"] = zonghe_nanxing
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["female"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["female"]["todo"] = zonghe_nvxing
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["daily_r18"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["daily_r18"]["todo"] = zonghe_r18_meiri
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["weekly_r18"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["weekly_r18"]["todo"] = zonghe_r18_meizhou
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["male_r18"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["male_r18"]["todo"] = zonghe_r18_nanxing
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["female_r18"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["female_r18"]["todo"] = zonghe_r18_nvxing
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["r18g"]["nums"] = zonghe_shuliang
    manager.settings["crawl_setting"]["ranking"]["all"]["type"]["r18g"]["todo"] = zonghe_r18g

    #关注用户设置
    manager.settings["crawl_setting"]["following"]["nums"] = guanzhu_shuliang
    manager.settings["crawl_setting"]["following"]["filter_setting"]["illustration"] = guanzhu_chahua
    manager.settings["crawl_setting"]["following"]["filter_setting"]["manga"] = guanzhu_manhua
    manager.settings["crawl_setting"]["following"]["filter_setting"]["ugoira"] = guanzhu_dongtu

    manager.apply_settings()

def on_show_window(event):
    global showing_frame,frame
    if showing_frame:
        return
    set_global_vars()
    frame = MainWindow(None, u'抓取选项')
    showing_frame = True

def on_exit(event):
    global manager,frame,task_bar_ico,showing_frame
    if manager.is_working:
        os.popen("kill -9 "+str(working_thread_id))
    if showing_frame:
        wx.CallAfter(frame.Destroy)
    wx.CallAfter(task_bar_ico.Destroy)

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskTimer(wx.Timer):
    def __init__(self):
        wx.Timer.__init__(self)
    def Notify(self):
        if not manager.is_working:
            print "begin working"
            thread.start_new_thread(manager.work,())

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TIMER, self.watch_time)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK,on_show_window)
        self.timer = wx.Timer(self)
        self.timer.Start(60000)
        self.task_timer = TaskTimer()
        self.begin_working = False

    def begin_work(self):
        self.task_timer.Start(manager.settings["time_setting"]["span_mili_second"])
        print "begin work"
        self.begin_working = True
        self.task_timer.Notify()


    def watch_time(self,evt):
        cur_time = datetime.now().time()
        begin_time = datetime.strptime(manager.settings["time_setting"]["from"],"%H:%M:%S").time()
        end_time = datetime.strptime(manager.settings["time_setting"]["to"],"%H:%M:%S").time()
        if cur_time > begin_time and cur_time < end_time:
            if not self.begin_working:
                self.task_timer.Start(manager.settings["time_setting"]["span_mili_second"])
                print "begin work"
                self.begin_working = True
        else:
            if self.begin_working:
                self.task_timer.Stop()
                print "end work"
                self.begin_working = False

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, u'设置', on_show_window)
        menu.AppendSeparator()
        create_menu_item(menu, u'退出', on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path,wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon, TRAY_TOOLTIP)


def check_runnable():
    global manager
    if not manager.settings["runnable"]:
        on_show_window(None)



app = wx.App(False)

process_name = sys.argv[0]
print process_name
WMI = win32com.client.GetObject('winmgmts:')
processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
if len(processCodeCov) > 0:
    wx.MessageBox(u"程序已在运行",u"提示",wx.OK|wx.ICON_INFORMATION)
    exit(0)

manager = Manager()
task_bar_ico = TaskBarIcon()
check_runnable()
app.MainLoop()
