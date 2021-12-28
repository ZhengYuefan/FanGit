import json
import os

# project_path = os.path.split(os.path.realpath(__file__))
project_path = 'Report/allureReport/widgets/summary.json'
dict = {}


class JsonAlter:
    # 获取summary.json里面的数据
    def get_json_data(self, name):
        # 定义为只读模型，并定义名称为f
        with open(f'{project_path}', 'rb') as f:
            # 加载json文件中的内容给params
            params = json.load(f)
            # 修改内容
            params['reportName'] = name
            # 将修改后的内容保存在dict中
            dict = params

        f.close()
        return dict

    def write_json_data(self, dict):
        with open(f'{project_path}', 'w', encoding='utf-8') as w:
            json.dump(dict, w, ensure_ascii=False, indent=4)

        w.close()


if __name__ == '__main__':
    w = JsonAlter()
    reportName = w.get_json_data("体测大师接口自动化测试报告")
    w.write_json_data(reportName)


