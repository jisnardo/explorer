import pyben
import struct

class packer_messages:
    def extended_ut_metadata_handshake(self, metadata_size):
        message = bytes()
        message_type = struct.pack('!B', 20)
        extended_message_type = struct.pack('!B', 0)
        payload = {
            'm': {
                'ut_metadata': 1
            },
            'metadata_size': metadata_size
        }
        payload = pyben.dumps(payload)
        message_length = struct.pack('!I', len(message_type + extended_message_type + payload))
        message = message_length + message_type + extended_message_type + payload
        return message

    def extended_ut_metadata_request(self, extended_message_type, piece):
        message = bytes()
        message_type = struct.pack('!B', 20)
        extended_message_type = struct.pack('!B', extended_message_type)
        payload = {
            'msg_type': 0,
            'piece': piece
        }
        payload = pyben.dumps(payload)
        message_length = struct.pack('!I', len(message_type + extended_message_type + payload))
        message = message_length + message_type + extended_message_type + payload
        return message

    def handshake(self, info_hash, peer_id):
        message = bytes()
        pstrlen = struct.pack('!B', 19)
        pstr = struct.pack('!19s', b'BitTorrent protocol')
        reserved = struct.pack('!Q', 1048577)
        info_hash = struct.pack('!20s', bytes.fromhex(info_hash))
        peer_id = struct.pack('!20s', bytes.fromhex(peer_id))
        message = pstrlen + pstr + reserved + info_hash + peer_id
        return message

    def interested(self):
        message = bytes()
        message_type = struct.pack('!B', 2)
        message_length = struct.pack('!I', len(message_type))
        message = message_length + message_type
        return message