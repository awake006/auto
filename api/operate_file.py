import json
import os
import sys
import time

import xlsxwriter
import yaml

from api.data import Case, Count
from api.log import console_logger


def operate_json(path):
    '''
    Convert json file to dictionary
    '''
    try:
        with open(path, encoding="utf-8") as f:
            result = json.load(f)
            return result
    except FileNotFoundError as e:
        console_logger.error(e)
        sys.exit()


def operate_yaml(path):
    '''
    Convert yaml file to dictionary
    '''
    try:
        with open(path, encoding="utf-8")as f:
            result = yaml.load(f)
            return result
    except FileNotFoundError as e:
        console_logger.error(e)
        sys.exit()


def get_all_yaml(path):
    '''
    Get all yaml files
        @path: folder path
    '''
    try:
        result = [os.path.join(path, filename) for filename in os.listdir(
            path) if filename.split('.')[-1] == "yaml"]
        return result
    except FileExistsError as e:
        console_logger.error(e)
        sys.exit()


def import_case(path):
    '''
    Import use cases into the Case class
    '''
    file = get_all_yaml(path)
    case_list = []
    for i in file:
        case_list += operate_yaml(i)
    for case in case_list:
        Case.case[case.get('id')] = case
    console_logger.info('Use case import completed')


def set_excel(result, path):
    head_detail = ['id', "name", "url", "type", "expected/request", "return/db", "result"]
    head_about = ['fail', "success", "total"]
    name = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + ".xlsx"
    filename = os.path.join(path, name)
    filename = os.path.abspath(filename)
    workbook = xlsxwriter.Workbook(filename)
    sheet_about = workbook.add_worksheet("about")  # 设置表格为about
    sheet_detail = workbook.add_worksheet("detail")
    sheet_detail.set_column('B:C', 25)
    sheet_detail.set_column('E:F', 35)
    sheet_about.set_column('A:C', 25)
    td = workbook.add_format(
        {"bold": True, 'font_size': 15, 'align': 'center'})  # 设置表头样式
    th = workbook.add_format({'font_size': 14, 'align': 'center'})
    sheet_about.write_row("A1", head_about, td)
    sheet_detail.write_row("A1", head_detail, td)
    # 表格detail填充数据
    row = 1
    for value in result:
        sheet_detail.write_row(row, 0, value, th)
        row += 1
    # 表格about填充数据
    sheet_about.write(1, 0, Count.fail, th)
    sheet_about.write(1, 1, Count.success, th)
    sheet_about.write(1, 2, Count.total, th)
    chart = workbook.add_chart({"type": "pie"})
    # 从about表格获取pie数据
    chart.add_series(
        {
            'name': 'Interface test report',
            'categories': '=about!$A$1:$B$1',
            'values': '=about!$A$2:$B$2',
            'points': [{'fill': {'color': 'red'}}, {'fill': {'color': 'green'}}, ],
        }
    )
    chart.set_title({'name': 'Interface test statistics'})
    chart.set_style(3)
    sheet_about.insert_chart('A5', chart, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
    return filename


if __name__ == "__main__":
    print(operate_yaml(r"E:\PythonProject\APIAutoTest-master\config\base_info.yaml"))
