from .database import insert
from .memory import memory
from .save_torrent_files import save_torrent_files
import IPy
import queue
import threading

class ut_metadata:
    spider_peer_wire_v4_ut_metadata_messages = queue.Queue()
    spider_peer_wire_v6_ut_metadata_messages = queue.Queue()

    def __listen_ipv4(self, explorer_database, explorer_krpc_v6, explorer_peer_wire_v4):
        while True:
            spider_peer_wire_v4_ut_metadata_messages = self.spider_peer_wire_v4_ut_metadata_messages.get()
            info_hash = spider_peer_wire_v4_ut_metadata_messages['header']['info_hash']
            for i in spider_peer_wire_v4_ut_metadata_messages['result']:
                ip_address = i[0]
                tcp_port = i[1]
                explorer_spider_peer_wire_work_ipv4_thread = threading.Thread(target = self.__work_ipv4, args = (explorer_database, explorer_krpc_v6, explorer_peer_wire_v4, info_hash, ip_address, tcp_port,))
                explorer_spider_peer_wire_work_ipv4_thread.setDaemon(True)
                explorer_spider_peer_wire_work_ipv4_thread.start()

    def __listen_ipv6(self, explorer_database, explorer_krpc_v4, explorer_peer_wire_v6):
        while True:
            spider_peer_wire_v6_ut_metadata_messages = self.spider_peer_wire_v6_ut_metadata_messages.get()
            info_hash = spider_peer_wire_v6_ut_metadata_messages['header']['info_hash']
            for i in spider_peer_wire_v6_ut_metadata_messages['result']:
                ip_address = i[0]
                tcp_port = i[1]
                explorer_spider_peer_wire_work_ipv6_thread = threading.Thread(target = self.__work_ipv6, args = (explorer_database, explorer_krpc_v4, explorer_peer_wire_v6, info_hash, ip_address, tcp_port,))
                explorer_spider_peer_wire_work_ipv6_thread.setDaemon(True)
                explorer_spider_peer_wire_work_ipv6_thread.start()

    def __work_ipv4(self, explorer_database, explorer_krpc_v6, explorer_peer_wire_v4, info_hash, ip_address, tcp_port):
        peer_wire_v4_ut_metadata_messages = explorer_peer_wire_v4.ut_metadata(info_hash, ip_address, tcp_port)
        if peer_wire_v4_ut_metadata_messages['result'] is not False:
            ipv6_address = peer_wire_v4_ut_metadata_messages['result']['ipv6_address']
            ipv6_udp_port = peer_wire_v4_ut_metadata_messages['result']['ipv6_udp_port']
            if not ipv6_address == '':
                ip_address_type = IPy.IP(ipv6_address).iptype()[:9]
                if ip_address_type == 'ALLOCATED':
                    if 1 <= ipv6_udp_port <= 65535:
                        if memory.ipv6_network_connectivity is True:
                            explorer_spider_peer_wire_work_ipv4_explorer_krpc_v6_ping_thread = threading.Thread(target = explorer_krpc_v6.ping, args = (ipv6_address, ipv6_udp_port,))
                            explorer_spider_peer_wire_work_ipv4_explorer_krpc_v6_ping_thread.setDaemon(True)
                            explorer_spider_peer_wire_work_ipv4_explorer_krpc_v6_ping_thread.start()
            database_count_info_hash_messages = explorer_database.count_info_hash(peer_wire_v4_ut_metadata_messages['header']['info_hash'])
            if database_count_info_hash_messages['result'] == 0:
                insert.spider_database_insert_messages.put({
                    'info': peer_wire_v4_ut_metadata_messages['result']['info']
                })
                save_torrent_files.spider_save_torrent_files_messages.put({
                    'info': peer_wire_v4_ut_metadata_messages['result']['info']
                })
        locals().clear()

    def __work_ipv6(self, explorer_database, explorer_krpc_v4, explorer_peer_wire_v6, info_hash, ip_address, tcp_port):
        peer_wire_v6_ut_metadata_messages = explorer_peer_wire_v6.ut_metadata(info_hash, ip_address, tcp_port)
        if peer_wire_v6_ut_metadata_messages['result'] is not False:
            ipv4_address = peer_wire_v6_ut_metadata_messages['result']['ipv4_address']
            ipv4_udp_port = peer_wire_v6_ut_metadata_messages['result']['ipv4_udp_port']
            if not ipv4_address == '':
                ip_address_type = IPy.IP(ipv4_address).iptype()
                if ip_address_type == 'PUBLIC':
                    if 1 <= ipv4_udp_port <= 65535:
                        if memory.ipv4_network_connectivity is True:
                            explorer_spider_peer_wire_work_ipv6_explorer_krpc_v4_ping_thread = threading.Thread(target = explorer_krpc_v4.ping, args = (ipv4_address, ipv4_udp_port,))
                            explorer_spider_peer_wire_work_ipv6_explorer_krpc_v4_ping_thread.setDaemon(True)
                            explorer_spider_peer_wire_work_ipv6_explorer_krpc_v4_ping_thread.start()
            database_count_info_hash_messages = explorer_database.count_info_hash(peer_wire_v6_ut_metadata_messages['header']['info_hash'])
            if database_count_info_hash_messages['result'] == 0:
                insert.spider_database_insert_messages.put({
                    'info': peer_wire_v6_ut_metadata_messages['result']['info']
                })
                save_torrent_files.spider_save_torrent_files_messages.put({
                    'info': peer_wire_v6_ut_metadata_messages['result']['info']
                })
        locals().clear()

    def start(self, explorer_database, explorer_krpc_v4, explorer_krpc_v6, explorer_peer_wire_v4, explorer_peer_wire_v6):
        explorer_spider_peer_wire_listen_ipv4_thread = threading.Thread(target = self.__listen_ipv4, args = (explorer_database, explorer_krpc_v6, explorer_peer_wire_v4,))
        explorer_spider_peer_wire_listen_ipv4_thread.setDaemon(True)
        explorer_spider_peer_wire_listen_ipv4_thread.start()
        explorer_spider_peer_wire_listen_ipv6_thread = threading.Thread(target = self.__listen_ipv6, args = (explorer_database, explorer_krpc_v4, explorer_peer_wire_v6,))
        explorer_spider_peer_wire_listen_ipv6_thread.setDaemon(True)
        explorer_spider_peer_wire_listen_ipv6_thread.start()