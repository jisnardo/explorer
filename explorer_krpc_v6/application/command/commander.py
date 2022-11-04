from ...application.command.announce_peer import announce_peer
from ...application.command.find_node import find_node
from ...application.command.get_peers import get_peers
from ...application.command.ping import ping
from ...application.command.sample_infohashes import sample_infohashes
import os
import queue
import threading

class commander:
    application_commander_announce_peer_messages_key = []
    application_commander_announce_peer_messages_operators = queue.Queue()
    application_commander_announce_peer_messages_recvfrom = queue.Queue()
    application_commander_announce_peer_messages_send = queue.Queue()
    application_commander_find_node_messages_key = []
    application_commander_find_node_messages_operators = queue.Queue()
    application_commander_find_node_messages_recvfrom = queue.Queue()
    application_commander_find_node_messages_send = queue.Queue()
    application_commander_get_peers_messages_key = []
    application_commander_get_peers_messages_operators = queue.Queue()
    application_commander_get_peers_messages_recvfrom = queue.Queue()
    application_commander_get_peers_messages_send = queue.Queue()
    application_commander_ping_messages_key = []
    application_commander_ping_messages_operators = queue.Queue()
    application_commander_ping_messages_recvfrom = queue.Queue()
    application_commander_ping_messages_send = queue.Queue()
    application_commander_sample_infohashes_messages_key = []
    application_commander_sample_infohashes_messages_operators = queue.Queue()
    application_commander_sample_infohashes_messages_recvfrom = queue.Queue()
    application_commander_sample_infohashes_messages_send = queue.Queue()

    def __announce_peer_operators(self):
        while True:
            application_commander_announce_peer_messages_operators = self.application_commander_announce_peer_messages_operators.get()
            operate = application_commander_announce_peer_messages_operators[0]
            element = application_commander_announce_peer_messages_operators[1]
            if operate == 'append':
                if element not in self.application_commander_announce_peer_messages_key:
                    self.application_commander_announce_peer_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_commander_announce_peer_messages_key:
                    self.application_commander_announce_peer_messages_key.remove(element)

    def __announce_peer_request(self):
        while True:
            application_commander_announce_peer_messages_recvfrom = self.application_commander_announce_peer_messages_recvfrom.get()
            info_hash = application_commander_announce_peer_messages_recvfrom[0]
            tcp_port = application_commander_announce_peer_messages_recvfrom[1]
            application_command_commander_keyword = os.urandom(20).hex()
            announce_peer.application_command_announce_peer_messages_recvfrom.put(
                [info_hash, tcp_port, application_command_commander_keyword]
            )
            self.application_commander_announce_peer_messages_operators.put(
                ['append', [application_command_commander_keyword]]
            )

    def __announce_peer_response(self):
        while True:
            application_command_announce_peer_messages_send = announce_peer.application_command_announce_peer_messages_send.get()
            result = application_command_announce_peer_messages_send[0]
            application_command_commander_keyword = application_command_announce_peer_messages_send[1]
            for i in self.application_commander_announce_peer_messages_key:
                if i[0] == application_command_commander_keyword:
                    self.application_commander_announce_peer_messages_send.put(
                        result
                    )
                    self.application_commander_announce_peer_messages_operators.put(
                        ['remove', i]
                    )

    def __find_node_operators(self):
        while True:
            application_commander_find_node_messages_operators = self.application_commander_find_node_messages_operators.get()
            operate = application_commander_find_node_messages_operators[0]
            element = application_commander_find_node_messages_operators[1]
            if operate == 'append':
                if element not in self.application_commander_find_node_messages_key:
                    self.application_commander_find_node_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_commander_find_node_messages_key:
                    self.application_commander_find_node_messages_key.remove(element)

    def __find_node_request(self):
        while True:
            application_commander_find_node_messages_recvfrom = self.application_commander_find_node_messages_recvfrom.get()
            target_id = application_commander_find_node_messages_recvfrom[0]
            application_command_commander_keyword = os.urandom(20).hex()
            find_node.application_command_find_node_messages_recvfrom.put(
                [target_id, application_command_commander_keyword]
            )
            self.application_commander_find_node_messages_operators.put(
                ['append', [application_command_commander_keyword]]
            )

    def __find_node_response(self):
        while True:
            application_command_find_node_messages_send = find_node.application_command_find_node_messages_send.get()
            result = application_command_find_node_messages_send[0]
            application_command_commander_keyword = application_command_find_node_messages_send[1]
            for i in self.application_commander_find_node_messages_key:
                if i[0] == application_command_commander_keyword:
                    self.application_commander_find_node_messages_send.put(
                        result
                    )
                    self.application_commander_find_node_messages_operators.put(
                        ['remove', i]
                    )

    def __get_peers_operators(self):
        while True:
            application_commander_get_peers_messages_operators = self.application_commander_get_peers_messages_operators.get()
            operate = application_commander_get_peers_messages_operators[0]
            element = application_commander_get_peers_messages_operators[1]
            if operate == 'append':
                if element not in self.application_commander_get_peers_messages_key:
                    self.application_commander_get_peers_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_commander_get_peers_messages_key:
                    self.application_commander_get_peers_messages_key.remove(element)

    def __get_peers_request(self):
        while True:
            application_commander_get_peers_messages_recvfrom = self.application_commander_get_peers_messages_recvfrom.get()
            info_hash = application_commander_get_peers_messages_recvfrom[0]
            application_command_commander_keyword = os.urandom(20).hex()
            get_peers.application_command_get_peers_messages_recvfrom.put(
                [info_hash, application_command_commander_keyword]
            )
            self.application_commander_get_peers_messages_operators.put(
                ['append', [application_command_commander_keyword]]
            )

    def __get_peers_response(self):
        while True:
            application_command_get_peers_messages_send = get_peers.application_command_get_peers_messages_send.get()
            result = application_command_get_peers_messages_send[0]
            application_command_commander_keyword = application_command_get_peers_messages_send[1]
            for i in self.application_commander_get_peers_messages_key:
                if i[0] == application_command_commander_keyword:
                    self.application_commander_get_peers_messages_send.put(
                        result
                    )
                    self.application_commander_get_peers_messages_operators.put(
                        ['remove', i]
                    )

    def __ping_operators(self):
        while True:
            application_commander_ping_messages_operators = self.application_commander_ping_messages_operators.get()
            operate = application_commander_ping_messages_operators[0]
            element = application_commander_ping_messages_operators[1]
            if operate == 'append':
                if element not in self.application_commander_ping_messages_key:
                    self.application_commander_ping_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_commander_ping_messages_key:
                    self.application_commander_ping_messages_key.remove(element)

    def __ping_request(self):
        while True:
            application_commander_ping_messages_recvfrom = self.application_commander_ping_messages_recvfrom.get()
            ip_address = application_commander_ping_messages_recvfrom[0]
            udp_port = application_commander_ping_messages_recvfrom[1]
            application_command_commander_keyword = os.urandom(20).hex()
            ping.application_command_ping_messages_recvfrom.put(
                [ip_address, udp_port, application_command_commander_keyword]
            )
            self.application_commander_ping_messages_operators.put(
                ['append', [application_command_commander_keyword]]
            )

    def __ping_response(self):
        while True:
            application_command_ping_messages_send = ping.application_command_ping_messages_send.get()
            result = application_command_ping_messages_send[0]
            application_command_commander_keyword = application_command_ping_messages_send[1]
            for i in self.application_commander_ping_messages_key:
                if i[0] == application_command_commander_keyword:
                    self.application_commander_ping_messages_send.put(
                        result
                    )
                    self.application_commander_ping_messages_operators.put(
                        ['remove', i]
                    )

    def __sample_infohashes_operators(self):
        while True:
            application_commander_sample_infohashes_messages_operators = self.application_commander_sample_infohashes_messages_operators.get()
            operate = application_commander_sample_infohashes_messages_operators[0]
            element = application_commander_sample_infohashes_messages_operators[1]
            if operate == 'append':
                if element not in self.application_commander_sample_infohashes_messages_key:
                    self.application_commander_sample_infohashes_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_commander_sample_infohashes_messages_key:
                    self.application_commander_sample_infohashes_messages_key.remove(element)

    def __sample_infohashes_request(self):
        while True:
            application_commander_sample_infohashes_messages_recvfrom = self.application_commander_sample_infohashes_messages_recvfrom.get()
            target_id = application_commander_sample_infohashes_messages_recvfrom[0]
            application_command_commander_keyword = os.urandom(20).hex()
            sample_infohashes.application_command_sample_infohashes_messages_recvfrom.put(
                [target_id, application_command_commander_keyword]
            )
            self.application_commander_sample_infohashes_messages_operators.put(
                ['append', [application_command_commander_keyword]]
            )

    def __sample_infohashes_response(self):
        while True:
            application_command_sample_infohashes_messages_send = sample_infohashes.application_command_sample_infohashes_messages_send.get()
            result = application_command_sample_infohashes_messages_send[0]
            application_command_commander_keyword = application_command_sample_infohashes_messages_send[1]
            for i in self.application_commander_sample_infohashes_messages_key:
                if i[0] == application_command_commander_keyword:
                    self.application_commander_sample_infohashes_messages_send.put(
                        result
                    )
                    self.application_commander_sample_infohashes_messages_operators.put(
                        ['remove', i]
                    )

    def start(self):
        explorer_krpc_v6_application_command_commander_announce_peer_operators_thread = threading.Thread(target = self.__announce_peer_operators)
        explorer_krpc_v6_application_command_commander_announce_peer_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_announce_peer_operators_thread.start()
        explorer_krpc_v6_application_command_commander_announce_peer_request_thread = threading.Thread(target = self.__announce_peer_request)
        explorer_krpc_v6_application_command_commander_announce_peer_request_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_announce_peer_request_thread.start()
        explorer_krpc_v6_application_command_commander_announce_peer_response_thread = threading.Thread(target = self.__announce_peer_response)
        explorer_krpc_v6_application_command_commander_announce_peer_response_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_announce_peer_response_thread.start()
        explorer_krpc_v6_application_command_commander_find_node_operators_thread = threading.Thread(target = self.__find_node_operators)
        explorer_krpc_v6_application_command_commander_find_node_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_find_node_operators_thread.start()
        explorer_krpc_v6_application_command_commander_find_node_request_thread = threading.Thread(target = self.__find_node_request)
        explorer_krpc_v6_application_command_commander_find_node_request_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_find_node_request_thread.start()
        explorer_krpc_v6_application_command_commander_find_node_response_thread = threading.Thread(target = self.__find_node_response)
        explorer_krpc_v6_application_command_commander_find_node_response_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_find_node_response_thread.start()
        explorer_krpc_v6_application_command_commander_get_peers_operators_thread = threading.Thread(target = self.__get_peers_operators)
        explorer_krpc_v6_application_command_commander_get_peers_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_get_peers_operators_thread.start()
        explorer_krpc_v6_application_command_commander_get_peers_request_thread = threading.Thread(target = self.__get_peers_request)
        explorer_krpc_v6_application_command_commander_get_peers_request_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_get_peers_request_thread.start()
        explorer_krpc_v6_application_command_commander_get_peers_response_thread = threading.Thread(target = self.__get_peers_response)
        explorer_krpc_v6_application_command_commander_get_peers_response_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_get_peers_response_thread.start()
        explorer_krpc_v6_application_command_commander_ping_operators_thread = threading.Thread(target = self.__ping_operators)
        explorer_krpc_v6_application_command_commander_ping_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_ping_operators_thread.start()
        explorer_krpc_v6_application_command_commander_ping_request_thread = threading.Thread(target = self.__ping_request)
        explorer_krpc_v6_application_command_commander_ping_request_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_ping_request_thread.start()
        explorer_krpc_v6_application_command_commander_ping_response_thread = threading.Thread(target = self.__ping_response)
        explorer_krpc_v6_application_command_commander_ping_response_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_ping_response_thread.start()
        explorer_krpc_v6_application_command_commander_sample_infohashes_operators_thread = threading.Thread(target = self.__sample_infohashes_operators)
        explorer_krpc_v6_application_command_commander_sample_infohashes_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_sample_infohashes_operators_thread.start()
        explorer_krpc_v6_application_command_commander_sample_infohashes_request_thread = threading.Thread(target = self.__sample_infohashes_request)
        explorer_krpc_v6_application_command_commander_sample_infohashes_request_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_sample_infohashes_request_thread.start()
        explorer_krpc_v6_application_command_commander_sample_infohashes_response_thread = threading.Thread(target = self.__sample_infohashes_response)
        explorer_krpc_v6_application_command_commander_sample_infohashes_response_thread.setDaemon(True)
        explorer_krpc_v6_application_command_commander_sample_infohashes_response_thread.start()