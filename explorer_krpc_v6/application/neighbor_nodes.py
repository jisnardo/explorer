from ..application.client import client
from ..database.distributed_hash_table import distributed_hash_table
from ..driver.memory import memory
import binascii
import copy
import crc32c
import IPy
import operator
import os
import queue
import random
import re
import socket
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

    def __check_node(self, node_id, ip_address):
        pattern = re.compile(r'\b[0-9a-f]{40}\b')
        match = re.match(pattern, node_id.lower())
        if match is not None:
            ip_address_type = IPy.IP(ip_address).iptype()[:9]
            if ip_address_type == 'ALLOCATED':
                check_data = match.group(0)[0:5]
                rand = int(match.group(0)[38:], 16)
                r = rand & 0x7
                network_byte_order_ip_address = socket.inet_pton(socket.AF_INET6, ip_address)
                hexadecimal_ip_address = binascii.hexlify(network_byte_order_ip_address)
                decimal_ip_address = int(hexadecimal_ip_address, 16)
                binary_ip_address = bin(decimal_ip_address)
                binary_ip_address = binary_ip_address[0:64]
                decimal_ip_address = int(binary_ip_address, 2)
                decimal_number = (decimal_ip_address & 0x0103070f1f3f7fff) | (r << 61)
                hexadecimal_number = hex(decimal_number).replace('0x', '').encode('ascii')
                if (len(hexadecimal_number) % 2) == 0:
                    network_byte_order_number = binascii.unhexlify(hexadecimal_number)
                    crc = crc32c.crc32c(network_byte_order_number)
                    calculation_data = ''
                    calculation_data = calculation_data + hex((crc >> 24) & 0xff).replace('0x', '').zfill(2)
                    calculation_data = calculation_data + hex((crc >> 16) & 0xff).replace('0x', '').zfill(2)
                    calculation_data = calculation_data + hex(((crc >> 8) & 0xf8) | (random.randint(0, 255) & 0x7)).replace('0x', '').zfill(2)
                    if check_data == calculation_data[0:5]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

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
                        distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                            [last_query_ip_address, last_query_udp_port]
                        )
                        self.application_neighbor_nodes_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = application_client_find_node_messages_send_application_neighbor_nodes_find_node[0]
                nodes6 = application_client_find_node_messages_send_application_neighbor_nodes_find_node[1]
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
                                    nodes_node_id = j[0]
                                    nodes_ip_address = j[1]
                                    check_node_result = self.__check_node(nodes_node_id, nodes_ip_address)
                                    if check_node_result is False:
                                        if j in nodes6:
                                            nodes6.remove(j)
                                new_nodes6 = []
                                for j in nodes6:
                                    flag = False
                                    for k in new_nodes6:
                                        if operator.eq(j, k) is True:
                                            flag = True
                                    if flag is False:
                                        new_nodes6.append(j)
                                nodes6 = new_nodes6
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
                            else:
                                distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                                    [ip_address, udp_port]
                                )
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
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
                        else:
                            distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                                [ip_address, udp_port]
                            )
                            distributed_hash_table.database_delete_node_with_ip_address_messages.put(
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
                nodes6 = distributed_hash_table.database_query_nodes_messages_send.get()
                if not len(nodes6) == 0:
                    nodes6_distance = []
                    for i in nodes6:
                        nodes6_node_id = i[0]
                        nodes6_distance.append(int(target_id, 16) ^ int(nodes6_node_id, 16))
                    nodes6_distance.sort()
                    for i in nodes6:
                        nodes6_node_id = i[0]
                        nodes6_ip_address = i[1]
                        nodes6_udp_port = i[2]
                        if nodes6_distance[0] == int(target_id, 16) ^ int(nodes6_node_id, 16):
                            application_neighbor_nodes_keyword = os.urandom(20).hex()
                            client.application_client_find_node_messages_recvfrom.put(
                                ['application_neighbor_nodes_find_node', target_id, nodes6_ip_address, nodes6_udp_port, application_neighbor_nodes_keyword]
                            )
                            self.application_neighbor_nodes_operators.put(
                                ['append', [application_neighbor_nodes_keyword, nodes6_node_id, nodes6_ip_address, nodes6_udp_port, int(time.time())]]
                            )
            time.sleep(15)

    def start(self):
        explorer_krpc_v6_application_neighbor_nodes_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v6_application_neighbor_nodes_check_thread.setDaemon(True)
        explorer_krpc_v6_application_neighbor_nodes_check_thread.start()
        explorer_krpc_v6_application_neighbor_nodes_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v6_application_neighbor_nodes_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_neighbor_nodes_operators_thread.start()
        explorer_krpc_v6_application_neighbor_nodes_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v6_application_neighbor_nodes_recvfrom_thread.setDaemon(True)
        explorer_krpc_v6_application_neighbor_nodes_recvfrom_thread.start()
        explorer_krpc_v6_application_neighbor_nodes_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v6_application_neighbor_nodes_send_thread.setDaemon(True)
        explorer_krpc_v6_application_neighbor_nodes_send_thread.start()