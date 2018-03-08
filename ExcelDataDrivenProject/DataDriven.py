# encoding = utf-8
# -*- coding: cp936 -*-
#coding = utf-8

from  selenium import webdriver
import unittest,time
import logging,traceback
import  ddt
from ExcelUtil import ParseExcel
from selenium.common.exceptions import NoSuchElementException

# ��ʼ����־
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d]%(levelname)s%(message)s',
    datefmt='%a,%Y-%m-%d%H:%M:%S',
    filename='E:/dataDrivereport.log',
    filemode='w'
)

excelPath = u'E:\\ExcelDataDrivenProject\\��������.xlsx'
sheetName = u'�������ݱ�'
excel = ParseExcel(excelPath,sheetName)

@ddt.ddt
class TestDemo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="E:\\geckodriver")

    @ddt.data(*excel.getDatasFromsheet())
    def test_dataDrivenByFile(self,data):
        testData,expectData = tuple(data)
        url= "https://www.baidu.com"
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        try:
            self.driver.find_element_by_id("kw").send_keys(testData)
            self.driver.find_element_by_id("su").click()
            time.sleep(3)
            self.assertTrue(expectData in self.driver.page_source)
        except NoSuchElementException,e:
            logging.error(u"������ҳ��Ԫ�ز����ڣ��쳣��ջ��Ϣ��"+str(traceback.format_exc()))
        except AssertionError,e:
            logging.info(u"����%s����%sʧ��"%(testData,expectData))
        except Exception,e:
            logging.error(u"δ֪���󣬴�����Ϣ��"+traceback.format_exc())
        else:
            logging.info(u"����%s����%s�ɹ�"%(testData,expectData))

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
