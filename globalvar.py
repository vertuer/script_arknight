class global_val:
    max_resolution = [1920,1080] #图片素材的分辨率
    window_resolution = [0,0]    #当前模拟器的分辨率
    yuanshi_used = 0             #已经碎石的数量

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