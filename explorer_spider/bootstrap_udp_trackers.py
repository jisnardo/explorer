import dns.resolver
import getuseragent
import httpx
import IPy
import json
import operator
import os
import random
import threading
import time
import urllib.parse

class bootstrap_udp_trackers:
    spider_bootstrap_udp_trackers_tracker_ipv4_list = []
    spider_bootstrap_udp_trackers_tracker_ipv6_list = []

    def __query_bootstrap_udp_trackers_ipv4_address(self, domain_name):
        ipv4_address_list = []
        try:
            for i in dns.resolver.query(domain_name, 'A').response.answer:
                for j in i.items:
                    if j.rdtype == 1:
                        ipv4_address_list.append(j.address)
            return ipv4_address_list
        except:
            return ipv4_address_list

    def __query_bootstrap_udp_trackers_ipv6_address(self, domain_name):
        ipv6_address_list = []
        try:
            for i in dns.resolver.query(domain_name, 'AAAA').response.answer:
                for j in i.items:
                    if j.rdtype == 28:
                        ipv6_address_list.append(j.address)
            return ipv6_address_list
        except:
            return ipv6_address_list

    def __query_bootstrap_udp_trackers_tracker_list(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/tracker_list_config.json', mode = 'r', encoding = 'utf-8') as file:
            config = file.read()
            tracker_list_config = json.loads(config)['udp_tracker_list']
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
                            if result.scheme == 'udp':
                                tracker_domain_name = result.netloc.rsplit(':', 1)[0]
                                tracker_domain_name = tracker_domain_name.replace('[', '')
                                tracker_domain_name = tracker_domain_name.replace(']', '')
                                if result.port is not None:
                                    try:
                                        if IPy.IP(tracker_domain_name).version() == 4:
                                            ip_address_type = IPy.IP(tracker_domain_name).iptype()
                                            if ip_address_type == 'PUBLIC':
                                                if 1 <= result.port <= 65535:
                                                    tracker_domain_list = [tracker_domain_name, result.port]
                                                    tracker_domain_result = False
                                                    for j in self.spider_bootstrap_udp_trackers_tracker_ipv4_list:
                                                        if operator.eq(j, tracker_domain_list) is True:
                                                            tracker_domain_result = True
                                                    if tracker_domain_result is False:
                                                        self.spider_bootstrap_udp_trackers_tracker_ipv4_list.append(tracker_domain_list)
                                        elif IPy.IP(tracker_domain_name).version() == 6:
                                            ip_address_type = IPy.IP(tracker_domain_name).iptype()[:9]
                                            if ip_address_type == 'ALLOCATED':
                                                if 1 <= result.port <= 65535:
                                                    tracker_domain_list = [tracker_domain_name, result.port]
                                                    tracker_domain_result = False
                                                    for j in self.spider_bootstrap_udp_trackers_tracker_ipv6_list:
                                                        if operator.eq(j, tracker_domain_list) is True:
                                                            tracker_domain_result = True
                                                    if tracker_domain_result is False:
                                                        self.spider_bootstrap_udp_trackers_tracker_ipv6_list.append(tracker_domain_list)
                                    except:
                                        ipv4_address_list = self.__query_bootstrap_udp_trackers_ipv4_address(tracker_domain_name)
                                        for j in ipv4_address_list:
                                            ip_address_type = IPy.IP(j).iptype()
                                            if ip_address_type == 'PUBLIC':
                                                if 1 <= result.port <= 65535:
                                                    tracker_domain_list = [j, result.port]
                                                    tracker_domain_result = False
                                                    for k in self.spider_bootstrap_udp_trackers_tracker_ipv4_list:
                                                        if operator.eq(k, tracker_domain_list) is True:
                                                            tracker_domain_result = True
                                                    if tracker_domain_result is False:
                                                        self.spider_bootstrap_udp_trackers_tracker_ipv4_list.append(tracker_domain_list)
                                        ipv6_address_list = self.__query_bootstrap_udp_trackers_ipv6_address(tracker_domain_name)
                                        for l in ipv6_address_list:
                                            ip_address_type = IPy.IP(l).iptype()[:9]
                                            if ip_address_type == 'ALLOCATED':
                                                if 1 <= result.port <= 65535:
                                                    tracker_domain_list = [l, result.port]
                                                    tracker_domain_result = False
                                                    for m in self.spider_bootstrap_udp_trackers_tracker_ipv6_list:
                                                        if operator.eq(m, tracker_domain_list) is True:
                                                            tracker_domain_result = True
                                                    if tracker_domain_result is False:
                                                        self.spider_bootstrap_udp_trackers_tracker_ipv6_list.append(tracker_domain_list)
                except httpx.HTTPError:
                    pass
                except Exception:
                    pass
        locals().clear()

    def __update_bootstrap_udp_trackers_tracker_list(self):
        while True:
            self.spider_bootstrap_udp_trackers_tracker_ipv4_list.clear()
            self.spider_bootstrap_udp_trackers_tracker_ipv6_list.clear()
            self.__query_bootstrap_udp_trackers_tracker_list()
            time.sleep(1800)

    def start(self):
        explorer_spider_bootstrap_udp_trackers_update_bootstrap_udp_trackers_tracker_list_thread = threading.Thread(target = self.__update_bootstrap_udp_trackers_tracker_list)
        explorer_spider_bootstrap_udp_trackers_update_bootstrap_udp_trackers_tracker_list_thread.setDaemon(True)
        explorer_spider_bootstrap_udp_trackers_update_bootstrap_udp_trackers_tracker_list_thread.start()