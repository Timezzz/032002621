import re
import os
import xlwt
import cProfile,pstats
city_list = ['中国大陆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
             '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆']
def save_data(worksheet, data1, data2, filename):
    col1 = ['地区', '新增确诊', '新增无症状']
    for j in range(0, 3):
        worksheet.write(0, j, col1[j])

    for i in range(0,32):
        worksheet.write(i + 1, 0, city_list[i])
    #初始化表格
    worksheet.write(1, 1, data1)#本土新增确诊
    worksheet.write(1, 2, data2)#本土新增无症状


def save_data1(worksheet, workbook, i,col, data, filename):
    worksheet.write(i, col, data)
    name = os.path.splitext(filename)[0]
    workbook.save('D:/python/mydatas/' + name + '.xls')
    #保存数据到excel表格


def readfile(path, filename):
    with open(path + '/' + filename, 'r', encoding='utf-8') as f:
        str_data = f.read()
        data_ml1 = re.findall(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例(.+?)例", str_data)
        data_ml2 = re.findall(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者(.+?)例", str_data)
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('数据统计', cell_overwrite_ok=True)
        save_data(worksheet, data_ml1, data_ml2, filename)#初始化工作表，并将本土新增确诊和本土新增无症状填入


        try:
            str_data_p = re.findall(r"本土病例(.+?)），含", str_data)[0]
        except IndexError:
            return
        # 提取本土病例的这整段话
        # 提取地区名称
        data_p_all = re.findall('[\u4e00-\u9fa5]+', str_data_p)
        data_p_all.pop(0)#去掉’本土病例‘这四个字
        # 提取数据
        data_num = re.findall(r"\d+\.?\d*", str_data_p)
        data_num.pop(0)#去掉’本土病例‘的数字
        cnt=0
        for city in data_p_all:
            if city_list.count(city)==0:
                continue
            save_data1(worksheet,workbook,city_list.index(city)+1,1,data_num[cnt],filename)
            cnt += 1
        #提取新增无症状的一整段话
        try:
            str_data_p2=re.findall(r'新增无症状感染者(.*?)）。',str_data)[0]
        except IndexError:
            return
        data_p2_all=re.findall('[\u4e00-\u9fa5]+', str_data_p2)
        data_p2_all.pop(0)
        data_num2=re.findall(r"\d+\.?\d*", str_data_p2)
        data_num2.pop(0)
        data_num2.pop(0)
        data_num2.pop(0)
        cnt = 0
        for city in data_p2_all:
            if city_list.count(city)==0:
                continue
            save_data1(worksheet, workbook, city_list.index(city) + 1, 2, data_num2[cnt],filename)
            cnt += 1

if __name__ == "__main__":
    filepath = 'D:/python/mydatas/'
    files = os.listdir(filepath)
    for file in files:
        readfile(filepath, file)
        basename = os.path.splitext(file)[0]
        print(basename)