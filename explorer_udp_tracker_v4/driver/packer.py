import struct

class packer_messages:
    def announce_completed(self, connection_id, transaction_id, info_hash, peer_id, downloaded, left, uploaded, tcp_port):
        message = struct.pack('!Q', connection_id)
        message = message + struct.pack('!i', 1)
        message = message + struct.pack('!i', transaction_id)
        message = message + struct.pack('!20s', bytes.fromhex(info_hash))
        message = message + struct.pack('!20s', bytes.fromhex(peer_id))
        message = message + struct.pack('!Q', downloaded)
        message = message + struct.pack('!Q', left)
        message = message + struct.pack('!Q', uploaded)
        message = message + struct.pack('!i', 1)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', -1)
        message = message + struct.pack('!H', tcp_port)
        return message

    def announce_none(self, connection_id, transaction_id, info_hash, peer_id, downloaded, left, uploaded, tcp_port):
        message = struct.pack('!Q', connection_id)
        message = message + struct.pack('!i', 1)
        message = message + struct.pack('!i', transaction_id)
        message = message + struct.pack('!20s', bytes.fromhex(info_hash))
        message = message + struct.pack('!20s', bytes.fromhex(peer_id))
        message = message + struct.pack('!Q', downloaded)
        message = message + struct.pack('!Q', left)
        message = message + struct.pack('!Q', uploaded)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', -1)
        message = message + struct.pack('!H', tcp_port)
        return message

    def announce_started(self, connection_id, transaction_id, info_hash, peer_id, downloaded, left, uploaded, tcp_port):
        message = struct.pack('!Q', connection_id)
        message = message + struct.pack('!i', 1)
        message = message + struct.pack('!i', transaction_id)
        message = message + struct.pack('!20s', bytes.fromhex(info_hash))
        message = message + struct.pack('!20s', bytes.fromhex(peer_id))
        message = message + struct.pack('!Q', downloaded)
        message = message + struct.pack('!Q', left)
        message = message + struct.pack('!Q', uploaded)
        message = message + struct.pack('!i', 2)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', -1)
        message = message + struct.pack('!H', tcp_port)
        return message

    def announce_stopped(self, connection_id, transaction_id, info_hash, peer_id, downloaded, left, uploaded, tcp_port):
        message = struct.pack('!Q', connection_id)
        message = message + struct.pack('!i', 1)
        message = message + struct.pack('!i', transaction_id)
        message = message + struct.pack('!20s', bytes.fromhex(info_hash))
        message = message + struct.pack('!20s', bytes.fromhex(peer_id))
        message = message + struct.pack('!Q', downloaded)
        message = message + struct.pack('!Q', left)
        message = message + struct.pack('!Q', uploaded)
        message = message + struct.pack('!i', 3)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', -1)
        message = message + struct.pack('!H', tcp_port)
        return message

    def connect(self, transaction_id):
        message = struct.pack('!Q', 0x41727101980)
        message = message + struct.pack('!i', 0)
        message = message + struct.pack('!i', transaction_id)
        return message

    def scrape(self, connection_id, transaction_id, info_hash):
        message = struct.pack('!Q', connection_id)
        message = message + struct.pack('!i', 2)
        message = message + struct.pack('!i', transaction_id)
        message = message + struct.pack('!20s', bytes.fromhex(info_hash))
        return message