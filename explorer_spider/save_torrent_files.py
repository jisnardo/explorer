from .torrent_information_parser import torrent_information_parser
import json
import os
import pyben
import queue
import threading

class save_torrent_files:
    spider_save_torrent_files_messages = queue.Queue()

    def __listen(self):
        while True:
            spider_save_torrent_files_messages = self.spider_save_torrent_files_messages.get()
            torrent_information_parser.spider_torrent_information_parser_messages_recvfrom.put(
                spider_save_torrent_files_messages
            )
            spider_torrent_information_parser_messages_send = torrent_information_parser.spider_torrent_information_parser_messages_send.get()
            if spider_torrent_information_parser_messages_send is not False:
                info_hash = spider_torrent_information_parser_messages_send[0]
                torrent_name = spider_torrent_information_parser_messages_send[1]
                with open(os.path.dirname(os.path.abspath(__file__)) + '/save_torrent_files_folder_config.json', mode = 'r', encoding = 'utf-8') as file:
                    config = file.read()
                    save_torrent_files_folder_path = json.loads(config)['save_torrent_files_folder_path']
                    save_torrent_files_name_with_info_hash = json.loads(config)['save_torrent_files_name_with_info_hash']
                    save_torrent_files_name_with_torrent_name = json.loads(config)['save_torrent_files_name_with_torrent_name']
                    if os.path.exists(save_torrent_files_folder_path):
                        write_data = pyben.dumps(spider_save_torrent_files_messages)
                        if save_torrent_files_name_with_info_hash is True:
                            with open(save_torrent_files_folder_path + '/' + info_hash + '.torrent', mode = 'wb') as file:
                                file.write(write_data)
                        if save_torrent_files_name_with_torrent_name is True:
                            with open(save_torrent_files_folder_path + '/' + torrent_name + '.torrent', mode = 'wb') as file:
                                file.write(write_data)

    def start(self):
        explorer_spider_save_torrent_files_listen_thread = threading.Thread(target = self.__listen)
        explorer_spider_save_torrent_files_listen_thread.setDaemon(True)
        explorer_spider_save_torrent_files_listen_thread.start()