from .krpc import append_info_hash
import getuseragent
import httpx
import re
import threading
import time

class indexer:
    def __apibay(self):
        while True:
            headers = {
                'Connection': 'close',
                'User-Agent': getuseragent.UserAgent().Random()
            }
            url = 'https://apibay.org/precompiled/data_top100_recent.json'
            with httpx.Client() as client:
                try:
                    response = client.get(url = url, headers = headers)
                    response.raise_for_status()
                    if response.status_code == 200:
                        data = response.json()
                        for i in data:
                            info_hash = i['info_hash']
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, info_hash.lower())
                            if match is not None:
                                append_info_hash.spider_krpc_append_info_hash_messages.put(
                                    match.group(0)
                                )
                except httpx.HTTPError:
                    pass
                except Exception:
                    pass
                finally:
                    locals().clear()
            time.sleep(3600)

    def __eztvre(self):
        while True:
            headers = {
                'Connection': 'close',
                'User-Agent': getuseragent.UserAgent().Random()
            }
            url = 'https://eztv.re/api/get-torrents?limit=100'
            with httpx.Client() as client:
                try:
                    response = client.get(url = url, headers = headers)
                    response.raise_for_status()
                    if response.status_code == 200:
                        data = response.json()
                        for i in data['torrents']:
                            info_hash = i['hash']
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, info_hash.lower())
                            if match is not None:
                                append_info_hash.spider_krpc_append_info_hash_messages.put(
                                    match.group(0)
                                )
                except httpx.HTTPError:
                    pass
                except Exception:
                    pass
                finally:
                    locals().clear()
            time.sleep(3600)

    def __ytsmx(self):
        while True:
            headers = {
                'Connection': 'close',
                'User-Agent': getuseragent.UserAgent().Random()
            }
            url = 'https://yts.mx/api/v2/list_movies.json'
            with httpx.Client() as client:
                try:
                    response = client.get(url = url, headers = headers)
                    response.raise_for_status()
                    if response.status_code == 200:
                        data = response.json()
                        for i in data['data']['movies']:
                            for j in i['torrents']:
                                info_hash = j['hash']
                                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                match = re.match(pattern, info_hash.lower())
                                if match is not None:
                                    append_info_hash.spider_krpc_append_info_hash_messages.put(
                                        match.group(0)
                                    )
                except httpx.HTTPError:
                    pass
                except Exception:
                    pass
                finally:
                    locals().clear()
            time.sleep(3600)

    def start(self):
        explorer_spider_indexer_apibay_thread = threading.Thread(target = self.__apibay)
        explorer_spider_indexer_apibay_thread.setDaemon(True)
        explorer_spider_indexer_apibay_thread.start()
        explorer_spider_indexer_eztvre_thread = threading.Thread(target = self.__eztvre)
        explorer_spider_indexer_eztvre_thread.setDaemon(True)
        explorer_spider_indexer_eztvre_thread.start()
        explorer_spider_indexer_ytsmx_thread = threading.Thread(target = self.__ytsmx)
        explorer_spider_indexer_ytsmx_thread.setDaemon(True)
        explorer_spider_indexer_ytsmx_thread.start()