import pymysql

import requests
import json
import xlwt
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkTWFwIjp7ImJlbG9uZyI6IjEiLCJhcHBsaWNhdGlvbiI6Imdsc3gtbmUtc2hpZWxkLXVzZXJjZW50ZXIiLCJjbGF6eiI6ImNvbS5nbHN4LnBsYXQuand0LmJhc2UuQ29tSnd0VXNlciIsInVzZXJJZCI6IjEiLCJhY2NvdW50IjoiYWRtaW4iLCJ0ZW5hbnQiOiIxIiwiand0SWQiOiJnbHN4LW5lLXNoaWVsZC11c2VyY2VudGVyOjdhNjYwYTE1LWY0M2MtNGE5MC1hMmYzLTE5MmYzZmZkNjc1NV9KV1QtU0VTU0lPTi0xIn0sInN1YiI6ImFkbWluIiwiZXhwIjoxNjM0ODM1Njg3LCJpYXQiOjE2MzQ4MDY4ODcsImp0aSI6Imdsc3gtbmUtc2hpZWxkLXVzZXJjZW50ZXI6N2E2NjBhMTUtZjQzYy00YTkwLWEyZjMtMTkyZjNmZmQ2NzU1X0pXVC1TRVNTSU9OLTEifQ.PusCYQDJ5OitEHlB4uC2ad4pVlyQAuBlg8m2lUG1qRM"
}

s = requests.Session()
requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)


class Kls(object):
    @staticmethod
    def getData(sn):
        url = 'https://eshield.didihu.com.cn/devicemonitor/api/location/single'
        params = {"sn": sn, "deviceCode": "gps"}
        response = s.get(url=url, params=params, headers=headers)
        return response


if __name__ == '__main__':
    conn = pymysql.connect(host='192.168.5.22',
                           port=3307,
                           user='user_yangll',
                           password='vGxw9jWg',
                           database='gps',
                           charset='utf8',
                           autocommit='True')

    cursor = conn.cursor()
    sql01 = '''
    SELECT 
    dvw.sqbh,
    dv.`name`,
    dv.standno,
    ddl.lastRtTrack,
    dti.sn
    FROM d_vehicle dv 
    left join d_vehicle_workorder dvw on dvw.standno = dv.standno
    left join d_class dc on dc.classid = dv.classId
    left join d_group dg on dg.vehicleGroupId = dc.vehicleGroupId
    left join d_track_info dti on dti.userId = dv.userId
    left join d_device_login ddl on ddl.sn = dti.sn 
    WHERE dv.`status` = 0 
    and dg.groupName like '%广汇%' and dg.groupName != '广汇江西自采';
        '''
    cursor.execute(sql01)
    gHinfoList = cursor.fetchall()

    excelList = list()
    num = 0
    for gHinfo in gHinfoList:
        num = num + 1
        if num != 0 and num % 75 == 0:
            print('进程开始等待15秒')
            time.sleep(15)

        dataLit = list()
        dataLit.append(str(gHinfo[0]))
        dataLit.append(str(gHinfo[1]))
        dataLit.append(str(gHinfo[2]))
        dataLit.append(str(gHinfo[3]))
        dataLit.append(str(gHinfo[4]))

        response = Kls().getData(gHinfo[4])
        print(response.text)
        jsonStr = json.loads(response.text)
        print(jsonStr['data'])
        if jsonStr['data'] is not None:
            if jsonStr['data']['gpsLocation'] is not None:
                gpsAdress = jsonStr['data']['gpsLocation']['address']
                print(gpsAdress)
                dataLit.append(str(gpsAdress))
            elif jsonStr['data']['bsLocation'] is not None:
                gpsAdress = jsonStr['data']['bsLocation']['address']
                print(gpsAdress)
                dataLit.append(str(gpsAdress))
            elif jsonStr['data']['wifiLocation'] is not None:
                gpsAdress = jsonStr['data']['wifiLocation']['address']
                print(gpsAdress)
                dataLit.append(str(gpsAdress))

        with open("F:\\tmp\\data.txt", "a+") as f:
            print('开始写文件===')
            print(dataLit)
            f.writelines(','.join(dataLit))
            f.write('\n')
            print('num===', num)
        excelList.append(dataLit)

        # 生成表格文件
    # print('开始写文件===')
    # # 初始化样式
    # style_head = xlwt.XFStyle()
    # # 初始化字体相关
    # font = xlwt.Font()
    # font.name = "微软雅黑"
    # font.bold = True
    # # 必须是数字索引
    # font.colour_index = 1
    # # 初始背景图案
    # bg = xlwt.Pattern()
    # # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    # bg.pattern = xlwt.Pattern.SOLID_PATTERN
    # # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    # bg.pattern_fore_colour = 4
    #
    # # 设置字体
    # style_head.font = font
    # # 设置背景
    # style_head.pattern = bg
    #
    # # 创建一个excel
    # excel = xlwt.Workbook(encoding='utf-8')
    # # 添加工作区
    # sheet = excel.add_sheet('广汇租赁')
    # # xlwt中是行和列都是从0开始计算的
    # first_col_1 = sheet.col(1)
    # first_col_2 = sheet.col(2)
    # first_col_3 = sheet.col(3)
    # # 设置创建时间宽度
    # first_col_1.width = 256 * 15
    # # 设置存储路径列宽度
    # first_col_3.width = 256 * 100
    # # 标题信息
    # head = ["申请编号", "姓名", "车架号", "分类名称", "主设备最后GPS时间", "主设备最后gps地址", "预警类型"]
    # for index, value in enumerate(head):
    #     sheet.write(0, index, value, style_head)
    #
    # # 循环写入
    # for index, value_list in enumerate(excelList, 1):
    #     for i, value in enumerate(value_list):
    #         sheet.write(index, i, value)
    #
    # # 保存excel
    # file_name = time.time()
    # excel.save("F:\\tmp\\%s.xls" % file_name)
    # print('写文件完成===')
