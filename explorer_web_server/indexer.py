import getuseragent
import httpx
import re
import urllib.parse

class indexer:
    def apibay(self, like_string):
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = 'https://apibay.org/q.php?q={}'.format(
            urllib.parse.quote(like_string)
        )
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    info_hash_list = []
                    data = response.json()
                    for i in data:
                        info_hash = i['info_hash']
                        pattern = re.compile(r'\b[0-9a-f]{40}\b')
                        match = re.match(pattern, info_hash.lower())
                        if match is not None:
                            info_hash_list.append(match.group(0))
                    result = {
                        'data': info_hash_list,
                        'state': True
                    }
                    return result
                else:
                    result = {
                        'error': response.status_code,
                        'state': False
                    }
                    return result
            except httpx.HTTPError as error:
                result = {
                    'error': error,
                    'state': False
                }
                return result
            except Exception as error:
                result = {
                    'error': error,
                    'state': False
                }
                return result
            finally:
                locals().clear()

    def ytsmx(self, like_string):
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = 'https://yts.mx/api/v2/list_movies.json?query_term={}'.format(
            urllib.parse.quote(like_string)
        )
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    info_hash_list = []
                    data = response.json()
                    for i in data['data']['movies']:
                        for j in i['torrents']:
                            info_hash = j['hash']
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, info_hash.lower())
                            if match is not None:
                                info_hash_list.append(match.group(0))
                    result = {
                        'data': info_hash_list,
                        'state': True
                    }
                    return result
                else:
                    result = {
                        'error': response.status_code,
                        'state': False
                    }
                    return result
            except httpx.HTTPError as error:
                result = {
                    'error': error,
                    'state': False
                }
                return result
            except Exception as error:
                result = {
                    'error': error,
                    'state': False
                }
                return result
            finally:
                locals().clear()