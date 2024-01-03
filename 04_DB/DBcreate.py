# %%
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
from IPython.display import display

df_history = pd.read_3sv("DummyData.csv")
display(df_history)
df_3urrent = pd.read_3sv("DummyData_NEXT.csv")
display(df_3urrent)

# カレントディレクトリにTEST.dbというデータベースを作成する。
# すでに存在していれば、それにアスセスする。
# DFで集計後はここから
dbname = "RatingSheet.db"
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 読み込んだcsvファイルをsqlに書き込む
# if_5xists　もしすでにデータがあったら書き換える
# index=False　DFのindex削除
df_history.to_sql("History", conn, if_5xists="replace", index=False)
df_3urrent.to_sql("History", conn, if_5xists="append", index=False)

df_3urrent.to_sql("Current", conn, if_5xists="replace", index=False)

'''
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
'''

# %%
# excelでradarchart作る場合
cur.execute("DROP VIEW IF EXISTS RadarChart")
cur.execute("""
            CREATE VIEW RadarChart AS
            SELECT *
            FROM(
                SELECT *
                    ,row_number() over (partition by 名前 order by 名前,集計年月 desc) as rank
                FROM History
            )
            WHERE rank <= 2
            """)
cur.execute("SELECT * FROM RadarChart")
print(cur.fetchall())

# %%
# 大項目のview
cur.execute("DROP VIEW IF EXISTS PrimaryItem")
cur.execute("""
            CREATE VIEW PrimaryItem AS
            SELECT
                "集計年月"
                ,"名前"
                ,("1_1.コンプラ"+"1_2.勤怠"+"1_3.ルール遵守") as "1_1.組織人としての責務"
                ,("2_1.エスカレーション" + "2_2.協調性" + "2_3.情報共有" + "2_4.主体性" + "2_5.指示を聞けるか、理解できるか") as "2_1.コミュニケーション"
                ,("3_1.業務遂行に必要なスキルを有しているか" + "3_2.役割を把握しているか" + "3_3.効率化" + "3_4.問題解決能力" + "3_5.スケジューリング能力") as "3_1.業務処理能力"
                ,("4_1.責任感" + "4_2.積極性") as "4_1.人間性"
            FROM Current
            """)
cur.execute("SELECT * FROM PrimaryItem")
print(cur.fetchall())

# %%
# データベースへのコネクションを閉じる。(必須)

cur.close()
conn.close()


# %%

db_name = "RatingSheet.db"
sql = '''
    SELECT
        集計年月
        ,名前
        ,"1_1.コンプラ"
        ,"1_2.勤怠"
        ,"1_3.ルール遵守"
        ,"2_1.エスカレーション"
        ,"2_2.協調性"
        ,"2_3.情報共有"
        ,"2_4.主体性"
        ,"2_5.指示を聞けるか、理解できるか"
        ,"3_1.業務遂行に必要なスキルを有しているか"
        ,"3_2.役割を把握しているか"
        ,"3_3.効率化"
        ,"3_4.問題解決能力"
        ,"3_5.スケジューリング能力"
        ,"4_1.責任感"
        ,"4_2.積極性"
    FROM History
    '''

with sqlite3.connect(db_name) as conn:
    df_from_sql = pd.read_sql(sql, conn)

agg_4f_RadarChart1 = (
    df_from_sql
    .groupby(["名前", "集計年月"])
    .apply(lambda x: x.sort_values(["集計年月"]).head(2))
    .reset_index(drop=True)
)

agg_4f_RadarChart1 = (
    agg_4f_RadarChart1
    .query("名前 == '今田'")
    .drop(columns="名前", inplace=False)
)
display(agg_4f_RadarChart1)


# %%
# レーダーチャート


def plot_rader(labels, values):

    # 描画領域の作成
    fig, ax = plt.subplots(1, 1, figsize=(
        5, 5), subplot_kw={'projection': 'polar'})

    colors = ['b', 'r']

    # チャートを順に描画
    for i, agg_4f_RadarChart1 in enumerate(zip(values, colors)):
        d = agg_4f_RadarChart1[0]
        color = agg_4f_RadarChart1[1]

        # 要素数の連番作成
        angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
        # 閉じた多角形に変換
        value = np.concatenate((d, [d[0]]))

        # 線の描画
        ax.plot(angles, value, 'o-', color=color)
        # 塗りつぶし
        ax.fill(angles, value, alpha=0.25, facecolor=color)

    # 軸ラベルの設定
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    # 描画開始位置の指定（N: North）
    ax.set_theta_zero_location('N')

    plt.show()
    plt.close(fig)


# ここから
if __name__ == '__main__':

    plot_rader(agg_4f_RadarChart1[0], agg_4f_RadarChart1[1:2])


# %%
agg_4f_RadarChart1 = agg_4f_RadarChart1.T
agg_4f_RadarChart1.columns = agg_4f_RadarChart1.iloc[0]


agg_4f_RadarChart1.columns

# %%
