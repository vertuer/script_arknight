import os
class global_val:
    max_resolution = [1920,1080] #图片素材的分辨率
    window_resolution = [0,0]    #当前模拟器的分辨率
    yuanshi_used = 0             #已经碎石的数量
    thresh_pic = 0.8
    drag_speed = 20
    yuanshi = 0
    duochong = True   #是否多重验证
    CONFIG_FILE = "./config.txt"
    handle_infor = []
    assert (os.path.exists(CONFIG_FILE))
    file = open(CONFIG_FILE, 'r')
    while True:
        text_line = file.readline()
        if text_line:
            handle_infor.append(text_line.split("\n")[0])
        else:
            file.close()
            break
def set_thresh_pic(value):
    global_val.thresh_pic = value
def get_thresh_pic():
    return global_val.thresh_pic
def set_drag_speed(value):
    global_val.drag_speed = value
def get_drag_speed():
    return global_val.drag_speed
def set_yuanshi(value):
    global_val.yuanshi = value
def get_yuanshi():
    return global_val.yuanshi
def get_max_resolution():
    return global_val.max_resolution
def get_window_resolution():
    return global_val.window_resolution
def set_window_resolution(value):
    if len(value)!=2:
        raise Exception("window resolution shape isn't right\n")
    global_val.window_resolution = value

def get_yuanshi_used():
    return global_val.yuanshi_used
def yuanshi_used_add(value):
    global_val.yuanshi_used += value
def get_handle_infor():
    return global_val.handle_infor