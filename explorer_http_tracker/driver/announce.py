from ..driver.memory import memory
import getuseragent
import httpx
import IPy
import operator
import pyben
import socket
import struct
import urllib.parse

class announce:
    def __get_self_wan_ipv4_address(self):
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

    def __get_self_wan_ipv6_address(self):
        ip_address = ''
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = 'https://ipv6.jsonip.com'
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

    def completed(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port):
        http_escape_character_info_hash = urllib.parse.quote_from_bytes(bytes.fromhex(info_hash))
        http_escape_character_peer_id = urllib.parse.quote_from_bytes(bytes.fromhex(memory.peer_id))
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = '{}/announce?info_hash={}&peer_id={}&downloaded={}&left={}&uploaded={}&port={}&compact=1&event=completed'.format(
            domain_url, http_escape_character_info_hash, http_escape_character_peer_id, str(downloaded), str(left), str(uploaded), str(tcp_port)
        )
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    message = pyben.loads(response.content)
                    complete = 0
                    downloaded = 0
                    incomplete = 0
                    interval = 0
                    min_interval = 0
                    wan_ipv4_address = self.__get_self_wan_ipv4_address()
                    wan_ipv6_address = self.__get_self_wan_ipv6_address()
                    peers = []
                    peers6 = []
                    if 'complete' in message:
                        complete = message.get('complete')
                    if 'downloaded' in message:
                        downloaded = message.get('downloaded')
                    if 'incomplete' in message:
                        incomplete = message.get('incomplete')
                    if 'interval' in message:
                        interval = message.get('interval')
                    if 'min interval' in message:
                        min_interval = message.get('min interval')
                    if 'peers' in message:
                        if type(message.get('peers')) == bytes:
                            for i in range(0, len(message.get('peers')), 6):
                                peer_ip_address = socket.inet_ntop(socket.AF_INET, message.get('peers')[i:i + 4])
                                peer_tcp_port = struct.unpack_from('!H', message.get('peers'), i + 4)[0]
                                ip_address_type = IPy.IP(peer_ip_address).iptype()
                                if ip_address_type == 'PUBLIC':
                                    if 1 <= peer_tcp_port <= 65535:
                                        if not wan_ipv4_address == peer_ip_address:
                                            peer_list = [peer_ip_address, peer_tcp_port]
                                            peer_list_result = False
                                            for j in peers:
                                                if operator.eq(j, peer_list) is True:
                                                    peer_list_result = True
                                            if peer_list_result is False:
                                                peers.append(peer_list)
                    if 'peers6' in message:
                        if type(message.get('peers6')) == bytes:
                            for i in range(0, len(message.get('peers6')), 18):
                                peer6_ip_address = socket.inet_ntop(socket.AF_INET6, message.get('peers6')[i:i + 16])
                                peer6_tcp_port = struct.unpack_from('!H', message.get('peers6'), i + 16)[0]
                                ip_address_type = IPy.IP(peer6_ip_address).iptype()[:9]
                                if ip_address_type == 'ALLOCATED':
                                    if 1 <= peer6_tcp_port <= 65535:
                                        if not wan_ipv6_address == peer6_ip_address:
                                            peer6_list = [peer6_ip_address, peer6_tcp_port]
                                            peer6_list_result = False
                                            for j in peers6:
                                                if operator.eq(j, peer6_list) is True:
                                                    peer6_list_result = True
                                            if peer6_list_result is False:
                                                peers6.append(peer6_list)
                    result = {
                        'complete': complete,
                        'downloaded': downloaded,
                        'incomplete': incomplete,
                        'interval': interval,
                        'min_interval': min_interval,
                        'peers': peers,
                        'peers6': peers6,
                        'status': True
                    }
                    return result
                else:
                    result = {
                        'error': response.status_code,
                        'status': False
                    }
                    return result
            except httpx.HTTPError as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            except Exception as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            finally:
                locals().clear()

    def none(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port):
        http_escape_character_info_hash = urllib.parse.quote_from_bytes(bytes.fromhex(info_hash))
        http_escape_character_peer_id = urllib.parse.quote_from_bytes(bytes.fromhex(memory.peer_id))
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = '{}/announce?info_hash={}&peer_id={}&downloaded={}&left={}&uploaded={}&port={}&compact=1&event=none'.format(
            domain_url, http_escape_character_info_hash, http_escape_character_peer_id, str(downloaded), str(left), str(uploaded), str(tcp_port)
        )
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    message = pyben.loads(response.content)
                    complete = 0
                    downloaded = 0
                    incomplete = 0
                    interval = 0
                    min_interval = 0
                    wan_ipv4_address = self.__get_self_wan_ipv4_address()
                    wan_ipv6_address = self.__get_self_wan_ipv6_address()
                    peers = []
                    peers6 = []
                    if 'complete' in message:
                        complete = message.get('complete')
                    if 'downloaded' in message:
                        downloaded = message.get('downloaded')
                    if 'incomplete' in message:
                        incomplete = message.get('incomplete')
                    if 'interval' in message:
                        interval = message.get('interval')
                    if 'min interval' in message:
                        min_interval = message.get('min interval')
                    if 'peers' in message:
                        if type(message.get('peers')) == bytes:
                            for i in range(0, len(message.get('peers')), 6):
                                peer_ip_address = socket.inet_ntop(socket.AF_INET, message.get('peers')[i:i + 4])
                                peer_tcp_port = struct.unpack_from('!H', message.get('peers'), i + 4)[0]
                                ip_address_type = IPy.IP(peer_ip_address).iptype()
                                if ip_address_type == 'PUBLIC':
                                    if 1 <= peer_tcp_port <= 65535:
                                        if not wan_ipv4_address == peer_ip_address:
                                            peer_list = [peer_ip_address, peer_tcp_port]
                                            peer_list_result = False
                                            for j in peers:
                                                if operator.eq(j, peer_list) is True:
                                                    peer_list_result = True
                                            if peer_list_result is False:
                                                peers.append(peer_list)
                    if 'peers6' in message:
                        if type(message.get('peers6')) == bytes:
                            for i in range(0, len(message.get('peers6')), 18):
                                peer6_ip_address = socket.inet_ntop(socket.AF_INET6, message.get('peers6')[i:i + 16])
                                peer6_tcp_port = struct.unpack_from('!H', message.get('peers6'), i + 16)[0]
                                ip_address_type = IPy.IP(peer6_ip_address).iptype()[:9]
                                if ip_address_type == 'ALLOCATED':
                                    if 1 <= peer6_tcp_port <= 65535:
                                        if not wan_ipv6_address == peer6_ip_address:
                                            peer6_list = [peer6_ip_address, peer6_tcp_port]
                                            peer6_list_result = False
                                            for j in peers6:
                                                if operator.eq(j, peer6_list) is True:
                                                    peer6_list_result = True
                                            if peer6_list_result is False:
                                                peers6.append(peer6_list)
                    result = {
                        'complete': complete,
                        'downloaded': downloaded,
                        'incomplete': incomplete,
                        'interval': interval,
                        'min_interval': min_interval,
                        'peers': peers,
                        'peers6': peers6,
                        'status': True
                    }
                    return result
                else:
                    result = {
                        'error': response.status_code,
                        'status': False
                    }
                    return result
            except httpx.HTTPError as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            except Exception as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            finally:
                locals().clear()

    def started(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port):
        http_escape_character_info_hash = urllib.parse.quote_from_bytes(bytes.fromhex(info_hash))
        http_escape_character_peer_id = urllib.parse.quote_from_bytes(bytes.fromhex(memory.peer_id))
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = '{}/announce?info_hash={}&peer_id={}&downloaded={}&left={}&uploaded={}&port={}&compact=1&event=started'.format(
            domain_url, http_escape_character_info_hash, http_escape_character_peer_id, str(downloaded), str(left), str(uploaded), str(tcp_port)
        )
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    message = pyben.loads(response.content)
                    complete = 0
                    downloaded = 0
                    incomplete = 0
                    interval = 0
                    min_interval = 0
                    wan_ipv4_address = self.__get_self_wan_ipv4_address()
                    wan_ipv6_address = self.__get_self_wan_ipv6_address()
                    peers = []
                    peers6 = []
                    if 'complete' in message:
                        complete = message.get('complete')
                    if 'downloaded' in message:
                        downloaded = message.get('downloaded')
                    if 'incomplete' in message:
                        incomplete = message.get('incomplete')
                    if 'interval' in message:
                        interval = message.get('interval')
                    if 'min interval' in message:
                        min_interval = message.get('min interval')
                    if 'peers' in message:
                        if type(message.get('peers')) == bytes:
                            for i in range(0, len(message.get('peers')), 6):
                                peer_ip_address = socket.inet_ntop(socket.AF_INET, message.get('peers')[i:i + 4])
                                peer_tcp_port = struct.unpack_from('!H', message.get('peers'), i + 4)[0]
                                ip_address_type = IPy.IP(peer_ip_address).iptype()
                                if ip_address_type == 'PUBLIC':
                                    if 1 <= peer_tcp_port <= 65535:
                                        if not wan_ipv4_address == peer_ip_address:
                                            peer_list = [peer_ip_address, peer_tcp_port]
                                            peer_list_result = False
                                            for j in peers:
                                                if operator.eq(j, peer_list) is True:
                                                    peer_list_result = True
                                            if peer_list_result is False:
                                                peers.append(peer_list)
                    if 'peers6' in message:
                        if type(message.get('peers6')) == bytes:
                            for i in range(0, len(message.get('peers6')), 18):
                                peer6_ip_address = socket.inet_ntop(socket.AF_INET6, message.get('peers6')[i:i + 16])
                                peer6_tcp_port = struct.unpack_from('!H', message.get('peers6'), i + 16)[0]
                                ip_address_type = IPy.IP(peer6_ip_address).iptype()[:9]
                                if ip_address_type == 'ALLOCATED':
                                    if 1 <= peer6_tcp_port <= 65535:
                                        if not wan_ipv6_address == peer6_ip_address:
                                            peer6_list = [peer6_ip_address, peer6_tcp_port]
                                            peer6_list_result = False
                                            for j in peers6:
                                                if operator.eq(j, peer6_list) is True:
                                                    peer6_list_result = True
                                            if peer6_list_result is False:
                                                peers6.append(peer6_list)
                    result = {
                        'complete': complete,
                        'downloaded': downloaded,
                        'incomplete': incomplete,
                        'interval': interval,
                        'min_interval': min_interval,
                        'peers': peers,
                        'peers6': peers6,
                        'status': True
                    }
                    return result
                else:
                    result = {
                        'error': response.status_code,
                        'status': False
                    }
                    return result
            except httpx.HTTPError as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            except Exception as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            finally:
                locals().clear()

    def stopped(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port):
        http_escape_character_info_hash = urllib.parse.quote_from_bytes(bytes.fromhex(info_hash))
        http_escape_character_peer_id = urllib.parse.quote_from_bytes(bytes.fromhex(memory.peer_id))
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = '{}/announce?info_hash={}&peer_id={}&downloaded={}&left={}&uploaded={}&port={}&compact=1&event=started'.format(
            domain_url, http_escape_character_info_hash, http_escape_character_peer_id, str(downloaded), str(left), str(uploaded), str(tcp_port)
        )
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    message = pyben.loads(response.content)
                    complete = 0
                    downloaded = 0
                    incomplete = 0
                    interval = 0
                    min_interval = 0
                    wan_ipv4_address = self.__get_self_wan_ipv4_address()
                    wan_ipv6_address = self.__get_self_wan_ipv6_address()
                    peers = []
                    peers6 = []
                    if 'complete' in message:
                        complete = message.get('complete')
                    if 'downloaded' in message:
                        downloaded = message.get('downloaded')
                    if 'incomplete' in message:
                        incomplete = message.get('incomplete')
                    if 'interval' in message:
                        interval = message.get('interval')
                    if 'min interval' in message:
                        min_interval = message.get('min interval')
                    if 'peers' in message:
                        if type(message.get('peers')) == bytes:
                            for i in range(0, len(message.get('peers')), 6):
                                peer_ip_address = socket.inet_ntop(socket.AF_INET, message.get('peers')[i:i + 4])
                                peer_tcp_port = struct.unpack_from('!H', message.get('peers'), i + 4)[0]
                                ip_address_type = IPy.IP(peer_ip_address).iptype()
                                if ip_address_type == 'PUBLIC':
                                    if 1 <= peer_tcp_port <= 65535:
                                        if not wan_ipv4_address == peer_ip_address:
                                            peer_list = [peer_ip_address, peer_tcp_port]
                                            peer_list_result = False
                                            for j in peers:
                                                if operator.eq(j, peer_list) is True:
                                                    peer_list_result = True
                                            if peer_list_result is False:
                                                peers.append(peer_list)
                    if 'peers6' in message:
                        if type(message.get('peers6')) == bytes:
                            for i in range(0, len(message.get('peers6')), 18):
                                peer6_ip_address = socket.inet_ntop(socket.AF_INET6, message.get('peers6')[i:i + 16])
                                peer6_tcp_port = struct.unpack_from('!H', message.get('peers6'), i + 16)[0]
                                ip_address_type = IPy.IP(peer6_ip_address).iptype()[:9]
                                if ip_address_type == 'ALLOCATED':
                                    if 1 <= peer6_tcp_port <= 65535:
                                        if not wan_ipv6_address == peer6_ip_address:
                                            peer6_list = [peer6_ip_address, peer6_tcp_port]
                                            peer6_list_result = False
                                            for j in peers6:
                                                if operator.eq(j, peer6_list) is True:
                                                    peer6_list_result = True
                                            if peer6_list_result is False:
                                                peers6.append(peer6_list)
                    result = {
                        'complete': complete,
                        'downloaded': downloaded,
                        'incomplete': incomplete,
                        'interval': interval,
                        'min_interval': min_interval,
                        'peers': peers,
                        'peers6': peers6,
                        'status': True
                    }
                    return result
                else:
                    result = {
                        'error': response.status_code,
                        'status': False
                    }
                    return result
            except httpx.HTTPError as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            except Exception as error:
                result = {
                    'error': error,
                    'status': False
                }
                return result
            finally:
                locals().clear()