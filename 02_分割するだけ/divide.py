# %%
import os
import openpyxl as opxl
from IPython.display import display

for root, dirs, files in os.walk("./01_分割前"):
    for file in files:
        ext = os.path.splitext(file)[1]
        print(ext)


# %%
'''
wb = opxl.load_workbook("02_分割するだけ\\01_分割前\現場評価シート（DDC様向け）_20231110_評価済み.xlsx")
ws =
'''
