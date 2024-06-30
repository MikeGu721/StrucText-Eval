import os, random
from Person import Person


def gen_QAs(node, n_ary_ratio, para_len_ratio):
    data, roster = Person.gen_random(node=node)
    finder = {}
    for i, row in enumerate(data):
        finder[row.primeKey] = i
    system = "The following is two table of people. The first one is about biotic information. The second one is " \
             "about the occupations. For each table, the first line is the name for each field, the following li" \
             "nes gives the value for each field, in the same order as the first line, one person per line. " \
             "The records with the same primeKey refer to the same person."
    bio_table = [Person.bio_table_head()] + [c.bio_to_string() for c in data]
    wrk_table = [Person.work_table_head()] + [c.work_to_string() for c in data]
    system += "\n".join(bio_table)
    system += "\n\n"
    system += "\n".join(wrk_table)
    # print(prompt_init)

    # select an node
    selected_id = random.choice(roster)

    # build the query
    # Q1: query the value
    fields_to_ask = random.choice(Person.fields())
    q1 = '\nWhat is the {} of record with primeKey {}\n'.format(fields_to_ask, selected_id)
    t1 = str(data[finder[selected_id]].__dict__[fields_to_ask])

    # Q2,3 query with statistic
    threshold = random.randint(1000, 999_999)
    q2 = '\nHow many people work with salary more than {}?\n'.format(threshold)
    t2 = f" {str(sum([int(p.salary > threshold) for p in data]))} "
    gender = ['female', 'male'][random.randint(0,1)]
    q3 = f'\nHow many people are {gender}?\n'
    t3 = f" {str(sum([int(p.gender == gender) for p in data]))} "

    # Q4 join
    city_picked = random.choice(Person.cities())
    lb = random.randint(150, 180)
    q4 = f'\nHow many people who work in {city_picked} are taller than {lb}?\n'
    t4 = f" {str(sum([int(p.location == city_picked and p.height > lb) for p in data]))} "

    input_thin = "\n".join(bio_table) + "\n\n" + "\n".join(wrk_table)
    return {'system': system, 'QA': [(q1, t1), (q2, t2), (q3, t3), (q4, t4)],
            'labels': [['TextRetrieval'], ['Statistics'], ['Statistics'], ['Join']],
            'QA_to_save': [(q1, t1, input_thin), (q2, t2, input_thin), (q3, t3, input_thin), (q4, t4, input_thin)],
            }



class CSV:
    @staticmethod
    def gen_QAs(node=4,n_ary_ratio=1,para_len_ratio=1):
        return gen_QAs(node=node, n_ary_ratio=n_ary_ratio, para_len_ratio=para_len_ratio)


if __name__ == '__main__':
    d = CSV.gen_QAs()
    print(d['system'])
    for i, qa in enumerate(d['QA']):
        print(i, qa[0])
        print(i, qa[1])
