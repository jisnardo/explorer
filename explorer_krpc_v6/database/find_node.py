from ..application.client import client
from ..driver.memory import memory
import binascii
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

class find_node:
    database_find_node_key = []
    database_find_node_messages_recvfrom = queue.Queue()
    database_find_node_messages_send = queue.Queue()
    database_find_node_operators = queue.Queue()

    def __check(self):
        while True:
            if len(self.database_find_node_key) > 0:
                for i in self.database_find_node_key:
                    if i[2] < int(time.time()) - 300:
                        self.database_find_node_operators.put(
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
            database_find_node_operators = self.database_find_node_operators.get()
            operate = database_find_node_operators[0]
            element = database_find_node_operators[1]
            if operate == 'append':
                if element not in self.database_find_node_key:
                    self.database_find_node_key.append(element)
            if operate == 'remove':
                if element in self.database_find_node_key:
                    self.database_find_node_key.remove(element)

    def __recvfrom(self):
        while True:
            database_find_node_messages = client.application_client_find_node_messages_send_database_find_node.get()
            if database_find_node_messages[0] is False:
                database_find_node_keyword = database_find_node_messages[1]
                for i in self.database_find_node_key:
                    if i[0] == database_find_node_keyword:
                        distributed_hash_table_keyword = i[1]
                        self.database_find_node_messages_send.put(
                            [False, distributed_hash_table_keyword]
                        )
                        self.database_find_node_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = database_find_node_messages[0]
                nodes6 = database_find_node_messages[1]
                database_find_node_keyword = database_find_node_messages[7]
                for i in self.database_find_node_key:
                    if i[0] == database_find_node_keyword:
                        distributed_hash_table_keyword = i[1]
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
                        self.database_find_node_messages_send.put(
                            [node_id, new_nodes6, distributed_hash_table_keyword]
                        )
                        self.database_find_node_operators.put(
                            ['remove', i]
                        )

    def __send(self):
        while True:
            database_find_node_messages_recvfrom = self.database_find_node_messages_recvfrom.get()
            target_id = database_find_node_messages_recvfrom[0]
            ip_address = database_find_node_messages_recvfrom[1]
            udp_port = database_find_node_messages_recvfrom[2]
            distributed_hash_table_keyword = database_find_node_messages_recvfrom[3]
            database_find_node_keyword = os.urandom(20).hex()
            client.application_client_find_node_messages_recvfrom.put(
                ['database_find_node', target_id, ip_address, udp_port, database_find_node_keyword]
            )
            self.database_find_node_operators.put(
                ['append', [database_find_node_keyword, distributed_hash_table_keyword, int(time.time())]]
            )

    def start(self):
        explorer_krpc_v6_database_find_node_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v6_database_find_node_check_thread.setDaemon(True)
        explorer_krpc_v6_database_find_node_check_thread.start()
        explorer_krpc_v6_database_find_node_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v6_database_find_node_operators_thread.setDaemon(True)
        explorer_krpc_v6_database_find_node_operators_thread.start()
        explorer_krpc_v6_database_find_node_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v6_database_find_node_recvfrom_thread.setDaemon(True)
        explorer_krpc_v6_database_find_node_recvfrom_thread.start()
        explorer_krpc_v6_database_find_node_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v6_database_find_node_send_thread.setDaemon(True)
        explorer_krpc_v6_database_find_node_send_thread.start()