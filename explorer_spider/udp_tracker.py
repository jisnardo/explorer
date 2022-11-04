from .bootstrap_udp_trackers import bootstrap_udp_trackers
from .memory import memory
from .peer_wire import ut_metadata
import IPy
import operator
import queue
import random
import threading
import time

class udp_tracker:
    spider_udp_tracker_v4_messages = queue.Queue()
    spider_udp_tracker_v6_messages = queue.Queue()

    def __listen_ipv4(self, explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4):
        while True:
            spider_udp_tracker_v4_messages = self.spider_udp_tracker_v4_messages.get()
            info_hash = spider_udp_tracker_v4_messages[0]
            force_query = spider_udp_tracker_v4_messages[1]
            if force_query is False:
                database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                if database_count_info_hash_messages['result'] == 0:
                    if len(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list) > 5:
                        bootstrap_udp_trackers_tracker_ipv4_list = random.sample(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list, 5)
                        for i in bootstrap_udp_trackers_tracker_ipv4_list:
                            ip_address = i[0]
                            udp_port = i[1]
                            explorer_spider_udp_tracker_work_ipv4_scrape_thread = threading.Thread(target = self.__work_ipv4_scrape, args = (explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash, force_query,))
                            explorer_spider_udp_tracker_work_ipv4_scrape_thread.setDaemon(True)
                            explorer_spider_udp_tracker_work_ipv4_scrape_thread.start()
                        time.sleep(60)
                    else:
                        for i in bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list:
                            ip_address = i[0]
                            udp_port = i[1]
                            explorer_spider_udp_tracker_work_ipv4_scrape_thread = threading.Thread(target = self.__work_ipv4_scrape, args = (explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash, force_query,))
                            explorer_spider_udp_tracker_work_ipv4_scrape_thread.setDaemon(True)
                            explorer_spider_udp_tracker_work_ipv4_scrape_thread.start()
                        time.sleep(60)
            elif force_query is True:
                if len(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list) > 5:
                    bootstrap_udp_trackers_tracker_ipv4_list = random.sample(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list, 5)
                    for i in bootstrap_udp_trackers_tracker_ipv4_list:
                        ip_address = i[0]
                        udp_port = i[1]
                        explorer_spider_udp_tracker_work_ipv4_scrape_thread = threading.Thread(target = self.__work_ipv4_scrape, args = (explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash, force_query,))
                        explorer_spider_udp_tracker_work_ipv4_scrape_thread.setDaemon(True)
                        explorer_spider_udp_tracker_work_ipv4_scrape_thread.start()
                    time.sleep(60)
                else:
                    for i in bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list:
                        ip_address = i[0]
                        udp_port = i[1]
                        explorer_spider_udp_tracker_work_ipv4_scrape_thread = threading.Thread(target = self.__work_ipv4_scrape, args = (explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash, force_query,))
                        explorer_spider_udp_tracker_work_ipv4_scrape_thread.setDaemon(True)
                        explorer_spider_udp_tracker_work_ipv4_scrape_thread.start()
                    time.sleep(60)

    def __listen_ipv6(self, explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6):
        while True:
            spider_udp_tracker_v6_messages = self.spider_udp_tracker_v6_messages.get()
            info_hash = spider_udp_tracker_v6_messages[0]
            force_query = spider_udp_tracker_v6_messages[1]
            if force_query is False:
                database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                if database_count_info_hash_messages['result'] == 0:
                    if len(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list) > 5:
                        bootstrap_udp_trackers_tracker_ipv6_list = random.sample(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list, 5)
                        for i in bootstrap_udp_trackers_tracker_ipv6_list:
                            ip_address = i[0]
                            udp_port = i[1]
                            explorer_spider_udp_tracker_work_ipv6_scrape_thread = threading.Thread(target = self.__work_ipv6_scrape, args = (explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash, force_query,))
                            explorer_spider_udp_tracker_work_ipv6_scrape_thread.setDaemon(True)
                            explorer_spider_udp_tracker_work_ipv6_scrape_thread.start()
                        time.sleep(60)
                    else:
                        for i in bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list:
                            ip_address = i[0]
                            udp_port = i[1]
                            explorer_spider_udp_tracker_work_ipv6_scrape_thread = threading.Thread(target = self.__work_ipv6_scrape, args = (explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash, force_query,))
                            explorer_spider_udp_tracker_work_ipv6_scrape_thread.setDaemon(True)
                            explorer_spider_udp_tracker_work_ipv6_scrape_thread.start()
                        time.sleep(60)
            elif force_query is True:
                if len(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list) > 5:
                    bootstrap_udp_trackers_tracker_ipv6_list = random.sample(bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list, 5)
                    for i in bootstrap_udp_trackers_tracker_ipv6_list:
                        ip_address = i[0]
                        udp_port = i[1]
                        explorer_spider_udp_tracker_work_ipv6_scrape_thread = threading.Thread(target = self.__work_ipv6_scrape, args = (explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash, force_query,))
                        explorer_spider_udp_tracker_work_ipv6_scrape_thread.setDaemon(True)
                        explorer_spider_udp_tracker_work_ipv6_scrape_thread.start()
                    time.sleep(60)
                else:
                    for i in bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list:
                        ip_address = i[0]
                        udp_port = i[1]
                        explorer_spider_udp_tracker_work_ipv6_scrape_thread = threading.Thread(target = self.__work_ipv6_scrape, args = (explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash, force_query,))
                        explorer_spider_udp_tracker_work_ipv6_scrape_thread.setDaemon(True)
                        explorer_spider_udp_tracker_work_ipv6_scrape_thread.start()
                    time.sleep(60)

    def __work_ipv4_announce_started(self, explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash):
        udp_tracker_v4_announce_started_messages = explorer_udp_tracker_v4.announce_started(ip_address, udp_port, info_hash, 0, 0, 0, 6881)
        ip_address = udp_tracker_v4_announce_started_messages['header']['ip_address']
        udp_port = udp_tracker_v4_announce_started_messages['header']['udp_port']
        info_hash = udp_tracker_v4_announce_started_messages['header']['info_hash']
        state = udp_tracker_v4_announce_started_messages['result']['state']
        if state is True:
            peers = udp_tracker_v4_announce_started_messages['result']['peers']
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
                                'header': udp_tracker_v4_announce_started_messages['header']
                            })
                        for i in peers_list:
                            peer_ip_address = i[0]
                            peer_tcp_port = i[1]
                            explorer_spider_udp_tracker_work_ipv4_announce_started_thread = threading.Thread(target = explorer_krpc_v4.ping, args = (peer_ip_address, peer_tcp_port,))
                            explorer_spider_udp_tracker_work_ipv4_announce_started_thread.setDaemon(True)
                            explorer_spider_udp_tracker_work_ipv4_announce_started_thread.start()
            time.sleep(60)
            self.__work_ipv4_announce_stopped(explorer_udp_tracker_v4, ip_address, udp_port, info_hash)

    def __work_ipv4_announce_stopped(self, explorer_udp_tracker_v4, ip_address, udp_port, info_hash):
        explorer_udp_tracker_v4.announce_stopped(ip_address, udp_port, info_hash, 0, 0, 0, 6881)
        locals().clear()

    def __work_ipv4_scrape(self, explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash, force_query):
        udp_tracker_v4_scrape_messages = explorer_udp_tracker_v4.scrape(ip_address, udp_port, info_hash)
        ip_address = udp_tracker_v4_scrape_messages['header']['ip_address']
        udp_port = udp_tracker_v4_scrape_messages['header']['udp_port']
        info_hash = udp_tracker_v4_scrape_messages['header']['info_hash']
        state = udp_tracker_v4_scrape_messages['result']['state']
        if state is True:
            seeders = udp_tracker_v4_scrape_messages['result']['seeders']
            completed = udp_tracker_v4_scrape_messages['result']['completed']
            leechers = udp_tracker_v4_scrape_messages['result']['leechers']
            all_number = seeders + completed + leechers
            if all_number > 0:
                if force_query is False:
                    database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                    if database_count_info_hash_messages['result'] == 0:
                        time.sleep(60)
                        self.__work_ipv4_announce_started(explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash)
                elif force_query is True:
                    time.sleep(60)
                    self.__work_ipv4_announce_started(explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4, ip_address, udp_port, info_hash)
        elif state is False:
            tracker_domain_list = [ip_address, udp_port]
            if tracker_domain_list in bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list:
                bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv4_list.remove(tracker_domain_list)
        locals().clear()

    def __work_ipv6_announce_started(self, explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash):
        udp_tracker_v6_announce_started_messages = explorer_udp_tracker_v6.announce_started(ip_address, udp_port, info_hash, 0, 0, 0, 6881)
        ip_address = udp_tracker_v6_announce_started_messages['header']['ip_address']
        udp_port = udp_tracker_v6_announce_started_messages['header']['udp_port']
        info_hash = udp_tracker_v6_announce_started_messages['header']['info_hash']
        state = udp_tracker_v6_announce_started_messages['result']['state']
        if state is True:
            peers6 = udp_tracker_v6_announce_started_messages['result']['peers6']
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
                                'header': udp_tracker_v6_announce_started_messages['header']
                            })
                        for i in peers6_list:
                            peer6_ip_address = i[0]
                            peer6_tcp_port = i[1]
                            explorer_spider_udp_tracker_work_ipv6_announce_started_thread = threading.Thread(target = explorer_krpc_v6.ping, args = (peer6_ip_address, peer6_tcp_port,))
                            explorer_spider_udp_tracker_work_ipv6_announce_started_thread.setDaemon(True)
                            explorer_spider_udp_tracker_work_ipv6_announce_started_thread.start()
            time.sleep(60)
            self.__work_ipv6_announce_stopped(explorer_udp_tracker_v6, ip_address, udp_port, info_hash)

    def __work_ipv6_announce_stopped(self, explorer_udp_tracker_v6, ip_address, udp_port, info_hash):
        explorer_udp_tracker_v6.announce_stopped(ip_address, udp_port, info_hash, 0, 0, 0, 6881)
        locals().clear()

    def __work_ipv6_scrape(self, explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash, force_query):
        udp_tracker_v6_scrape_messages = explorer_udp_tracker_v6.scrape(ip_address, udp_port, info_hash)
        ip_address = udp_tracker_v6_scrape_messages['header']['ip_address']
        udp_port = udp_tracker_v6_scrape_messages['header']['udp_port']
        info_hash = udp_tracker_v6_scrape_messages['header']['info_hash']
        state = udp_tracker_v6_scrape_messages['result']['state']
        if state is True:
            seeders = udp_tracker_v6_scrape_messages['result']['seeders']
            completed = udp_tracker_v6_scrape_messages['result']['completed']
            leechers = udp_tracker_v6_scrape_messages['result']['leechers']
            all_number = seeders + completed + leechers
            if all_number > 0:
                if force_query is False:
                    database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                    if database_count_info_hash_messages['result'] == 0:
                        time.sleep(60)
                        self.__work_ipv6_announce_started(explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash)
                elif force_query is True:
                    time.sleep(60)
                    self.__work_ipv6_announce_started(explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6, ip_address, udp_port, info_hash)
        elif state is False:
            tracker_domain_list = [ip_address, udp_port]
            if tracker_domain_list in bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list:
                bootstrap_udp_trackers.spider_bootstrap_udp_trackers_tracker_ipv6_list.remove(tracker_domain_list)
        locals().clear()

    def start(self, explorer_database, explorer_krpc_v4, explorer_krpc_v6, explorer_udp_tracker_v4, explorer_udp_tracker_v6):
        explorer_spider_udp_tracker_listen_ipv4_thread = threading.Thread(target = self.__listen_ipv4, args = (explorer_database, explorer_krpc_v4, explorer_udp_tracker_v4,))
        explorer_spider_udp_tracker_listen_ipv4_thread.setDaemon(True)
        explorer_spider_udp_tracker_listen_ipv4_thread.start()
        explorer_spider_udp_tracker_listen_ipv6_thread = threading.Thread(target = self.__listen_ipv6, args = (explorer_database, explorer_krpc_v6, explorer_udp_tracker_v6,))
        explorer_spider_udp_tracker_listen_ipv6_thread.setDaemon(True)
        explorer_spider_udp_tracker_listen_ipv6_thread.start()