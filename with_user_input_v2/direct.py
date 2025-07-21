from openai import OpenAI
import pandas as pd
import json

def get_csv_data_as_text(csv_path, valuation_year, format_type="json", date_column="year"):
    """
    讀取 CSV，篩選 valuation_year 之前的資料，轉為字串

    Args:
        csv_path (str): CSV 檔案路徑
        valuation_year (int): 估值基準年，僅保留該年以前資料
        format_type (str): "json" 或 "markdown"
        date_column (str): 年份欄位名稱，預設為 "year"

    Returns:
        str: 可嵌入 Prompt 的字串
    """
    df = pd.read_csv(csv_path)

    if date_column not in df.columns:
        raise ValueError(f"指定的日期欄位 '{date_column}' 不存在於 CSV 中")

    df_filtered = df[df[date_column] <= valuation_year]

    if df_filtered.empty:
        return f"No data available before valuation year {valuation_year}."

    if format_type == "json":
        return json.dumps(df_filtered.to_dict(orient="records"), indent=2, ensure_ascii=False)

    elif format_type == "markdown":
        header = "| " + " | ".join(df_filtered.columns) + " |"
        separator = "| " + " | ".join(["---"] * len(df_filtered.columns)) + " |"
        rows = ["| " + " | ".join(map(str, row)) + " |" for row in df_filtered.values]
        return "\n".join([header, separator] + rows)

    else:
        raise ValueError("format_type must be 'json' or 'markdown'")


def generate_dcf_prompt(
    openai_api_key,
    company,
    valuation_year,
    user_prompt_direct,
    testnum,
    model="gpt-4.1-nano",
    temperature=0.2,
    max_tokens=2000
):

data_for_prompt = get_csv_data_as_text('path to the csv', valuation_year=2014, format_type="json")




    SYSTEM_PROMPT = f"""
You are a professional financial analyst.

You have access to historical financial data provided, containing all key metrics necessary for financial analysis.
The historical financial data: {data_for_prompt}

Your task is to strictly follow the formatting and presentation guidelines described below.  
Your output will be shown directly on a webpage — it must be clear, well-structured, and require **no further processing**.

---

## 🔵 Formatting Rules (Strictly Mandatory):

1️⃣ **All output must be written in clean, well-structured Markdown.**  
2️⃣ **You must divide the output into clear sections with headings.**  
3️⃣ **Use Markdown tables for any multi-year projections or scenario comparisons.**  
4️⃣ **Every table must have a header row and appropriate column labels.**  
5️⃣ **For every financial metric you project, you must:**
- Present a 5-year projection in table format.
- Provide a separate paragraph explaining the reasoning behind the projection.
  
6️⃣ **Explain all calculations (e.g., Free Cash Flow, Terminal Value, Discounting) in concise, structured paragraphs.**  
7️⃣ **Summarize final implied stock price in a Markdown table with scenarios.**  
8️⃣ **Do NOT output JSON, code snippets, or unstructured text blocks.**

---

## 📝 Example Output Structure:

### 1️⃣ Selected Data & SQL Queries

> **SQL-like Query Example:**  
> `SELECT revenue, ebit FROM financials WHERE year >= 2010`  

> **Reasoning:**  
> Revenue and EBIT are key drivers for cash flow and profitability, historically stable for this company.

---

### 2️⃣ 5-Year Financial Projection

| Metric | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|--------|--------|--------|--------|--------|--------|
| Revenue Growth (%) | 12.5 | 12.0 | 11.5 | 11.0 | 10.5 |
| EBIT Margin (%) | 15.0 | 15.5 | 16.0 | 16.5 | 17.0 |
| Effective Tax Rate (%) | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |
| D&A (%) | 4.5 | 4.4 | 4.3 | 4.2 | 4.1 |
| CapEx (%) | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 |
| Change in NWC (%) | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 |

> **Reasoning for Revenue Growth:**  
> The company's revenue is expected to decelerate slightly due to market saturation, though sustained demand in core markets supports stable growth.

---

### 3️⃣ Methodology & Calculations

- **Free Cash Flow:**  
  Projected using EBIT minus taxes, plus depreciation & amortization, less CapEx and changes in net working capital.

- **Terminal Value:**  
  Estimated using the Gordon Growth Model with a terminal growth rate of 2.5%.

- **Discounting:**  
  Applied at a 10% discount rate over the 5-year projection period.

---

### 4️⃣ Implied Stock Price Summary

| Scenario | Implied Stock Price |
|----------|----------------------|
| Optimistic | 150.00 |
| Base | 120.00 |
| Pessimistic | 90.00 |

---

### 5️⃣ Summary of Reasoning

The projections reflect realistic market growth rates, conservative expense assumptions, and industry benchmarks.  
The implied stock prices capture varying degrees of operational success under different scenarios.

---

## ❗ Important:
- Stick to this structure exactly.
- Never include JSON, code, or raw output.
- Present all results in Markdown-formatted text.
"""

    
    
    
    USER_PROMPT = f"""
{user_prompt_direct}
"""

    
    
    
    USER_PROMPT_Default= """You are tasked with performing a complete end-to-end DCF valuation for **{company}** as of **{valuation_date}**.

Your mission is to:
- Select the relevant data points for valuation.
- Decide how to query this data using SQL-like expressions.
- Provide reasoning for selecting each data point.
- Project the following financial metrics for the next 5 years, giving both the **values** and the **reasoning behind each projection**:
  - Revenue growth
  - EBIT margin
  - Effective income tax rate
  - Depreciation & amortization percentage
  - CapEx percentage
  - Change in net working capital percentage

For each projected metric, explain **why you chose these specific projection values**, considering industry factors, company performance, and economic outlook.

After projection:
- Calculate free cash flows.
- Estimate terminal value.
- Discount the projected cash flows and terminal value.
- Present the final implied stock price for each scenario (**optimistic**, **base**, **pessimistic**).

Be thorough, explain your thought process, and justify all assumptions.
"""

    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content
