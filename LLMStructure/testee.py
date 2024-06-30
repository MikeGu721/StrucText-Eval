'''
In this file we collect a variable of APIs that are publicly available
'''
import time
from time import sleep



def spark_fn_api(prompt, _, credentials=None):
    from SparkAPI import SparkApi, \
        test  # https://www.xfyun.cn/doc/spark/Web.html, need download their example code to import

    test.text.clear()
    if credentials is None:
        credentials = {'appid': test.appid, 'api_key': test.api_key, 'api_secret': test.api_secret}
    question = test.checklen(test.getText("user", prompt))
    SparkApi.main(credentials['appid'], credentials['api_key'], credentials['api_secret'], test.Spark_url, test.domain, question)
    return SparkApi.answer

class API:
    timeout = 45
    max_try = 2
    min_intv = 10

    def __init__(self, credentials, fn_api, ident):
        self.credentials = credentials
        self.ident = ident

        # Input: (prompt: str[, system: str]), where the prompt is the query to be completed and the system is the settings of AI in NL
        # Output: response: str, the pure string extracted from the response of API request
        self.fn_api = fn_api

    def query(self, messages=("To live or die, this is a", "You are Shakespear now")):
        # Here we generally retry to overcome simple network exception.
        response, fail_cnt = None, 0
        while fail_cnt < self.max_try:
            sleep(fail_cnt * self.timeout)
            try:
                response = self.fn_api(*messages, credentials=self.credentials)
                if response == "E2ROR: minimax output sensitive": break
                if response == "336000Internal error":
                    print("ernie, internal error")
                    break
                if not response:
                    print("empty response")
                    raise Exception("empty response")
                sleep(self.min_intv)
                break
            except Exception as e:
                fail_cnt += 1
                print("Expection happend on query: ",e)
                if 'backup_keys' in self.credentials and 'api_key' in self.credentials:
                    next_cur = (self.credentials['cur'] + 1) % len(self.credentials['backup_keys'])
                    self.credentials['api_key'] = self.credentials['backup_keys'][next_cur]
                    print(
                        f"For {self.ident}:chaaaaaaanging from {self.credentials['cur']}th key to {next_cur}th key, amongst {len(self.credentials['backup_keys'])} keys")
                    self.credentials['cur'] = next_cur
        if not response:
            print('in testee query method, empty response: panickkkkkk!')
        return response


def minimax(prompt, system, credentials):
# https://platform.minimaxi.com/document/guides/chat-model/pro/api?id=6569c85948bc7b684b30377e
    raise NotImplementedError


def gpt3(prompt, _, credentials):
    import openai
    openai.api_type = "open_ai"
    openai.api_version = None
    openai.api_base = "https://api.openai.com/v1"
    openai.api_key = credentials['api_key']
    response = openai.Completion.create(
        model="davinci",
        prompt=prompt
    )
    return response.choices[0].text


# GPT-4
def gpt4(prompt, _, credentials):
    gpt4_turbo_url = 'https://runway.devops.xiaohongshu.com/openai/chat/completions?api-version=2023-05-15'
    gpt_param = {"max_tokens": 500,
                 "temperature": 0.8, "top_p": 1, "stream": False,
                 "frequency_penalty": 0.1, "presence_penalty": 0.1, "stop": None}
    result = GPT_request_by_url(prompt,gpt_param,gpt4_turbo_url,credentials['api_key'])
    # print(result)
    return result['choices'][0]['message']['content']


def GPT_request_by_url(message_or_prompt, gpt_params, url, key):
    import  json, requests
    if isinstance(message_or_prompt, str):
        messages = [{"role": "user", "content": message_or_prompt}]
    else:
        messages = message_or_prompt
    headers = {
        'api-key': key,
        'Content-Type': 'application/json'
    }
    payload = {
        "messages": messages,
    }
    if gpt_params is not None:
        payload.update(gpt_params)
    payload_json = json.dumps(payload)
    response_raw = requests.request("POST", url, headers=headers, data=payload_json)
    response_json = response_raw.json()
    if 'finish_reason' in response_json['choices'][0]:
        if response_json['choices'][0]['finish_reason'] == 'content_filter':
            print("content filter detected: generation finished due to 'content_filter'.")
        else:
            print("finished due to ", response_json['choices'][0]['finish_reason'])
    return response_json



def api_ErnieBot_turbo(prompt, _, credentials):
    # https://cloud.baidu.com/doc/WENXINWORKSHOP/s/4lilb2lpf#请求示例（单轮）
    raise NotImplementedError


minimax_api = API({"group_id": "<SECRET>", "api_key": "<SECRET>"}, minimax, "minimax")
gpt4_api = API({"api_key": "<SECRET>"}, gpt4, "gpt4xhs")
gpt4_base_api = API({"api_key": "<SECRET>"}, gpt4, "gpt4xhs_base_non_turbo")
spark_api = API(None, spark_fn_api, 'spark')
baidu_api = API({'API_KEY': "<SECRET>", 'SECRET_KEY': "<SECRET>"}, api_ErnieBot_turbo, "baidu_erniebot_turbo")

def test_minimax():
    print("MINIMAX:", minimax_api.query(),"&&THE END")

def test_gpt4xhs():
    print("GPT4XHS:", gpt4_api.query(),"&&THE END")
    print("GPT4_BASE_XHS:", gpt4_base_api.query(),"&&THE END")

def test_spark():
    print("SPARK:", spark_api.query(),"&&THE END")


def test_baidu():
    print("BAiDU:", baidu_api.query(),"&&THE END")
if __name__ == "__main__":
    # test_minimax()
    # test_gpt4xhs()
    # test_spark()
    test_baidu()
