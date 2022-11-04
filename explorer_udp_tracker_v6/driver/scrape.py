from ..driver.packer import packer_messages
from ..driver.unpacker import unpacker_messages
import random
import socket

class scrape:
    def scrape(self, ip_address, udp_port, info_hash):
        socket_server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        socket_server.settimeout(10)
        transaction_id = random.randint(1, 255)
        message = packer_messages().connect(transaction_id)
        try:
            socket_server.sendto(message, (ip_address, udp_port))
            (message, server_address) = socket_server.recvfrom(65536)
            if server_address[0] == ip_address and server_address[1] == udp_port:
                connect_messages = unpacker_messages().connect(message)
                if connect_messages[0] == 0 and connect_messages[1] == transaction_id:
                    connection_id = connect_messages[2]
                    message = packer_messages().scrape(connection_id, transaction_id, info_hash)
                    socket_server.sendto(message, (ip_address, udp_port))
                    (message, server_address) = socket_server.recvfrom(65536)
                    if server_address[0] == ip_address and server_address[1] == udp_port:
                        scrape_messages = unpacker_messages().scrape(message)
                        if scrape_messages[0] == 2 and scrape_messages[1] == transaction_id:
                            socket_server.close()
                            seeders = scrape_messages[2]
                            completed = scrape_messages[3]
                            leechers = scrape_messages[4]
                            result = {
                                'seeders': seeders,
                                'completed': completed,
                                'leechers': leechers,
                                'state': True
                            }
                            return result
                        elif scrape_messages[0] == 3 and scrape_messages[1] == transaction_id:
                            socket_server.close()
                            error_message = scrape_messages[2]
                            result = {
                                'error': error_message,
                                'state': False
                            }
                            return result
                    else:
                        socket_server.close()
                        result = {
                            'state': False
                        }
                        return result
                elif connect_messages[0] == 3 and connect_messages[1] == transaction_id:
                    socket_server.close()
                    error_message = connect_messages[2]
                    result = {
                        'error': error_message,
                        'state': False
                    }
                    return result
            else:
                socket_server.close()
                result = {
                    'state': False
                }
                return result
        except Exception as error:
            socket_server.close()
            result = {
                'error': error,
                'state': False
            }
            return result
        finally:
            locals().clear()