from call_api import call_model_api, call_gpt_api, call_glm_api
import tqdm
import sys
import fire
import json
import time
import os

def write_new_data(data, file):
    if not os.path.exists(file):
        open(file, 'w', encoding='utf-8')
    open(file, 'a', encoding='utf-8').write(str(data)+'\n')

def get_llm_response(prompt, llm_engine):
    call_model = call_model_api
    if 'gpt' in llm_engine:
        call_model = call_gpt_api
    if 'o1' in llm_engine:
        call_model = call_gpt_api
    if 'glm' in llm_engine:
        call_model = call_glm_api
    response_dict = call_model(prompt, llm_engine)  # response: json
    write_new_data(response_dict, 'response_from_model_api.jsonl')
    content = response_dict["choices"][0]["message"]["content"]
    return content

def evaluate(dataset_file, llm_engine, save_file, save_dir):
    if not os.path.exists(save_file):
        open(save_file, 'w', encoding='utf-8')
    stop_num = 6
    has_index = [json.loads(line)['index'] for line in open(save_file, encoding='utf-8').readlines() if (json.loads(line)['info']['llm_engine']==llm_engine and json.loads(line)['r']!='<JUMP>')]
    print('LLM Engine:', llm_engine)
    print('Has results:', len(has_index))

    f = open(dataset_file, encoding='utf-8')

    jump_continue = 0
    for index, line in tqdm.tqdm(enumerate(f)):
        if index in has_index: continue
        jsonline = json.loads(line)
        q = jsonline['q']
        a = jsonline['a']
        info = jsonline['info']

        try:
            r = get_llm_response(q, llm_engine)
            jump_continue = 0
        except:
            r = '<JUMP>'
            jump_continue += 1
        if jump_continue == stop_num: 
            sys.exit()
        info['llm_engine'] = llm_engine
        result_dict = {'index':index,
                        'q':q,
                        'a':a,
                        'r': r,
                        'info': info}
        write_new_data(json.dumps(result_dict), save_file)
        time.sleep(0.1)

if __name__ == '__main__':
    fire.Fire(evaluate)

