import pandas as pd 

# 这个路径在 WSL 里就是 /mnt/e/...
file_path = "/mnt/e/excel/随机员工信息表.xlsx"

# 先看有几个 Sheet
xls = pd.ExcelFile(file_path)
print("Sheet 列表：", xls.sheet_names)
print()

# 逐个 Sheet 看前 3 行
for sheet in xls.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(f"===== Sheet: {sheet} =====")
    print(f"行数: {len(df)}")
    print(f"列名: {list(df.columns)}")
    print(df.head(3))
    print()
