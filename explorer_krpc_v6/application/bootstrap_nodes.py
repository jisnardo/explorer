from ..application.client import client
from ..database.distributed_hash_table import distributed_hash_table
from ..driver.memory import memory
import copy
import IPy
import os
import queue
import random
import re
import threading
import time

class bootstrap_nodes:
    application_bootstrap_nodes = []
    application_bootstrap_nodes_key = []
    application_bootstrap_nodes_operators = queue.Queue()
    application_bootstrap_nodes_prefix = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    def __check(self):
        while True:
            if len(self.application_bootstrap_nodes_key) > 0:
                for i in self.application_bootstrap_nodes_key:
                    if i[1] < int(time.time()) - 300:
                        self.application_bootstrap_nodes_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __operators(self):
        while True:
            application_bootstrap_nodes_operators = self.application_bootstrap_nodes_operators.get()
            operate = application_bootstrap_nodes_operators[0]
            element = application_bootstrap_nodes_operators[1]
            if operate == 'append':
                if element not in self.application_bootstrap_nodes_key:
                    self.application_bootstrap_nodes_key.append(element)
            if operate == 'remove':
                if element in self.application_bootstrap_nodes_key:
                    self.application_bootstrap_nodes_key.remove(element)

    def __recvfrom_find_node(self):
        while True:
            application_client_find_node_messages_send_application_bootstrap_nodes_find_node = client.application_client_find_node_messages_send_application_bootstrap_nodes_find_node.get()
            if application_client_find_node_messages_send_application_bootstrap_nodes_find_node[0] is not False:
                nodes6 = application_client_find_node_messages_send_application_bootstrap_nodes_find_node[1]
                application_bootstrap_nodes_keyword = application_client_find_node_messages_send_application_bootstrap_nodes_find_node[7]
                for i in self.application_bootstrap_nodes_key:
                    if i[0] == application_bootstrap_nodes_keyword:
                        for j in nodes6:
                            nodes6_node_id = j[0]
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, nodes6_node_id.lower())
                            if match is None:
                                if j in nodes6:
                                    nodes6.remove(j)
                            elif match.group(0) == memory.node_id:
                                if j in nodes6:
                                    nodes6.remove(j)
                        for j in nodes6:
                            nodes6_ip_address = j[1]
                            ip_address_type = IPy.IP(nodes6_ip_address).iptype()[:9]
                            if ip_address_type == 'LINKLOCAL':
                                if j in nodes6:
                                    nodes6.remove(j)
                            if ip_address_type == 'LOOPBACK':
                                if j in nodes6:
                                    nodes6.remove(j)
                        for j in nodes6:
                            nodes6_udp_port = j[2]
                            if not 1 <= nodes6_udp_port <= 65535:
                                if j in nodes6:
                                    nodes6.remove(j)
                        for j in nodes6:
                            nodes6_node_id = j[0]
                            distributed_hash_table.database_query_node_with_node_id_messages_recvfrom.put(
                                nodes6_node_id
                            )
                            database_query_node_with_node_id_messages_send = distributed_hash_table.database_query_node_with_node_id_messages_send.get()
                            if database_query_node_with_node_id_messages_send is True:
                                if j in nodes6:
                                    nodes6.remove(j)
                        for j in nodes6:
                            nodes6_node_id = j[0]
                            nodes6_ip_address = j[1]
                            nodes6_udp_port = j[2]
                            distributed_hash_table.database_append_node_messages.put(
                                [nodes6_node_id, nodes6_ip_address, nodes6_udp_port]
                            )
                        self.application_bootstrap_nodes_operators.put(
                            ['remove', i]
                        )

    def __recvfrom_ping(self):
        while True:
            application_client_ping_messages_send_application_bootstrap_nodes_ping = client.application_client_ping_messages_send_application_bootstrap_nodes_ping.get()
            if application_client_ping_messages_send_application_bootstrap_nodes_ping[0] is not False:
                node_id = application_client_ping_messages_send_application_bootstrap_nodes_ping[0]
                ip_address = application_client_ping_messages_send_application_bootstrap_nodes_ping[5]
                udp_port = application_client_ping_messages_send_application_bootstrap_nodes_ping[6]
                application_bootstrap_nodes_keyword = application_client_ping_messages_send_application_bootstrap_nodes_ping[7]
                for i in self.application_bootstrap_nodes_key:
                    if i[0] == application_bootstrap_nodes_keyword:
                        pattern = re.compile(r'\b[0-9a-f]{40}\b')
                        match = re.match(pattern, node_id.lower())
                        if match is not None:
                            ip_address_type = IPy.IP(ip_address).iptype()[:9]
                            if ip_address_type == 'ALLOCATED':
                                if 1 <= udp_port <= 65535:
                                    distributed_hash_table.database_append_node_messages.put(
                                        [match.group(0), ip_address, udp_port]
                                    )
                                    self.application_bootstrap_nodes_operators.put(
                                        ['remove', i]
                                    )
                                    application_bootstrap_nodes_keyword = os.urandom(20).hex()
                                    application_bootstrap_nodes_new_prefix = copy.deepcopy(self.application_bootstrap_nodes_prefix)
                                    application_bootstrap_nodes_new_prefix.remove(memory.node_id[39:])
                                    target_id = memory.node_id[:39] + random.choice(application_bootstrap_nodes_new_prefix)
                                    client.application_client_find_node_messages_recvfrom.put(
                                        ['application_bootstrap_nodes_find_node', target_id, ip_address, udp_port, application_bootstrap_nodes_keyword]
                                    )
                                    self.application_bootstrap_nodes_operators.put(
                                        ['append', [application_bootstrap_nodes_keyword, int(time.time())]]
                                    )

    def __send(self):
        while True:
            if len(self.application_bootstrap_nodes) > 0:
                for i in self.application_bootstrap_nodes:
                    application_bootstrap_nodes_keyword = os.urandom(20).hex()
                    ip_address = i[0]
                    udp_port = i[1]
                    ip_address_type = IPy.IP(ip_address).iptype()[:9]
                    if ip_address_type == 'ALLOCATED':
                        if 1 <= udp_port <= 65535:
                            client.application_client_ping_messages_recvfrom.put(
                                ['application_bootstrap_nodes_ping', ip_address, udp_port, application_bootstrap_nodes_keyword]
                            )
                            self.application_bootstrap_nodes_operators.put(
                                ['append', [application_bootstrap_nodes_keyword, int(time.time())]]
                            )
                            self.application_bootstrap_nodes.remove(i)
            time.sleep(5)

    def start(self):
        explorer_krpc_v6_application_bootstrap_nodes_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v6_application_bootstrap_nodes_check_thread.setDaemon(True)
        explorer_krpc_v6_application_bootstrap_nodes_check_thread.start()
        explorer_krpc_v6_application_bootstrap_nodes_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v6_application_bootstrap_nodes_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_bootstrap_nodes_operators_thread.start()
        explorer_krpc_v6_application_bootstrap_nodes_recvfrom_find_node_thread = threading.Thread(target = self.__recvfrom_find_node)
        explorer_krpc_v6_application_bootstrap_nodes_recvfrom_find_node_thread.setDaemon(True)
        explorer_krpc_v6_application_bootstrap_nodes_recvfrom_find_node_thread.start()
        explorer_krpc_v6_application_bootstrap_nodes_recvfrom_ping_thread = threading.Thread(target = self.__recvfrom_ping)
        explorer_krpc_v6_application_bootstrap_nodes_recvfrom_ping_thread.setDaemon(True)
        explorer_krpc_v6_application_bootstrap_nodes_recvfrom_ping_thread.start()
        explorer_krpc_v6_application_bootstrap_nodes_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v6_application_bootstrap_nodes_send_thread.setDaemon(True)
        explorer_krpc_v6_application_bootstrap_nodes_send_thread.start()