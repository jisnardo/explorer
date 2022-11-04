import pyben
import struct

class unpacker_messages:
    def handshake(self, message):
        handshake_bytes_result = {}
        try:
            pstrlen = struct.unpack_from('!B', message)[0]
            handshake_bytes_result['pstrlen'] = pstrlen
            pstr = struct.unpack_from('!19s', message, 1)[0]
            handshake_bytes_result['pstr'] = pstr
            reserved = struct.unpack_from('!Q', message, 20)[0]
            handshake_bytes_result['reserved'] = reserved
            info_hash = struct.unpack_from('!20s', message, 28)[0].hex()
            handshake_bytes_result['info_hash'] = info_hash
            peer_id = struct.unpack_from('!20s', message, 48)[0].hex()
            handshake_bytes_result['peer_id'] = peer_id
            return handshake_bytes_result
        except:
            return handshake_bytes_result
        finally:
            locals().clear()

    def peer_wire(self, message):
        peer_wire_bytes_length = 0
        peer_wire_bytes_result = {}
        try:
            while peer_wire_bytes_length < len(message):
                message_length = struct.unpack_from('!I', message)[0]
                peer_wire_bytes_length = peer_wire_bytes_length + 4
                message = message[4:]
                message_type = struct.unpack_from('!B', message)[0]
                peer_wire_bytes_length = peer_wire_bytes_length + 1
                message = message[1:]
                if message_type == 0:
                    peer_wire_bytes_result['type_0'] = False
                if message_type == 1:
                    peer_wire_bytes_result['type_1'] = True
                if message_type == 9:
                    peer_wire_bytes_result['type_9'] = struct.unpack_from('!H', message)[0]
                    peer_wire_bytes_length = peer_wire_bytes_length + 2
                    message = message[2:]
                if message_type == 20:
                    extended_message_type = struct.unpack_from('!B', message)[0]
                    peer_wire_bytes_length = peer_wire_bytes_length + 1
                    message = message[1:]
                    if extended_message_type == 0:
                        payload = pyben.loads(message[:message_length - 2])
                        peer_wire_bytes_result['type_20'] = {
                            'payload': payload,
                            'data': ''
                        }
                        peer_wire_bytes_length = peer_wire_bytes_length + message_length - 2
                        message = message[message_length - 2:]
                    else:
                        payload = pyben.loads(message[:message_length - 2])
                        data = message[len(pyben.dumps(payload)):message_length - 2]
                        peer_wire_bytes_result['type_20'] = {
                            'payload': payload,
                            'data': data
                        }
                        peer_wire_bytes_length = peer_wire_bytes_length + message_length - 2
                        message = message[message_length - 2:]
            return peer_wire_bytes_result
        except:
            return peer_wire_bytes_result
        finally:
            locals().clear()