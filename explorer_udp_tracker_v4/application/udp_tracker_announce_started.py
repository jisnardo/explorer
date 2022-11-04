from ..driver.control import control
import os
import queue
import threading

class udp_tracker_announce_started:
    application_udp_tracker_announce_started_messages_key = []
    application_udp_tracker_announce_started_messages_operators = queue.Queue()
    application_udp_tracker_announce_started_messages_recvfrom = queue.Queue()
    application_udp_tracker_announce_started_messages_send = queue.Queue()

    def __operators(self):
        while True:
            application_udp_tracker_announce_started_messages_operators = self.application_udp_tracker_announce_started_messages_operators.get()
            operate = application_udp_tracker_announce_started_messages_operators[0]
            element = application_udp_tracker_announce_started_messages_operators[1]
            if operate == 'append':
                if element not in self.application_udp_tracker_announce_started_messages_key:
                    self.application_udp_tracker_announce_started_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_udp_tracker_announce_started_messages_key:
                    self.application_udp_tracker_announce_started_messages_key.remove(element)

    def __recvfrom(self):
        while True:
            application_udp_tracker_announce_started_messages_recvfrom = self.application_udp_tracker_announce_started_messages_recvfrom.get()
            ip_address = application_udp_tracker_announce_started_messages_recvfrom[0]
            udp_port = application_udp_tracker_announce_started_messages_recvfrom[1]
            info_hash = application_udp_tracker_announce_started_messages_recvfrom[2]
            downloaded = application_udp_tracker_announce_started_messages_recvfrom[3]
            left = application_udp_tracker_announce_started_messages_recvfrom[4]
            uploaded = application_udp_tracker_announce_started_messages_recvfrom[5]
            tcp_port = application_udp_tracker_announce_started_messages_recvfrom[6]
            application_udp_tracker_announce_started_keyword = os.urandom(20).hex()
            control.driver_control_announce_started_messages_recvfrom.put(
                [ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_udp_tracker_announce_started_keyword]
            )
            self.application_udp_tracker_announce_started_messages_operators.put(
                ['append', [application_udp_tracker_announce_started_keyword, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port]]
            )

    def __send(self):
        while True:
            driver_control_announce_started_messages_send = control.driver_control_announce_started_messages_send.get()
            result = driver_control_announce_started_messages_send[0]
            application_udp_tracker_announce_started_keyword = driver_control_announce_started_messages_send[1]
            for i in self.application_udp_tracker_announce_started_messages_key:
                if i[0] == application_udp_tracker_announce_started_keyword:
                    ip_address = i[1]
                    udp_port = i[2]
                    info_hash = i[3]
                    downloaded = i[4]
                    left = i[5]
                    uploaded = i[6]
                    tcp_port = i[7]
                    self.application_udp_tracker_announce_started_messages_send.put({
                        'result': result,
                        'header': {
                            'ip_address': ip_address,
                            'udp_port': udp_port,
                            'info_hash': info_hash,
                            'downloaded': downloaded,
                            'left': left,
                            'uploaded': uploaded,
                            'tcp_port': tcp_port
                        }
                    })
                    self.application_udp_tracker_announce_started_messages_operators.put(
                        ['remove', i]
                    )

    def start(self):
        explorer_udp_tracker_application_udp_tracker_announce_started_operators_thread = threading.Thread(target = self.__operators)
        explorer_udp_tracker_application_udp_tracker_announce_started_operators_thread.setDaemon(True)
        explorer_udp_tracker_application_udp_tracker_announce_started_operators_thread.start()
        explorer_udp_tracker_application_udp_tracker_announce_started_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_udp_tracker_application_udp_tracker_announce_started_recvfrom_thread.setDaemon(True)
        explorer_udp_tracker_application_udp_tracker_announce_started_recvfrom_thread.start()
        explorer_udp_tracker_application_udp_tracker_announce_started_send_thread = threading.Thread(target = self.__send)
        explorer_udp_tracker_application_udp_tracker_announce_started_send_thread.setDaemon(True)
        explorer_udp_tracker_application_udp_tracker_announce_started_send_thread.start()