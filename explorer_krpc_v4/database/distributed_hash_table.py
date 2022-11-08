from ..database.find_node import find_node
from ..database.ping import ping
from ..driver.memory import memory
import collections
import copy
import IPy
import math
import os
import pyben
import queue
import random
import re
import socket
import struct
import threading
import time

class distributed_hash_table:
    database_append_node_key = []
    database_append_node_messages = queue.Queue()
    database_append_node_operators = queue.Queue()
    database_binary_tree = {}
    database_confirm_nodes_time_key = []
    database_confirm_nodes_time_operators = queue.Queue()
    database_delete_node_with_ip_address_messages = queue.Queue()
    database_delete_node_with_node_id_messages = queue.Queue()
    database_prefix = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    database_query_node_with_ip_address_messages_recvfrom = queue.Queue()
    database_query_node_with_ip_address_messages_send = queue.Queue()
    database_query_node_with_node_id_messages_recvfrom = queue.Queue()
    database_query_node_with_node_id_messages_send = queue.Queue()
    database_query_nodes_messages_recvfrom = queue.Queue()
    database_query_nodes_messages_send = queue.Queue()
    database_query_nodes_number_messages_recvfrom = queue.Queue()
    database_query_nodes_number_messages_send = queue.Queue()
    database_self_node_id = ''

    def __append_node(self):
        while True:
            database_append_node_messages = self.database_append_node_messages.get()
            node_id = database_append_node_messages[0]
            ip_address = database_append_node_messages[1]
            udp_port = database_append_node_messages[2]
            pattern = re.compile(r'\b[0-9a-f]{40}\b')
            match = re.match(pattern, node_id.lower())
            if match is not None:
                if not match.group(0) == memory.node_id:
                    ip_address_type = IPy.IP(ip_address).iptype()
                    if ip_address_type == 'PUBLIC':
                        if 1 <= udp_port <= 65535:
                            distance = int(match.group(0), 16) ^ int(memory.node_id, 16)
                            if distance == 0:
                                k_bucket_name = 0
                            else:
                                k_bucket_name = int(math.log2(distance))
                            self.database_query_node_with_ip_address_messages_recvfrom.put(
                                [ip_address, udp_port]
                            )
                            database_query_node_with_ip_address_messages_send = self.database_query_node_with_ip_address_messages_send.get()
                            if database_query_node_with_ip_address_messages_send is False:
                                k_bucket_nodes_number = 0
                                for i in range(0, 8):
                                    if not self.database_binary_tree[str(k_bucket_name)][str(i)]['ip_address'] == '':
                                        k_bucket_nodes_number = k_bucket_nodes_number + 1
                                if k_bucket_nodes_number == 8:
                                    k_bucket_node_place = 0
                                    temporary_ip_address = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['ip_address']
                                    temporary_udp_port = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['udp_port']
                                    distributed_hash_table_keyword = os.urandom(20).hex()
                                    ping.database_ping_messages_recvfrom.put(
                                        [temporary_ip_address, temporary_udp_port, distributed_hash_table_keyword]
                                    )
                                    self.database_append_node_operators.put(
                                        ['append', [distributed_hash_table_keyword, k_bucket_name, temporary_ip_address, temporary_udp_port, match.group(0), ip_address, udp_port, int(time.time())]]
                                    )
                                else:
                                    self.database_binary_tree[str(k_bucket_name)][str(k_bucket_nodes_number)]['node_id'] = match.group(0)
                                    self.database_binary_tree[str(k_bucket_name)][str(k_bucket_nodes_number)]['ip_address'] = ip_address
                                    self.database_binary_tree[str(k_bucket_name)][str(k_bucket_nodes_number)]['udp_port'] = udp_port
                                    self.database_binary_tree[str(k_bucket_name)][str(k_bucket_nodes_number)]['update_time'] = int(time.time())
                            else:
                                k_bucket_node_place = database_query_node_with_ip_address_messages_send[1]
                                k_bucket_nodes_number = 0
                                for i in range(0, 8):
                                    if not self.database_binary_tree[str(k_bucket_name)][str(i)]['ip_address'] == '':
                                        k_bucket_nodes_number = k_bucket_nodes_number + 1
                                for j in range(k_bucket_node_place, k_bucket_nodes_number):
                                    if j == k_bucket_nodes_number - 1:
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['node_id'] = match.group(0)
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['ip_address'] = ip_address
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['udp_port'] = udp_port
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['update_time'] = int(time.time())
                                    else:
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['node_id'] = self.database_binary_tree[str(k_bucket_name)][str(j + 1)]['node_id']
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['ip_address'] = self.database_binary_tree[str(k_bucket_name)][str(j + 1)]['ip_address']
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['udp_port'] = self.database_binary_tree[str(k_bucket_name)][str(j + 1)]['udp_port']
                                        self.database_binary_tree[str(k_bucket_name)][str(j)]['update_time'] = self.database_binary_tree[str(k_bucket_name)][str(j + 1)]['update_time']

    def __append_node_check(self):
        while True:
            if len(self.database_append_node_key) > 0:
                for i in self.database_append_node_key:
                    if i[7] < int(time.time()) - 300:
                        self.database_append_node_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __append_node_operators(self):
        while True:
            database_append_node_operators = self.database_append_node_operators.get()
            operate = database_append_node_operators[0]
            element = database_append_node_operators[1]
            if operate == 'append':
                if element not in self.database_append_node_key:
                    self.database_append_node_key.append(element)
            if operate == 'remove':
                if element in self.database_append_node_key:
                    self.database_append_node_key.remove(element)

    def __append_node_ping(self):
        while True:
            database_ping_messages_send = ping.database_ping_messages_send.get()
            if database_ping_messages_send[0] is False:
                distributed_hash_table_keyword = database_ping_messages_send[1]
                for i in self.database_append_node_key:
                    if i[0] == distributed_hash_table_keyword:
                        k_bucket_name = i[1]
                        temporary_ip_address = i[2]
                        temporary_udp_port = i[3]
                        node_id = i[4]
                        ip_address = i[5]
                        udp_port = i[6]
                        self.database_query_node_with_ip_address_messages_recvfrom.put(
                            [ip_address, udp_port]
                        )
                        database_query_node_with_ip_address_messages_send = self.database_query_node_with_ip_address_messages_send.get()
                        if database_query_node_with_ip_address_messages_send is False:
                            self.database_query_node_with_ip_address_messages_recvfrom.put(
                                [temporary_ip_address, temporary_udp_port]
                            )
                            database_query_node_with_ip_address_messages_send = self.database_query_node_with_ip_address_messages_send.get()
                            if database_query_node_with_ip_address_messages_send is False:
                                self.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                            else:
                                k_bucket_node_place = database_query_node_with_ip_address_messages_send[1]
                                k_bucket_nodes_number = 0
                                for j in range(0, 8):
                                    if not self.database_binary_tree[str(k_bucket_name)][str(j)]['ip_address'] == '':
                                        k_bucket_nodes_number = k_bucket_nodes_number + 1
                                for k in range(k_bucket_node_place, k_bucket_nodes_number):
                                    if k == k_bucket_nodes_number - 1:
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['node_id'] = node_id
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['ip_address'] = ip_address
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['udp_port'] = udp_port
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['update_time'] = int(time.time())
                                    else:
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['node_id'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['node_id']
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['ip_address'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['ip_address']
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['udp_port'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['udp_port']
                                        self.database_binary_tree[str(k_bucket_name)][str(k)]['update_time'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['update_time']
                        self.database_append_node_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = database_ping_messages_send[0]
                distributed_hash_table_keyword = database_ping_messages_send[1]
                for i in self.database_append_node_key:
                    if i[0] == distributed_hash_table_keyword:
                        k_bucket_name = i[1]
                        temporary_ip_address = i[2]
                        temporary_udp_port = i[3]
                        self.database_query_node_with_ip_address_messages_recvfrom.put(
                            [temporary_ip_address, temporary_udp_port]
                        )
                        database_query_node_with_ip_address_messages_send = self.database_query_node_with_ip_address_messages_send.get()
                        if database_query_node_with_ip_address_messages_send is False:
                            self.database_append_node_messages.put(
                                [node_id, temporary_ip_address, temporary_udp_port]
                            )
                        else:
                            k_bucket_node_place = database_query_node_with_ip_address_messages_send[1]
                            node_id = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['node_id']
                            ip_address = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['ip_address']
                            udp_port = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['udp_port']
                            k_bucket_nodes_number = 0
                            for j in range(0, 8):
                                if not self.database_binary_tree[str(k_bucket_name)][str(j)]['ip_address'] == '':
                                    k_bucket_nodes_number = k_bucket_nodes_number + 1
                            for k in range(k_bucket_node_place, k_bucket_nodes_number):
                                if k == k_bucket_nodes_number - 1:
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['node_id'] = node_id
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['ip_address'] = ip_address
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['udp_port'] = udp_port
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['update_time'] = int(time.time())
                                else:
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['node_id'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['node_id']
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['ip_address'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['ip_address']
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['udp_port'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['udp_port']
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['update_time'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['update_time']
                        self.database_append_node_operators.put(
                            ['remove', i]
                        )

    def __check_database_binary_tree(self):
        while True:
            for i in range(0, 160):
                node_id_list = []
                for j in range(0, 8):
                    if not self.database_binary_tree[str(i)][str(j)]['node_id'] == '':
                        node_id_list.append(self.database_binary_tree[str(i)][str(j)]['node_id'])
                node_id_dict = dict(collections.Counter(node_id_list))
                for key, value in node_id_dict.items():
                    if value > 1:
                        self.database_delete_node_with_node_id_messages.put(
                            key
                        )
            time.sleep(30)

    def __confirm_nodes_time(self):
        while True:
            for i in range(0, 160):
                for j in range(0, 8):
                    if not self.database_binary_tree[str(i)][str(j)]['ip_address'] == '':
                        if self.database_binary_tree[str(i)][str(j)]['update_time'] < int(time.time()) - 900:
                            database_new_prefix = copy.deepcopy(self.database_prefix)
                            database_new_prefix.remove(memory.node_id[39:])
                            ip_address = self.database_binary_tree[str(i)][str(j)]['ip_address']
                            udp_port = self.database_binary_tree[str(i)][str(j)]['udp_port']
                            distributed_hash_table_keyword = os.urandom(20).hex()
                            k_bucket_name = i
                            find_node.database_find_node_messages_recvfrom.put(
                                [memory.node_id[:39] + random.choice(database_new_prefix), ip_address, udp_port, distributed_hash_table_keyword]
                            )
                            self.database_confirm_nodes_time_operators.put(
                                ['append', [distributed_hash_table_keyword, k_bucket_name, ip_address, udp_port, int(time.time())]]
                            )
            time.sleep(60)

    def __confirm_nodes_time_check(self):
        while True:
            if len(self.database_confirm_nodes_time_key) > 0:
                for i in self.database_confirm_nodes_time_key:
                    if i[4] < int(time.time()) - 300:
                        self.database_confirm_nodes_time_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __confirm_nodes_time_find_node(self):
        while True:
            database_find_node_messages_send = find_node.database_find_node_messages_send.get()
            if database_find_node_messages_send[0] is False:
                distributed_hash_table_keyword = database_find_node_messages_send[1]
                for i in self.database_confirm_nodes_time_key:
                    if i[0] == distributed_hash_table_keyword:
                        k_bucket_name = i[1]
                        ip_address = i[2]
                        udp_port = i[3]
                        self.database_query_node_with_ip_address_messages_recvfrom.put(
                            [ip_address, udp_port]
                        )
                        database_query_node_with_ip_address_messages_send = self.database_query_node_with_ip_address_messages_send.get()
                        if database_query_node_with_ip_address_messages_send is not False:
                            k_bucket_node_place = database_query_node_with_ip_address_messages_send[1]
                            k_bucket_nodes_number = 0
                            for j in range(0, 8):
                                if not self.database_binary_tree[str(k_bucket_name)][str(j)]['ip_address'] == '':
                                    k_bucket_nodes_number = k_bucket_nodes_number + 1
                            for k in range(k_bucket_node_place, k_bucket_nodes_number):
                                if k == k_bucket_nodes_number - 1:
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['node_id'] = ''
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['ip_address'] = ''
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['udp_port'] = ''
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['update_time'] = int(time.time())
                                else:
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['node_id'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['node_id']
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['ip_address'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['ip_address']
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['udp_port'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['udp_port']
                                    self.database_binary_tree[str(k_bucket_name)][str(k)]['update_time'] = self.database_binary_tree[str(k_bucket_name)][str(k + 1)]['update_time']
                        self.database_confirm_nodes_time_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = database_find_node_messages_send[0]
                nodes = database_find_node_messages_send[1]
                distributed_hash_table_keyword = database_find_node_messages_send[2]
                for i in self.database_confirm_nodes_time_key:
                    if i[0] == distributed_hash_table_keyword:
                        k_bucket_name = i[1]
                        ip_address = i[2]
                        udp_port = i[3]
                        for j in nodes:
                            nodes_node_id = j[0]
                            nodes_ip_address = j[1]
                            nodes_udp_port = j[2]
                            self.database_append_node_messages.put(
                                [nodes_node_id, nodes_ip_address, nodes_udp_port]
                            )
                        self.database_query_node_with_ip_address_messages_recvfrom.put(
                            [ip_address, udp_port]
                        )
                        database_query_node_with_ip_address_messages_send = self.database_query_node_with_ip_address_messages_send.get()
                        if database_query_node_with_ip_address_messages_send is False:
                            self.database_append_node_messages.put(
                                [node_id, ip_address, udp_port]
                            )
                        else:
                            k_bucket_node_place = database_query_node_with_ip_address_messages_send[1]
                            k_bucket_nodes_number = 0
                            for k in range(0, 8):
                                if not self.database_binary_tree[str(k_bucket_name)][str(k)]['ip_address'] == '':
                                    k_bucket_nodes_number = k_bucket_nodes_number + 1
                            node_id = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['node_id']
                            ip_address = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['ip_address']
                            udp_port = self.database_binary_tree[str(k_bucket_name)][str(k_bucket_node_place)]['udp_port']
                            for l in range(k_bucket_node_place, k_bucket_nodes_number):
                                if l == k_bucket_nodes_number - 1:
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['node_id'] = node_id
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['ip_address'] = ip_address
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['udp_port'] = udp_port
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['update_time'] = int(time.time())
                                else:
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['node_id'] = self.database_binary_tree[str(k_bucket_name)][str(l + 1)]['node_id']
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['ip_address'] = self.database_binary_tree[str(k_bucket_name)][str(l + 1)]['ip_address']
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['udp_port'] = self.database_binary_tree[str(k_bucket_name)][str(l + 1)]['udp_port']
                                    self.database_binary_tree[str(k_bucket_name)][str(l)]['update_time'] = self.database_binary_tree[str(k_bucket_name)][str(l + 1)]['update_time']
                        self.database_confirm_nodes_time_operators.put(
                            ['remove', i]
                        )

    def __confirm_nodes_time_operators(self):
        while True:
            database_confirm_nodes_time_operators = self.database_confirm_nodes_time_operators.get()
            operate = database_confirm_nodes_time_operators[0]
            element = database_confirm_nodes_time_operators[1]
            if operate == 'append':
                if element not in self.database_confirm_nodes_time_key:
                    self.database_confirm_nodes_time_key.append(element)
            if operate == 'remove':
                if element in self.database_confirm_nodes_time_key:
                    self.database_confirm_nodes_time_key.remove(element)

    def __delete_node_with_ip_address(self):
        while True:
            database_delete_node_with_ip_address_messages = self.database_delete_node_with_ip_address_messages.get()
            ip_address = database_delete_node_with_ip_address_messages[0]
            udp_port = database_delete_node_with_ip_address_messages[1]
            for i in range(0, 160):
                for j in range(0, 8):
                    if self.database_binary_tree[str(i)][str(j)]['ip_address'] == ip_address and self.database_binary_tree[str(i)][str(j)]['udp_port'] == udp_port:
                        k_bucket_node_place = j
                        k_bucket_nodes_number = 0
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(i)][str(k)]['ip_address'] == '':
                                k_bucket_nodes_number = k_bucket_nodes_number + 1
                        for l in range(k_bucket_node_place, k_bucket_nodes_number):
                            if l == k_bucket_nodes_number - 1:
                                self.database_binary_tree[str(i)][str(l)]['node_id'] = ''
                                self.database_binary_tree[str(i)][str(l)]['ip_address'] = ''
                                self.database_binary_tree[str(i)][str(l)]['udp_port'] = ''
                                self.database_binary_tree[str(i)][str(l)]['update_time'] = int(time.time())
                            else:
                                self.database_binary_tree[str(i)][str(l)]['node_id'] = self.database_binary_tree[str(i)][str(l + 1)]['node_id']
                                self.database_binary_tree[str(i)][str(l)]['ip_address'] = self.database_binary_tree[str(i)][str(l + 1)]['ip_address']
                                self.database_binary_tree[str(i)][str(l)]['udp_port'] = self.database_binary_tree[str(i)][str(l + 1)]['udp_port']
                                self.database_binary_tree[str(i)][str(l)]['update_time'] = self.database_binary_tree[str(i)][str(l + 1)]['update_time']

    def __delete_node_with_node_id(self):
        while True:
            node_id = self.database_delete_node_with_node_id_messages.get()
            for i in range(0, 160):
                for j in range(0, 8):
                    if self.database_binary_tree[str(i)][str(j)]['node_id'] == node_id:
                        k_bucket_node_place = j
                        k_bucket_nodes_number = 0
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(i)][str(k)]['ip_address'] == '':
                                k_bucket_nodes_number = k_bucket_nodes_number + 1
                        for l in range(k_bucket_node_place, k_bucket_nodes_number):
                            if l == k_bucket_nodes_number - 1:
                                self.database_binary_tree[str(i)][str(l)]['node_id'] = ''
                                self.database_binary_tree[str(i)][str(l)]['ip_address'] = ''
                                self.database_binary_tree[str(i)][str(l)]['udp_port'] = ''
                                self.database_binary_tree[str(i)][str(l)]['update_time'] = int(time.time())
                            else:
                                self.database_binary_tree[str(i)][str(l)]['node_id'] = self.database_binary_tree[str(i)][str(l + 1)]['node_id']
                                self.database_binary_tree[str(i)][str(l)]['ip_address'] = self.database_binary_tree[str(i)][str(l + 1)]['ip_address']
                                self.database_binary_tree[str(i)][str(l)]['udp_port'] = self.database_binary_tree[str(i)][str(l + 1)]['udp_port']
                                self.database_binary_tree[str(i)][str(l)]['update_time'] = self.database_binary_tree[str(i)][str(l + 1)]['update_time']

    def __query_node_with_ip_address(self):
        while True:
            database_query_node_with_ip_address_messages_recvfrom = self.database_query_node_with_ip_address_messages_recvfrom.get()
            ip_address = database_query_node_with_ip_address_messages_recvfrom[0]
            udp_port = database_query_node_with_ip_address_messages_recvfrom[1]
            flag = False
            for i in range(0, 160):
                for j in range(0, 8):
                    if self.database_binary_tree[str(i)][str(j)]['ip_address'] == ip_address and self.database_binary_tree[str(i)][str(j)]['udp_port'] == udp_port:
                        flag = True
                        self.database_query_node_with_ip_address_messages_send.put(
                            [i, j]
                        )
            if flag is False:
                self.database_query_node_with_ip_address_messages_send.put(
                    False
                )

    def __query_node_with_node_id(self):
        while True:
            node_id = self.database_query_node_with_node_id_messages_recvfrom.get()
            distance = int(node_id, 16) ^ int(memory.node_id, 16)
            if distance == 0:
                k_bucket_name = 0
            else:
                k_bucket_name = int(math.log2(distance))
            flag = False
            for i in range(0, 8):
                if self.database_binary_tree[str(k_bucket_name)][str(i)]['node_id'] == node_id:
                    flag = True
                    self.database_query_node_with_node_id_messages_send.put(
                        True
                    )
            if flag is False:
                self.database_query_node_with_node_id_messages_send.put(
                    False
                )

    def __query_nodes(self):
        while True:
            target_id = self.database_query_nodes_messages_recvfrom.get()
            distance = int(target_id, 16) ^ int(memory.node_id, 16)
            if distance == 0:
                k_bucket_name = 0
            else:
                k_bucket_name = int(math.log2(distance))
            nodes = []
            for i in range(0, 8):
                if not self.database_binary_tree[str(k_bucket_name)][str(i)]['node_id'] == '':
                    nodes_node_id = self.database_binary_tree[str(k_bucket_name)][str(i)]['node_id']
                    nodes_ip_address = self.database_binary_tree[str(k_bucket_name)][str(i)]['ip_address']
                    nodes_udp_port = self.database_binary_tree[str(k_bucket_name)][str(i)]['udp_port']
                    nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
            if len(nodes) == 0:
                self.database_query_nodes_number_messages_recvfrom.put(
                    0
                )
                nodes_number = self.database_query_nodes_number_messages_send.get()
                if nodes_number == 0:
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    temporary_nodes = []
                    temporary_nodes_distance = []
                    for j in range(0, 160):
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                    if len(temporary_nodes) > 8:
                        temporary_nodes_distance.sort()
                        for l in temporary_nodes:
                            nodes_node_id = l[0]
                            nodes_ip_address = l[1]
                            nodes_udp_port = l[2]
                            if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                            if temporary_nodes_distance[1] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                            if temporary_nodes_distance[2] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                            if temporary_nodes_distance[3] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                            if temporary_nodes_distance[4] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                            if temporary_nodes_distance[5] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                            if temporary_nodes_distance[6] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                            if temporary_nodes_distance[7] == int(target_id, 16) ^ int(nodes_node_id, 16):
                                nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        self.database_query_nodes_messages_send.put(
                            nodes
                        )
                    else:
                        for l in temporary_nodes:
                            nodes_node_id = l[0]
                            nodes_ip_address = l[1]
                            nodes_udp_port = l[2]
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        self.database_query_nodes_messages_send.put(
                            nodes
                        )
            elif len(nodes) == 1:
                temporary_nodes = []
                temporary_nodes_distance = []
                for j in range(0, 160):
                    if not k_bucket_name == j:
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                if len(temporary_nodes) > 7:
                    temporary_nodes_distance.sort()
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[1] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[2] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[3] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[4] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[5] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[6] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
            elif len(nodes) == 2:
                temporary_nodes = []
                temporary_nodes_distance = []
                for j in range(0, 160):
                    if not k_bucket_name == j:
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                if len(temporary_nodes) > 6:
                    temporary_nodes_distance.sort()
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[1] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[2] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[3] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[4] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[5] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
            elif len(nodes) == 3:
                temporary_nodes = []
                temporary_nodes_distance = []
                for j in range(0, 160):
                    if not k_bucket_name == j:
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                if len(temporary_nodes) > 5:
                    temporary_nodes_distance.sort()
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[1] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[2] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[3] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[4] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
            elif len(nodes) == 4:
                temporary_nodes = []
                temporary_nodes_distance = []
                for j in range(0, 160):
                    if not k_bucket_name == j:
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                if len(temporary_nodes) > 4:
                    temporary_nodes_distance.sort()
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[1] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[2] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[3] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
            elif len(nodes) == 5:
                temporary_nodes = []
                temporary_nodes_distance = []
                for j in range(0, 160):
                    if not k_bucket_name == j:
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                if len(temporary_nodes) > 3:
                    temporary_nodes_distance.sort()
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[1] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[2] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
            elif len(nodes) == 6:
                temporary_nodes = []
                temporary_nodes_distance = []
                for j in range(0, 160):
                    if not k_bucket_name == j:
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                if len(temporary_nodes) > 2:
                    temporary_nodes_distance.sort()
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                        if temporary_nodes_distance[1] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
            elif len(nodes) == 7:
                temporary_nodes = []
                temporary_nodes_distance = []
                for j in range(0, 160):
                    if not k_bucket_name == j:
                        for k in range(0, 8):
                            if not self.database_binary_tree[str(j)][str(k)]['node_id'] == '':
                                nodes_node_id = self.database_binary_tree[str(j)][str(k)]['node_id']
                                nodes_ip_address = self.database_binary_tree[str(j)][str(k)]['ip_address']
                                nodes_udp_port = self.database_binary_tree[str(j)][str(k)]['udp_port']
                                temporary_nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                temporary_nodes_distance.append(int(target_id, 16) ^ int(nodes_node_id, 16))
                if len(temporary_nodes) > 1:
                    temporary_nodes_distance.sort()
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        if temporary_nodes_distance[0] == int(target_id, 16) ^ int(nodes_node_id, 16):
                            nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
                else:
                    for l in temporary_nodes:
                        nodes_node_id = l[0]
                        nodes_ip_address = l[1]
                        nodes_udp_port = l[2]
                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                    self.database_query_nodes_messages_send.put(
                        nodes
                    )
            elif len(nodes) == 8:
                self.database_query_nodes_messages_send.put(
                    nodes
                )

    def __query_nodes_number(self):
        while True:
            self.database_query_nodes_number_messages_recvfrom.get()
            nodes_number = 0
            for i in range(0, 160):
                for j in range(0, 8):
                    if not self.database_binary_tree[str(i)][str(j)]['node_id'] == '':
                        nodes_number = nodes_number + 1
            self.database_query_nodes_number_messages_send.put(
                nodes_number
            )

    def __restart(self):
        while True:
            if self.database_self_node_id == memory.node_id:
                time.sleep(1)
            else:
                database_new_prefix = copy.deepcopy(self.database_prefix)
                database_new_prefix.remove(memory.node_id[39:])
                self.database_query_nodes_messages_recvfrom.put(
                    memory.node_id[:39] + random.choice(database_new_prefix)
                )
                bootstrap_nodes = self.database_query_nodes_messages_send.get()
                self.database_binary_tree.clear()
                for i in range(0, 160):
                    self.database_binary_tree.update({str(i): {}})
                    for j in range(0, 8):
                        self.database_binary_tree[str(i)].update({str(j): {}})
                        self.database_binary_tree[str(i)][str(j)].update({'node_id': ''})
                        self.database_binary_tree[str(i)][str(j)].update({'ip_address': ''})
                        self.database_binary_tree[str(i)][str(j)].update({'udp_port': ''})
                        self.database_binary_tree[str(i)][str(j)].update({'update_time': int(time.time())})
                for k in bootstrap_nodes:
                    bootstrap_nodes_node_id = k[0]
                    bootstrap_nodes_ip_address = k[1]
                    bootstrap_nodes_udp_port = k[2]
                    self.database_append_node_messages.put(
                        [bootstrap_nodes_node_id, bootstrap_nodes_ip_address, bootstrap_nodes_udp_port]
                    )
                self.database_self_node_id = memory.node_id
                time.sleep(1)

    def __write_nodes_to_file(self):
        time.sleep(900)
        while True:
            nodes = bytes()
            for i in range(0, 160):
                for j in range(0, 8):
                    if not self.database_binary_tree[str(i)][str(j)]['node_id'] == '':
                        ip_address = self.database_binary_tree[str(i)][str(j)]['ip_address']
                        udp_port = self.database_binary_tree[str(i)][str(j)]['udp_port']
                        nodes_ip_address = socket.inet_pton(socket.AF_INET, ip_address)
                        nodes_udp_port = struct.pack('!H', udp_port)
                        nodes = nodes + nodes_ip_address + nodes_udp_port
            write_data = pyben.dumps({'nodes': nodes})
            with open(os.path.dirname(os.path.abspath(__file__)) + '/dht.dat', mode = 'wb') as file:
                file.write(write_data)
            time.sleep(900)

    def start(self):
        for i in range(0, 160):
            self.database_binary_tree.update({str(i): {}})
            for j in range(0, 8):
                self.database_binary_tree[str(i)].update({str(j): {}})
                self.database_binary_tree[str(i)][str(j)].update({'node_id': ''})
                self.database_binary_tree[str(i)][str(j)].update({'ip_address': ''})
                self.database_binary_tree[str(i)][str(j)].update({'udp_port': ''})
                self.database_binary_tree[str(i)][str(j)].update({'update_time': int(time.time())})
        self.database_self_node_id = memory.node_id
        explorer_krpc_v4_database_distributed_hash_table_append_node_thread = threading.Thread(target = self.__append_node)
        explorer_krpc_v4_database_distributed_hash_table_append_node_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_append_node_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_append_node_check_thread = threading.Thread(target = self.__append_node_check)
        explorer_krpc_v4_database_distributed_hash_table_append_node_check_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_append_node_check_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_append_node_operators_thread = threading.Thread(target = self.__append_node_operators)
        explorer_krpc_v4_database_distributed_hash_table_append_node_operators_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_append_node_operators_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_append_node_ping_thread = threading.Thread(target = self.__append_node_ping)
        explorer_krpc_v4_database_distributed_hash_table_append_node_ping_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_append_node_ping_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_check_database_binary_tree_thread = threading.Thread(target = self.__check_database_binary_tree)
        explorer_krpc_v4_database_distributed_hash_table_check_database_binary_tree_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_check_database_binary_tree_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_check_thread = threading.Thread(target = self.__confirm_nodes_time_check)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_check_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_check_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_find_node_thread = threading.Thread(target = self.__confirm_nodes_time_find_node)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_find_node_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_find_node_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_operators_thread = threading.Thread(target = self.__confirm_nodes_time_operators)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_operators_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_operators_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_thread = threading.Thread(target = self.__confirm_nodes_time)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_confirm_nodes_time_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_delete_node_with_ip_address_thread = threading.Thread(target = self.__delete_node_with_ip_address)
        explorer_krpc_v4_database_distributed_hash_table_delete_node_with_ip_address_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_delete_node_with_ip_address_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_delete_node_with_node_id_thread = threading.Thread(target = self.__delete_node_with_node_id)
        explorer_krpc_v4_database_distributed_hash_table_delete_node_with_node_id_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_delete_node_with_node_id_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_query_node_with_ip_address_thread = threading.Thread(target = self.__query_node_with_ip_address)
        explorer_krpc_v4_database_distributed_hash_table_query_node_with_ip_address_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_query_node_with_ip_address_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_query_node_with_node_id_thread = threading.Thread(target = self.__query_node_with_node_id)
        explorer_krpc_v4_database_distributed_hash_table_query_node_with_node_id_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_query_node_with_node_id_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_query_nodes_thread = threading.Thread(target = self.__query_nodes)
        explorer_krpc_v4_database_distributed_hash_table_query_nodes_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_query_nodes_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_query_nodes_number_thread = threading.Thread(target = self.__query_nodes_number)
        explorer_krpc_v4_database_distributed_hash_table_query_nodes_number_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_query_nodes_number_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_restart_thread = threading.Thread(target = self.__restart)
        explorer_krpc_v4_database_distributed_hash_table_restart_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_restart_thread.start()
        explorer_krpc_v4_database_distributed_hash_table_write_nodes_to_file_thread = threading.Thread(target = self.__write_nodes_to_file)
        explorer_krpc_v4_database_distributed_hash_table_write_nodes_to_file_thread.setDaemon(True)
        explorer_krpc_v4_database_distributed_hash_table_write_nodes_to_file_thread.start()