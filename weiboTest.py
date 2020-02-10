import time
import xlrd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import excelSave as save

# 用来控制页面滚动
def Transfer_Clicks(browser):
    try:
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Transfer successfully \n"

#判断页面是否加载出来
def isPresent():
    temp =1
    try: 
        driver.find_elements_by_css_selector('div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
    except:
        temp =0
    return temp

#把超话页面滚动到底
def SuperwordRollToTheEnd():
    before = 0 
    after = 0
    n = 0
    timeToSleep = 50
    while True:
        before = after
        Transfer_Clicks(driver)
        time.sleep(3)
        elems = driver.find_elements_by_css_selector('div.m-box')
        print("当前包含超话最大数量:%d,n当前的值为:%d,当n为5无法解析出新的超话" % (len(elems),n))
        after = len(elems)
        if after > before:
            n = 0
        if after == before:        
            n = n + 1
        if n == 5:
            print("当前包含最大超话数为：%d" % after)
            break
        if after > timeToSleep:
            print("抓取到%d多条超话，休眠30秒" % timeToSleep)
            timeToSleep = timeToSleep + 50
            time.sleep(30)
#插入数据
def insert_data(elems,path,name):
    for elem in elems:
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数       
        rid = rows_old
        #用户名
        weibo_username = elem.find_elements_by_css_selector('h3.m-text-cut')[0].text
        weibo_userlevel = "普通用户"
        #微博等级
        try: 
            weibo_userlevel_color_class = elem.find_elements_by_css_selector("i.m-icon")[0].get_attribute("class").replace("m-icon ","")
            if weibo_userlevel_color_class == "m-icon-yellowv":
                weibo_userlevel = "黄v"
            if weibo_userlevel_color_class == "m-icon-bluev":
                weibo_userlevel = "蓝v"
            if weibo_userlevel_color_class == "m-icon-goldv-static":
                weibo_userlevel = "金v"
            if weibo_userlevel_color_class == "m-icon-club":
                weibo_userlevel = "微博达人"     
        except:
            weibo_userlevel = "普通用户"
        #微博内容
        weibo_content = elem.find_elements_by_css_selector('div.weibo-text')[0].text
        shares = elem.find_elements_by_css_selector('i.m-font.m-font-forward + h4')[0].text
        comments = elem.find_elements_by_css_selector('i.m-font.m-font-comment + h4')[0].text
        likes = elem.find_elements_by_css_selector('i.m-icon.m-icon-like + h4')[0].text
        #发布时间
        weibo_time = elem.find_elements_by_css_selector('span.time')[0].text
        print("用户名："+ weibo_username + "|"
              "微博等级："+ weibo_userlevel + "|"
              "微博内容："+ weibo_content + "|"
              "转发："+ shares + "|"
              "评论数："+ comments + "|"
              "点赞数："+ likes + "|"
              "发布时间："+ weibo_time + "|"
              "话题名称" + name + "|" )
        value1 = [[rid, weibo_username, weibo_userlevel,weibo_content, shares,comments,likes,weibo_time,keyword,name],]
        print("当前插入第%d条数据" % rid)
        save.write_excel_xls_append_norepeat(book_name_xls, value1)
#获取当前页面的数据
def get_current_weibo_data(book_name_xls,name,maxWeibo):
    #开始爬取数据
        before = 0 
        after = 0
        n = 0 
        timeToSleep = 300
        while True:
            before = after
            Transfer_Clicks(driver)
            time.sleep(3)
            elems = driver.find_elements_by_css_selector('div.card.m-panel.card9')
            print("当前包含微博最大数量：%d,n当前的值为：%d, n值到5说明已无法解析出新的微博" % (len(elems),n))
            after = len(elems)
            if after > before:
                n = 0
            if after == before:        
                n = n + 1
            if n == 5:
                print("当前关键词最大微博数为：%d" % after)
                insert_data(elems,book_name_xls,name)
                break
            if len(elems)>maxWeibo:
                print("当前微博数以达到%d条"%maxWeibo)
                insert_data(elems,book_name_xls,name)
                break
            if after > timeToSleep:
                print("抓取到%d多条，插入当前新抓取数据并休眠30秒" % timeToSleep)
                timeToSleep = timeToSleep + 300
                insert_data(elems,book_name_xls,name) 
                time.sleep(30) 

#点击超话按钮，获取超话页面
#一开始就是超话，不用这一坨
# def get_superWords():
#     time.sleep(5)
#     elem = driver.find_element_by_xpath("//*[@class='scroll-box nav_item']/ul/li/span[text()='话题']")
#     elem.click()
#     #获取所有超话
#     SuperwordRollToTheEnd()
#     elemsOfSuper = driver.find_elements_by_css_selector('div.card.m-panel.card26')   
#     return elemsOfSuper

#获取超话链接、名称、讨论量、阅读量
# def get_superwordsUrl():
#     elemsOfSuper = driver.find_elements_by_css_selector('div.card.m-panel.card4')
#     superWords_url = []
#     for i in range(0,len(elemsOfSuper)):
#         superwordsInfo = []
#         print("当前获取第%d个超话链接，共有%d个超话"% (i+1,len(elemsOfSuper)))
#         time.sleep(1)      
#         element = driver.find_elements_by_css_selector('div.card.m-panel.card26')[i]
#         name = driver.find_elements_by_css_selector('div.card.m-panel.card26 h3')[i].text
#         yuedu_taolun = driver.find_elements_by_css_selector('div.card.m-panel.card26 h4:nth-last-child(1)')[i].text
#         yuedu = yuedu_taolun.split(" ")[0]
#         taolun = yuedu_taolun.split(" ")[1]
#         #获取话题名称，话题讨论数，阅读数   
#         print(name)
#         print(taolun)
#         print(yuedu)
#         #获取超话链接
#         driver.execute_script('arguments[0].click()',element)
#         time.sleep(3)
#         print(driver.current_url)
#         #把链接和超话信息一起存放于列表中
#         superwordsInfo = [driver.current_url,name,taolun,yuedu]
#         superWords_url.append(superwordsInfo)
#         driver.back()
#     return superWords_url

#爬虫运行 
def spider(username,password,driver,book_name_xls,sheet_name_xls,keyword,maxWeibo):
    
    #创建文件
    if os.path.exists(book_name_xls):
        print("文件已存在")
    else:
        print("文件不存在，重新创建")
        value_title = [["rid", "用户名称", "微博等级", "微博内容", "微博转发量","微博评论量","微博点赞","发布时间","搜索关键词","话题名称"],]
        save.write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    
    #加载驱动，使用浏览器打开指定网址  
    driver.set_window_size(452, 790)
    driver.get("https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F")  
    time.sleep(3)
    #登陆
    elem = driver.find_element_by_xpath("//*[@id='loginName']");
    elem.send_keys(username)
    elem = driver.find_element_by_xpath("//*[@id='loginPassword']");
    elem.send_keys(password)
    elem = driver.find_element_by_xpath("//*[@id='loginAction']");
    elem.send_keys(Keys.ENTER) 
    time.sleep(5)
    #判断页面是否加载出
    while 1:  # 循环条件为1必定成立
        result = isPresent()
        print ('判断页面1成功 0失败  结果是=%d' % result )
        if result == 1:
            elems = driver.find_elements_by_css_selector('div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
            #return elems #如果封装函数，返回页面
            break
        else:
            print ('页面还没加载出来呢')
            time.sleep(20)
    time.sleep(10)
    driver.get("https://m.weibo.cn/p/index?containerid=1008084882401a015244a2ab18ee43f7772d6f&extparam=%E8%82%BA%E7%82%8E%E6%82%A3%E8%80%85%E6%B1%82%E5%8A%A9&luicode=10000011&lfid=100103type%3D1%26q%3D%E8%82%BA%E7%82%8E%E6%82%A3%E8%80%85%E6%B1%82%E5%8A%A9") 
    # #搜索关键词
    # elem = driver.find_element_by_xpath("//*[@class='m-text-cut']").click();
    # time.sleep(5)
    # elem = driver.find_element_by_xpath("//*[@type='search']");
    # elem.send_keys(keyword)
    # elem.send_keys(Keys.ENTER)

    # #get related keyword
    # print(driver.find_element_by_xpath("//*[@text='肺炎患者求助超话']"))
    # elem = driver.find_element_by_xpath("//*[@text='肺炎患者求助超话']").click()
    name = keyword

    get_current_weibo_data(book_name_xls,name, maxWeibo) #爬取综合
    time.sleep(3)
   
    
if __name__ == '__main__':
    username = "juzhidangsi66655@163.com" #你的微博登录名
    password = "bg841754" #你的密码
    driver = webdriver.Chrome('./chromedriver')#你的chromedriver的地址
    book_name_xls = "./weibo.xls" #填写你想存放excel的路径，没有文件会自动创建
    sheet_name_xls = '微博数据' #sheet表名
    maxWeibo = 3000 #设置最多多少条微博，如果未达到最大微博数量可以爬取当前已解析的微博数量
    keywords = ["肺炎患者求助",] #输入你想要的关键字，可以是多个关键词的列表的形式
    for keyword in keywords:
        spider(username,password,driver,book_name_xls,sheet_name_xls,keyword,maxWeibo)

# juzhidangsi66655@163.com----bg841754----
