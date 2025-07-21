import streamlit as st
from sbs_s2 import run_sbs_step2
from sbs_s3 import run_sbs_step3
import json

st.title("📊 DCF Projection Pipeline")

version = st.text_input("請輸入測試版本編碼", value="20250721.1")
openai_api_key = 'open_api_key'

company = st.text_input("請輸入公司代碼", value="AAPL")
valuation_date = st.text_input("請輸入估值基準年份", value="2014")

col1, col2 = st.columns(2)
with col1:
    discount_rate = st.number_input("折現率 (%)", min_value=0.0, value=10.0)
with col2:
    terminal_growth_rate = st.number_input("終值成長率 (%)", min_value=0.0, value=2.5)

st.markdown("---")
st.subheader("📝 歷史財報數據 (JSON 格式)")
def_hist_data = json.dumps([
    {
        "filed_date": "2010-12-31",
        "revenue": 100000000,
        "ebit": 15000000,
        "capex": 5000000,
        "average_debt": 20000000,
        "effective_income_tax_rate": 0.21
    },
    {
        "filed_date": "2011-12-31",
        "revenue": 110000000,
        "ebit": 16000000,
        "capex": 5200000,
        "average_debt": 21000000,
        "effective_income_tax_rate": 0.20
    }
], indent=2)

hist_data_json = st.text_area("請貼上歷史財報數據 (JSON)", value=def_hist_data, height=200)

if st.button("🚀 執行 Step 2: 預測財報"):
    try:
        historical_data = json.loads(hist_data_json)
        sbs2_output = run_sbs_step2(
            openai_api_key=openai_api_key,
            company=company,
            valuation_date=valuation_date,
            historical_data=historical_data,
            testnum=version
        )
        st.success("✅ Step 2 完成並已儲存")
        st.code(sbs2_output, language="json")
    except Exception as e:
        st.error(f"❌ 執行失敗：{e}")

if st.button("🚀 執行 Step 3: 計算 DCF 最終估值"):
    try:
        sbs3_output = run_sbs_step3(
            openai_api_key=openai_api_key,
            discount_rate=discount_rate,
            terminal_growth_rate=terminal_growth_rate,
            testnum=version
        )
        st.success("✅ Step 3 完成並已儲存")
        st.code(sbs3_output, language="json")
    except Exception as e:
        st.error(f"❌ 執行失敗：{e}")
