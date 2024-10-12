#!/usr/bin/env python3
from structure import Structure
from name import Name
from random import randint, choice
from random import random as rand
from MYtree import Tree


class XML:
    @staticmethod
    def find_tag_by_name(keeper, tag_name):
        for v in keeper.values():
            if v.tag_name == tag_name:
                return v
        return None

    @staticmethod
    def find_tag_by_attr(keeper, tgt_val):
        for v in keeper.values():
            for val in v.attributes.values():
                if val == tgt_val:
                    return v
        return None

    @staticmethod
    def dump_content(root):
        buffer = XML.dump(root, error=False, output_str=False)
        return '\n'.join(buffer[2:-1])

    @staticmethod
    def dump(root, error=False, output_str=True):
        Tree.assign_depth(root)
        buffer = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>"]
        if error:
            has_error = False

        def dfs_dump(node):
            nonlocal error
            nonlocal has_error
            # tag begin
            indent_prefix = ' ' * node.depth
            attr_list = [f"{attr}=\"{val}\"" for attr, val in node.attributes.items()]
            buffer.append(f"{indent_prefix}<{node.tag_name}{' ' if attr_list else ''}{' '.join(attr_list)}>")

            # child tags
            for c in node.children:
                dfs_dump(c)

            # cur content
            buffer.append(f'{indent_prefix} {node.content}')

            # end tag, if error, 0.8 prob missing end tag
            if not error or rand() > 0.8:
                buffer.append(f"{indent_prefix}</{node.tag_name}>")
            else:
                has_error = True

        dfs_dump(root)
        xml_file = '\n'.join(buffer) if output_str else buffer
        if error:
            return xml_file, has_error
        else:
            return xml_file

    @staticmethod
    def random(depth, n_ary, attr_cnt):
        content_vocab = ["apple", "banana", "cafe", "dentist", "essence", "far", "groot", "halo", "idiot", "jargon",
                         "kangaroo", "lamb", "monkey", "nob", "oops", "perish", "qualify", "ravish", "salvage", "transformer", "unique",
                         "vigor", "wake", "X-ray", "yogurt", "zen", "ant", "bliss", "coral", "dusk", "eagle", "frost", "glare", "horizon",
                         "index", "jewel", "knight", "lunar", "mystic", "nebula", "oasis", "pivot", "quartz", "ripple", "silk", "twilight", 
                         "uplift", "vortex", "whisper", "xenon", "yarn", "zephyr", "arch", "blaze", "crimson", "dawn", "echo", "flame", 
                         "gale", "harbor", "insight", "journey", "keystone", "lyric", "mirage", "nomad", "orbit", "pulse", "quiver", 
                         "riddle", "serene", "thunder", "utopia", "vivid", "whale", "xylem", "yearn", "zenith"]
        root, name, keeper = Structure.random(
            depth, n_ary, content_name=Name(0, vocab=content_vocab, delimiter=' '))
        tag_vocab = {i: chr(ord('A') + i) for i in range(26)}
        attr_vocab = {i: chr(ord('Z') - i) for i in range(26)}
        val_vocab = {i: chr(ord('z') - i) for i in range(26)}

        import random
        tag_name, attr_name, val_name = Name(0, tag_vocab), Name(0, attr_vocab), Name(init=random.randint(0,25), vocab=val_vocab)

        def assign_tag_attr(node: Structure):
            node.properties['tag_name'] = tag_name.poll()
            node.properties['attributes'] = {
                attr_name.poll(): val_name.poll() for _ in range(randint(1, attr_cnt))}

        root.dfs(assign_tag_attr)
        return root, (name, tag_name, attr_name, val_name), keeper


    """
    What is the content(s) of tag author?
    What are the tags with attribute version of value "1"?
    Is there any structural error in this XML? If so, give the answer 'True' and
    spot them out. If it is free from error, just give the answer 'False'.
    ...(content of XML)
    """
    @staticmethod
    def gen_QAs(node, n_ary_ratio, para_len_ratio):
        depth = node
        n_ary = int(node * n_ary_ratio)
        attr_max = int(node * para_len_ratio)
        root, (content_name, tag_name, attr_name,
               val_name), keeper = XML.random(depth, n_ary, attr_max)

        system = 'You are an XML parser now. You have to answer my questions regarding this XML file.'
        content_for = choice(list(tag_name.hist))
        try:
            attr_for = choice(list(val_name.hist))
        except:
            print('ERROR')
            print(val_name.hist)
            import sys
            sys.exit()

        xml_file = XML.dump(root)
        here_is_input = f"Here is the content of the XML file:\n{xml_file}"
        # content
        q1_thin = (f"What is the content of tag {content_for}? "
                   "The content should be an excerpt as it "
                   "appears in the XML file. ")
        q1 = q1_thin+here_is_input
        a1 = XML.dump_content(XML.find_tag_by_name(keeper, content_for))

        # tag by attr
        q2_thin = f"What is the tag with attribute of value {attr_for}?"
        q2 = q2_thin+here_is_input
        a2 = XML.find_tag_by_attr(keeper, attr_for).tag_name

        # syntax
        xml_file_maybe_error, has_error = XML.dump(root, error=True)
        a3 = str(has_error)
        q3_thin = ("Is there any structural error in this XML? If so, give the answer "
                   "'True' and spot them out. If it is free from error, just give the answer "
                   "'False'.")
        q3 = (q3_thin, f"Here is the content of the XML file:\n{xml_file_maybe_error}")
        return {'system': system, 'QA': [(q1, a1), (q2, a2), (q3, a3)],
                'labels': [['TextRetrieval'], ['TextRetrieval'], ['Syntax']],
                'QA_to_save': [(q1_thin, a1, xml_file), (q2_thin, a2, xml_file), (q3_thin, a3, xml_file_maybe_error)],
                }
