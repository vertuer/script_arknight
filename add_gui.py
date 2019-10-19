#from PIL import Image
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import wx
import os
# OpenCV
import cv2
import config_ark
from basic_function import get_handle,prtsc,pic_locate
import numpy as np
import globalvar


class TREE():
    @staticmethod
    def get_children(tree, item):
        children = []
        (tmp, cookie) = tree.GetFirstChild(item)
        while tmp.IsOk():
            children.append(tree.GetItemText(tmp))
            (tmp, cookie) = tree.GetNextChild(tmp, cookie)
        return children

class SubclassDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '请选择关卡图库类型',
                           size=(300, 100))
        okButton = wx.Button(self, wx.ID_OK, "关卡图库", pos=(15, 15))
        okButton.SetDefault()
        cancelButton = wx.Button(self, wx.ID_CANCEL, "关卡确认图库",
                                 pos=(115, 15))

class MyFrame1(wx.Frame):
    def __init__(self, parent, pathToImage=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(900,650), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        # relative data
        self.cut_img = None
        self.origin_img = None
        self.handle = None
        self.draws = []
        self.guanqia_save = {}
        self.TotalChapter = [u'chapter1', u'chapter2', u'chapter3', u'chapter4', u'chapter5', u'活动']  # 第一级菜单
        # Use English dialog
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)


        # Intitialise the matplotlib figure
        # self.figure = plt.figure(facecolor='gray')
        self.figure = Figure(facecolor='gray')
        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure, [0, 0, 1, 1])
        self.axes.set_axis_off()
        self.figure.add_axes(self.axes)

        # Add the figure to the wxFigureCanvas
        self.canvas = FigureCanvas(self, -1, self.figure)

        #关卡选择choice窗体
        # choices = ["Alpha", "Baker", "Charlie", "Delta"]
        # self.dialog = wx.ListBox(choices = choices, id=wx.ID_ANY,name='listBox1',
        #                          parent=self, pos=(650,240),size=wx.Size(80, 80), style=0)


        # Add Button and Progress Bar
        self.openBtn = wx.Button(self, -1, "打开文件", pos=(650, 30), size=(70, 40))
        self.simBtn = wx.Button(self, -1, "模拟器图像载入", pos=(740, 30), size=(100, 40))
        self.srcBtn = wx.Button(self, -1, "查看截图", pos=(250, 520), size=(150, 50))
        self.matchBtn = wx.Button(self, -1, "开始图像匹配", pos=(650, 160), size=(80, 40))
        # self.check = wx.CheckBox(self, -1, "一级菜单", pos=(650, 340), size=(70, 20))
        # self.chapterChoice = wx.Choice(self, wx.ID_ANY, (650, 365), (80, 30), self.TotalChapter, 0)
        # self.chapterChoice.SetSelection(0)
        # self.inputIntroText = wx.StaticText(self, -1, u"关卡或章节（活动）名称", pos=(730, 340), size=(175, 25))
        # self.inputText = wx.TextCtrl(self, -1, "", pos=(740, 365), size=(120, 25))
        # self.saveBtn = wx.Button(self, -1, "保存截图", pos=(760, 430), size=(100, 50))
        # yuanshi_choiceChoices = [u"No！", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10"]
        # self.yuanshi_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, yuanshi_choiceChoices, 0)
        # self.yuanshi_choice.SetSelection(0)
        #self.scoreText = wx.StaticText(self, wx.ID_ANY, u"识图分数:", (650, 120), (60, 40), 0)
        #self.scoreText2 = wx.StaticText(self, wx.ID_ANY, u"", (710, 120), (50, 40), 0)
        self.scoreText3 = wx.StaticText(self, wx.ID_ANY, u"截图来源分辨率:", (650, 120), (100, 40), 0)
        self.scoreText4 = wx.StaticText(self, wx.ID_ANY, u"", (750, 120), (80, 40), 0)
        guanqia_pic,_ = config_ark.get_guanqia_pic()
        huodong_pic,_ = config_ark.get_huodong_pic()
        self.guanqia_dict = config_ark.get_guanqia(guanqia_pic,huodong_pic)
        self.tree = wx.TreeCtrl(self,id=wx.ID_ANY,pos=(650,220),size=(220,130))
        # self.imglist = wx.ImageList(16, 16, True, 2)
        # self.imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        # self.imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        # self.tree.AssignImageList(self.imglist)
        root = self.tree.AddRoot('root')

        for i in self.guanqia_dict.keys():
            total_class = self.tree.AppendItem(root,i)
            for j in self.guanqia_dict[i].keys():
                chapter = self.tree.AppendItem(total_class,j)
                for k in self.guanqia_dict[i][j]:
                    self.tree.AppendItem(chapter,k)
        self.tree.Expand(root)
        self.Bind(wx.EVT_BUTTON,self.get_score,self.matchBtn)
        self.Bind(wx.EVT_BUTTON,self.show_cut_img,self.srcBtn)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK,self.tree_click,self.tree)
        #self.check.Bind(wx.EVT_CHECKBOX, self.onCheck)
        self.Bind(wx.EVT_BUTTON, self.getSimPic, self.simBtn)
        self.Bind(wx.EVT_BUTTON, self.load, self.openBtn)
        #self.Bind(wx.EVT_BUTTON, self.save, self.saveBtn)
        # self.Bind(wx.EVT_BUTTON,self.front,self.frontBtn)
        # self.Bind(wx.EVT_BUTTON,self.next,self.nextBtn)

        # Initialise the rectangle
        self.rect = Rectangle((0, 0), 0, 0, facecolor='None', edgecolor='red')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.axes.add_patch(self.rect)

        # The list of the picture(absolute path)
        self.fileList = []

        # Picture name
        self.picNameList = []

        # Picture index in list
        self.count = 0

        # Cut from the picture of the rectangle
        self.cut_img = None

        # Connect the mouse events to their relevant callbacks
        self.canvas.mpl_connect('button_press_event', self._onPress)
        self.canvas.mpl_connect('button_release_event', self._onRelease)
        self.canvas.mpl_connect('motion_notify_event', self._onMotion)

        # Lock to stop the motion event from behaving badly when the mouse isn't pressed
        self.pressed = False

        # If there is an initial image, display it on the figure
        if pathToImage is not None:
            self.setImage(pathToImage)
    #图像匹配
    def get_score(self,event):
        # if self.handle==None:
        #     self.handle = get_handle()
        # im = prtsc(self.handle)
        if isinstance(self.origin_img,np.ndarray) and isinstance(self.cut_img,np.ndarray):
            pass
        else:
            wx.MessageBox("请先载入并裁剪相应图像")
            return
        im = self.origin_img
        #changed to BGR aligned to the cv2
        #im = im [:,:,::-1]
        window_resolution = globalvar.get_window_resolution()
        max_resolution = self.origin_res
        match_im = config_ark.pic_resize(self.cut_img,window_resolution,max_resolution)
        results = pic_locate(match_im,im,0.8,True,True)
        if results:
            for i in results:
                pos = i['rectangle'][0]
                width = i['rectangle'][2][0] - i['rectangle'][0][0]
                height = i['rectangle'][1][1] - i['rectangle'][0][1]
        # Draw the bounding rectangle
                #self.rect = Rectangle((0, 0), 0, 0, facecolor='None', edgecolor='red')
                #self.axes.add_patch(self.rect)
                tmp_rect = Rectangle((0, 0), 0, 0, facecolor='None', edgecolor='red')
                tmp_rect.set_width(width)
                tmp_rect.set_height(height)
                tmp_rect.set_xy(pos)
                self.axes.add_patch(tmp_rect)
                #tmp_rect.remove()
                self.draws.append(tmp_rect)
                #self.text = plt.text(pos[0],pos[1],"{0:.4f}".format(i['confidence']))
                tmp_text = self.axes.text(pos[0],pos[1],"{0:.3f}".format(i['confidence']),fontdict={'color':'red','size':12},
                                          bbox=dict(facecolor='white', alpha=0.8))
                #tmp_text.remove()
                self.draws.append(tmp_text)
            self.canvas.draw()
            for j in self.draws:
                j.remove()
            self.draws = []

    def getSimPic(self,event):
        # 获取模拟器当前图像信息
        self.handle = get_handle()
        im = prtsc(self.handle)
        im = im[:,:,::-1]
        self.origin_img = im
        self.origin_res = [self.origin_img.shape[1], self.origin_img.shape[0]]
        self.setImage(im)

    # GetFilesPath with the end with .jpg or .png
    def getFilesPath(self, path):
        filesname = []
        dirs = os.listdir(path)
        for i in dirs:
            if os.path.splitext(i)[1] == ".jpg" or os.path.splitext(i)[1] == ".png":
                filesname += [path + "/" + i]
                self.picNameList += [i[:-4]]
        return filesname

    # Load Picture button function
    def load(self, event):
        filesFilter = "JPEG|*.jpg|PNG|*.png|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "choose pic", wildcard=filesFilter, style=wx.DD_DEFAULT_STYLE)
        # dlg = wx.DirDialog(self,"Choose File",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            if filepath:
                self.origin_img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), -1)
                #self.origin_img = cv2.imread(filepath)
                self.setImage(filepath)
                #self.origin_res = [self.origin_img.shape[1],self.origin_img.shape[0]]
                self.scoreText4.SetLabel('{},{}'.format(self.origin_res[0],self.origin_res[1]))
            else:
                print("list null")
        dlg.Destroy()

    #右键tree时触发
    def tree_click(self,event):
        pos = event.GetPoint()
        pos_ctrl = self.tree.GetPosition()
        pos = pos + pos_ctrl
        items = event.GetItem()
        tmp_parent = self._get_tree_struct()
        self.popmenu = wx.Menu()
        num_level = len(tmp_parent)
        if num_level is 2:
            self.popmenu.Append(-1,'修改图库')
            tmp = self.popmenu.Append(-1, '载入图库')
            self.Bind(wx.EVT_MENU,self.show_pic,tmp)
            tmp = self.popmenu.Append(-1,'添加章节')
            self.Bind(wx.EVT_MENU,self.save_chapter,tmp)
        elif num_level is 3:
            self.popmenu.Append(-1,'重命名')
            tmp = self.popmenu.Append(-1, '载入章节图库')
            self.Bind(wx.EVT_MENU,self.show_pic,tmp)
            tmp = self.popmenu.Append(-1,'添加关卡图库')
            self.Bind(wx.EVT_MENU,self.save_guanqia,tmp)
            tmp = self.popmenu.Append(-1,'添加关卡确认图库')
            self.Bind(wx.EVT_MENU,self.save_guanqia_confirm,tmp)
            tmp = self.popmenu.Append(-1,'删除章节')
            self.Bind(wx.EVT_MENU,self.delete_item,tmp)
        elif num_level is 4:
            self.popmenu.Append(-1,'重命名')
            tmp = self.popmenu.Append(-1, '载入关卡图库')
            self.Bind(wx.EVT_MENU,self.show_pic,tmp)
            tmp = self.popmenu.Append(-1,'删除关卡')
            self.Bind(wx.EVT_MENU,self.delete_item,tmp)
        self.PopupMenu(self.popmenu,pos)
        #self.tree.Get
    #双击tree控件时显示对应库中的图库,并自动载入到可以供识图的变量中
    def show_pic(self,event):
        tmp_parent = self._get_tree_struct()
        num_parent = len(tmp_parent)
        if tmp_parent[1] == '活动':
            huodong = True
        else:
            huodong = False
        if num_parent==4:
            tmp = config_ark.ChapterCTE(tmp_parent[1])+ '|' + tmp_parent[2]+"|"+tmp_parent[3]
        elif num_parent==3:
            tmp = config_ark.ChapterCTE(tmp_parent[1])+ '|' + tmp_parent[2]
        elif num_parent==2:
            tmp = config_ark.ChapterCTE(tmp_parent[1])
        if num_parent==4:
            dialog = SubclassDialog()
            result = dialog.ShowModal()
            if result == wx.ID_CANCEL:
                img_path = config_ark.get_img_path(tmp + '_confirm',huodong)
                tmp_res = config_ark.get_img_res(tmp + '_confirm', huodong)
            else:
                img_path = config_ark.get_img_path(tmp,huodong)
                tmp_res = config_ark.get_img_res(tmp, huodong)
        else:
            img_path = config_ark.get_img_path(tmp,huodong)
            tmp_res = config_ark.get_img_res(tmp, huodong)
        if os.path.exists(img_path):
            self.cut_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
            #self.cut_img = cv2.imread(img_path.encode('gbk').decode())
            cv2.destroyAllWindows()
            cv2.imshow('cut_image', self.cut_img)
            self.scoreText4.SetLabel('{},{}'.format(tmp_res[0],tmp_res[1]))
            self.origin_res = tmp_res
        else:
            wx.MessageBox('img_file {} doesn\'t exsit'.format(img_path))




    def save_chapter(self, event):
        if isinstance(self.cut_img,np.ndarray):
            pass
        else:
            wx.MessageBox("请先截图！")
            return
        tmp_str = self.tree.GetItemText(self.tree.GetSelection())
        #parent = self._get_tree_struct()
        dialog = wx.TextEntryDialog(None,
                                    "请输入添加章节的名称",
                                    "图库添加", "", style=wx.OK | wx.CANCEL)
        # 检查名称是否重名
        while(1):
            if dialog.ShowModal() == wx.ID_OK:
                name = dialog.GetValue()

                children = TREE.get_children(self.tree,self.tree.GetSelection())
                parent = self._get_tree_struct()
                if name in children:
                    wx.MessageBox("输出章节名称与当前存在章节名称重复，请重新输入!")
                else:
                    if tmp_str == "活动":
                        file_name = os.path.join(config_ark.huodong_path, name)
                    else:
                        file_name = os.path.join(config_ark.guanqia_path,name)
                    name_all = config_ark.ChapterCTE(parent[1])+ '|' + name
                    tmp_file = file_name
                    cnt = 0
                    while (1):
                        # 检查保存文件是否重名
                        if os.path.isfile(tmp_file + '.png'):
                            tmp_file = file_name + "{}".format(cnt)
                            cnt += 1
                        else:
                            break
                    # 保存图片文件
                    cv2.imencode('.png', self.cut_img)[1].tofile(tmp_file + ".png")
                    if os.path.isfile(tmp_file + ".png"):
                        wx.MessageBox("图像保存成功，位置{}".format(tmp_file+".png"))
                    #cv2.imwrite(tmp_file + '.png',self.cut_img)
                    # 更新配置文件及内存配置信息
                    if tmp_str == "活动":
                        config_path = os.path.join(config_ark.CONFIG_PATH,'pic_huodong')
                        config_ark.huodong_pic[name_all] = tmp_file + ".png"
                        config_ark.huodong_pic_res[name_all] = self.origin_res
                    else:
                        config_path = os.path.join(config_ark.CONFIG_PATH,"guanqia")
                        config_ark.guanqia_pic[name_all] = tmp_file + ".png"
                        config_ark.guanqia_pic_res[name_all] = self.origin_res
                    with open(config_path,'a',encoding='utf-8') as file:
                        file.write("{} {} {} {}\n".format(name_all,tmp_file + ".png",self.origin_res[0],self.origin_res[1]))
                    file.close()
                    # 更新tree
                    new_item = self.tree.AppendItem(self.tree.GetSelection(),name)
                    wx.MessageBox("图库添加成功")
                    break
            else:
                break


    def save_guanqia(self, event):
        if isinstance(self.cut_img,np.ndarray):
            pass
        else:
            wx.MessageBox("请先截图！")
            return
        tmp_str = self.tree.GetItemText(self.tree.GetSelection())
        parent = self._get_tree_struct()
        dialog = wx.TextEntryDialog(None,
                                    "请输入添加关卡的名称",
                                    "图库添加", "", style=wx.OK | wx.CANCEL)
        # 检查名称是否重名
        while(1):
            if dialog.ShowModal() == wx.ID_OK:
                name = dialog.GetValue()
                children = TREE.get_children(self.tree,self.tree.GetSelection())
                if name in children:
                    wx.MessageBox("输出关卡名称与当前存在关卡名称重复，请重新输入!")
                else:
                    save_dict = {}
                    name_all = config_ark.ChapterCTE(parent[1])+ '|' + parent[2]+"|" + name
                    if tmp_str == "活动":
                        file_name = os.path.join(config_ark.huodong_path, name)
                    else:
                        file_name = os.path.join(config_ark.guanqia_path,name)
                    tmp_file = file_name
                    cnt = 0
                    while (1):
                        # 检查保存文件是否重名
                        if os.path.isfile(tmp_file + '.png'):
                            tmp_file = file_name + "{}".format(cnt)
                            cnt += 1
                        else:
                            break

                    save_dict['image'] = self.cut_img
                    save_dict['image_save_path'] = tmp_file + ".png"
                    save_dict['name_all'] = name_all
                    save_dict['origin_res'] = self.origin_res
                    save_dict['tree_item'] = self.tree.GetSelection()
                    save_dict['tree_add_name'] = name
                    save_dict['tmp'] = tmp_str
                    self.guanqia_save[name] = save_dict
                    name_confirm = name + "_confirm"
                    if (name in self.guanqia_save) and (name_confirm in self.guanqia_save):
                        self._save_guanqia(name)
                    else:
                        wx.MessageBox("{}关卡已保存至内存，请继续添加对应关卡的确认图库完整图库添加流程".format(name))
                    break
            else:
                break

    def save_guanqia_confirm(self, event):
        if isinstance(self.cut_img,np.ndarray):
            pass
        else:
            wx.MessageBox("请先截图！")
            return
        tmp_str = self.tree.GetItemText(self.tree.GetSelection())
        parent = self._get_tree_struct()
        dialog = wx.TextEntryDialog(None,
                                    "请输入添加关卡的名称",
                                    "图库添加", "", style=wx.OK | wx.CANCEL)
        # 检查名称是否重名
        while(1):
            if dialog.ShowModal() == wx.ID_OK:
                name_origin = dialog.GetValue()
                children = TREE.get_children(self.tree,self.tree.GetSelection())
                if name_origin in children:
                    wx.MessageBox("输出关卡名称与当前存在关卡名称重复，请重新输入!")
                else:
                    save_dict = {}
                    name = name_origin + "_confirm"
                    name_all = config_ark.ChapterCTE(parent[1])+ '|' + parent[2] + "|" + name
                    if tmp_str == "活动":
                        file_name = os.path.join(config_ark.huodong_path, name)
                    else:
                        file_name = os.path.join(config_ark.guanqia_path,name)
                    tmp_file = file_name
                    cnt = 0
                    while (1):
                        # 检查保存文件是否重名
                        if os.path.isfile(tmp_file + '.png'):
                            tmp_file = file_name + "{}".format(cnt)
                            cnt += 1
                        else:
                            break
                    # 保存相关信息，若图及确认图都存在则添加
                    save_dict['image'] = self.cut_img
                    save_dict['image_save_path'] = tmp_file + ".png"
                    save_dict['name_all'] = name_all
                    save_dict['origin_res'] = self.origin_res
                    save_dict['tree_item'] = self.tree.GetSelection()
                    save_dict['tree_add_name'] = name_origin
                    save_dict['tmp'] = tmp_str
                    self.guanqia_save[name] = save_dict
                    if (name in self.guanqia_save) and (name_origin in self.guanqia_save):
                        self._save_guanqia(name_origin)
                    else:
                        wx.MessageBox("{}关卡确认图库已保存至内存，请继续添加对应关卡的图库完整图库添加流程".format(name_origin))
                    break
                    #wx.MessageBox("图库添加成功")
            else:
                break
        pass

    def delete_item(self,event):
        item_now = self.tree.GetSelection()
        #tmp_str = self.tree.GetItemText(item_now)
        parent = self._get_tree_struct()
        if len(parent)==4:
            #删除关卡
            name = config_ark.ChapterCTE(parent[1])+ '|' + parent[2]+"|"+parent[3]
            name_confirm = config_ark.ChapterCTE(parent[1])+ '|' + parent[2]+"|"+parent[3] + "_confirm"
            if parent[1]=="活动":
                huodong = True
            else:
                huodong = False
            self._delete(name,huodong)
            self._delete(name_confirm,huodong)
            pass
        elif len(parent)==3:
            #删除章节
            name = config_ark.ChapterCTE(parent[1])+ '|' + parent[2]
            if parent[1]=="活动":
                huodong = True
            else:
                huodong = False
            self._delete(name,huodong)
        else:
            #其余情况暂时不可能出现
            print("123")
            pass
        #删除tree控件
        self.tree.Delete(item_now)
        wx.MessageBox("{}删除成功".format(name))


    def _delete(self,name,huodong=False):
        if huodong:
            pic_path = config_ark.huodong_pic[name]
            config_ark.huodong_pic.pop(name)
            config_ark.huodong_pic_res.pop(name)
        else:
            pic_path = config_ark.guanqia_pic[name]
            config_ark.guanqia_pic.pop(name)
            config_ark.guanqia_pic_res.pop(name)
        os.remove(pic_path)
        print("删除成功{}".format(pic_path))
        config_path = os.path.join(config_ark.CONFIG_PATH,'guanqia')
        with open(config_path,'r',encoding='utf-8') as file:
            lines = file.readlines()
            for index,s in enumerate(lines):
                if s:
                    if s.split(" ")[0] == name:
                        lines.pop(index)
                        break
        file.close()
        with open(config_path,'w',encoding='utf-8') as file:
            file.writelines(lines)
        file.close()
        print("配置文件信息删除成功{}".format(config_path))




    #若confirm及原图两个都被添加，则保存到本地
    def _save_guanqia(self,name):
        def _save(self,name):
            file_name = self.guanqia_save[name]['image_save_path']
            name_all = self.guanqia_save[name]['name_all']
            origin_res = self.guanqia_save[name]['origin_res']
            cut_img = self.guanqia_save[name]['image']
            cv2.imencode('.png', cut_img)[1].tofile(file_name)
            if os.path.isfile(file_name):
                wx.MessageBox("图像保存成功，位置{}".format(file_name))
            # cv2.imwrite(tmp_file + '.png',self.cut_img)
            # 更新配置文件及内存配置信息
            if self.guanqia_save[name]['tmp'] == "活动":
                config_path = os.path.join(config_ark.CONFIG_PATH, 'pic_huodong')
                config_ark.huodong_pic[name_all] = file_name
                config_ark.huodong_pic_res[name_all] = origin_res
            else:
                config_path = os.path.join(config_ark.CONFIG_PATH, "guanqia")
                config_ark.guanqia_pic[name_all] = file_name
                config_ark.guanqia_pic_res[name_all] = origin_res
            with open(config_path, 'a', encoding='utf-8') as file:
                file.write("{} {} {} {}\n".format(name_all, file_name, origin_res[0], origin_res[1]))
            file.close()
        _save(self,name)
        _save(self,name+ "_confirm")
        # 更新tree
        new_item = self.tree.AppendItem(self.guanqia_save[name]['tree_item'], name)
        wx.MessageBox("图库添加成功")



    #返回list,包含当前选中的节点及其父节点，父节点在前
    def _get_tree_struct(self):
        tmp_parent = []
        current_selection = self.tree.GetSelection()
        parent_text = self.tree.GetItemText(current_selection)
        tmp_parent.append(self.tree.GetItemText(current_selection))
        while (1):
            if parent_text == 'root':
                break
            current_selection = self.tree.GetItemParent(current_selection)
            parent_text = self.tree.GetItemText(current_selection)
            tmp_parent.insert(0,parent_text)
        return tmp_parent

    def _onPress(self, event):
        ''' Callback to handle the mouse being clicked and held over the canvas'''
        # Check the mouse press was actually on the canvas
        if event.xdata is not None and event.ydata is not None:
            # Upon initial press of the mouse record the origin and record the mouse as pressed
            self.pressed = True
            self.rect.set_linestyle('dashed')
            self.x0 = event.xdata
            self.y0 = event.ydata

    def _onRelease(self, event):
        '''Callback to handle the mouse being released over the canvas'''
        # Check that the mouse was actually pressed on the canvas to begin with and this isn't a rouge mouse
        # release event that started somewhere else
        if self.pressed:

            # Upon release draw the rectangle as a solid rectangle
            self.pressed = False
            self.rect.set_linestyle('solid')

            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata

            # Set the width and height and origin of the bounding rectangle
            self.boundingRectWidth = abs(self.x1 - self.x0)
            self.boundingRectHeight = abs(self.y1 - self.y0)
            self.boundingRectOrigin = (min(self.x0, self.x1), min(self.y0, self.y1))

            # Draw the bounding rectangle
            self.rect.set_width(self.boundingRectWidth)
            self.rect.set_height(self.boundingRectHeight)
            self.rect.set_xy(self.boundingRectOrigin)
            #self.text = plt.text(self.boundingRectOrigin[0],self.boundingRectOrigin[1],"0.9865")
            self.canvas.draw()

            # OpenCV cut picture(all number shoudle be integer)
            x = int(self.boundingRectOrigin[0])
            y = int(self.boundingRectOrigin[1])
            width = int(self.boundingRectWidth)
            height = int(self.boundingRectHeight)
            if isinstance(self.origin_img,np.ndarray) and width:
                self.cut_img = self.origin_img[y:y + height, x:x + width,:]
                self.origin_res = [self.origin_img.shape[1],self.origin_img.shape[0]]
                self.scoreText4.SetLabel("{},{}".format(self.origin_res[0],self.origin_res[1]))
                #cv2.imshow('1231',self.origin_img)
                cv2.destroyAllWindows()
                cv2.imshow('cut_image', self.cut_img)
            else:
                print("Draw Null Rectangle")
                return

    def _onMotion(self, event):
        '''Callback to handle the motion event created by the mouse moving over the canvas'''
        # If the mouse has been pressed draw an updated rectangle when the mouse is moved so
        # the user can see what the current selection is
        if self.pressed:
            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata

            # Set the width and height and draw the rectangle
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()

        # Show Picture
    def show_cut_img(self, event):
        if isinstance(self.cut_img,np.ndarray):
            cv2.destroyAllWindows()
            cv2.imshow('cut_image', self.cut_img)
        else:
            wx.MessageBox('cut_img doesn\'t exsit')
    def setImage(self, image):
        #image BGR need transpose first
        '''Sets the background image of the canvas'''
        # Clear the rectangle in front picture
        self.axes.text(100, 100, '', None)
        self.rect.set_width(0)
        self.rect.set_height(0)
        self.rect.set_xy((0, 0))
        self.canvas.draw()
        # plt.cla()
        # self.initCanvas()

        # Load pic by OpenCV
        # image=cv2.imread(pathToImage,1)

        # Load the image into matplotlib and PIL
        if isinstance(image,np.ndarray):
            image = image[:, :, ::-1]
        else:
            image = matplotlib.image.imread(image)

        # Save the image's dimensions from PIL
        #self.imageSize = imPIL.size

        '''
        self.imageSize = image.shape
        print(pathToImage)
        print("It's width and height:")
        print(self.imageSize)

        print("------------------------")

        # OpenCV add text on pic
        str1='(%s,%s)' % (str(self.imageSize[0]),str(self.imageSize[1]))
        rev=wx.StaticText(self,-1,str1,(670,400))
        #rev.SetForegroundColour('white')
        #rev.SetBackgroundColour('black')
        #rev.SetFont(wx.Font(15,wx.DECORATIVE,wx.ITALIC,wx.NORMAL))
        cv2.putText(image,str1,(10,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
        '''

        #str1 = '%s,%s' % (str(self.imageSize[0]), str(self.imageSize[1]))
        #rev = wx.StaticText(self, -1, str1, (680, 550))

        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(image, aspect='equal')

        self.canvas.draw()

class Myapp(wx.App):
    def __init__(self):
        self.qwe = 123
        wx.App.__init__(self,redirect=False)


    def OnInit(self):
        print(self.qwe)
        self.frame = MyFrame1(parent=None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
if __name__ == "__main__":
    #just for test
    app = Myapp()
    app.MainLoop()
    app.OnExit()