import json
import os
from openai import OpenAI

def run_sbs_step3(openai_api_key,  discount_rate, terminal_growth_rate, testnum, user_prompt):
    input_json_path=f'/Users/buzider/Desktop/Job/CITI/DCF DEMO/demo/output/sbs/step2/{testnum}.json'
    output_path=f'/Users/buzider/Desktop/Job/CITI/DCF DEMO/demo/output/sbs/step3/{testnum}.json'
    try:
        with open(input_json_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"❌ 無法讀取 JSON 檔案：{e}")

    scenario_data_str = json.dumps(data, indent=2)
    prompt = f"""
    
{user_prompt}

For each scenario (optimistic, base, pessimistic), use the following projected financial assumptions:

{scenario_data_str}

Assume the following DCF parameters:
- Projection horizon: 5 years
- Discount rate: {discount_rate}%
- Terminal growth rate: {terminal_growth_rate}%

Please return your answer in the following JSON format:
{{
  "optimistic": {{ "implied_stock_price": <number>, "reasoning": "<text>" }},
  "base": {{ "implied_stock_price": <number>, "reasoning": "<text>" }},
  "pessimistic": {{ "implied_stock_price": <number>, "reasoning": "<text>" }}
}}

Return **ONLY** the JSON.
"""

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1200
    )
    content = response.choices[0].message.content

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content
