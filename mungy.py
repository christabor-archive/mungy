from pyquery import PyQuery as pq
import json


class MalformedHTMLError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Munger():
    """Designed to be fluent/chainable."""

    def to_json(self, data):
        return json.dumps(data)

    def html_to_lists(self, pqhtml):
        """Takes a chunk of html and generates multiple lists
        from all found UL's on the page.
        """
        # TODO: Add OL support
        list_html = []
        for k, ul in enumerate(pq(pqhtml).find('ul')):
            list_html.append(self.list_to_list(pq(ul)))
        return list_html

    def dict_to_list(self, data):
        ls = []
        for _, v in data.iteritems():
            ls.append(v)
        return ls

    def list_to_list(self, list_html):
        """Takes a single ul node and converts it to a
        list of list-items"""
        list_items = []
        for li in pq(list_html).find('li'):
            list_items.append(pq(li).text())
        return list_items

    def table_to_dict_values(self, table_html):
        """Takes table html and converts into a
        dictionary with the following format:
            {
                "0": {
                    "thead1": "td1"
                    "thead2": "td2"
                },
                "1": {
                    "thead1": "td1"
                    "thead2": "td2"
                }
            }
        """
        data = {}
        headings = []
        # Try proper theader formatting first.
        ths = pq(table_html).find('thead th')
        if not ths:
            ths = pq(table_html).find('th')
        if not ths:
            raise MalformedHTMLError('Invalid html. No THs could be found.')
        for th in ths:
            headings.append('_'.join(pq(th).text().strip().lower().split(' ')))
        trs = pq(table_html).find('tbody tr')
        if not trs:
            trs = pq(table_html).find('tr')
        if not trs:
            raise MalformedHTMLError('Invalid html. No TRs could be found.')
        for k, tr in enumerate(trs):
            tr_data = {}
            for k1, td in enumerate(pq(tr).children()):
                tr_data[headings[k1]] = pq(td).text().strip().lower()
            data[k] = tr_data
        return data

    def table_to_dict_indices(self, table_html):
        # Sort by indices
        data = {}
        """
        Example output
        data = {
            [0: (th1, [td1, tdn]),
            [1: (th2, [td2, tdn]),
        }
        """
        # TODO: handle images
        # Handle plain tables, no headings
        if not pq(table_html).find('tbody') and not \
                pq(table_html).find('thead'):
                    for k, row in enumerate(pq(table_html).find('tr')):
                        data[k] = []
                        for k1, cell in enumerate(pq(row).find('td')):
                            data[k].append(pq(cell).text().strip().lower())
        else:
            # Handle traditionally (properly) formatted tables
            for _, heading in enumerate(pq(table_html).find('thead th')):
                data[k] = (pq(heading).text().strip().lower(), [])
            for _, row in enumerate(pq(table_html).find('tbody tr')):
                for k1, cell in enumerate(pq(row).find('td')):
                    try:
                        # Nested tables, etc will just
                        # merged into the single td
                        data[k1][1].append(pq(cell).text().strip().lower())
                    except KeyError:
                        continue
        return data
