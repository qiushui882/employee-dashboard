import pandas as pd
import pymysql

# === 读 Excel ===
df = pd.read_excel("/mnt/e/excel/随机员工信息表.xlsx", sheet_name="员工信息表")

# === 拆籍贯：用省份名列表匹配 ===
provinces = ['黑龙江', '吉林', '辽宁', '北京', '天津', '上海', '重庆',
             '河北', '河南', '山东', '山西', '陕西', '甘肃', '青海', '四川',
             '贵州', '云南', '海南', '广东', '广西', '湖南', '湖北', '江西',
             '福建', '浙江', '江苏', '安徽', '西藏', '新疆', '宁夏', '内蒙古']

def split_place(place):
    for p in provinces:
        if place.startswith(p):
            return p, place[len(p):]
    return place, ""

# === 连接 MySQL ===
conn = pymysql.connect(host='localhost', user='root', password='123456', database='emp')
cursor = conn.cursor()

# === 逐行插入 ===
for _, row in df.iterrows():
    # 1. 插入 emp 表
    cursor.execute(
        "INSERT INTO emp (workernumber, name, gender, age, idcard, entry_date, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (row['员工工号'], row['姓名'], row['性别'], row['年龄'],
         row['身份证号码'], str(row['入职时间'])[:10], row['联系电话'])
    )
    emp_id = cursor.lastrowid  # 拿到自动生成的 id

    # 2. 插入 native_place
    province, city = split_place(row['籍贯'])
    cursor.execute(
        "INSERT INTO native_place (emp_id, province, city) VALUES (%s, %s, %s)",
        (emp_id, province, city)
    )

    # 3. 插入 education（学校/专业 Excel 没有，填"待补充"）
    cursor.execute(
        "INSERT INTO education (emp_id, school, degree, major) VALUES (%s, %s, %s, %s)",
        (emp_id, '待补充', row['学历'], '待补充')
    )

conn.commit()
conn.close()
print(f"完成！{len(df)} 条数据已写入三张表")
