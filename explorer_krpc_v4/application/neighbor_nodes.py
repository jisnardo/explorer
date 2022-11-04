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

class neighbor_nodes:
    application_neighbor_nodes_key = []
    application_neighbor_nodes_operators = queue.Queue()
    application_neighbor_nodes_prefix = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    def __check(self):
        while True:
            if len(self.application_neighbor_nodes_key) > 0:
                for i in self.application_neighbor_nodes_key:
                    if i[4] < int(time.time()) - 300:
                        self.application_neighbor_nodes_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __operators(self):
        while True:
            application_neighbor_nodes_operators = self.application_neighbor_nodes_operators.get()
            operate = application_neighbor_nodes_operators[0]
            element = application_neighbor_nodes_operators[1]
            if operate == 'append':
                if element not in self.application_neighbor_nodes_key:
                    self.application_neighbor_nodes_key.append(element)
            if operate == 'remove':
                if element in self.application_neighbor_nodes_key:
                    self.application_neighbor_nodes_key.remove(element)

    def __recvfrom(self):
        while True:
            application_client_find_node_messages_send_application_neighbor_nodes_find_node = client.application_client_find_node_messages_send_application_neighbor_nodes_find_node.get()
            if application_client_find_node_messages_send_application_neighbor_nodes_find_node[0] is False:
                application_neighbor_nodes_keyword = application_client_find_node_messages_send_application_neighbor_nodes_find_node[1]
                for i in self.application_neighbor_nodes_key:
                    if i[0] == application_neighbor_nodes_keyword:
                        last_query_ip_address = i[2]
                        last_query_udp_port = i[3]
                        distributed_hash_table.database_delete_node_messages.put(
                            [last_query_ip_address, last_query_udp_port]
                        )
                        self.application_neighbor_nodes_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = application_client_find_node_messages_send_application_neighbor_nodes_find_node[0]
                nodes = application_client_find_node_messages_send_application_neighbor_nodes_find_node[1]
                ip_address = application_client_find_node_messages_send_application_neighbor_nodes_find_node[5]
                udp_port = application_client_find_node_messages_send_application_neighbor_nodes_find_node[6]
                application_neighbor_nodes_keyword = application_client_find_node_messages_send_application_neighbor_nodes_find_node[7]
                for i in self.application_neighbor_nodes_key:
                    if i[0] == application_neighbor_nodes_keyword:
                        last_query_node_id = i[1]
                        last_query_ip_address = i[2]
                        last_query_udp_port = i[3]
                        self.application_neighbor_nodes_operators.put(
                            ['remove', i]
                        )
                        if last_query_ip_address == ip_address and last_query_udp_port == udp_port:
                            if last_query_node_id == node_id:
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                                for j in nodes:
                                    nodes_node_id = j[0]
                                    pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                    match = re.match(pattern, nodes_node_id.lower())
                                    if match is None:
                                        if j in nodes:
                                            nodes.remove(j)
                                    elif match.group(0) == memory.node_id:
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_ip_address = j[1]
                                    ip_address_type = IPy.IP(nodes_ip_address).iptype()
                                    if ip_address_type == 'PRIVATE':
                                        if j in nodes:
                                            nodes.remove(j)
                                    if ip_address_type == 'LOOPBACK':
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_udp_port = j[2]
                                    if not 1 <= nodes_udp_port <= 65535:
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_node_id = j[0]
                                    distributed_hash_table.database_query_node_messages_recvfrom.put(
                                        nodes_node_id
                                    )
                                    database_query_node_messages_send = distributed_hash_table.database_query_node_messages_send.get()
                                    if database_query_node_messages_send is True:
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_node_id = j[0]
                                    nodes_ip_address = j[1]
                                    nodes_udp_port = j[2]
                                    distributed_hash_table.database_append_node_messages.put(
                                        [nodes_node_id, nodes_ip_address, nodes_udp_port]
                                    )
                            else:
                                distributed_hash_table.database_delete_node_messages.put(
                                    [ip_address, udp_port]
                                )
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                                for j in nodes:
                                    nodes_node_id = j[0]
                                    pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                    match = re.match(pattern, nodes_node_id.lower())
                                    if match is None:
                                        if j in nodes:
                                            nodes.remove(j)
                                    elif match.group(0) == memory.node_id:
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_ip_address = j[1]
                                    ip_address_type = IPy.IP(nodes_ip_address).iptype()
                                    if ip_address_type == 'PRIVATE':
                                        if j in nodes:
                                            nodes.remove(j)
                                    if ip_address_type == 'LOOPBACK':
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_udp_port = j[2]
                                    if not 1 <= nodes_udp_port <= 65535:
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_node_id = j[0]
                                    distributed_hash_table.database_query_node_messages_recvfrom.put(
                                        nodes_node_id
                                    )
                                    database_query_node_messages_send = distributed_hash_table.database_query_node_messages_send.get()
                                    if database_query_node_messages_send is True:
                                        if j in nodes:
                                            nodes.remove(j)
                                for j in nodes:
                                    nodes_node_id = j[0]
                                    nodes_ip_address = j[1]
                                    nodes_udp_port = j[2]
                                    distributed_hash_table.database_append_node_messages.put(
                                        [nodes_node_id, nodes_ip_address, nodes_udp_port]
                                    )
                        else:
                            distributed_hash_table.database_delete_node_messages.put(
                                [ip_address, udp_port]
                            )
                            distributed_hash_table.database_delete_node_messages.put(
                                [last_query_ip_address, last_query_udp_port]
                            )

    def __send(self):
        while True:
            distributed_hash_table.database_query_nodes_number_messages_recvfrom.put(
                0
            )
            nodes_number = distributed_hash_table.database_query_nodes_number_messages_send.get()
            if nodes_number < 1280:
                application_neighbor_nodes_new_prefix = copy.deepcopy(self.application_neighbor_nodes_prefix)
                application_neighbor_nodes_new_prefix.remove(memory.node_id[39:])
                target_id = memory.node_id[:39] + random.choice(application_neighbor_nodes_new_prefix)
                distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                    target_id
                )
                nodes = distributed_hash_table.database_query_nodes_messages_send.get()
                if not len(nodes) == 0:
                    nodes_distance = []
                    for i in nodes:
                        nodes_node_id = i[0]
                        nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                    nodes_distance.sort()
                    for i in nodes:
                        nodes_node_id = i[0]
                        nodes_ip_address = i[1]
                        nodes_udp_port = i[2]
                        if nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            application_neighbor_nodes_keyword = os.urandom(20).hex()
                            client.application_client_find_node_messages_recvfrom.put(
                                ['application_neighbor_nodes_find_node', target_id, nodes_ip_address, nodes_udp_port, application_neighbor_nodes_keyword]
                            )
                            self.application_neighbor_nodes_operators.put(
                                ['append', [application_neighbor_nodes_keyword, nodes_node_id, nodes_ip_address, nodes_udp_port, int(time.time())]]
                            )
            time.sleep(15)

    def start(self):
        explorer_krpc_v4_application_neighbor_nodes_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v4_application_neighbor_nodes_check_thread.setDaemon(True)
        explorer_krpc_v4_application_neighbor_nodes_check_thread.start()
        explorer_krpc_v4_application_neighbor_nodes_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v4_application_neighbor_nodes_operators_thread.setDaemon(True)
        explorer_krpc_v4_application_neighbor_nodes_operators_thread.start()
        explorer_krpc_v4_application_neighbor_nodes_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_application_neighbor_nodes_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_application_neighbor_nodes_recvfrom_thread.start()
        explorer_krpc_v4_application_neighbor_nodes_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v4_application_neighbor_nodes_send_thread.setDaemon(True)
        explorer_krpc_v4_application_neighbor_nodes_send_thread.start()