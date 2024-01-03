# %%
import pandas as pd
import numpy as np
from IPython.display import display

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# サンプルデータの作成
df = pd.read_csv("sample_data\\4段階5項目のパターン表_石橋.csv",
                 encoding="shift-jis")

# 特徴量とラベルに分割
X = df[['2_1', '2_2', '2_3', "2_4", "2_5"]]
y = df['label']


# KFoldのインスタンスを作成
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 分割ごとにスコアを算出
scores = []

# 交差検証
for train_index, test_index in kf.split(df):
    # データを分割
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    # モデルの学習
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)
    # モデルの評価
    y_pred = rf_model.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    scores.append(score)

# スコアの平均値と標準偏差を表示
print(f"Mean score: {np.mean(scores):.3f}")
print(f"Standard deviation: {np.std(scores):.3f}")


"""
# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train, y_train, test_size=0.3, random_state=0)

# ランダムフォレストモデルの構築
rf_model = RandomForestClassifier(
    n_estimators=10, random_state=0)
rf_model.fit(X_train, y_train)

# テストデータでの予測
y_pred = rf_model.predict(X_valid)

# 分類精度の評価
accuracy = accuracy_score(y_valid, y_pred)
print(f'Accuracy: {accuracy}')
"""

# %%
DDC_data_2 = pd.read_csv(
    "sample_data\DDC_評価データ_2.csv")
prediction = rf_model.predict(DDC_data_2)
# print(f'Predicted Class: {prediction}')

DDC_data_2["label"] = prediction
display(DDC_data_2)

DDC_data_3 = pd.read_csv(
    "sample_data\DDC_評価データ_3.csv")
prediction = rf_model.predict(DDC_data_3)
# print(f'Predicted Class: {prediction}')

DDC_data_3["label"] = prediction
display(DDC_data_3)

# %%
