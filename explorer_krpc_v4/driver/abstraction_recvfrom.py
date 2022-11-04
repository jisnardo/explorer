from ..driver.control import control
from ..driver.interface import krpc_server
import binascii
import crc32c
import IPy
import random
import re
import socket
import struct
import threading

class recvfrom:
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

    def __listen(self):
        while True:
            response = krpc_server().driver_interface_recvfrom_messages.get()
            if not response == None:
                message = response[0]
                server_address = response[1]
                if 'y' in message.keys():
                    if message['y'] == 'e':
                        transaction_id = message['t']
                        error_number = message['e'][0]
                        error_message = message['e'][1]
                        ip_address = server_address[0]
                        udp_port = server_address[1]
                        explorer_krpc_v4_driver_abstraction_recvfrom_listen_e_thread = threading.Thread(target = control().e_client, args = (transaction_id, error_number, error_message, ip_address, udp_port,))
                        explorer_krpc_v4_driver_abstraction_recvfrom_listen_e_thread.setDaemon(True)
                        explorer_krpc_v4_driver_abstraction_recvfrom_listen_e_thread.start()
                    if message['y'] == 'q':
                        if type(message['a'].get('id')) == bytes:
                            if len(message['a'].get('id')) == 20:
                                if 'v' in message:
                                    node_id = message['a'].get('id').hex()
                                    transaction_id = message['t']
                                    query = message['q']
                                    tcp_port = 0
                                    token = b''
                                    target_id = ''
                                    info_hash = ''
                                    ip_address = server_address[0]
                                    udp_port = server_address[1]
                                    check_node_result = self.__check_node(node_id, ip_address)
                                    if check_node_result is True:
                                        if 'port' in message['a']:
                                            if type(message['a'].get('port')) == int:
                                                tcp_port = message['a'].get('port')
                                        if 'token' in message['a']:
                                            if type(message['a'].get('token')) == bytes:
                                                token = message['a'].get('token')
                                        if 'target_id' in message['a']:
                                            if type(message['a'].get('target_id')) == bytes:
                                                target_id = message['a'].get('target_id').hex()
                                        if 'info_hash' in message['a']:
                                            if type(message['a'].get('info_hash')) == bytes:
                                                info_hash = message['a'].get('info_hash').hex()
                                        explorer_krpc_v4_driver_abstraction_recvfrom_listen_q_thread = threading.Thread(target = control().q_client, args = (node_id, transaction_id, query, tcp_port, token, target_id, info_hash, ip_address, udp_port,))
                                        explorer_krpc_v4_driver_abstraction_recvfrom_listen_q_thread.setDaemon(True)
                                        explorer_krpc_v4_driver_abstraction_recvfrom_listen_q_thread.start()
                    if message['y'] == 'r':
                        if type(message['r'].get('id')) == bytes:
                            if len(message['r'].get('id')) == 20:
                                if type(message['t']) == bytes:
                                    if 'v' in message:
                                        node_id = message['r'].get('id').hex()
                                        transaction_id = message['t']
                                        self_ip_address = ''
                                        self_udp_port = 0
                                        nodes = []
                                        values = []
                                        samples = []
                                        token = b''
                                        ip_address = server_address[0]
                                        udp_port = server_address[1]
                                        check_node_result = self.__check_node(node_id, ip_address)
                                        if check_node_result is True:
                                            if 'ip' in message:
                                                if type(message.get('ip')) == bytes:
                                                    self_ip_address = socket.inet_ntop(socket.AF_INET, message.get('ip')[:4])
                                            if 'p' in message['r']:
                                                if type(message['r'].get('p')) == int:
                                                    self_udp_port = message['r'].get('p')
                                            if 'nodes' in message['r']:
                                                if type(message['r'].get('nodes')) == bytes:
                                                    for i in range(0, len(message['r'].get('nodes')), 26):
                                                        nodes_node_id = message['r'].get('nodes')[i:i + 20].hex()
                                                        nodes_ip_address = socket.inet_ntop(socket.AF_INET, message['r'].get('nodes')[i + 20:i + 24])
                                                        nodes_udp_port = struct.unpack_from('!H', message['r'].get('nodes')[i + 24:i + 26])[0]
                                                        nodes.append([nodes_node_id, nodes_ip_address, nodes_udp_port])
                                            if 'values' in message['r']:
                                                if type(message['r'].get('values')) == list:
                                                    for i in message['r'].get('values'):
                                                        if type(i) == bytes:
                                                            if len(i) == 6:
                                                                values_ip_address = socket.inet_ntop(socket.AF_INET, i[:4])
                                                                values_tcp_port = struct.unpack_from('!H', i, 4)[0]
                                                                values.append([values_ip_address, values_tcp_port])
                                            if 'samples' in message['r']:
                                                if type(message['r'].get('samples')) == bytes:
                                                    for i in range(0, len(message['r'].get('samples')), 20):
                                                        info_hash = message['r'].get('samples')[i:i + 20].hex()
                                                        samples.append(info_hash)
                                            if 'token' in message['r']:
                                                if type(message['r'].get('token')) == bytes:
                                                    token = message['r'].get('token')
                                            explorer_krpc_v4_driver_abstraction_recvfrom_listen_r_thread = threading.Thread(target = control().r_client, args = (node_id, transaction_id, self_ip_address, self_udp_port, nodes, values, samples, token, ip_address, udp_port,))
                                            explorer_krpc_v4_driver_abstraction_recvfrom_listen_r_thread.setDaemon(True)
                                            explorer_krpc_v4_driver_abstraction_recvfrom_listen_r_thread.start()

    def start_listen(self):
        explorer_krpc_v4_driver_abstraction_recvfrom_listen_thread = threading.Thread(target = self.__listen)
        explorer_krpc_v4_driver_abstraction_recvfrom_listen_thread.setDaemon(True)
        explorer_krpc_v4_driver_abstraction_recvfrom_listen_thread.start()