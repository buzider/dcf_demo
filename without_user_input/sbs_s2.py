import json
import os
from openai import OpenAI

def run_sbs_step2(openai_api_key, company, valuation_date, historical_data, testnum):
    output_path=f'/Users/buzider/Desktop/Job/CITI/DCF DEMO/demo/output/sbs/step2/{testnum}.json'
    prompt = f"""
Assume you are making financial projections for **{company}** using discounted cash flow (DCF) analysis as of **{valuation_date}**.

The following is the historical financial data in JSON format:

{json.dumps(historical_data, indent=2)}

Generate a **5-year projection** for the following metrics (as percentages):
1. Revenue growth (percentage list): The percentage growth of the company''s revenue
  each year.

2. EBIT margin (percentage list): EBIT as a percentage of revenue each year.

3. Effective income tax rate (percentage list): Effective Income Tax Rate of the
  company each year.

4. Depreciation & amortization percentage (percentage list): Depreciation & amortization
  as a percentage of revenue each year.

5. CapEx percentage (percentage list): Capital expenditure as a percentage of revenue
  each year.

6. Change in net working capital percentage (percentage list): Change in net working
  capital as a percentage of revenue each year.

For each scenario (optimistic, base, pessimistic), provide:
- The **value** of each metric
- A **reasoning** for each value that explains the assumptions and factors driving that specific projected metric.
- An overall **scenario_reasoning**

Return only valid JSON in this structure:
{{
  "optimistic": {{
    "revenue_growth": {{"value": 12.5, "reasoning": "..." }},
    ...
    "scenario_reasoning": "..."
  }},
  "base": {{ ... }},
  "pessimistic": {{ ... }}
}}
"""

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000
    )
    content = response.choices[0].message.content

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content
