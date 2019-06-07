import win32con,win32gui,win32ui
import time
from PIL import Image
import numpy as np
import aircv
# import skimage.io as io
# import re
#import pyocr
import globalvar
# def ocr(im,mode='time'): #input PIL image
#     #ocr识别
#     im = Image.fromarray(im)
#     tools = pyocr.get_available_tools()
#     b = im.convert('L')
#     a = tools[0].image_to_string(b, lang='eng')
#     if mode =='time':
#         a = re.sub('\D','',a)
#     return a

def pic_locate(pic_match,pic_origin,thresh,findall=True,rgb_bool=True):  #pic_match is the dir path, pic_origin is the data array
    """

    :param pic_match:  源图像路径或图像数组
    :param pic_origin:  背景图像，ndarray
    :param thresh:      阈值，数值
    :param findall:     true 为寻找全部匹配图像，false为只返回一个
    :param rgb_bool:    true为匹配颜色，false为不匹配颜色
    :return:
    """
    if(isinstance(pic_match,str)):      #若为路径，则根据当前分辨率动态调整实际对比图像
        pic_test = Image.open(pic_match,'r')
        resolution = globalvar.get_window_resolution()
        max_resolution = globalvar.get_max_resolution()
        width = int(resolution[0] / max_resolution[0] * pic_test.size[0])
        height = int(resolution[1] / max_resolution[1] * pic_test.size[1])
        pic_test = np.array(pic_test.resize((width, height), Image.ANTIALIAS))
    elif(isinstance(pic_match,np.ndarray)):
        pic_test = pic_match
    if findall:
        position = aircv.find_all_template(pic_origin,pic_test,thresh,rgb=rgb_bool)
    else:
        position = aircv.find_template(pic_origin, pic_test, thresh,rgb=rgb_bool)
    # C = np.fft.ifft2(np.fft.fft2(pic_origin)*fftpack.fft2(pic_match_path,(888,1435,3)))
    return position

def hide_window(handle):
    #最小化窗口
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,win32con.SC_MINIMIZE,0)
    # win32gui.SendMessage(handle, win32con.WM_CLOSE,0)

def get_cursor(handle):
    #返回鼠标位置，相对窗体位置
    [x,y] = win32gui.GetCursorPos()
    return x,y

def pos(x,y):
    #鼠标位置整合，32位整数型
    return y<<16|x

def mouse_click(handle,xy):
    #模拟鼠标点击，
    x = int(xy[0])
    y = int(xy[1])
    # x,y = win32gui.ScreenToClient(handle,(x,y))
    win32gui.SendMessage(handle,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON, pos(x,y))
    # win32gui.PostMessage(handle,win32con.WM_LBUTTONDBLCLK,win32con.MK_LBUTTON, win32api.MAKELONG(x,y))
    time.sleep(0.1)
    # win32gui.SendMessage(handle, win32con.WM_MOUSELEAVE, win32con.MK_LBUTTON, pos(x,y))
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP,0, pos(x,y))

def mouse_scroll(handle):
    #模拟鼠标滚轮
    win32gui.SendMessage(handle,win32con.WM_MBUTTONDOWN,win32con.MK_MBUTTON, 0)
    time.sleep(0.1)
    win32gui.SendMessage(handle, win32con.WM_MBUTTONUP,0, 0)

def mouse_drag(handle,xy,speed):
    #模拟鼠标拖拽
    # win32gui.PostMessage(handle,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,pos(x,y))
    # win32gui.SetCapture(handle)
    x,y = int(xy[0][0]),int(xy[0][1])
    x_move,y_move = int(xy[1][0]),int(xy[1][1])
    win32gui.PostMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos(x, y))
    win32gui.SendMessage(handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos(x, y))
    for i in range(speed):
        time.sleep(0.05)
        win32gui.PostMessage(handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos(x+int((x_move-x)/speed*(i+1)), y+int((y_move-y)/speed*(i+1))))
    # win32gui.PostMessage(handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos(x_move, y_move+117))
    # win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos(x, y))
    time.sleep(0.5)
    win32gui.PostMessage(handle, win32con.WM_LBUTTONUP, 0, pos(x_move, y_move))
    # win32gui.SendMessage(handle,win32con.WM_MOUSEMOVE,win32con.MK_LBUTTON,pos(x,y))
    # win32gui.SendMessage(handle,win32con.WM_MOUSEMOVE,win32con.MK_LBUTTON,pos(x_move,y_move))
    # time.sleep(0.1)
    # win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, 0, pos(x_move, y_move))

def show_window(handle):
    #最大化窗口
    if win32gui.IsIconic(handle):
        win32gui.SendMessage(handle,win32con.WM_SYSCOMMAND,win32con.SC_RESTORE,0)
    time.sleep(0.2)

def TestEnumWindows():
    def _MyCallback(hwnd, extra):
        windows = extra
        temp = []
        temp.append(hex(hwnd))
        temp.append(win32gui.GetClassName(hwnd))
        temp.append(win32gui.GetWindowText(hwnd))
        windows[hwnd] = temp
    windows = {}
    win32gui.EnumWindows(_MyCallback, windows)

    for item in windows:
        print(windows[item])
    return windows

def prtsc(handle): #returns the im of the printed software
    left, top, right, bot = win32gui.GetWindowRect(handle)
    w = right - left
    h = bot - top
    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwndDC = win32gui.GetWindowDC(handle)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    # # 截图至内存设备描述表
    img_dc = mfcDC
    mem_dc = saveDC
    mem_dc.BitBlt((0, 0), (w, h), img_dc, (0, 0), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    return np.array(im)

def save_im(handle,file_name):
    im = prtsc(handle)
    temp_im = Image.fromarray(im)
    temp_im.save(file_name)
    print("img saved to {}\n".format(file_name))


def get_handle(resolution=[1920,1080]): #now only the 夜神 is supported
    handlelist = []
    win32gui.EnumWindows(lambda hWnd, param: param.append([hWnd,
                                                           win32gui.GetClassName(hWnd),
                                                           win32gui.GetWindowText(hWnd)])
                         , handlelist)
    win = win32gui.FindWindow(None, '夜神模拟器')
    if win==0:
        win = win32gui.FindWindow(None, 'MuMu模拟器')
        hWndChildList = []
        win32gui.EnumChildWindows(win, lambda hWnd, param: param.append([hWnd
                                                                            , win32gui.GetClassName(hWnd)
                                                                            , win32gui.GetWindowText(hWnd)])
        if win32gui.GetWindowText(hWnd) in ['NemuPlayer']  else None, hWndChildList)
        try:
            win = hWndChildList[0][0]
        except:
            return -1

    else:
        hWndChildList = []
        win32gui.EnumChildWindows(win, lambda hWnd, param: param.append([hWnd
                                                                            , win32gui.GetClassName(hWnd)
                                                                            , win32gui.GetWindowText(hWnd)])
        if win32gui.GetWindowText(hWnd) in ['QWidgetClassWindow','ScreenBoardClassWindow']  else None, hWndChildList)
        try:
            win = hWndChildList[0][0]
        except:
            return -1
    rect = win32gui.GetWindowRect(win)
    globalvar.set_window_resolution([rect[2]-rect[0],rect[3]-rect[1]])
    print("当前窗体大小为{}x{}".format(rect[2]-rect[0],rect[3]-rect[1]))
    if (rect[2] - rect[0])==resolution[0] and (rect[3] - rect[1])==resolution[1]:
        pass
    else:
        print('resolution isn\'t {}p'.format(resolution[1]))
    return win
    # if (rect[2]-rect[0])!=resolution[0] or (rect[3]-rect[1])!=resolution[1]:
    #     raise Exception('resolution isn\'t {}p'.format(resolution[1]))