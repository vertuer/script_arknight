import numpy as np
from PIL import Image
import time
import config
from config_ark import *
import scipy.fftpack as fftpack
import aircv
from skimage import io,transform
from basic_function import pic_locate,prtsc,get_handle,mouse_scroll
# def judge_where():
#     def _judge(im):
#         for index,i in enumerate(config.pic_judge):
#             if pic_locate(config.pic_judge[i], im, 0.95, False) != None:
#                 current_pos = index+1
#                 # if current_pos in [6,7,10]:
#                 return current_pos
#
#         return None
#     im = np.array(Image.open('./pics/123.png'))
#     count =0
#     current_pos = _judge(im)
#     if current_pos ==None:
#         print('no situation detected, detect three seconds later')
#         time.sleep(3)
#         current_pos = _judge(im)
#         count+=1
#         if count >=3:
#             io.imsave('./abnormal/judge_failure', im)
#             raise Exception('模拟器可能卡死')
#     else:
#         return current_pos
import function
# def pic_locate(pic_match_path,pic_origin):  #pic_match is the dir path, pic_origin is the data array
#     pic_match_path = transform.rotate(pic_match_path,90)
#     temp1 =fftpack.fft2(pic_match_path[:,:,0],shape=(888,1435))
#     temp = fftpack.fft2(pic_origin[:,:,0])
#     c = np.real(fftpack.ifft2(temp*temp1))
#     pos = np.argwhere(c == np.max(c))
#     # C = np.fft.ifft2(np.fft.fft2(pic_origin)*fftpack.fft2(pic_match_path,(888,1435,3)))
#     return pos
class A:
    pass
if __name__=='__main__':
    # A.count = np.zeros((8,4),dtype=int)    #远征统计
    # pic_origin = io.imread('123.png')
    # position = pic_locate('./yuanzheng_exist.png',pic_origin,0.9,True)
    # reset = function.yuanzheng(handle,'zhujiemian',True)
    # function.return_to_zhujiemian(handle,'zhandou')
    # function.chaijie(handle,reset=False)
    reset = False
    a=config.CS_attackcount  #
    a = 0
    while(1):
        if config.attack_count <a:
            if reset == True:
                reset = function.yuanzheng(handle, 'zhujiemian', reset)
                function.return_to_zhujiemian(handle, 'zhandou')
            function.xiufu(handle,reset)
            function.return_to_zhujiemian(handle)
            if function.zhandou(handle,'zhujiemian',reset)==-1:
                config.attack_count = config.attack_count+1
                continue
        else:
            if reset == False:  # 傻瓜式远征
                function.enter_zhujiemian(handle, 'zhujiemian', reset=reset)
                time.sleep(60)
            else:  # 机智的远征模式

                _, yuanzheng_number = function.enter_zhujiemian(handle, 'zhujiemian', reset)
                if reset == True:
                    reset = function.yuanzheng(handle, 'zhujiemian', reset)
                    function.return_to_zhujiemian(handle, 'zhandou')
                time.sleep(60)


        # if config.attack_count <config.CS_attackcount:
        #     function.xiufu(handle,reset)
        #     function.return_to_zhujiemian(handle, 'zhandou')
        #     if function.zhandou(handle,'zhujiemian',reset)==-1:
        #         config.attack_count = config.attack_count+1
        #         continue
        # else:

    # while(1):
    #     function.enter_zhujiemian(handle, 'zhujiemian', reset=reset)
    #     print('123')
    #     time.sleep(30)
    # while(1):
    #     print('等待5分钟后判断\n')
    #     time.sleep(80)
    #     _,yuanzheng_number = function.enter_zhujiemian(handle,'zhujiemian',reset)
    #     if yuanzheng_number>0:
    #         reset=function.yuanzheng(handle,'zhandou',True,yuanzheng_number)

    # a = function.xiufu(handle,reset)
    # function.return_to_zhujiemian(handle, 'xiufu')
    # function.zhandou(handle,'zhujiemian',False)

    # a = function.judge_where(handle)
    print('233')

