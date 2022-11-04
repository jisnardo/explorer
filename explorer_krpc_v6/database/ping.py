from ..application.client import client
import os
import queue
import threading
import time

class ping:
    database_ping_key = []
    database_ping_messages_recvfrom = queue.Queue()
    database_ping_messages_send = queue.Queue()
    database_ping_operators = queue.Queue()

    def __check(self):
        while True:
            if len(self.database_ping_key) > 0:
                for i in self.database_ping_key:
                    if i[2] < int(time.time()) - 300:
                        self.database_ping_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __operators(self):
        while True:
            database_ping_operators = self.database_ping_operators.get()
            operate = database_ping_operators[0]
            element = database_ping_operators[1]
            if operate == 'append':
                if element not in self.database_ping_key:
                    self.database_ping_key.append(element)
            if operate == 'remove':
                if element in self.database_ping_key:
                    self.database_ping_key.remove(element)

    def __recvfrom(self):
        while True:
            database_ping_messages = client.application_client_ping_messages_send_database_ping.get()
            if database_ping_messages[0] is False:
                database_ping_keyword = database_ping_messages[1]
                for i in self.database_ping_key:
                    if i[0] == database_ping_keyword:
                        distributed_hash_table_keyword = i[1]
                        self.database_ping_messages_send.put(
                            [False, distributed_hash_table_keyword]
                        )
                        self.database_ping_operators.put(
                            ['remove', i]
                        )
            else:
                database_ping_keyword = database_ping_messages[7]
                for i in self.database_ping_key:
                    if i[0] == database_ping_keyword:
                        distributed_hash_table_keyword = i[1]
                        self.database_ping_messages_send.put(
                            [True, distributed_hash_table_keyword]
                        )
                        self.database_ping_operators.put(
                            ['remove', i]
                        )

    def __send(self):
        while True:
            database_ping_messages_recvfrom = self.database_ping_messages_recvfrom.get()
            ip_address = database_ping_messages_recvfrom[0]
            udp_port = database_ping_messages_recvfrom[1]
            distributed_hash_table_keyword = database_ping_messages_recvfrom[2]
            database_ping_keyword = os.urandom(20).hex()
            client.application_client_ping_messages_recvfrom.put(
                ['database_ping', ip_address, udp_port, database_ping_keyword]
            )
            self.database_ping_operators.put(
                ['append', [database_ping_keyword, distributed_hash_table_keyword, int(time.time())]]
            )

    def start(self):
        explorer_krpc_v6_database_ping_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v6_database_ping_check_thread.setDaemon(True)
        explorer_krpc_v6_database_ping_check_thread.start()
        explorer_krpc_v6_database_ping_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v6_database_ping_operators_thread.setDaemon(True)
        explorer_krpc_v6_database_ping_operators_thread.start()
        explorer_krpc_v6_database_ping_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v6_database_ping_recvfrom_thread.setDaemon(True)
        explorer_krpc_v6_database_ping_recvfrom_thread.start()
        explorer_krpc_v6_database_ping_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v6_database_ping_send_thread.setDaemon(True)
        explorer_krpc_v6_database_ping_send_thread.start()