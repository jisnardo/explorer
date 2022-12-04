from .bootstrap_http_trackers import bootstrap_http_trackers
from .bootstrap_udp_trackers import bootstrap_udp_trackers
from .database import insert
from .http_tracker import http_tracker
from .indexer import indexer
from .krpc import append_info_hash
from .krpc import get_peers
from .krpc import query_announce_info_hashes
from .krpc import query_get_peers_info_hashes
from .krpc import query_nodes_number
from .krpc import sample_infohashes
from .memory import memory
from .peer_wire import ut_metadata
from .ping import ping
from .save_torrent_files import save_torrent_files
from .searcher import searcher
from .torrent_information_parser import torrent_information_parser
from .torrents_downloader import torrents_downloader
from .udp_tracker import udp_tracker

def add_info_hash(info_hash):
    '''

    explorer_spider.add_info_hash()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        None

    '''
    append_info_hash.spider_krpc_append_info_hash_messages.put(
        info_hash
    )

def get_info_hash(keyword):
    '''

    explorer_spider.get_info_hash()

    Args:
        keyword: string.

    Returns:
        For example:

        ['59abaad8e68806ebac108bd69b13d7e9a38be5fb', 'cf0a537944c001ad86b1ca058e8d877f5f022fc6']

    '''
    apibay_result = searcher().apibay(keyword)
    ytsmx_result = searcher().ytsmx(keyword)
    result = []
    if apibay_result['status'] is True:
        for i in apibay_result['data']:
            if i not in result:
                result.append(i)
    if ytsmx_result['status'] is True:
        for j in ytsmx_result['data']:
            if j not in result:
                result.append(j)
    return result

def ipv4_network_connectivity():
    '''

    explorer_spider.ipv4_network_connectivity()

    Args:
        None

    Returns:
        True or False.

    '''
    return memory.ipv4_network_connectivity

def ipv6_network_connectivity():
    '''

    explorer_spider.ipv6_network_connectivity()

    Args:
        None

    Returns:
        True or False.

    '''
    return memory.ipv6_network_connectivity

def launch(explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6, explorer_peer_wire_v4, explorer_peer_wire_v6, explorer_udp_tracker_v4, explorer_udp_tracker_v6):
    '''

    explorer_spider.launch()

    Args:
        explorer_database: explorer_database package
        explorer_http_tracker: explorer_http_tracker package
        explorer_krpc_v4: explorer_krpc_v4 package
        explorer_krpc_v6: explorer_krpc_v6 package
        explorer_peer_wire_v4: explorer_peer_wire_v4 package
        explorer_peer_wire_v6: explorer_peer_wire_v6 package
        explorer_udp_tracker_v4: explorer_udp_tracker_v4 package
        explorer_udp_tracker_v6: explorer_udp_tracker_v6 package

    '''
    append_info_hash().start(explorer_database)
    bootstrap_http_trackers().start()
    bootstrap_udp_trackers().start()
    get_peers().start(explorer_database, explorer_krpc_v4, explorer_krpc_v6)
    http_tracker().start(explorer_database, explorer_http_tracker, explorer_krpc_v4, explorer_krpc_v6)
    indexer().start()
    insert().start(explorer_database)
    ping().start()
    query_announce_info_hashes().start(explorer_database, explorer_krpc_v4, explorer_krpc_v6)
    query_get_peers_info_hashes().start(explorer_database, explorer_krpc_v4, explorer_krpc_v6)
    query_nodes_number().start(explorer_database, explorer_krpc_v4, explorer_krpc_v6)
    sample_infohashes().start(explorer_database, explorer_krpc_v4, explorer_krpc_v6)
    save_torrent_files().start()
    searcher().start()
    torrent_information_parser().start()
    torrents_downloader().start(explorer_database)
    udp_tracker().start(explorer_database, explorer_krpc_v4, explorer_krpc_v6, explorer_udp_tracker_v4, explorer_udp_tracker_v6)
    ut_metadata().start(explorer_database, explorer_krpc_v4, explorer_krpc_v6, explorer_peer_wire_v4, explorer_peer_wire_v6)

def torrent_parser(metadata):
    '''

    explorer_spider.torrent_parser()

    Args:
        metadata:
            For example:

            {
                'announce': 'https://torrent.ubuntu.com/announce',
                'announce-list': [
                    ['https://torrent.ubuntu.com/announce'],
                    ['https://ipv6.torrent.ubuntu.com/announce']
                ],
                'comment': 'Ubuntu CD releases.ubuntu.com',
                'created by': 'mktorrent 1.1',
                'creation date': 1634219565,
                'info': {
                    'length': 3116482560,
                    'name': 'ubuntu-21.10-desktop-amd64.iso',
                    'piece length': 262144,
                    'pieces': '%a7%c2%d7%12%04N]...'
                }
            }

    Returns:
        For example:

        [
            'f1fcdc1462d36530f526c1d9402eec9100b7ba18',
            'ubuntu-21.10-desktop-amd64.iso',
            {
                '0': {
                    'file_name': 'ubuntu-21.10-desktop-amd64.iso',
                    'file_size': 3116482560
                }
            },
            3116482560
        ]

    '''
    torrent_information_parser.spider_torrent_information_parser_messages_recvfrom.put(
        metadata
    )
    result = torrent_information_parser.spider_torrent_information_parser_messages_send.get()
    return result