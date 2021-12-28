import os
import pytest
from Common.jsonAlter import JsonAlter
from Common.report_windows_title import set_windows_title

w = JsonAlter()

if __name__ == '__main__':
    pytest.main()
    os.system('copy environment.properties temp\my_allureReport\environment.properties')
    os.system('allure generate ./temp/my_allureReport -o ./report/allureReport --clean')
    reportName = w.get_json_data("体测大师-接口自动化测试报告")
    w.write_json_data(reportName)
    set_windows_title("体测大师接口测试报告")
