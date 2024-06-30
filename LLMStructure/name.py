#!/usr/bin/env python3
import testee


class Name:
    def __init__(self, init=0, vocab=None, delimiter=''):
        self.delimiter = delimiter
        self.id = init
        self.hist = set()
        if not vocab:
            vocab = {i: chr(ord('a')+i) for i in range(26)}
        self.vocab = vocab

    def poll(self):
        name = self[self.id]
        self.hist.add(name)
        self.id += 1
        return name

    def __getitem__(self, key):
        if key == 0:
            name = self.vocab[0]
        else:
            name_seg = []
            while key:
                name_seg.append(self.vocab[key % 26])
                key = key//26
            name = self.delimiter.join(name_seg)
        return name

if __name__ == '__main__':
    import sys
    print(sys.path)