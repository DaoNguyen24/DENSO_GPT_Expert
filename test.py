import fitz
import pandas
tables =[]
i = 200000000000000
table = f'table {i}'
data = pandas.ExcelFile("sample pdf/thay thế Motor trục - Robot.xlsx")
for sheetname in data.sheet_names:
    df = pandas.read_excel(data, sheet_name=sheetname).fillna('').values.astype(str)
    df = [','.join(val) for val in df]
    df = '\n'.join(df)
    table += '\n' + df
    tables.append(table)

print(tables)

