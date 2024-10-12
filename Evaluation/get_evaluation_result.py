import os
import json
import fire
from call_api import calculate_rouge_l
from collections import defaultdict
import numpy as np

def judge_detail(jsonline):
    a = jsonline['a']
    r = jsonline['r']
    lang = jsonline['info']['type']
    task = jsonline['info']['task']
    depth = jsonline['info']['depth']
    width = jsonline['info']['width']
    llm_model = jsonline['info']["llm_engine"]
    rule_hint = jsonline['info']["rule_hint"]
    few_shot_num = jsonline['info']['few_shot_num']

    rouge_l = calculate_rouge_l(a, r)

    return rouge_l, lang, task, depth, width, few_shot_num, rule_hint, llm_model


def judge(result_dir='../result', tofile='../overall_performance.json'):
    overall_dict = {}
    for file in os.listdir(result_dir):

        baseline = file.split('.')[-2]
        if baseline not in ['cot', 'ps']: 
            baseline = 'naive'

        lang_result = defaultdict(list)
        task_result = defaultdict(list)
        depth_result = defaultdict(list)
        width_result = defaultdict(list)
        rule_result = defaultdict(list)
        few_shot_result = defaultdict(list)


        rule_lang_result = defaultdict(list)
        rule_task_result = defaultdict(list)
        rule_depth_result = defaultdict(list)
        rule_width_result = defaultdict(list)
        rule_rule_result = defaultdict(list)
        rule_few_shot_result = defaultdict(list)

        overall = []
        rule_overall = []

        index_dict = {}

        f = open(os.path.join(result_dir, file), encoding='utf-8')
        for line in f:
            try:
                jsonline = json.loads(line)
                index = jsonline['index']
                result, lang, task, depth, width, few_shot_num, rule_hint, llm_model = judge_detail(jsonline)

                if index not in index_dict:
                    index_dict[index] = [0, lang, task, depth, width, few_shot_num, rule_hint]
                if jsonline['r'] == '<JUMP>':
                    continue
                
                if result < 0.75:
                    result = 0

                index_dict[index] = [result, lang, task, depth, width, few_shot_num, rule_hint]
            except:
                continue

        for index, item in index_dict.items():
            try:
                result, lang, task, depth, width, few_shot_num, rule_hint = item
                if not rule_hint:
                    few_shot_result[few_shot_num].append(result)
                    lang_result[lang].append(result)
                    task_result[task].append(result)
                    depth_result[depth].append(result)
                    width_result[width].append(result)
                    overall.append(result)
                else:
                    rule_few_shot_result[few_shot_num].append(result)
                    rule_lang_result[lang].append(result)
                    rule_task_result[task].append(result)
                    rule_depth_result[depth].append(result)
                    rule_width_result[width].append(result)
                    rule_overall.append(result)
            except:
                continue

        print(file,'Detected %d Samples'%len(overall))
        

        if len(overall) == 0: continue

        lang_result_dict = {}
        for lang in lang_result:
            lang_result_dict[lang] = {'mean': np.mean(lang_result[lang]), 'std': np.std(lang_result[lang])}
        
        task_result_dict = {}
        for task in task_result:
            task_result_dict[task] = {'mean': np.mean(task_result[task]), 'std': np.std(task_result[task])}
        
        depth_result_dict = {}
        for depth in depth_result:
            depth_result_dict[depth] = {'mean': np.mean(depth_result[depth]), 'std': np.std(depth_result[depth])}
        
        width_result_dict = {}
        for width in width_result:
            width_result_dict[width] = {'mean': np.mean(width_result[width]), 'std': np.std(width_result[width])}

        few_shot_result_dict = {}
        for few_shot in few_shot_result:
            few_shot_result_dict[few_shot] = {'mean': np.mean(few_shot_result[few_shot]), 'std': np.std(few_shot_result[few_shot])}


        rule_lang_result_dict = {}
        for lang in lang_result:
            rule_lang_result_dict[lang] = {'mean': np.mean(rule_lang_result[lang]), 'std': np.std(rule_lang_result[lang])}
        
        rule_task_result_dict = {}
        for task in task_result:
            rule_task_result_dict[task] = {'mean': np.mean(rule_task_result[task]), 'std': np.std(rule_task_result[task])}
        
        rule_depth_result_dict = {}
        for depth in depth_result:
            rule_depth_result_dict[depth] = {'mean': np.mean(rule_depth_result[depth]), 'std': np.std(rule_depth_result[depth])}
        
        rule_width_result_dict = {}
        for width in width_result:
            rule_width_result_dict[width] = {'mean': np.mean(rule_width_result[width]), 'std': np.std(rule_width_result[width])}

        rule_few_shot_result_dict = {}
        for few_shot in few_shot_result:
            rule_few_shot_result_dict[few_shot] = {'mean': np.mean(rule_few_shot_result[few_shot]), 'std': np.std(rule_few_shot_result[few_shot])}


        overall = {'mean': np.mean(overall), 'std': np.std(overall)}
        rule_overall = {'mean': np.mean(rule_overall), 'std': np.std(rule_overall)}

        rule_dict = {'Language': rule_lang_result_dict,
                    'Task': rule_task_result_dict,
                    'FewShotNum': rule_few_shot_result_dict,
                    'Depth': rule_depth_result_dict,
                    'Width': rule_width_result_dict,
                    'Overall': rule_overall
                    }

        overall_dict[llm_model+'-'+baseline]={'Language': lang_result_dict,
                                'Task': task_result_dict,
                                'FewShotNum': few_shot_result_dict,
                                'Depth': depth_result_dict,
                                'Width': width_result_dict,
                                'RuleHint': rule_dict,
                                'Overall': overall
                            }
                            
    open(tofile, 'w', encoding='utf-8').write(json.dumps(overall_dict, ensure_ascii=False, indent=4))

    print('--'*20)
    for model in sorted(overall_dict):
        print(model, '%.4f'%overall_dict[model]['FewShotNum'][0]['mean'])

    # return overall_dict


if __name__ == '__main__':
    fire.Fire(judge)

