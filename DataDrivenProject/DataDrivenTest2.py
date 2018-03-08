# encoding=utf-8

from  selenium import webdriver
import unittest,time
import logging,traceback
import ddt
import HTMLTestRunner
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

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path= "E:\\geckodriver")

    @ddt.file_data("test_data_list.json")
    def test_dataDrivenByFile(self,value):
        url = "https://www.baidu.com"
        self.driver.get(url)
        self.driver.maximize_window()
        print value
        testdata,expectdata = tuple(value.strip().split("||"))
        self.driver.implicitly_wait(10)

        try:
            self.driver.find_element_by_id("kw").send_keys(testdata)
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            # 断言期望结果是否出现在页面源代码中
            self.assertTrue(expectdata in self.driver.page_source)
        except NoSuchElementException,e:
            logging.error(u"查找页面元素不存在，异常堆栈信息："+str(traceback.format_exc()))
        except AssertionError,e:
            logging.info(u"搜索%s期望%s失败"%(testdata,expectdata))
        except Exception,e:
            logging.error(u"未知错误，错误信息"+str(traceback.format_exc()))
        else:
            logging.info(u"搜索%s期望%s通过"%(testdata,expectdata))

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
# if __name__ == 'DataDrivenProject':
    # unittest.main()
    suit1 = unittest.TestLoader().loadTestsFromTestCase(TestDemo)
    suite = unittest.TestSuite(suit1)
    filename ='E:\\testresult.html'
    #  'E:\\report.html'
    fp = file(filename, 'wb')
    # fp.close()
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Report_title',description='Report_description')
    runner.run(suite)
    fp.close()
