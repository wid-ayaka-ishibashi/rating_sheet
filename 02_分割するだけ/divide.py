# %%
import os
import openpyxl as px
from IPython.display import display

divide_pre = "01_分割前"
divide_after = "02_分割後"
save_file_name = "2023年上期評価シート("

folder, subFolder, files in os.walk(divide_pre)
for file in files:
#       ext = os.path.splitext(file)[0] #拡張子変更考慮
#        files = [i for i in files if "_評価済み" in file]
    wb = px.load_workbook(folder + "\\" + file)
    sheetnames = wb.sheetnames
    sheetnames = [i for i in sheetnames if ("【" and "】") not in i]
    for sheetname in sheetnames:
        wb = px.load_workbook(folder + "\\" + file)
        for ws in wb.worksheets:
            if ws.title == sheetname:
                continue
            else:
                wb.remove(ws)
            ws = wb[sheetname]
            name = ws["A2"].value
        wb.save(divide_after + "\\" + save_file_name + name + ").xlsx")

# %%
