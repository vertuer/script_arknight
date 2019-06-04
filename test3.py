import numpy as np
from PIL import Image
import os
import time
import config_ark
import scipy.fftpack as fftpack
import aircv
from skimage import io,transform
from basic_function import pic_locate,prtsc,get_handle,mouse_scroll
import function_ark
import globalvar
def pic_load_ram():
    get_handle()
    for keys,pic_path in config_ark.pic_confirm.items():
        temp_im = Image.open(pic_path)
        temp_im = temp_im.convert("RGB")
        window_resolution = globalvar.get_window_resolution()
        max_resolution = globalvar.get_max_resolution()
        width = int(window_resolution[0] / max_resolution[0] * temp_im.size[0])
        height = int(window_resolution[1] / max_resolution[1] * temp_im.size[1])
        temp_im = temp_im.resize((width, height), Image.ANTIALIAS)
        config_ark.pic_confirm[keys] = np.array(temp_im)

    for keys, pic_path in config_ark.pic_huodong.items():
        temp_im = Image.open(pic_path)
        temp_im = temp_im.convert("RGB")
        window_resolution = globalvar.get_window_resolution()
        max_resolution = globalvar.get_max_resolution()
        width = int(window_resolution[0] / max_resolution[0] * temp_im.size[0])
        height = int(window_resolution[1] / max_resolution[1] * temp_im.size[1])
        temp_im = temp_im.resize((width, height), Image.ANTIALIAS)
        config_ark.pic_huodong[keys] = np.array(temp_im)

    for keys, pic_path in config_ark.pic_where.items():
        temp_im = Image.open(pic_path)
        temp_im = temp_im.convert("RGB")
        window_resolution = globalvar.get_window_resolution()
        max_resolution = globalvar.get_max_resolution()
        width = int(window_resolution[0] / max_resolution[0] * temp_im.size[0])
        height = int(window_resolution[1] / max_resolution[1] * temp_im.size[1])
        temp_im = temp_im.resize((width, height), Image.ANTIALIAS)
        config_ark.pic_where[keys] = np.array(temp_im)
    #常量点 自定义分辨率适应
    for keys,values in config_ark.points.items():
        window_resolution = globalvar.get_window_resolution()
        max_resolution = globalvar.get_max_resolution()
        width = int(window_resolution[0] / max_resolution[0] * values[0])
        height = int(window_resolution[1] / max_resolution[1] * values[1])
        config_ark.points[keys] = [width,height]


class Shark_Event:
    def __init__(self,handle,**kwarg):
        self.handle = handle
        self.num = kwarg['num']
        self.guanqia = kwarg['guanqia']
        self.operation_sequence = [   #前面仍有相关步骤，先做简易版 2019-6-3
            "进入战斗界面",
            "选择并进入活动界面",
            "选择关卡,确认选择正确,使用代理,进入队伍配置界面",
            "确认使用代理并开始战斗",     #若代理确认成功说明在队伍配置界面
            "确认进入战斗,确认没有暂停并等待战斗结束",    #confirm   zhandou start隔一段时间检测一次
            "判断战役成功",  #目前没有失败素材，没有做

        ]
        self.operation_mapping = {}
        for i in range(len(self.operation_sequence)):
            self.operation_mapping[self.operation_sequence[i]] = i

    def find_where(self):
        #重新定位当前位置,根据不同位置决定开始执行哪一步操作
        position = function_ark.judge_where(self.handle,10)
        if position == "gonggao" or position == "zhujiemian":
            return self.operation_mapping["进入战斗界面"]
        elif position == "zhandou_xuanze" or position == "huodongjiemian":
            return self.operation_mapping["选择并进入活动界面"]
        elif position == "huodong_xuanze":
            return self.operation_mapping["选择关卡,确认选择正确,使用代理,进入队伍配置界面"]
        elif position == "zhandou_start":
            return self.operation_mapping["确认使用代理并开始战斗"]
        elif position == "zhandou_ing":
            return self.operation_mapping["确认进入战斗,确认没有暂停并等待战斗结束"]
        elif position == "zhandou_end":
            return self.operation_mapping["判断战役成功"]
        elif position == "yuanshi_lizhi":
            if config_ark.YUANSHI > globalvar.get_yuanshi_used():
                function_ark.mouse_click(self.handle,config_ark.points["yuanshi_ok"])
                globalvar.yuanshi_used_add(1)
            else:
                function_ark.mouse_click(self.handle,config_ark.points["yuanshi_no"])
                print("石乐志，结束\n")
                raise config_ark.ExitError
            time.sleep(1)

        else:
            position1 = function_ark.pic_position(handle, config_ark.pic_where["enter_quick"], once=2)
            if position1 ==None:
                function_ark.save_im(handle,os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                        time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))))
                function_ark.mouse_click(handle,config_ark.points["kongbai"])
            else:
                #若可以快速访问，则直接跳转到战斗主界面
                function_ark.mouse_click(self.handle,position1["result"])
                time.sleep(1)
                position2 = function_ark.pic_position(handle, config_ark.pic_confirm["zhandou_quickenter"], once=2)
                if position2!=None:
                    function_ark.mouse_click(self.handle, position2["result"])
                    time.sleep(2)
                    return self.operation_mapping["选择并进入活动界面"]
                else:
                    #再次判断位置
                    pass
        return self.find_where()

    def start_once(self):
        i = 0
        while(i<len(self.operation_sequence)):
            i = self.find_where()
            if self.operation_sequence[i]=="进入战斗界面":
                function_ark.enter_where(self.handle,"zhandou_xuanze")
                #i += 1
            elif self.operation_sequence[i]=="选择并进入活动界面":
                position = function_ark.pic_position(handle,config_ark.pic_huodong["huodong_enter"],once=3)
                if position!=None:
                    function_ark.mouse_click(self.handle,position["result"])
                    position1 = function_ark.pic_position(handle, config_ark.pic_where["huodongjiemian"], once=3)
                    if position1 != None:
                        function_ark.mouse_click(self.handle, position1["result"])
                    else:
                        pass
                    #i += 1
                else:
                    #i = self.find_where()
                    pass
            elif self.operation_sequence[i]=="选择关卡,确认选择正确,使用代理,进入队伍配置界面":
                function_ark.mouse_click(self.handle,config_ark.points["kongbai"])
                current_position = function_ark.pic_position(self.handle,config_ark.pic_huodong[self.guanqia])
                function_ark.mouse_click(self.handle,current_position["result"])
                time.sleep(1)
                #i += 1
                #确认选择正确
                if function_ark.confirm_where(self.handle,config_ark.pic_confirm[self.guanqia],confirm_once=True):
                    print("关卡信息正确\n")
                    pass
                    #i += 1
                else:
                    #没有选择正确的关卡，重新进入‘选择关卡’
                    #i = self.operation_mapping["选择关卡,确认选择正确,使用代理,进入队伍配置界面"]
                    pass
                #使用代理
                position = function_ark.pic_position(self.handle,config_ark.pic_confirm["daili_do"],once=True)
                if position != None:
                    print("代理已使用\n")
                    #i += 1
                    pass
                else:
                    function_ark.mouse_click(self.handle,config_ark.points['daili'])
                    print("使用代理\n")
                    #i += 1
                #进入队伍配置界面
                time.sleep(1)
                function_ark.mouse_click(self.handle,config_ark.points["peizhi_enter"])
                print("进入队伍配置界面\n")
                time.sleep(3)
                #i += 1
            elif self.operation_sequence[i]=="确认使用代理并开始战斗":
                if function_ark.confirm_where(self.handle,config_ark.pic_where['zhandou_start'],confirm_once=4):
                    if function_ark.confirm_where(self.handle,config_ark.pic_confirm["daili_confirm"]):
                        function_ark.mouse_click(self.handle,config_ark.points["zhandou_start"])
                        time.sleep(3)
                        #i += 1
                    else:
                        raise config_ark.ExitError
                else:
                    #上一步操作点击被吞了
                    #i = self.operation_mapping["进入队伍配置界面"]
                    pass
            elif self.operation_sequence[i]=="确认进入战斗,确认没有暂停并等待战斗结束":
                if function_ark.confirm_where(self.handle,config_ark.pic_where["zhandou_ing"],confirm_once=20):
                    i += 1
                else:
                    #从新定位当前位置
                    continue
                while(1):
                    if function_ark.confirm_where(self.handle,config_ark.pic_where["zhandou_ing"],confirm_once=2):
                        print("正在战斗中\n")
                        position = function_ark.pic_position(self.handle,config_ark.pic_confirm["zhandou_pause"],once=True)
                        if position!=None:
                            function_ark.mouse_click(self.handle,position["result"])
                            print("检测到暂停，继续战斗\n")
                        time.sleep(config_ark.BATTLE_WAIT)
                    else:
                        #结束
                        #i += 1
                        break
            elif self.operation_sequence[i]=="判断战役成功":
                if function_ark.confirm_where(self.handle,config_ark.pic_where["zhandou_end"],confirm_once=10):
                    function_ark.mouse_click(self.handle,config_ark.points["kongbai"])
                    i += 1
                else:
                    #从新定位当前位置
                    #判断是否代理未满3星
                    #self.find_where()
                    pass

    def start(self):
        for i in range(self.num):
            self.start_once()
            time.sleep(3)

if __name__ == "__main__":
    temp = ["GT2","GT3","GT4","GT5","GT6"]              #支持的关卡
    pic_load_ram()                                          #将配置文件中的图像载入内存
    handle = get_handle([1280,720])                         #获取模拟器窗体句柄
    temp_class = Shark_Event(handle,num=20,guanqia=temp[4])  #类实例化，num为刷本次数，guanqia为刷图类型，仅支持GT2-6
    temp_class.start()

    # handle = get_handle([1280, 720])
    # position = function_ark.pic_position(handle,config_ark.pic_where['zhandou_end'])
    # haha = function_ark.confirm_where(handle, "GT3", True, False)
    # im1 = Image.open(config_ark.pic_huodong["GT2"])
    # #im1 = Image.open(pic_confirm["daili_do"])
    # im_origin = Image.open("./ark_images/unprocessed/720p-xuanze.png")
    # #position = pic_locate(pic_others["daili_do"], np.array(im_origin), 0.1,True,True)
    # width = int(1280 / 1920 * im1.size[0])
    # height = int(720 / 1080 * im1.size[1])
    # im1 = im1.resize((width, height), Image.ANTIALIAS)
    # position = pic_locate(config_ark.pic_confirm["GT2"], np.array(im_origin), 0.1, True,True)
    # position = pic_locate(np.array(im1), np.array(im_origin), 0.1, True,True)
    #
    # handle = get_handle([1280, 720])
    # haha = function_ark.confirm_where(handle,"GT1",True,False)