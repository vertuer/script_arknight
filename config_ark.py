import os
#明日方舟预载入配置信息 2019-6-3 版本
THRESH_PIC = 0.8
BATTLE_WAIT = 15
IMG_SAVE = "./abnormal_ark"
YUANSHI = 0
LOG_PATH = "./log/"
pic_path = "./ark_images/processed"
assert(os.path.isdir(pic_path))
if os.path.exists(IMG_SAVE):
    pass
else:
    os.makedirs(IMG_SAVE)
points = {}
points["kongbai"] = [650,700]
points["peizhi_enter"] = [1741,990]
points["zhandou_start"] = [1650,800]
points["daili"] = [1725,890]
points["zhandou_pause"] = [1797,80]
points["zhandou_enter"] = [1460,300]
points["yuanshi_ok"] = [1420,813]
points["yuanshi_no"] = [463,813]
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


pic_where = {
    "gonggao": os.path.join(pic_path,"gonggao.png"),
    "zhujiemian": os.path.join(pic_path,"zhandou.png"),
    "zhandou_xuanze": os.path.join(pic_path,"zhandou_jiemian.png"),
    "huodongjiemian": os.path.join(pic_path,"zhandou_huodong_enter.png"),
    "huodong_xuanze": os.path.join(pic_path,"zhandou_huodong_confirm.png"),
    "zhandou_start": os.path.join(pic_path,"zhandou_start.png"),
    "zhandou_ing": os.path.join(pic_path,"zhandou_ing.png"),
    "zhandou_end": os.path.join(pic_path,"zhandou_end.png"),
    "yuanshi_lizhi": os.path.join(pic_path, "yuanshi_lizhi.png"),
    "enter_quick": os.path.join(pic_path, "enter_quick.png"),
}
pic_huodong = {
    "GT2": os.path.join(pic_path,"huodong_GT2.png"),
    "GT3": os.path.join(pic_path,"huodong_GT3.png"),
    "GT4": os.path.join(pic_path,"huodong_GT4.png"),
    "GT5": os.path.join(pic_path,"huodong_GT5.png"),
    "GT6": os.path.join(pic_path,"huodong_GT6.png"),
    "huodong_enter": os.path.join(pic_path,"zhandou_huodong1.png"),
}

pic_confirm = {
    "GT2": os.path.join(pic_path, "huodong_GT2_confirm.png"),
    "GT3": os.path.join(pic_path, "huodong_GT3_confirm.png"),
    "GT4": os.path.join(pic_path, "huodong_GT4_confirm.png"),
    "GT5": os.path.join(pic_path, "huodong_GT5_confirm.png"),
    "GT6": os.path.join(pic_path, "huodong_GT6_confirm.png"),
    "daili_do": os.path.join(pic_path, "daili_do.png"),
    "daili_undo": os.path.join(pic_path, "daili_undo.png"),
    "zhandou_pause": os.path.join(pic_path, "zhandou_pause.png"),
    "daili_confirm": os.path.join(pic_path, "daili_confirm.png"),
    "enter_quick": os.path.join(pic_path,"enter_quick.png"),
    "zhandou_quickenter": os.path.join(pic_path,"zhandou_quickenter.png"),
    "yuanshi_lizhi": os.path.join(pic_path,"yuanshi_lizhi.png"),
}
pic_others = {
    "daili_undo": os.path.join(pic_path,"daili_undo.png"),
    "daili_do": os.path.join(pic_path,"daili_do.png"),
    "zhandou_pause": os.path.join(pic_path,"zhandou_pause.png")

}
