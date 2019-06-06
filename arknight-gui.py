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
import time
from test3 import *
import wx.adv
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
        raise ValueError("invalid thread id")
    elif res != 1:
    # """if it returns a number greater than one, you're in trouble,
    # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


class RunThread(threading.Thread):
    def __init__(self,guanqia_infor,yuanshi_num,shuatu_num,thresh,handle):
        self.guanqia_infor = guanqia_infor
        self.shuatu_num = shuatu_num
        if yuanshi_num=="No！":
            config_ark.YUANSHI = 0
        else:
            config_ark.YUANSHI = int(yuanshi_num)
        config_ark.THRESH_PIC = float(thresh)/100
        self.handle = handle
        threading.Thread.__init__(self)
    def run(self):
        temp_class = Shark_Event(self.handle, num=self.shuatu_num, guanqia=self.guanqia_infor)  # 类实例化，num为刷本次数，guanqia为刷图类型，仅支持GT2-6
        temp_class.start()
        print("脚本运行完成")


class MyFrame1(wx.Frame):

    def __init__(self, parent):


        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(327, 456), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(2, 2, 0, 0)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"关卡选择", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        gSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"碎石万岁", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gSizer1.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        event_choiseChoices = [u"GT2", u"GT3", u"GT4", u"GT5", u"GT6"]
        self.event_choise = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, event_choiseChoices, 0)
        self.event_choise.SetSelection(0)
        gSizer1.Add(self.event_choise, 0, wx.ALL, 5)

        yuanshi_choiceChoices = [u"No！", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10"]
        self.yuanshi_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, yuanshi_choiceChoices, 0)
        self.yuanshi_choice.SetSelection(0)
        gSizer1.Add(self.yuanshi_choice, 0, wx.ALL, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        gSizer4 = wx.GridSizer(2, 2, 0, 0)

        self.num_label = wx.StaticText(self, wx.ID_ANY, u"刷图次数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.num_label.Wrap(-1)
        gSizer4.Add(self.num_label, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.thresh_label = wx.StaticText(self, wx.ID_ANY, u"识图阈值", wx.DefaultPosition, wx.DefaultSize, 0)
        self.thresh_label.Wrap(-1)
        gSizer4.Add(self.thresh_label, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.num = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.num.SetMaxLength(0)
        gSizer4.Add(self.num, 0, wx.ALL, 5)

        self.thresh = wx.Slider(self, wx.ID_ANY, 80, 60, 100, wx.DefaultPosition, wx.DefaultSize,
                                wx.SL_HORIZONTAL | wx.SL_LABELS)
        gSizer4.Add(self.thresh, 0, wx.ALL, 5)

        bSizer1.Add(gSizer4, 0, wx.EXPAND, 5)

        gSizer3 = wx.GridSizer(1, 2, 0, 0)

        self.start = wx.Button(self, wx.ID_ANY, u"开始", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.start, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        self.end = wx.Button(self, wx.ID_ANY, u"停止", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.end, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer1.Add(gSizer3, 0, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.infor = wx.TextCtrl(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        self.infor.SetMaxLength(0)
        self.infor.Enable(False)
        sys.stdout = RedirectText(self.infor)
        self.infor.SetMinSize(wx.Size(-1, 80))
        self.infor.SetMaxSize(wx.Size(-1, 400))

        bSizer6.Add(self.infor, 0, wx.ALL | wx.EXPAND, 5)

        self.m_hyperlink1 = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, u"使用说明", u"https://github.com/vertuer/script_arknight",
                                             wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE)
        bSizer6.Add(self.m_hyperlink1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer1.Add(bSizer6, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.start.Bind(wx.EVT_BUTTON, self.ScriptBegin)
        self.end.Bind(wx.EVT_BUTTON, self.ScriptEnd)

        #初始化操作
        handle = get_handle([1920, 1080])  # 获取模拟器窗体句柄
        if handle == -1:
            wx.MessageBox("未检测到夜神模拟器,请重新启动", "提示", wx.OK | wx.ICON_INFORMATION, parent=self)
            wx.Exit()
        self.handle = handle
        pic_load_ram()  # 将配置文件中的图像载入内存

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def ScriptBegin(self, event):
        if self.start.GetLabel()=="开始":
            try:
                temp_num = int(self.num.GetValue())
            except:
                wx.MessageBox("战斗次数请输入数字！！", "提示", wx.OK | wx.ICON_INFORMATION, parent=self)
                self.num.Clear()
                return

            self.start.Enable(False)
            self.end.Enable(True)
            self.start.SetLabel("正在运行中")
            t = RunThread(self.event_choise.GetStringSelection(),self.yuanshi_choice.GetStringSelection(),temp_num,self.thresh.GetValue(),self.handle)
            self.thread_id = t
            self.event_choise.GetCurrentSelection()
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

class Myapp(wx.App):
    def __init__(self):
        self.qwe = 123
        wx.App.__init__(self,redirect=False)


    def OnInit(self):
        print(self.qwe)
        self.frame = MyFrame1(parent=None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
if __name__ == "__main__":

    app = Myapp()
    app.MainLoop()