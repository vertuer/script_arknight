import os

#少女前线预载入配置信息  2018-8月版本
CS_kuaixiu = True
CS_kuaixiushangxian = 50
CS_attackcount = 30
CS_zhandou_zhuli = 2
CS_zhandou_peilian = 5
CS_zhandou_renwu = [0,2,1]  #前两位代表任务号，最后是普通，紧急，夜战
CS_houqin_biandui = [1,4,6,7,8]
CS_houqin_xuanze = [[0,1],[6,2],[4,1],[8,1]]
attack_count = 0
thresh_pic = 0.8
thresh_kuaixiu = 200





count = 0
zhujiemian_zhandou_enter = [947,502]
zhujiemian_houqin_confirm = [740,503]
zhujiemian_houqin_status = [18,354]
zhujiemian_houqin_status_return = [761,360]
zhujiemian_houqin_cancel = [510,503]
zhujiemian_xiufu_enter = [936,231]
zhujiemian_gongchang_enter = [1165,344]
zhandou_zuozhan = [118,161]
zhandou_houqin = [112,250]
zhandou_houqin_zhanyi_wipeup = [[271,263],[265,656]]
zhandou_houqin_zhanyi_wipedown = [[265,656],[271,263]]
zhandou_return_zhujiemian = [61,42]
zhandou_leixing = [[982,184],[1100,184],[1220,184]]
xiufu_confirm = [1192,553]
xiufu_start = [932,503]
gongchang_chaijie = [100,430]
guanbi = [655,487]
tidui_cancel = [1010,643]
single_confirm = [654,521]  #单个选项确认及取消坐标位置
tri_return = [238,102]
def xiufu_xuanze(i,j=1):#i从0开始
    if j==1:
        return [90+(i)*180,240]
    else:
        return [90+(i)*180,557]
def yuanzhengkaishi(i):
    return [280+220*i,660]
# this file determines the constant value of the scripts
scene = 0  #determined    1:
judge_prefix = './pics/judge'
battle_judge_prefix = './pics/battle_judge'
confirm_prefix = './pics/confirm'
map_prefix = './pics/map'


pic_judge = {'liebiao': os.path.join(judge_prefix, 'liebiao_judge.png'),
             'zhujiemian':os.path.join(judge_prefix,'zhujiemian_judge.png'),
             'tiduixuanze': os.path.join(judge_prefix, 'tiduixuanze_judge.png'),
             'zhandouing': os.path.join(judge_prefix, 'zhandouing_judge.png'),
             'zhandouzhunbei': os.path.join(judge_prefix, 'zhandouzhunbei_judge.png'),
             'zhandoujiangli': os.path.join(judge_prefix, 'zhandoujiangli_judge.png'),
             'zhandouend': os.path.join(judge_prefix, 'zhandouend_judge.png'),
             # 'zuozhan': os.path.join(judge_prefix, 'zuozhan_judge.png'),
             'xiufu': os.path.join(judge_prefix, 'xiufu_judge.png'),
             'houqin':os.path.join(judge_prefix,'houqin_judge.png'),
             'houqinagain': os.path.join(judge_prefix, 'houqinagain_judge.png'),
             'gonggao': os.path.join(confirm_prefix, 'gonggao.png'),
             'tanchuang': os.path.join(confirm_prefix, 'tanchuang.png'),
             'biancheng':os.path.join(judge_prefix,'biancheng_judge.png'),
             'gongchang':os.path.join(judge_prefix,'gongchang_judge.png'),
             'sushe':os.path.join(judge_prefix,'sushe_judge.png'),
             # 'yuanzheng':os.path.join(judge_prefix,'yuanzheng_judge.png'),
             'zhandou':os.path.join(judge_prefix,'zhandou_judge.png'),


             }
pic_confirm = {'liebiao': os.path.join(judge_prefix, 'liebiao_judge.png'),
             'zhujiemian':os.path.join(judge_prefix,'zhujiemian_judge.png'),
             'tiduixuanze': os.path.join(judge_prefix, 'tiduixuanze_judge.png'),
             'zhandouing': os.path.join(judge_prefix, 'zhandouing_judge.png'),
             'zhandouzhunbei': os.path.join(judge_prefix, 'zhandouzhunbei_judge.png'),
             'zhandoujiangli': os.path.join(judge_prefix, 'zhandoujiangli_judge.png'),
             'zhandouend': os.path.join(judge_prefix, 'zhandouend_judge.png'),
             'zuozhan': os.path.join(judge_prefix, 'zuozhan_judge.png'),
             'xiufu': os.path.join(judge_prefix, 'xiufu_judge.png'),
             'houqin':os.path.join(judge_prefix,'houqin_judge.png'),
             'biancheng':os.path.join(judge_prefix,'biancheng_judge.png'),
             'sushe':os.path.join(judge_prefix,'sushe_judge.png'),
             'yuanzheng':os.path.join(judge_prefix,'yuanzheng_judge.png'),
             'zhandou':os.path.join(judge_prefix,'zhandou_judge.png'),
             'houqinagain':os.path.join(judge_prefix,'houqinagain_judge.png'),
             '0zhanyi':os.path.join(confirm_prefix,'0zhanyi_confirm.png'),
             '1zhanyi':os.path.join(confirm_prefix,'1zhanyi_confirm.png'),
             '2zhanyi':os.path.join(confirm_prefix,'2zhanyi_confirm.png'),
             '3zhanyi':os.path.join(confirm_prefix,'3zhanyi_confirm.png'),
             '4zhanyi':os.path.join(confirm_prefix,'4zhanyi_confirm.png'),
             '5zhanyi':os.path.join(confirm_prefix,'5zhanyi_confirm.png'),
             '6zhanyi':os.path.join(confirm_prefix,'6zhanyi_confirm.png'),
             '7zhanyi':os.path.join(confirm_prefix,'7zhanyi_confirm.png'),
             '8zhanyi':os.path.join(confirm_prefix,'8zhanyi_confirm.png'),
             'yuanzhengsent':os.path.join(confirm_prefix,'yuanzheng_sent.png'),
             '1tidui': os.path.join(confirm_prefix, '1tidui.png'),
             '2tidui': os.path.join(confirm_prefix, '2tidui.png'),
             '3tidui': os.path.join(confirm_prefix, '3tidui.png'),
             '4tidui': os.path.join(confirm_prefix, '4tidui.png'),
             '5tidui': os.path.join(confirm_prefix, '5tidui.png'),
             '6tidui': os.path.join(confirm_prefix, '6tidui.png'),
             '7tidui': os.path.join(confirm_prefix, '7tidui.png'),
             '8tidui': os.path.join(confirm_prefix, '8tidui.png'),
             'xiufu_xuanze': os.path.join(confirm_prefix, 'xiufu_xuanze.png'),
             'chaijie_2xing': os.path.join(confirm_prefix, 'chaijie_2xing.png'),
             'chaijie_confirm': os.path.join(confirm_prefix, 'chaijie_confirm.png'),
             'chaijie_xuanze_juese': os.path.join(confirm_prefix, 'chaijie_xuanze_juese.png'),
             'wuxiufu': os.path.join(confirm_prefix, 'wuxiufu.png'),
             'kuaixiu': os.path.join(confirm_prefix, 'kuaixiu.png'),
             'zhandou_enter': os.path.join(confirm_prefix, 'zhandou_enter.png'),
             '5-4-2': os.path.join(confirm_prefix, '5-4-2.png'),
             '5-4-2map': os.path.join(map_prefix, '5-4-2.png'),
             '0-2-1': os.path.join(confirm_prefix, '0-2-1.png'),
             '0-2-1map': os.path.join(map_prefix, '0-2-1.png'),
             'ditu_wudian1': os.path.join(confirm_prefix, 'ditu_wudian1.png'),
             'ditu_wudian2': os.path.join(confirm_prefix, 'ditu_wudian1.png'),
             'jihuamoshi': os.path.join(confirm_prefix, 'jihuamoshi.png'),
             'renxingman': os.path.join(confirm_prefix, 'renxingman1.png'),
             '4jihua': os.path.join(map_prefix, '4jihua.png'),
               '31jihua': os.path.join(map_prefix, '31jihua.png'),
             'cancel':os.path.join(confirm_prefix,'cancel.png'),
             'kuaisuxiufu':os.path.join(confirm_prefix,'kuaisuxiufu.png'),
             'chaijie': os.path.join(confirm_prefix, 'chaijie.png'),
           'gongchang': os.path.join(judge_prefix, 'gongchang_judge.png'),
           'kuaixiu_confirm': os.path.join(confirm_prefix, 'kuaixiu_confirm.png'),
           'gonggao': os.path.join(confirm_prefix, 'gonggao.png'),
           'jihuaxuanzhong': os.path.join(confirm_prefix, 'jihuaxuanzhong.png'),
           'jieshuhuihe': os.path.join(confirm_prefix, 'jieshuhuihe.png'),
            'tanchuang': os.path.join(confirm_prefix, 'tanchuang.png'),
             }
battle_judge = {'total_end': os.path.join(battle_judge_prefix, 'total_end.png'),
'zhandouend': os.path.join(battle_judge_prefix, 'zhandouend_judge.png'),
'zhandouing': os.path.join(battle_judge_prefix, 'zhandouing_judge.png'),
'zhandoujiangli': os.path.join(battle_judge_prefix, 'zhandoujiangli_judge.png'),
             }


tiaochu_judge = {''}
action_confirm = [os.path.join(confirm_prefix,'zhujiemian_judge.png')]
yuanzheng_num = './pics/yuanzheng_exist.png'

yuanzheng_log = './log_yuanzheng.txt'
zuozhan_log = './log_zuozhan.txt'

zhandou_suoxiao = [[170,670],[370,670]]


#zuobian
tidui_confirm = [1180,640]
click = [640,520]


