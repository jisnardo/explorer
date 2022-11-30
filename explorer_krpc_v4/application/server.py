from ..database.distributed_hash_table import distributed_hash_table
from ..database.peer_database import peer_database
from ..driver.control import control
from ..driver.memory import memory
import binascii
import crc32c
import IPy
import random
import re
import socket
import threading
import time

class server:
    application_server_request_info_hash = []

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

    def __check_request_info_hash(self):
        time.sleep(3600)
        while True:
            self.application_server_request_info_hash.clear()
            time.sleep(3600)

    def __recvfrom(self):
        while True:
            driver_control_server_messages = control().driver_control_server_messages.get()
            node_id = driver_control_server_messages[0]
            transaction_id = driver_control_server_messages[1]
            query = driver_control_server_messages[2]
            tcp_port = driver_control_server_messages[3]
            token = driver_control_server_messages[4]
            target_id = driver_control_server_messages[5]
            info_hash = driver_control_server_messages[6]
            ip_address = driver_control_server_messages[7]
            udp_port = driver_control_server_messages[8]
            check_node_result = self.__check_node(node_id, ip_address)
            if check_node_result is True:
                if not node_id == memory.node_id:
                    ip_address_type = IPy.IP(ip_address).iptype()
                    if ip_address_type == 'PUBLIC':
                        if 1 <= udp_port <= 65535:
                            if query == 'announce_peer':
                                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                match = re.match(pattern, info_hash.lower())
                                if match is not None:
                                    if 1 <= tcp_port <= 65535:
                                        if token == memory.token:
                                            distributed_hash_table.database_append_node_messages.put(
                                                [node_id, ip_address, udp_port]
                                            )
                                            peer_database.database_append_peer_messages.put(
                                                [match.group(0), ip_address, tcp_port]
                                            )
                                            control().response_announce_peer(transaction_id, ip_address, udp_port)
                            if query == 'find_node':
                                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                match = re.match(pattern, target_id.lower())
                                if match is not None:
                                    distributed_hash_table.database_append_node_messages.put(
                                        [node_id, ip_address, udp_port]
                                    )
                                    distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                                        match.group(0)
                                    )
                                    nodes = distributed_hash_table.database_query_nodes_messages_send.get()
                                    control().response_find_node(transaction_id, nodes, ip_address, udp_port)
                            if query == 'get_peers':
                                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                match = re.match(pattern, info_hash.lower())
                                if match is not None:
                                    if match.group(0) not in self.application_server_request_info_hash:
                                        self.application_server_request_info_hash.append(match.group(0))
                                    distributed_hash_table.database_append_node_messages.put(
                                        [node_id, ip_address, udp_port]
                                    )
                                    distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                                        match.group(0)
                                    )
                                    nodes = distributed_hash_table.database_query_nodes_messages_send.get()
                                    peer_database.database_query_peers_messages_recvfrom.put(
                                        match.group(0)
                                    )
                                    values = peer_database.database_query_peers_messages_send.get()
                                    control().response_get_peers(transaction_id, nodes, values, ip_address, udp_port)
                            if query == 'ping':
                                distributed_hash_table.database_append_node_messages.put(
                                    [node_id, ip_address, udp_port]
                                )
                                control().response_ping(transaction_id, ip_address, udp_port)
                            if query == 'sample_infohashes':
                                pattern = re.compile(r'\b[0-9a-f]{40}\b')
                                match = re.match(pattern, target_id.lower())
                                if match is not None:
                                    if node_id[:1] == match.group(0)[:1]:
                                        distributed_hash_table.database_append_node_messages.put(
                                            [node_id, ip_address, udp_port]
                                        )
                                        distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                                            match.group(0)
                                        )
                                        nodes = distributed_hash_table.database_query_nodes_messages_send.get()
                                        peer_database.database_query_info_hashes_messages_recvfrom.put(
                                            0
                                        )
                                        samples = peer_database.database_query_info_hashes_messages_send.get()
                                        number = len(samples)
                                        control().response_sample_infohashes(transaction_id, nodes, number, samples, ip_address, udp_port)

    def start(self):
        explorer_krpc_v4_application_server_check_request_info_hash_thread = threading.Thread(target = self.__check_request_info_hash)
        explorer_krpc_v4_application_server_check_request_info_hash_thread.setDaemon(True)
        explorer_krpc_v4_application_server_check_request_info_hash_thread.start()
        explorer_krpc_v4_application_server_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_application_server_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_application_server_recvfrom_thread.start()