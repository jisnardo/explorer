from ..database.distributed_hash_table import distributed_hash_table
from ..database.peer_database import peer_database
from ..driver.control import control
from ..driver.memory import memory
import IPy
import re
import threading

class server:
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
            if not node_id == memory.node_id:
                ip_address_type = IPy.IP(ip_address).iptype()[:9]
                if ip_address_type == 'ALLOCATED':
                    if 1 <= udp_port <= 65535:
                        distributed_hash_table.database_append_node_messages.put(
                            [node_id, ip_address, udp_port]
                        )
                        if query == 'announce_peer':
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, info_hash.lower())
                            if match is not None:
                                if 1 <= tcp_port <= 65535:
                                    if token == memory.token:
                                        peer_database.database_append_peer_messages.put(
                                            [match.group(0), ip_address, tcp_port]
                                        )
                                        control().response_announce_peer(transaction_id, ip_address, udp_port)
                        if query == 'find_node':
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, target_id.lower())
                            if match is not None:
                                distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                                    match.group(0)
                                )
                                nodes6 = distributed_hash_table.database_query_nodes_messages_send.get()
                                control().response_find_node(transaction_id, nodes6, ip_address, udp_port)
                        if query == 'get_peers':
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, info_hash.lower())
                            if match is not None:
                                distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                                    match.group(0)
                                )
                                nodes6 = distributed_hash_table.database_query_nodes_messages_send.get()
                                peer_database.database_query_peers_messages_recvfrom.put(
                                    match.group(0)
                                )
                                values = peer_database.database_query_peers_messages_send.get()
                                control().response_get_peers(transaction_id, nodes6, values, ip_address, udp_port)
                        if query == 'ping':
                            control().response_ping(transaction_id, ip_address, udp_port)
                        if query == 'sample_infohashes':
                            pattern = re.compile(r'\b[0-9a-f]{40}\b')
                            match = re.match(pattern, target_id.lower())
                            if match is not None:
                                distributed_hash_table.database_query_nodes_messages_recvfrom.put(
                                    match.group(0)
                                )
                                nodes6 = distributed_hash_table.database_query_nodes_messages_send.get()
                                peer_database.database_query_info_hashes_messages_recvfrom.put(
                                    0
                                )
                                samples = peer_database.database_query_info_hashes_messages_send.get()
                                number = len(samples)
                                control().response_sample_infohashes(transaction_id, nodes6, number, samples, ip_address, udp_port)

    def start(self):
        explorer_krpc_v6_application_server_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v6_application_server_recvfrom_thread.setDaemon(True)
        explorer_krpc_v6_application_server_recvfrom_thread.start()