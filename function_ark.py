from  basic_function import *
import time
import os
import config_ark
# time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
def judge_where(handle,count_max=60):
    #判断当前位置
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
                temp_im = Image.fromarray(im)
                temp_im.save(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                    time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))))
                # io.imsave(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                #     time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))), im)
                raise Exception('模拟器可能卡死')
            else:
                return current_pos

    return current_pos

def confirm_where(handle,pic_data,rgb_bool = True,confirm_once=True):
    #验证当前是否处于某位置
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
                temp_im = Image.fromarray(im)
                temp_im.save(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                    time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))))
                # io.imsave(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                #     time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))), im)
                raise Exception('模拟器可能卡死')
            else:
                return exist

    return exist

def pic_position(handle,pic_data,thresh=config_ark.THRESH_PIC,findall=False,once=False):
    #寻找图像位于模拟器的像素位置，左上为（0，0）
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
                temp_im = Image.fromarray(im)
                temp_im.save(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                    time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))))
                # io.imsave(os.path.join(config_ark.IMG_SAVE,'error_{}.png'.format(
                #     time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))), im)
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

def enter_chapter(handle,where):
    #从战斗进入主线
    #where为主线章节,如 "1-11"
    position = pic_position(handle,config_ark.pic_where["zhandou_xuanze"],once=True)
    if position!=None:
        mouse_click(handle,position["result"])
        time.sleep(1)
    else:
        return False
    cnt=0
    chapter = where.split('-')[0]
    while (1):
        position = pic_position(handle, config_ark.pic_confirm["chapter{}".format(chapter)],once=1)
        if position!=None:
            break
        mouse_drag(handle, config_ark.points['drag_left'], 20)
        cnt += 1
        if cnt > 10:
            print("主线进入失败，重新进入战斗界面")
            return False

    mouse_click(handle,position["result"])
    print("进入chapter{}".format(chapter))
    return True
def enter_zhuxian(handle,where):
    #从章节进入主线
    cnt = 0
    while (1):
        position = pic_position(handle, config_ark.guanqia_pic[where],once=1)
        if position != None:
            break
        mouse_drag(handle, config_ark.points['drag_left'], 20)
        cnt += 1
        if cnt > 20:
            print("主线进入失败，重新进入战斗界面")
            return False
    mouse_click(handle, position["result"])
    print("选择关卡")
    if confirm_where(handle, config_ark.guanqia_pic["{}_confirm".format(where)], confirm_once=2):
        mouse_click(handle, config_ark.points["peizhi_enter"])
        print("进入队伍配置界面")
    else:
        return False
    time.sleep(3)
    return True


def set_direction(handle,xy,direction):
    #direction left ,right up down
    if direction == "left":
        temp_xy = [xy[0]-config_ark.BUSHU_OFFSET,xy[1]]
        mouse_drag(handle,(xy,temp_xy),config_ark.DRAG_SPEED)
    elif direction == "right":
        temp_xy = [xy[0]+config_ark.BUSHU_OFFSET,xy[1]]
        mouse_drag(handle,(xy,temp_xy),config_ark.DRAG_SPEED)
    elif direction == "up":
        temp_xy = [xy[0],xy[1]-config_ark.BUSHU_OFFSET]
        mouse_drag(handle,(xy,temp_xy),config_ark.DRAG_SPEED)
    elif direction == "down":
        temp_xy = [xy[0],xy[1]-config_ark.BUSHU_OFFSET]
        mouse_drag(handle,(xy,temp_xy),config_ark.DRAG_SPEED)

def battle_speed_set(handle,speed=2):
    if speed ==2:
        position = pic_position(handle,config_ark.pic_confirm["1xspeed"],once=True)
        if position!=None:
            mouse_click(handle,position["result"])
            time.sleep(0.5)
            if confirm_where(handle,config_ark.pic_confirm["2xspeed"],confirm_once=True):
                print("战斗速度修改为2x")
                return True
        else:
            print("当前战斗速度为2x")
            return True
    return False

def staff_set(handle,name_or_xy,target_xy,direction):
    """
    部署干员,自动检查费用是否足够及部署目标位置是否正确
    :param handle: 窗口句柄
    :param name_or_xy: 部署干员名称或xy坐标
    :param target_xy: 部署位置xy坐标
    :return:  true部署正确，false未知错误
    """
    if isinstance(name_or_xy,str):
        #干员名称
        assert(name_or_xy in config_ark.staff_pic.keys())
        staff_pic = config_ark.staff_pic[name_or_xy]
        i = 0
        while(i<30):
            i += 1
            position = pic_position(handle,staff_pic,config_ark.THRESH_PIC,once=True)
            if position!=None:
                mouse_drag(handle,(position["result"],target_xy),config_ark.DRAG_SPEED)
                time.sleep(1)
                if confirm_where(handle,config_ark.pic_confirm["bushu_fangxiang"]):
                    set_direction(handle,target_xy,direction)
                    time.sleep(2)
                    return True
            else:
                print("No staff{} detected".format(name_or_xy))

        return False