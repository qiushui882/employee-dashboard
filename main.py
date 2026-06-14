from fastapi import FastAPI
import pymysql

app = FastAPI()

def get_db():
    """连接数据库"""
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='emp',
        charset='utf8mb4'
)

@app.get("/employees/count")
def employee_count():
    """总览：员工总数和平均年龄"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(age) FROM emp")
    row = cursor.fetchone()
    conn.close()
    return {"总人数": row[0], "平均年龄": round(row[1], 1)}

@app.get("/employees/analysis/degree")
def degree_analysis():
    """学历分析"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ed.degree, COUNT(*) AS 人数, AVG(e.age) AS 平均年龄
        FROM education ed
        JOIN emp e ON ed.emp_id = e.id
        GROUP BY ed.degree
        ORDER BY 人数 DESC
    """)
    results = []
    for row in cursor:
        results.append({
            "学历": row[0],
            "人数": row[1],
            "平均年龄": round(row[2], 1)
        })
    conn.close()
    return {"学历分析": results}

@app.get("/employees/analysis/province")
def province_analysis():
    """籍贯分布"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT n.province, COUNT(*) AS cnt
        FROM native_place n
        JOIN emp e ON n.emp_id = e.id
        GROUP BY n.province
        ORDER BY cnt DESC
    """)
    results = []
    for row in cursor:
        results.append({"省份": row[0], "人数": row[1]})
    conn.close()
    return {"籍贯分布": results}


@app.get("/employees/analysis/age_group")
def age_group_analysis():
    """年龄段分析"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            CASE
                WHEN age BETWEEN 25 AND 34 THEN '25-34岁'
                WHEN age BETWEEN 35 AND 44 THEN '35-44岁'
                WHEN age BETWEEN 45 AND 54 THEN '45-54岁'
                ELSE '55岁以上'
            END AS age_group,
            COUNT(*) AS cnt
        FROM emp
        GROUP BY age_group
        ORDER BY MIN(age)
    """)
    results = []
    for row in cursor:
        results.append({"年龄段": row[0], "人数": row[1]})
    conn.close()
    return {"年龄段分析": results}


@app.get("/employees/analysis/gender")
def gender_analysis():
    """性别比例"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM emp")
    total = cursor.fetchone()[0]
    cursor.execute("""
        SELECT gender, COUNT(*) AS cnt
        FROM emp
        GROUP BY gender
    """)
    results = []
    for row in cursor:
        pct = round(row[1] / total * 100, 1)
        results.append({"性别": row[0], "人数": row[1], "占比": f"{pct}%"})
    conn.close()
    return {"总人数": total, "性别比例": results}


@app.get("/employees/analysis/entry_year")
def entry_year_analysis():
    """入职年份统计"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT YEAR(entry_date), COUNT(*)
        FROM emp
        GROUP BY YEAR(entry_date)
        ORDER BY YEAR(entry_date)
    """)
    results = []
    for row in cursor:
        results.append({"入职年份": row[0], "人数": row[1]})
    conn.close()
    return {"入职年份统计": results}
