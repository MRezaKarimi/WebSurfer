from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseNotFound
from .storage import Storage
from .ranking import tfidf_ranking, positional_ranking, merge_sort
from django.core.paginator import Paginator
import json
import time

def rank_sort(query_string: list, ranking_method, positional=False)-> list:
    """
    Params: query set and ranking
    Returns: sorted results
    """
    with Storage() as db:
        title_docs = []
        body_docs = []

        title_dic_list = list(db.load_title_dicts(query_string))
        body_dic_list = list(db.load_body_dicts(query_string))

        if len(title_dic_list) == 0 and len(body_dic_list) == 0:
            return HttpResponseNotFound('<h1>No result was found</h1>')
        
        if len(title_dic_list) != 0:
            # Rank based on title
            title_doc_id_list = set.intersection(*[set(dic.keys()) for dic in title_dic_list])

            # Remove '_id' & 'word' from list and keep doc IDs
            title_doc_id_list.remove('_id')
            title_doc_id_list.remove('word')

            # Load docs from DB
            title_docs = list(db.load_docs(list(title_doc_id_list)))

            if positional:
                ranking_method(query_string, title_docs, title_dic_list, 10)
            else:
                ranking_method(title_docs, title_dic_list, 10)

        if len(body_dic_list) != 0:
            # Rank based on body
            body_doc_id_list = set.intersection(*[set(dic.keys()) for dic in body_dic_list])
        
            # Remove '_id' & 'word' from list and keep doc IDs
            body_doc_id_list.remove('_id')
            body_doc_id_list.remove('word')

            # Load docs from DB
            body_docs = list(db.load_docs(list(body_doc_id_list)))

            if positional:
                ranking_method(query_string, body_docs, body_dic_list, 1)
            else:
                ranking_method(body_docs, body_dic_list, 1)


    return merge_sort(title_docs, body_docs)


def search(request):
    start_time = time.time()

    query_string = request.GET['q'].strip().split(' ')
    page_num = request.GET.get('page', 1)

    result = rank_sort(query_string, tfidf_ranking)
    paginator = Paginator(result, 10)

    return render(request, 'query/serp.html', {
        'page': paginator.get_page(page_num), 
        'words': list(cache.get('words')),
        'time': time.time() - start_time,
        'url_query': '+'.join(query_string)
        })

def psearch(request):
    start_time = time.time()

    # if id:
    #     print(id)

    query_string = request.GET['q'].split(' ')
    page_num = request.GET.get('page', 1)

    result = rank_sort(query_string, positional_ranking, True)
    paginator = Paginator(result, 10)
    
    return render(request, 'query/serp.html', {
        'page': paginator.get_page(page_num), 
        'words': list(cache.get('words')),
        'time': time.time() - start_time,
        'url_query': '+'.join(query_string)
    })

def home(request):
    return render(request, 'query/index.html', {'words': json.dumps(list(cache.get('words')))})
    