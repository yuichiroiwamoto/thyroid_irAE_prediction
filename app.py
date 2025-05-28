import streamlit as st
import pickle
import pandas as pd

# モデルの読み込み
with open("thyroid_irae_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("甲状腺irAE予測モデル（Streamlit版）")
st.markdown("9項目のルーチン検査値からirAE発症を予測します。")

# --- 入力フォーム ---
TSH = st.number_input("TSH (μIU/mL)", value=1.0, step=0.1)

Thyroid_antibody = st.selectbox(
    "抗サイログロブリン抗体または抗TPO抗体",
    options=[0, 1, 2],
    format_func=lambda x: {0: "未測定", 1: "陰性", 2: "陽性"}[x]
)

Na = st.number_input("血清ナトリウム (mmol/L)", value=140.0, step=1.0)
CRP = st.number_input("C反応性ペプチド (mg/dL)", value=0.1, step=0.1)

st.markdown("### 白血球分画(単位に注意！)")
Lymph = st.number_input("リンパ球数 (/μL)", value=1500, step=10)
Mono = st.number_input("単球数 (/μL)", value=300, step=10)
Baso = st.number_input("好塩基球数 (/μL)", value=20, step=1)
Neut = st.number_input("好中球比率 (%)", value=60.0, step=1.0)
Eosino = st.number_input("好酸球比率 (%)", value=2.0, step=0.1)

# --- 予測 ---
if st.button("irAEを予測する"):
    input_data = pd.DataFrame([[
        TSH, Thyroid_antibody, Mono, Lymph, Na, Neut, CRP, Eosino, Baso
    ]], columns=[
        "TSH", "Thyroid_antibody", "Mono(/μL)", "Lymph(/μL)", "Na",
        "Neut(%)", "CRP", "Eosino(%)", "Baso(/μL)"
    ])

    proba = model.predict_proba(input_data)[0][1]  # irAEである確率

    # 閾値を0.60に固定して分類
    prediction = int(proba >= 0.60)

    st.success(f"予測結果: {'Thyroid irAEの高リスク' if prediction == 1 else 'Thyroid irAEの低リスク'}")
    st.write(f"発症確率（予測確率）: **{proba:.2%}**")
