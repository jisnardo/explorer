from ..driver.control import control
import os
import queue
import threading

class udp_tracker_scrape:
    application_udp_tracker_scrape_messages_key = []
    application_udp_tracker_scrape_messages_operators = queue.Queue()
    application_udp_tracker_scrape_messages_recvfrom = queue.Queue()
    application_udp_tracker_scrape_messages_send = queue.Queue()

    def __operators(self):
        while True:
            application_udp_tracker_scrape_messages_operators = self.application_udp_tracker_scrape_messages_operators.get()
            operate = application_udp_tracker_scrape_messages_operators[0]
            element = application_udp_tracker_scrape_messages_operators[1]
            if operate == 'append':
                if element not in self.application_udp_tracker_scrape_messages_key:
                    self.application_udp_tracker_scrape_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_udp_tracker_scrape_messages_key:
                    self.application_udp_tracker_scrape_messages_key.remove(element)

    def __recvfrom(self):
        while True:
            application_udp_tracker_scrape_messages_recvfrom = self.application_udp_tracker_scrape_messages_recvfrom.get()
            ip_address = application_udp_tracker_scrape_messages_recvfrom[0]
            udp_port = application_udp_tracker_scrape_messages_recvfrom[1]
            info_hash = application_udp_tracker_scrape_messages_recvfrom[2]
            application_udp_tracker_scrape_keyword = os.urandom(20).hex()
            control.driver_control_scrape_messages_recvfrom.put(
                [ip_address, udp_port, info_hash, application_udp_tracker_scrape_keyword]
            )
            self.application_udp_tracker_scrape_messages_operators.put(
                ['append', [application_udp_tracker_scrape_keyword, ip_address, udp_port, info_hash]]
            )

    def __send(self):
        while True:
            driver_control_scrape_messages_send = control.driver_control_scrape_messages_send.get()
            result = driver_control_scrape_messages_send[0]
            application_udp_tracker_scrape_keyword = driver_control_scrape_messages_send[1]
            for i in self.application_udp_tracker_scrape_messages_key:
                if i[0] == application_udp_tracker_scrape_keyword:
                    ip_address = i[1]
                    udp_port = i[2]
                    info_hash = i[3]
                    self.application_udp_tracker_scrape_messages_send.put({
                        'result': result,
                        'header': {
                            'ip_address': ip_address,
                            'udp_port': udp_port,
                            'info_hash': info_hash
                        }
                    })
                    self.application_udp_tracker_scrape_messages_operators.put(
                        ['remove', i]
                    )

    def start(self):
        explorer_udp_tracker_v6_application_udp_tracker_scrape_operators_thread = threading.Thread(target = self.__operators)
        explorer_udp_tracker_v6_application_udp_tracker_scrape_operators_thread.setDaemon(True)
        explorer_udp_tracker_v6_application_udp_tracker_scrape_operators_thread.start()
        explorer_udp_tracker_v6_application_udp_tracker_scrape_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_udp_tracker_v6_application_udp_tracker_scrape_recvfrom_thread.setDaemon(True)
        explorer_udp_tracker_v6_application_udp_tracker_scrape_recvfrom_thread.start()
        explorer_udp_tracker_v6_application_udp_tracker_scrape_send_thread = threading.Thread(target = self.__send)
        explorer_udp_tracker_v6_application_udp_tracker_scrape_send_thread.setDaemon(True)
        explorer_udp_tracker_v6_application_udp_tracker_scrape_send_thread.start()