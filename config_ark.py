import os
#明日方舟预载入配置信息 2019-6-3 版本
THRESH_PIC = 0.8
BATTLE_WAIT = 15
DRAG_SPEED = 20
BUSHU_OFFSET = 300
IMG_SAVE = "./abnormal_ark"

YUANSHI = 0
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
points["kongbai"] = [200,1000]
points["peizhi_enter"] = [1741,990]
points["zhandou_start"] = [1650,800]
points["daili"] = [1725,890]
points["zhandou_pause"] = [1797,80]
points["zhandou_enter"] = [1460,300]
points["yuanshi_ok"] = [1420,813]
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
guanqia_pic = {
    "1-11": os.path.join(guanqia_path, "1-11.png"),
    "1-11_confirm": os.path.join(guanqia_path, "1-11_confirm.png"),
    "LS-5": os.path.join(guanqia_path, "LS-5.png"),
    "LS-5_confirm": os.path.join(guanqia_path, "LS-5_confirm.png"),
    "CE-5": os.path.join(guanqia_path, "CE-5.png"),
    "CE-5_confirm": os.path.join(guanqia_path, "CE-5_confirm.png"),
    "AP-5": os.path.join(guanqia_path, "AP-5.png"),
    "AP-5_confirm": os.path.join(guanqia_path, "AP-5_confirm.png"),
    "SK-5": os.path.join(guanqia_path, "SK-5.png"),
    "SK-5_confirm": os.path.join(guanqia_path, "SK-5_confirm.png"),
    "SK-3": os.path.join(guanqia_path, "SK-3.png"),
    "SK-3_confirm": os.path.join(guanqia_path, "SK-3_confirm.png"),
    "S2-12": os.path.join(guanqia_path, "S2-12.png"),
    "S2-12_confirm": os.path.join(guanqia_path, "S2-12_confirm.png"),
}
pic_where = {
    "gonggao": os.path.join(pic_path,"gonggao.png"),
    "zhujiemian": os.path.join(pic_path,"zhandou.png"),
    "zhandou_xuanze": os.path.join(pic_path,"zhandou_jiemian.png"),
    "huodongjiemian": os.path.join(pic_path,"zhandou_huodong_enter.png"),
    "huodong_xuanze": os.path.join(pic_path,"zhandou_huodong_confirm.png"),
    "zhandou_start": os.path.join(pic_path,"zhandou_start.png"),
    "zhandou_ing": os.path.join(pic_path,"zhandouing.png"),
    "zhandou_end": os.path.join(pic_path,"zhandou_end.png"),
    "yuanshi_lizhi": os.path.join(pic_path, "yuanshi_lizhi.png"),
    "enter_quick": os.path.join(pic_path, "enter_quick.png"),
    "skip": os.path.join(pic_path, "skip.png"),
    "zhandou_failed": os.path.join(pic_path, "mission_failed.png"),

}
pic_huodong = {
    "GT2": os.path.join(huodong_path,"huodong_GT2.png"),
    "GT3": os.path.join(huodong_path,"huodong_GT3.png"),
    "GT4": os.path.join(huodong_path,"huodong_GT4.png"),
    "GT5": os.path.join(huodong_path,"huodong_GT5.png"),
    "GT6": os.path.join(huodong_path,"huodong_GT6.png"),
    "huodong_enter": os.path.join(huodong_path,"zhandou_huodong1.png"),
}

pic_confirm = {
    "GT2": os.path.join(huodong_path, "huodong_GT2_confirm.png"),
    "GT3": os.path.join(huodong_path, "huodong_GT3_confirm.png"),
    "GT4": os.path.join(huodong_path, "huodong_GT4_confirm.png"),
    "GT5": os.path.join(huodong_path, "huodong_GT5_confirm.png"),
    "GT6": os.path.join(huodong_path, "huodong_GT6_confirm.png"),
    "daili_do": os.path.join(pic_path, "daili_do.png"),
    "daili_undo": os.path.join(pic_path, "daili_undo.png"),
    "zhandou_pause": os.path.join(pic_path, "zhandou_pause.png"),
    "daili_confirm": os.path.join(pic_path, "daili_confirm.png"),
    "enter_quick": os.path.join(pic_path,"enter_quick.png"),
    "zhandou_quickenter": os.path.join(pic_path,"zhandou_quickenter.png"),
    "yuanshi_lizhi": os.path.join(pic_path,"yuanshi_lizhi.png"),
    "bushu_fangxiang": os.path.join(pic_path,"bushu_fangxiang.png"),
    "2xspeed": os.path.join(pic_path,"2xspeed.png"),
    "1xspeed": os.path.join(pic_path, "1xspeed.png"),
    "chapter1": os.path.join(pic_path, "chapter1.png"),
    "chapter2": os.path.join(pic_path, "chapter2.png"),
    "chapter3": os.path.join(pic_path, "chapter3.png"),
    "chapter4": os.path.join(pic_path, "chapter4.png"),
    "gouliang": os.path.join(pic_path, "gouliang.png"),
    "hongpiao": os.path.join(pic_path, "hongpiao.png"),
    "jiancai": os.path.join(pic_path, "jiancai.png"),
    "longmenbi": os.path.join(pic_path, "longmenbi.png"),
    "skip": os.path.join(pic_path, "skip.png"),
    "skip_confirm": os.path.join(pic_path, "skip_confirm.png"),
    "zhuxian": os.path.join(pic_path, "zhandou_jiemian.png"),
    "wuzichoubei": os.path.join(pic_path, "wuzichoubei.png"),
    "xinpiansousuo": os.path.join(pic_path, "xinpiansousuo.png"),
    "LS": os.path.join(pic_path, "gouliang.png"),
    "AP": os.path.join(pic_path, "hongpiao.png"),
    "SK": os.path.join(pic_path, "jiancai.png"),
    "CE": os.path.join(pic_path, "longmenbi.png"),
}
pic_others = {
    "daili_undo": os.path.join(pic_path,"daili_undo.png"),
    "daili_do": os.path.join(pic_path,"daili_do.png"),
    "zhandou_pause": os.path.join(pic_path,"zhandou_pause.png")

}
