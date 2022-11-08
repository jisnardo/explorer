from ..application.client import client
from ..driver.memory import memory
import IPy
import os
import queue
import re
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
                nodes = database_find_node_messages[1]
                database_find_node_keyword = database_find_node_messages[7]
                for i in self.database_find_node_key:
                    if i[0] == database_find_node_keyword:
                        distributed_hash_table_keyword = i[1]
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
                        self.database_find_node_messages_send.put(
                            [node_id, nodes, distributed_hash_table_keyword]
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
        explorer_krpc_v4_database_find_node_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v4_database_find_node_check_thread.setDaemon(True)
        explorer_krpc_v4_database_find_node_check_thread.start()
        explorer_krpc_v4_database_find_node_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v4_database_find_node_operators_thread.setDaemon(True)
        explorer_krpc_v4_database_find_node_operators_thread.start()
        explorer_krpc_v4_database_find_node_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_database_find_node_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_database_find_node_recvfrom_thread.start()
        explorer_krpc_v4_database_find_node_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v4_database_find_node_send_thread.setDaemon(True)
        explorer_krpc_v4_database_find_node_send_thread.start()