from .http_tracker import http_tracker
from .memory import memory
from .peer_wire import ut_metadata
from .udp_tracker import udp_tracker
import IPy
import operator
import os
import queue
import random
import re
import threading
import time

class append_info_hash:
    spider_krpc_append_info_hash_messages = queue.Queue()

    def __listen(self, explorer_database):
        while True:
            spider_krpc_append_info_hash_messages = self.spider_krpc_append_info_hash_messages.get()
            pattern = re.compile(r'\b[0-9a-f]{40}\b')
            match = re.match(pattern, spider_krpc_append_info_hash_messages.lower())
            if match is not None:
                database_count_info_hash_messages = explorer_database.count_info_hash(match.group(0))
                if database_count_info_hash_messages['result'] == 0:
                    if http_tracker.spider_http_tracker_messages.qsize() < 100:
                        http_tracker.spider_http_tracker_messages.put(
                            [match.group(0), False]
                        )
                    if memory.ipv4_network_connectivity is True:
                        if udp_tracker.spider_udp_tracker_v4_messages.qsize() < 100:
                            udp_tracker.spider_udp_tracker_v4_messages.put(
                                [match.group(0), False]
                            )
                        get_peers.spider_krpc_v4_get_peers_messages.put(
                            match.group(0)
                        )
                    if memory.ipv6_network_connectivity is True:
                        if udp_tracker.spider_udp_tracker_v6_messages.qsize() < 100:
                            udp_tracker.spider_udp_tracker_v6_messages.put(
                                [match.group(0), False]
                            )
                        get_peers.spider_krpc_v6_get_peers_messages.put(
                            match.group(0)
                        )
            time.sleep(0.002)

    def start(self, explorer_database):
        explorer_spider_krpc_append_info_hash_listen_thread = threading.Thread(target = self.__listen, args = (explorer_database,))
        explorer_spider_krpc_append_info_hash_listen_thread.setDaemon(True)
        explorer_spider_krpc_append_info_hash_listen_thread.start()

class get_peers:
    spider_krpc_v4_get_peers_messages = queue.Queue()
    spider_krpc_v6_get_peers_messages = queue.Queue()

    def __get_peers_listen_ipv4(self, explorer_database, explorer_krpc_v4):
        while True:
            spider_krpc_v4_get_peers_messages = self.spider_krpc_v4_get_peers_messages.get()
            explorer_spider_krpc_get_peers_work_ipv4_thread = threading.Thread(target = self.__get_peers_work_ipv4, args = (explorer_database, explorer_krpc_v4, spider_krpc_v4_get_peers_messages,))
            explorer_spider_krpc_get_peers_work_ipv4_thread.setDaemon(True)
            explorer_spider_krpc_get_peers_work_ipv4_thread.start()

    def __get_peers_listen_ipv6(self, explorer_database, explorer_krpc_v6):
        while True:
            spider_krpc_v6_get_peers_messages = self.spider_krpc_v6_get_peers_messages.get()
            explorer_spider_krpc_get_peers_work_ipv6_thread = threading.Thread(target = self.__get_peers_work_ipv6, args = (explorer_database, explorer_krpc_v6, spider_krpc_v6_get_peers_messages,))
            explorer_spider_krpc_get_peers_work_ipv6_thread.setDaemon(True)
            explorer_spider_krpc_get_peers_work_ipv6_thread.start()

    def __get_peers_work_ipv4(self, explorer_database, explorer_krpc_v4, info_hash):
        krpc_v4_get_peers_messages = explorer_krpc_v4.get_peers(info_hash)
        if not len(krpc_v4_get_peers_messages['result']) == 0:
            database_count_info_hash_messages = explorer_database.count_info_hash(krpc_v4_get_peers_messages['header']['info_hash'])
            if database_count_info_hash_messages['result'] == 0:
                peers = []
                for i in krpc_v4_get_peers_messages['result']:
                    peer_ip_address = i[0]
                    peer_tcp_port = i[1]
                    ip_address_type = IPy.IP(peer_ip_address).iptype()
                    if ip_address_type == 'PUBLIC':
                        if 1 <= peer_tcp_port <= 65535:
                            peer_list = [peer_ip_address, peer_tcp_port]
                            peer_list_result = False
                            for j in peers:
                                if operator.eq(j, peer_list) is True:
                                    peer_list_result = True
                            if peer_list_result is False:
                                peers.append(peer_list)
                if len(peers) > 0:
                    ut_metadata.spider_peer_wire_v4_ut_metadata_messages.put({
                        'result': peers,
                        'header': krpc_v4_get_peers_messages['header']
                    })
        locals().clear()

    def __get_peers_work_ipv6(self, explorer_database, explorer_krpc_v6, info_hash):
        krpc_v6_get_peers_messages = explorer_krpc_v6.get_peers(info_hash)
        if not len(krpc_v6_get_peers_messages['result']) == 0:
            database_count_info_hash_messages = explorer_database.count_info_hash(krpc_v6_get_peers_messages['header']['info_hash'])
            if database_count_info_hash_messages['result'] == 0:
                peers6 = []
                for i in krpc_v6_get_peers_messages['result']:
                    peer6_ip_address = i[0]
                    peer6_tcp_port = i[1]
                    ip_address_type = IPy.IP(peer6_ip_address).iptype()[:9]
                    if ip_address_type == 'ALLOCATED':
                        if 1 <= peer6_tcp_port <= 65535:
                            peer6_list = [peer6_ip_address, peer6_tcp_port]
                            peer6_list_result = False
                            for j in peers6:
                                if operator.eq(j, peer6_list) is True:
                                    peer6_list_result = True
                            if peer6_list_result is False:
                                peers6.append(peer6_list)
                if len(peers6) > 0:
                    ut_metadata.spider_peer_wire_v6_ut_metadata_messages.put({
                        'result': peers6,
                        'header': krpc_v6_get_peers_messages['header']
                    })
        locals().clear()

    def start(self, explorer_database, explorer_krpc_v4, explorer_krpc_v6):
        explorer_spider_krpc_get_peers_listen_ipv4_thread = threading.Thread(target = self.__get_peers_listen_ipv4, args = (explorer_database, explorer_krpc_v4,))
        explorer_spider_krpc_get_peers_listen_ipv4_thread.setDaemon(True)
        explorer_spider_krpc_get_peers_listen_ipv4_thread.start()
        explorer_spider_krpc_get_peers_listen_ipv6_thread = threading.Thread(target = self.__get_peers_listen_ipv6, args = (explorer_database, explorer_krpc_v6,))
        explorer_spider_krpc_get_peers_listen_ipv6_thread.setDaemon(True)
        explorer_spider_krpc_get_peers_listen_ipv6_thread.start()

class query_info_hashes:
    def __listen_ipv4(self, explorer_database, explorer_krpc_v4):
        while True:
            for i in explorer_krpc_v4.query_info_hashes().keys():
                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                match = re.match(pattern, i.lower())
                if match is not None:
                    database_count_info_hash_messages = explorer_database.count_info_hash(match.group(0))
                    if database_count_info_hash_messages['result'] == 0:
                        if http_tracker.spider_http_tracker_messages.qsize() < 100:
                            http_tracker.spider_http_tracker_messages.put(
                                [match.group(0), False]
                            )
                        if memory.ipv4_network_connectivity is True:
                            if udp_tracker.spider_udp_tracker_v4_messages.qsize() < 100:
                                udp_tracker.spider_udp_tracker_v4_messages.put(
                                    [match.group(0), False]
                                )
                            get_peers.spider_krpc_v4_get_peers_messages.put(
                                match.group(0)
                            )
                        if memory.ipv6_network_connectivity is True:
                            if udp_tracker.spider_udp_tracker_v6_messages.qsize() < 100:
                                udp_tracker.spider_udp_tracker_v6_messages.put(
                                    [match.group(0), False]
                                )
                            get_peers.spider_krpc_v6_get_peers_messages.put(
                                match.group(0)
                            )
                time.sleep(0.002)
            time.sleep(900)

    def __listen_ipv6(self, explorer_database, explorer_krpc_v6):
        while True:
            for i in explorer_krpc_v6.query_info_hashes().keys():
                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                match = re.match(pattern, i.lower())
                if match is not None:
                    database_count_info_hash_messages = explorer_database.count_info_hash(match.group(0))
                    if database_count_info_hash_messages['result'] == 0:
                        if http_tracker.spider_http_tracker_messages.qsize() < 100:
                            http_tracker.spider_http_tracker_messages.put(
                                [match.group(0), False]
                            )
                        if memory.ipv4_network_connectivity is True:
                            if udp_tracker.spider_udp_tracker_v4_messages.qsize() < 100:
                                udp_tracker.spider_udp_tracker_v4_messages.put(
                                    [match.group(0), False]
                                )
                            get_peers.spider_krpc_v4_get_peers_messages.put(
                                match.group(0)
                            )
                        if memory.ipv6_network_connectivity is True:
                            if udp_tracker.spider_udp_tracker_v6_messages.qsize() < 100:
                                udp_tracker.spider_udp_tracker_v6_messages.put(
                                    [match.group(0), False]
                                )
                            get_peers.spider_krpc_v6_get_peers_messages.put(
                                match.group(0)
                            )
                time.sleep(0.002)
            time.sleep(900)

    def start(self, explorer_database, explorer_krpc_v4, explorer_krpc_v6):
        explorer_spider_krpc_query_info_hashes_listen_ipv4_thread = threading.Thread(target = self.__listen_ipv4, args = (explorer_database, explorer_krpc_v4,))
        explorer_spider_krpc_query_info_hashes_listen_ipv4_thread.setDaemon(True)
        explorer_spider_krpc_query_info_hashes_listen_ipv4_thread.start()
        explorer_spider_krpc_query_info_hashes_listen_ipv6_thread = threading.Thread(target = self.__listen_ipv6, args = (explorer_database, explorer_krpc_v6,))
        explorer_spider_krpc_query_info_hashes_listen_ipv6_thread.setDaemon(True)
        explorer_spider_krpc_query_info_hashes_listen_ipv6_thread.start()

class query_nodes_number:
    spider_krpc_query_nodes_number_like_string = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def __listen_ipv4(self, explorer_database, explorer_krpc_v4):
        time.sleep(300)
        while True:
            if explorer_krpc_v4.query_nodes_number() == 0:
                if memory.ipv4_network_connectivity is True:
                    like_string = random.choice(self.spider_krpc_query_nodes_number_like_string)
                    database_query_like_messages = explorer_database.query_like(like_string)
                    if database_query_like_messages['result'] is not False:
                        messages_length = len(database_query_like_messages['result'])
                        if messages_length > 25:
                            for i in range(0, 25):
                                key = str(random.randint(0, messages_length - 1))
                                info_hash = database_query_like_messages['result'][key]['info_hash']
                                http_tracker.spider_http_tracker_messages.put(
                                    [info_hash, True]
                                )
                                udp_tracker.spider_udp_tracker_v4_messages.put(
                                    [info_hash, True]
                                )
                                time.sleep(0.002)
            time.sleep(600)

    def __listen_ipv6(self, explorer_database, explorer_krpc_v6):
        time.sleep(300)
        while True:
            if explorer_krpc_v6.query_nodes_number() == 0:
                if memory.ipv6_network_connectivity is True:
                    like_string = random.choice(self.spider_krpc_query_nodes_number_like_string)
                    database_query_like_messages = explorer_database.query_like(like_string)
                    if database_query_like_messages['result'] is not False:
                        messages_length = len(database_query_like_messages['result'])
                        if messages_length > 25:
                            for i in range(0, 25):
                                key = str(random.randint(0, messages_length - 1))
                                info_hash = database_query_like_messages['result'][key]['info_hash']
                                http_tracker.spider_http_tracker_messages.put(
                                    [info_hash, True]
                                )
                                udp_tracker.spider_udp_tracker_v6_messages.put(
                                    [info_hash, True]
                                )
                                time.sleep(0.002)
            time.sleep(600)

    def start(self, explorer_database, explorer_krpc_v4, explorer_krpc_v6):
        explorer_spider_krpc_query_nodes_number_listen_ipv4_thread = threading.Thread(target = self.__listen_ipv4, args = (explorer_database, explorer_krpc_v4,))
        explorer_spider_krpc_query_nodes_number_listen_ipv4_thread.setDaemon(True)
        explorer_spider_krpc_query_nodes_number_listen_ipv4_thread.start()
        explorer_spider_krpc_query_nodes_number_listen_ipv6_thread = threading.Thread(target = self.__listen_ipv6, args = (explorer_database, explorer_krpc_v6,))
        explorer_spider_krpc_query_nodes_number_listen_ipv6_thread.setDaemon(True)
        explorer_spider_krpc_query_nodes_number_listen_ipv6_thread.start()

class sample_infohashes:
    spider_krpc_v4_sample_infohashes_prefix = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    spider_krpc_v4_sample_infohashes_prefix_number = 0
    spider_krpc_v6_sample_infohashes_prefix = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    spider_krpc_v6_sample_infohashes_prefix_number = 0

    def __sample_infohashes_listen_ipv4(self, explorer_database, explorer_krpc_v4):
        while True:
            ip_address_type = IPy.IP(explorer_krpc_v4.self_ip_address()).iptype()
            if ip_address_type == 'PUBLIC':
                if explorer_krpc_v4.query_nodes_number() > 0:
                    target_id = explorer_krpc_v4.self_node_id()[:1] + self.spider_krpc_v4_sample_infohashes_prefix[self.spider_krpc_v4_sample_infohashes_prefix_number] + os.urandom(19).hex()
                    self.spider_krpc_v4_sample_infohashes_prefix_number = self.spider_krpc_v4_sample_infohashes_prefix_number + 1
                    if self.spider_krpc_v4_sample_infohashes_prefix_number == 16:
                        self.spider_krpc_v4_sample_infohashes_prefix_number = 0
                    krpc_v4_sample_infohashes_messages = explorer_krpc_v4.sample_infohashes(target_id)
                    if not len(krpc_v4_sample_infohashes_messages['result']) == 0:
                        for i in krpc_v4_sample_infohashes_messages['result']:
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, i.lower())
                            if match is not None:
                                database_count_info_hash_messages = explorer_database.count_info_hash(match.group(0))
                                if database_count_info_hash_messages['result'] == 0:
                                    if http_tracker.spider_http_tracker_messages.qsize() < 100:
                                        http_tracker.spider_http_tracker_messages.put(
                                            [match.group(0), False]
                                        )
                                    if memory.ipv4_network_connectivity is True:
                                        if udp_tracker.spider_udp_tracker_v4_messages.qsize() < 100:
                                            udp_tracker.spider_udp_tracker_v4_messages.put(
                                                [match.group(0), False]
                                            )
                                        get_peers.spider_krpc_v4_get_peers_messages.put(
                                            match.group(0)
                                        )
                                    if memory.ipv6_network_connectivity is True:
                                        if udp_tracker.spider_udp_tracker_v6_messages.qsize() < 100:
                                            udp_tracker.spider_udp_tracker_v6_messages.put(
                                                [match.group(0), False]
                                            )
                                        get_peers.spider_krpc_v6_get_peers_messages.put(
                                            match.group(0)
                                        )
                            time.sleep(0.002)
                        time.sleep(30)
                    else:
                        time.sleep(30)
                else:
                    time.sleep(30)
            else:
                time.sleep(30)

    def __sample_infohashes_listen_ipv6(self, explorer_database, explorer_krpc_v6):
        while True:
            ip_address_type = IPy.IP(explorer_krpc_v6.self_ip_address()).iptype()[:9]
            if ip_address_type == 'ALLOCATED':
                if explorer_krpc_v6.query_nodes_number() > 0:
                    target_id = explorer_krpc_v6.self_node_id()[:1] + self.spider_krpc_v6_sample_infohashes_prefix[self.spider_krpc_v6_sample_infohashes_prefix_number] + os.urandom(19).hex()
                    self.spider_krpc_v6_sample_infohashes_prefix_number = self.spider_krpc_v6_sample_infohashes_prefix_number + 1
                    if self.spider_krpc_v6_sample_infohashes_prefix_number == 16:
                        self.spider_krpc_v6_sample_infohashes_prefix_number = 0
                    krpc_v6_sample_infohashes_messages = explorer_krpc_v6.sample_infohashes(target_id)
                    if not len(krpc_v6_sample_infohashes_messages['result']) == 0:
                        for i in krpc_v6_sample_infohashes_messages['result']:
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, i.lower())
                            if match is not None:
                                database_count_info_hash_messages = explorer_database.count_info_hash(match.group(0))
                                if database_count_info_hash_messages['result'] == 0:
                                    if http_tracker.spider_http_tracker_messages.qsize() < 100:
                                        http_tracker.spider_http_tracker_messages.put(
                                            [match.group(0), False]
                                        )
                                    if memory.ipv4_network_connectivity is True:
                                        if udp_tracker.spider_udp_tracker_v4_messages.qsize() < 100:
                                            udp_tracker.spider_udp_tracker_v4_messages.put(
                                                [match.group(0), False]
                                            )
                                        get_peers.spider_krpc_v4_get_peers_messages.put(
                                            match.group(0)
                                        )
                                    if memory.ipv6_network_connectivity is True:
                                        if udp_tracker.spider_udp_tracker_v6_messages.qsize() < 100:
                                            udp_tracker.spider_udp_tracker_v6_messages.put(
                                                [match.group(0), False]
                                            )
                                        get_peers.spider_krpc_v6_get_peers_messages.put(
                                            match.group(0)
                                        )
                            time.sleep(0.002)
                        time.sleep(30)
                    else:
                        time.sleep(30)
                else:
                    time.sleep(30)
            else:
                time.sleep(30)

    def start(self, explorer_database, explorer_krpc_v4, explorer_krpc_v6):
        self.spider_krpc_v4_sample_infohashes_prefix_number = 0
        explorer_spider_krpc_sample_infohashes_listen_ipv4_thread = threading.Thread(target = self.__sample_infohashes_listen_ipv4, args = (explorer_database, explorer_krpc_v4,))
        explorer_spider_krpc_sample_infohashes_listen_ipv4_thread.setDaemon(True)
        explorer_spider_krpc_sample_infohashes_listen_ipv4_thread.start()
        self.spider_krpc_v6_sample_infohashes_prefix_number = 0
        explorer_spider_krpc_sample_infohashes_listen_ipv6_thread = threading.Thread(target = self.__sample_infohashes_listen_ipv6, args = (explorer_database, explorer_krpc_v6,))
        explorer_spider_krpc_sample_infohashes_listen_ipv6_thread.setDaemon(True)
        explorer_spider_krpc_sample_infohashes_listen_ipv6_thread.start()