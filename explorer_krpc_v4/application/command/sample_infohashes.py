from ...application.client import client
from ...database.distributed_hash_table import distributed_hash_table
from ...driver.memory import memory
import IPy
import os
import queue
import re
import threading
import time

class sample_infohashes:
    application_command_sample_infohashes_key = []
    application_command_sample_infohashes_messages_recvfrom = queue.Queue()
    application_command_sample_infohashes_messages_send = queue.Queue()
    application_command_sample_infohashes_operators = queue.Queue()

    def __check(self):
        while True:
            if len(self.application_command_sample_infohashes_key) > 0:
                for i in self.application_command_sample_infohashes_key:
                    if i[9] < int(time.time()) - 300:
                        self.application_command_sample_infohashes_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __operators(self):
        while True:
            application_command_sample_infohashes_operators = self.application_command_sample_infohashes_operators.get()
            operate = application_command_sample_infohashes_operators[0]
            element = application_command_sample_infohashes_operators[1]
            if operate == 'append':
                if element not in self.application_command_sample_infohashes_key:
                    self.application_command_sample_infohashes_key.append(element)
            if operate == 'remove':
                if element in self.application_command_sample_infohashes_key:
                    self.application_command_sample_infohashes_key.remove(element)

    def __recvfrom(self):
        while True:
            application_client_sample_infohashes_messages_send_application_command_sample_infohashes = client.application_client_sample_infohashes_messages_send_application_command_sample_infohashes.get()
            if application_client_sample_infohashes_messages_send_application_command_sample_infohashes[0] is False:
                application_command_sample_infohashes_keyword = application_client_sample_infohashes_messages_send_application_command_sample_infohashes[1]
                for i in self.application_command_sample_infohashes_key:
                    if i[0] == application_command_sample_infohashes_keyword:
                        target_id = i[1]
                        last_query_nodes = i[5]
                        response_nodes = i[6]
                        response_samples = i[7]
                        application_command_commander_keyword = i[8]
                        self.application_command_sample_infohashes_operators.put(
                            ['remove', i]
                        )
                        if len(response_nodes) > 0:
                            ip_address = response_nodes[-1][1]
                            udp_port = response_nodes[-1][2]
                            distributed_hash_table.database_delete_node_messages.put(
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
                        if len(last_query_nodes) == 0:
                            result = {
                                'result': response_samples,
                                'header': {
                                    'target_id': target_id
                                }
                            }
                            self.application_command_sample_infohashes_messages_send.put(
                                [result, application_command_commander_keyword]
                            )
                        else:
                            nodes_distance = []
                            for j in last_query_nodes:
                                nodes_node_id = j[0]
                                nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                            nodes_distance.sort()
                            for j in last_query_nodes:
                                nodes_node_id = j[0]
                                nodes_ip_address = j[1]
                                nodes_udp_port = j[2]
                                if nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                    application_command_sample_infohashes_keyword = os.urandom(20).hex()
                                    last_query_nodes.remove(j)
                                    response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                    client.application_client_sample_infohashes_messages_recvfrom.put(
                                        ['application_command_sample_infohashes', target_id, nodes_ip_address, nodes_udp_port, application_command_sample_infohashes_keyword]
                                    )
                                    self.application_command_sample_infohashes_operators.put(
                                        ['append', [application_command_sample_infohashes_keyword, target_id, nodes_node_id, nodes_ip_address, nodes_udp_port, last_query_nodes, response_nodes, response_samples, application_command_commander_keyword, int(time.time())]]
                                    )
            else:
                node_id = application_client_sample_infohashes_messages_send_application_command_sample_infohashes[0]
                nodes = application_client_sample_infohashes_messages_send_application_command_sample_infohashes[1]
                samples = application_client_sample_infohashes_messages_send_application_command_sample_infohashes[3]
                ip_address = application_client_sample_infohashes_messages_send_application_command_sample_infohashes[5]
                udp_port = application_client_sample_infohashes_messages_send_application_command_sample_infohashes[6]
                application_command_sample_infohashes_keyword = application_client_sample_infohashes_messages_send_application_command_sample_infohashes[7]
                for i in self.application_command_sample_infohashes_key:
                    if i[0] == application_command_sample_infohashes_keyword:
                        target_id = i[1]
                        last_query_node_id = i[2]
                        last_query_ip_address = i[3]
                        last_query_udp_port = i[4]
                        last_query_nodes = i[5]
                        response_nodes = i[6]
                        response_samples = i[7]
                        application_command_commander_keyword = i[8]
                        self.application_command_sample_infohashes_operators.put(
                            ['remove', i]
                        )
                        if last_query_ip_address == ip_address and last_query_udp_port == udp_port:
                            if last_query_node_id == node_id:
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                                distance = int(target_id, 16) ^ int(node_id, 16)
                                if len(samples) > 0:
                                    for j in samples:
                                        for k in response_samples:
                                            if j == k:
                                                if j in samples:
                                                    samples.remove(j)
                                if len(samples) > 0:
                                    for j in samples:
                                        pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                        match = re.match(pattern, j.lower())
                                        if match is None:
                                            if j in samples:
                                                samples.remove(j)
                                if len(samples) > 0:
                                    for j in samples:
                                        response_samples.append(j)
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
                                    for k in response_nodes:
                                        response_node_id = k[0]
                                        if nodes_node_id == response_node_id:
                                            if j in nodes:
                                                nodes.remove(j)
                                if len(nodes) == 0:
                                    result = {
                                        'result': response_samples,
                                        'header': {
                                            'target_id': target_id
                                        }
                                    }
                                    self.application_command_sample_infohashes_messages_send.put(
                                        [result, application_command_commander_keyword]
                                    )
                                else:
                                    nodes_distance = []
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                                    nodes_distance.sort()
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_ip_address = j[1]
                                        nodes_udp_port = j[2]
                                        if nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                            if distance > nodes_distance[0]:
                                                application_command_sample_infohashes_keyword = os.urandom(20).hex()
                                                nodes.remove(j)
                                                response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                                client.application_client_sample_infohashes_messages_recvfrom.put(
                                                    ['application_command_sample_infohashes', target_id, nodes_ip_address, nodes_udp_port, application_command_sample_infohashes_keyword]
                                                )
                                                self.application_command_sample_infohashes_operators.put(
                                                    ['append', [application_command_sample_infohashes_keyword, target_id, nodes_node_id, nodes_ip_address, nodes_udp_port, nodes, response_nodes, response_samples, application_command_commander_keyword, int(time.time())]]
                                                )
                                            else:
                                                result = {
                                                    'result': response_samples,
                                                    'header': {
                                                        'target_id': target_id
                                                    }
                                                }
                                                self.application_command_sample_infohashes_messages_send.put(
                                                    [result, application_command_commander_keyword]
                                                )
                            else:
                                distributed_hash_table.database_delete_node_messages.put(
                                    [ip_address, udp_port]
                                )
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                                distance = int(target_id, 16) ^ int(node_id, 16)
                                if len(samples) > 0:
                                    for j in samples:
                                        for k in response_samples:
                                            if j == k:
                                                if j in samples:
                                                    samples.remove(j)
                                if len(samples) > 0:
                                    for j in samples:
                                        pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                        match = re.match(pattern, j.lower())
                                        if match is None:
                                            if j in samples:
                                                samples.remove(j)
                                if len(samples) > 0:
                                    for j in samples:
                                        response_samples.append(j)
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
                                    for k in response_nodes:
                                        response_node_id = k[0]
                                        if nodes_node_id == response_node_id:
                                            if j in nodes:
                                                nodes.remove(j)
                                if len(nodes) == 0:
                                    result = {
                                        'result': response_samples,
                                        'header': {
                                            'target_id': target_id
                                        }
                                    }
                                    self.application_command_sample_infohashes_messages_send.put(
                                        [result, application_command_commander_keyword]
                                    )
                                else:
                                    nodes_distance = []
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                                    nodes_distance.sort()
                                    for j in nodes:
                                        nodes_node_id = j[0]
                                        nodes_ip_address = j[1]
                                        nodes_udp_port = j[2]
                                        if nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                            if distance > nodes_distance[0]:
                                                application_command_sample_infohashes_keyword = os.urandom(20).hex()
                                                nodes.remove(j)
                                                response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                                client.application_client_sample_infohashes_messages_recvfrom.put(
                                                    ['application_command_sample_infohashes', target_id, nodes_ip_address, nodes_udp_port, application_command_sample_infohashes_keyword]
                                                )
                                                self.application_command_sample_infohashes_operators.put(
                                                    ['append', [application_command_sample_infohashes_keyword, target_id, nodes_node_id, nodes_ip_address, nodes_udp_port, nodes, response_nodes, response_samples, application_command_commander_keyword, int(time.time())]]
                                                )
                                            else:
                                                result = {
                                                    'result': response_samples,
                                                    'header': {
                                                        'target_id': target_id
                                                    }
                                                }
                                                self.application_command_sample_infohashes_messages_send.put(
                                                    [result, application_command_commander_keyword]
                                                )
                        else:
                            distributed_hash_table.database_delete_node_messages.put(
                                [ip_address, udp_port]
                            )
                            distributed_hash_table.database_delete_node_messages.put(
                                [last_query_ip_address, last_query_udp_port]
                            )
                            if len(response_nodes) > 0:
                                ip_address = response_nodes[-1][1]
                                udp_port = response_nodes[-1][2]
                                distributed_hash_table.database_delete_node_messages.put(
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
                            if len(last_query_nodes) == 0:
                                result = {
                                    'result': response_samples,
                                    'header': {
                                        'target_id': target_id
                                    }
                                }
                                self.application_command_sample_infohashes_messages_send.put(
                                    [result, application_command_commander_keyword]
                                )
                            else:
                                nodes_distance = []
                                for j in last_query_nodes:
                                    nodes_node_id = j[0]
                                    nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                                nodes_distance.sort()
                                for j in last_query_nodes:
                                    nodes_node_id = j[0]
                                    nodes_ip_address = j[1]
                                    nodes_udp_port = j[2]
                                    if nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                        application_command_sample_infohashes_keyword = os.urandom(20).hex()
                                        last_query_nodes.remove(j)
                                        response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                        client.application_client_sample_infohashes_messages_recvfrom.put(
                                            ['application_command_sample_infohashes', target_id, nodes_ip_address, nodes_udp_port, application_command_sample_infohashes_keyword]
                                        )
                                        self.application_command_sample_infohashes_operators.put(
                                            ['append', [application_command_sample_infohashes_keyword, target_id, nodes_node_id, nodes_ip_address, nodes_udp_port, last_query_nodes, response_nodes, response_samples, application_command_commander_keyword, int(time.time())]]
                                        )

    def __send(self):
        while True:
            application_command_sample_infohashes_messages_recvfrom = self.application_command_sample_infohashes_messages_recvfrom.get()
            target_id = application_command_sample_infohashes_messages_recvfrom[0]
            application_command_commander_keyword = application_command_sample_infohashes_messages_recvfrom[1]
            distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                target_id
            )
            nodes = distributed_hash_table.database_query_nodes_messages_send.get()
            if len(nodes) == 0:
                result = {
                    'result': [],
                    'header': {
                        'target_id': target_id
                    }
                }
                self.application_command_sample_infohashes_messages_send.put(
                    [result, application_command_commander_keyword]
                )
            else:
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
                        application_command_sample_infohashes_keyword = os.urandom(20).hex()
                        nodes.remove(i)
                        response_nodes = []
                        response_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        response_samples = []
                        client.application_client_sample_infohashes_messages_recvfrom.put(
                            ['application_command_sample_infohashes', target_id, nodes_ip_address, nodes_udp_port, application_command_sample_infohashes_keyword]
                        )
                        self.application_command_sample_infohashes_operators.put(
                            ['append', [application_command_sample_infohashes_keyword, target_id, nodes_node_id, nodes_ip_address, nodes_udp_port, nodes, response_nodes, response_samples, application_command_commander_keyword, int(time.time())]]
                        )

    def start(self):
        explorer_krpc_v4_application_command_sample_infohashes_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v4_application_command_sample_infohashes_check_thread.setDaemon(True)
        explorer_krpc_v4_application_command_sample_infohashes_check_thread.start()
        explorer_krpc_v4_application_command_sample_infohashes_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v4_application_command_sample_infohashes_operators_thread.setDaemon(True)
        explorer_krpc_v4_application_command_sample_infohashes_operators_thread.start()
        explorer_krpc_v4_application_command_sample_infohashes_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_application_command_sample_infohashes_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_application_command_sample_infohashes_recvfrom_thread.start()
        explorer_krpc_v4_application_command_sample_infohashes_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v4_application_command_sample_infohashes_send_thread.setDaemon(True)
        explorer_krpc_v4_application_command_sample_infohashes_send_thread.start()