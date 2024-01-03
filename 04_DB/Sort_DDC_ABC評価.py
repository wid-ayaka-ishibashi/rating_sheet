# %%
import pandas as pd
import numpy as np
from IPython.display import display

# サンプルデータの作成
df = pd.read_csv(
    "sample_data\\4段階5項目のパターン表_個数カウント.csv",
    encoding="shift-jis", index_col=None
)

rename_cols = ["1", "2", "3", "4"]
df.rename(columns={
    rename_col: f"Count_{rename_col}" for rename_col in rename_cols}, inplace=True)

display(df.head())

"""
for n in range(1, 5):
    df["count_" + str(n)] = df.apply(lambda x: sum(x == n), axis=1)
"""

# %%
DDC_data_3 = pd.read_csv(
    "sample_data\DDC_評価データ_3.csv")
display(DDC_data_3)
# %%
