import os
from pyquery import PyQuery as pq
import mungy

if __name__ == '__main__':
    mung = mungy.Munger()
    # Table to dict
    html = pq(filename='{}/comps.html'.format(os.getcwd()))
    f = mung.table_to_dict_values(html.find('#top10'))
    # f = mung.table_to_dict_indices(html.find('#top10'))
    print mung.json(mung.dict_to_list(f))
    print f

    # Single list
    list_html = pq(filename='{}/list.html'.format(os.getcwd()))
    t = mung.list_to_list(list_html.find('#complex'))
    print t

    # Multiple lists
    swords = {}
    listhtml = pq(filename='{}/swords.html'.format(os.getcwd()))
    headlines = pq(listhtml).find('.mw-headline')
    for k, ul in enumerate(pq(listhtml).find('ul')):
        key = pq(headlines).eq(k).text().strip().lower()
        if key:
            swords[key] = mung.list_to_list(pq(ul))
    print mung.json(swords)

    # Multiple lists generic
    swords = {}
    listhtml = pq(filename='{}/syseng.html'.format(os.getcwd()))
    for k, ul in enumerate(pq(listhtml).find('ul')):
        swords[k] = mung.list_to_list(pq(ul))
    print mung.json(swords)
