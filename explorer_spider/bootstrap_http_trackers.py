import getuseragent
import httpx
import json
import operator
import os
import random
import threading
import time
import urllib.parse

class bootstrap_http_trackers:
    spider_bootstrap_http_trackers_tracker_list = []

    def __query_bootstrap_http_trackers_tracker_list(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/tracker_list_config.json', mode = 'r', encoding = 'utf-8') as file:
            config = file.read()
            tracker_list_config = json.loads(config)['http_tracker_list']
            key = str(random.randint(0, len(tracker_list_config) - 1))
            tracker_list_api_url = tracker_list_config[key]
            headers = {
                'Connection': 'close',
                'User-Agent': getuseragent.UserAgent().Random()
            }
            with httpx.Client() as client:
                try:
                    response = client.get(url = tracker_list_api_url, headers = headers)
                    response.raise_for_status()
                    if response.status_code == 200:
                        message = response.text
                        message = message.replace(' ', '')
                        message_list = message.split('\n')
                        message_list.pop()
                        for i in message_list:
                            result = urllib.parse.urlparse(url = i)
                            if result.scheme == 'http':
                                tracker_domain_name = result.netloc.rsplit(':', 1)[0]
                                if result.port is not None:
                                    tracker_domain_list = [result.scheme, tracker_domain_name, result.port]
                                    tracker_domain_result = False
                                    for j in self.spider_bootstrap_http_trackers_tracker_list:
                                        if operator.eq(j, tracker_domain_list) is True:
                                            tracker_domain_result = True
                                    if tracker_domain_result is False:
                                        self.spider_bootstrap_http_trackers_tracker_list.append(tracker_domain_list)
                            elif result.scheme == 'https':
                                tracker_domain_name = result.netloc.rsplit(':', 1)[0]
                                if result.port is not None:
                                    tracker_domain_list = [result.scheme, tracker_domain_name, result.port]
                                    tracker_domain_result = False
                                    for j in self.spider_bootstrap_http_trackers_tracker_list:
                                        if operator.eq(j, tracker_domain_list) is True:
                                            tracker_domain_result = True
                                    if tracker_domain_result is False:
                                        self.spider_bootstrap_http_trackers_tracker_list.append(tracker_domain_list)
                except httpx.HTTPError:
                    pass
                except Exception:
                    pass
        locals().clear()

    def __update_bootstrap_http_trackers_tracker_list(self):
        while True:
            self.spider_bootstrap_http_trackers_tracker_list.clear()
            self.__query_bootstrap_http_trackers_tracker_list()
            time.sleep(1800)

    def start(self):
        explorer_spider_bootstrap_http_trackers_update_bootstrap_http_trackers_tracker_list_thread = threading.Thread(target = self.__update_bootstrap_http_trackers_tracker_list)
        explorer_spider_bootstrap_http_trackers_update_bootstrap_http_trackers_tracker_list_thread.setDaemon(True)
        explorer_spider_bootstrap_http_trackers_update_bootstrap_http_trackers_tracker_list_thread.start()