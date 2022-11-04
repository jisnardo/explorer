import hashlib
import pyben
import queue
import threading

class torrent_information_parser:
    spider_torrent_information_parser_messages_recvfrom = queue.Queue()
    spider_torrent_information_parser_messages_send = queue.Queue()

    def __decode_info_hash(self, message):
        try:
            info = pyben.dumps(message['info'])
            info_hash = hashlib.sha1(info).hexdigest()
            return info_hash
        except:
            return False

    def __decode_torrent_contents(self, message):
        try:
            torrent_contents = {}
            torrent_contents_number = 0
            if 'files' in message['info']:
                for i in range(0, len(message['info']['files'])):
                    if 'path.utf-8' in message['info']['files'][i]:
                        file_name_list = message['info']['files'][i]['path.utf-8']
                        if len(file_name_list) == 1:
                            file_name = file_name_list[0]
                            if type(file_name) == str:
                                torrent_contents.update({str(torrent_contents_number): {}})
                                torrent_contents[str(torrent_contents_number)]['file_name'] = file_name
                                torrent_contents[str(torrent_contents_number)]['file_size'] = message['info']['files'][i]['length']
                                torrent_contents_number = torrent_contents_number + 1
                            else:
                                return False
                        else:
                            file_name = ''
                            for j in file_name_list:
                                file_name = file_name + '/' + j
                            if type(file_name) == str:
                                torrent_contents.update({str(torrent_contents_number): {}})
                                torrent_contents[str(torrent_contents_number)]['file_name'] = file_name
                                torrent_contents[str(torrent_contents_number)]['file_size'] = message['info']['files'][i]['length']
                                torrent_contents_number = torrent_contents_number + 1
                            else:
                                return False
                    else:
                        file_name_list = message['info']['files'][i]['path']
                        if len(file_name_list) == 1:
                            file_name = file_name_list[0]
                            if type(file_name) == str:
                                torrent_contents.update({str(torrent_contents_number): {}})
                                torrent_contents[str(torrent_contents_number)]['file_name'] = file_name
                                torrent_contents[str(torrent_contents_number)]['file_size'] = message['info']['files'][i]['length']
                                torrent_contents_number = torrent_contents_number + 1
                            else:
                                return False
                        else:
                            file_name = ''
                            for j in file_name_list:
                                file_name = file_name + '/' + j
                            if type(file_name) == str:
                                torrent_contents.update({str(torrent_contents_number): {}})
                                torrent_contents[str(torrent_contents_number)]['file_name'] = file_name
                                torrent_contents[str(torrent_contents_number)]['file_size'] = message['info']['files'][i]['length']
                                torrent_contents_number = torrent_contents_number + 1
                            else:
                                return False
            elif 'name.utf-8' in message['info']:
                file_name = message['info']['name.utf-8']
                if type(file_name) == str:
                    torrent_contents.update({str(torrent_contents_number): {}})
                    torrent_contents[str(torrent_contents_number)]['file_name'] = file_name
                    torrent_contents[str(torrent_contents_number)]['file_size'] = message['info']['length']
                    torrent_contents_number = torrent_contents_number + 1
                else:
                    return False
            else:
                file_name = message['info']['name']
                if type(file_name) == str:
                    torrent_contents.update({str(torrent_contents_number): {}})
                    torrent_contents[str(torrent_contents_number)]['file_name'] = file_name
                    torrent_contents[str(torrent_contents_number)]['file_size'] = message['info']['length']
                    torrent_contents_number = torrent_contents_number + 1
                else:
                    return False
            return torrent_contents
        except:
            return False

    def __decode_torrent_name(self, message):
        try:
            if 'name.utf-8' in message['info']:
                torrent_name = message['info']['name.utf-8']
                if type(torrent_name) == str:
                    return torrent_name
                else:
                    return False
            else:
                torrent_name = message['info']['name']
                if type(torrent_name) == str:
                    return torrent_name
                else:
                    return False
        except:
            return False

    def __decode_torrent_size(self, message):
        try:
            if 'files' in message['info']:
                torrent_size = 0
                for i in range(0, len(message['info']['files'])):
                    torrent_size = torrent_size + message['info']['files'][i]['length']
                return torrent_size
            else:
                torrent_size = message['info']['length']
                return torrent_size
        except:
            return False

    def __parser(self):
        while True:
            message = self.spider_torrent_information_parser_messages_recvfrom.get()
            info_hash = self.__decode_info_hash(message)
            torrent_name = self.__decode_torrent_name(message)
            torrent_contents = self.__decode_torrent_contents(message)
            torrent_size = self.__decode_torrent_size(message)
            if info_hash is False:
                self.spider_torrent_information_parser_messages_send.put(
                    False
                )
            elif torrent_name is False:
                self.spider_torrent_information_parser_messages_send.put(
                    False
                )
            elif torrent_contents is False:
                self.spider_torrent_information_parser_messages_send.put(
                    False
                )
            elif torrent_size is False:
                self.spider_torrent_information_parser_messages_send.put(
                    False
                )
            else:
                self.spider_torrent_information_parser_messages_send.put(
                    [info_hash, torrent_name, torrent_contents, torrent_size]
                )

    def start(self):
        explorer_spider_torrent_information_parser_parser_thread = threading.Thread(target = self.__parser)
        explorer_spider_torrent_information_parser_parser_thread.setDaemon(True)
        explorer_spider_torrent_information_parser_parser_thread.start()