# encoding=utf-8

from  selenium import webdriver
import unittest,time
import logging,traceback
import ddt
from ReportTemplate import htmlTemplate
from selenium.common.exceptions import NoSuchElementException

#初始化日志对象
logging.basicConfig(
    #日记级别
    level=logging.INFO,
    # 日志格式
    # 时间、代码所在文件名、代码行号、日志级别名称、日志信息
    format= '%(asctime)s%(filename)s[line:%(lineno)d]%(levelname)s%(message)s',
    # 打印日志时间
    datefmt='%a,%Y-%m-%d-%H:%M:%S',
    # 日志文件存放的目录（目录必须存在）及日志文件名
    filename='E:/report.log',
    # 打开日志文件的方式
    filemode= 'w'
)

@ddt.ddt
class TestDemo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 整个测试过程只被调用一次
        TestDemo.trStr= ""

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path= "E:\\geckodriver")
        status = None # 用于存放测试结果状态，失败‘fail’，成功‘pass’
        flag= 0 # 数据驱动测试结果的标记，失败置0，成功置1

    @ddt.file_data("test_data_list.json")
    def test_dataDrivenByFile(self,value):
        flagDict = {0:'red',1:'#00AC4E'}
        url = "https://www.baidu.com"
        self.driver.get(url)
        self.driver.maximize_window()
        print value
        testdata,expectdata = tuple(value.strip().split("||"))
        self.driver.implicitly_wait(10)

        try:
            # 获取当前的时间戳，用于后面计算查询耗时用
            start = time.time()
            # 获取当前时间的字符串，表示测试开始时间
            startTime= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            self.driver.find_element_by_id("kw").send_keys(testdata)
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            # 断言期望结果是否出现在页面源代码中
            self.assertTrue(expectdata in self.driver.page_source)
        except NoSuchElementException,e:
            logging.error(u"查找页面元素不存在，异常堆栈信息："+str(traceback.format_exc()))
            status = 'fail'
            flag= 0
        except AssertionError,e:
            logging.info(u"搜索%s期望%s失败"%(testdata,expectdata))
            status = 'fail'
            flag = 0
        except Exception,e:
            logging.error(u"未知错误，错误信息"+str(traceback.format_exc()))
            status = 'fail'
            flag = 0
        else:
            logging.info(u"搜索%s期望%s通过"%(testdata,expectdata))
            status = 'pass'
            flag = 1
        # 计算耗时，从将测试数据输入到输入框到断言期望结果之间所耗时
        wasteTime = time.time()-start-3 # 减去强制等待的3s
        TestDemo.trStr +=u'''
        <tr>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
           <td>%.2f</td>
           <td style = "color:%s">%s</td>
        </tr><br/>'''%(testdata,expectdata,startTime,wasteTime,flagDict[flag],status)

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        # 写自定义的HTML测试报告
        # 整个测试过程只被调用一次
        htmlTemplate(TestDemo.trStr)

if __name__ =='__main__':
    unittest.main()

