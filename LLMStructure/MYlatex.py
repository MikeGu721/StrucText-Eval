#!/usr/bin/env python3
import random

from structure import Structure
from name import Name
from random import randint, choice
from MYtree import Tree

exts = ['jpg', 'jpeg', 'png', 'gif']
prefixes = ['sub'*(i-1) + 'section' for i in range(20)]


def add_bold_style(bold_text: str):
    pref = '\\textbf{'
    suff = '}'
    return f'{pref}{bold_text}{suff}'


def with_ext(name):
    return f'{name}.{exts[(abs(hash(name)) % 42) % len(exts)]}'


def add_image_mark(image_file_name_no_ext: str):
    pref = '\\includegraphics[width=0.5\\textwidth]{'
    suff = '}'
    return f'{pref}{with_ext(image_file_name_no_ext)}{suff}'



def compse_text_seg(node):
    # content, mixed with bold text and images
    text_inserts = []
    if node.bold_text is not None:
        bold_text, pos = node.bold_text
        bold_text = add_bold_style(bold_text)
        text_inserts.append((bold_text, pos))
    if node.img is not None:
        img_path, pos = node.img
        img_path = add_image_mark(img_path)
        text_inserts.append((img_path, pos))
    text_segmants, prev_cut = [], 0
    for t, p in text_inserts:
        text_segmants.append(node.text[prev_cut:p])
        text_segmants.append(t)
        prev_cut = p
    text_segmants.append(node.text[prev_cut:])
    return text_segmants


class LaTeX:

    @staticmethod
    def path_to_node_by_id(root, id):
        def dfs(node, id):
            if node.id == id:
                return []
            for i, c in enumerate(node.children, 1):
                sub_res = dfs(c, id)
                if sub_res is not None:
                    sub_res.append(i)
                    return sub_res
            return None

        return list(reversed(dfs(root, id)))

    @staticmethod
    def dump(root):
        buffer = []

        def dfs(node):
            # heading/id
            command = (['']+prefixes)[node.depth]
            lbrace, rbrace = '{', '}'
            buffer.append(f'\\{command}{lbrace}{node.id}{rbrace}' if command else node.id)

            buffer.append(''.join(compse_text_seg(node)))

        root.dfs(dfs)
        return '\n'.join(buffer)

    @staticmethod
    def random(depth, n_ary, para_len):
        root, name, keeper = Structure.random(depth, n_ary)
        content_vocab = ["apple", "banana", "cafe", "dentist", "essence", "far", "groot", "halo", "idiot", "jargon",
                         "kangaroo", "lamb",
                         "monkey", "nob", "oops", "perish", "qualify", "ravish", "salvage", "transformer", "unique",
                         "vigor", "wake", "X-ray", "yogurt", "zen"]
        val_name = Name(init=randint(1700, 26 ** (para_len)), vocab=content_vocab, delimiter=' ')
        img_paths = Name(randint(100, 250))
        bold_texts = Name(init=randint(0, 25), vocab=content_vocab, delimiter=' ')

        def assign_id_text(node: Structure):
            node.properties['id'] = node.content
            node.properties['text'] = val_name.poll()
            node.properties['bold_text'] = (
                bold_texts.poll(), randint(0, len(node.properties['text']) - 1)) if random.random() > 0.5 else None
            node.properties['img'] = (
                img_paths.poll(), randint(0, len(node.properties['text']) - 1)) if random.random() < 0.5 else None

        root.dfs(assign_id_text)
        Tree.assign_depth(root)
        return root, (name, val_name, bold_texts, img_paths), keeper


    """
    Extract all bold text.
    What is the 2nd subsection under section 6.
    Extract all included image files.
    ...(content of markdown)
    """
    @staticmethod
    def gen_QAs(node,n_ary_ratio, para_len_ratio):
        depth = node
        n_ary = int(node * n_ary_ratio)
        para_len = int(node * para_len_ratio)
        # depth, n_ary, para_len = (2, 1, 8)
        # print(depth, n_ary, para_len)
        root, (ids, contents, bold_texts, img_paths), keeper = LaTeX.random(depth, n_ary, para_len)

        system = 'You are a LaTeX file parser, you have to answer questions regarding this LaTeX file.'

        LaTeX_file = LaTeX.dump(root)
        here_is_input = f"Here is the content of the LaTeX file:\n{LaTeX_file}"
        # bold texts retrieval
        q1_thin = (f"Extract all bold texts. "
                   "Print those raw texts separated by \\n. ")
        q1 = q1_thin+here_is_input
        a1 = '\n'.join(bold_texts.hist) if bold_texts.hist else "No bold texts presented in file."

        # find content by path
        id_in_question = choice(list(ids.hist))
        while id_in_question == root.id:  # section is at depth 1
            id_in_question = choice(list(ids.hist))
        path_to_id = LaTeX.path_to_node_by_id(root, id_in_question)
        prefixes = ['section', 'subsection', 'subsubsection'][:len(path_to_id)]
        path_as_text = ' under '.join(reversed([f'{no}th {heading}' for no, heading in zip(path_to_id, prefixes)]))
        a2 = LaTeX.dump(keeper[id_in_question])
        q2_thin = (f"What is the content of {path_as_text}? "
                   "The content should be an excerpt as it "
                   "appears in the LaTeX file, including the heading line and any sub-section. ")
        q2 = q2_thin+here_is_input

        # image retrieval
        q3_thin = (f"Extract all included figure files. "
                   "Print those file names separated by \\n. ")
        q3 = q3_thin+here_is_input
        a3 = '\n'.join([with_ext(iname) for iname in
                        img_paths.hist]) if img_paths.hist else "No figure file is included in the file."

        return {'system': system, 'QA': [(q1, a1), (q2, a2), (q3, a3)],
                'labels': [['TextRetrieval'], ['PathWalk'], ['TextRetrieval']],
                'QA_to_save': [(q1_thin, a1, LaTeX_file), (q2_thin, a2, LaTeX_file),
                               (q3_thin, a3, LaTeX_file)],
                }


if __name__ == '__main__':
    d = LaTeX.gen_QAs(False)
    i = 0
    txt = d['QA_to_save'][0][2]
    for q, a, _ in d['QA_to_save']:
        i += 1
        print(f'{"*" * 5}{i}{"*" * 5}')
        print('+' * 10)
        print(q)
        print('-' * 10)
        print(a)
    print(txt)

