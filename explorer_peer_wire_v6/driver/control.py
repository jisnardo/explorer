from ..driver.checker import check
from ..driver.connecter import connection
from ..driver.transmitter import transmission
import queue
import socket
import threading
import time

class control:
    driver_control_extension_ut_metadata_messages_recvfrom = queue.Queue()
    driver_control_extension_ut_metadata_messages_send = queue.Queue()

    def __extension_ut_metadata_recvfrom(self):
        while True:
            driver_control_extension_ut_metadata_messages_recvfrom = self.driver_control_extension_ut_metadata_messages_recvfrom.get()
            info_hash = driver_control_extension_ut_metadata_messages_recvfrom[0]
            ip_address = driver_control_extension_ut_metadata_messages_recvfrom[1]
            tcp_port = driver_control_extension_ut_metadata_messages_recvfrom[2]
            application_extension_ut_metadata_keyword = driver_control_extension_ut_metadata_messages_recvfrom[3]
            explorer_peer_wire_v6_driver_control_extension_ut_metadata_send_thread = threading.Thread(target = self.__extension_ut_metadata_send, args = (info_hash, ip_address, tcp_port, application_extension_ut_metadata_keyword))
            explorer_peer_wire_v6_driver_control_extension_ut_metadata_send_thread.setDaemon(True)
            explorer_peer_wire_v6_driver_control_extension_ut_metadata_send_thread.start()

    def __extension_ut_metadata_send(self, info_hash, ip_address, tcp_port, application_extension_ut_metadata_keyword):
        socket_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        socket_server.settimeout(120)
        connection_connect_messages = connection().connect(socket_server, ip_address, tcp_port)
        if connection_connect_messages is True:
            time.sleep(1)
            connection_handshake_messages = connection().handshake(socket_server, info_hash)
            if connection_handshake_messages is not False:
                peer_unanalysed_handshake_response_message = connection_handshake_messages
                time.sleep(1)
                connection_extension_ut_metadata_messages = connection().extension_ut_metadata(socket_server, peer_unanalysed_handshake_response_message)
                if connection_extension_ut_metadata_messages is not False:
                    time.sleep(1)
                    connection_interested_messages = connection().interested(socket_server)
                    if connection_interested_messages is True:
                        ut_metadata = connection_extension_ut_metadata_messages[0]
                        metadata_size = connection_extension_ut_metadata_messages[1]
                        ipv4_address = connection_extension_ut_metadata_messages[2]
                        ipv4_udp_port = connection_extension_ut_metadata_messages[3]
                        time.sleep(1)
                        transmission.driver_transmission_extension_ut_metadata_messages_recvfrom.put(
                            [socket_server, info_hash, ip_address, tcp_port, ut_metadata, metadata_size, ipv4_address, ipv4_udp_port, application_extension_ut_metadata_keyword]
                        )
                        transmission_extension_ut_metadata_messages = transmission.driver_transmission_extension_ut_metadata_messages_send.get()
                        torrent_data = transmission_extension_ut_metadata_messages[0]
                        socket_server = transmission_extension_ut_metadata_messages[1]
                        info_hash = transmission_extension_ut_metadata_messages[2]
                        application_extension_ut_metadata_keyword = transmission_extension_ut_metadata_messages[3]
                        socket_server.close()
                        if torrent_data is not False:
                            result = check().extension_ut_metadata(torrent_data, info_hash)
                            if result is True:
                                self.driver_control_extension_ut_metadata_messages_send.put(
                                    [torrent_data, application_extension_ut_metadata_keyword]
                                )
                            else:
                                self.driver_control_extension_ut_metadata_messages_send.put(
                                    [False, application_extension_ut_metadata_keyword]
                                )
                        else:
                            self.driver_control_extension_ut_metadata_messages_send.put(
                                [False, application_extension_ut_metadata_keyword]
                            )
                    else:
                        socket_server.close()
                        self.driver_control_extension_ut_metadata_messages_send.put(
                            [False, application_extension_ut_metadata_keyword]
                        )
                else:
                    socket_server.close()
                    self.driver_control_extension_ut_metadata_messages_send.put(
                        [False, application_extension_ut_metadata_keyword]
                    )
            else:
                socket_server.close()
                self.driver_control_extension_ut_metadata_messages_send.put(
                    [False, application_extension_ut_metadata_keyword]
                )
        else:
            socket_server.close()
            self.driver_control_extension_ut_metadata_messages_send.put(
                [False, application_extension_ut_metadata_keyword]
            )

    def start(self):
        explorer_peer_wire_v6_driver_control_extension_ut_metadata_recvfrom_thread = threading.Thread(target = self.__extension_ut_metadata_recvfrom)
        explorer_peer_wire_v6_driver_control_extension_ut_metadata_recvfrom_thread.setDaemon(True)
        explorer_peer_wire_v6_driver_control_extension_ut_metadata_recvfrom_thread.start()