from .torrent_information_parser import torrent_information_parser
import queue
import threading

class insert:
    spider_database_insert_messages = queue.Queue()

    def __listen(self, explorer_database):
        while True:
            spider_database_insert_messages = self.spider_database_insert_messages.get()
            torrent_information_parser.spider_torrent_information_parser_messages_recvfrom.put(
                spider_database_insert_messages
            )
            spider_torrent_information_parser_messages_send = torrent_information_parser.spider_torrent_information_parser_messages_send.get()
            if spider_torrent_information_parser_messages_send is not False:
                info_hash = spider_torrent_information_parser_messages_send[0]
                torrent_name = spider_torrent_information_parser_messages_send[1]
                torrent_contents = spider_torrent_information_parser_messages_send[2]
                torrent_size = spider_torrent_information_parser_messages_send[3]
                database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
                if database_count_info_hash_messages['result'] == 0:
                    explorer_database.insert(info_hash, torrent_name, torrent_contents, torrent_size)

    def start(self, explorer_database):
        explorer_spider_database_listen_thread = threading.Thread(target = self.__listen, args = (explorer_database,))
        explorer_spider_database_listen_thread.setDaemon(True)
        explorer_spider_database_listen_thread.start()