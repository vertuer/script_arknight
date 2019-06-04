from  basic_function import *
import time
import config
current_pos = 0
def judge_where(handle):
    def _judge(handle,im):
        for index,i in enumerate(config.pic_judge):
            if pic_locate(config.pic_judge[i], im, 0.8, False,True,[1280,720]) != None:
                current_pos = i
                return current_pos

            else:
                current_pos = None
        return None
    im = prtsc(handle)
    count =0
    current_pos = _judge(handle,im)
    while(current_pos ==None):
        print('no situation detected, detect two seconds later')
        time.sleep(2)
        im = prtsc(handle)
        current_pos = _judge(handle, im)
        count+=1
        if count >=60:
            io.imsave('./abnormal/judge_failure.png', im)
            raise Exception('模拟器可能卡死')

    return current_pos

def confirm_where(handle,where,rgb_bool = True,confirm_once=True):
    def _judge(handle,im):
        if pic_locate(config.pic_confirm['{}'.format(where)], im, config.thresh_pic, rgb_bool,False,[1280,720]) != None:
            return True
        else:
            return False
    time.sleep(1)
    im = prtsc(handle)
    count =0
    exist = _judge(handle,im)
    if confirm_once ==True:
        return exist

    while (exist == False):
        print('no situation detected, detect two seconds later')
        time.sleep(2)
        im = prtsc(handle)
        exist = _judge(handle, im)
        count += 1
        if count >= 60:
            io.imsave('./abnormal/judge_failure.png', im)
            raise Exception('模拟器可能卡死')

    else:
        return exist

def pic_position(handle,where,thresh=config.thresh_pic,findall=False,once=False):
    while(1):
        im = prtsc(handle)
        position = pic_locate(config.pic_confirm[where], im, thresh, findall,False,[1280,720])
        if position!=None or once==False:
            break
        time.sleep(2)
    return position

def enter_zhujiemian(handle,where,reset=True): #如果检测到有远征回归并且reset为True那么返回需要重新出征的数量
    yuanzheng_number = 0
    if where =='zhandou':
        while(1):
            time.sleep(1)
            current_pos = judge_where(handle)
            if current_pos in ['zhujiemian','liebiao']:
                mouse_click(handle,config.zhujiemian_zhandou_enter)

            elif current_pos in ['houqin','houqinagain']:
                if reset==False:
                    mouse_click(handle, config.zhujiemian_houqin_confirm)
                else:
                    mouse_click(handle, config.zhujiemian_houqin_cancel)
                    if current_pos == 'houqinagain':
                        yuanzheng_number +=1
            elif current_pos in ['gonggao']:
                position = pic_position(handle,'gonggao',config.thresh_pic,False,False)
                if position!= None:
                    mouse_click(handle,position['result'])
                    print('检测到公告界面\n')
            elif current_pos in ['tanchuang']:
                mouse_click(handle,config.single_confirm)
                print('检测到成就完成或者是签到界面\n')
            if confirm_where(handle, 'zhandou'):
                return True, yuanzheng_number
        # if current_pos in [10]:
        #     mouse_click(handle, config.click[0], config.click[1])
        #     time.sleep(0.5)
        #     if confirm_where(handle,'houqinagain'):
        #         mouse_click(handle,config.houqin_confirm[0],config.houqin_confirm[1])
        #         if confirm_where(handle,'zhujiemian'):
        #             mouse_click(handle,config.zhandou_enter[0],config.zhandou_enter[1])
        #     else:
        #         raise('no houqinagain detected')

    elif where =='liebiao':
        while(1):
            time.sleep(1)
            current_pos = judge_where(handle)
            if current_pos in ['liebiao']:
                return True,yuanzheng_number
            elif current_pos in ['zhujiemian']:
                mouse_click(handle,config.zhujiemian_houqin_status)
                if confirm_where(handle,'liebiao'):
                    return True,yuanzheng_number
            elif current_pos in ['houqin','houqinagain']:
                if reset==False:
                    mouse_click(handle, config.zhujiemian_houqin_confirm)
                else:
                    mouse_click(handle, config.zhujiemian_houqin_cancel)
                    if current_pos =='houqinagain':
                        yuanzheng_number += 1
    elif where == 'zhujiemian':
        while(1):
            time.sleep(1)
            current_pos = judge_where(handle)
            if current_pos in ['liebiao']:
                return True, yuanzheng_number
            elif current_pos in ['zhujiemian']:
                return True, yuanzheng_number
            elif current_pos in ['houqin', 'houqinagain']:
                if reset == False:
                    mouse_click(handle, config.zhujiemian_houqin_confirm)
                else:
                    mouse_click(handle, config.zhujiemian_houqin_cancel)
                    if current_pos == 'houqinagain':
                        yuanzheng_number += 1
            elif current_pos in ['gonggao']:
                position = pic_position(handle,'gonggao',config.thresh_pic,False,False)
                if position!= None:
                    mouse_click(handle,position['result'])
                    print('检测到公告界面\n')
            elif current_pos in ['tanchuang']:
                mouse_click(handle,config.single_confirm)
                print('检测到成就完成或者是签到界面\n')
    elif where == 'xiufu':
        while(1):
            time.sleep(1)
            current_pos = judge_where(handle)
            if current_pos in ['liebiao','zhujiemian']:
                mouse_click(handle,config.zhujiemian_xiufu_enter)
            elif current_pos in ['houqin', 'houqinagain']:
                if reset == False:
                    mouse_click(handle, config.zhujiemian_houqin_confirm)
                else:
                    mouse_click(handle, config.zhujiemian_houqin_cancel)
                    if current_pos == 'houqinagain':
                        yuanzheng_number += 1
            elif current_pos in ['gonggao']:
                position = pic_position(handle,'gonggao',config.thresh_pic,False,False)
                if position!= None:
                    mouse_click(handle,position['result'])

            if current_pos in ['xiufu']:
                return True, yuanzheng_number
    elif where == 'gongchang':
        while(1):
            time.sleep(1)
            current_pos = judge_where(handle)
            if current_pos in ['liebiao','zhujiemian']:
                mouse_click(handle,config.zhujiemian_gongchang_enter)
            elif current_pos in ['houqin', 'houqinagain']:
                if reset == False:
                    mouse_click(handle, config.zhujiemian_houqin_confirm)
                else:
                    mouse_click(handle, config.zhujiemian_houqin_cancel)
                    if current_pos == 'houqinagain':
                        yuanzheng_number += 1
            elif current_pos in ['gonggao']:
                position = pic_position(handle,'gonggao',config.thresh_pic,False,False)
                if position!= None:
                    mouse_click(handle,position['result'])
            if current_pos in ['gongchang']:
                return True, yuanzheng_number
    # im = prtsc(handle)
    # io.imsave('./abnormal/judge_failure.jpg', im)
    # raise('模拟器可能卡死')
    # return

def return_to_zhujiemian(handle,reset=False):
    while(1):
        where = judge_where(handle)
        if where in ['zhujiemian']:
            return True
        elif where=='zhandou':
            mouse_click(handle,config.zhandou_return_zhujiemian)
            print('返回主界面\n')
        elif where=='xiufu':
            mouse_click(handle, config.zhandou_return_zhujiemian)
            print('返回主界面\n')
        elif where == 'gongchang':
            mouse_click(handle, config.zhandou_return_zhujiemian)
            print('返回主界面\n')
        elif where in ['houqin', 'houqinagain']:
            if reset == False:
                mouse_click(handle, config.zhujiemian_houqin_confirm)
            else:
                mouse_click(handle, config.zhujiemian_houqin_cancel)
            print('chuxian houqin\n')
        elif where in ['gonggao']:
            position = pic_position(handle, 'gonggao', config.thresh_pic, False, False)
            if position != None:
                mouse_click(handle, position['result'])
                print('检测到zuozhanshezhi\n')
        elif where in ['tanchuang']:
            mouse_click(handle, config.single_confirm)
            print('检测到成就完成或者是签到界面\n')
        time.sleep(2)
def kuaixiu_function(handle,thresh = 1000):
    count=0
    time.sleep(1)
    t =[]
    im = prtsc(handle)
    position = pic_locate(config.pic_confirm['kuaisuxiufu'], im, 0.8, True, False,[1280,720])
    if position!=None:
        for i in position:
            w = int(i['result'][0])
            h = int(i['result'][1])
            im1 = im[h-70:h-40,w-60:w+60]
            result = ocr(im1)
            if len(result)!=6:
                break
            elif int(result)>thresh:
                while(1):
                    mouse_click(handle,i['result'])
                    if confirm_where(handle,'kuaixiu_confirm',False):
                        break
                mouse_click(handle,config.zhujiemian_houqin_confirm)
                count = count+1
    return count


def yuanzheng(handle,where,reset=False,chuji_number=0):
    houqin_biandui = config.CS_houqin_biandui
    houqin_xuanze = config.CS_houqin_xuanze
    # yuanzheng_file = open(config.yuanzheng_log,'w')
    def yuanzheng_chuji(number):
        mission_match = 0
        if number < 4:
            # yuanzheng_file.write(
            #     '后勤未满，开始远征  {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            print(('后勤未满，开始远征  {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S'
                                                          , time.localtime(time.time())))))
            enter_zhujiemian(handle, 'zhandou', reset)
            while(1):
                mouse_click(handle, config.zhandou_houqin)
                time.sleep(0.5)
                if confirm_where(handle,'yuanzheng',True,True):
                    break


            i = 0
            while (i < 4 - number):   #远征未满时派出
                cnt=0  #防意外卡死
                if houqin_xuanze[i][0] <= 5:
                    while (confirm_where(handle, '0zhanyi', False,True) != True):
                        mouse_drag(handle, config.zhandou_houqin_zhanyi_wipeup, 20)
                        cnt+=1
                        if cnt>15:
                            raise Exception('进入到了奇怪的地方')
                else:
                    while (confirm_where(handle, '8zhanyi',False, True) != True):
                        mouse_drag(handle, config.zhandou_houqin_zhanyi_wipedown, 20)
                        cnt+=1
                        if cnt>15:
                            raise Exception('进入到了奇怪的地方')
                while(1):
                    im = prtsc(handle)
                    position = pic_locate(config.pic_confirm['{}zhanyi'.format(houqin_xuanze[i][0])], im, config.thresh_pic, False,False,[1280,720])
                    mouse_click(handle, position['result'])
                    time.sleep(0.5)
                    if pic_locate(config.pic_confirm['{}zhanyi'.format(houqin_xuanze[i][0])], im, config.thresh_pic, False,True,[1280,720])!=None:
                        break
                im = prtsc(handle)
                position = pic_locate(config.pic_confirm['yuanzhengsent'],
                                 im[606:712, 173 + 220 * houqin_xuanze[i][1]:383 + 220 * houqin_xuanze[i][1]], config.thresh_pic,
                                 False,False,[1280,720])
                if position != None:
                    print('{}任务已有梯队执行'.format(houqin_xuanze[i]))
                    number-=1 #yuanzheng wei paichu
                else:
                    mouse_click(handle, config.yuanzhengkaishi(houqin_xuanze[i][1]))
                    time.sleep(0.5)
                    if confirm_where(handle, 'tiduixuanze'):
                        im = prtsc(handle)
                        count = 0
                        for j in houqin_biandui:
                            position = pic_locate(config.pic_confirm['{}tidui'.format(j)], im, config.thresh_pic, False,False,[1280,720])
                            if position == None:
                                count += 1
                                if count >= len(houqin_biandui):
                                    raise Exception('后勤编队无效')
                            else:
                                mouse_click(handle, position['result'])
                                time.sleep(0.5)
                                mouse_click(handle, config.tidui_confirm)
                                print('{}编队出击{}任务'.format(j, houqin_xuanze[i]))
                                # yuanzheng_file.write('{}远征任务开始\n'.format(houqin_xuanze[i]))
                                # number+=1
                                break
                i += 1
        print('开始判断远征是否匹配')
        enter_zhujiemian(handle,'zhandou',reset)  #不论是否出征，都判断是否匹配
        mouse_click(handle, config.zhandou_houqin)
        time.sleep(0.5)
        for i in range(4):  #判断远征是否全部匹配
            cnt=0
            if houqin_xuanze[i][0] <= 5:
                while (confirm_where(handle, '0zhanyi', False) != True):
                    mouse_drag(handle, config.zhandou_houqin_zhanyi_wipeup, 20)
                    cnt += 1
                    if cnt > 15:
                        raise Exception('进入到了奇怪的地方')
            else:
                while (confirm_where(handle, '8zhanyi', False) != True):
                    mouse_drag(handle, config.zhandou_houqin_zhanyi_wipedown, 20)
                    cnt += 1
                    if cnt > 15:
                        raise Exception('进入到了奇怪的地方')
            im = prtsc(handle)
            position = pic_locate(config.pic_confirm['{}zhanyi'.format(houqin_xuanze[i][0])], im, config.thresh_pic, False,False,[1280,720])
            mouse_click(handle, position['result'])
            time.sleep(0.5)
            im = prtsc(handle)
            position = pic_locate(config.pic_confirm['yuanzhengsent'],
                             im[606:712, 173 + 220 * houqin_xuanze[i][1]:383 + 220 * houqin_xuanze[i][1]], 0.9,
                             False,False,[1280,720])
            if position != None:
                print('{}任务已有梯队执行'.format(houqin_xuanze[i]))
                mission_match += 1
                if mission_match == 4:
                    print('后勤任务全部匹配，开始傻瓜式远征\n')
                    return False
        print('当前共有{}梯队远征匹配\n'.format(mission_match))
        return True
    if where =='zhujiemian':
        enter_zhujiemian(handle,'liebiao',reset)
        time.sleep(1)
        im = prtsc(handle)
        position = pic_locate(config.yuanzheng_num,im,config.thresh_pic,True,True,[1280,720])
        number = len(position)
        while(number==None):
            print('no liebiao  detected')
            enter_zhujiemian(handle,'liebiao',reset)
            im = prtsc(handle)
            pos = pic_locate(config.yuanzheng_num, im, config.thresh_pic, True,True,[1280,720])
            number = len(pos)
        return yuanzheng_chuji(number)
    elif where=='zhandou':
        return yuanzheng_chuji(4-chuji_number)

def xiufu(handle,reset,kuaixiu = config.CS_kuaixiu):
    return_to_zhujiemian(handle)
    _,number = enter_zhujiemian(handle,'xiufu',reset)
    im = prtsc(handle)
    position = pic_locate(config.pic_confirm['xiufu_xuanze'], im, config.thresh_pic, False,True,[1280,720])
    if position==None:
        # im = prtsc(handle)
        # io.imsave('./abnormal/xiufu_failure.jpg', im)
        # raise Exception('不在修复界面内')
        pass
    else:
        mouse_click(handle, position['result'])
    while(1):
        time.sleep(1)
        if confirm_where(handle,'wuxiufu',True)==True:
            print('没有需要修复的枪\n')
            mouse_click(handle, config.single_confirm)
            time.sleep(0.5)
            break
        else:
            for i in range(6):
                mouse_click(handle,config.xiufu_xuanze(i,1))
            mouse_click(handle,config.xiufu_confirm)
            time.sleep(0.5)
            position = pic_position(handle, 'kuaixiu')
            if position ==None:
                print('确认修理界面未正常出现\n')
                im = prtsc(handle)
                position = pic_locate(config.pic_confirm['xiufu_xuanze'], im, config.thresh_pic, False,True,[1280,720])
                mouse_click(handle, position['result'])
            else:
                mouse_click(handle,config.xiufu_start)
                time.sleep(0.5)
                break
            # if kuaixiu==True:
            #     print('使用快速修理\n')
            #     config.count = config.count+kuaixiu_function(handle,thresh = config.thresh_kuaixiu)
            #     if config.count>= config.CS_kuaixiushangxian:
            #         config.CS_kuaixiu = False
            #     mouse_click(handle,position['result'])
    cnt = 0
    while(1):

        if pic_position(handle,'kuaisuxiufu')==None:
            break
        time.sleep(10)
        print('有枪在修复中，等待10秒\n')
        if kuaixiu == True and cnt ==0:
            cnt = 1
            print('使用快速修理\n')
            config.count = config.count + kuaixiu_function(handle, thresh=config.thresh_kuaixiu)
            if config.count >= config.CS_kuaixiushangxian:
                config.CS_kuaixiu = False
    print('修复完成\n')
    return number

def zhandou_manage(handle):
    current_pos = zhandou_judge(handle)
    if current_pos in  ['zhandouend','zhandoujiangli','total_end']:
        mouse_click(handle,config.click)
        time.sleep(0.5)
        print('现在处于{}'.format(current_pos))
        return True
    elif current_pos in ['zhandouing']:
        return True
    else:
        return False

def zhandou_judge(handle):
    def _judge(handle,im):
        for index,i in enumerate(config.battle_judge):
            if pic_locate(config.battle_judge[i], im, 0.9, False,False,[1280,720]) != None:
                current_pos = i
                return current_pos

            else:
                current_pos = None
        return None
    im = prtsc(handle)
    count =0
    current_pos = _judge(handle,im)
    while(current_pos ==None):
        print('no situation detected, detect two seconds later')
        time.sleep(2)
        im = prtsc(handle)
        current_pos = _judge(handle, im)
        count+=1
        if count >=6:
            break
            # io.imsave('./abnormal/battle_judge_failure.png', im)
            # raise'模拟器可能卡死'

    return current_pos

def zhandou(handle,where,reset):
    zhandou_zhuli = config.CS_zhandou_zhuli
    zhandou_peilian = config.CS_zhandou_peilian
    zhandou_renwu = config.CS_zhandou_renwu  #前两位代表任务号，最后是普通，紧急，夜战
    def renwu_xuanze(reset):  #进入作战场景,返回是否傻瓜式远征
        cnt=0
        if where == 'zhujiemian':
            _,number = enter_zhujiemian(handle,'zhandou',reset)
            if number!=0:
                reset = yuanzheng(handle,'zhandou',reset,number)
        elif where =='zhandou':
            pass
        time.sleep(1)
        mouse_click(handle,config.zhandou_zuozhan)
        time.sleep(1)
        if zhandou_renwu[0] <= 5:
            while (confirm_where(handle, '0zhanyi', False,True) != True):
                mouse_drag(handle, config.zhandou_houqin_zhanyi_wipeup, 20)
                cnt += 1
                if cnt > 30:
                    raise Exception('进入到了奇怪的地方')
        else:
            while (confirm_where(handle, '8zhanyi', False,True) != True):
                mouse_drag(handle, config.zhandou_houqin_zhanyi_wipedown, 20)
                cnt += 1
                if cnt > 30:
                    raise Exception('进入到了奇怪的地方')
        time.sleep(0.5)
        im = prtsc(handle)
        position = pic_locate(config.pic_confirm['{}zhanyi'.format(zhandou_renwu[0])], im, config.thresh_pic, False,False,[1280,720])
        mouse_click(handle, position['result'])
        time.sleep(0.5)
        mouse_click(handle,config.zhandou_leixing[zhandou_renwu[2]-1])
        time.sleep(1)
        if zhandou_renwu[2]==1 and zhandou_renwu[1]>=5:
            pass
        else:
            position = pic_position(handle,'{}-{}-{}'.format(zhandou_renwu[0],zhandou_renwu[1],zhandou_renwu[2]),thresh=0.9)
        if position ==None:
            raise Exception
        else:
            mouse_click(handle,position['result'])
        time.sleep(1)
        position = pic_position(handle,'zhandou_enter')
        if position ==None:
            raise Exception
        else:
            mouse_click(handle,position['result'])
        time.sleep(0.5)
        print('进入战斗场景\n')
        while(1):
            if confirm_where(handle,'renxingman')==True:
                chaijie(handle) #拆枪
                return -1
            elif confirm_where(handle,'zhandouzhunbei',True)==True:
                return reset
            #其余情况重新进入
    def ditu(mission):
        mouse_scroll(handle)
        cnt =0
        im = prtsc(handle)
        pic_match_path = config.pic_confirm['{}-{}-{}map'.format(mission[0],mission[1],mission[2])]
        pic_test = np.array(Image.open(pic_match_path, 'r'))
        position = aircv.find_all_template(im,pic_test[:,0:int(pic_test.shape[1]/2),:],0.9)
        while(position==[]):
            cnt+=1
            if cnt>30:
                raise Exception('地图校正失败')
            mouse_drag(handle,config.zhandou_suoxiao,20)
            time.sleep(0.5)
            for i in ['ditu_wudian1','ditu_wudian2']:
                if confirm_where(handle,i,True)==True:
                    mouse_click(handle,config.single_confirm)
            if confirm_where(handle,'tiduixuanze',True)==True:
                mouse_click(handle, config.tidui_cancel)
            time.sleep(1)
            im = prtsc(handle)
            pic_test = np.array(Image.open(pic_match_path, 'r'))
            position = aircv.find_all_template(im, pic_test[:, 0:int(pic_test.shape[1] / 2), :], 0.9)
        mouse_scroll(handle)
        print('地图校正完成\n')

    def _peilian(xy):
        mouse_click(handle, xy)
        time.sleep(1)
        position = pic_position(handle, '{}tidui'.format(zhandou_peilian), config.thresh_pic, False, False)
        if position == None:
            raise Exception
        else:
            mouse_click(handle, position['result'])
            time.sleep(0.5)
            mouse_click(handle, config.tidui_confirm)
            time.sleep(0.5)
            print('陪练队部署完毕\n')
    def _zhuli(xy):
        mouse_click(handle,xy)
        time.sleep(0.5)
        im = prtsc(handle)
        position = pic_locate(config.pic_confirm['{}tidui'.format(zhandou_zhuli)], im, config.thresh_pic, False,False,[1280,720])
        if position == []:
            raise Exception
        else:
            mouse_click(handle, position['result'])
            mouse_click(handle, config.tidui_confirm)
            time.sleep(0.5)
            print('主力队部署完毕\n')

    def _jihua_start():
        time.sleep(3)
        cnt = 0
        while(1):
            time.sleep(0.5)
            cnt += 1
            if cnt > 60:
                raise Exception
            im = prtsc(handle)
            position = pic_locate(config.pic_confirm['jihuamoshi'], im, config.thresh_pic, False, True,[1280,720])
            if position != None:
                mouse_click(handle, position['result'])
                time.sleep(0.5)
            if pic_locate(config.pic_confirm['jihuaxuanzhong'], im, config.thresh_pic,False, True,[1280,720])!=None:
                break
        print('计划模式选中\n')


    def _huadong(mode='up'):
        if mode=='up':
            mouse_drag(handle,config.zhandou_houqin_zhanyi_wipeup,20)
            time.sleep(0.5)
            mouse_drag(handle, config.zhandou_houqin_zhanyi_wipeup, 20)
            time.sleep(0.5)

    def _jihua_end(name):
        im = prtsc(handle)
        position = pic_locate(config.pic_confirm[name], im, config.thresh_pic, False, True,[1280,720])
        if position == None:
            raise Exception
        else:
            mouse_click(handle, config.tidui_confirm)
            time.sleep(0.5)
            print('执行计划\n')

    def _zhandou_end(final=True):
        cnt =0
        while(1):
            time.sleep(10)
            cnt+=1
            if cnt>60:
                raise Exception
            if confirm_where(handle,'jihuamoshi',True)==True:
                break
        while(1):
            mouse_click(handle,config.tidui_confirm)
            time.sleep(0.5)
            if confirm_where(handle,'jieshuhuihe',True,True)!=True:
                break
        print('战斗完成\n')
        time.sleep(0.5)
        if final== True:
            while(1):
                if zhandou_manage(handle):
                    pass
                else:
                    pos = judge_where(handle)
                    if pos in ['zhujiemian','liebiao','houqin','houqinagain','zhandou']:
                        break


    def zhandou_start542():
        _peilian([1043, 551])
        _huadong()

        _zhuli([1080,174])
        mouse_click(handle,config.tidui_confirm)  #战斗开始
        _jihua_start()

        mouse_click(handle, [1080, 174])
        time.sleep(0.3)
        mouse_click(handle, [858, 155])
        time.sleep(0.3)
        mouse_click(handle, [683, 214])
        time.sleep(0.3)
        mouse_click(handle, [480, 180])
        time.sleep(0.3)
        mouse_click(handle, [258, 204])
        time.sleep(0.3)

        _jihua_end('4jihua')

        _zhandou_end()

    def zhandou_start021():
        _peilian([262,345])


        _zhuli([665,364])
        mouse_click(handle,config.tidui_confirm)  #战斗开始
        _jihua_start()

        mouse_click(handle, [671, 358])
        time.sleep(0.3)
        mouse_click(handle, [494, 259])
        time.sleep(0.3)
        _huadong('up')
        mouse_click(handle, [534,559])
        time.sleep(0.3)
        mouse_click(handle, [671,358])
        time.sleep(0.3)
        mouse_click(handle, [522,258])
        time.sleep(0.3)

        _jihua_end('4jihua')
        _zhandou_end(False)
        print('铁血回合\n')
        time.sleep(4)
        _jihua_start()
        mouse_click(handle, [520,256])
        time.sleep(0.3)
        mouse_click(handle, [811,257])
        time.sleep(0.3)
        mouse_click(handle, [988,294])
        time.sleep(0.3)
        _jihua_end('31jihua')
        _zhandou_end()

    reset = renwu_xuanze(reset)
    if reset==-1:
        return -1
    ditu(zhandou_renwu)
    if zhandou_renwu == [0,2,1]:
        zhandou_start021()
    elif zhandou_renwu == [5,4,2]:
        zhandou_start542()
    # globals().get('zhandou_start{}'.format(number))()
    return reset

def chaijie(handle,mode = 0):
    while(1):
        im = prtsc(handle)
        position = pic_locate(config.pic_confirm['renxingman'], im, config.thresh_pic, False,True,[1280,720])
        if position!=None:
            mouse_click(handle,position['result'])
            time.sleep(0.5)
        if confirm_where(handle,'gongchang',False)==True:
            break
    # mouse_click(handle,config.tri_return)
    # time.sleep(0.5)
    # if return_to_zhujiemian(handle,'zhandou')==True:
    #     pass
    # else:
    #     raise Exception
    # _,number = enter_zhujiemian(handle,'gongchang',reset)
    mouse_click(handle,config.gongchang_chaijie)
    time.sleep(1)
    while(1):
        position = pic_position(handle, 'chaijie_xuanze_juese', 0.95)
        if position != None:
            mouse_click(handle,position['result'])
            break
    time.sleep(0.5)
    if mode ==0:
        mouse_click(handle,[1188,284])
        time.sleep(0.5)
        mouse_click(handle, [622,265])
        time.sleep(0.5)
        if confirm_where(handle,'chaijie_2xing'):
            mouse_click(handle,[948,675])
        else:
            raise Exception('123')
        time.sleep(0.5)
    for i in range(6):
        for j in range(2):
            mouse_click(handle,config.xiufu_xuanze(i,j))
            time.sleep(0.1)
    mouse_click(handle,config.tidui_confirm)
    time.sleep(0.5)
    position = pic_position(handle,'chaijie_confirm',0.98,False,True)
    mouse_click(handle,position['result'])
    time.sleep(0.5)
    if return_to_zhujiemian(handle,'gongchang')==True:
        pass
    else:
        raise Exception
    # def yuanzheng(handle, reset=False):
    #     houqin_biandui = [4, 6, 7, 8]
    #     houqin_xuanze = [[1, 4], [0, 4], [7, 2], [8, 2]]
    #     yuanzheng_file = open(config.yuanzheng_log, 'a')
    #     im = prtsc(handle)
    #     enter_zhujiemian(handle, 'liebiao', reset)
    #     time.sleep(1)
    #     im = prtsc(handle)
    #     pos = pic_locate(config.yuanzheng_num, im, 0.9, True)
    #     number = len(pos)
    #     while (number == None):
    #         print('no liebiao  detected')
    #         enter_zhujiemian(handle, 'liebiao', reset)
    #         im = prtsc(handle)
    #         pos = pic_locate(config.yuanzheng_num, im, 0.9, True)
    #         number = len(pos)
    #     if number < 4:
    #         yuanzheng_file.write(
    #             '后勤未满，开始远征  {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    #         enter_zhujiemian(handle, 'zhandou', reset)
    #         mouse_click(handle, config.zhandou_houqin)
    #         time.sleep(0.5)
    #         mission_match = 0
    #         if confirm_where(handle, 'yuanzheng'):
    #             i = 0
    #             while (i < 4 - number):
    #                 if houqin_xuanze[i][0] <= 5:
    #                     while (confirm_where(handle, '0zhanyi', True) != True):
    #                         mouse_drag(handle, config.zhandou_houqin_zhanyi_wipeup, 20)
    #                 else:
    #                     while (confirm_where(handle, '8zhanyi', True) != True):
    #                         mouse_drag(handle, config.zhandou_houqin_zhanyi_wipedown, 20)
    #                 im = prtsc(handle)
    #                 pos = pic_locate(config.pic_confirm['{}zhanyi'.format(houqin_xuanze[i][0])], im, 0.9, False)
    #                 mouse_click(handle, pos['result'])
    #                 time.sleep(0.5)
    #                 im = prtsc(handle)
    #                 pos = pic_locate(config.pic_confirm['yuanzhengsent'],
    #                                  im[606:712, 173 + 220 * houqin_xuanze[i][1]:383 + 220 * houqin_xuanze[i][1]], 0.9,
    #                                  False)
    #                 if pos != None:
    #                     print('{}任务已有梯队执行'.format(houqin_xuanze[i]))
    #                     mission_match += 1
    #                     number -= 1
    #                     if mission_match == 4:
    #                         yuanzheng_file.write('后勤任务全部匹配，开始傻瓜式远征\n')
    #                         return False
    #                 else:
    #                     mouse_click(handle, config.yuanzhengkaishi(houqin_xuanze[i][1]))
    #                     time.sleep(0.5)
    #                     if confirm_where(handle, 'tiduixuanze'):
    #                         im = prtsc(handle)
    #                         count = 0
    #                         for j in houqin_biandui:
    #                             pos = pic_locate(config.pic_confirm['{}tidui'.format(j)], im, 0.95, False)
    #                             if pos == None:
    #                                 count += 1
    #                                 if count >= len(houqin_biandui):
    #                                     raise '后勤编队无效'
    #                             else:
    #                                 mouse_click(handle, pos['result'])
    #                                 time.sleep(0.5)
    #                                 mouse_click(handle, config.tidui_confirm)
    #                                 print('{}编队出击{}任务'.format(j, houqin_xuanze[i]))
    #                                 yuanzheng_file.write('{}远征任务开始\n'.format(houqin_xuanze[i]))
    #                                 yuanzheng_file.close()
    #                                 break
    #                 i += 1
    #
    #
    #
    #     else:
    #         return True


    # reset = True
    #
    #
    # reset = yuanzheng(handle,'zhujiemian',reset)   #所有远征派出
    # enter_zhujiemian(handle,'zhujiemian',reset)

