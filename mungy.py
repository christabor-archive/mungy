from pyquery import PyQuery as pq
import json


class MalformedHTMLError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Munger():
    """Designed to be fluent/chainable."""

    def json(self, data):
        return json.dumps(data)

    def dict_to_list(self, data):
        ls = []
        for k, v in data.iteritems():
            ls.append(v)
        return ls

    def list_to_list(self, list_html):
        data = []
        # ul > li to list of lists
        for li in pq(list_html).find('li'):
            data.append(pq(li).text())
        return data

    def table_to_dict_values(self, table_html):
        # Sort by values
        data = {}
        headings = []
        for k, heading in enumerate(pq(table_html).find('thead th')):
            headings.append(pq(heading).text().strip().lower())
        for k, row in enumerate(pq(table_html).find('tbody tr')):
            data[k] = {}
            for k1, cell in enumerate(pq(row).find('td')):
                title = headings[k1]
                data[k][title] = pq(cell).text().strip().lower()
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
            for k, heading in enumerate(pq(table_html).find('thead th')):
                data[k] = (pq(heading).text().strip().lower(), [])
            for k, row in enumerate(pq(table_html).find('tbody tr')):
                for k1, cell in enumerate(pq(row).find('td')):
                    try:
                        # Nested tables, etc will just
                        # merged into the single td
                        data[k1][1].append(pq(cell).text().strip().lower())
                    except KeyError:
                        continue
        return data
