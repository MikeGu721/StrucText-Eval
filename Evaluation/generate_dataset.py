
import os
import json
from collections import defaultdict
import tqdm
import fire


def parse_jsonfile(jsonfile):
    jsondata = json.load(open(jsonfile, encoding='utf-8'))

    question = jsondata['Question']
    reference = jsondata["Reference"]
    answer = jsondata['Answer']
    rule_hint = jsondata["RuleHint"]

    few_shot_num = jsondata['Label']['few_shot_num']

    if few_shot_num != 0:
        examples = jsondata['examples']
    else:
        examples = []

    type_name = jsondata["Label"]['typename']
    task = jsondata["Label"]['other_label_list'][0]

    depth = jsondata["Label"]['node_number']
    width = jsondata["Label"]['n_ary_ratio']

    info = {'type': type_name,
            'task': task,
            'depth': depth,
            'width': width,
            'few_shot_num': few_shot_num}

    return question, reference, answer, rule_hint, examples, info

def get_data(language, question, reference, answer, examples=[], rule_hint=None):
    prompt = 'There are References in %s. Based on the content under “### Question:”, please provide the answer directly after “### Answer:”. Avoid including any redundant information in your answer.\n\n'%language
    if rule_hint:
        prompt += '### Hint:\n'+ rule_hint +'\n\n'

    examples_prompt = ''
    if examples:
        examples_prompt = '### Examples:\n\n'
        for ex in examples:
            ex_question = ex['Question']
            ex_answer = ex['Answer']
            ex_reference = ex['Reference']

            examples_prompt += '### Question:\n' + ex_question + '\n\n### Reference:\n'+ ex_reference + '\n\n### Answer:\n' + ex_answer + '\n\n' 
    
    prompt += examples_prompt
    prompt +=  '### Question:\n' + question + '\n\n### Reference:\n'+ reference + '\n\n### Answer:\n'
    return prompt, answer


def generate_dataset(benchmark_dir, save_dataset_file='evaluate_dataset.jsonl'):
    dirs = [benchmark_dir]
    json_files = []
    index = 0

    while(index < len(dirs)):
        dirr = dirs[index]
        index += 1

        for dir_file in os.listdir(dirr):
            dir_file = os.path.join(dirr, dir_file)
            if os.path.isdir(dir_file):
                dirs.append(dir_file)
            elif dir_file.endswith('.json'):
                json_files.append(dir_file)
    print('Data Count:',len(json_files))
    
    fw = open(save_dataset_file, 'w', encoding='utf-8')

    for jsonfile in tqdm.tqdm(json_files):
        question, reference, answer, rule_hint, examples, info = parse_jsonfile(jsonfile)
        prompt, answer = get_data(info['type'], question, reference, answer, examples)
        rule_hint_prompt, _ = get_data(info['type'], question, reference, answer, examples, rule_hint)
        
        info['rule_hint'] = False
        jsonline = {'q':prompt,
                    'a': answer,
                    'info': info}
        fw.write(json.dumps(jsonline, ensure_ascii=False)+'\n')

        info['rule_hint'] = True
        jsonline = {'q':rule_hint_prompt,
                    'a': answer,
                    'info': info}
        fw.write(json.dumps(jsonline, ensure_ascii=False)+'\n')
        
    fw.close()


if __name__ == '__main__':
    fire.Fire(generate_dataset)
