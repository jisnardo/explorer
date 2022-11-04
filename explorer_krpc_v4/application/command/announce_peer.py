from ...application.client import client
from ...database.distributed_hash_table import distributed_hash_table
from ...database.token_manager import token_manager
import os
import queue
import threading
import time

class announce_peer:
    application_command_announce_peer_key = []
    application_command_announce_peer_messages_recvfrom = queue.Queue()
    application_command_announce_peer_messages_send = queue.Queue()
    application_command_announce_peer_operators = queue.Queue()

    def __check(self):
        while True:
            if len(self.application_command_announce_peer_key) > 0:
                for i in self.application_command_announce_peer_key:
                    if i[7] < int(time.time()) - 300:
                        self.application_command_announce_peer_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __operators(self):
        while True:
            application_command_announce_peer_operators = self.application_command_announce_peer_operators.get()
            operate = application_command_announce_peer_operators[0]
            element = application_command_announce_peer_operators[1]
            if operate == 'append':
                if element not in self.application_command_announce_peer_key:
                    self.application_command_announce_peer_key.append(element)
            if operate == 'remove':
                if element in self.application_command_announce_peer_key:
                    self.application_command_announce_peer_key.remove(element)

    def __recvfrom(self):
        while True:
            application_client_announce_peer_messages_send_application_command_announce_peer = client.application_client_announce_peer_messages_send_application_command_announce_peer.get()
            if application_client_announce_peer_messages_send_application_command_announce_peer[0] is False:
                application_command_announce_peer_keyword = application_client_announce_peer_messages_send_application_command_announce_peer[1]
                for i in self.application_command_announce_peer_key:
                    if i[0] == application_command_announce_peer_keyword:
                        node_id = i[1]
                        ip_address = i[2]
                        udp_port = i[3]
                        info_hash = i[4]
                        tcp_port = i[5]
                        application_command_commander_keyword = i[6]
                        result = {
                            'result': {
                                'node_id': node_id,
                                'ip_address': ip_address,
                                'storing': False,
                                'udp_port': udp_port
                            },
                            'header': {
                                'info_hash': info_hash,
                                'tcp_port': tcp_port
                            }
                        }
                        self.application_command_announce_peer_messages_send.put(
                            [result, application_command_commander_keyword]
                        )
                        self.application_command_announce_peer_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = application_client_announce_peer_messages_send_application_command_announce_peer[0]
                ip_address = application_client_announce_peer_messages_send_application_command_announce_peer[5]
                udp_port = application_client_announce_peer_messages_send_application_command_announce_peer[6]
                application_command_announce_peer_keyword = application_client_announce_peer_messages_send_application_command_announce_peer[7]
                for i in self.application_command_announce_peer_key:
                    if i[0] == application_command_announce_peer_keyword:
                        node_id = i[1]
                        ip_address = i[2]
                        udp_port = i[3]
                        info_hash = i[4]
                        tcp_port = i[5]
                        application_command_commander_keyword = i[6]
                        distributed_hash_table.database_append_node_messages.put(
                            [node_id, ip_address, udp_port]
                        )
                        result = {
                            'result': {
                                'node_id': node_id,
                                'ip_address': ip_address,
                                'storing': True,
                                'udp_port': udp_port
                            },
                            'header': {
                                'info_hash': info_hash,
                                'tcp_port': tcp_port
                            }
                        }
                        self.application_command_announce_peer_messages_send.put(
                            [result, application_command_commander_keyword]
                        )
                        self.application_command_announce_peer_operators.put(
                            ['remove', i]
                        )

    def __send(self):
        while True:
            application_command_announce_peer_messages_recvfrom = self.application_command_announce_peer_messages_recvfrom.get()
            info_hash = application_command_announce_peer_messages_recvfrom[0]
            tcp_port = application_command_announce_peer_messages_recvfrom[1]
            application_command_commander_keyword = application_command_announce_peer_messages_recvfrom[2]
            token_manager.database_query_token_messages_recvfrom.put(
                info_hash
            )
            database_query_token_messages_send = token_manager.database_query_token_messages_send.get()
            if len(database_query_token_messages_send) == 0:
                result = {
                    'result': {
                        'node_id': None,
                        'ip_address': None,
                        'storing': False,
                        'udp_port': None
                    },
                    'header': {
                        'info_hash': info_hash,
                        'tcp_port': tcp_port
                    }
                }
                self.application_command_announce_peer_messages_send.put(
                    [result, application_command_commander_keyword]
                )
            else:
                node_id = database_query_token_messages_send[0]
                ip_address = database_query_token_messages_send[1]
                udp_port = database_query_token_messages_send[2]
                token = database_query_token_messages_send[3]
                application_command_announce_peer_keyword = os.urandom(20).hex()
                client.application_client_announce_peer_messages_recvfrom.put(
                    ['application_command_announce_peer', info_hash, tcp_port, token, ip_address, udp_port, application_command_announce_peer_keyword]
                )
                self.application_command_announce_peer_operators.put(
                    ['append', [application_command_announce_peer_keyword, node_id, ip_address, udp_port, info_hash, tcp_port, application_command_commander_keyword, int(time.time())]]
                )

    def start(self):
        explorer_krpc_v4_application_command_announce_peer_check_thread = threading.Thread(target = self.__check)
        explorer_krpc_v4_application_command_announce_peer_check_thread.setDaemon(True)
        explorer_krpc_v4_application_command_announce_peer_check_thread.start()
        explorer_krpc_v4_application_command_announce_peer_operators_thread = threading.Thread(target = self.__operators)
        explorer_krpc_v4_application_command_announce_peer_operators_thread.setDaemon(True)
        explorer_krpc_v4_application_command_announce_peer_operators_thread.start()
        explorer_krpc_v4_application_command_announce_peer_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_application_command_announce_peer_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_application_command_announce_peer_recvfrom_thread.start()
        explorer_krpc_v4_application_command_announce_peer_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v4_application_command_announce_peer_send_thread.setDaemon(True)
        explorer_krpc_v4_application_command_announce_peer_send_thread.start()