from datetime import datetime
import os
import glob
import fire

import MYCSV, MYmarkdown, MYtree, MYxml, MYjson, MYyaml, MYlatex, json, MYorg

type_set = [MYCSV.CSV, MYjson.JSON, MYxml.XML, MYtree.Tree, MYyaml.YAML, MYmarkdown.Markdown, MYlatex.LaTeX, MYorg.ORG]
type_name = ['csv','json','xml','tree','yaml','markdown','latex','org']

def open_wrapper(file_path, mode='r', *args, **kwargs):
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    return open(file_path, mode, *args, **kwargs)
def write_data_for_sample(sample, few_shot,node, n_ary_ratio, para_len_ratio, few_shot_num, typename,output_dir='.'): # few_shot is just list of other samples
    '''
    sample:
    typename:
    level: "simple" or "hard", just used to create dir
    i:
    few_shot: Number of few shot demonstration
    with_rule_hint: bool
    '''
    with_rule_hint = True
    for idx,((q, a, input_thin), label_list) in enumerate(zip(sample['QA_to_save'], sample['labels'])):
        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S.%f")
        to_dump = {'Question': q.strip(),
                   'Answer': a.strip(),
                   'Label': {'typename':typename,
                             'node_number':node,
                             'n_ary_ratio':n_ary_ratio,
                             'para_len_ratio':para_len_ratio,
                             'few_shot_num':few_shot_num,
                             'with_rule_hint': with_rule_hint,
                             'other_label_list':label_list
                             },
                   'Reference': input_thin,
                   'timestamp': timestamp,
                   'input_hash': hash(input_thin)}

        if few_shot: # if len(few_shot) > 0, add examples to data
            key_dict = ['Question', 'Answer', 'Reference']
            def build_sub_dict(q_a_input):
                return {key_dict[i]: v for i, v in enumerate(q_a_input)}
            to_dump['examples'] = [build_sub_dict(eg['QA_to_save'][idx]) for eg in few_shot]
        if with_rule_hint:
            from rule_hint import fetch_rule_hint
            to_dump['RuleHint'] = fetch_rule_hint(typename, idx)

        # q1 and q3 could have exact same labels,
        # thus resulting in same file name, using Q hash to name file instead
        filename = f'{abs(hash(q)) % 42}.{timestamp}'
        label_as_directory = '_'.join(label_list)

        root_name = f'{len(few_shot)}Shotbenchmark'
        write_dir = f'{output_dir}/{root_name}/{typename}/{label_as_directory}'
        if not os.path.exists(write_dir):
            os.makedirs(write_dir)
        write_path = f'{write_dir}/{filename}_{idx}.json'
        if not os.path.exists(write_path):
            open(write_path,'w',encoding='utf-8')
        with open_wrapper(write_path, 'a+', encoding="utf-8") as f:
            # print(f'i={i}, path={write_path}')
            json.dump(to_dump, f, indent=4, ensure_ascii=False)


def procedure_gen(generate_setting='../generate_setting.json'):
    '''
    few_shot: Number of few shot demonstration
    num: Number of questions generated for each level and task
    with_rule_hint: generated rule hint
    '''

    jsondata = json.load(open(generate_setting,encoding='utf-8'))

    general_setting = jsondata['#']
    output_dir = general_setting['output_dir']

    few_shots = general_setting['few_shots']

    for few_shot in few_shots:
        for Type,typename in zip(type_set,type_name):
            typesetting = jsondata[typename]
            nodes = typesetting['nodes']
            n_ary_ratios = typesetting['n_ary_ratios']
            para_len_ratios = typesetting['para_len_ratios']
            # nodes, n_ary_ratio, para_len_ratio = typesetting['nodes'], typesetting['n_ary_ratio'], typesetting['para_len_ratio']
            for node in nodes:
                for n_ary_ratio in n_ary_ratios:
                    for para_len_ratio in para_len_ratios:
                        sample = Type.gen_QAs(node = node,n_ary_ratio=n_ary_ratio,para_len_ratio=para_len_ratio)
                        shot_example = list(Type.gen_QAs(node = node,n_ary_ratio=n_ary_ratio,para_len_ratio=para_len_ratio) for _ in range(few_shot))
                        write_data_for_sample(sample,
                                            shot_example,
                                            node, n_ary_ratio, para_len_ratio, few_shot, typename,
                                            output_dir=output_dir)


if __name__ == '__main__':
    fire.Fire(procedure_gen)
    # procedure_gen(few_shot=0, num=4)
