import random
split = ','




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

class Person:

    def __init__(self, key: str, name: str):
        self.primeKey = key
        '''=====Bioinfo Table====='''
        self.age = random.randint(10, 70)
        self.gender = random.choice(['male', 'female'])
        self.name = name
        self.height = random.randint(120, 220)
        self.weight = random.randint(70, 180)
        self.color = random.choice(Person.color())

        '''=====Work Table====='''
        self.status = random.choice(["retired", "employed", "unemployed"])
        self.salary = random.randint(1000, 1000_000)
        self.company = random.choice(["NVIDIA", "Apple", "Meta", "Google", "Twitter", "Microsoft", "OPENAI"])
        self.location = random.choice(Person.cities())

    def __bio(self):
        return f'{self.gender}{split}{self.age}{split}{self.name}{split}{self.height}{split}{self.weight}{split}{self.color}'

    def __wrk(self):
        return f'{self.status}{split}{self.salary}{split}{self.company}{split}{self.location}'

    def bio_to_string(self):
        return f'{self.primeKey}{split}{self.__bio()}'

    def work_to_string(self):
        return f'{self.primeKey}{split}{self.__wrk()}'

    def to_string(self):
        return f'{self.primeKey}{split}{self.__bio()}{split}{self.__wrk()}'

    @classmethod
    def gen_random(cls, node):
        key_gen = Name()
        name_gen = Name(init=random.randint(0, 25))
        size = node
        data = [Person(key_gen.poll(), name_gen.poll()) for _ in range(size)]
        return data, list(key_gen.hist)

    @classmethod
    def bio_table_head(cls):
        return f'primeKey{split}gender{split}age{split}name{split}height{split}weight{split}color'

    @classmethod
    def work_table_head(cls):
        return f'primeKey{split}status{split}salary{split}company{split}location'

    @classmethod
    def fields(cls):
        return ['age', 'gender', 'name', 'height', 'weight', 'color', 'status', 'salary', 'company', 'location']

    @classmethod
    def color(cls):
        return ['white', 'black', 'brown', 'olive', 'swarthy', 'mulatto']

    @classmethod
    def cities(cls):
        return ["CA", "WA", "TX", "NY", "GA", "HI", "IL"]
