from  basic_function import *
import time
import os
import config_ark
# time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
def judge_where(handle,count_max=60):
    def _judge(im):
        for keys,pic_data in config_ark.pic_where.items():
            if pic_locate(pic_data, im, config_ark.THRESH_PIC,False,True) != None:
                current_pos = keys
                return current_pos
        return None
    im = prtsc(handle)
    count =0
    current_pos = _judge(im)
    while(current_pos ==None):
        print('no situation detected, detect two seconds later')
        time.sleep(2)
        im = prtsc(handle)
        current_pos = _judge(im)
        count+=1
        if count >=count_max:
            if count_max == 60:
                io.imsave(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                    time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))), im)
                raise Exception('模拟器可能卡死')
            else:
                return current_pos

    return current_pos

def confirm_where(handle,pic_data,rgb_bool = True,confirm_once=True):
    def _judge(im):
        if pic_locate(pic_data, im, config_ark.THRESH_PIC, rgb_bool= rgb_bool,findall=False) != None:
            return True
        else:
            return False
    time.sleep(1)
    im = prtsc(handle)
    count =0
    exist = _judge(im)
    if confirm_once ==True:
        return exist
    if confirm_once==False:
        count_max = 60
    else:
        count_max = confirm_once
    while (exist == False):
        print('no situation detected, detect two seconds later')
        time.sleep(2)
        im = prtsc(handle)
        exist = _judge(im)
        count += 1
        if count >= count_max:
            if count_max ==60:
                io.imsave(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                    time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))), im)
                raise Exception('模拟器可能卡死')
            else:
                return exist

    return exist

def pic_position(handle,pic_data,thresh=config_ark.THRESH_PIC,findall=False,once=False):
    count = 0
    if once != False and once != True:
        count_max = once
    else:
        count_max = 60
    while(1):
        im = prtsc(handle)
        position = pic_locate(pic_data, im, thresh, findall,rgb_bool=False)
        if position!=None or once==True:
            break
        time.sleep(2)
        count +=1
        if count>=count_max:
            if count_max ==60:
                io.imsave(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                    time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))), im)
                raise Exception('模拟器可能卡死')
            else:
                return position
    return position

def enter_where(handle,where):
    #利用导航进入各个主界面
    #先判断当前所在位置，若为公告：关闭 战斗中：等待 战斗结束：随意点击 若与where一致：不操作 主界面：点击对应位置
    # where: 表示进入的位置   目前暂时只支持"作战"
    # return false:失败 true:成功
    current_pos = judge_where(handle,60)  #若有不存在当前图像库的状况保存
    if current_pos == "gonggao":
        position = pic_position(handle,config_ark.pic_where["gonggao"],once=True)
        if position!=None:
            mouse_click(handle,position["result"])
            if confirm_where(handle,config_ark.pic_where["gonggao"]) and where=="zhandou_xuanze":
                mouse_click(handle,config_ark.points["zhandou_enter"])
                if confirm_where(handle,config_ark.pic_where[where],confirm_once=5):
                    return True

        else:
            print("人为关闭公告，略过\n")
    elif current_pos == "zhujiemian":
        mouse_click(handle, config_ark.points["zhandou_enter"])
        if confirm_where(handle, config_ark.pic_where[where], confirm_once=5):
            return True
    else:
        #暂时用不上，懒得写
        pass
    #enter_where(handle,where) 不使用迭代，较危险
    return False

