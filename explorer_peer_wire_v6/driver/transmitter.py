from ..driver.packer import packer_messages
from ..driver.unpacker import unpacker_messages
import math
import pyben
import time

class transmission:
    def extension_ut_metadata(self, socket_server, ut_metadata, metadata_size, ipv4_address, ipv4_udp_port):
        try:
            all_piece_number = math.ceil(metadata_size / 16384)
            contract_number = 0
            load_piece_number = 0
            max_contract_number = all_piece_number * 2
            piece = {}
            for i in range(0, all_piece_number):
                piece.update({str(i): b''})
            while True:
                client_extended_ut_metadata_request_message = packer_messages().extended_ut_metadata_request(ut_metadata, load_piece_number)
                socket_server.send(client_extended_ut_metadata_request_message)
                peer_unanalysed_extended_ut_metadata_response_message = socket_server.recv(65536)
                contract_number = contract_number + 1
                peer_extended_ut_metadata_response_message = unpacker_messages().peer_wire(peer_unanalysed_extended_ut_metadata_response_message)
                if 'type_20' in peer_extended_ut_metadata_response_message:
                    if peer_extended_ut_metadata_response_message['type_20']['payload']['piece'] == load_piece_number:
                        if load_piece_number == all_piece_number - 1:
                            last_piece_size = metadata_size - (all_piece_number - 1) * 16384
                            if len(peer_extended_ut_metadata_response_message['type_20']['data']) > last_piece_size - len(piece[str(load_piece_number)]):
                                piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data'][0:last_piece_size - len(piece[str(load_piece_number)])]
                            else:
                                piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data']
                            if len(piece[str(load_piece_number)]) == last_piece_size:
                                break
                        elif len(peer_extended_ut_metadata_response_message['type_20']['data']) > 16384 - len(piece[str(load_piece_number)]):
                            piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data'][0:16384 - len(piece[str(load_piece_number)])]
                        else:
                            piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_extended_ut_metadata_response_message['type_20']['data']
                        if len(piece[str(load_piece_number)]) == 16384:
                            load_piece_number = load_piece_number + 1
                elif load_piece_number == all_piece_number - 1:
                    last_piece_size = metadata_size - (all_piece_number - 1) * 16384
                    if len(peer_unanalysed_extended_ut_metadata_response_message) > last_piece_size - len(piece[str(load_piece_number)]):
                        piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message[0:last_piece_size - len(piece[str(load_piece_number)])]
                    else:
                        piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message
                    if len(piece[str(load_piece_number)]) == last_piece_size:
                        break
                elif len(peer_unanalysed_extended_ut_metadata_response_message) > 16384 - len(piece[str(load_piece_number)]):
                    piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message[0:16384 - len(piece[str(load_piece_number)])]
                else:
                    piece[str(load_piece_number)] = piece[str(load_piece_number)] + peer_unanalysed_extended_ut_metadata_response_message
                if len(piece[str(load_piece_number)]) == 16384:
                    load_piece_number = load_piece_number + 1
                if contract_number >= max_contract_number:
                    break
                elif contract_number < max_contract_number:
                    time.sleep(1)
            load_data = bytes()
            for j in range(0, all_piece_number):
                load_data = load_data + piece[str(j)]
            torrent_data = {}
            torrent_data.update({
                'info': pyben.loads(load_data),
                'ipv4_address': ipv4_address,
                'ipv4_udp_port': ipv4_udp_port
            })
            return torrent_data
        except:
            return False
        finally:
            locals().clear()