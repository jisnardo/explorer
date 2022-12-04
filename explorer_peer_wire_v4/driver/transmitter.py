from ..driver.packer import packer_messages
from ..driver.unpacker import unpacker_messages
import math
import pyben
import queue
import threading
import time

class transmission:
    driver_transmission_extension_ut_metadata_messages_recvfrom = queue.Queue()
    driver_transmission_extension_ut_metadata_messages_send = queue.Queue()
    driver_transmission_extension_ut_metadata_progress = {}
    driver_transmission_extension_ut_metadata_progress_key = 0

    def __check_outdated_extension_ut_metadata_progress_messages(self):
        while True:
            for i in list(self.driver_transmission_extension_ut_metadata_progress.keys()):
                if self.driver_transmission_extension_ut_metadata_progress[i]['update_time'] < int(time.time()) - 300:
                    del self.driver_transmission_extension_ut_metadata_progress[i]
            if self.driver_transmission_extension_ut_metadata_progress_key > 10000:
                self.driver_transmission_extension_ut_metadata_progress_key = 0
            time.sleep(300)

    def __downloader(self, socket_server, info_hash, ip_address, tcp_port, ut_metadata, metadata_size):
        try:
            all_piece_number = math.ceil(metadata_size / 16384)
            contract_number = 0
            load_piece_number = 0
            max_contract_number = all_piece_number * 10
            peer_unanalysed_extended_ut_metadata_response_messages = bytes()
            piece = {}
            for i in range(0, all_piece_number):
                piece.update({str(i): b''})
            piece_transmission = False
            reject = False
            key = self.driver_transmission_extension_ut_metadata_progress_key
            self.driver_transmission_extension_ut_metadata_progress_key = self.driver_transmission_extension_ut_metadata_progress_key + 1
            if all_piece_number == 1:
                self.driver_transmission_extension_ut_metadata_progress[str(key)] = {
                    'info_hash': info_hash,
                    'all_piece_number': all_piece_number,
                    'load_piece_number': load_piece_number,
                    'ip_address': ip_address,
                    'tcp_port': tcp_port,
                    'status': False,
                    'update_time': int(time.time())
                }
            else:
                self.driver_transmission_extension_ut_metadata_progress[str(key)] = {
                    'info_hash': info_hash,
                    'all_piece_number': all_piece_number - 1,
                    'load_piece_number': load_piece_number,
                    'ip_address': ip_address,
                    'tcp_port': tcp_port,
                    'status': False,
                    'update_time': int(time.time())
                }
            while True:
                client_extended_ut_metadata_request_message = packer_messages().extended_ut_metadata_request(ut_metadata, load_piece_number)
                socket_server.send(client_extended_ut_metadata_request_message)
                peer_unanalysed_extended_ut_metadata_response_message = socket_server.recv(65536)
                contract_number = contract_number + 1
                peer_extended_ut_metadata_response_message = unpacker_messages().peer_wire(peer_unanalysed_extended_ut_metadata_response_message)
                if 'type_20' in peer_extended_ut_metadata_response_message:
                    peer_unanalysed_extended_ut_metadata_response_messages = bytes()
                    if peer_extended_ut_metadata_response_message['type_20']['payload']['msg_type'] == 1:
                        if peer_extended_ut_metadata_response_message['type_20']['payload']['piece'] == load_piece_number:
                            piece_transmission = True
                            if load_piece_number == all_piece_number - 1:
                                last_piece_size = metadata_size - (all_piece_number - 1) * 16384
                                if len(peer_extended_ut_metadata_response_message['type_20']['data']) > last_piece_size - len(piece[str(load_piece_number)]):
                                    piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data'][0:last_piece_size - len(piece[str(load_piece_number)])]
                                else:
                                    piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data']
                                if len(piece[str(load_piece_number)]) == last_piece_size:
                                    if all_piece_number == 1:
                                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number + 1
                                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = True
                                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                                    else:
                                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number
                                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = True
                                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                                    break
                            elif len(peer_extended_ut_metadata_response_message['type_20']['data']) > 16384 - len(piece[str(load_piece_number)]):
                                piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data'][0:16384 - len(piece[str(load_piece_number)])]
                            else:
                                piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data']
                            if len(piece[str(load_piece_number)]) == 16384:
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                                load_piece_number = load_piece_number + 1
                                piece_transmission = False
                    if peer_extended_ut_metadata_response_message['type_20']['payload']['msg_type'] == 2:
                        reject = True
                        break
                elif piece_transmission is True:
                    if load_piece_number == all_piece_number - 1:
                        last_piece_size = metadata_size - (all_piece_number - 1) * 16384
                        if len(peer_unanalysed_extended_ut_metadata_response_message) > last_piece_size - len(piece[str(load_piece_number)]):
                            piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message[0:last_piece_size - len(piece[str(load_piece_number)])]
                        else:
                            piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message
                        if len(piece[str(load_piece_number)]) == last_piece_size:
                            if all_piece_number == 1:
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number + 1
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = True
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                            else:
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = True
                                self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                            break
                    elif len(peer_unanalysed_extended_ut_metadata_response_message) > 16384 - len(piece[str(load_piece_number)]):
                        piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message[0:16384 - len(piece[str(load_piece_number)])]
                    else:
                        piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message
                    if len(piece[str(load_piece_number)]) == 16384:
                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number
                        self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                        load_piece_number = load_piece_number + 1
                        piece_transmission = False
                else:
                    peer_unanalysed_extended_ut_metadata_response_messages = peer_unanalysed_extended_ut_metadata_response_messages + peer_extended_ut_metadata_response_message
                    peer_extended_ut_metadata_response_message = unpacker_messages().peer_wire(peer_unanalysed_extended_ut_metadata_response_messages)
                    if 'type_20' in peer_extended_ut_metadata_response_message:
                        peer_unanalysed_extended_ut_metadata_response_messages = bytes()
                        if peer_extended_ut_metadata_response_message['type_20']['payload']['msg_type'] == 1:
                            if peer_extended_ut_metadata_response_message['type_20']['payload']['piece'] == load_piece_number:
                                piece_transmission = True
                                if load_piece_number == all_piece_number - 1:
                                    last_piece_size = metadata_size - (all_piece_number - 1) * 16384
                                    if len(peer_extended_ut_metadata_response_message['type_20']['data']) > last_piece_size - len(piece[str(load_piece_number)]):
                                        piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data'][0:last_piece_size - len(piece[str(load_piece_number)])]
                                    else:
                                        piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data']
                                    if len(piece[str(load_piece_number)]) == last_piece_size:
                                        if all_piece_number == 1:
                                            self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number + 1
                                            self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = True
                                            self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                                        else:
                                            self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number
                                            self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = True
                                            self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                                        break
                                elif len(peer_extended_ut_metadata_response_message['type_20']['data']) > 16384 - len(piece[str(load_piece_number)]):
                                    piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data'][0:16384 - len(piece[str(load_piece_number)])]
                                else:
                                    piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data']
                                if len(piece[str(load_piece_number)]) == 16384:
                                    self.driver_transmission_extension_ut_metadata_progress[str(key)]['load_piece_number'] = load_piece_number
                                    self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                                    load_piece_number = load_piece_number + 1
                                    piece_transmission = False
                        if peer_extended_ut_metadata_response_message['type_20']['payload']['msg_type'] == 2:
                            reject = True
                            break
                if contract_number >= max_contract_number:
                    break
                elif contract_number < max_contract_number:
                    time.sleep(1)
            return [reject, all_piece_number, piece, key]
        except:
            return [reject, all_piece_number, piece, key]

    def __extension_ut_metadata_recvfrom(self):
        while True:
            driver_transmission_extension_ut_metadata_messages_recvfrom = self.driver_transmission_extension_ut_metadata_messages_recvfrom.get()
            socket_server = driver_transmission_extension_ut_metadata_messages_recvfrom[0]
            info_hash = driver_transmission_extension_ut_metadata_messages_recvfrom[1]
            ip_address = driver_transmission_extension_ut_metadata_messages_recvfrom[2]
            tcp_port = driver_transmission_extension_ut_metadata_messages_recvfrom[3]
            ut_metadata = driver_transmission_extension_ut_metadata_messages_recvfrom[4]
            metadata_size = driver_transmission_extension_ut_metadata_messages_recvfrom[5]
            ipv6_address = driver_transmission_extension_ut_metadata_messages_recvfrom[6]
            ipv6_udp_port = driver_transmission_extension_ut_metadata_messages_recvfrom[7]
            application_extension_ut_metadata_keyword = driver_transmission_extension_ut_metadata_messages_recvfrom[8]
            explorer_peer_wire_v4_driver_transmission_extension_ut_metadata_send_thread = threading.Thread(target = self.__extension_ut_metadata_send, args = (socket_server, info_hash, ip_address, tcp_port, ut_metadata, metadata_size, ipv6_address, ipv6_udp_port, application_extension_ut_metadata_keyword))
            explorer_peer_wire_v4_driver_transmission_extension_ut_metadata_send_thread.setDaemon(True)
            explorer_peer_wire_v4_driver_transmission_extension_ut_metadata_send_thread.start()

    def __extension_ut_metadata_send(self, socket_server, info_hash, ip_address, tcp_port, ut_metadata, metadata_size, ipv6_address, ipv6_udp_port, application_extension_ut_metadata_keyword):
        result = self.__downloader(socket_server, info_hash, ip_address, tcp_port, ut_metadata, metadata_size)
        reject = result[0]
        all_piece_number = result[1]
        piece = result[2]
        key = result[3]
        if reject is True:
            self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = False
            self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
            self.driver_transmission_extension_ut_metadata_messages_send.put(
                [False, socket_server, info_hash, application_extension_ut_metadata_keyword]
            )
        else:
            load_data = bytes()
            for j in range(0, all_piece_number):
                load_data = load_data + piece[str(j)]
            if len(load_data) == metadata_size:
                try:
                    torrent_data = {}
                    torrent_data.update({
                        'info': pyben.loads(load_data),
                        'ipv6_address': ipv6_address,
                        'ipv6_udp_port': ipv6_udp_port
                    })
                    self.driver_transmission_extension_ut_metadata_messages_send.put(
                        [torrent_data, socket_server, info_hash, application_extension_ut_metadata_keyword]
                    )
                except:
                    self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = False
                    self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                    self.driver_transmission_extension_ut_metadata_messages_send.put(
                        [False, socket_server, info_hash, application_extension_ut_metadata_keyword]
                    )
            else:
                self.driver_transmission_extension_ut_metadata_progress[str(key)]['status'] = False
                self.driver_transmission_extension_ut_metadata_progress[str(key)]['update_time'] = int(time.time())
                self.driver_transmission_extension_ut_metadata_messages_send.put(
                    [False, socket_server, info_hash, application_extension_ut_metadata_keyword]
                )

    def start(self):
        explorer_peer_wire_v4_driver_transmission_check_outdated_extension_ut_metadata_progress_messages_thread = threading.Thread(target = self.__check_outdated_extension_ut_metadata_progress_messages)
        explorer_peer_wire_v4_driver_transmission_check_outdated_extension_ut_metadata_progress_messages_thread.setDaemon(True)
        explorer_peer_wire_v4_driver_transmission_check_outdated_extension_ut_metadata_progress_messages_thread.start()
        explorer_peer_wire_v4_driver_transmission_extension_ut_metadata_recvfrom_thread = threading.Thread(target = self.__extension_ut_metadata_recvfrom)
        explorer_peer_wire_v4_driver_transmission_extension_ut_metadata_recvfrom_thread.setDaemon(True)
        explorer_peer_wire_v4_driver_transmission_extension_ut_metadata_recvfrom_thread.start()