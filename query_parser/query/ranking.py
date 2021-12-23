from math import log10
from django.core.cache import cache


def merge_sort(title_doc_list: list, body_doc_list: list)-> list:
    temp_docs = {doc['id']: doc for doc in title_doc_list}
    for doc in body_doc_list:
        if doc['id'] in temp_docs.keys():
            temp_docs[doc['id']]['score'] += doc['score']
        else:
            temp_docs[doc['id']] = doc
    return sorted(list(temp_docs.values()), key=lambda doc: doc['score'], reverse=True)


def tfidf_ranking(docs: list, dic_list: list, weight: int)-> list:
    N = cache.get('total_docs')
    for doc in docs:
        score = 0
        for dictionary in dic_list:
            tf = len(dictionary[doc.get('id')])
            idf = N / (len(dictionary.keys()) - 2)
            score += (1 + log10(tf)) * log10(idf)
        doc['score'] = score * weight


def dic_search(word: str, dic_list: list, doc_id: str)-> list:
    for dic in dic_list:
        if dic['word'] == word:
            return dic[doc_id]
    return []


def positional_ranking(query: list, docs: list, dic_list: list, weight: int):
    for doc in docs:
        l = []
        
        for term in query:
            term_positions = dic_search(term, dic_list, doc['id'])
            l.extend([(term, pos) for pos in term_positions])
        
        l.sort(key=lambda i: i[1])

        di = 0
        for i in range(len(l)):
            if len(l) == 1 or i+1 == len(l):
                break
            if query.index(l[i+1][0]) == query.index(l[i][0]):
                continue
            di += l[i+1][1] - l[i][1]
            if query.index(l[i+1][0]) - query.index(l[i][0]) < 0:
                di += 2
        doc['score'] = (1 / di) * weight if di else 0
