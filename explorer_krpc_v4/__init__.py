from .application import application_loader
from .application.command.commander import commander
from .database import database_loader
from .database.distributed_hash_table import distributed_hash_table
from .database.peer_database import peer_database
from .driver import driver_loader
from .driver.memory import memory
import copy
import IPy
import re
import time

def announce_peer(info_hash, tcp_port):
    '''

    explorer_krpc_v4.announce_peer()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'node_id': '59abaad8e68806ebac108bd69b13d7e9a38be5fb',
                'ip_address': '8.8.4.4',
                'storing': True,
                'udp_port': 51413
            },
            'header': {
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        if 1 <= tcp_port <= 65535:
            commander.application_commander_announce_peer_messages_recvfrom.put(
                [match.group(0), tcp_port]
            )
            result = commander.application_commander_announce_peer_messages_send.get()
            return result

def append_peer(info_hash, ip_address, tcp_port):
    '''

    explorer_krpc_v4.append_peer()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        ip_address: ipv4 ip.
        tcp_port: decimal number(1 - 65535).

    Returns:
        None

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()
        if ip_address_type == 'PUBLIC':
            if 1 <= tcp_port <= 65535:
                peer_database.database_append_peer_messages.put(
                    [match.group(0), ip_address, tcp_port]
                )

def delete_peer(info_hash, ip_address, tcp_port):
    '''

    explorer_krpc_v4.delete_peer()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        ip_address: ipv4 ip.
        tcp_port: decimal number(1 - 65535).

    Returns:
        None

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        ip_address_type = IPy.IP(ip_address).iptype()
        if ip_address_type == 'PUBLIC':
            if 1 <= tcp_port <= 65535:
                peer_database.database_delete_peer_messages.put(
                    [match.group(0), ip_address, tcp_port]
                )

def find_node(target_id):
    '''

    explorer_krpc_v4.find_node()

    Args:
        target_id: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
    
    Returns:
        For example:

        {
            'result': True,
            'header': {
                'target_id': '59abaad8e68806ebac108bd69b13d7e9a38be5fb',
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, target_id.lower())
    if match is not None:
        commander.application_commander_find_node_messages_recvfrom.put(
            [match.group(0)]
        )
        result = commander.application_commander_find_node_messages_send.get()
        return result

def get_peers(info_hash):
    '''

    explorer_krpc_v4.get_peers()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        For example:

        {
            'result': [['8.8.4.4', 51413], ['8.8.8.8', 6881]],
            'header': {
                'info_hash': '59abaad8e68806ebac108bd69b13d7e9a38be5fb',
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        commander.application_commander_get_peers_messages_recvfrom.put(
            [match.group(0)]
        )
        values = commander.application_commander_get_peers_messages_send.get()
        return values

def ping(ip_address, udp_port):
    '''

    explorer_krpc_v4.ping()

    Args:
        ip_address: ipv4 ip.
        udp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': True,
            'header': {
                'ip_address': '8.8.4.4',
                'udp_port': 51413
            }
        }

    '''
    ip_address_type = IPy.IP(ip_address).iptype()
    if ip_address_type == 'PUBLIC':
        if 1 <= udp_port <= 65535:
            commander.application_commander_ping_messages_recvfrom.put(
                [ip_address, udp_port]
            )
            result = commander.application_commander_ping_messages_send.get()
            return result

def query_info_hashes():
    '''

    explorer_krpc_v4.query_info_hashes()

    Args:
        None

    Returns:
        For example:

        {
            '59abaad8e68806ebac108bd69b13d7e9a38be5fb': [
                ['8.8.4.4', 51413, 1666969066]
            ],
            'cf0a537944c001ad86b1ca058e8d877f5f022fc6': [
                ['8.8.8.8', 6881, 1666969123]
            ]
        }

    '''
    return copy.deepcopy(peer_database.database_info_hash_key)

def query_nodes():
    '''

    explorer_krpc_v4.query_nodes()

    Args:
        None

    Returns:
        For example:

        {
            '0': {
                'update_time': 1666702844,
                '0': {
                    'node_id': '59abaad8e68806ebac108bd69b13d7e9a38be5fb',
                    'ip_address': '8.8.4.4',
                    'udp_port': 51413
                },
            ...
            }
        }

    '''
    return copy.deepcopy(distributed_hash_table.database_binary_tree)

def query_nodes_number():
    '''

    explorer_krpc_v4.query_nodes_number()

    Args:
        None

    Returns:
        For example:

        47

    '''
    distributed_hash_table.database_query_nodes_number_messages_recvfrom.put(
        0
    )
    nodes_number = distributed_hash_table.database_query_nodes_number_messages_send.get()
    return nodes_number

def sample_infohashes(target_id):
    '''

    explorer_krpc_v4.sample_infohashes()

    Args:
        target_id: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        For example:

        {
            'result': ['59abaad8e68806ebac108bd69b13d7e9a38be5fb', 'cf0a537944c001ad86b1ca058e8d877f5f022fc6'],
            'header': {
                'target_id': '34037b2321855f5151686fb877120eabf231f628'
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, target_id.lower())
    if match is not None:
        commander.application_commander_sample_infohashes_messages_recvfrom.put(
            [match.group(0)]
        )
        samples = commander.application_commander_sample_infohashes_messages_send.get()
        return samples

def self_ip_address():
    '''

    explorer_krpc_v4.self_ip_address()

    Args:
        None

    Returns:
        For example:

        '8.8.4.4'

    '''
    return memory().ip_address

def self_node_id():
    '''

    explorer_krpc_v4.self_node_id()

    Args:
        None

    Returns:
        For example:

        '59abaad8e68806ebac108bd69b13d7e9a38be5fb'

    '''
    return memory().node_id

def self_udp_port():
    '''

    explorer_krpc_v4.self_udp_port()

    Args:
        None

    Returns:
        For example:

        6881

    '''
    return memory().udp_port

driver_loader().launch()
time.sleep(1)
database_loader().launch()
time.sleep(1)
application_loader().launch()
time.sleep(1)