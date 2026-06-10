"""
员工数据调取程序
"""
#!/usr/bin/env python3
#_*_ coding:utf-8_*_
import pymysql

#数据库连接
def connect_db():
#连接MySQL，返回连接对象
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='emp',
        charset='utf8mb4'
    )
    return conn

#主菜单
def main_menu():
    print("\n" + "=" * 50)
    print(" 员工数据调取系统 v1.0")
    print("=" * 50)
    print("  [1] 总览仪表盘")
    print("  [2] 学历分析")
    print("  [3] 籍贯分布")
    print("  [4] 年龄分析")
    print("  [5] 性别比例")
    print("  [0] 退出系统")
    print("=" * 50)
    return input("  请选择功能：")

#功能函数

def dashboard(conn):
    """[1] 总览仪表盘"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM emp")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(age) FROM emp")
    avg_age = cursor.fetchone()[0]
    print(f"\n   总员工数：{total} 人")
    print(f"   平均年龄：{avg_age:.1f} 岁")

def edu_analysis(conn):
    """[2] 学历分析"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ed.degree, COUNT(*) AS cnt, AVG(e.age) AS avg_age
        FROM education ed
        JOIN emp e ON ed.emp_id = e.id
        GROUP BY ed.degree
        ORDER BY cnt DESC
    """)
    print("\n 学历分布：")
    print("  " + "-" * 28)
    for row in cursor:
        print(f"  {row[0]:4s}  {row[1]:3d} 人  平均年龄 {row[2]:.0f} 岁")


def place_analysis(conn):
    """[3] 籍贯分布"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT n.province, COUNT(*) AS cnt
        FROM native_place n
        JOIN emp e ON n.emp_id = e.id
        GROUP BY n.province
        ORDER BY cnt DESC
    """)
    print("\n 籍贯分布（TOP 10）：")
    print("  " + "-" * 22)
    for row in cursor:
        print(f"  {row[0]:6s}  {row[1]}人")


def age_analysis(conn):
    """[4] 年龄段分析"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            CASE
                WHEN age BETWEEN 25 AND 34 THEN '25-34岁'
                WHEN age BETWEEN 35 AND 44 THEN '35-44岁'
                WHEN age BETWEEN 45 AND 54 THEN '45-54岁'
                ELSE '55岁以上'
            END AS 年龄段,
            COUNT(*) AS cnt
        FROM emp
        GROUP BY 年龄段
        ORDER BY MIN(age)
    """)
    print("\n 年龄段分布：")
    print("  " + "-" * 22)
    for row in cursor:
        print(f"  {row[0]:8s}  {row[1]}人")


def gender_analysis(conn):
    """[5] 性别比例"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM emp")
    total = cursor.fetchone()[0]
    cursor.execute("""
        SELECT gender, COUNT(*) AS cnt
        FROM emp
        GROUP BY gender
    """)
    print("\n 性别比例：")
    print("  " + "-" * 22)
    for row in cursor:
        gender_label = '男' if row[0] == '男' else '女'
        pct = row[1] / total * 100
        print(f"  {gender_label}：{row[1]} 人 ({pct:.1f}%)")

#入口
if __name__ == "__main__":
    conn = connect_db()
    print("连接数据库成功")

    while True:
        choice = main_menu()
        if choice == '1':
            dashboard(conn)
        elif choice == '2':
            edu_analysis(conn)
        elif choice == '3':
            place_analysis(conn)
        elif choice == '4':
            age_analysis(conn)
        elif choice == '5':
            gender_analysis(conn)
        elif choice == '0':
            print(" 再见！")
            break
        else:
            print("请输入正确的数字..")

    conn.close()
