#/usr/ben/env python3
from itertools import accumulate
def fetch_rule_hint(category, ith_task):
    """
    categary: Tabular,Tree,Json,Yaml,XML,Markdown,LaTeX,Org
    ith_task: [0,4], noteice # of tasks for each category is 4,3,5,5,3,3,3,3
    """
    with open('RuleHint.txt', 'r') as f:
        lines = list(line.strip() for line in f.readlines())
        rid = {v.lower():i for i,v in enumerate(lines[0].split(","))}
        seg_counts = [int(num) for num in lines[1].split(",")]
        assert 0<= ith_task < seg_counts[rid[category]]
        presum = [0] + list(accumulate(seg_counts))
        return lines[2 + presum[rid[category]] + ith_task].strip()

# def transform(data):
#     data = data.copy()
#     INPUT = f"Question: \n{data['Question']}\nAnswer: \n{data['Answer']}\nFile: \n{data['Reference']}\n"
#     OUTPUT = data['rule_hint']
#     INSTRUCTION = "Given as input is a QA pertaining to a file with special format and syntax, please explain how to get the answer from the file: \n"
#     data['Question'] = data['Question']
#     data['Answer'] = OUTPUT
#     data['input'] = INPUT
#     return data

if __name__ == "__main__":
    print(fetch_rule_hint('Tree', 0))
    print(fetch_rule_hint('Tree', 1))
    print(fetch_rule_hint('Tree', 2))
