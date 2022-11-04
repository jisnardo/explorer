import pyben
import queue
import socket
import threading

class krpc_server:
    driver_interface_recvfrom_messages = queue.Queue()
    driver_interface_send_messages = queue.Queue()
    driver_interface_socket_server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def __recvfrom(self):
        while True:
            try:
                (message, server_address) = self.driver_interface_socket_server.recvfrom(65536)
                self.driver_interface_recvfrom_messages.put(
                    [pyben.loads(message), server_address]
                )
            except:
                pass

    def __send(self):
        while True:
            try:
                driver_interface_send_messages = self.driver_interface_send_messages.get()
                message = driver_interface_send_messages[0]
                ip_address = driver_interface_send_messages[1]
                udp_port = driver_interface_send_messages[2]
                self.driver_interface_socket_server.sendto(pyben.dumps(message), (ip_address, udp_port))
            except:
                pass

    def bind(self, ip_address, udp_port):
        self.driver_interface_socket_server.bind((ip_address, udp_port))
        explorer_krpc_v6_driver_interface_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v6_driver_interface_recvfrom_thread.setDaemon(True)
        explorer_krpc_v6_driver_interface_recvfrom_thread.start()
        explorer_krpc_v6_driver_interface_send_thread = threading.Thread(target = self.__send)
        explorer_krpc_v6_driver_interface_send_thread.setDaemon(True)
        explorer_krpc_v6_driver_interface_send_thread.start()