# %%
import sqlite3
import pandas as pd
from IPython.display import display

df_history = pd.read_csv("DummyData.csv")
display(df_history)
df_current = pd.read_csv("DummyData_NEXT.csv")
display(df_current)

# カレントディレクトリにTEST.dbというデータベースを作成する。
# すでに存在していれば、それにアスセスする。
#DFで集計後はここから
dbname = "RatingSheet.db"
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# dbのnameをsampleとし、読み込んだcsvファイルをsqlに書き込む
# if_exists　もしすでにデータがあったら書き換える
#index=False　DFのindex削除
df_history.to_sql("History", conn, if_exists="replace", index=False)
df_current.to_sql("History", conn, if_exists="append", index=False)

df_current.to_sql("Current", conn, if_exists="replace", index=False)



# 作成したデータベースを1行ずつ見る
select_sql = """
    SELECT *
    FROM History
    """
#for row in cur.execute(select_sql):
#    print(row)

# DB内の全テーブルをfetchall()を使って、printする。
cur.execute(select_sql)
print(cur.fetchall())

# %%
# データベースへのコネクションを閉じる。(必須)
cur.close()
conn.close()

# %%
