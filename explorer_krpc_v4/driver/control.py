from ..driver.abstraction_send import send
from ..driver.memory import memory
import binascii
import crc32c
import faker
import getuseragent
import httpx
import IPy
import os
import queue
import random
import socket
import threading
import time

class control:
    driver_control_announce_peer_messages = queue.Queue()
    driver_control_error_messages = queue.Queue()
    driver_control_find_node_messages = queue.Queue()
    driver_control_get_peers_messages = queue.Queue()
    driver_control_inbound_nodes_key = []
    driver_control_inbound_nodes_operators = queue.Queue()
    driver_control_outbound_nodes_key = []
    driver_control_outbound_nodes_operators = queue.Queue()
    driver_control_ping_messages = queue.Queue()
    driver_control_sample_infohashes_messages = queue.Queue()
    driver_control_server_messages = queue.Queue()

    def __check_driver_inbound_nodes(self):
        while True:
            if len(self.driver_control_inbound_nodes_key) > 0:
                for i in self.driver_control_inbound_nodes_key:
                    if i[1] < int(time.time()) - 120:
                        self.driver_control_inbound_nodes_operators.put(
                            ['remove', i]
                        )
            time.sleep(120)

    def __check_driver_outbound_nodes(self):
        while True:
            if len(self.driver_control_outbound_nodes_key) > 0:
                for i in self.driver_control_outbound_nodes_key:
                    if i[3] < int(time.time()) - 30:
                        if i[1] == 'announce_peer':
                            announce_peer_keyword = i[2]
                            self.driver_control_announce_peer_messages.put(
                                [False, announce_peer_keyword]
                            )
                        if i[1] == 'find_node':
                            find_node_keyword = i[2]
                            self.driver_control_find_node_messages.put(
                                [False, find_node_keyword]
                            )
                        if i[1] == 'get_peers':
                            get_peers_keyword = i[2]
                            self.driver_control_get_peers_messages.put(
                                [False, get_peers_keyword]
                            )
                        if i[1] == 'ping':
                            ping_keyword = i[2]
                            self.driver_control_ping_messages.put(
                                [False, ping_keyword]
                            )
                        if i[1] == 'sample_infohashes':
                            sample_infohashes_keyword = i[2]
                            self.driver_control_sample_infohashes_messages.put(
                                [False, sample_infohashes_keyword]
                            )
                        self.driver_control_outbound_nodes_operators.put(
                            ['remove', i]
                        )
            time.sleep(1)

    def __driver_inbound_nodes_operators(self):
        while True:
            driver_control_inbound_nodes_operators = self.driver_control_inbound_nodes_operators.get()
            operate = driver_control_inbound_nodes_operators[0]
            element = driver_control_inbound_nodes_operators[1]
            if operate == 'append':
                if element not in self.driver_control_inbound_nodes_key:
                    self.driver_control_inbound_nodes_key.append(element)
            if operate == 'remove':
                if element in self.driver_control_inbound_nodes_key:
                    self.driver_control_inbound_nodes_key.remove(element)

    def __driver_outbound_nodes_operators(self):
        while True:
            driver_control_outbound_nodes_operators = self.driver_control_outbound_nodes_operators.get()
            operate = driver_control_outbound_nodes_operators[0]
            element = driver_control_outbound_nodes_operators[1]
            if operate == 'append':
                if element not in self.driver_control_outbound_nodes_key:
                    self.driver_control_outbound_nodes_key.append(element)
            if operate == 'remove':
                if element in self.driver_control_outbound_nodes_key:
                    self.driver_control_outbound_nodes_key.remove(element)

    def __get_self_lan_ip_address(self):
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_server.connect(('8.8.8.8', 80))
            ip_address = socket_server.getsockname()[0]
        except:
            ip_address = faker.Faker().ipv4(network = False, address_class = None, private = True)
        finally:
            socket_server.close()
            return ip_address

    def __get_self_node_id(self, ip_address):
        while True:
            ip_address_type = IPy.IP(ip_address).iptype()
            if ip_address_type == 'PUBLIC':
                rand = random.randint(0, 255) & 0xff
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
                    node_id = ''
                    node_id = node_id + hex((crc >> 24) & 0xff).replace('0x', '').zfill(2)
                    node_id = node_id + hex((crc >> 16) & 0xff).replace('0x', '').zfill(2)
                    node_id = node_id + hex(((crc >> 8) & 0xf8) | (random.randint(0, 255) & 0x7)).replace('0x', '').zfill(2)
                    for i in range(0, 16):
                        node_id = node_id + hex(random.randint(0, 255)).replace('0x', '').zfill(2)
                    node_id = node_id + hex(rand).replace('0x', '').zfill(2)
                    return node_id
            else:
                return os.urandom(20).hex()

    def __get_self_wan_ip_address(self):
        ip_address = ''
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = 'https://ipv4.jsonip.com'
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    data = response.json()
                    ip_address = data['ip']
            except httpx.HTTPError:
                pass
            except Exception:
                pass
            finally:
                locals().clear()
        return ip_address

    def e_client(self, transaction_id, error_number, error_message, ip_address, udp_port):
        self.driver_control_error_messages.put(
            [transaction_id, error_number, error_message, ip_address, udp_port]
        )

    def q_client(self, node_id, transaction_id, query, tcp_port, token, target_id, info_hash, ip_address, udp_port):
        self.driver_control_server_messages.put(
            [node_id, transaction_id, query, tcp_port, token, target_id, info_hash, ip_address, udp_port]
        )
        self.driver_control_inbound_nodes_operators.put(
            ['append', [transaction_id, int(time.time())]]
        )

    def r_client(self, node_id, transaction_id, self_ip_address, self_udp_port, nodes, values, samples, token, ip_address, udp_port):
        if self_ip_address == '':
            for i in self.driver_control_outbound_nodes_key:
                if i[0] == transaction_id:
                    if i[1] == 'announce_peer':
                        announce_peer_keyword = i[2]
                        self.driver_control_announce_peer_messages.put(
                            [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                        )
                    if i[1] == 'find_node':
                        find_node_keyword = i[2]
                        self.driver_control_find_node_messages.put(
                            [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                        )
                    if i[1] == 'get_peers':
                        get_peers_keyword = i[2]
                        self.driver_control_get_peers_messages.put(
                            [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                        )
                    if i[1] == 'ping':
                        ping_keyword = i[2]
                        self.driver_control_ping_messages.put(
                            [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                        )
                    if i[1] == 'sample_infohashes':
                        sample_infohashes_keyword = i[2]
                        self.driver_control_sample_infohashes_messages.put(
                            [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                        )
                    self.driver_control_outbound_nodes_operators.put(
                        ['remove', i]
                    )
        else:
            self_ip_address_type = IPy.IP(self_ip_address).iptype()
            if self_ip_address_type == 'PUBLIC':
                if memory.ip_address == self_ip_address:
                    if memory.udp_port == self_udp_port:
                        for i in self.driver_control_outbound_nodes_key:
                            if i[0] == transaction_id:
                                if i[1] == 'announce_peer':
                                    announce_peer_keyword = i[2]
                                    self.driver_control_announce_peer_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                    )
                                if i[1] == 'find_node':
                                    find_node_keyword = i[2]
                                    self.driver_control_find_node_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                    )
                                if i[1] == 'get_peers':
                                    get_peers_keyword = i[2]
                                    self.driver_control_get_peers_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                    )
                                if i[1] == 'ping':
                                    ping_keyword = i[2]
                                    self.driver_control_ping_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                    )
                                if i[1] == 'sample_infohashes':
                                    sample_infohashes_keyword = i[2]
                                    self.driver_control_sample_infohashes_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                    )
                                self.driver_control_outbound_nodes_operators.put(
                                    ['remove', i]
                                )
                    elif 1 <= self_udp_port <= 65535:
                        memory.udp_port = self_udp_port
                        for i in self.driver_control_outbound_nodes_key:
                            if i[0] == transaction_id:
                                if i[1] == 'announce_peer':
                                    announce_peer_keyword = i[2]
                                    self.driver_control_announce_peer_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                    )
                                if i[1] == 'find_node':
                                    find_node_keyword = i[2]
                                    self.driver_control_find_node_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                    )
                                if i[1] == 'get_peers':
                                    get_peers_keyword = i[2]
                                    self.driver_control_get_peers_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                    )
                                if i[1] == 'ping':
                                    ping_keyword = i[2]
                                    self.driver_control_ping_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                    )
                                if i[1] == 'sample_infohashes':
                                    sample_infohashes_keyword = i[2]
                                    self.driver_control_sample_infohashes_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                    )
                                self.driver_control_outbound_nodes_operators.put(
                                    ['remove', i]
                                )
                    else:
                        for i in self.driver_control_outbound_nodes_key:
                            if i[0] == transaction_id:
                                if i[1] == 'announce_peer':
                                    announce_peer_keyword = i[2]
                                    self.driver_control_announce_peer_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                    )
                                if i[1] == 'find_node':
                                    find_node_keyword = i[2]
                                    self.driver_control_find_node_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                    )
                                if i[1] == 'get_peers':
                                    get_peers_keyword = i[2]
                                    self.driver_control_get_peers_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                    )
                                if i[1] == 'ping':
                                    ping_keyword = i[2]
                                    self.driver_control_ping_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                    )
                                if i[1] == 'sample_infohashes':
                                    sample_infohashes_keyword = i[2]
                                    self.driver_control_sample_infohashes_messages.put(
                                        [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                    )
                                self.driver_control_outbound_nodes_operators.put(
                                    ['remove', i]
                                )
                else:
                    lan_ip_address = self.__get_self_lan_ip_address()
                    ip_address_type = IPy.IP(lan_ip_address).iptype()
                    if ip_address_type == 'PUBLIC':
                        if memory.ip_address == lan_ip_address:
                            for i in self.driver_control_outbound_nodes_key:
                                if i[0] == transaction_id:
                                    if i[1] == 'announce_peer':
                                        announce_peer_keyword = i[2]
                                        self.driver_control_announce_peer_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                        )
                                    if i[1] == 'find_node':
                                        find_node_keyword = i[2]
                                        self.driver_control_find_node_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                        )
                                    if i[1] == 'get_peers':
                                        get_peers_keyword = i[2]
                                        self.driver_control_get_peers_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                        )
                                    if i[1] == 'ping':
                                        ping_keyword = i[2]
                                        self.driver_control_ping_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                        )
                                    if i[1] == 'sample_infohashes':
                                        sample_infohashes_keyword = i[2]
                                        self.driver_control_sample_infohashes_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                        )
                                    self.driver_control_outbound_nodes_operators.put(
                                        ['remove', i]
                                    )
                        else:
                            memory.node_id = self.__get_self_node_id(lan_ip_address)
                            memory.ip_address = lan_ip_address
                            for i in self.driver_control_outbound_nodes_key:
                                if i[0] == transaction_id:
                                    if i[1] == 'announce_peer':
                                        announce_peer_keyword = i[2]
                                        self.driver_control_announce_peer_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                        )
                                    if i[1] == 'find_node':
                                        find_node_keyword = i[2]
                                        self.driver_control_find_node_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                        )
                                    if i[1] == 'get_peers':
                                        get_peers_keyword = i[2]
                                        self.driver_control_get_peers_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                        )
                                    if i[1] == 'ping':
                                        ping_keyword = i[2]
                                        self.driver_control_ping_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                        )
                                    if i[1] == 'sample_infohashes':
                                        sample_infohashes_keyword = i[2]
                                        self.driver_control_sample_infohashes_messages.put(
                                            [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                        )
                                    self.driver_control_outbound_nodes_operators.put(
                                        ['remove', i]
                                    )
                    else:
                        wan_ip_address = self.__get_self_wan_ip_address()
                        if wan_ip_address == '':
                            if len(memory.ip_address_returned) < 8:
                                memory.ip_address_returned.append(self_ip_address)
                                for i in self.driver_control_outbound_nodes_key:
                                    if i[0] == transaction_id:
                                        if i[1] == 'announce_peer':
                                            announce_peer_keyword = i[2]
                                            self.driver_control_announce_peer_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                            )
                                        if i[1] == 'find_node':
                                            find_node_keyword = i[2]
                                            self.driver_control_find_node_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                            )
                                        if i[1] == 'get_peers':
                                            get_peers_keyword = i[2]
                                            self.driver_control_get_peers_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                            )
                                        if i[1] == 'ping':
                                            ping_keyword = i[2]
                                            self.driver_control_ping_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                            )
                                        if i[1] == 'sample_infohashes':
                                            sample_infohashes_keyword = i[2]
                                            self.driver_control_sample_infohashes_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                            )
                                        self.driver_control_outbound_nodes_operators.put(
                                            ['remove', i]
                                        )
                            else:
                                self_ip_address = max(set(memory.ip_address_returned), key = memory.ip_address_returned.count)
                                memory.ip_address_returned.clear()
                                if memory.ip_address == self_ip_address:
                                    for i in self.driver_control_outbound_nodes_key:
                                        if i[0] == transaction_id:
                                            if i[1] == 'announce_peer':
                                                announce_peer_keyword = i[2]
                                                self.driver_control_announce_peer_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                                )
                                            if i[1] == 'find_node':
                                                find_node_keyword = i[2]
                                                self.driver_control_find_node_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                                )
                                            if i[1] == 'get_peers':
                                                get_peers_keyword = i[2]
                                                self.driver_control_get_peers_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                                )
                                            if i[1] == 'ping':
                                                ping_keyword = i[2]
                                                self.driver_control_ping_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                                )
                                            if i[1] == 'sample_infohashes':
                                                sample_infohashes_keyword = i[2]
                                                self.driver_control_sample_infohashes_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                                )
                                            self.driver_control_outbound_nodes_operators.put(
                                                ['remove', i]
                                            )
                                else:
                                    memory.node_id = self.__get_self_node_id(self_ip_address)
                                    memory.ip_address = self_ip_address
                                    for i in self.driver_control_outbound_nodes_key:
                                        if i[0] == transaction_id:
                                            if i[1] == 'announce_peer':
                                                announce_peer_keyword = i[2]
                                                self.driver_control_announce_peer_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                                )
                                            if i[1] == 'find_node':
                                                find_node_keyword = i[2]
                                                self.driver_control_find_node_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                                )
                                            if i[1] == 'get_peers':
                                                get_peers_keyword = i[2]
                                                self.driver_control_get_peers_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                                )
                                            if i[1] == 'ping':
                                                ping_keyword = i[2]
                                                self.driver_control_ping_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                                )
                                            if i[1] == 'sample_infohashes':
                                                sample_infohashes_keyword = i[2]
                                                self.driver_control_sample_infohashes_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                                )
                                            self.driver_control_outbound_nodes_operators.put(
                                                ['remove', i]
                                            )
                        else:
                            ip_address_type = IPy.IP(wan_ip_address).iptype()
                            if ip_address_type == 'PUBLIC':
                                if memory.ip_address == wan_ip_address:
                                    for i in self.driver_control_outbound_nodes_key:
                                        if i[0] == transaction_id:
                                            if i[1] == 'announce_peer':
                                                announce_peer_keyword = i[2]
                                                self.driver_control_announce_peer_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                                )
                                            if i[1] == 'find_node':
                                                find_node_keyword = i[2]
                                                self.driver_control_find_node_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                                )
                                            if i[1] == 'get_peers':
                                                get_peers_keyword = i[2]
                                                self.driver_control_get_peers_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                                )
                                            if i[1] == 'ping':
                                                ping_keyword = i[2]
                                                self.driver_control_ping_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                                )
                                            if i[1] == 'sample_infohashes':
                                                sample_infohashes_keyword = i[2]
                                                self.driver_control_sample_infohashes_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                                )
                                            self.driver_control_outbound_nodes_operators.put(
                                                ['remove', i]
                                            )
                                else:
                                    memory.node_id = self.__get_self_node_id(wan_ip_address)
                                    memory.ip_address = wan_ip_address
                                    for i in self.driver_control_outbound_nodes_key:
                                        if i[0] == transaction_id:
                                            if i[1] == 'announce_peer':
                                                announce_peer_keyword = i[2]
                                                self.driver_control_announce_peer_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                                )
                                            if i[1] == 'find_node':
                                                find_node_keyword = i[2]
                                                self.driver_control_find_node_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                                )
                                            if i[1] == 'get_peers':
                                                get_peers_keyword = i[2]
                                                self.driver_control_get_peers_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                                )
                                            if i[1] == 'ping':
                                                ping_keyword = i[2]
                                                self.driver_control_ping_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                                )
                                            if i[1] == 'sample_infohashes':
                                                sample_infohashes_keyword = i[2]
                                                self.driver_control_sample_infohashes_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                                )
                                            self.driver_control_outbound_nodes_operators.put(
                                                ['remove', i]
                                            )
                            elif len(memory.ip_address_returned) < 8:
                                memory.ip_address_returned.append(self_ip_address)
                                for i in self.driver_control_outbound_nodes_key:
                                    if i[0] == transaction_id:
                                        if i[1] == 'announce_peer':
                                            announce_peer_keyword = i[2]
                                            self.driver_control_announce_peer_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                            )
                                        if i[1] == 'find_node':
                                            find_node_keyword = i[2]
                                            self.driver_control_find_node_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                            )
                                        if i[1] == 'get_peers':
                                            get_peers_keyword = i[2]
                                            self.driver_control_get_peers_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                            )
                                        if i[1] == 'ping':
                                            ping_keyword = i[2]
                                            self.driver_control_ping_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                            )
                                        if i[1] == 'sample_infohashes':
                                            sample_infohashes_keyword = i[2]
                                            self.driver_control_sample_infohashes_messages.put(
                                                [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                            )
                                        self.driver_control_outbound_nodes_operators.put(
                                            ['remove', i]
                                        )
                            else:
                                self_ip_address = max(set(memory.ip_address_returned), key = memory.ip_address_returned.count)
                                memory.ip_address_returned.clear()
                                if memory.ip_address == self_ip_address:
                                    for i in self.driver_control_outbound_nodes_key:
                                        if i[0] == transaction_id:
                                            if i[1] == 'announce_peer':
                                                announce_peer_keyword = i[2]
                                                self.driver_control_announce_peer_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                                )
                                            if i[1] == 'find_node':
                                                find_node_keyword = i[2]
                                                self.driver_control_find_node_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                                )
                                            if i[1] == 'get_peers':
                                                get_peers_keyword = i[2]
                                                self.driver_control_get_peers_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                                )
                                            if i[1] == 'ping':
                                                ping_keyword = i[2]
                                                self.driver_control_ping_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                                )
                                            if i[1] == 'sample_infohashes':
                                                sample_infohashes_keyword = i[2]
                                                self.driver_control_sample_infohashes_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                                )
                                            self.driver_control_outbound_nodes_operators.put(
                                                ['remove', i]
                                            )
                                else:
                                    memory.node_id = self.__get_self_node_id(self_ip_address)
                                    memory.ip_address = self_ip_address
                                    for i in self.driver_control_outbound_nodes_key:
                                        if i[0] == transaction_id:
                                            if i[1] == 'announce_peer':
                                                announce_peer_keyword = i[2]
                                                self.driver_control_announce_peer_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                                                )
                                            if i[1] == 'find_node':
                                                find_node_keyword = i[2]
                                                self.driver_control_find_node_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                                                )
                                            if i[1] == 'get_peers':
                                                get_peers_keyword = i[2]
                                                self.driver_control_get_peers_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                                                )
                                            if i[1] == 'ping':
                                                ping_keyword = i[2]
                                                self.driver_control_ping_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                                                )
                                            if i[1] == 'sample_infohashes':
                                                sample_infohashes_keyword = i[2]
                                                self.driver_control_sample_infohashes_messages.put(
                                                    [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                                                )
                                            self.driver_control_outbound_nodes_operators.put(
                                                ['remove', i]
                                            )
            else:
                for i in self.driver_control_outbound_nodes_key:
                    if i[0] == transaction_id:
                        if i[1] == 'announce_peer':
                            announce_peer_keyword = i[2]
                            self.driver_control_announce_peer_messages.put(
                                [node_id, nodes, values, samples, token, ip_address, udp_port, announce_peer_keyword]
                            )
                        if i[1] == 'find_node':
                            find_node_keyword = i[2]
                            self.driver_control_find_node_messages.put(
                                [node_id, nodes, values, samples, token, ip_address, udp_port, find_node_keyword]
                            )
                        if i[1] == 'get_peers':
                            get_peers_keyword = i[2]
                            self.driver_control_get_peers_messages.put(
                                [node_id, nodes, values, samples, token, ip_address, udp_port, get_peers_keyword]
                            )
                        if i[1] == 'ping':
                            ping_keyword = i[2]
                            self.driver_control_ping_messages.put(
                                [node_id, nodes, values, samples, token, ip_address, udp_port, ping_keyword]
                            )
                        if i[1] == 'sample_infohashes':
                            sample_infohashes_keyword = i[2]
                            self.driver_control_sample_infohashes_messages.put(
                                [node_id, nodes, values, samples, token, ip_address, udp_port, sample_infohashes_keyword]
                            )
                        self.driver_control_outbound_nodes_operators.put(
                            ['remove', i]
                        )

    def request_announce_peer(self, application_name, info_hash, tcp_port, token, ip_address, udp_port, announce_peer_keyword):
        transaction_id = send().request_announce_peer(info_hash, tcp_port, token, ip_address, udp_port)
        self.driver_control_outbound_nodes_operators.put(
            ['append', [transaction_id, application_name, announce_peer_keyword, int(time.time())]]
        )

    def request_find_node(self, application_name, target_id, ip_address, udp_port, find_node_keyword):
        transaction_id = send().request_find_node(target_id, ip_address, udp_port)
        self.driver_control_outbound_nodes_operators.put(
            ['append', [transaction_id, application_name, find_node_keyword, int(time.time())]]
        )

    def request_get_peers(self, application_name, info_hash, ip_address, udp_port, get_peers_keyword):
        transaction_id = send().request_get_peers(info_hash, ip_address, udp_port)
        self.driver_control_outbound_nodes_operators.put(
            ['append', [transaction_id, application_name, get_peers_keyword, int(time.time())]]
        )

    def request_ping(self, application_name, ip_address, udp_port, ping_keyword):
        transaction_id = send().request_ping(ip_address, udp_port)
        self.driver_control_outbound_nodes_operators.put(
            ['append', [transaction_id, application_name, ping_keyword, int(time.time())]]
        )

    def request_sample_infohashes(self, application_name, target_id, ip_address, udp_port, sample_infohashes_keyword):
        transaction_id = send().request_sample_infohashes(target_id, ip_address, udp_port)
        self.driver_control_outbound_nodes_operators.put(
            ['append', [transaction_id, application_name, sample_infohashes_keyword, int(time.time())]]
        )

    def response_announce_peer(self, transaction_id, ip_address, udp_port):
        for i in self.driver_control_inbound_nodes_key:
            if i[0] == transaction_id:
                send().response_announce_peer(transaction_id, ip_address, udp_port)
                self.driver_control_inbound_nodes_operators.put(
                    ['remove', i]
                )

    def response_find_node(self, transaction_id, nodes, ip_address, udp_port):
        for i in self.driver_control_inbound_nodes_key:
            if i[0] == transaction_id:
                send().response_find_node(transaction_id, nodes, ip_address, udp_port)
                self.driver_control_inbound_nodes_operators.put(
                    ['remove', i]
                )

    def response_get_peers(self, transaction_id, nodes, values, ip_address, udp_port):
        for i in self.driver_control_inbound_nodes_key:
            if i[0] == transaction_id:
                send().response_get_peers(transaction_id, nodes, values, ip_address, udp_port)
                self.driver_control_inbound_nodes_operators.put(
                    ['remove', i]
                )

    def response_ping(self, transaction_id, ip_address, udp_port):
        for i in self.driver_control_inbound_nodes_key:
            if i[0] == transaction_id:
                send().response_ping(transaction_id, ip_address, udp_port)
                self.driver_control_inbound_nodes_operators.put(
                    ['remove', i]
                )

    def response_sample_infohashes(self, transaction_id, nodes, number, samples, ip_address, udp_port):
        for i in self.driver_control_inbound_nodes_key:
            if i[0] == transaction_id:
                send().response_sample_infohashes(transaction_id, nodes, number, samples, ip_address, udp_port)
                self.driver_control_inbound_nodes_operators.put(
                    ['remove', i]
                )

    def start_control(self):
        explorer_krpc_v4_driver_control_check_driver_inbound_nodes_thread = threading.Thread(target = self.__check_driver_inbound_nodes)
        explorer_krpc_v4_driver_control_check_driver_inbound_nodes_thread.setDaemon(True)
        explorer_krpc_v4_driver_control_check_driver_inbound_nodes_thread.start()
        explorer_krpc_v4_driver_control_check_driver_outbound_nodes_thread = threading.Thread(target = self.__check_driver_outbound_nodes)
        explorer_krpc_v4_driver_control_check_driver_outbound_nodes_thread.setDaemon(True)
        explorer_krpc_v4_driver_control_check_driver_outbound_nodes_thread.start()
        explorer_krpc_v4_driver_control_driver_inbound_nodes_operators_thread = threading.Thread(target = self.__driver_inbound_nodes_operators)
        explorer_krpc_v4_driver_control_driver_inbound_nodes_operators_thread.setDaemon(True)
        explorer_krpc_v4_driver_control_driver_inbound_nodes_operators_thread.start()
        explorer_krpc_v4_driver_control_driver_outbound_nodes_operators_thread = threading.Thread(target = self.__driver_outbound_nodes_operators)
        explorer_krpc_v4_driver_control_driver_outbound_nodes_operators_thread.setDaemon(True)
        explorer_krpc_v4_driver_control_driver_outbound_nodes_operators_thread.start()