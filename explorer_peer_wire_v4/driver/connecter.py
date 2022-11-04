from ..driver.memory import memory
from ..driver.packer import packer_messages
from ..driver.unpacker import unpacker_messages
import IPy
import socket

class connection:
    def connect(self, socket_server, ip_address, tcp_port):
        try:
            socket_server.connect((ip_address, tcp_port))
            return True
        except:
            return False

    def extension_ut_metadata(self, socket_server, peer_unanalysed_handshake_response_message):
        try:
            if len(peer_unanalysed_handshake_response_message) > 0:
                peer_extended_response_message = unpacker_messages().peer_wire(peer_unanalysed_handshake_response_message)
                if 'type_20' in peer_extended_response_message:
                    if 'm' in peer_extended_response_message['type_20']['payload']:
                        if 'ut_metadata' in peer_extended_response_message['type_20']['payload']['m']:
                            ut_metadata = peer_extended_response_message['type_20']['payload']['m']['ut_metadata']
                            if 'metadata_size' in peer_extended_response_message['type_20']['payload']:
                                metadata_size = peer_extended_response_message['type_20']['payload']['metadata_size']
                                ipv6_address = ''
                                ipv6_udp_port = 0
                                if 'ipv6' in peer_extended_response_message['type_20']['payload']:
                                    ipv6_address = socket.inet_ntop(socket.AF_INET6, peer_extended_response_message['type_20']['payload']['ipv6'])
                                    ip_address_type = IPy.IP(ipv6_address).iptype()[:9]
                                    if not ip_address_type == 'ALLOCATED':
                                        ipv6_address = ''
                                if 'p' in peer_extended_response_message['type_20']['payload']:
                                    ipv6_udp_port = peer_extended_response_message['type_20']['payload']['p']
                                    if not 1 <= ipv6_udp_port <= 65535:
                                        ipv6_udp_port = 0
                                client_extended_handshake_request_message = packer_messages().extended_ut_metadata_handshake(metadata_size)
                                socket_server.send(client_extended_handshake_request_message)
                                peer_extended_handshake_unanalysed_response_message = socket_server.recv(65536)
                                peer_extended_handshake_response_message = unpacker_messages().peer_wire(peer_extended_handshake_unanalysed_response_message)
                                if 'type_0' in peer_extended_handshake_response_message:
                                    return ut_metadata, metadata_size, ipv6_address, ipv6_udp_port
                                elif 'type_1' in peer_extended_handshake_response_message:
                                    return ut_metadata, metadata_size, ipv6_address, ipv6_udp_port
                                else:
                                    return ut_metadata, metadata_size, ipv6_address, ipv6_udp_port
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    metadata_size = 0
                    client_extended_handshake_request_message = packer_messages().extended_ut_metadata_handshake(metadata_size)
                    socket_server.send(client_extended_handshake_request_message)
                    peer_extended_handshake_unanalysed_response_message = socket_server.recv(65536)
                    peer_extended_handshake_response_message = unpacker_messages().peer_wire(peer_unanalysed_handshake_response_message + peer_extended_handshake_unanalysed_response_message)
                    if 'type_20' in peer_extended_handshake_response_message:
                        if 'm' in peer_extended_handshake_response_message['type_20']['payload']:
                            if 'ut_metadata' in peer_extended_handshake_response_message['type_20']['payload']['m']:
                                ut_metadata = peer_extended_handshake_response_message['type_20']['payload']['m']['ut_metadata']
                                if 'metadata_size' in peer_extended_handshake_response_message['type_20']['payload']:
                                    metadata_size = peer_extended_handshake_response_message['type_20']['payload']['metadata_size']
                                    ipv6_address = ''
                                    ipv6_udp_port = 0
                                    if 'ipv6' in peer_extended_handshake_response_message['type_20']['payload']:
                                        ipv6_address = socket.inet_ntop(socket.AF_INET6, peer_extended_handshake_response_message['type_20']['payload']['ipv6'])
                                        ip_address_type = IPy.IP(ipv6_address).iptype()[:9]
                                        if not ip_address_type == 'ALLOCATED':
                                            ipv6_address = ''
                                    if 'p' in peer_extended_handshake_response_message['type_20']['payload']:
                                        ipv6_udp_port = peer_extended_handshake_response_message['type_20']['payload']['p']
                                        if not 1 <= ipv6_udp_port <= 65535:
                                            ipv6_udp_port = 0
                                    return ut_metadata, metadata_size, ipv6_address, ipv6_udp_port
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
            else:
                metadata_size = 0
                client_extended_handshake_request_message = packer_messages().extended_ut_metadata_handshake(metadata_size)
                socket_server.send(client_extended_handshake_request_message)
                peer_extended_handshake_unanalysed_response_message = socket_server.recv(65536)
                peer_extended_handshake_response_message = unpacker_messages().peer_wire(peer_extended_handshake_unanalysed_response_message)
                if 'type_20' in peer_extended_handshake_response_message:
                    if 'm' in peer_extended_handshake_response_message['type_20']['payload']:
                        if 'ut_metadata' in peer_extended_handshake_response_message['type_20']['payload']['m']:
                            ut_metadata = peer_extended_handshake_response_message['type_20']['payload']['m']['ut_metadata']
                            if 'metadata_size' in peer_extended_handshake_response_message['type_20']['payload']:
                                metadata_size = peer_extended_handshake_response_message['type_20']['payload']['metadata_size']
                                ipv6_address = ''
                                ipv6_udp_port = 0
                                if 'ipv6' in peer_extended_handshake_response_message['type_20']['payload']:
                                    ipv6_address = socket.inet_ntop(socket.AF_INET6, peer_extended_handshake_response_message['type_20']['payload']['ipv6'])
                                    ip_address_type = IPy.IP(ipv6_address).iptype()[:9]
                                    if not ip_address_type == 'ALLOCATED':
                                        ipv6_address = ''
                                if 'p' in peer_extended_handshake_response_message['type_20']['payload']:
                                    ipv6_udp_port = peer_extended_handshake_response_message['type_20']['payload']['p']
                                    if not 1 <= ipv6_udp_port <= 65535:
                                        ipv6_udp_port = 0
                                return ut_metadata, metadata_size, ipv6_address, ipv6_udp_port
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        except:
            return False

    def handshake(self, socket_server, info_hash):
        try:
            client_handshake_request_message = packer_messages().handshake(info_hash, memory.peer_id)
            socket_server.send(client_handshake_request_message)
            peer_unanalysed_handshake_response_message = socket_server.recv(65536)
            peer_handshake_response_message = unpacker_messages().handshake(peer_unanalysed_handshake_response_message)
            if 'info_hash' in peer_handshake_response_message:
                if peer_handshake_response_message['info_hash'] == info_hash:
                    if len(peer_unanalysed_handshake_response_message) > 68:
                        return peer_unanalysed_handshake_response_message[68:]
                    else:
                        return ''
                else:
                    return False
            else:
                return False
        except:
            return False

    def interested(self, socket_server):
        try:
            client_interested_request_message = packer_messages().interested()
            socket_server.send(client_interested_request_message)
            peer_unanalysed_interested_response_message = socket_server.recv(65536)
            peer_interested_response_message = unpacker_messages().peer_wire(peer_unanalysed_interested_response_message)
            if 'type_1' in peer_interested_response_message:
                return True
            else:
                return False
        except:
            return False