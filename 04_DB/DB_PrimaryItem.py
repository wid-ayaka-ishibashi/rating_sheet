# %%
import sqlite3
import pandas as pd
from IPython.display import display

dbname = "RatingSheet.db"
table_name = 'PrimaryItem'
sql = '''
    select *
    from PrimaryItem
    '''

# SQLiteに書き込む
with sqlite3.connect(dbname) as conn:
    df_from_sql_PrimaryItem = pd.read_sql(sql, conn)

# %%


def df_PrimaryItem_DeviationValue(PrimaryItem):
    df_score = df_from_sql_PrimaryItem[PrimaryItem]
    df_score_std = df_score.std(ddof=0)
    df_score_mean = df_score.mean()
    df_from_sql_PrimaryItem[f"{PrimaryItem} (偏差値)"] = df_score.map(
        lambda x: round((x - df_score_mean) / df_score_std * 10 + 50)
    ).astype(int)


PrimaryItems = [
    "1_1.組織人としての責務",
    "2_1.コミュニケーション",
    "3_1.業務処理能力",
    "4_1.人間性"
]

for PrimaryItem in PrimaryItems:
    df_PrimaryItem_DeviationValue(PrimaryItem)

display(df_from_sql_PrimaryItem)
# %%

df_from_sql_PrimaryItem.to_sql(
    "Current_Primary_DeviationValue", conn, if_exists="replace", index=False)

# %%
