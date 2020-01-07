# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import inspect
import ctypes
import sys
import threading
from test3 import *
import wx.adv
from config_ark import ChapterCTE,ChapterETC
from add_gui import MyFrame1 as MyFrame2
###########################################################################
## Class MyFrame1
###########################################################################
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        return 0
    elif res != 1:
    # """if it returns a number greater than one, you're in trouble,
    # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    return 1

def stop_thread(thread):
    return _async_raise(thread.ident, SystemExit)

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


class RunThread(threading.Thread):
    def __init__(self,zhuxian_num,guanqia_infor,yuanshi_num,shuatu_num,thresh,handle):
        self.zhuxian_num = int(zhuxian_num)
        #self.chapter = guanqia_infor[0]
        self.guanqia_infor = guanqia_infor
        self.shuatu_num = shuatu_num
        if yuanshi_num=="No！":
            globalvar.set_yuanshi(0)
        elif yuanshi_num=="仅使用体力药":
            globalvar.set_yuanshi(1)
        elif yuanshi_num=="使用源石":
            globalvar.set_yuanshi(2)
        globalvar.set_thresh_pic(float(thresh)/100)
        self.handle = handle
        threading.Thread.__init__(self)
    def run(self):
        #print("当前选择关卡{}".format())
        temp_zhuxian = zx_1_11(self.handle, self.zhuxian_num)
        signal = 0
        try:
            #verified at 2019-9-3
            #verified at 2019-10-12
            #改变关卡命名规则
            chapter = self.guanqia_infor.split('|')[0]
            if chapter in ['HD']:
                temp_class = Shark_Event(self.handle, num=self.shuatu_num, guanqia=self.guanqia_infor)  # 类实例化，num为刷本次数，guanqia为刷图类型，仅支持GT2-6
                temp_class.start()
            else:
                temp_class = Zhuxian(self.handle, num=self.shuatu_num, guanqia=self.guanqia_infor)
                temp_class.start()
        except config_ark.ExitError:
            temp_zhuxian.start()
        except:
            signal = 1

        if signal==0:
            temp_zhuxian.start()
        print("脚本运行完成")


class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(290, 430), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SIZE1 = (100,30)


        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)



        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"总章选择", (10,15), (100,25), 0)
        self.m_staticText1.Wrap(-1)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"子类选择", (100,15), (100,25), 0)
        self.m_staticText2.Wrap(-1)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"关卡选择", (180,15),(100,25) , 0)
        self.m_staticText3.Wrap(-1)


        tmp1 = list(config_ark.guanqia_pic.keys())
        tmp2 = list(config_ark.huodong_pic.keys())
        tmp_guanqia = tmp1 + tmp2
        index = 0
        for i in range(len(tmp_guanqia)):
            tmp_str = tmp_guanqia[index]
            if "|" in tmp_str:
                if "1-11" in tmp_str or "_confirm" in tmp_str:
                    tmp_guanqia.remove(tmp_str)
                    index -= 1
            else:
                tmp_guanqia.remove(tmp_str)
                index -= 1
            index += 1


        self.guanqia_dict = {'主线':{},'物资筹备':{},'芯片获取':{},'活动':{}}
        for i in tmp_guanqia:
            tmp_split = i.split('|')
            if len(tmp_split)!=3:
                continue
            total_class = tmp_split[0]
            map_total_class = ChapterETC(total_class)
            chapter = tmp_split[1]
            name = tmp_split[2]
            if chapter in self.guanqia_dict[map_total_class]:
                self.guanqia_dict[map_total_class][chapter].append(name)
            else:
                self.guanqia_dict[map_total_class][chapter] = [name]

            #self.guanqia_dict[self._ChapterETC(chapter)].append(name)

        self.event_choise = wx.Choice(self, wx.ID_ANY, (5,40), (70,30), list(self.guanqia_dict.keys()), 0)
        self.event_choise.SetSelection(0)
        self.event_choise.Bind(wx.EVT_CHOICE,self.Choice1Selected)

        choise2_dict = list(self.guanqia_dict[list(self.guanqia_dict.keys())[0]].keys())
        self.event_choise2 = wx.Choice(self, wx.ID_ANY, (95,40), (70,30), choise2_dict, 0)
        self.event_choise2.SetSelection(0)
        self.event_choise2.Bind(wx.EVT_CHOICE,self.Choice2Selected)

        choise3_dict = self.guanqia_dict[list(self.guanqia_dict.keys())[0]][choise2_dict[0]]
        self.event_choise3 = wx.Choice(self, wx.ID_ANY, (175,40), (70,30), choise3_dict, 0)
        self.event_choise3.SetSelection(0)
        #
        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"理智万岁", (10,90), (100,25), 0)
        self.m_staticText4.Wrap(-1)

        self.num_label = wx.StaticText(self, wx.ID_ANY, u"刷图次数",(100,90), (100,25), 0)
        self.num_label.Wrap(-1)

        self.thresh_label = wx.StaticText(self, wx.ID_ANY, u"识图阈值", (185,90), (100,25), 0)
        self.thresh_label.Wrap(-1)
        #
        yuanshi_choiceChoices = [u"No！", u"仅使用体力药", u"使用源石"]
        self.yuanshi_choice = wx.Choice(self, wx.ID_ANY, (5,120), (80,25), yuanshi_choiceChoices, 0)
        self.yuanshi_choice.SetSelection(0)

        self.num = wx.TextCtrl(self, wx.ID_ANY, u"20", (100,120), (40,25), 0)
        self.num.SetMaxLength(0)

        self.thresh = wx.Slider(self, wx.ID_ANY, 85, 60, 100, (160,120), (100,25),
                                wx.SL_HORIZONTAL | wx.SL_LABELS)

        self.label1 = wx.StaticText(self, wx.ID_ANY, u"关卡结束后1-11主线次数", (10,170), (100,25), 0)
        self.label1.Wrap(-1)

        zhuxian_numChoices = [u"0", u"1", u"2", u"3", u"4", u"5"]
        self.zhuxian_num = wx.Choice(self, wx.ID_ANY, (5,200), (40,25), zhuxian_numChoices, 0)
        self.zhuxian_num.SetSelection(5)
        #
        #
        #
        self.drag_speed_label = wx.StaticText(self, wx.ID_ANY, u"拖拽速度", (185,170), (100,25), 0)
        self.drag_speed_label.Wrap(-1)

        self.drag_speed = wx.Slider(self, wx.ID_ANY, 20, 5, 30, (165,200), (100,25),
                                    wx.SL_HORIZONTAL | wx.SL_INVERSE)
        #
        #
        #
        self.start = wx.Button(self, wx.ID_ANY, u"开始", (5,230), (90,35), 0)
        self.end = wx.Button(self, wx.ID_ANY, u"停止", (170,230), (90,35), 0)

        self.infor = wx.TextCtrl(self, wx.ID_ANY, u"", (5,270), (255,90), wx.TE_MULTILINE|wx.TE_READONLY)
        self.infor.SetMaxLength(200)
        #self.infor.Enable(False)
        self.infor.SetMinSize(wx.Size(-1, 80))
        self.infor.SetMaxSize(wx.Size(-1, 400))
        sys.stdout = RedirectText(self.infor)
        self.infor.Bind(wx.EVT_TEXT_MAXLEN,self.TextClear)
        self.m_hyperlink1 = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, u"使用说明", u"https://github.com/vertuer/script_arknight",
                                                 (110,365), (50,30), wx.adv.HL_DEFAULT_STYLE)



        #Connect Events
        self.start.Bind(wx.EVT_BUTTON, self.ScriptBegin)
        self.end.Bind(wx.EVT_BUTTON, self.ScriptEnd)
        #初始化操作
        handle = get_handle([1920, 1080])  # 获取模拟器窗体句柄
        if handle == -1:
            wx.MessageBox("未检测到夜神模拟器,请重新启动", "提示", wx.OK | wx.ICON_INFORMATION, parent=self)
            wx.Exit()
        self.handle = handle
    def __del__(self):
        pass
    def TextClear(self,event):
        self.infor.Clear()
    def Choice1Selected(self,event):
        #dealing when choice1 is selected
        tmp_items = list(self.guanqia_dict[self.event_choise.GetStringSelection()].keys())
        self.event_choise2.SetItems(tmp_items)
        if tmp_items!=[]:
            self.event_choise2.SetSelection(0)
            self.event_choise3.SetItems(self.guanqia_dict[self.event_choise.GetStringSelection()][self.event_choise2.GetStringSelection()])
            self.event_choise3.SetSelection(0)
        else:
            self.event_choise3.Clear()
    def Choice2Selected(self,event):
        #dealing when choice2 is selected
        self.event_choise3.SetItems(self.guanqia_dict[self.event_choise.GetStringSelection()][self.event_choise2.GetStringSelection()])
        self.event_choise3.SetSelection(0)
    # Virtual event handlers, overide them in your derived class
    def ScriptBegin(self, event):
        def _get_full_name(total_class,chapter,name):
            return ChapterCTE(total_class) + "|" + chapter + "|" + name
        if self.start.GetLabel()=="开始":
            try:
                temp_num = int(self.num.GetValue())
            except:
                wx.MessageBox("战斗次数请输入数字！！", "提示", wx.OK | wx.ICON_INFORMATION, parent=self)
                self.num.Clear()
                return
            globalvar.set_drag_speed(int(self.drag_speed.GetValue()))
            self.start.Enable(False)
            self.end.Enable(True)
            self.start.SetLabel("正在运行中")
            total_class = self.event_choise.GetStringSelection() #'主线'
            chapter = self.event_choise2.GetStringSelection()  # '第一章'
            name = self.event_choise3.GetStringSelection()   #"1-7'
            t = RunThread(self.zhuxian_num.GetStringSelection(),_get_full_name(total_class,chapter,name),self.yuanshi_choice.GetStringSelection(),temp_num,self.thresh.GetValue(),self.handle)
            self.thread_id = t
            #self.event_choise.GetCurrentSelection()
            #t.run() #only for test
            t.start()
            self.end.Enable(True)
            #self.start.SetLabel("开始")
            #self.start.Enable(True)
        elif self.start.GetLabel()=="暂停":
            pass
            #pass 还不会

    def ScriptEnd(self, event):
        stop_thread(self.thread_id)
        self.start.Enable(True)
        self.end.Enable(False)
        self.start.SetLabel("开始")


class SubclassDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '请选择脚本功能',
                           size=(300, 100))
        okButton = wx.Button(self, wx.ID_OK, "脚本挂机", pos=(15, 15))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, "脚本关卡管理",
                                 pos=(115, 15))

class Myapp(wx.App):
    def __init__(self):
        #self.qwe = 123
        wx.App.__init__(self,redirect=False)

    def OnClose(self,event):
        self.ExitMainLoop()

    def OnInit(self):
        #print(self.qwe)
        self.frame1 = MyFrame1(parent=None)
        self.frame2 = MyFrame2(parent=None)
        self.frame1.Bind(wx.EVT_CLOSE,self.OnClose)
        self.frame2.Bind(wx.EVT_CLOSE,self.OnClose)
        dialog = SubclassDialog()
        result = dialog.ShowModal()
        #dialog.Bind(wx.EVT_CLOSE,self.OnClose)
        dialog.Destroy()
        if result == wx.ID_OK:
            config_ark.pic_load_ram()  # 将配置文件中的图像载入内存
            #self.SetTopWindow(self.frame1)
            self.frame1.Show()

        elif result == wx.ID_CANCEL:
            #self.SetTopWindow(self.frame2)
            self.frame2.Show()



        #self.SetTopWindow(self.frame1)
        return True
if __name__ == "__main__":
    #just for test
    app = Myapp()
    app.MainLoop()
    #app.OnExit()
    # handle = function_ark.get_handle()
    # pic_load_ram()
    # temp = zx_1_11(handle,2)
    # temp.start()
    #
    # origin_pic = "./ark_images/unprocessed/1-11/1.png"
    # origin_pic = Image.open(origin_pic)
    # origin_pic = origin_pic.convert("RGB")
    # img_temp = "./ark_images/1-11/1.png"
    # img_temp = Image.open(img_temp)
    # temp_im = img_temp.convert("RGB")
    # width = int(1920 / 1920 * temp_im.size[0])
    # height = int(1080 / 1080 * temp_im.size[1])
    # temp_im = temp_im.resize((width, height), Image.ANTIALIAS)
    # position = function_ark.pic_locate(np.array(temp_im),np.array(origin_pic),0.8,True,True)
    # handle = get_handle()
    # position = function_ark.pic_position(handle,np.array(temp_im))


