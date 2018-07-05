import requests
# import urllib2
# import urllib
import unittest
import selenium
from selenium import webdriver
import lxml
from lxml import etree
import lxml
from lxml import etree
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

def getweb(url):
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': '__guid=234720664.1957677918312848600.1528701092141.5796; dy_did=d313849bb78d32f27ade11fe00071501; smidV2=201806132247102d0c649a35c7a616cd77c9656bb74d7300a67006ddce49190; monitor_count=16; acf_did=d313849bb78d32f27ade11fe00071501; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1528701094,1528881111,1529224877; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1529224877'
    }

    response = requests.get(url, headers=headers)
    html = response.text
    return html
def finalist(sehtml):
    totalist = []  # 外列表
    sehtml = etree.HTML(sehtml)
    zb_name = sehtml.xpath('//div[@class="mes"]/p/span[@class="dy-name ellipsis fl"]/text()')  # 主播账号名
    title = sehtml.xpath('//li/a[@class="play-list-link"]/@title')  # 标题
    zb_id  = sehtml.xpath('//li/a[@class="play-list-link"]/@href')
    #print(zb_id)
    fans_online = sehtml.xpath('//div[@class="mes"]/p/span[@class="dy-num fr"]/text()')  # 在线粉丝数
    gamezone = sehtml.xpath('//div[@class="mes-tit"]/span[@class="tag ellipsis"]/text()')  # 游戏区
    # zb_tag = sehtml.xpath('//div[@class="impress-tag-list"]/span/text()')
    zb_attention =[]
    for m in zb_id:
        thurl = 'https://www.douyu.com'+ m
        #print(thurl)
        ddriver = selenium.webdriver.Chrome()
        ddriver.get(thurl)
        #time.sleep(30)
        try:
            WebDriverWait(ddriver, 30).until_not(EC.presence_of_element_located((By.XPATH, '//div[@class="focus-box-con clearfix"]/p/span[@data-anchor-info="nic"]/img')))
            attention = ddriver.find_element_by_xpath('//div[@class="focus-box-con clearfix"]/p/span[@data-anchor-info="nic"]').text  # 关注度
        except :
            attention = "nothing"
        finally:
            zb_attention.append(attention)
            ddriver.quit()
            #print(zb_attention)
    for i in range(len(zb_name)):
        mmlist = []  # 内列表
        mmlist.append(zb_name[i])
        mmlist.append(title[i])
        mmlist.append(zb_id[i])
        mmlist.append(fans_online[i])
        mmlist.append(zb_attention[i])  #关注度
        mmlist.append(gamezone[i])
        totalist.append(mmlist)  # 列表套列表
    return totalist

'''def geturl(url):
    res = requests.get("https://www.douyu.com" + url)  #向指定某分类页发送请求
    # 通过接收到的数据，是通过js动态实现多页数据显示的
    # 后来通过查看js文件发现他调用了API的接口
    # /gapi/rkc/directory/"(分类编号)/(分类页数)
    # 所以后面只需要分析接口的数据就行
    res.encoding='utf-8'
    ze = 'PAGE.rk= "(.*?)";'  #指定某个分类的接口编号
    ze2 = 'count: "(.*?)",'   #指定某个分类的页数
    s = re.findall(ze,res.text)   #当前url的分类
    s2 =re.findall(ze2,res.text)  # 总页数
    return s,s2  '''
def geturlist(html):
    html = etree.HTML(html)
    totainfo = []
    for i in range(1, 50):
        href = html.xpath('//div/ul[@id="live-list-contentbox"]/li[%d]/a[@target="_blank"]/@href' % i)
        secondurl = "https://www.douyu.com" + href[0]
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        driver = selenium.webdriver.Chrome()
        driver.get(secondurl)
        time.sleep(30)
        while True:
            sehtml = driver.page_source
            if driver.page_source.find("overflow: hidden; white-space: nowrap;") != -1:
                break
            totalist = finalist(sehtml)
            totainfo = totainfo + totalist
            if driver.page_source.find("shark-pager-disable-next") != -1 or driver.page_source.find(
                    "tcd-page-code") == -1:
                break
            driver.find_element_by_class_name("shark-pager-next").click()
            time.sleep(10)
        driver.quit()
    return totainfo
import xlwt
def writepage(urlist,m):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('douyu', cell_overwrite_ok=True)
    headname = ['主播账号', '标题', '外号','热度','关注度','游戏区']
    for n in range(len(headname)):
        worksheet.write(0, n , headname[n])
    # workbook.save('data2.xls')
    index = 1
    #print('-----------------')
    for element in urlist:
        for ind in range(6):
            worksheet.write(index, ind , element[ind])
        index += 1
        filename = 'douyu'+str(m)+ '.xls'
        workbook.save(filename)
def main():
	url = 'https://www.douyu.com/directory'
	miao = 0
	m = 25
	while miao <=9:
		html = getweb(url)
		urlist = geturlist(html)
		writepage(urlist,m)
		miao+=1
		m+=1
		time.sleep(600)
main()


#对 爬取到的数据进行初步分析
#-*-coding:utf-8-*-
import ch
ch.set_ch()
total_redu = []
total_zhubo = []
for number in range(7, 20):
    file = pd.read_excel('douyu' + str(number) + '.xls')
    df = pd.DataFrame(file)
    #print(df)
    # 按热度由上向下排序
    df = df.sort_values(['热度'], ascending=False)
    # 总直播人数
    zhubo_count = df['主播账号'].count()
    # 游戏分区直播人数
    game_zhubo_count = df.groupby('游戏区')['主播账号'].count()
    # 总热度，近似代表在线用户数(万，单位)
    redu_count = df['热度'].sum()
    # 游戏分区热度总值
    game_redu_count = df.groupby('游戏区')['热度'].sum()
    total_redu.append(redu_count)
    total_zhubo.append(zhubo_count)

# 比较不同时间，zhubo_count，redu_count的变化
import matplotlib.pyplot as plt
total_redu = np.array(total_redu)
total_zhubo = np.array(total_zhubo)
timeline = ['9:00', '11:00', '13:00', '15:00', '17:00', '19:00', '21:00', '23:00', '1:00','2:00','3:00','4:00','5:00']
timeline = np.array(timeline)

fig = plt.title('直播人数 & 热度 时间变化  ')  #表格命名
plt.plot(timeline, total_redu, color="blue", linewidth=2.5, linestyle="-",label='redu')
plt.plot(timeline, total_zhubo, color="green", linewidth=2.5, linestyle="-",label = 'zhubo')
plt.legend(loc='upper left')
plt.savefig("exercice_1.png",dpi=72)
#plt.show()

file1 = pd.read_excel('douyu14.xls')
df1 = pd.DataFrame(file1)
#以14文件为样本分析游戏占比
game_zhubo_count1 = df1.groupby('游戏区')['主播账号'].count()
game_zhubo_count1 = game_zhubo_count1.sort_values(ascending=False).head(50)
#print(game_zhubo_count1.index)
#game_redu_count1 = df1.groupby('游戏区')['热度'].sum()
plt.pie(game_zhubo_count1,labels=game_zhubo_count1.index,autopct='%1.2f%%',shadow=True)
plt.title('直播人数TOP10 中各游戏区占比')
plt.savefig("exercice_2.png",dpi=72)
#plt.legend(loc='best')
#plt.pie(game_redu_count1)
#plt.show()

#热度TOP100主播游戏分区占比
zhubo_rank=df1.sort_values(['热度'],ascending=False).head(100)
zhubo_rank_zone = zhubo_rank.groupby('游戏区')['热度'].count()
plt.pie(zhubo_rank_zone,labels=zhubo_rank_zone.index,textprops = {'fontsize':6, 'color':'k'},shadow=True)
plt.title('热度TOP100主播游戏分区占比')
plt.legend(loc='center left', bbox_to_anchor=(0.1, 1.12),ncol=3)
plt.savefig("exercice_3.png",dpi=72)
plt.show()

#建模，评估
from sklearn import linear_model  # 线性回归
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
import xlwt
#将多个excel表合为一张
excel_list = []
for number in range(7, 15):
    file = pd.read_excel('douyu' + str(number) + '.xls')
    df = pd.DataFrame(file)
    excel_list.append(df)
totaldf=pd.concat(excel_list)
#print(tdf)
pd.DataFrame.to_csv(totaldf,"dy.csv")
totaldf=pd.read_csv('dy.csv')
totaldf = (pd.DataFrame(totaldf))
#print(type(totaldf))
pat_data = pd.DataFrame.sample(totaldf,n=2000,replace=False, axis=0).reset_index()   #任意取出部分数据
print(pat_data['外号'].values)
#数据预处理

#将时间分为0，1，2三等级
for i in range(1,13):
    if i<=7 or i>10:
        totaldf.loc[totaldf["时间"]==i ,"时间"]=0
    else:
        totaldf.loc[totaldf["时间"] == i, "时间"] = 1

gamelist = totaldf['游戏区'].tolist()
a =['绝地求生', '英雄联盟', '王者荣耀', '主机游戏', '刺激战场']
b = list(set(gamelist)-set(a))
#将游戏区分为0，1，2三个等级
totaldf.loc[totaldf["游戏区"].isin(a[0:5]),"游戏区"]=0

totaldf.loc[totaldf["游戏区"].isin(a[2:5]),"游戏区"]=1
totaldf.loc[totaldf["游戏区"].isin(b),"游戏区"]=2
#print(totaldf)
#pat_data.loc[pat_data["游戏区"].isin(a),"游戏区"]=3
#删除部分列
drop_column = ['主播账号','标题','外号']
totaldf = totaldf.drop(drop_column,axis = 1)
#
#标准化数据
indexlist= totaldf[totaldf['关注度']=="nothing"].index
totaldf = totaldf.drop(indexlist,axis=0)
print(totaldf)
#关注度数据转换
#totaldf['关注度']= totaldf["关注度"].astype(int)
#totaldf.loc[totaldf["关注度"]>2000,"关注度"]=1
#totaldf.loc[totaldf["关注度"]<2000,"关注度"]=0

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
colist = ['时间','游戏区','关注度']
y = totaldf['热度']     #划分y
X = totaldf[colist]    #划分X

X =X.as_matrix().astype(np.float)
X =scaler.fit_transform(X)
from sklearn.model_selection import train_test_split
penalty = {0:3,1:10}
#print(type(X))
X =pd.DataFrame(X)
train_x,test_x,train_y,test_y= train_test_split(X,y,test_size=0.2,random_state=0)  #切分数据集
#print(train_x['关注度'])

#from cm_plot import *
def cm_plot(y, yp):
  from sklearn.metrics import confusion_matrix #导入混淆矩阵函数
  cm = confusion_matrix(y, yp) #混淆矩阵
  import matplotlib.pyplot as plt #导入作图库
  plt.matshow(cm, cmap=plt.cm.Greens) #画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
  plt.colorbar() #颜色标签
  for x in range(len(cm)): #数据标签
    for y in range(len(cm)):
      plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
  plt.ylabel('True label') #坐标轴标签
  plt.xlabel('Predicted label') #坐标轴标签
  return plt.show()

def run_ev(X, y, clf_class, **kwargs):  # 数据，标签，分类器，分类器的参数
    cv = StratifiedKFold(n_splits=20, random_state=0)
    y_pred = y.copy()
    for train, test in cv.split(X, y):
        #print('Train: %s | test: %s' % (train, test))
        X_train = X.iloc[train]
        y_train = y.iloc[train]
        X_test = X.iloc[test]
        #y_train = y.iloc[train]
        clf = clf_class(**kwargs)
        clf.fit(X_train, y_train.values.ravel())
        #print(y_pred.iloc[test])
        y_predd= clf.predict(X_test)
        #预测出的数据属于ndarray类型
        y_predd = pd.DataFrame(y_predd)  #转为dataframe格式
        print('-----------')
        #print(y_predd)
       # predictions.append(y_predd)
        print(np.mean(y.iloc[test].values==y_predd.values))  # 返回预测值

#def accuracy(y_true,y_pred):
    #return
penalty = {0:10,1:3}
from sklearn.svm import SVC  #支持向量机
from sklearn.ensemble import RandomForestClassifier as RF  #随机森林
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.tree import DecisionTreeClassifier as Tree

run_ev(train_x.astype(int),train_y.astype(int),SVC,class_weight = penalty) #y为真实判断值，run_ev为预测值
run_ev(train_x.astype(int),train_y.astype(int),RF,n_estimators=20,min_samples_split=3, min_samples_leaf=1,class_weight = penalty)
#run_ev(train_x.astype(int),train_y.astype(int),KNN)
#run_ev(train_x.astype(int),train_y.astype(int),Tree,class_weight = penalty)

#混淆矩阵图绘制
#随机森林
RF = RF(n_estimators=20,min_samples_split=2, min_samples_leaf=1,class_weight = penalty)
RF.fit(train_x,train_y.astype('int'))
print(accuracy_score(test_y.astype(int),RF.predict(test_x).astype(int)))
print(recall_score(test_y.astype(int),RF.predict(test_x).astype(int)))
#KNN近邻
KNN = KNN()
KNN.fit(train_x,train_y.astype('int'))
print(accuracy_score(test_y.astype(int),KNN.predict(test_x).astype(int)))
print(recall_score(test_y.astype(int),KNN.predict(test_x).astype(int)))
#kf = KFold(),n_folds = 3,random_state=0)
from sklearn import cross_validation
#scores = cross_validation.cross_val_score(tree,train_x.astype(int),train_y.astype(int),cv=3)
#print(scores.mean())


