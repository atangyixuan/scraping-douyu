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
import requests
import unittest
import selenium
from selenium import webdriver
import lxml
from lxml import etree
import time
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
tdf = totaldf.sample(10000)
#print(tdf)
pd.DataFrame.to_csv(tdf,"dy.csv")
totaldf=pd.read_csv('dy.csv')
totaldf = (pd.DataFrame(totaldf))[0:2001]
totaldf['关注度']=['36', '5030', '211', '4', '187', '5', '122', '2068', '15', '77', '79332', '107', '1027', '1', '11', '296', '9', '4', '15', '24811', '4', '15', '5', '771', '2814', '31', '318', '11872', '10', '303', '0', '25', '1', '1', '3591', '47', '4', '9673', '20601', '0', '3', '15897', '50', '0', '3897', '25', '25', '0', '82', '397', '15', '4610', '833', '281', '0', '3', '282', '45', '2661', '921', '103', '7', '1111', '5', '35', '1362', '153', '31', '6', '1303', '0', '82', '2258', '218', '33', '273', '25', '462', '1458', '0', '918', '14', '0', '1', '4788', 'nothing', '149', '1201', '9', '19', '282', '6120', '148', '767', '1312', '776', 'nothing', '5519', '441039', '1', '27473', '897', '1640', '1', '5863', '3', '1021', '526', '162', '15', '0', '1884147', '1857', '1', '4', '86', '241', '0', '138', '93', '489', '518', '19010', '3304', '1281', '130', '4', '10450', '4762', '41', '62', '4883', '8', '12846', '0', '19', '431', '74724', '13137', '11', '75', '3065', '34', '1', '114', '23', '126', '42384', '21', '7', '1315', '0', '134', '194', '19', '689', '7', '1737', '1', '283', '37', '470', '0', '0', '50', '7993', '32', '0', '1251', '0', '119', '2290', '8459', '2365', '136', '0', '313', '31', '1308', '378', '13', '2', '342', '3', '45', '84', '215', '45', '2197', '435', '16', '58', '151', '0', '5', '4550', '17', '0', 'nothing', '6606', '31', '9105', '75', '896', '213', '0', '206', '41660', '393834', '0', '153', '20', '17', '193544', '124', '39465', '1634', '42', '226', '41', '11299', '52', '24740', '39337', '2870', '0', '11', '2554', '50', '2032', '38', '2140', '1024', '66', '185', '123', '32', '5', '802', '14', '31', '45950', '256', '72', '375', '12', '11149', '28015', '3026', '44', '54628', '464', '6873', '57', '18', '875655', '3755', '0', '3', '42', '201', '1302', '144', '33', '185', '321', '29', '76', '3722', '645', '4000', '0', '33', '0', '0', '32', '1', '8029', '60', '61', '19', '5238', '225', '168', '158', '236', '16', '865', '17', '0', '171', '1153', '0', '78', '7459', 'nothing', '489', '55', '21724', '71', '19995', '555197', '1032', '285', '2', '3', '0', '443', '0', '232', '88', '1120', '47', '16', '22', '3', '14405', '345', '1', '31', '989', '4469', '5422', '865', '101', '28', '38', '1970', '1', '10258', '11', '1', '200', '3', '0', '43', '2', '5', '3', '29', '847', '11130', '4', '4', '21653', '4579', '154', '70', '2353', '24', '765', '6', '4', '613', '0', '23', '815', '18', '120', '2', '6', '21', '58', '8966', '3', '232', '3503', '1766', '0', '22', '3', '81435', '393', '0', '0', '30499', '25548', '963', '1', '2281', '38', '47788', '13', '3047', '232403', '4', '49', '2623', '17', '711', '87', '31', '43', '192', '102', '865', '4', '3', '22', '89', '1033', '802', '985', '51', '321', '0', '0', '0', '187', '229', '921', '59', '10270', '56', '22776', '1', '16707', '145', '1', '1045', '61', '92946', '2803', '741', '27', '77', '1205', '335', '146', '1243', '3338', '2471', '8734', '87907', '13291', '2981', '3725', '127', '19', '1291', '44492', '216', '129', '306', '2', '0', '6', '0', '102459', '266', '47', '529', '115', '0', '257', '115', '45', '30823', '1440', '25', '10310', '64', '181', '0', '296', '508', '1', '12990', '14', '275', '5', '392', '2', '43', '24', '123', '19', '2182', '543', '27', '79', '45', '47', '33', '89', '16', '3375', '10047', '36', '40', '91', '0', '10005', '506', '9', '3', '0', '5285', '11', '71','44','1153', '0', '326882', '126', '3', '0', '1', '3314', '215', '1241', '23451', '130', '2', '55', '13726', '6', '2', '49', '550', '13600', '1723', '0', '2715', '882', '1376', '2549', '569', '171', '219', '44', '951', '321', '0', '2029', '21', '48', '2082', '130', '12340', '35420', '12293362', '1513', '14445', '12', '892', '24', '1675', '200', '65', '3355', '3162', '1088', '18', '11', '29', '141', '121', '1784', '4789', '6', '23', '304', '55', '0', '365', '553', '1', '12', '18', '53350', '115', '31089', '895', '6192', '18', '358', '85354', '138', '30680', '159', '183', '62', '19773', '1', '1034', '21392', '591', '1731', '920', '8920', '49', '45', '6', '471', '33', '0', '303', '15', '968', '0', '40', '8', '491', '1633', '45', '2829', '86913', '8861', '329', '2965', '2659', '906', '0', '29', '0', '0', '148055', '15', '92', '11', '1263', '8', '0', '581', '440', '0', '414', '58', '287', '5', '76', '255', '0', '150', '94', '18119', '11', '114', '24', '20', '513', '0', '2690', '11', '19442', '3', '3092', '264134', '0', '145', '855', '157', '90450', '26', '381', '219', '4586', '5542', '5062', '1', '59', '1', '83', '400', '339', '7964', '13492', '640', '83', '15213', '393151', '1', '32', '1951', '63', '478', '35', '54', 'nothing', '7816', '455', '59', '16', '103', '968', '3', '0', '74', '3', '1127', '3', '2288', '436', '2', '11', '179', '0', '14691', '1359', '88', '33744', '891', '3004', '33', '1352', '0', '12576', '147', '1', '2079', '18', '60', '143', '52', '6762', '3772', '288', '923', '406', '0', '0', '3409', 'nothing', '2244', '220', '350', '19201', '280', '0', '3', '25', '16', '736', '2476', '8', '13457', '35', '781', '0', '69621', 'nothing', '299', '6685', '121', '114683', '168', '10217', '12', '3747', '0', '12', '5445', '964', '354', '0', '30055', '160', '0', '1634', '243391', '177774', '56', '26581', '281', '59', '2455', '17258', '193', '147', '14', '24155', '135', '2', '26', '85', '313', '1', '10', '36', '1506', '6', '69', '710', '342', '0', '3', '27', '145016', '42', '66', '0', '76', '16321', '2449', '3458', '220', '31', '621', '157', '21', '54', '645', '320', '5159', '47', '75055', '1', '1268', '27', '343', '365', '0', '0', '46', '3433', '762', '12415', '3305', '5020', '2529', '416', '0', '11844', '33', '530', '118', '4125', '11', '2213', '406', '120', '3', '228', '0', '0', '8757', '1688', '176', '2', '0', '2', '2563', '64624', '33', '766', '360', '0', '5247', '164', '5029', '8995', '936', '33', '173', '1024', '8', '187', '1', '55', '27', '269', '303', '210', '35', '6091', '18', '6796', '18', '22', '0', '169', '51', '20076', '190', '111', '11', '0', '17125', '23', '61', '24', '35', '13', '10', '15', '448', '44', '1765', '1108', '11187', '45', '33', '277354', '373', '2', '496', '175', '2', '0', '133', '2', '262', '3', '2', '146', '2977', '356', '754', '652', '326', '43', '6490', '409', '54', '13', '26', '81', '8457', '30493', '316', '0', '5251', '646', '0', '16', '141891', '1251', '231', '1191', '8', '1129', '459', '176', '3202', '18264', '394', '1', '34', '50', '1', '91', '843', '5738', '1060', '412', '407', '2958', '6', '15', '7', '60', '71', '172', '1', '6782', '11', '1878', '3', '215', '8', '6453', '785', '0', '1216', '1832', '5', '507', '11', '139', '88', '0', '28', '3492', '3271', '0', '125', '0', '29', '2016', '0', '0', '1', '0', '224', '6', '16958', '161', '2591', '29', '18', '861', '179', '1262', '190', '10', '0', '151', '13128', '101', '2426', '29', '69', '2', '369', '446', '1', '2384', '55', '14', '103036', '331', '22', '35', '21', '5899', '26', '129', '501', '3', '240', '96', '39460', '51', '55', '7', '245', '13', '8', '3425', '9', '1198', '3', '3309', '82', '1869', '1824', '1', '1028', '89', '1129', '7428', '2046', '121', '9595', '19', '54', '213', '14', '144', '37', '17', '10', '1216', '1', '0', '50', '6429', '0', '0', '0', '76', '1', '138', '171', '4071', '330', '91', '0', '10', '563', '21', '322', '961', '104', '112', '369', '2330', '0', '17', '7', '133994', '175', '60', '823', '63', '126', '4018', '3086', '0', '0', '1510', '16', '71', '169', '5399', '0', '1', '120', '2', '144', '16', '46471', '1375', '78', '115', '0', '9', '3883', '1577', '0', '2', '0', '19', '25', '10', '22', '24', 'nothing', '92', '7340', '5946', '871', '771', '562', '40', '2', '0', '95', '530', '560', '693', '14', '3336', '301', '25', '1031', '34614', '733', '14', '0', '0', '1', '855', '754', '63', '34', '180', '918', '4464', '14', '71', '5002', 'nothing', '575', '37', '21843', '2133', '26', '1', '12544', '948', '345', '230', '20', '854', '1025', '3419', '7', '0', '504', '990660', '23', '99', '552', '2443', '6', '12050', '116', '0', '7', '100', '30', '59', '361', '0', '3747', '187', '32724', '0', '33', '46', '6782', '4', '50', '69', '14', '0', '399', '2883', '5142', '0', '72', '1', '278', '860', '25269', '0', '0', '14', '99', '1980', '1191', '26', '24', '1580', '1', '1697', '11', '2111', '77883', '0', '4558', '0', '570', '416', '306', '62', '781', '4', '5189', '1544', '62', '77', '6', '1882', '5940', '4915', '72', '0', '0', '15', '73', '0', '9371', '22', '1419', '3338', '79', '23', '91', '29', '13', '0', '3', '341', '40', '139', '25531', '290', '53', '44', '44', '255', '35', '303', '4078', '53', '0', '242', '319', '4', '7', '4', '3', '0', '230', '0', '1351', '102', '10610', '82', '634', '2', '1', '16', '139', '13', '15', '62', '1', '953', '3', '119340', '97', '59', '215', '107', '386', '269', '1', '20434', '236', '117', '0', '285', '22775', '133', '1135', '12', '0', '0', '17', '329', '116', '4386', '3681', '7781', '80', '81', '1', '94', '34', '2', '3', '66', '994', '33738', '13', '508', '575', '85', '160', '69', '1960', '0', '0', '2076', '0', '4', '17', '2619', '845', '2007', '51429', '17', '43', '121', '2', '2', '165', '1114', '2603', '32', '0', '68', '443', '102989', '31', '0', '65', '1', '230', '2553', '6', '255', '4557', '73', '0', '121', '4416', '2976', '680', '0', '24122', '1', '0', '8', '135614', '94', '11893', '7938', '0', '31', '94', '1661', '131', '54', '155', '1327', '33', '61', '9', '1233', '249', '32', '37', '553', '276', '6', '18198', '2', '138', '36', '0', '0', '0', '75', '7', '71', '6765', '68', '7834', '47116', '1339', '6583', '101', '0', '32', '25', '3280', '573', '22', '277353', '9827', '120', '563', '49', '0', '1', '146', '6170', '13', '8', '46', '11115', '1092', '242522', '0', '77', '197', '40', '107', '0', '46', '2740', '33471', '1672', '28', '452', '122', '1562', '0', '365', '47', '93', '161', '10', '336', '76', '109', '7134', '171', '2414', '22', '5', '143', '91', '2569', '147', '88', '12220', '44', '0', '2111', '13', '128', '1913', '2', '1300048', '72058', '1', '139', '2621', '6479', '4305', '264', '39842', '2', '3', '3140', '8', '105', '26', '151', '156', '485', '827', '0', '1036','32442','nothing', '81', '2', '0', '0', '7', '13', '1911', 'nothing', '76', '16700', '72', '17', '0', '347', '27', '0', '3936', '102', '1157', '0', '10', '348', '61', '32', '808', '352008', '2174', '107', '130', '12484', '21109', '0', '216', '7022', '188', '0', '48', '326', '655709', '91', '12455', '5', '26', '0', '91', '82', '2', '1262', '32', '12461', '74329', '155', '2244', '216', '250', '855', '2740', '2687', '278', '2662', '427', '482', '55', '133718', '76', '0', '7', '2750', '15', '27', '19200', '1427', '2936', '31', '24', '149', '4', '85', '919', '225', '593', '728541', '4', '71', '171172', '500', '2948', '350', '0', '171175', '10', '0', '2', '257', '12', '23', '98', '540', '26', '158', '16', '771', '1', '100238', '2', '209', '30731', '59', '841', '212', '11', '0', '157', '168', '9', '1144', '2', '28', '17069', '2807', '27', '5', '743', 'nothing', '3973', '3122', '903', '4185', '0', '0', '488', '14414', '499', '449', '9', '358', '5066', '766', '60', '124', '65', '2206', '53', '5', '0', '785', '0', '1956', '796', '32', '277', '103280', '24', '20', '104', '36', '1004', '25', '4112', '1', '0', '3', '344', '6', '0', '22', '15416', '1104', '6417', '90', '98', '0', '110', '19', '216', '2', '1619', '47', '0', '521', '11914', '79', '213', '86', '0', '24888', '112', '15', '6', '5', '217', '6767', '0', '0', '598', '133', '31002', '33', '3', '0', '20', '8', '177', '6', '23', '7', '3904', '5380', '0', '18', '2', '42', '16579', '3', '0', '224', '4', '9652', '44074', '148', '0', '176', '331', '62', '39', '44', '15', '0', '4316', '1', '280', '95', '1781', '578', '24268', '1725', '61', '16', '68', '6', '8', '1414832', '1', '1283', '49', '4430', '8151', '95', '283', '101', '4429', '33', '30', '579', '6', '30', '7', '53', '0', '2', '1209', '19', '6', '0', '605', '3', '10', '313', '125', '15', '45', '238', '1', '1', '0', '145005', '10', '248', '4912', '12', '7', '19', '24', '517', '29', '91', '20486', '1375', '150', '31', '6695', '585469', '6718', '55', '104', '11034', '10045', '4', '1', '13', '182', '76', '1266', '0', '111548', '57', '41650', '100', '1', '69964', '1', '684', '7', '387', '535', '75', '673', '7699', '337', '1513', '33', '0', '0', '2', '121', '441', '340', '2158', '95', '10662', '2306', '3377', '21', '88', '60', '67', '706', '10', '1', '31', '13192', '12', '27', '217801', '3', '91', '71', '7494', '6497', '133', '38026', '1660', '326', '15', '70', '135', '3', '1', '938', '3', '15462', '29946', '819', '1', '18', '41', '22', '3318', '13', '0', '134', '78405', '0', '211', '16691', '59', '6863', '133', '4381', '0', '1026', '6', '0', '0', '38', '11063', '102000', '35', '34', '22', '1252', '1', '0', '10', '1889', '1245', '527', '1209', '121', '17', '644', '46', '16', '1186', '328', '107', '9', '21', '2754', '119', '24', '2161', '2', '318', '1', '16', '22', '31224', '20', '3', '748', '78', '814', '3', '31', '6068', '464', '0', '18', '36', '0', '4', '6', '0', '1', '74', '84', '0', '34', '125009', '69', '402', '469', '2', '4', '443', '322', '1', '5318', '5278', '0', '36', '0', '196', '3', '4308', 'nothing', '227', '991', '443', '33', '0', '266', '2549', '1', '2', '333', '872', '33464', '44', '0', '188', '61', '57', '61', '4608', '7', '10', '1', '36334', '0', '34', '0', '1196', '3', '150', '563', '0', '1803', '1', '3', '84', '10800', '259', '95145', '0', '91', '246','3802']
#print(totaldf)
'''
zb_attention=[]
for m in totaldf['外号']:
    thurl = 'https://www.douyu.com' + m
    # print(thurl)
    ddriver = selenium.webdriver.Chrome()
    ddriver.get(thurl)
    # time.sleep(30)
    try:
        WebDriverWait(ddriver, 30).until_not(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="focus-box-con clearfix"]/p/span[@data-anchor-info="nic"]/img')))
        attention = ddriver.find_element_by_xpath(
            '//div[@class="focus-box-con clearfix"]/p/span[@data-anchor-info="nic"]').text  
    except:
        attention = "nothing"
    finally:
        zb_attention.append(attention)
        ddriver.quit()
print(zb_attention)
#print(type(totaldf))
pat_data = pd.DataFrame.sample(totaldf,n=2000,replace=False, axis=0).reset_index()   #任意取出部分数据
print(pat_data['外号'].values)
#数据预处理'''

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


