from .application import application_loader
from .application.extension_ut_metadata import extension_ut_metadata
from .driver import driver_loader
from .driver.memory import memory
import IPy
import re

def ut_metadata(info_hash, ip_address, tcp_port):
    '''

    explorer_peer_wire_v4.ut_metadata()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        ip_address: ipv4 ip.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'info': {
                    'length': 1331691520,
                    'name': 'ubuntu-20.04.4-live-server-amd64.iso',
                    'piece length': 262144,
                    'pieces': b'\xc8aB\x81h\xda\...'
                },
                'ipv6_address': '2001:4860:4860::8844',
                'ipv6_udp_port': 6881
            },
            'header': {
                'info_hash': '59abaad8e68806ebac108bd69b13d7e9a38be5fb',
                'ip_address': '8.8.8.8',
                'tcp_port': 51413
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()
        if ip_address_type == 'PUBLIC':
            if 1 <= tcp_port <= 65535:
                extension_ut_metadata.application_extension_ut_metadata_messages_recvfrom.put(
                    [match.group(0), ip_address, tcp_port]
                )
                result = extension_ut_metadata.application_extension_ut_metadata_messages_send.get()
                return result

def self_peer_id():
    '''

    explorer_peer_wire_v4.self_peer_id()

    Args:
        None

    Returns:
        For example:

        '2d4550303030312d36634e5e356f4b2a3169592a'

    '''
    return memory().peer_id

driver_loader().launch()
application_loader().launch()