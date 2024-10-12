#!/usr/bin/env python3
import random

from name import Name


class Structure:
    def __init__(self, properties, content, children):
        self.properties = properties
        self.content = content
        self.children = children

    def __getattr__(self, name):
        return self.properties[name]

    def dfs(self, func):
        func(self)
        for node in self.children:
            node.dfs(func)

    @staticmethod
    def __dfs(depth, n_ary, func, **kwargs):
        root = Structure(properties={}, content='', children=[])
        func(root, **kwargs)
        if depth != 0:
            for _ in range(n_ary):
                kwargs['father'] = root
                root.children.append(Structure.__dfs(
                    depth-1, n_ary, func, **kwargs))
        return root

    @staticmethod
    def random(depth, n_ary, content_name=None):
        name = content_name if content_name else Name(init=random.randint(0,25))
        keeper = dict()

        def func(node, **kwargs):
            node.content = name.poll()
            node.father = kwargs['father']
            keeper[node.content] = node

        return Structure.__dfs(depth, n_ary, func, father=None), name, keeper
