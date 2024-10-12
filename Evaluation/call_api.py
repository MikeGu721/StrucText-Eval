
import json
import time
from openai import OpenAI
import os
import tqdm
from rouge import Rouge
from zhipuai import ZhipuAI
rouge = Rouge()

gpt_api_key = ''
gpt_api_url = ''
glm_api_key = ''
authorization = ''


class APILLM:
    def __init__(self):
        pass

def calculate_rouge_l(reference, hypothesis):
    scores = rouge.get_scores(reference, hypothesis)
    return scores[0]['rouge-l']['f']

def call_glm_api(prompt, engine='glm-4-flash'):
    client = ZhipuAI(api_key=glm_api_key)  # 请填写您自己的APIKey
    completion = client.chat.completions.create(
        model=engine,  # 请填写您要调用的模型名称
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    
    return completion.dict()


def call_gpt_api(prompt, engine='gpt-4o-mini'):
    
    client = OpenAI(
        base_url=gpt_api_url,
        api_key=gpt_api_key
    )

    completion = client.chat.completions.create(
    model=engine,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    return completion.dict()

def call_model_api(prompt, engine = "TA/Qwen/Qwen2-72B-Instruct"):
    import http.client
    conn = http.client.HTTPSConnection("cn2us02.opapi.win")
    headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json',
    "Authorization": authorization
    }
    payload = json.dumps({
    "model": engine,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False
    })
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

if __name__ == '__main__':

