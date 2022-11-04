from ..driver.control import control
import os
import queue
import threading

class extension_ut_metadata:
    application_extension_ut_metadata_messages_key = []
    application_extension_ut_metadata_messages_operators = queue.Queue()
    application_extension_ut_metadata_messages_recvfrom = queue.Queue()
    application_extension_ut_metadata_messages_send = queue.Queue()

    def __operators(self):
        while True:
            application_extension_ut_metadata_messages_operators = self.application_extension_ut_metadata_messages_operators.get()
            operate = application_extension_ut_metadata_messages_operators[0]
            element = application_extension_ut_metadata_messages_operators[1]
            if operate == 'append':
                if element not in self.application_extension_ut_metadata_messages_key:
                    self.application_extension_ut_metadata_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_extension_ut_metadata_messages_key:
                    self.application_extension_ut_metadata_messages_key.remove(element)

    def __recvfrom(self):
        while True:
            application_extension_ut_metadata_messages_recvfrom = self.application_extension_ut_metadata_messages_recvfrom.get()
            info_hash = application_extension_ut_metadata_messages_recvfrom[0]
            ip_address = application_extension_ut_metadata_messages_recvfrom[1]
            tcp_port = application_extension_ut_metadata_messages_recvfrom[2]
            application_extension_ut_metadata_keyword = os.urandom(20).hex()
            control.driver_control_extension_ut_metadata_messages_recvfrom.put(
                [info_hash, ip_address, tcp_port, application_extension_ut_metadata_keyword]
            )
            self.application_extension_ut_metadata_messages_operators.put(
                ['append', [application_extension_ut_metadata_keyword, info_hash, ip_address, tcp_port]]
            )

    def __send(self):
        while True:
            driver_control_extension_ut_metadata_messages_send = control.driver_control_extension_ut_metadata_messages_send.get()
            result = driver_control_extension_ut_metadata_messages_send[0]
            application_extension_ut_metadata_keyword = driver_control_extension_ut_metadata_messages_send[1]
            for i in self.application_extension_ut_metadata_messages_key:
                if i[0] == application_extension_ut_metadata_keyword:
                    info_hash = i[1]
                    ip_address = i[2]
                    tcp_port = i[3]
                    self.application_extension_ut_metadata_messages_send.put(
                        {
                            'result': result,
                            'header': {
                                'info_hash': info_hash,
                                'ip_address': ip_address,
                                'tcp_port': tcp_port
                            }
                        }
                    )
                    self.application_extension_ut_metadata_messages_operators.put(
                        ['remove', i]
                    )

    def start(self):
        explorer_peer_wire_v6_application_extension_ut_metadata_operators_thread = threading.Thread(target = self.__operators)
        explorer_peer_wire_v6_application_extension_ut_metadata_operators_thread.setDaemon(True)
        explorer_peer_wire_v6_application_extension_ut_metadata_operators_thread.start()
        explorer_peer_wire_v6_application_extension_ut_metadata_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_peer_wire_v6_application_extension_ut_metadata_recvfrom_thread.setDaemon(True)
        explorer_peer_wire_v6_application_extension_ut_metadata_recvfrom_thread.start()
        explorer_peer_wire_v6_application_extension_ut_metadata_send_thread = threading.Thread(target = self.__send)
        explorer_peer_wire_v6_application_extension_ut_metadata_send_thread.setDaemon(True)
        explorer_peer_wire_v6_application_extension_ut_metadata_send_thread.start()