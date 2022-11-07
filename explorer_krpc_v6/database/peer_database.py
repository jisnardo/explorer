import IPy
import queue
import re
import threading
import time

class peer_database:
    database_append_peer_messages = queue.Queue()
    database_info_hash_key = {}
    database_delete_peer_messages = queue.Queue()
    database_query_info_hashes_messages_recvfrom = queue.Queue()
    database_query_info_hashes_messages_send = queue.Queue()
    database_query_peers_messages_recvfrom = queue.Queue()
    database_query_peers_messages_send = queue.Queue()

    def __append_peer(self):
        while True:
            database_append_peer_messages = self.database_append_peer_messages.get()
            info_hash = database_append_peer_messages[0]
            ip_address = database_append_peer_messages[1]
            tcp_port = database_append_peer_messages[2]
            pattern = re.compile(r'\b[0-9a-f]{40}\b')
            match = re.match(pattern, info_hash.lower())
            if match is not None:
                ip_address_type = IPy.IP(ip_address).iptype()[:9]
                if ip_address_type == 'ALLOCATED':
                    if 1 <= tcp_port <= 65535:
                        if match.group(0) in self.database_info_hash_key:
                            flag = False
                            for i in self.database_info_hash_key[match.group(0)]:
                                if i[0] == ip_address:
                                    if i[1] == tcp_port:
                                        i[2] = int(time.time())
                                        flag = True
                                        break
                            if flag is False:
                                self.database_info_hash_key[match.group(0)].append([ip_address, tcp_port, int(time.time())])
                        else:
                            self.database_info_hash_key.update({match.group(0): []})
                            self.database_info_hash_key[match.group(0)].append([ip_address, tcp_port, int(time.time())])

    def __check_bad_peers(self):
        while True:
            for i in self.database_info_hash_key.keys():
                for j in self.database_info_hash_key[i]:
                    if j[2] < int(time.time()) - 14400:
                        self.database_info_hash_key[i].remove(j)
            time.sleep(1800)

    def __check_empty_info_hashs(self):
        while True:
            for i in self.database_info_hash_key.keys():
                if i is False:
                    del self.database_info_hash_key[i]
            time.sleep(60)

    def __delete_peer(self):
        while True:
            database_delete_peer_messages = self.database_delete_peer_messages.get()
            info_hash = database_delete_peer_messages[0]
            ip_address = database_delete_peer_messages[1]
            tcp_port = database_delete_peer_messages[2]
            if info_hash in self.database_info_hash_key:
                for i in self.database_info_hash_key[info_hash]:
                    if i[0] == ip_address:
                        if i[1] == tcp_port:
                            self.database_info_hash_key[info_hash].remove(i)

    def __query_info_hashes(self):
        while True:
            self.database_query_info_hashes_messages_recvfrom.get()
            samples = []
            for i in self.database_info_hash_key.keys():
                samples.append(i)
            self.database_query_info_hashes_messages_send.put(
                samples
            )

    def __query_peers(self):
        while True:
            info_hash = self.database_query_peers_messages_recvfrom.get()
            if info_hash in self.database_info_hash_key:
                self.database_query_peers_messages_send.put(
                    self.database_info_hash_key[info_hash]
                )
            else:
                self.database_query_peers_messages_send.put(
                    []
                )

    def start(self):
        explorer_krpc_v6_database_peer_database_append_peer_thread = threading.Thread(target = self.__append_peer)
        explorer_krpc_v6_database_peer_database_append_peer_thread.setDaemon(True)
        explorer_krpc_v6_database_peer_database_append_peer_thread.start()
        explorer_krpc_v6_database_peer_database_check_bad_peers_thread = threading.Thread(target = self.__check_bad_peers)
        explorer_krpc_v6_database_peer_database_check_bad_peers_thread.setDaemon(True)
        explorer_krpc_v6_database_peer_database_check_bad_peers_thread.start()
        explorer_krpc_v6_database_peer_database_check_empty_info_hashs_thread = threading.Thread(target = self.__check_empty_info_hashs)
        explorer_krpc_v6_database_peer_database_check_empty_info_hashs_thread.setDaemon(True)
        explorer_krpc_v6_database_peer_database_check_empty_info_hashs_thread.start()
        explorer_krpc_v6_database_peer_database_delete_peer_thread = threading.Thread(target = self.__delete_peer)
        explorer_krpc_v6_database_peer_database_delete_peer_thread.setDaemon(True)
        explorer_krpc_v6_database_peer_database_delete_peer_thread.start()
        explorer_krpc_v6_database_peer_database_query_info_hashes_thread = threading.Thread(target = self.__query_info_hashes)
        explorer_krpc_v6_database_peer_database_query_info_hashes_thread.setDaemon(True)
        explorer_krpc_v6_database_peer_database_query_info_hashes_thread.start()
        explorer_krpc_v6_database_peer_database_query_peers_thread = threading.Thread(target = self.__query_peers)
        explorer_krpc_v6_database_peer_database_query_peers_thread.setDaemon(True)
        explorer_krpc_v6_database_peer_database_query_peers_thread.start()