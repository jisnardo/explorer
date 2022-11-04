from ..driver.control import control
import os
import queue
import threading

class http_tracker_announce_stopped:
    application_http_tracker_announce_stopped_messages_key = []
    application_http_tracker_announce_stopped_messages_operators = queue.Queue()
    application_http_tracker_announce_stopped_messages_recvfrom = queue.Queue()
    application_http_tracker_announce_stopped_messages_send = queue.Queue()

    def __operators(self):
        while True:
            application_http_tracker_announce_stopped_messages_operators = self.application_http_tracker_announce_stopped_messages_operators.get()
            operate = application_http_tracker_announce_stopped_messages_operators[0]
            element = application_http_tracker_announce_stopped_messages_operators[1]
            if operate == 'append':
                if element not in self.application_http_tracker_announce_stopped_messages_key:
                    self.application_http_tracker_announce_stopped_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_http_tracker_announce_stopped_messages_key:
                    self.application_http_tracker_announce_stopped_messages_key.remove(element)

    def __recvfrom(self):
        while True:
            application_http_tracker_announce_stopped_messages_recvfrom = self.application_http_tracker_announce_stopped_messages_recvfrom.get()
            domain_url = application_http_tracker_announce_stopped_messages_recvfrom[0]
            info_hash = application_http_tracker_announce_stopped_messages_recvfrom[1]
            downloaded = application_http_tracker_announce_stopped_messages_recvfrom[2]
            left = application_http_tracker_announce_stopped_messages_recvfrom[3]
            uploaded = application_http_tracker_announce_stopped_messages_recvfrom[4]
            tcp_port = application_http_tracker_announce_stopped_messages_recvfrom[5]
            application_http_tracker_announce_stopped_keyword = os.urandom(20).hex()
            control.driver_control_announce_stopped_messages_recvfrom.put(
                [domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_stopped_keyword]
            )
            self.application_http_tracker_announce_stopped_messages_operators.put(
                ['append', [application_http_tracker_announce_stopped_keyword, domain_url, info_hash, downloaded, left, uploaded, tcp_port]]
            )

    def __send(self):
        while True:
            driver_control_announce_stopped_messages_send = control.driver_control_announce_stopped_messages_send.get()
            result = driver_control_announce_stopped_messages_send[0]
            application_http_tracker_announce_stopped_keyword = driver_control_announce_stopped_messages_send[1]
            for i in self.application_http_tracker_announce_stopped_messages_key:
                if i[0] == application_http_tracker_announce_stopped_keyword:
                    domain_url = i[1]
                    info_hash = i[2]
                    downloaded = i[3]
                    left = i[4]
                    uploaded = i[5]
                    tcp_port = i[6]
                    self.application_http_tracker_announce_stopped_messages_send.put({
                        'result': result,
                        'header': {
                            'domain_url': domain_url,
                            'info_hash': info_hash,
                            'downloaded': downloaded,
                            'left': left,
                            'uploaded': uploaded,
                            'tcp_port': tcp_port
                        }
                    })
                    self.application_http_tracker_announce_stopped_messages_operators.put(
                        ['remove', i]
                    )

    def start(self):
        explorer_http_tracker_application_http_tracker_announce_stopped_operators_thread = threading.Thread(target = self.__operators)
        explorer_http_tracker_application_http_tracker_announce_stopped_operators_thread.setDaemon(True)
        explorer_http_tracker_application_http_tracker_announce_stopped_operators_thread.start()
        explorer_http_tracker_application_http_tracker_announce_stopped_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_http_tracker_application_http_tracker_announce_stopped_recvfrom_thread.setDaemon(True)
        explorer_http_tracker_application_http_tracker_announce_stopped_recvfrom_thread.start()
        explorer_http_tracker_application_http_tracker_announce_stopped_send_thread = threading.Thread(target = self.__send)
        explorer_http_tracker_application_http_tracker_announce_stopped_send_thread.setDaemon(True)
        explorer_http_tracker_application_http_tracker_announce_stopped_send_thread.start()