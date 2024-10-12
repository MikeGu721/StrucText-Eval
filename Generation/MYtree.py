#!/usr/bin/env python3
from structure import Structure
from random import choices


class Tree(Structure):
    @staticmethod
    def get_edges(node):
        buffer = []

        def print_edge(node):
            buffer.append(
                f"{node.father.content if node.father else None}->{node.content}")

        node.dfs(print_edge)
        return "\n".join(buffer)

    @staticmethod
    def assign_depth(root):
        def dfs(node, depth):
            node.properties['depth'] = depth
            for c in node.children:
                dfs(c, depth + 1)

        dfs(root, 0)

    @staticmethod
    def random(depth, n_ary):
        root, name, keeper = Structure.random(depth, n_ary)
        Tree.assign_depth(root)
        return root, name, keeper

    @staticmethod
    def get_height(node: Structure):
        if not node.children:
            return 0
        return max([1 + Tree.get_height(c) for c in node.children])

    @staticmethod
    def get_path(root: Structure, target: str):
        def dfs(root, target):
            if root.content == target:
                return [root.content]
            sub_path = []
            for c in root.children:
                sub_path = dfs(c, target)
                if sub_path:
                    sub_path.append(root.content)
                    break
            return sub_path

        return '->'.join(reversed(dfs(root, target)))

    """
    What is the height of node A? Answer an integer, leaf is of height 0.
    What is the depth of node B? Answer an integer, root is of depth 0.
    What is the path from root node to E? Answer should look like A->D->H.
    """

    @staticmethod
    def gen_QAs(node,n_ary_ratio, para_len_ratio):
        depth = node
        n_ary = int(node * n_ary_ratio)
        # para_len = int(node * para_len_ratio)
        root, name, keeper = Tree.random(depth, n_ary)
        depth_for, path_for = choices(list(keeper.keys()), k=2)
        dumped_edges_raw = Tree.get_edges(root).split('\n')
        dumped_edges = []
        for e in dumped_edges_raw:
            if not e.startswith("None"):
                dumped_edges.append(e)
        dumped_edges='\n'.join(dumped_edges)
        here_is_input = ("In the following is the edges in the tree, with father being placed "
                         f"before child node: {dumped_edges}.")

        system = ("You are an undergraduate majoring in computer science who is "
                  "currently learning Data Structure and Algorithm, you are required to "
                  "answer some questions about the commonly used structure TREE.")

        # height
        q1_thin = ("What is the height of the root node, i.e., the number of edges "
                   "in the longest path from root node to any leaf nodes? "
                   "Answer an integer, leaf is of height 0. ")
        q1 = q1_thin+here_is_input
        a1 = str(Tree.get_height(root))

        # depth
        q2_thin = (f"What is the depth of node {depth_for}? "
                   "Answer an integer, root is of depth 0. ")
        q2 = q2_thin+here_is_input
        a2 = str(keeper[depth_for].depth)

        # path
        q3_thin = ("What is the path from the root "
                   f"node to the node {path_for}. "
                   "Answer should look like A->D->H. ")
        q3 = q3_thin+here_is_input
        a3 = Tree.get_path(root, path_for)

        return {'system': system, 'QA': [(q1, a1), (q2, a2), (q3, a3)],
                'labels': [['Tree.Height'], ['Tree.Depth'], ['PathCompose']],
                'QA_to_save': [(q1_thin, a1, dumped_edges), (q2_thin, a2, dumped_edges), (q3_thin, a3, dumped_edges)],
                }

if __name__ == '__main__':
    print(Tree.gen_QAs()['QA'][0][0])