from ..driver.control import control
import os
import queue
import threading

class http_tracker_scrape:
    application_http_tracker_scrape_messages_key = []
    application_http_tracker_scrape_messages_operators = queue.Queue()
    application_http_tracker_scrape_messages_recvfrom = queue.Queue()
    application_http_tracker_scrape_messages_send = queue.Queue()

    def __operators(self):
        while True:
            application_http_tracker_scrape_messages_operators = self.application_http_tracker_scrape_messages_operators.get()
            operate = application_http_tracker_scrape_messages_operators[0]
            element = application_http_tracker_scrape_messages_operators[1]
            if operate == 'append':
                if element not in self.application_http_tracker_scrape_messages_key:
                    self.application_http_tracker_scrape_messages_key.append(element)
            if operate == 'remove':
                if element in self.application_http_tracker_scrape_messages_key:
                    self.application_http_tracker_scrape_messages_key.remove(element)

    def __recvfrom(self):
        while True:
            application_http_tracker_scrape_messages_recvfrom = self.application_http_tracker_scrape_messages_recvfrom.get()
            domain_url = application_http_tracker_scrape_messages_recvfrom[0]
            info_hash = application_http_tracker_scrape_messages_recvfrom[1]
            application_http_tracker_scrape_keyword = os.urandom(20).hex()
            control.driver_control_scrape_messages_recvfrom.put(
                [domain_url, info_hash, application_http_tracker_scrape_keyword]
            )
            self.application_http_tracker_scrape_messages_operators.put(
                ['append', [application_http_tracker_scrape_keyword, domain_url, info_hash]]
            )

    def __send(self):
        while True:
            driver_control_scrape_messages_send = control.driver_control_scrape_messages_send.get()
            result = driver_control_scrape_messages_send[0]
            application_http_tracker_scrape_keyword = driver_control_scrape_messages_send[1]
            for i in self.application_http_tracker_scrape_messages_key:
                if i[0] == application_http_tracker_scrape_keyword:
                    domain_url = i[1]
                    info_hash = i[2]
                    self.application_http_tracker_scrape_messages_send.put({
                        'result': result,
                        'header': {
                            'domain_url': domain_url,
                            'info_hash': info_hash
                        }
                    })
                    self.application_http_tracker_scrape_messages_operators.put(
                        ['remove', i]
                    )

    def start(self):
        explorer_http_tracker_application_http_tracker_scrape_operators_thread = threading.Thread(target = self.__operators)
        explorer_http_tracker_application_http_tracker_scrape_operators_thread.setDaemon(True)
        explorer_http_tracker_application_http_tracker_scrape_operators_thread.start()
        explorer_http_tracker_application_http_tracker_scrape_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_http_tracker_application_http_tracker_scrape_recvfrom_thread.setDaemon(True)
        explorer_http_tracker_application_http_tracker_scrape_recvfrom_thread.start()
        explorer_http_tracker_application_http_tracker_scrape_send_thread = threading.Thread(target = self.__send)
        explorer_http_tracker_application_http_tracker_scrape_send_thread.setDaemon(True)
        explorer_http_tracker_application_http_tracker_scrape_send_thread.start()