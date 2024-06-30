#!/usr/bin/env python3
from structure import Structure
from name import Name
from random import randint, choice
from random import random as rand
from MYtree import Tree


# a yaml object is composed of id, subs, and other attr
class YAML:
    @staticmethod
    def find_obj_by_id(keeper, id):
        for v in keeper.values():
            if v.id == id:
                return v
        return None

    @staticmethod
    def find_obj_by_val(keeper, tgt_val):
        for v in keeper.values():
            for val in v.properties.values():
                if val == tgt_val:
                    return v
        return None

    @staticmethod
    def dump_content(root):
        return YAML.dump(root, error=False, output_str=True)

    @staticmethod
    def dump(root, error=False, output_str=True):
        Tree.assign_depth(root)
        buffer = []
        if error:
            has_error = False
            error_word = Name(init=randint(0,25))

        def dfs_dump(node):
            nonlocal error
            nonlocal has_error
            # tag begin
            indent_prefix = '  ' * node.depth
            if 0 == node.depth:
                buffer.append(f'{indent_prefix}id: "{node.id}"')
            else:
                prefix = '  ' * (node.depth - 1)
                buffer.append(f'{prefix}- id: "{node.id}"')

            # cur content
            for k, v in node.properties.items():
                if k not in ['depth', 'id', 'father']:
                    buffer.append(f'{indent_prefix}{k}: {v},')

            # child tags
            if node.children:
                buffer.append(f'{indent_prefix}subs: ')
                for c in node.children:
                    dfs_dump(c)
            else:
                buffer.append(f'{indent_prefix}subs: []')

            # end tag, if error, 0.8 prob missing end tag
            if not error or rand() > 0.8:
                pass
            else:
                has_error = True
                buffer.append(indent_prefix + ':' + error_word.poll())

        dfs_dump(root)
        yaml_file = '\n'.join(buffer) if output_str else buffer
        if error:
            return yaml_file, has_error
        else:
            return yaml_file

    @staticmethod
    def random(depth, n_ary, attr_cnt):
        root, name, keeper = Structure.random(depth, n_ary)
        attr_vocab = {i: chr(ord('Z') - i) for i in range(26)}
        val_vocab = {i: chr(ord('z') - i) for i in range(26)}

        attr_name, val_name = Name(0, attr_vocab), Name(init=randint(0,25), vocab=val_vocab)

        def assign_id_attr(node: Structure):
            node.properties['id'] = node.content
            for _ in range(randint(1, attr_cnt)):
                node.properties[attr_name.poll()] = val_name.poll()

        root.dfs(assign_id_attr)
        return root, (name, attr_name, val_name), keeper

    @staticmethod
    def find_deepest(root, keeper):
        Tree.assign_depth(root)
        keys = list(keeper.keys())
        keys.sort(key=lambda x: keeper[x].depth, reverse=True)
        res = [keys[0]]
        for k in keys[1:]:
            if keeper[k].depth != keeper[res[0]].depth: break
            res.append(k)
        return [keeper[k] for k in res]


    """
    What is the object with id {id}?
    What is the first element of subs?
    How to access value {val}? Answer should be like obj[key1][key2][key3]...
    ...(content of YAML)
    """
    @staticmethod
    def gen_QAs(node,n_ary_ratio, para_len_ratio):
        depth = node
        n_ary = int(node * n_ary_ratio)
        attr_max = int(node * para_len_ratio)
        root, (content_name, attr_name, val_name), keeper = YAML.random(depth, n_ary, attr_max)

        system = 'You are a YAML file parser, you have to answer my questions regarding this YAML file. ' \
                 'In your answer, double quote is preferred wherever possible'
        id_for = choice(list(content_name.hist))
        val_for = choice(list(val_name.hist))

        yaml_file = YAML.dump(root)
        here_is_input = f"Here is the content of the YAML file:\n{yaml_file}"
        # id
        q1_thin = (f"What is the object with id {id_for}? "
                   "The content should be an excerpt as it "
                   "appears in the YAML file. ")
        q1 = q1_thin+here_is_input
        a1 = YAML.dump_content(YAML.find_obj_by_id(keeper, id_for))

        # first child
        q2_thin = f"What is the first object's id of subs?"
        q2 = q2_thin+here_is_input
        a2 = root.children[0].id

        # syntax
        yaml_file_maybe_error, has_error = YAML.dump(root, error=True)
        a3 = str(has_error)
        q3_thin = ("Is there any structural error in this YAML? If so, give the answer "
                   "'True' and spot them out. If it is free from error, just give the answer "
                   "'False'.")
        q3 = (q3_thin,
              f"Here is the content of the YAML file:\n{yaml_file_maybe_error}")

        # access path
        q4_thin = f'How to access value "{val_for}"? Answer should be like obj[key or index 1][key or index 2][key or index 3]...'
        q4 = q4_thin+here_is_input
        a4 = YAML.find_path_to_val(root, val_for)

        # atom object
        q5_thin = ("What are the most deeply nested objects, i.e., no value of type list or dict?"
                   "The content should be an excerpt as they appear in the YAML file, separated by \\n\\n. ")
        q5 = q5_thin+here_is_input
        leaf_nodes = YAML.find_deepest(root, keeper)
        a5 = "\n\n".join([YAML.dump_content(n) for n in leaf_nodes])

        return {'system': system, 'QA': [(q1, a1), (q2, a2), (q3, a3), (q4, a4), (q5, a5)],
                'labels': [['TextRetrieval'], ['PathWalk'], ['Syntax'], ['PathCompose'], ['TextRetrieval']],
                'QA_to_save': [(q1_thin, a1, yaml_file), (q2_thin, a2, yaml_file), (q3_thin, a3, yaml_file_maybe_error),
                               (q4_thin, a4, yaml_file), (q5_thin, a5, yaml_file)]}

    @staticmethod
    def find_path_to_val(root, val_for):
        buffer = []

        def dfs(node):
            for k, v in node.properties.items():
                if k not in ['depth', 'id', 'father']:
                    if v == val_for:
                        buffer.append(f'["{k}"]')
                        return True

            for i, c in enumerate(node.children):
                if dfs(c):
                    buffer.append(f'[{i}]')
                    buffer.append('["subs"]')
                    return True
            return False

        dfs(root)
        buffer.append('obj')
        buffer.reverse()
        return ''.join(buffer)


if __name__ == '__main__':
    for i in range(20):
        # d = YAML.gen_QAs(simple=True)
        d = YAML.gen_QAs(simple=False)
        for q,a in d['QA']:
            print('+'*20)
            print(q)
            print('-'*20)
            print(a)
