from .bootstrap_http_trackers import bootstrap_http_trackers
from .memory import memory
from .peer_wire import ut_metadata
import IPy
import operator
import queue
import random
import threading
import time
import urllib.parse

class http_tracker:
    spider_http_tracker_messages = queue.Queue()

    def __listen(self, explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6):
        while True:
            spider_http_tracker_messages = self.spider_http_tracker_messages.get()
            info_hash = spider_http_tracker_messages[0]
            force_query = spider_http_tracker_messages[1]
            if force_query is False:
                database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                if database_count_info_hash_messages['result'] == 0:
                    if len(bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list) > 5:
                        bootstrap_http_trackers_tracker_list = random.sample(bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list, 5)
                        for i in bootstrap_http_trackers_tracker_list:
                            tracker_domain_scheme = i[0]
                            tracker_domain_name = i[1]
                            tracker_domain_port = i[2]
                            domain_url = tracker_domain_scheme + '://' + tracker_domain_name + ':' + str(tracker_domain_port)
                            explorer_spider_http_tracker_work_scrape_thread = threading.Thread(target = self.__work_scrape, args = (explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash, force_query,))
                            explorer_spider_http_tracker_work_scrape_thread.setDaemon(True)
                            explorer_spider_http_tracker_work_scrape_thread.start()
                        time.sleep(60)
                    else:
                        for i in bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list:
                            tracker_domain_scheme = i[0]
                            tracker_domain_name = i[1]
                            tracker_domain_port = i[2]
                            domain_url = tracker_domain_scheme + '://' + tracker_domain_name + ':' + str(tracker_domain_port)
                            explorer_spider_http_tracker_work_scrape_thread = threading.Thread(target = self.__work_scrape, args = (explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash, force_query,))
                            explorer_spider_http_tracker_work_scrape_thread.setDaemon(True)
                            explorer_spider_http_tracker_work_scrape_thread.start()
                        time.sleep(60)
            elif force_query is True:
                if len(bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list) > 5:
                    bootstrap_http_trackers_tracker_list = random.sample(bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list, 5)
                    for i in bootstrap_http_trackers_tracker_list:
                        tracker_domain_scheme = i[0]
                        tracker_domain_name = i[1]
                        tracker_domain_port = i[2]
                        domain_url = tracker_domain_scheme + '://' + tracker_domain_name + ':' + str(tracker_domain_port)
                        explorer_spider_http_tracker_work_scrape_thread = threading.Thread(target = self.__work_scrape, args = (explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash, force_query,))
                        explorer_spider_http_tracker_work_scrape_thread.setDaemon(True)
                        explorer_spider_http_tracker_work_scrape_thread.start()
                    time.sleep(60)
                else:
                    for i in bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list:
                        tracker_domain_scheme = i[0]
                        tracker_domain_name = i[1]
                        tracker_domain_port = i[2]
                        domain_url = tracker_domain_scheme + '://' + tracker_domain_name + ':' + str(tracker_domain_port)
                        explorer_spider_http_tracker_work_scrape_thread = threading.Thread(target = self.__work_scrape, args = (explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash, force_query,))
                        explorer_spider_http_tracker_work_scrape_thread.setDaemon(True)
                        explorer_spider_http_tracker_work_scrape_thread.start()
                    time.sleep(60)

    def __work_announce_started(self, explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash):
        http_tracker_announce_started_messages = explorer_http_tracker.announce_started(domain_url, info_hash, 0, 0, 0, 6881)
        domain_url = http_tracker_announce_started_messages['header']['domain_url']
        info_hash = http_tracker_announce_started_messages['header']['info_hash']
        state = http_tracker_announce_started_messages['result']['state']
        if state is True:
            peers = http_tracker_announce_started_messages['result']['peers']
            peers6 = http_tracker_announce_started_messages['result']['peers6']
            if memory.ipv4_network_connectivity is True:
                if len(peers) > 0:
                    peers_list = []
                    for i in peers:
                        peer_ip_address = i[0]
                        peer_tcp_port = i[1]
                        ip_address_type = IPy.IP(peer_ip_address).iptype()
                        if ip_address_type == 'PUBLIC':
                            if 1 <= peer_tcp_port <= 65535:
                                peer_list = [peer_ip_address, peer_tcp_port]
                                peer_list_result = False
                                for j in peers_list:
                                    if operator.eq(j, peer_list) is True:
                                        peer_list_result = True
                                if peer_list_result is False:
                                    peers_list.append(peer_list)
                    if len(peers_list) > 0:
                        database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                        if database_count_info_hash_messages['result'] == 0:
                            ut_metadata.spider_peer_wire_v4_ut_metadata_messages.put({
                                'result': peers_list,
                                'header': http_tracker_announce_started_messages['header']
                            })
                        for i in peers_list:
                            peer_ip_address = i[0]
                            peer_tcp_port = i[1]
                            explorer_spider_http_tracker_work_announce_started_explorer_krpc_v4_ping_thread = threading.Thread(target = explorer_krpc_v4.ping, args = (peer_ip_address, peer_tcp_port,))
                            explorer_spider_http_tracker_work_announce_started_explorer_krpc_v4_ping_thread.setDaemon(True)
                            explorer_spider_http_tracker_work_announce_started_explorer_krpc_v4_ping_thread.start()
            if memory.ipv6_network_connectivity is True:
                if len(peers6) > 0:
                    peers6_list = []
                    for i in peers6:
                        peer6_ip_address = i[0]
                        peer6_tcp_port = i[1]
                        ip_address_type = IPy.IP(peer6_ip_address).iptype()[:9]
                        if ip_address_type == 'ALLOCATED':
                            if 1 <= peer6_tcp_port <= 65535:
                                peer6_list = [peer6_ip_address, peer6_tcp_port]
                                peer6_list_result = False
                                for j in peers6_list:
                                    if operator.eq(j, peer6_list) is True:
                                        peer6_list_result = True
                                if peer6_list_result is False:
                                    peers6_list.append(peer6_list)
                    if len(peers6_list) > 0:
                        database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                        if database_count_info_hash_messages['result'] == 0:
                            ut_metadata.spider_peer_wire_v6_ut_metadata_messages.put({
                                'result': peers6_list,
                                'header': http_tracker_announce_started_messages['header']
                            })
                        for i in peers6_list:
                            peer6_ip_address = i[0]
                            peer6_tcp_port = i[1]
                            explorer_spider_http_tracker_work_announce_started_explorer_krpc_v6_ping_thread = threading.Thread(target = explorer_krpc_v6.ping, args = (peer6_ip_address, peer6_tcp_port,))
                            explorer_spider_http_tracker_work_announce_started_explorer_krpc_v6_ping_thread.setDaemon(True)
                            explorer_spider_http_tracker_work_announce_started_explorer_krpc_v6_ping_thread.start()
            time.sleep(60)
            self.__work_announce_stopped(explorer_http_tracker, domain_url, info_hash)

    def __work_announce_stopped(self, explorer_http_tracker, domain_url, info_hash):
        explorer_http_tracker.announce_stopped(domain_url, info_hash, 0, 0, 0, 6881)
        locals().clear()

    def __work_scrape(self, explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash, force_query):
        http_tracker_scrape_messages = explorer_http_tracker.scrape(domain_url, info_hash)
        domain_url = http_tracker_scrape_messages['header']['domain_url']
        info_hash = http_tracker_scrape_messages['header']['info_hash']
        state = http_tracker_scrape_messages['result']['state']
        if state is True:
            complete = http_tracker_scrape_messages['result']['complete']
            downloaded = http_tracker_scrape_messages['result']['downloaded']
            incomplete = http_tracker_scrape_messages['result']['incomplete']
            all_number = complete + downloaded + incomplete
            if all_number > 0:
                if force_query is False:
                    database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                    if database_count_info_hash_messages['result'] == 0:
                        time.sleep(60)
                        self.__work_announce_started(explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash)
                elif force_query is True:
                    time.sleep(60)
                    self.__work_announce_started(explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, domain_url, info_hash)
        elif state is False:
            result = urllib.parse.urlparse(url = domain_url)
            if result.scheme == 'http':
                tracker_domain_name = result.netloc.rsplit(':', 1)[0]
                tracker_domain_list = [result.scheme, tracker_domain_name, result.port]
                if tracker_domain_list in bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list:
                    bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list.remove(tracker_domain_list)
            elif result.scheme == 'https':
                tracker_domain_name = result.netloc.rsplit(':', 1)[0]
                tracker_domain_list = [result.scheme, tracker_domain_name, result.port]
                if tracker_domain_list in bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list:
                    bootstrap_http_trackers.spider_bootstrap_http_trackers_tracker_list.remove(tracker_domain_list)
        locals().clear()

    def start(self, explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6):
        explorer_spider_http_tracker_listen_thread = threading.Thread(target = self.__listen, args = (explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6,))
        explorer_spider_http_tracker_listen_thread.setDaemon(True)
        explorer_spider_http_tracker_listen_thread.start()