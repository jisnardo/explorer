import IPy
import operator
import socket
import struct

class unpacker_messages:
    def announce(self, message):
        action = struct.unpack_from('!i', message)[0]
        if action == 1:
            transaction_id = struct.unpack_from('!i', message, 4)[0]
            interval = struct.unpack_from('!i', message, 8)[0]
            leechers = struct.unpack_from('!i', message, 12)[0]
            seeders = struct.unpack_from('!i', message, 16)[0]
            peers = []
            for i in range(20, len(message), 6):
                peer_ip_address = socket.inet_ntop(socket.AF_INET, message[i:i + 4])
                peer_tcp_port = struct.unpack_from('!H', message, i + 4)[0]
                ip_address_type = IPy.IP(peer_ip_address).iptype()
                if ip_address_type == 'PUBLIC':
                    peer_list = [peer_ip_address, peer_tcp_port]
                    peer_list_result = False
                    for j in peers:
                        if operator.eq(j, peer_list) is True:
                            peer_list_result = True
                    if peer_list_result is False:
                        peers.append(peer_list)
            return action, transaction_id, interval, leechers, seeders, peers
        if action == 3:
            transaction_id = struct.unpack_from('!i', message, 4)[0]
            error_message = struct.unpack_from('!s', message, 8)[0]
            return action, transaction_id, error_message

    def connect(self, message):
        action = struct.unpack_from('!i', message)[0]
        if action == 0:
            transaction_id = struct.unpack_from('!i', message, 4)[0]
            connection_id = struct.unpack_from('!Q', message, 8)[0]
            return action, transaction_id, connection_id
        if action == 3:
            transaction_id = struct.unpack_from('!i', message, 4)[0]
            error_message = struct.unpack_from('!s', message, 8)[0]
            return action, transaction_id, error_message

    def scrape(self, message):
        action = struct.unpack_from('!i', message)[0]
        if action == 2:
            transaction_id = struct.unpack_from('!i', message, 4)[0]
            seeders = struct.unpack_from('!i', message, 8)[0]
            completed = struct.unpack_from('!i', message, 12)[0]
            leechers = struct.unpack_from('!i', message, 16)[0]
            return action, transaction_id, seeders, completed, leechers
        if action == 3:
            transaction_id = struct.unpack_from('!i', message, 4)[0]
            error_message = struct.unpack_from('!s', message, 8)[0]
            return action, transaction_id, error_message