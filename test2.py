import numpy as np
import cv2
import os
import math
import matplotlib.pyplot as plt
def circles_image(image):
    # 由于霍夫圆检测对噪声敏感，这里用 均值偏移滤波 移除噪声
    # pyrMeanShiftFiltering(src, sp, sr[, dst[, maxLevel[, termcrit]]]) -> dst
    # 1 data 2 空间窗半径 3 色彩窗半径
    dst = cv2.pyrMeanShiftFiltering(image, 10, 100)
    cv2.imshow("23",dst)
    cimage = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(cimage, cv2.HOUGH_GRADIENT, 1, 100, param1=80, param2=70, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles)) # 把类型换成整数
    pic_area = [] #矩形区域坐标信息，i[0]为左上 i[1]右下
    for i in circles[0, :]: # return (a,b,r)
        pic_area.append((i[0],i[1],i[2]))
        cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 255), 2)
        cv2.circle(image, (i[0], i[1]), 2, (255, 0, 255), 2) # 画出小圆心
    cv2.imshow("圆形", image)

def getMatchNum(matches,ratio):
    '''返回特征点匹配数量和匹配掩码'''
    matchesMask=[[0,0] for i in range(len(matches))]
    matchNum=0
    for i,(m,n) in enumerate(matches):
        if m.distance<ratio*n.distance: #将距离比率小于ratio的匹配点删选出来
            matchesMask[i]=[1,0]
            matchNum+=1
    return (matchNum,matchesMask)

def get_match_result():

    #path='D:/CodeProjects/AnacondaSamples/HandleImages/'
    queryPath = './ark_images/processed/src' #图库路径
    samplePath = './test1.png' #样本图片
    comparisonImageList=[] #记录比较结果

    #创建SIFT特征提取器
    sift = cv2.xfeatures2d.SIFT_create()
    FLANN_INDEX_KDTREE=0
    indexParams=dict(algorithm=FLANN_INDEX_KDTREE,trees=5)
    searchParams=dict(checks=50)
    flann=cv2.FlannBasedMatcher(indexParams,searchParams)

    sampleImage=cv2.imread(samplePath,0)
    kp1, des1 = sift.detectAndCompute(sampleImage, None) #提取样本图片的特征
    for parent,dirnames,filenames in os.walk(queryPath):
        for p in filenames:
            p=os.path.join(queryPath,p)
            queryImage=cv2.imread(p,0)
            kp2, des2 = sift.detectAndCompute(queryImage, None) #提取比对图片的特征
            matches=flann.knnMatch(des1,des2,k=2) #匹配特征点，为了删选匹配点，指定k为2，这样对样本图的每个特征点，返回两个匹配
            (matchNum,matchesMask)=getMatchNum(matches,0.9) #通过比率条件，计算出匹配程度
            matchRatio=matchNum*100/len(matches)
            drawParams=dict(matchColor=(0,255,0),
                    singlePointColor=(255,0,0),
                    matchesMask=matchesMask,
                    flags=0)
            comparisonImage=cv2.drawMatchesKnn(sampleImage,kp1,queryImage,kp2,matches,None,**drawParams)
            comparisonImageList.append((comparisonImage,matchRatio)) #记录下结果

    comparisonImageList.sort(key=lambda x:x[1],reverse=True) #按照匹配度排序
    count=len(comparisonImageList)
    column=4
    row=math.ceil(count/column)
    print(comparisonImageList[0])
    #绘图显示
    figure,ax=plt.subplots(row,column)
    for index,(image,ratio) in enumerate(comparisonImageList):
        ax[index%column].set_title('Similiarity %.2f%%' % ratio)
        ax[index%column].imshow(image)
    plt.show()

if __name__ == '__main__':
    img_file = './test1.png'
    image = cv2.imread(img_file)
    circles_image(image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    get_match_result()
    print(123)
