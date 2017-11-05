#encoding:utf-8
#author:xiaoyuan liu

from selenium import webdriver
import  unittest,time,ddt
from lib.utils import captureScreen  #从外部目录引入captureScreen方法

#L=[['admin','123456',True],['admin','1',False]]
# #这是把值写死，一般不让新人去动代码，而是去修改文件，所以定义了一个数据文件，在文件写值
def get_data():
    L=[]
    data_file='data/test_data.txt'

    fp=open(data_file,'r')
    for line in fp.readlines():
        tmp=line.strip().split(',')    #strip是？split是？
        L.append(tmp)
    fp.close()
    return L

@ddt.ddt   #声明这个类要使用ddt进行数据驱动
class RanzhiLogin(unittest.TestCase):
    def setUp(self):
        self.driver=webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url="http://localhost/ranzhi/www"

    def tearDown(self):
        self.driver.quit()

    @ddt.unpack
    @ddt.data(*get_data()) #缺一不可，*是按照位置解包的意思
    def test_login_test(self,username,password,type):
        driver=self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("account").clear()
        driver.find_element_by_id("account").send_keys(username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("submit").click()  #是click而不是clear要细心
        time.sleep(3)
        captureScreen(driver)
        if str(type)=='True':
            #登录成功，就验证退出关键字是否存在
            self.assertEqual(u'然之协同',driver.title,u'断言标题必须是然之协同')
            self.assertIn(u'退出',driver.page_source,u'断言页面中包含退出')
            ad_text=driver.find_element_by_xpath("//div[@id='home']/nav/div/ul/li/a").text
            #以上不能少，前面通过xpath找到路径，在通过句尾的.text传值
            self.assertIn('admin',ad_text)
        else:
            #登录失败，会弹出提示框
            self.assertIn(u'登录失败',driver.page_source)
        #pycharm的好处是不需要自己写main函数，直接在文件右键-run所有测试用例
        #写了main函数，在main右键-run main
