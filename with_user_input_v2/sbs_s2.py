import json
import os
from openai import OpenAI

def run_sbs_step2(openai_api_key, company, valuation_date, historical_data, testnum, user_prompt):
    output_path=f'/Users/buzider/Desktop/Job/CITI/DCF DEMO/demo/output/sbs/step2/{testnum}.json'
    prompt = f"""

{user_prompt}

The following is the historical financial data in JSON format:

{json.dumps(historical_data, indent=2)}

Return only valid JSON in this structure:
{
  "optimistic": {
    "revenue_growth": { "value": [12.5, 12.0, 11.5, 11.0, 10.5], "reasoning": "..." },
    "ebit_margin": { "value": [...], "reasoning": "..." },
    ...
    "scenario_reasoning": "..."
  },
  "base": {
    ...
  },
  "pessimistic": {
    ...
  }
}
Return **ONLY** the JSON.
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
