from ...application.client import client
from ...database.distributed_hash_table import distributed_hash_table
from ...database.token_manager import token_manager
from ...driver.memory import memory
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

class get_peers:
    application_command_get_peers_key = []
    application_command_get_peers_messages_recvfrom = queue.Queue()
    application_command_get_peers_messages_send = queue.Queue()
    application_command_get_peers_operators = queue.Queue()

    def __check(self):
        while True:
            if len(self.application_command_get_peers_key) > 0:
                for i in self.application_command_get_peers_key:
                    if i[9] < int(time.time()) - 300:
                        self.application_command_get_peers_operators.put(
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
            application_command_get_peers_operators = self.application_command_get_peers_operators.get()
            operate = application_command_get_peers_operators[0]
            element = application_command_get_peers_operators[1]
            if operate == 'append':
                if element not in self.application_command_get_peers_key:
                    self.application_command_get_peers_key.append(element)
            if operate == 'remove':
                if element in self.application_command_get_peers_key:
                    self.application_command_get_peers_key.remove(element)

    def __recvfrom(self):
        while True:
            application_client_get_peers_messages_send_application_command_get_peers = client.application_client_get_peers_messages_send_application_command_get_peers.get()
            if application_client_get_peers_messages_send_application_command_get_peers[0] is False:
                application_command_get_peers_keyword = application_client_get_peers_messages_send_application_command_get_peers[1]
                for i in self.application_command_get_peers_key:
                    if i[0] == application_command_get_peers_keyword:
                        info_hash = i[1]
                        last_query_nodes = i[5]
                        response_nodes = i[6]
                        response_values = i[7]
                        application_command_commander_keyword = i[8]
                        self.application_command_get_peers_operators.put(
                            ['remove', i]
                        )
                        if len(response_nodes) > 0:
                            ip_address = response_nodes[-1][1]
                            udp_port = response_nodes[-1][2]
                            distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                                [ip_address, udp_port]
                            )
                        for j in last_query_nodes:
                            nodes_node_id = j[0]
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, nodes_node_id.lower())
                            if match is None:
                                if j in last_query_nodes:
                                    last_query_nodes.remove(j)
                            elif match.group(0) == memory.node_id:
                                if j in last_query_nodes:
                                    last_query_nodes.remove(j)
                        for j in last_query_nodes:
                            nodes_ip_address = j[1]
                            ip_address_type = IPy.IP(nodes_ip_address).iptype()
                            if ip_address_type == 'PRIVATE':
                                if j in last_query_nodes:
                                    last_query_nodes.remove(j)
                            if ip_address_type == 'LOOPBACK':
                                if j in last_query_nodes:
                                    last_query_nodes.remove(j)
                        for j in last_query_nodes:
                            nodes_udp_port = j[2]
                            if not 1 <= nodes_udp_port <= 65535:
                                if j in last_query_nodes:
                                    last_query_nodes.remove(j)
                        for j in last_query_nodes:
                            nodes_node_id = j[0]
                            nodes_ip_address = j[1]
                            check_node_result = self.__check_node(nodes_node_id, nodes_ip_address)
                            if check_node_result is False:
                                if j in last_query_nodes:
                                    last_query_nodes.remove(j)
                        new_nodes = []
                        for j in last_query_nodes:
                            flag = False
                            for k in new_nodes:
                                if operator.eq(j, k) is True:
                                    flag = True
                            if flag is False:
                                new_nodes.append(j)
                        last_query_nodes = new_nodes
                        if len(last_query_nodes) == 0:
                            result = {
                                'result': response_values,
                                'header': {
                                    'info_hash': info_hash
                                }
                            }
                            self.application_command_get_peers_messages_send.put(
                                [result, application_command_commander_keyword]
                            )
                        else:
                            nodes_distance = []
                            for j in last_query_nodes:
                                nodes_node_id = j[0]
                                nodes_distance.append(int(info_hash, 16) ^ int(nodes_node_id, 16))
                            nodes_distance.sort()
                            for j in last_query_nodes:
                                nodes_node_id = j[0]
                                nodes_ip_address = j[1]
                                nodes_udp_port = j[2]
                                if nodes_distance[0] == int(info_hash, 16) ^ int(nodes_node_id, 16):
                                    application_command_get_peers_keyword = os.urandom(20).hex()
                                    last_query_nodes.remove(j)
                                    response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                    client.application_client_get_peers_messages_recvfrom.put(
                                        ['application_command_get_peers', info_hash, nodes_ip_address, nodes_udp_port, application_command_get_peers_keyword]
                                    )
                                    self.application_command_get_peers_operators.put(
                                        ['append', [application_command_get_peers_keyword, info_hash, nodes_node_id, nodes_ip_address, nodes_udp_port, last_query_nodes, response_nodes, response_values, application_command_commander_keyword, int(time.time())]]
                                    )
            else:
                node_id = application_client_get_peers_messages_send_application_command_get_peers[0]
                nodes = application_client_get_peers_messages_send_application_command_get_peers[1]
                values = application_client_get_peers_messages_send_application_command_get_peers[2]
                token = application_client_get_peers_messages_send_application_command_get_peers[4]
                ip_address = application_client_get_peers_messages_send_application_command_get_peers[5]
                udp_port = application_client_get_peers_messages_send_application_command_get_peers[6]
                application_command_get_peers_keyword = application_client_get_peers_messages_send_application_command_get_peers[7]
                for i in self.application_command_get_peers_key:
                    if i[0] == application_command_get_peers_keyword:
                        info_hash = i[1]
                        last_query_node_id = i[2]
                        last_query_ip_address = i[3]
                        last_query_udp_port = i[4]
                        last_query_nodes = i[5]
                        response_nodes = i[6]
                        response_values = i[7]
                        application_command_commander_keyword = i[8]
                        self.application_command_get_peers_operators.put(
                            ['remove', i]
                        )
                        if last_query_ip_address == ip_address and last_query_udp_port == udp_port:
                            if last_query_node_id == node_id:
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                                if len(token) == 4:
                                    token_manager.database_append_token_messages.put(
                                        [node_id, ip_address, udp_port, token]
                                    )
                                distance = int(info_hash, 16) ^ int(node_id, 16)
                                if len(values) > 0:
                                    for j in values:
                                        for k in response_values:
                                            if operator.eq(j, k) is True:
                                                if j in values:
                                                    values.remove(j)
                                if len(values) > 0:
                                    for j in values:
                                        values_ip_address = j[0]
                                        values_tcp_port = j[1]
                                        ip_address_type = IPy.IP(values_ip_address).iptype()
                                        if ip_address_type == 'PUBLIC':
                                            if 1 <= values_tcp_port <= 65535:
                                                response_values.append(j)
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
                                    for k in response_nodes:
                                        response_node_id = k[0]
                                        if nodes_node_id == response_node_id:
                                            if j in nodes:
                                                nodes.remove(j)
                                if len(nodes) == 0:
                                    result = {
                                        'result': response_values,
                                        'header': {
                                            'info_hash': info_hash
                                        }
                                    }
                                    self.application_command_get_peers_messages_send.put(
                                        [result, application_command_get_peers_keyword]
                                    )
                                else:
                                    nodes_distance = []
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_distance.append(int(info_hash, 16) ^ int(nodes_node_id, 16))
                                    nodes_distance.sort()
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_ip_address = j[1]
                                        nodes_udp_port = j[2]
                                        if nodes_distance[0] == int(info_hash, 16) ^ int(nodes_node_id, 16):
                                            if distance > nodes_distance[0]:
                                                application_command_get_peers_keyword = os.urandom(20).hex()
                                                nodes.remove(j)
                                                response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                                client.application_client_get_peers_messages_recvfrom.put(
                                                    ['application_command_get_peers', info_hash, nodes_ip_address, nodes_udp_port, application_command_get_peers_keyword]
                                                )
                                                self.application_command_get_peers_operators.put(
                                                    ['append', [application_command_get_peers_keyword, info_hash, nodes_node_id, nodes_ip_address, nodes_udp_port, nodes, response_nodes, response_values, application_command_commander_keyword, int(time.time())]]
                                                )
                                            else:
                                                result = {
                                                    'result': response_values,
                                                    'header': {
                                                        'info_hash': info_hash
                                                    }
                                                }
                                                self.application_command_get_peers_messages_send.put(
                                                    [result, application_command_commander_keyword]
                                                )
                            else:
                                distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                                    [ip_address, udp_port]
                                )
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                                if len(token) == 4:
                                    token_manager.database_append_token_messages.put(
                                        [node_id, ip_address, udp_port, token]
                                    )
                                distance = int(info_hash, 16) ^ int(node_id, 16)
                                if len(values) > 0:
                                    for j in values:
                                        for k in response_values:
                                            if operator.eq(j, k) is True:
                                                if j in values:
                                                    values.remove(j)
                                if len(values) > 0:
                                    for j in values:
                                        values_ip_address = j[0]
                                        values_tcp_port = j[1]
                                        ip_address_type = IPy.IP(values_ip_address).iptype()
                                        if ip_address_type == 'PUBLIC':
                                            if 1 <= values_tcp_port <= 65535:
                                                response_values.append(j)
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
                                    for k in response_nodes:
                                        response_node_id = k[0]
                                        if nodes_node_id == response_node_id:
                                            if j in nodes:
                                                nodes.remove(j)
                                if len(nodes) == 0:
                                    result = {
                                        'result': response_values,
                                        'header': {
                                            'info_hash': info_hash
                                        }
                                    }
                                    self.application_command_get_peers_messages_send.put(
                                        [result, application_command_get_peers_keyword]
                                    )
                                else:
                                    nodes_distance = []
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_distance.append(int(info_hash, 16) ^ int(nodes_node_id, 16))
                                    nodes_distance.sort()
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_ip_address = j[1]
                                        nodes_udp_port = j[2]
                                        if nodes_distance[0] == int(info_hash, 16) ^ int(nodes_node_id, 16):
                                            if distance > nodes_distance[0]:
                                                application_command_get_peers_keyword = os.urandom(20).hex()
                                                nodes.remove(j)
                                                response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                                client.application_client_get_peers_messages_recvfrom.put(
                                                    ['application_command_get_peers', info_hash, nodes_ip_address, nodes_udp_port, application_command_get_peers_keyword]
                                                )
                                                self.application_command_get_peers_operators.put(
                                                    ['append', [application_command_get_peers_keyword, info_hash, nodes_node_id, nodes_ip_address, nodes_udp_port, nodes, response_nodes, response_values, application_command_commander_keyword, int(time.time())]]
                                                )
                                            else:
                                                result = {
                                                    'result': response_values,
                                                    'header': {
                                                        'info_hash': info_hash
                                                    }
                                                }
                                                self.application_command_get_peers_messages_send.put(
                                                    [result, application_command_commander_keyword]
                                                )
                        else:
                            distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                                [ip_address, udp_port]
                            )
                            distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                                [last_query_ip_address, last_query_udp_port]
                            )
                            if len(response_nodes) > 0:
                                ip_address = response_nodes[-1][1]
                                udp_port = response_nodes[-1][2]
                                distributed_hash_table.database_delete_node_with_ip_address_messages.put(
                                    [ip_address, udp_port]
                                )
                            for j in last_query_nodes:
                                nodes_node_id = j[0]
                                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                match = re.match(pattern, nodes_node_id.lower())
                                if match is None:
                                    if j in last_query_nodes:
                                        last_query_nodes.remove(j)
                                elif match.group(0) == memory.node_id:
                                    if j in last_query_nodes:
                                        last_query_nodes.remove(j)
                            for j in last_query_nodes:
                                nodes_ip_address = j[1]
                                ip_address_type = IPy.IP(nodes_ip_address).iptype()
                                if ip_address_type == 'PRIVATE':
                                    if j in last_query_nodes:
                                        last_query_nodes.remove(j)
                                if ip_address_type == 'LOOPBACK':
                                    if j in last_query_nodes:
                                        last_query_nodes.remove(j)
                            for j in last_query_nodes:
                                nodes_udp_port = j[2]
                                if not 1 <= nodes_udp_port <= 65535:
                                    if j in last_query_nodes:
                                        last_query_nodes.remove(j)
                            for j in last_query_nodes:
                                nodes_node_id = j[0]
                                nodes_ip_address = j[1]
                                check_node_result = self.__check_node(nodes_node_id, nodes_ip_address)
                                if check_node_result is False:
                                    if j in last_query_nodes:
                                        last_query_nodes.remove(j)
                            new_nodes = []
                            for j in last_query_nodes:
                                flag = False
                                for k in new_nodes:
                                    if operator.eq(j, k) is True:
                                        flag = True
                                if flag is False:
                                    new_nodes.append(j)
                            last_query_nodes = new_nodes
                            if len(last_query_nodes) == 0:
                                result = {
                                    'result': response_values,
                                    'header': {
                                        'info_hash': info_hash
                                    }
                                }
                                self.application_command_get_peers_messages_send.put(
                                    [result, application_command_commander_keyword]
                                )
                            else:
                                nodes_distance = []
                                for j in last_query_nodes:
                                    nodes_node_id = j[0]
                                    nodes_distance.append(int(info_hash, 16) ^ int(nodes_node_id, 16))
                                nodes_distance.sort()
                                for j in last_query_nodes:
                                    nodes_node_id = j[0]
                                    nodes_ip_address = j[1]
                                    nodes_udp_port = j[2]
                                    if nodes_distance[0] == int(info_hash, 16) ^ int(nodes_node_id, 16):
                                        application_command_get_peers_keyword = os.urandom(20).hex()
                                        last_query_nodes.remove(j)
                                        response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                        client.application_client_get_peers_messages_recvfrom.put(
                                            ['application_command_get_peers', info_hash, nodes_ip_address, nodes_udp_port, application_command_get_peers_keyword]
                                        )
                                        self.application_command_get_peers_operators.put(
                                            ['append', [application_command_get_peers_keyword, info_hash, nodes_node_id, nodes_ip_address, nodes_udp_port, last_query_nodes, response_nodes, response_values, application_command_commander_keyword, int(time.time())]]
                                        )

    def __send(self):
        while True:
            application_command_get_peers_messages_recvfrom = self.application_command_get_peers_messages_recvfrom.get()
            info_hash = application_command_get_peers_messages_recvfrom[0]
            application_command_commander_keyword = application_command_get_peers_messages_recvfrom[1]
            distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                info_hash
            )
            nodes = distributed_hash_table.database_query_nodes_messages_send.get()
            if len(nodes) == 0:
                result = {
                    'result': [],
                    'header': {
                        'info_hash': info_hash
                    }
                }
                self.application_command_get_peers_messages_send.put(
                    [result, application_command_commander_keyword]
                )
            else:
                nodes_distance = []
                for i in nodes:
                    nodes_node_id = i[0]
                    nodes_distance.append(int(info_hash, 16) ^ int(nodes_node_id, 16))
                nodes_distance.sort()
                for i in nodes:
                    nodes_node_id = i[0]
                    nodes_ip_address = i[1]
                    nodes_udp_port = i[2]
                    if nodes_distance[0] == int(info_hash, 16) ^ int(nodes_node_id, 16):
                        application_command_get_peers_keyword = os.urandom(20).hex()
                        nodes.remove(i)
                        response_nodes = []
                        response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        response_values = []
                        client.application_client_get_peers_messages_recvfrom.put(
                            ['application_command_get_peers', info_hash, nodes_ip_address, nodes_udp_port, application_command_get_peers_keyword]
                        )
                        self.application_command_get_peers_operators.put(
                            ['append', [application_command_get_peers_keyword, info_hash, nodes_node_id, nodes_ip_address, nodes_udp_port, nodes, response_nodes, response_values, application_command_commander_keyword, int(time.time())]]
                        )

    def start(self):
        explorer_krpc_v4_application_command_get_peers_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v4_application_command_get_peers_check_thread.setDaemon(True)
        explorer_krpc_v4_application_command_get_peers_check_thread.start()
        explorer_krpc_v4_application_command_get_peers_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v4_application_command_get_peers_operators_thread.setDaemon(True)
        explorer_krpc_v4_application_command_get_peers_operators_thread.start()
        explorer_krpc_v4_application_command_get_peers_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_application_command_get_peers_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_application_command_get_peers_recvfrom_thread.start()
        explorer_krpc_v4_application_command_get_peers_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v4_application_command_get_peers_send_thread.setDaemon(True)
        explorer_krpc_v4_application_command_get_peers_send_thread.start()