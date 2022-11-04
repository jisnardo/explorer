from ...application.client import client
from ...database.distributed_hash_table import distributed_hash_table
import os
import queue
import threading
import time

class ping:
    application_command_ping_key = []
    application_command_ping_messages_recvfrom = queue.Queue()
    application_command_ping_messages_send = queue.Queue()
    application_command_ping_operators = queue.Queue()

    def __check(self):
        while True:
            if len(self.application_command_ping_key) > 0:
                for i in self.application_command_ping_key:
                    if i[4] < int(time.time()) - 300:
                        self.application_command_ping_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __operators(self):
        while True:
            application_command_ping_operators = self.application_command_ping_operators.get()
            operate = application_command_ping_operators[0]
            element = application_command_ping_operators[1]
            if operate == 'append':
                if element not in self.application_command_ping_key:
                    self.application_command_ping_key.append(element)
            if operate == 'remove':
                if element in self.application_command_ping_key:
                    self.application_command_ping_key.remove(element)

    def __recvfrom(self):
        while True:
            application_client_ping_messages_send_application_command_ping = client.application_client_ping_messages_send_application_command_ping.get()
            if application_client_ping_messages_send_application_command_ping[0] is False:
                application_command_ping_keyword = application_client_ping_messages_send_application_command_ping[1]
                for i in self.application_command_ping_key:
                    if i[0] == application_command_ping_keyword:
                        result = {
                            'result': False,
                            'header': {
                                'ip_address': i[1],
                                'udp_port': i[2]
                            }
                        }
                        application_command_commander_keyword = i[3]
                        self.application_command_ping_messages_send.put(
                            [result, application_command_commander_keyword]
                        )
                        self.application_command_ping_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = application_client_ping_messages_send_application_command_ping[0]
                ip_address = application_client_ping_messages_send_application_command_ping[5]
                udp_port = application_client_ping_messages_send_application_command_ping[6]
                application_command_ping_keyword = application_client_ping_messages_send_application_command_ping[7]
                for i in self.application_command_ping_key:
                    if i[0] == application_command_ping_keyword:
                        distributed_hash_table.database_append_node_messages.put(
                            [node_id, ip_address, udp_port]
                        )
                        result = {
                            'result': True,
                            'header': {
                                'ip_address': i[1],
                                'udp_port': i[2]
                            }
                        }
                        application_command_commander_keyword = i[3]
                        self.application_command_ping_messages_send.put(
                            [result, application_command_commander_keyword]
                        )
                        self.application_command_ping_operators.put(
                            ['remove', i]
                        )

    def __send(self):
        while True:
            application_command_ping_messages_recvfrom = self.application_command_ping_messages_recvfrom.get()
            ip_address = application_command_ping_messages_recvfrom[0]
            udp_port = application_command_ping_messages_recvfrom[1]
            application_command_commander_keyword = application_command_ping_messages_recvfrom[2]
            application_command_ping_keyword = os.urandom(20).hex()
            client.application_client_ping_messages_recvfrom.put(
                ['application_command_ping', ip_address, udp_port, application_command_ping_keyword]
            )
            self.application_command_ping_operators.put(
                ['append', [application_command_ping_keyword, ip_address, udp_port, application_command_commander_keyword, int(time.time())]]
            )

    def start(self):
        explorer_krpc_v4_application_command_ping_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v4_application_command_ping_check_thread.setDaemon(True)
        explorer_krpc_v4_application_command_ping_check_thread.start()
        explorer_krpc_v4_application_command_ping_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v4_application_command_ping_operators_thread.setDaemon(True)
        explorer_krpc_v4_application_command_ping_operators_thread.start()
        explorer_krpc_v4_application_command_ping_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_application_command_ping_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_application_command_ping_recvfrom_thread.start()
        explorer_krpc_v4_application_command_ping_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v4_application_command_ping_send_thread.setDaemon(True)
        explorer_krpc_v4_application_command_ping_send_thread.start()