from ..driver.control import control
import os
import queue
import threading
import time

class client:
    application_client_announce_peer_messages_key = []
    application_client_announce_peer_messages_operators = queue.Queue()
    application_client_announce_peer_messages_recvfrom = queue.Queue()
    application_client_announce_peer_messages_send_application_command_announce_peer = queue.Queue()
    application_client_find_node_messages_key = []
    application_client_find_node_messages_operators = queue.Queue()
    application_client_find_node_messages_recvfrom = queue.Queue()
    application_client_find_node_messages_send_application_bootstrap_nodes_find_node = queue.Queue()
    application_client_find_node_messages_send_application_command_find_node = queue.Queue()
    application_client_find_node_messages_send_application_neighbor_nodes_find_node = queue.Queue()
    application_client_find_node_messages_send_database_find_node = queue.Queue()
    application_client_get_peers_messages_key = []
    application_client_get_peers_messages_operators = queue.Queue()
    application_client_get_peers_messages_recvfrom = queue.Queue()
    application_client_get_peers_messages_send_application_command_get_peers = queue.Queue()
    application_client_ping_messages_key = []
    application_client_ping_messages_operators = queue.Queue()
    application_client_ping_messages_recvfrom = queue.Queue()
    application_client_ping_messages_send_application_bootstrap_nodes_ping = queue.Queue()
    application_client_ping_messages_send_application_command_ping = queue.Queue()
    application_client_ping_messages_send_database_ping = queue.Queue()
    application_client_sample_infohashes_messages_key = []
    application_client_sample_infohashes_messages_operators = queue.Queue()
    application_client_sample_infohashes_messages_recvfrom = queue.Queue()
    application_client_sample_infohashes_messages_send_application_command_sample_infohashes = queue.Queue()

    def __announce_peer_check(self):
        while True:
            if len(self.application_client_announce_peer_messages_key) > 0:
                for i in self.application_client_announce_peer_messages_key:
                    if i[3] < int(time.time()) - 300:
                        self.application_client_announce_peer_messages_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __announce_peer_operators(self):
        while True:
            application_client_announce_peer_messages_operators = self.application_client_announce_peer_messages_operators.get()
            operate = application_client_announce_peer_messages_operators[0]
            element = application_client_announce_peer_messages_operators[1]
            if operate == 'append':
                if element not in self.application_client_announce_peer_messages_key:
                    self.application_client_announce_peer_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_client_announce_peer_messages_key:
                    self.application_client_announce_peer_messages_key.remove(element)

    def __announce_peer_request(self):
        while True:
            application_client_announce_peer_messages_recvfrom = self.application_client_announce_peer_messages_recvfrom.get()
            application_name = application_client_announce_peer_messages_recvfrom[0]
            info_hash = application_client_announce_peer_messages_recvfrom[1]
            tcp_port = application_client_announce_peer_messages_recvfrom[2]
            token = application_client_announce_peer_messages_recvfrom[3]
            ip_address = application_client_announce_peer_messages_recvfrom[4]
            udp_port = application_client_announce_peer_messages_recvfrom[5]
            application_keyword = application_client_announce_peer_messages_recvfrom[6]
            announce_peer_keyword = os.urandom(20).hex()
            control().request_announce_peer('announce_peer', info_hash, tcp_port, token, ip_address, udp_port, announce_peer_keyword)
            self.application_client_announce_peer_messages_operators.put(
                ['append', [announce_peer_keyword, application_name, application_keyword, int(time.time())]]
            )

    def __announce_peer_response(self):
        while True:
            driver_control_announce_peer_messages = control().driver_control_announce_peer_messages.get()
            if driver_control_announce_peer_messages[0] is False:
                announce_peer_keyword = driver_control_announce_peer_messages[1]
                for i in self.application_client_announce_peer_messages_key:
                    if i[0] == announce_peer_keyword:
                        if i[1] == 'application_command_announce_peer':
                            application_keyword = i[2]
                            self.application_client_announce_peer_messages_send_application_command_announce_peer.put(
                                [False, application_keyword]
                            )
                        self.application_client_announce_peer_messages_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = driver_control_announce_peer_messages[0]
                nodes6 = driver_control_announce_peer_messages[1]
                values = driver_control_announce_peer_messages[2]
                samples = driver_control_announce_peer_messages[3]
                token = driver_control_announce_peer_messages[4]
                ip_address = driver_control_announce_peer_messages[5]
                udp_port = driver_control_announce_peer_messages[6]
                announce_peer_keyword = driver_control_announce_peer_messages[7]
                for i in self.application_client_announce_peer_messages_key:
                    if i[0] == announce_peer_keyword:
                        if i[1] == 'application_command_announce_peer':
                            application_keyword = i[2]
                            self.application_client_announce_peer_messages_send_application_command_announce_peer.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        self.application_client_announce_peer_messages_operators.put(
                            ['remove', i]
                        )

    def __find_node_check(self):
        while True:
            if len(self.application_client_find_node_messages_key) > 0:
                for i in self.application_client_find_node_messages_key:
                    if i[3] < int(time.time()) - 300:
                        self.application_client_find_node_messages_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __find_node_operators(self):
        while True:
            application_client_find_node_messages_operators = self.application_client_find_node_messages_operators.get()
            operate = application_client_find_node_messages_operators[0]
            element = application_client_find_node_messages_operators[1]
            if operate == 'append':
                if element not in self.application_client_find_node_messages_key:
                    self.application_client_find_node_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_client_find_node_messages_key:
                    self.application_client_find_node_messages_key.remove(element)

    def __find_node_request(self):
        while True:
            application_client_find_node_messages_recvfrom = self.application_client_find_node_messages_recvfrom.get()
            application_name = application_client_find_node_messages_recvfrom[0]
            target_id = application_client_find_node_messages_recvfrom[1]
            ip_address = application_client_find_node_messages_recvfrom[2]
            udp_port = application_client_find_node_messages_recvfrom[3]
            application_keyword = application_client_find_node_messages_recvfrom[4]
            find_node_keyword = os.urandom(20).hex()
            control().request_find_node('find_node', target_id, ip_address, udp_port, find_node_keyword)
            self.application_client_find_node_messages_operators.put(
                ['append', [find_node_keyword, application_name, application_keyword, int(time.time())]]
            )

    def __find_node_response(self):
        while True:
            driver_control_find_node_messages = control().driver_control_find_node_messages.get()
            if driver_control_find_node_messages[0] is False:
                find_node_keyword = driver_control_find_node_messages[1]
                for i in self.application_client_find_node_messages_key:
                    if i[0] == find_node_keyword:
                        if i[1] == 'application_bootstrap_nodes_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_application_bootstrap_nodes_find_node.put(
                                [False, application_keyword]
                            )
                        if i[1] == 'application_command_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_application_command_find_node.put(
                                [False, application_keyword]
                            )
                        if i[1] == 'application_neighbor_nodes_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_application_neighbor_nodes_find_node.put(
                                [False, application_keyword]
                            )
                        if i[1] == 'database_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_database_find_node.put(
                                [False, application_keyword]
                            )
                        self.application_client_find_node_messages_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = driver_control_find_node_messages[0]
                nodes6 = driver_control_find_node_messages[1]
                values = driver_control_find_node_messages[2]
                samples = driver_control_find_node_messages[3]
                token = driver_control_find_node_messages[4]
                ip_address = driver_control_find_node_messages[5]
                udp_port = driver_control_find_node_messages[6]
                find_node_keyword = driver_control_find_node_messages[7]
                for i in self.application_client_find_node_messages_key:
                    if i[0] == find_node_keyword:
                        if i[1] == 'application_bootstrap_nodes_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_application_bootstrap_nodes_find_node.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        if i[1] == 'application_command_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_application_command_find_node.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        if i[1] == 'application_neighbor_nodes_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_application_neighbor_nodes_find_node.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        if i[1] == 'database_find_node':
                            application_keyword = i[2]
                            self.application_client_find_node_messages_send_database_find_node.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        self.application_client_find_node_messages_operators.put(
                            ['remove', i]
                        )

    def __get_peers_check(self):
        while True:
            if len(self.application_client_get_peers_messages_key) > 0:
                for i in self.application_client_get_peers_messages_key:
                    if i[3] < int(time.time()) - 300:
                        self.application_client_get_peers_messages_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __get_peers_operators(self):
        while True:
            application_client_get_peers_messages_operators = self.application_client_get_peers_messages_operators.get()
            operate = application_client_get_peers_messages_operators[0]
            element = application_client_get_peers_messages_operators[1]
            if operate == 'append':
                if element not in self.application_client_get_peers_messages_key:
                    self.application_client_get_peers_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_client_get_peers_messages_key:
                    self.application_client_get_peers_messages_key.remove(element)

    def __get_peers_request(self):
        while True:
            application_client_get_peers_messages_recvfrom = self.application_client_get_peers_messages_recvfrom.get()
            application_name = application_client_get_peers_messages_recvfrom[0]
            info_hash = application_client_get_peers_messages_recvfrom[1]
            ip_address = application_client_get_peers_messages_recvfrom[2]
            udp_port = application_client_get_peers_messages_recvfrom[3]
            application_keyword = application_client_get_peers_messages_recvfrom[4]
            get_peers_keyword = os.urandom(20).hex()
            control().request_get_peers('get_peers', info_hash, ip_address, udp_port, get_peers_keyword)
            self.application_client_get_peers_messages_operators.put(
                ['append', [get_peers_keyword, application_name, application_keyword, int(time.time())]]
            )

    def __get_peers_response(self):
        while True:
            driver_control_get_peers_messages = control().driver_control_get_peers_messages.get()
            if driver_control_get_peers_messages[0] is False:
                get_peers_keyword = driver_control_get_peers_messages[1]
                for i in self.application_client_get_peers_messages_key:
                    if i[0] == get_peers_keyword:
                        if i[1] == 'application_command_get_peers':
                            application_keyword = i[2]
                            self.application_client_get_peers_messages_send_application_command_get_peers.put(
                                [False, application_keyword]
                            )
                        self.application_client_get_peers_messages_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = driver_control_get_peers_messages[0]
                nodes6 = driver_control_get_peers_messages[1]
                values = driver_control_get_peers_messages[2]
                samples = driver_control_get_peers_messages[3]
                token = driver_control_get_peers_messages[4]
                ip_address = driver_control_get_peers_messages[5]
                udp_port = driver_control_get_peers_messages[6]
                get_peers_keyword = driver_control_get_peers_messages[7]
                for i in self.application_client_get_peers_messages_key:
                    if i[0] == get_peers_keyword:
                        if i[1] == 'application_command_get_peers':
                            application_keyword = i[2]
                            self.application_client_get_peers_messages_send_application_command_get_peers.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        self.application_client_get_peers_messages_operators.put(
                            ['remove', i]
                        )

    def __ping_check(self):
        while True:
            if len(self.application_client_ping_messages_key) > 0:
                for i in self.application_client_ping_messages_key:
                    if i[3] < int(time.time()) - 300:
                        self.application_client_ping_messages_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __ping_operators(self):
        while True:
            application_client_ping_messages_operators = self.application_client_ping_messages_operators.get()
            operate = application_client_ping_messages_operators[0]
            element = application_client_ping_messages_operators[1]
            if operate == 'append':
                if element not in self.application_client_ping_messages_key:
                    self.application_client_ping_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_client_ping_messages_key:
                    self.application_client_ping_messages_key.remove(element)

    def __ping_request(self):
        while True:
            application_client_ping_messages_recvfrom = self.application_client_ping_messages_recvfrom.get()
            application_name = application_client_ping_messages_recvfrom[0]
            ip_address = application_client_ping_messages_recvfrom[1]
            udp_port = application_client_ping_messages_recvfrom[2]
            application_keyword = application_client_ping_messages_recvfrom[3]
            ping_keyword = os.urandom(20).hex()
            control().request_ping('ping', ip_address, udp_port, ping_keyword)
            self.application_client_ping_messages_operators.put(
                ['append', [ping_keyword, application_name, application_keyword, int(time.time())]]
            )

    def __ping_response(self):
        while True:
            driver_control_ping_messages = control().driver_control_ping_messages.get()
            if driver_control_ping_messages[0] is False:
                ping_keyword = driver_control_ping_messages[1]
                for i in self.application_client_ping_messages_key:
                    if i[0] == ping_keyword:
                        if i[1] == 'application_bootstrap_nodes_ping':
                            application_keyword = i[2]
                            self.application_client_ping_messages_send_application_bootstrap_nodes_ping.put(
                                [False, application_keyword]
                            )
                        if i[1] == 'application_command_ping':
                            application_keyword = i[2]
                            self.application_client_ping_messages_send_application_command_ping.put(
                                [False, application_keyword]
                            )
                        if i[1] == 'database_ping':
                            application_keyword = i[2]
                            self.application_client_ping_messages_send_database_ping.put(
                                [False, application_keyword]
                            )
                        self.application_client_ping_messages_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = driver_control_ping_messages[0]
                nodes6 = driver_control_ping_messages[1]
                values = driver_control_ping_messages[2]
                samples = driver_control_ping_messages[3]
                token = driver_control_ping_messages[4]
                ip_address = driver_control_ping_messages[5]
                udp_port = driver_control_ping_messages[6]
                ping_keyword = driver_control_ping_messages[7]
                for i in self.application_client_ping_messages_key:
                    if i[0] == ping_keyword:
                        if i[1] == 'application_bootstrap_nodes_ping':
                            application_keyword = i[2]
                            self.application_client_ping_messages_send_application_bootstrap_nodes_ping.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        if i[1] == 'application_command_ping':
                            application_keyword = i[2]
                            self.application_client_ping_messages_send_application_command_ping.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        if i[1] == 'database_ping':
                            application_keyword = i[2]
                            self.application_client_ping_messages_send_database_ping.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        self.application_client_ping_messages_operators.put(
                            ['remove', i]
                        )

    def __sample_infohashes_check(self):
        while True:
            if len(self.application_client_sample_infohashes_messages_key) > 0:
                for i in self.application_client_sample_infohashes_messages_key:
                    if i[3] < int(time.time()) - 300:
                        self.application_client_sample_infohashes_messages_operators.put(
                            ['remove', i]
                        )
            time.sleep(300)

    def __sample_infohashes_operators(self):
        while True:
            application_client_sample_infohashes_messages_operators = self.application_client_sample_infohashes_messages_operators.get()
            operate = application_client_sample_infohashes_messages_operators[0]
            element = application_client_sample_infohashes_messages_operators[1]
            if operate == 'append':
                if element not in self.application_client_sample_infohashes_messages_key:
                    self.application_client_sample_infohashes_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_client_sample_infohashes_messages_key:
                    self.application_client_sample_infohashes_messages_key.remove(element)

    def __sample_infohashes_request(self):
        while True:
            application_client_sample_infohashes_messages_recvfrom = self.application_client_sample_infohashes_messages_recvfrom.get()
            application_name = application_client_sample_infohashes_messages_recvfrom[0]
            target_id = application_client_sample_infohashes_messages_recvfrom[1]
            ip_address = application_client_sample_infohashes_messages_recvfrom[2]
            udp_port = application_client_sample_infohashes_messages_recvfrom[3]
            application_keyword = application_client_sample_infohashes_messages_recvfrom[4]
            sample_infohashes_keyword = os.urandom(20).hex()
            control().request_sample_infohashes('sample_infohashes', target_id, ip_address, udp_port, sample_infohashes_keyword)
            self.application_client_sample_infohashes_messages_operators.put(
                ['append', [sample_infohashes_keyword, application_name, application_keyword, int(time.time())]]
            )

    def __sample_infohashes_response(self):
        while True:
            driver_control_sample_infohashes_messages = control().driver_control_sample_infohashes_messages.get()
            if driver_control_sample_infohashes_messages[0] is False:
                sample_infohashes_keyword = driver_control_sample_infohashes_messages[1]
                for i in self.application_client_sample_infohashes_messages_key:
                    if i[0] == sample_infohashes_keyword:
                        if i[1] == 'application_command_sample_infohashes':
                            application_keyword = i[2]
                            self.application_client_sample_infohashes_messages_send_application_command_sample_infohashes.put(
                                [False, application_keyword]
                            )
                        self.application_client_sample_infohashes_messages_operators.put(
                            ['remove', i]
                        )
            else:
                node_id = driver_control_sample_infohashes_messages[0]
                nodes6 = driver_control_sample_infohashes_messages[1]
                values = driver_control_sample_infohashes_messages[2]
                samples = driver_control_sample_infohashes_messages[3]
                token = driver_control_sample_infohashes_messages[4]
                ip_address = driver_control_sample_infohashes_messages[5]
                udp_port = driver_control_sample_infohashes_messages[6]
                sample_infohashes_keyword = driver_control_sample_infohashes_messages[7]
                for i in self.application_client_sample_infohashes_messages_key:
                    if i[0] == sample_infohashes_keyword:
                        if i[1] == 'application_command_sample_infohashes':
                            application_keyword = i[2]
                            self.application_client_sample_infohashes_messages_send_application_command_sample_infohashes.put(
                                [node_id, nodes6, values, samples, token, ip_address, udp_port, application_keyword]
                            )
                        self.application_client_sample_infohashes_messages_operators.put(
                            ['remove', i]
                        )

    def start(self):
        explorer_krpc_v6_application_client_announce_peer_check_thread = threading.Thread(target = self.__announce_peer_check)
        explorer_krpc_v6_application_client_announce_peer_check_thread.setDaemon(True)
        explorer_krpc_v6_application_client_announce_peer_check_thread.start()
        explorer_krpc_v6_application_client_announce_peer_operators_thread = threading.Thread(target = self.__announce_peer_operators)
        explorer_krpc_v6_application_client_announce_peer_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_client_announce_peer_operators_thread.start()
        explorer_krpc_v6_application_client_announce_peer_request_thread = threading.Thread(target = self.__announce_peer_request)
        explorer_krpc_v6_application_client_announce_peer_request_thread.setDaemon(True)
        explorer_krpc_v6_application_client_announce_peer_request_thread.start()
        explorer_krpc_v6_application_client_announce_peer_response_thread = threading.Thread(target = self.__announce_peer_response)
        explorer_krpc_v6_application_client_announce_peer_response_thread.setDaemon(True)
        explorer_krpc_v6_application_client_announce_peer_response_thread.start()
        explorer_krpc_v6_application_client_find_node_check_thread = threading.Thread(target = self.__find_node_check)
        explorer_krpc_v6_application_client_find_node_check_thread.setDaemon(True)
        explorer_krpc_v6_application_client_find_node_check_thread.start()
        explorer_krpc_v6_application_client_find_node_operators_thread = threading.Thread(target = self.__find_node_operators)
        explorer_krpc_v6_application_client_find_node_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_client_find_node_operators_thread.start()
        explorer_krpc_v6_application_client_find_node_request_thread = threading.Thread(target = self.__find_node_request)
        explorer_krpc_v6_application_client_find_node_request_thread.setDaemon(True)
        explorer_krpc_v6_application_client_find_node_request_thread.start()
        explorer_krpc_v6_application_client_find_node_response_thread = threading.Thread(target = self.__find_node_response)
        explorer_krpc_v6_application_client_find_node_response_thread.setDaemon(True)
        explorer_krpc_v6_application_client_find_node_response_thread.start()
        explorer_krpc_v6_application_client_get_peers_check_thread = threading.Thread(target = self.__get_peers_check)
        explorer_krpc_v6_application_client_get_peers_check_thread.setDaemon(True)
        explorer_krpc_v6_application_client_get_peers_check_thread.start()
        explorer_krpc_v6_application_client_get_peers_operators_thread = threading.Thread(target = self.__get_peers_operators)
        explorer_krpc_v6_application_client_get_peers_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_client_get_peers_operators_thread.start()
        explorer_krpc_v6_application_client_get_peers_request_thread = threading.Thread(target = self.__get_peers_request)
        explorer_krpc_v6_application_client_get_peers_request_thread.setDaemon(True)
        explorer_krpc_v6_application_client_get_peers_request_thread.start()
        explorer_krpc_v6_application_client_get_peers_response_thread = threading.Thread(target = self.__get_peers_response)
        explorer_krpc_v6_application_client_get_peers_response_thread.setDaemon(True)
        explorer_krpc_v6_application_client_get_peers_response_thread.start()
        explorer_krpc_v6_application_client_ping_check_thread = threading.Thread(target = self.__ping_check)
        explorer_krpc_v6_application_client_ping_check_thread.setDaemon(True)
        explorer_krpc_v6_application_client_ping_check_thread.start()
        explorer_krpc_v6_application_client_ping_operators_thread = threading.Thread(target = self.__ping_operators)
        explorer_krpc_v6_application_client_ping_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_client_ping_operators_thread.start()
        explorer_krpc_v6_application_client_ping_request_thread = threading.Thread(target = self.__ping_request)
        explorer_krpc_v6_application_client_ping_request_thread.setDaemon(True)
        explorer_krpc_v6_application_client_ping_request_thread.start()
        explorer_krpc_v6_application_client_ping_response_thread = threading.Thread(target = self.__ping_response)
        explorer_krpc_v6_application_client_ping_response_thread.setDaemon(True)
        explorer_krpc_v6_application_client_ping_response_thread.start()
        explorer_krpc_v6_application_client_sample_infohashes_check_thread = threading.Thread(target = self.__sample_infohashes_check)
        explorer_krpc_v6_application_client_sample_infohashes_check_thread.setDaemon(True)
        explorer_krpc_v6_application_client_sample_infohashes_check_thread.start()
        explorer_krpc_v6_application_client_sample_infohashes_operators_thread = threading.Thread(target = self.__sample_infohashes_operators)
        explorer_krpc_v6_application_client_sample_infohashes_operators_thread.setDaemon(True)
        explorer_krpc_v6_application_client_sample_infohashes_operators_thread.start()
        explorer_krpc_v6_application_client_sample_infohashes_request_thread = threading.Thread(target = self.__sample_infohashes_request)
        explorer_krpc_v6_application_client_sample_infohashes_request_thread.setDaemon(True)
        explorer_krpc_v6_application_client_sample_infohashes_request_thread.start()
        explorer_krpc_v6_application_client_sample_infohashes_response_thread = threading.Thread(target = self.__sample_infohashes_response)
        explorer_krpc_v6_application_client_sample_infohashes_response_thread.setDaemon(True)
        explorer_krpc_v6_application_client_sample_infohashes_response_thread.start()