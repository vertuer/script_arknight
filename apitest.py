import win32gui
import win32ui
import win32con
import win32api
import time
from ctypes import windll
import function
import pyocr
from PIL import Image
import numpy as np
import re
import os
from basic_function import *
from function import *
def qwe123():
    print('123')

def qwe789():
    print('124')

number = '123'
globals().get('qwe{}'.format(number))()
print('123')


# def get_allwindow():
#     win32gui.EnumWindows(_MyCallback, lambda handle: handle.append(handle))
# handle = win32gui.FindWindow(None,'腾讯手游助手【标准引擎】')
# win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
# get_allwindow()
# win32gui.CloseWindow(handle)
# print('233')

# def kuaixiu_function(thresh = 1000):
#     while(1):
#         time.sleep(1)
#         t =[]
#         im = np.asarray(Image.open('./pics/ocr/6.png'))
#         position = pic_locate(config.pic_confirm['kuaisuxiufu'], im, 0.8, True, rgb_bool=False)
#         if position!=None:
#             for i in position:
#                 w = int(i['result'][0])
#                 h = int(i['result'][1])
#                 im = im[h-70:h-40,w-60:w+60]
#                 im = Image.fromarray(im)
#                 result = ocr(im)
#                 if len(result)!=6:
#                     break
#                 elif int(result)>thresh:
#                     while(1):
#                         mouse_click(handle,i)
#                         if confirm_where(handle,'kuaixiu_confirm',False):
#                             break
#                     mouse_click(handle,config.zhujiemian_houqin_confirm)
handlelist = []
win32gui.EnumWindows(lambda hWnd, param: param.append([hWnd,
                                                       win32gui.GetClassName(hWnd),
                                                       win32gui.GetWindowText(hWnd)])
                                                       if win32gui.GetWindowText(hWnd)=='腾讯手游助手【标准引擎】' else None, handlelist)
win32gui.EnumWindows(lambda hWnd, param: param.append([hWnd,
                                                       win32gui.GetClassName(hWnd),
                                                       win32gui.GetWindowText(hWnd)])
                                                       , handlelist)
win = win32gui.FindWindow(None,'夜神模拟器')
# win = win32gui.GetDesktopWindow()position[0]
# show_window(win)
# im = prtsc(win)
# im.show()
# hide_window(win)
# win = 396158
hWndChildList=[]
win32gui.EnumChildWindows(win, lambda hWnd, param: param.append([hWnd
                                                                ,win32gui.GetClassName(hWnd)
                                                                ,win32gui.GetWindowText(hWnd)])
                                                                if win32gui.GetWindowText(hWnd) == 'ScreenBoardClassWindow' else None, hWndChildList)
handle = hWndChildList[0][0]
im = prtsc(handle)
# im = np.asarray(Image.open('./pics/ocr/13.png'))
position = pic_locate(config.pic_confirm['3zhanyi'], im, 0.6,False, rgb_bool=False)
if position != None:
    for i in position:
        w = int(i['result'][0])
        h = int(i['result'][1])
        im = im[h - 70:h - 40, w - 60:w + 60]
        result = ocr(im)
        if len(result) != 6:
            break
        elif int(result) > 1000:
            count = count + 1
# im = prtsc(win)
# function.confirm_where(win,'chaijie',True)
# (a,b,c,d) = win32gui.GetClientRect(win)


kuaixiu_function(1000)


# tools = pyocr.get_available_tools()
# b = Image.open('./pics/ocr/2.png')
# b = b.convert('L')
# b = np.asarray(b)
# # b =b.resize((120,40))
# b = Image.fromarray(b)
# a =tools[0].image_to_string(b,lang='eng')
# time.sleep(1)
# win32gui.SetForegroundWindow(win)
# mouse_click(win,288,364)
print('233')
