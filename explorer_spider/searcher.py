from .krpc import append_info_hash
import datetime
import getuseragent
import httpx
import re
import threading
import time
import urllib.parse

class searcher:
    def __auto_search(self):
        while True:
            like_string_list = []
            for i in range(0, 30):
                year = datetime.datetime.today().year - i
                like_string_list.append(str(year))
            for j in like_string_list:
                apibay_result = self.apibay(j)
                ytsmx_result = self.ytsmx(j)
                result = []
                if apibay_result['state'] is True:
                    for k in apibay_result['data']:
                        if k not in result:
                            result.append(k)
                if ytsmx_result['state'] is True:
                    for l in ytsmx_result['data']:
                        if l not in result:
                            result.append(l)
                for m in result:
                    append_info_hash.spider_krpc_append_info_hash_messages.put(
                        m
                    )
                time.sleep(900)
            time.sleep(3600)

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

    def start(self):
        explorer_spider_searcher_auto_search_thread = threading.Thread(target = self.__auto_search)
        explorer_spider_searcher_auto_search_thread.setDaemon(True)
        explorer_spider_searcher_auto_search_thread.start()

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