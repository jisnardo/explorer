import IPy
import queue
import re
import threading
import time

class token_manager:
    database_append_token_messages = queue.Queue()
    database_query_token_messages_recvfrom = queue.Queue()
    database_query_token_messages_send = queue.Queue()
    database_token = []

    def __append_token(self):
        while True:
            database_append_token_messages = self.database_append_token_messages.get()
            node_id = database_append_token_messages[0]
            ip_address = database_append_token_messages[1]
            udp_port = database_append_token_messages[2]
            token = database_append_token_messages[3]
            pattern = re.compile(r'\b[0-9a-f]{40}\b')
            match = re.match(pattern, node_id.lower())
            if match is not None:
                ip_address_type = IPy.IP(ip_address).iptype()
                if ip_address_type == 'PUBLIC':
                    if 1 <= udp_port <= 65535:
                        if len(token) == 4:
                            flag = False
                            for i in self.database_token:
                                if match.group(0) == i[0]:
                                    if ip_address == i[1]:
                                        if udp_port == i[2]:
                                            i[3] = token
                                            i[4] = int(time.time())
                                            flag = True
                            if flag is False:
                                self.database_token.append([match.group(0), ip_address, udp_port, token, int(time.time())])

    def __check_bad_token(self):
        while True:
            for i in self.database_token:
                if i[4] < int(time.time()) - 21600:
                    self.database_token.remove(i)
            time.sleep(21600)

    def __query_token(self):
        while True:
            target_id = self.database_query_token_messages_recvfrom.get()
            if len(self.database_token) > 0:
                distance = []
                for i in self.database_token:
                    node_id = i[0]
                    distance.append(int(target_id, 16) ^ int(node_id, 16))
                distance.sort()
                for i in self.database_token:
                    node_id = i[0]
                    if distance[0] == int(target_id, 16) ^ int(node_id, 16):
                        self.database_query_token_messages_send.put(
                            i
                        )
            else:
                self.database_query_token_messages_send.put(
                    []
                )

    def start(self):
        explorer_krpc_v4_database_token_manager_append_token_thread = threading.Thread(target = self.__append_token)
        explorer_krpc_v4_database_token_manager_append_token_thread.setDaemon(True)
        explorer_krpc_v4_database_token_manager_append_token_thread.start()
        explorer_krpc_v4_database_token_manager_check_bad_token_thread = threading.Thread(target = self.__check_bad_token)
        explorer_krpc_v4_database_token_manager_check_bad_token_thread.setDaemon(True)
        explorer_krpc_v4_database_token_manager_check_bad_token_thread.start()
        explorer_krpc_v4_database_token_manager_query_token_thread = threading.Thread(target = self.__query_token)
        explorer_krpc_v4_database_token_manager_query_token_thread.setDaemon(True)
        explorer_krpc_v4_database_token_manager_query_token_thread.start()