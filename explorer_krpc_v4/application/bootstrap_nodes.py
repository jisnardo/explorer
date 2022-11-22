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

    def __check_node(self, node_id, ip_address):
        pattern = re.compile(r'\b[0-9a-f]{40}\b')
        match = re.match(pattern, node_id.lower())
        if match is not None:
            ip_address_type = IPy.IP(ip_address).iptype()
            if ip_address_type == 'PUBLIC':
                check_data = match.group(0)[0:5]
                rand = int(match.group(0)[38:], 16)
                r = rand & 0x7
                network_byte_order_ip_address = socket.inet_pton(socket.AF_INET, ip_address)
                hexadecimal_ip_address = binascii.hexlify(network_byte_order_ip_address)
                decimal_ip_address = int(hexadecimal_ip_address, 16)
                binary_ip_address = bin(decimal_ip_address)
                decimal_ip_address = int(binary_ip_address, 2)
                decimal_number = (decimal_ip_address & 0x030f3fff) | (r << 29)
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
                nodes = application_client_find_node_messages_send_application_bootstrap_nodes_find_node[1]
                application_bootstrap_nodes_keyword = application_client_find_node_messages_send_application_bootstrap_nodes_find_node[7]
                for i in self.application_bootstrap_nodes_key:
                    if i[0] == application_bootstrap_nodes_keyword:
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
                            nodes_ip_address = j[1]
                            check_node_result = self.__check_node(nodes_node_id, nodes_ip_address)
                            if check_node_result is False:
                                if j in nodes:
                                    nodes.remove(j)
                        new_nodes = []
                        for j in nodes:
                            flag = False
                            for k in new_nodes:
                                if operator.eq(j, k) is True:
                                    flag = True
                            if flag is False:
                                new_nodes.append(j)
                        nodes = new_nodes
                        for j in nodes:
                            nodes_node_id = j[0]
                            distributed_hash_table.database_query_node_with_node_id_messages_recvfrom.put(
                                nodes_node_id
                            )
                            database_query_node_with_node_id_messages_send = distributed_hash_table.database_query_node_with_node_id_messages_send.get()
                            if database_query_node_with_node_id_messages_send is True:
                                if j in nodes:
                                    nodes.remove(j)
                        for j in nodes:
                            nodes_node_id = j[0]
                            nodes_ip_address = j[1]
                            nodes_udp_port = j[2]
                            distributed_hash_table.database_append_node_messages.put(
                                [nodes_node_id, nodes_ip_address, nodes_udp_port]
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
                            ip_address_type = IPy.IP(ip_address).iptype()
                            if ip_address_type == 'PUBLIC':
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
                    ip_address_type = IPy.IP(ip_address).iptype()
                    if ip_address_type == 'PUBLIC':
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
        explorer_krpc_v4_application_bootstrap_nodes_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v4_application_bootstrap_nodes_check_thread.setDaemon(True)
        explorer_krpc_v4_application_bootstrap_nodes_check_thread.start()
        explorer_krpc_v4_application_bootstrap_nodes_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v4_application_bootstrap_nodes_operators_thread.setDaemon(True)
        explorer_krpc_v4_application_bootstrap_nodes_operators_thread.start()
        explorer_krpc_v4_application_bootstrap_nodes_recvfrom_find_node_thread = threading.Thread(target = self.__recvfrom_find_node)
        explorer_krpc_v4_application_bootstrap_nodes_recvfrom_find_node_thread.setDaemon(True)
        explorer_krpc_v4_application_bootstrap_nodes_recvfrom_find_node_thread.start()
        explorer_krpc_v4_application_bootstrap_nodes_recvfrom_ping_thread = threading.Thread(target = self.__recvfrom_ping)
        explorer_krpc_v4_application_bootstrap_nodes_recvfrom_ping_thread.setDaemon(True)
        explorer_krpc_v4_application_bootstrap_nodes_recvfrom_ping_thread.start()
        explorer_krpc_v4_application_bootstrap_nodes_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v4_application_bootstrap_nodes_send_thread.setDaemon(True)
        explorer_krpc_v4_application_bootstrap_nodes_send_thread.start()