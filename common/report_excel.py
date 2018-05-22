import os
import time

import xlsxwriter

from common.count_case import CountResult


class ReportExcel(object):
    def __init__(self, result, path, head_detail=['id', "name", "url", "type", "expectedValues", "returnValue", "result"], head_about=['fail', "success", "total"]):
        self.result = result

        self.head_detail = head_detail
        self.head_about = head_about
        self.path = path

    def set_excel(self):
        name = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + ".xlsx"
        filename = os.path.join(self.path, name)
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
        sheet_about.write_row("A1", self.head_about, td)
        sheet_detail.write_row("A1", self.head_detail, td)
        # 表格detail填充数据
        row = 1
        for value in self.result:
            sheet_detail.write_row(row, 0, value, th)
            row += 1
        # 表格about填充数据
        sheet_about.write(1, 0, CountResult.fail, th)
        sheet_about.write(1, 1, CountResult.success, th)
        sheet_about.write(1, 2, CountResult.total, th)
        chart = workbook.add_chart({"type": "pie"})
        # 从about表格获取pie数据
        chart.add_series(
            {
                'name': '接口测试报表图',
                'categories': '=about!$A$1:$B$1',
                'values': '=about!$A$2:$B$2',
                'points': [{'fill': {'color': 'red'}}, {'fill': {'color': 'green'}}, ],
            }
        )
        chart.set_title({'name': '接口测试统计'})
        chart.set_style(3)
        sheet_about.insert_chart('A5', chart, {'x_offset': 25, 'y_offset': 10})
        workbook.close()
        return filename
