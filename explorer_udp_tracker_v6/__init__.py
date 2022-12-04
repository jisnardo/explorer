from .application import application_loader
from .application.udp_tracker_announce_completed import udp_tracker_announce_completed
from .application.udp_tracker_announce_none import udp_tracker_announce_none
from .application.udp_tracker_announce_started import udp_tracker_announce_started
from .application.udp_tracker_announce_stopped import udp_tracker_announce_stopped
from .application.udp_tracker_scrape import udp_tracker_scrape
from .driver import driver_loader
from .driver.memory import memory
import IPy
import re

def announce_completed(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_udp_tracker_v6.announce_completed()

    Args:
        ip_address: ipv6 ip.
        udp_port: decimal number(1 - 65535).
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        downloaded: decimal number.
        left: decimal number.
        uploaded: decimal number.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'interval': 1994,
                'leechers': 1,
                'seeders': 3,
                'peers6': [],
                'status': True
            },
            'header': {
                'ip_address': 'fe80::1',
                'udp_port': 6969,
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()[:9]
        if ip_address_type == 'ALLOCATED':
            if 1 <= udp_port <= 65535:
                if 1 <= tcp_port <= 65535:
                    udp_tracker_announce_completed.application_udp_tracker_announce_completed_messages_recvfrom.put(
                        [ip_address, udp_port, match.group(0), downloaded, left, uploaded, tcp_port]
                    )
                    result = udp_tracker_announce_completed.application_udp_tracker_announce_completed_messages_send.get()
                    return result

def announce_none(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_udp_tracker_v6.announce_none()

    Args:
        ip_address: ipv6 ip.
        udp_port: decimal number(1 - 65535).
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        downloaded: decimal number.
        left: decimal number.
        uploaded: decimal number.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'interval': 1994,
                'leechers': 1,
                'seeders': 3,
                'peers6': [['2001:4860:4860::8844', 51413], ['2001:4860:4860::8888', 6881]],
                'status': True
            },
            'header': {
                'ip_address': 'fe80::1',
                'udp_port': 6969,
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()[:9]
        if ip_address_type == 'ALLOCATED':
            if 1 <= udp_port <= 65535:
                if 1 <= tcp_port <= 65535:
                    udp_tracker_announce_none.application_udp_tracker_announce_none_messages_recvfrom.put(
                        [ip_address, udp_port, match.group(0), downloaded, left, uploaded, tcp_port]
                    )
                    result = udp_tracker_announce_none.application_udp_tracker_announce_none_messages_send.get()
                    return result

def announce_started(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_udp_tracker_v6.announce_started()

    Args:
        ip_address: ipv6 ip.
        udp_port: decimal number(1 - 65535).
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        downloaded: decimal number.
        left: decimal number.
        uploaded: decimal number.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'interval': 1994,
                'leechers': 1,
                'seeders': 3,
                'peers6': [['2001:4860:4860::8844', 51413], ['2001:4860:4860::8888', 6881]],
                'status': True
            },
            'header': {
                'ip_address': 'fe80::1',
                'udp_port': 6969,
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()[:9]
        if ip_address_type == 'ALLOCATED':
            if 1 <= udp_port <= 65535:
                if 1 <= tcp_port <= 65535:
                    udp_tracker_announce_started.application_udp_tracker_announce_started_messages_recvfrom.put(
                        [ip_address, udp_port, match.group(0), downloaded, left, uploaded, tcp_port]
                    )
                    result = udp_tracker_announce_started.application_udp_tracker_announce_started_messages_send.get()
                    return result

def announce_stopped(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_udp_tracker_v6.announce_stopped()

    Args:
        ip_address: ipv6 ip.
        udp_port: decimal number(1 - 65535).
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        downloaded: decimal number.
        left: decimal number.
        uploaded: decimal number.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'interval': 1994,
                'leechers': 1,
                'seeders': 3,
                'peers6': [],
                'status': True
            },
            'header': {
                'ip_address': 'fe80::1',
                'udp_port': 6969,
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()[:9]
        if ip_address_type == 'ALLOCATED':
            if 1 <= udp_port <= 65535:
                if 1 <= tcp_port <= 65535:
                    udp_tracker_announce_stopped.application_udp_tracker_announce_stopped_messages_recvfrom.put(
                        [ip_address, udp_port, match.group(0), downloaded, left, uploaded, tcp_port]
                    )
                    result = udp_tracker_announce_stopped.application_udp_tracker_announce_stopped_messages_send.get()
                    return result

def scrape(ip_address, udp_port, info_hash):
    '''

    explorer_udp_tracker_v6.scrape()

    Args:
        ip_address: ipv6 ip.
        udp_port: decimal number(1 - 65535).
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        For example:

        {
            'result': {
                'seeders': 1,
                'completed': 3,
                'leechers': 0,
                'status': True
            },
            'header': {
                'ip_address': 'fe80::1',
                'udp_port': 6969,
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6'
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()[:9]
        if ip_address_type == 'ALLOCATED':
            if 1 <= udp_port <= 65535:
                udp_tracker_scrape.application_udp_tracker_scrape_messages_recvfrom.put(
                    [ip_address, udp_port, match.group(0)]
                )
                result = udp_tracker_scrape.application_udp_tracker_scrape_messages_send.get()
                return result

def self_peer_id():
    '''

    explorer_udp_tracker_v6.self_peer_id()

    Args:
        None

    Returns:
        For example:

        '2d4550303030312d36634e5e356f4b2a3169592a'

    '''
    return memory().peer_id

driver_loader().launch()
application_loader().launch()