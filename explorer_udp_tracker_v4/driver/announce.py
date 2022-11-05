from ..driver.memory import memory
from ..driver.packer import packer_messages
from ..driver.unpacker import unpacker_messages
import getuseragent
import httpx
import IPy
import operator
import random
import socket

class announce:
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

    def completed(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_server.settimeout(10)
        transaction_id = random.randint(1, 255)
        message = packer_messages().connect(transaction_id)
        try:
            socket_server.sendto(message, (ip_address, udp_port))
            (message, server_address) = socket_server.recvfrom(65536)
            if server_address[0] == ip_address and server_address[1] == udp_port:
                connect_messages = unpacker_messages().connect(message)
                if connect_messages[0] == 0 and connect_messages[1] == transaction_id:
                    connection_id = connect_messages[2]
                    message = packer_messages().announce_completed(connection_id, transaction_id, info_hash, memory.peer_id, downloaded, left, uploaded, tcp_port)
                    socket_server.sendto(message, (ip_address, udp_port))
                    (message, server_address) = socket_server.recvfrom(65536)
                    if server_address[0] == ip_address and server_address[1] == udp_port:
                        announce_completed_messages = unpacker_messages().announce(message)
                        if announce_completed_messages[0] == 1 and announce_completed_messages[1] == transaction_id:
                            socket_server.close()
                            interval = announce_completed_messages[2]
                            leechers = announce_completed_messages[3]
                            seeders = announce_completed_messages[4]
                            peers = announce_completed_messages[5]
                            wan_ip_address = self.__get_self_wan_ip_address()
                            new_peers = []
                            if len(peers) > 0:
                                for i in peers:
                                    peer_ip_address = i[0]
                                    peer_udp_port = i[1]
                                    ip_address_type = IPy.IP(peer_ip_address).iptype()
                                    if ip_address_type == 'PUBLIC':
                                        if 1 <= peer_udp_port <= 65535:
                                            if not wan_ip_address == peer_ip_address:
                                                peer_list = [peer_ip_address, peer_udp_port]
                                                peer_list_result = False
                                                for j in new_peers:
                                                    if operator.eq(j, peer_list) is True:
                                                        peer_list_result = True
                                                if peer_list_result is False:
                                                    new_peers.append(peer_list)
                            result = {
                                'interval': interval,
                                'leechers': leechers,
                                'seeders': seeders,
                                'peers': new_peers,
                                'state': True
                            }
                            return result
                        elif announce_completed_messages[0] == 3 and announce_completed_messages[1] == transaction_id:
                            socket_server.close()
                            error_message = announce_completed_messages[2]
                            result = {
                                'error': error_message,
                                'state': False
                            }
                            return result
                    else:
                        socket_server.close()
                        result = {
                            'state': False
                        }
                        return result
                elif connect_messages[0] == 3 and connect_messages[1] == transaction_id:
                    socket_server.close()
                    error_message = connect_messages[2]
                    result = {
                        'error': error_message,
                        'state': False
                    }
                    return result
            else:
                socket_server.close()
                result = {
                    'state': False
                }
                return result
        except Exception as error:
            socket_server.close()
            result = {
                'error': error,
                'state': False
            }
            return result
        finally:
            locals().clear()

    def none(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_server.settimeout(10)
        transaction_id = random.randint(1, 255)
        message = packer_messages().connect(transaction_id)
        try:
            socket_server.sendto(message, (ip_address, udp_port))
            (message, server_address) = socket_server.recvfrom(65536)
            if server_address[0] == ip_address and server_address[1] == udp_port:
                connect_messages = unpacker_messages().connect(message)
                if connect_messages[0] == 0 and connect_messages[1] == transaction_id:
                    connection_id = connect_messages[2]
                    message = packer_messages().announce_none(connection_id, transaction_id, info_hash, memory.peer_id, downloaded, left, uploaded, tcp_port)
                    socket_server.sendto(message, (ip_address, udp_port))
                    (message, server_address) = socket_server.recvfrom(65536)
                    if server_address[0] == ip_address and server_address[1] == udp_port:
                        announce_none_messages = unpacker_messages().announce(message)
                        if announce_none_messages[0] == 1 and announce_none_messages[1] == transaction_id:
                            socket_server.close()
                            interval = announce_none_messages[2]
                            leechers = announce_none_messages[3]
                            seeders = announce_none_messages[4]
                            peers = announce_none_messages[5]
                            wan_ip_address = self.__get_self_wan_ip_address()
                            new_peers = []
                            if len(peers) > 0:
                                for i in peers:
                                    peer_ip_address = i[0]
                                    peer_udp_port = i[1]
                                    ip_address_type = IPy.IP(peer_ip_address).iptype()
                                    if ip_address_type == 'PUBLIC':
                                        if 1 <= peer_udp_port <= 65535:
                                            if not wan_ip_address == peer_ip_address:
                                                peer_list = [peer_ip_address, peer_udp_port]
                                                peer_list_result = False
                                                for j in new_peers:
                                                    if operator.eq(j, peer_list) is True:
                                                        peer_list_result = True
                                                if peer_list_result is False:
                                                    new_peers.append(peer_list)
                            result = {
                                'interval': interval,
                                'leechers': leechers,
                                'seeders': seeders,
                                'peers': new_peers,
                                'state': True
                            }
                            return result
                        elif announce_none_messages[0] == 3 and announce_none_messages[1] == transaction_id:
                            socket_server.close()
                            error_message = announce_none_messages[2]
                            result = {
                                'error': error_message,
                                'state': False
                            }
                            return result
                    else:
                        socket_server.close()
                        result = {
                            'state': False
                        }
                        return result
                elif connect_messages[0] == 3 and connect_messages[1] == transaction_id:
                    socket_server.close()
                    error_message = connect_messages[2]
                    result = {
                        'error': error_message,
                        'state': False
                    }
                    return result
            else:
                socket_server.close()
                result = {
                    'state': False
                }
                return result
        except Exception as error:
            socket_server.close()
            result = {
                'error': error,
                'state': False
            }
            return result
        finally:
            locals().clear()

    def started(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_server.settimeout(10)
        transaction_id = random.randint(1, 255)
        message = packer_messages().connect(transaction_id)
        try:
            socket_server.sendto(message, (ip_address, udp_port))
            (message, server_address) = socket_server.recvfrom(65536)
            if server_address[0] == ip_address and server_address[1] == udp_port:
                connect_messages = unpacker_messages().connect(message)
                if connect_messages[0] == 0 and connect_messages[1] == transaction_id:
                    connection_id = connect_messages[2]
                    message = packer_messages().announce_started(connection_id, transaction_id, info_hash, memory.peer_id, downloaded, left, uploaded, tcp_port)
                    socket_server.sendto(message, (ip_address, udp_port))
                    (message, server_address) = socket_server.recvfrom(65536)
                    if server_address[0] == ip_address and server_address[1] == udp_port:
                        announce_started_messages = unpacker_messages().announce(message)
                        if announce_started_messages[0] == 1 and announce_started_messages[1] == transaction_id:
                            socket_server.close()
                            interval = announce_started_messages[2]
                            leechers = announce_started_messages[3]
                            seeders = announce_started_messages[4]
                            peers = announce_started_messages[5]
                            wan_ip_address = self.__get_self_wan_ip_address()
                            new_peers = []
                            if len(peers) > 0:
                                for i in peers:
                                    peer_ip_address = i[0]
                                    peer_udp_port = i[1]
                                    ip_address_type = IPy.IP(peer_ip_address).iptype()
                                    if ip_address_type == 'PUBLIC':
                                        if 1 <= peer_udp_port <= 65535:
                                            if not wan_ip_address == peer_ip_address:
                                                peer_list = [peer_ip_address, peer_udp_port]
                                                peer_list_result = False
                                                for j in new_peers:
                                                    if operator.eq(j, peer_list) is True:
                                                        peer_list_result = True
                                                if peer_list_result is False:
                                                    new_peers.append(peer_list)
                            result = {
                                'interval': interval,
                                'leechers': leechers,
                                'seeders': seeders,
                                'peers': new_peers,
                                'state': True
                            }
                            return result
                        elif announce_started_messages[0] == 3 and announce_started_messages[1] == transaction_id:
                            socket_server.close()
                            error_message = announce_started_messages[2]
                            result = {
                                'error': error_message,
                                'state': False
                            }
                            return result
                    else:
                        socket_server.close()
                        result = {
                            'state': False
                        }
                        return result
                elif connect_messages[0] == 3 and connect_messages[1] == transaction_id:
                    socket_server.close()
                    error_message = connect_messages[2]
                    result = {
                        'error': error_message,
                        'state': False
                    }
                    return result
            else:
                socket_server.close()
                result = {
                    'state': False
                }
                return result
        except Exception as error:
            socket_server.close()
            result = {
                'error': error,
                'state': False
            }
            return result
        finally:
            locals().clear()

    def stopped(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_server.settimeout(10)
        transaction_id = random.randint(1, 255)
        message = packer_messages().connect(transaction_id)
        try:
            socket_server.sendto(message, (ip_address, udp_port))
            (message, server_address) = socket_server.recvfrom(65536)
            if server_address[0] == ip_address and server_address[1] == udp_port:
                connect_messages = unpacker_messages().connect(message)
                if connect_messages[0] == 0 and connect_messages[1] == transaction_id:
                    connection_id = connect_messages[2]
                    message = packer_messages().announce_stopped(connection_id, transaction_id, info_hash, memory.peer_id, downloaded, left, uploaded, tcp_port)
                    socket_server.sendto(message, (ip_address, udp_port))
                    (message, server_address) = socket_server.recvfrom(65536)
                    if server_address[0] == ip_address and server_address[1] == udp_port:
                        announce_stopped_messages = unpacker_messages().announce(message)
                        if announce_stopped_messages[0] == 1 and announce_stopped_messages[1] == transaction_id:
                            socket_server.close()
                            interval = announce_stopped_messages[2]
                            leechers = announce_stopped_messages[3]
                            seeders = announce_stopped_messages[4]
                            peers = announce_stopped_messages[5]
                            wan_ip_address = self.__get_self_wan_ip_address()
                            new_peers = []
                            if len(peers) > 0:
                                for i in peers:
                                    peer_ip_address = i[0]
                                    peer_udp_port = i[1]
                                    ip_address_type = IPy.IP(peer_ip_address).iptype()
                                    if ip_address_type == 'PUBLIC':
                                        if 1 <= peer_udp_port <= 65535:
                                            if not wan_ip_address == peer_ip_address:
                                                peer_list = [peer_ip_address, peer_udp_port]
                                                peer_list_result = False
                                                for j in new_peers:
                                                    if operator.eq(j, peer_list) is True:
                                                        peer_list_result = True
                                                if peer_list_result is False:
                                                    new_peers.append(peer_list)
                            result = {
                                'interval': interval,
                                'leechers': leechers,
                                'seeders': seeders,
                                'peers': new_peers,
                                'state': True
                            }
                            return result
                        elif announce_stopped_messages[0] == 3 and announce_stopped_messages[1] == transaction_id:
                            socket_server.close()
                            error_message = announce_stopped_messages[2]
                            result = {
                                'error': error_message,
                                'state': False
                            }
                            return result
                    else:
                        socket_server.close()
                        result = {
                            'state': False
                        }
                        return result
                elif connect_messages[0] == 3 and connect_messages[1] == transaction_id:
                    socket_server.close()
                    error_message = connect_messages[2]
                    result = {
                        'error': error_message,
                        'state': False
                    }
                    return result
            else:
                socket_server.close()
                result = {
                    'state': False
                }
                return result
        except Exception as error:
            socket_server.close()
            result = {
                'error': error,
                'state': False
            }
            return result
        finally:
            locals().clear()