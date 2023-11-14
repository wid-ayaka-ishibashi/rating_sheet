# %%
import os
import openpyxl as px
from IPython.display import display

divide_pre = "01_分割前"
divide_after = "02_分割後"
save_file_name = "2023年上期評価シート("

# ファイル名のリストを作る
files = [file for folder, subFolder, files in os.walk(divide_pre) for file in files]

for file in files:
    wb = px.load_workbook(divide_pre + "\\" + file)
    sheetnames = [i for i in wb.sheetnames if ("【" and "】") not in i]

    for sheetname in sheetnames:
        wb = px.load_workbook(divide_pre + "\\" + file)

        # 不要なシートを削除する
        for ws in wb.worksheets:
            if ws.title != sheetname:
                wb.remove(ws)
        ws = wb[sheetname]
        # フルネームを取得する
        name = ws["A2"].value

        wb.save(divide_after + "\\" + save_file_name + name + ").xlsx")

# %%
