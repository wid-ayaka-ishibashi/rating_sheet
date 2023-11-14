# %%
import os
import openpyxl as opxl
from IPython.display import display

divide_pre = "01_分割前"
divide_after = "02_分割後"
save_file_name = "2023年上期評価シート("

for folder, subFolder, files in os.walk(divide_pre):
    for file in files:
#        ext = os.path.splitext(file)[0] #拡張子変更考慮
        if "_評価済み" in file:
            wb = opxl.load_workbook(folder + "\\" + file)
            sheetnames = wb.sheetnames
            for sheetname in sheetnames:
                if "【" and "】" not in sheetname:
                    sheet = wb[sheetname]
                    name = sheet["A2"].value
                    wb.remove(sheet)
                    wb.save(divide_after + "\\" + save_file_name + name + ").xlsx")

# %%
