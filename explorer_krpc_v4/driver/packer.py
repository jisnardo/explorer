import socket

class krpc_request_messages:
    def announce_peer(self, transaction_id, node_id, info_hash, tcp_port, token):
        message = {
            't': transaction_id,
            'y': 'q',
            'q': 'announce_peer',
            'a': {
                'id': node_id,
                'implied_port': 0,
                'info_hash': info_hash,
                'port': tcp_port,
                'token': token
            },
            'v': 'EP'
        }
        return message

    def find_node(self, transaction_id, node_id, target_id):
        message = {
            't': transaction_id,
            'y': 'q',
            'q': 'find_node',
            'a': {
                'id': node_id,
                'target': target_id
            },
            'v': 'EP'
        }
        return message

    def get_peers(self, transaction_id, node_id, info_hash):
        message = {
            't': transaction_id,
            'y': 'q',
            'q': 'get_peers',
            'a': {
                'id': node_id,
                'info_hash': info_hash
            },
            'v': 'EP'
        }
        return message

    def ping(self, transaction_id, node_id):
        message = {
            't': transaction_id,
            'y': 'q',
            'q': 'ping',
            'a': {
                'id': node_id
            },
            'v': 'EP'
        }
        return message

    def sample_infohashes(self, transaction_id, node_id, target_id):
        message = {
            't': transaction_id,
            'y': 'q',
            'q': 'sample_infohashes',
            'a': {
                'id': node_id,
                'target': target_id
            },
            'v': 'EP'
        }
        return message

class krpc_response_messages:
    def announce_peer(self, transaction_id, node_id, ip_address, udp_port):
        message = {
            'ip': socket.inet_pton(socket.AF_INET, ip_address),
            't': transaction_id,
            'y': 'r',
            'r': {
                'id': node_id,
                'p': udp_port
            },
            'v': 'EP'
        }
        return message

    def find_node(self, transaction_id, node_id, nodes, ip_address, udp_port):
        message = {
            'ip': socket.inet_pton(socket.AF_INET, ip_address),
            't': transaction_id,
            'y': 'r',
            'r': {
                'id': node_id,
                'nodes': nodes,
                'p': udp_port
            },
            'v': 'EP'
        }
        return message

    def get_peers(self, transaction_id, node_id, nodes, values, token, ip_address, udp_port):
        message = {
            'ip': socket.inet_pton(socket.AF_INET, ip_address),
            't': transaction_id,
            'y': 'r',
            'r': {
                'id': node_id,
                'nodes': nodes,
                'token': token,
                'values': values,
                'p': udp_port
            },
            'v': 'EP'
        }
        return message

    def ping(self, transaction_id, node_id, ip_address, udp_port):
        message = {
            'ip': socket.inet_pton(socket.AF_INET, ip_address),
            't': transaction_id,
            'y': 'r',
            'r': {
                'id': node_id,
                'p': udp_port
            },
            'v': 'EP'
        }
        return message

    def sample_infohashes(self, transaction_id, node_id, nodes, number, samples, ip_address, udp_port):
        message = {
            'ip': socket.inet_pton(socket.AF_INET, ip_address),
            't': transaction_id,
            'y': 'r',
            'r': {
                'id': node_id,
                'interval': 14400,
                'nodes': nodes,
                'num': number,
                'samples': samples,
                'p': udp_port
            },
            'v': 'EP'
        }
        return message