import requests
import pandas

def traverse_nested_dict(d):
    iters = [d.iteritems()]

    while iters:
        it = iters.pop()
        try:
            k, v = it.next()
        except StopIteration:
            continue

        iters.append(it)

        if isinstance(v, dict):
            iters.append(v.iteritems())
        yield k, v


def transform_to_json(dot_notation_dict):
    keys_dict = {}
    delim = '.'
    for key, val in dot_notation_dict.items():
        if delim in key:
            splits = key.split(delim)
            if splits[0] not in keys_dict:
                keys_dict[splits[0]] = {}
            keys_dict[splits[0]]['.'.join(splits[1:])] = val
        else:
            keys_dict[key] = val
    for key, val in keys_dict.items():
        if isinstance(val, dict):
            keys_dict[key] = transform_to_json(val)
    return keys_dict

class QueryResult(object):
    def __init__(self, response):
        self.response = response

    @property
    def _rows(self):
        return self.response['rows']

    @property
    def _headers(self):
        return self.response['headers']

    def toJson(self):
        rows = self._rows
        for row in rows:
            yield transform_to_json(row)
    
    def toPandas(self):
        headers = [h['name'] for h in self._headers]
        rows = [[r.get(h, None) for h in headers] for r in self._rows]
        return pandas.DataFrame(rows, columns=headers)

    def __str__(self):
        return "<Results len = %s>" % len(self._rows)


class FoxtrotException(Exception):
    pass


class Foxtrot(object):
    def __init__(self, uri, auth_token = None,cookies = {}, timeout = 10):
        self.uri = uri
        self.cookies = cookies
        self.timeout = timeout
        self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        if auth_token is not None:
            self.headers['Authorization'] = "Bearer "+ auth_token

    def fql(self, query):
        api = self.uri+ '/foxtrot/v1/fql'
        # print api
        try:
            res = requests.post(api, data=query, headers=self.headers, timeout=self.timeout, cookies=self.cookies)
            if res.status_code == 204:
                return QueryResult({'rows': [], 'headers': []})
            if res.status_code != 200:
                raise FoxtrotException("Invalid query. Please check the query and try again. Status %s" %res.status_code)
            return QueryResult(res.json())
        except requests.exceptions.ConnectionError:
            raise FoxtrotException("Could not connect to node")
        except ValueError as e:
            raise FoxtrotException("Unknown response"+e)


