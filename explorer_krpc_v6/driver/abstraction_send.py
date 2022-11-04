from ..driver.interface import krpc_server
from ..driver.memory import memory
from ..driver.packer import krpc_request_messages
from ..driver.packer import krpc_response_messages
import os
import socket
import struct

class send:
    def request_announce_peer(self, info_hash, tcp_port, token, ip_address, udp_port):
        transaction_id = b'ap\x00\x00' + os.urandom(4)
        message = krpc_request_messages().announce_peer(transaction_id, bytes.fromhex(memory.node_id), bytes.fromhex(info_hash), tcp_port, token)
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )
        return transaction_id

    def request_find_node(self, target_id, ip_address, udp_port):
        transaction_id = b'fn\x00\x00' + os.urandom(4)
        message = krpc_request_messages().find_node(transaction_id, bytes.fromhex(memory.node_id), bytes.fromhex(target_id))
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )
        return transaction_id

    def request_get_peers(self, info_hash, ip_address, udp_port):
        transaction_id = b'gp\x00\x00' + os.urandom(4)
        message = krpc_request_messages().get_peers(transaction_id, bytes.fromhex(memory.node_id), bytes.fromhex(info_hash))
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )
        return transaction_id

    def request_ping(self, ip_address, udp_port):
        transaction_id = b'pn\x00\x00' + os.urandom(4)
        message = krpc_request_messages().ping(transaction_id, bytes.fromhex(memory.node_id))
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )
        return transaction_id

    def request_sample_infohashes(self, target_id, ip_address, udp_port):
        transaction_id = b'si\x00\x00' + os.urandom(4)
        message = krpc_request_messages().sample_infohashes(transaction_id, bytes.fromhex(memory.node_id), bytes.fromhex(target_id))
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )
        return transaction_id

    def response_announce_peer(self, transaction_id, ip_address, udp_port):
        message = krpc_response_messages().announce_peer(transaction_id, bytes.fromhex(memory.node_id), ip_address, udp_port)
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )

    def response_find_node(self, transaction_id, nodes6, ip_address, udp_port):
        new_nodes6 = bytes()
        for i in nodes6:
            nodes6_node_id = bytes.fromhex(i[0])
            nodes6_ip_address = socket.inet_pton(socket.AF_INET6, i[1])
            nodes6_udp_port = struct.pack('!H', i[2])
            new_nodes6 = new_nodes6 + nodes6_node_id + nodes6_ip_address + nodes6_udp_port
        message = krpc_response_messages().find_node(transaction_id, bytes.fromhex(memory.node_id), new_nodes6, ip_address, udp_port)
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )

    def response_get_peers(self, transaction_id, nodes6, values, ip_address, udp_port):
        new_nodes6 = bytes()
        for i in nodes6:
            nodes6_node_id = bytes.fromhex(i[0])
            nodes6_ip_address = socket.inet_pton(socket.AF_INET6, i[1])
            nodes6_udp_port = struct.pack('!H', i[2])
            new_nodes6 = new_nodes6 + nodes6_node_id + nodes6_ip_address + nodes6_udp_port
        new_values = list()
        for i in values:
            values_ip_address = socket.inet_pton(socket.AF_INET6, i[0])
            values_tcp_port = struct.pack('!H', i[1])
            new_values.append(values_ip_address + values_tcp_port)
        message = krpc_response_messages().get_peers(transaction_id, bytes.fromhex(memory.node_id), new_nodes6, new_values, memory.token, ip_address, udp_port)
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )

    def response_ping(self, transaction_id, ip_address, udp_port):
        message = krpc_response_messages().ping(transaction_id, bytes.fromhex(memory.node_id), ip_address, udp_port)
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )

    def response_sample_infohashes(self, transaction_id, nodes6, number, samples, ip_address, udp_port):
        new_nodes6 = bytes()
        for i in nodes6:
            nodes6_node_id = bytes.fromhex(i[0])
            nodes6_ip_address = socket.inet_pton(socket.AF_INET6, i[1])
            nodes6_udp_port = struct.pack('!H', i[2])
            new_nodes6 = new_nodes6 + nodes6_node_id + nodes6_ip_address + nodes6_udp_port
        new_samples = bytes()
        for i in samples:
            info_hash = bytes.fromhex(i)
            new_samples = new_samples + info_hash
        message = krpc_response_messages().ping(transaction_id, bytes.fromhex(memory.node_id), new_nodes6, number, new_samples, ip_address, udp_port)
        krpc_server.driver_interface_send_messages.put(
            [message, ip_address, udp_port]
        )