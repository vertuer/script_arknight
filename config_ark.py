import os
import globalvar
from PIL import Image
#from basic_function import get_handle
import numpy as np
#明日方舟预载入配置信息 2019-6-3 版本

BATTLE_WAIT = 10
BUSHU_OFFSET = 300
IMG_SAVE = "./abnormal_ark"
CONFIG_PATH = "./config"
LOG_PATH = "./log/"
pic_path = "./ark_images/processed"
staff_pic_path = "./ark_images/staff"
guanqia_path = "./ark_images/processed/guanqia"
huodong_path = "./ark_images/processed/huodong"


assert(os.path.isdir(pic_path))
if os.path.exists(IMG_SAVE):
    pass
else:
    os.makedirs(IMG_SAVE)

drag_left = [[580,539],[880,543]]
points = {}
points["kongbai"] = [1000,1000]
points["peizhi_enter"] = [1741,990]
points["zhandou_start"] = [1650,800]
points["daili"] = [1725,890]
points["zhandou_pause"] = [1797,80]
points["zhandou_enter"] = [1460,300]
points["yuanshi_ok"] = [1420,813]
points['tili_ok'] = [1637,870]
points["yuanshi_no"] = [463,813]
points["skip_yes"] = [1270,775]
points["drag_left"] = [[580,539],[880,543]]
points["drag_right"] = [[880,543],[580,539]]
points["1-11-target-xy"] = [[949,510],[790,629],[649,649],
                            [807,381],[946,285],[936,774]]
class ReturnToWhere(Exception):
    # the error is triggled when it should go somewhere
    def __init__(self,where):
        self._where = where
    @property
    def where(self):
        return self._where

class ExitError(Exception):
    # fatal error, the program should exit
    pass

staff_pic = {
    "hj": os.path.join(staff_pic_path,"hj.png"),
    "12F": os.path.join(staff_pic_path,"12F.png"),
    "ase": os.path.join(staff_pic_path,"ase.png"),
    "longmenbi": os.path.join(staff_pic_path,"longmenbi.png"),
    "mgl": os.path.join(staff_pic_path,"mgl.png"),
    "ry": os.path.join(staff_pic_path,"ry.png"),
    "sdhd": os.path.join(staff_pic_path,"sdhd.png"),

}
staff_pic_res = {}
for i in staff_pic.keys():
    staff_pic_res[i] = [1920,1080]

def get_confirm_pic():
    confirm_pic = {}
    confirm_pic_res = {}
    with open(os.path.join(CONFIG_PATH,"pic_confirm"),'r',encoding='utf-8') as file:
        while(1):
            tmp = file.readline()
            if not tmp:
                break
            tmp = tmp.split(' ')
            confirm_pic[tmp[0]] = tmp[1]
            confirm_pic_res[tmp[0]] = [int(tmp[2]),int(tmp[3].strip('\n'))]
    file.close()
    return confirm_pic,confirm_pic_res
def get_guanqia_pic():
    guanqia_pic = {}
    guanqia_pic_res = {}
    with open(os.path.join(CONFIG_PATH,"guanqia"),'r',encoding='utf-8') as file:
        while(1):
            tmp = file.readline()
            if tmp in ['\n',' ']:
                continue
            if not tmp:
                break
            tmp = tmp.split(' ')
            guanqia_pic[tmp[0]] = tmp[1]
            guanqia_pic_res[tmp[0]] = [int(tmp[2]),int(tmp[3].strip('\n'))]
    file.close()
    return guanqia_pic,guanqia_pic_res
def get_huodong_pic():
    huodong_pic = {}
    huodong_pic_res = {}
    with open(os.path.join(CONFIG_PATH,"pic_huodong"),'r',encoding='utf-8') as file:
        while(1):
            tmp = file.readline()
            if not tmp:
                break
            tmp = tmp.split(' ')
            huodong_pic[tmp[0]] = tmp[1]
            huodong_pic_res[tmp[0]] = [int(tmp[2]),int(tmp[3].strip('\n'))]
    file.close()
    return huodong_pic,huodong_pic_res
pic_confirm,pic_confirm_res = get_confirm_pic()
guanqia_pic,guanqia_pic_res = get_guanqia_pic()
huodong_pic,huodong_pic_res = get_huodong_pic()
def ChapterCTE(chapter):
    reverse_mapping = {'主线':'ZX','物资筹备':'WZ','芯片获取':'PR','活动':'HD'}
    # reverse_mapping = {'第一章':'1','第二章':'2','第三章':'3','第四章':'4','第五章':'5',
    #                    '经验本':'LS','红票子':'AP','龙门币':'CE','建材':'SK','活动':'HD'}
    return reverse_mapping[chapter]
def ChapterETC(chapter):
    mapping_keys = {'ZX':'主线','WZ':'物资筹备','PR':'芯片获取','HD':'活动'}
    # mapping_keys = {'1':'第一章','2':'第二章','3':'第三章','4':'第四章','5':'第五章',
    #               'LS':'经验本','AP':'红票子','CE':'龙门币','SK':'建材','HD':'活动'}
    return mapping_keys[chapter]

def get_img_path(name,huodong=False):
    if huodong:
        return huodong_pic[name]
    else:
        return guanqia_pic[name]
def get_img_res(name,huodong=False):
    if huodong:
        return huodong_pic_res[name]
    else:
        return guanqia_pic_res[name]

def get_guanqia(guanqia_pic,pic_huodong):
    tmp1 = list(guanqia_pic.keys())
    tmp2 = list(pic_huodong.keys())
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

    guanqia_dict = {'主线': {}, '物资筹备': {}, '芯片获取': {}, '活动': {}}
    for i in tmp_guanqia:
        tmp_split = i.split('|')
        total_class = tmp_split[0]
        map_total_class = ChapterETC(total_class)
        chapter = tmp_split[1]
        if len(tmp_split)==3:
            name = tmp_split[2]
        if chapter in guanqia_dict[map_total_class]:
            if len(tmp_split)==2:
                #章节
                pass
            else:
                guanqia_dict[map_total_class][chapter].append(name)
        else:
            if len(tmp_split)==2:
                #章节
                guanqia_dict[map_total_class][chapter] = []
            else:
                guanqia_dict[map_total_class][chapter] = [name]
    return guanqia_dict

def pic_resize(pic_path,window_resolution,max_resolution):
    if isinstance(pic_path,np.ndarray):
        temp_im = pic_path
        temp_im = Image.fromarray(temp_im)
    else:
        temp_im = Image.open(pic_path)
        temp_im = temp_im.convert("RGB")
    im_w= temp_im.size[0]
    im_h = temp_im.size[1]
    width = int(window_resolution[0] / max_resolution[0] * im_w)
    height = int(window_resolution[1] / max_resolution[1] * im_h)
    temp_im = temp_im.resize((width, height), Image.ANTIALIAS)
    return np.array(temp_im)
def pic_load_ram():
    #must run after getting handle, when dealing with the pics which resolutions lower than the current one,
    # the function should remove these pics which may cause unpredictable errors
    window_resolution = globalvar.get_window_resolution()
    max_resolution = globalvar.get_max_resolution()
    if window_resolution[0]==0:
        raise Exception("未检测到模拟器")
    for keys,pic_path in pic_confirm.items():
        temp_im = pic_resize(pic_path,window_resolution,pic_confirm_res[keys])
        pic_confirm[keys] = np.array(temp_im)
    for keys, pic_path in huodong_pic.items():
        temp_im = pic_resize(pic_path,window_resolution,huodong_pic_res[keys])
        huodong_pic[keys] = np.array(temp_im)

    for keys, pic_path in pic_where.items():
        temp_im = pic_resize(pic_path,window_resolution,pic_where_res[keys])
        pic_where[keys] = np.array(temp_im)

    for keys, pic_path in staff_pic.items():
        temp_im = pic_resize(pic_path,window_resolution,staff_pic_res[keys])
        staff_pic[keys] = np.array(temp_im)

    for keys, pic_path in guanqia_pic.items():
        temp_im = pic_resize(pic_path,window_resolution,guanqia_pic_res[keys])
        guanqia_pic[keys] = np.array(temp_im)
    #常量点 自定义分辨率适应
    for keys,values in points.items():
        if isinstance(values[0],int):
            width = int(window_resolution[0] / max_resolution[0] * values[0])
            height = int(window_resolution[1] / max_resolution[1] * values[1])
            points[keys] = [width, height]
        else:
            for index,value_temp in enumerate(values):
                width = int(window_resolution[0] / max_resolution[0] * value_temp[0])
                height = int(window_resolution[1] / max_resolution[1] * value_temp[1])
                values[index] = [width, height]
            points[keys] = values
# guanqia_pic = {
#     "1-11": os.path.join(guanqia_path, "1-11.png"),
#     "1-11_confirm": os.path.join(guanqia_path, "1-11_confirm.png"),
#     "1-7": os.path.join(guanqia_path, "1-7.png"),
#     "1-7_confirm": os.path.join(guanqia_path, "1-7_confirm.png"),
#     "LS-5": os.path.join(guanqia_path, "LS-5.png"),
#     "LS-5_confirm": os.path.join(guanqia_path, "LS-5_confirm.png"),
#     "CE-5": os.path.join(guanqia_path, "CE-5.png"),
#     "CE-5_confirm": os.path.join(guanqia_path, "CE-5_confirm.png"),
#     "AP-5": os.path.join(guanqia_path, "AP-5.png"),
#     "AP-5_confirm": os.path.join(guanqia_path, "AP-5_confirm.png"),
#     "SK-5": os.path.join(guanqia_path, "SK-5.png"),
#     "SK-5_confirm": os.path.join(guanqia_path, "SK-5_confirm.png"),
#     "SK-3": os.path.join(guanqia_path, "SK-3.png"),
#     "SK-3_confirm": os.path.join(guanqia_path, "SK-3_confirm.png"),
#     "S2-12": os.path.join(guanqia_path, "S2-12.png"),
#     "S2-12_confirm": os.path.join(guanqia_path, "S2-12_confirm.png"),
# }
pic_where = {
    "gonggao": os.path.join(pic_path,"gonggao.png"),
    "zhujiemian": os.path.join(pic_path,"zhandou.png"),
    "zhandou_xuanze": os.path.join(pic_path,"guanqia","zhandou_jiemian.png"),
    "huodong_xuanze": os.path.join(huodong_path,"zhandou_huodong_confirm.png"),
    "zhandou_start": os.path.join(pic_path,"zhandou_start.png"),
    "zhandou_ing": os.path.join(pic_path,"zhandouing.png"),
    "zhandou_end": os.path.join(pic_path,"zhandou_end.png"),
    "yuanshi_lizhi": os.path.join(pic_path, "yuanshi_lizhi.png"),
    "enter_quick": os.path.join(pic_path, "enter_quick.png"),
    "skip": os.path.join(pic_path, "skip.png"),
    "zhandou_failed": os.path.join(pic_path, "mission_failed.png"),
    #门票不足
}
pic_where_res = {}
for i in pic_where.keys():
    pic_where_res[i] = [1920,1080]
# pic_huodong = {
#     "GT2": os.path.join(huodong_path,"huodong_GT2.png"),
#     "GT3": os.path.join(huodong_path,"huodong_GT3.png"),
#     "GT4": os.path.join(huodong_path,"huodong_GT4.png"),
#     "GT5": os.path.join(huodong_path,"huodong_GT5.png"),
#     "GT6": os.path.join(huodong_path,"huodong_GT6.png"),
#     "GT2_confirm": os.path.join(huodong_path, "huodong_GT2_confirm.png"),
#     "GT3_confirm": os.path.join(huodong_path, "huodong_GT3_confirm.png"),
#     "GT4_confirm": os.path.join(huodong_path, "huodong_GT4_confirm.png"),
#     "GT5_confirm": os.path.join(huodong_path, "huodong_GT5_confirm.png"),
#     "GT6_confirm": os.path.join(huodong_path, "huodong_GT6_confirm.png"),
#     "huodong_enter": os.path.join(huodong_path,"zhandou_huodong1.png"),
# }

# pic_confirm = {
#     "60tili": os.path.join(pic_path, "60ti.png"),
#     "100tili": os.path.join(pic_path, "100ti.png"),
#     "daili_do": os.path.join(pic_path, "daili_do.png"),
#     "daili_undo": os.path.join(pic_path, "daili_undo.png"),
#     "zhandou_pause": os.path.join(pic_path, "zhandou_pause.png"),
#     "daili_confirm": os.path.join(pic_path, "daili_confirm.png"),
#     "enter_quick": os.path.join(pic_path,"enter_quick.png"),
#     "zhandou_quickenter": os.path.join(pic_path,"zhandou_quickenter.png"),
#     "yuanshi_lizhi": os.path.join(pic_path,"yuanshi_lizhi.png"),
#     "bushu_fangxiang": os.path.join(pic_path,"bushu_fangxiang.png"),
#     "2xspeed": os.path.join(pic_path,"2xspeed.png"),
#     "1xspeed": os.path.join(pic_path, "1xspeed.png"),
#     "chapter1": os.path.join(pic_path, "chapter1.png"),
#     "chapter2": os.path.join(pic_path, "chapter2.png"),
#     "chapter3": os.path.join(pic_path, "chapter3.png"),
#     "chapter4": os.path.join(pic_path, "chapter4.png"),
#     "gouliang": os.path.join(pic_path, "gouliang.png"),
#     "hongpiao": os.path.join(pic_path, "hongpiao.png"),
#     "jiancai": os.path.join(pic_path, "jiancai.png"),
#     "longmenbi": os.path.join(pic_path, "longmenbi.png"),
#     "skip": os.path.join(pic_path, "skip.png"),
#     "skip_confirm": os.path.join(pic_path, "skip_confirm.png"),
#     "zhuxian": os.path.join(pic_path, "zhandou_jiemian.png"),
#     "wuzichoubei": os.path.join(pic_path, "wuzichoubei.png"),
#     "xinpiansousuo": os.path.join(pic_path, "xinpiansousuo.png"),
#     "LS": os.path.join(pic_path, "gouliang.png"),
#     "AP": os.path.join(pic_path, "hongpiao.png"),
#     "SK": os.path.join(pic_path, "jiancai.png"),
#     "CE": os.path.join(pic_path, "longmenbi.png"),
# }
pic_others = {
    "daili_undo": os.path.join(pic_path,"daili_undo.png"),
    "daili_do": os.path.join(pic_path,"daili_do.png"),
    "zhandou_pause": os.path.join(pic_path,"zhandou_pause.png")

}


if __name__ == "__main__":
    # file = open('./config/guanqia','w')
    # for i in guanqia_pic.keys():
    #     file.write("{} {}\n".format(i,guanqia_pic[i]))
    # file.close()
    print(123)
