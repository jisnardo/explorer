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
            peers6 = []
            for i in range(20, len(message), 18):
                peer6_ip_address = socket.inet_ntop(socket.AF_INET6, message[i:i + 16])
                peer6_tcp_port = struct.unpack_from('!H', message, i + 16)[0]
                ip_address_type = IPy.IP(peer6_ip_address).iptype()[:9]
                if ip_address_type == 'ALLOCATED':
                    peer6_list = [peer6_ip_address, peer6_tcp_port]
                    peer6_list_result = False
                    for j in peers6:
                        if operator.eq(j, peer6_list) is True:
                            peer6_list_result = True
                    if peer6_list_result is False:
                        peers6.append(peer6_list)
            return action, transaction_id, interval, leechers, seeders, peers6
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