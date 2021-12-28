# 设置报告窗口的标题
def set_windows_title(new_title):
    """
    设置打开的Allure报告的浏览器窗口标题文案
    :param new_title: 需要更改的标题文案-原文案为：Allure Report
    :return: 没有返回内容，调用此方法传入需要更改的文案即可修改窗体标题
    """
    report_path = r"Report/allureReport/index.html"
    # 定义为只读模型，并定义名称为：f
    with open(report_path, 'r+', encoding='utf-8') as f:
        all_the_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_the_lines:
            f.write(line.replace("Allure Report", new_title))
        f.close()


if __name__ == '__main__':
    set_windows_title("体测大师接口测试报告")