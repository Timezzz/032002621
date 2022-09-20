import os
import xlrd
from pyecharts.charts import map
from pyecharts import options as opts


def visualize(filename):
    basename = os.path.splitext(filename)[0]
    data = xlrd.open_workbook(filename)

    table = data.sheets()[0]

    attr = ['中国大陆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
             '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆']
    datas = []

    for i in range(1, table.nrows):
        a = table.row_values(i)
        da = a[1]
        datas.append(da)


    map_virus = Map("新增确诊数据统计", width=1000, height=800)
    map_virus.add("China", attr, datas, is_map_symbol_show=True, maptype='china', is_visualmap=True, is_piecewise=True,
                  visual_text_color='#000',
                  is_label_show=True, pieces=[
            {"max": 10000, "min": 1001, "label": ">1000"},
            {"max": 1000, "min": 500, "label": "500-1000"},
            {"max": 499, "min": 200, "label": "200-499"},
            {"max": 199, "min": 100, "label": "100-199"},
            {"max": 99, "min": 10, "label": "10-99"},
            {"max": 9, "min": 1, "label": "1-9"}])
    map_virus.render('疫情地图.html')
    bar.render('D:\python\homeworks\example\mydatas\可视化' + basename + '.html')
    print(basename)


if __name__ == '__main__':
    spath = 'D:\python\homeworks\example\mydatas\excel表格'
    files = os.listdir(spath)
    for file in files:
        visualize(file)