from ..driver.announce import announce
from ..driver.scrape import scrape
import queue
import threading

class control:
    driver_control_announce_completed_messages_recvfrom = queue.Queue()
    driver_control_announce_completed_messages_send = queue.Queue()
    driver_control_announce_none_messages_recvfrom = queue.Queue()
    driver_control_announce_none_messages_send = queue.Queue()
    driver_control_announce_started_messages_recvfrom = queue.Queue()
    driver_control_announce_started_messages_send = queue.Queue()
    driver_control_announce_stopped_messages_recvfrom = queue.Queue()
    driver_control_announce_stopped_messages_send = queue.Queue()
    driver_control_scrape_messages_recvfrom = queue.Queue()
    driver_control_scrape_messages_send = queue.Queue()

    def __announce_completed_recvfrom(self):
        while True:
            driver_control_announce_completed_messages_recvfrom = self.driver_control_announce_completed_messages_recvfrom.get()
            domain_url = driver_control_announce_completed_messages_recvfrom[0]
            info_hash = driver_control_announce_completed_messages_recvfrom[1]
            downloaded = driver_control_announce_completed_messages_recvfrom[2]
            left = driver_control_announce_completed_messages_recvfrom[3]
            uploaded = driver_control_announce_completed_messages_recvfrom[4]
            tcp_port = driver_control_announce_completed_messages_recvfrom[5]
            application_http_tracker_announce_completed_keyword = driver_control_announce_completed_messages_recvfrom[6]
            explorer_http_tracker_driver_control_announce_completed_send_thread = threading.Thread(target = self.__announce_completed_send, args = (domain_url, info_hash, uploaded, downloaded, left, tcp_port, application_http_tracker_announce_completed_keyword,))
            explorer_http_tracker_driver_control_announce_completed_send_thread.setDaemon(True)
            explorer_http_tracker_driver_control_announce_completed_send_thread.start()

    def __announce_completed_send(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_completed_keyword):
        result = announce().completed(domain_url, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_completed_messages_send.put(
            [result, application_http_tracker_announce_completed_keyword]
        )
        locals().clear()

    def __announce_none_recvfrom(self):
        while True:
            driver_control_announce_none_messages_recvfrom = self.driver_control_announce_none_messages_recvfrom.get()
            domain_url = driver_control_announce_none_messages_recvfrom[0]
            info_hash = driver_control_announce_none_messages_recvfrom[1]
            downloaded = driver_control_announce_none_messages_recvfrom[2]
            left = driver_control_announce_none_messages_recvfrom[3]
            uploaded = driver_control_announce_none_messages_recvfrom[4]
            tcp_port = driver_control_announce_none_messages_recvfrom[5]
            application_http_tracker_announce_none_keyword = driver_control_announce_none_messages_recvfrom[6]
            explorer_http_tracker_driver_control_announce_none_send_thread = threading.Thread(target = self.__announce_none_send, args = (domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_none_keyword,))
            explorer_http_tracker_driver_control_announce_none_send_thread.setDaemon(True)
            explorer_http_tracker_driver_control_announce_none_send_thread.start()

    def __announce_none_send(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_none_keyword):
        result = announce().none(domain_url, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_none_messages_send.put(
            [result, application_http_tracker_announce_none_keyword]
        )
        locals().clear()

    def __announce_started_recvfrom(self):
        while True:
            driver_control_announce_started_messages_recvfrom = self.driver_control_announce_started_messages_recvfrom.get()
            domain_url = driver_control_announce_started_messages_recvfrom[0]
            info_hash = driver_control_announce_started_messages_recvfrom[1]
            downloaded = driver_control_announce_started_messages_recvfrom[2]
            left = driver_control_announce_started_messages_recvfrom[3]
            uploaded = driver_control_announce_started_messages_recvfrom[4]
            tcp_port = driver_control_announce_started_messages_recvfrom[5]
            application_http_tracker_announce_started_keyword = driver_control_announce_started_messages_recvfrom[6]
            explorer_http_tracker_driver_control_announce_started_send_thread = threading.Thread(target = self.__announce_started_send, args = (domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_started_keyword,))
            explorer_http_tracker_driver_control_announce_started_send_thread.setDaemon(True)
            explorer_http_tracker_driver_control_announce_started_send_thread.start()

    def __announce_started_send(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_started_keyword):
        result = announce().started(domain_url, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_started_messages_send.put(
            [result, application_http_tracker_announce_started_keyword]
        )
        locals().clear()

    def __announce_stopped_recvfrom(self):
        while True:
            driver_control_announce_stopped_messages_recvfrom = self.driver_control_announce_stopped_messages_recvfrom.get()
            domain_url = driver_control_announce_stopped_messages_recvfrom[0]
            info_hash = driver_control_announce_stopped_messages_recvfrom[1]
            downloaded = driver_control_announce_stopped_messages_recvfrom[2]
            left = driver_control_announce_stopped_messages_recvfrom[3]
            uploaded = driver_control_announce_stopped_messages_recvfrom[4]
            tcp_port = driver_control_announce_stopped_messages_recvfrom[5]
            application_http_tracker_announce_stopped_keyword = driver_control_announce_stopped_messages_recvfrom[6]
            explorer_http_tracker_driver_control_announce_stopped_send_thread = threading.Thread(target = self.__announce_stopped_send, args = (domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_stopped_keyword,))
            explorer_http_tracker_driver_control_announce_stopped_send_thread.setDaemon(True)
            explorer_http_tracker_driver_control_announce_stopped_send_thread.start()

    def __announce_stopped_send(self, domain_url, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_stopped_keyword):
        result = announce().stopped(domain_url, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_stopped_messages_send.put(
            [result, application_http_tracker_announce_stopped_keyword]
        )
        locals().clear()

    def __scrape_recvfrom(self):
        while True:
            driver_control_scrape_messages_recvfrom = self.driver_control_scrape_messages_recvfrom.get()
            domain_url = driver_control_scrape_messages_recvfrom[0]
            info_hash = driver_control_scrape_messages_recvfrom[1]
            application_http_tracker_scrape_keyword = driver_control_scrape_messages_recvfrom[2]
            explorer_http_tracker_driver_control_scrape_send_thread = threading.Thread(target = self.__scrape_send, args = (domain_url, info_hash, application_http_tracker_scrape_keyword))
            explorer_http_tracker_driver_control_scrape_send_thread.setDaemon(True)
            explorer_http_tracker_driver_control_scrape_send_thread.start()

    def __scrape_send(self, domain_url, info_hash, application_http_tracker_scrape_keyword):
        result = scrape().scrape(domain_url, info_hash)
        self.driver_control_scrape_messages_send.put(
            [result, application_http_tracker_scrape_keyword]
        )
        locals().clear()

    def start(self):
        explorer_http_tracker_driver_control_announce_completed_recvfrom_thread = threading.Thread(target = self.__announce_completed_recvfrom)
        explorer_http_tracker_driver_control_announce_completed_recvfrom_thread.setDaemon(True)
        explorer_http_tracker_driver_control_announce_completed_recvfrom_thread.start()
        explorer_http_tracker_driver_control_announce_none_recvfrom_thread = threading.Thread(target = self.__announce_none_recvfrom)
        explorer_http_tracker_driver_control_announce_none_recvfrom_thread.setDaemon(True)
        explorer_http_tracker_driver_control_announce_none_recvfrom_thread.start()
        explorer_http_tracker_driver_control_announce_started_recvfrom_thread = threading.Thread(target = self.__announce_started_recvfrom)
        explorer_http_tracker_driver_control_announce_started_recvfrom_thread.setDaemon(True)
        explorer_http_tracker_driver_control_announce_started_recvfrom_thread.start()
        explorer_http_tracker_driver_control_announce_stopped_recvfrom_thread = threading.Thread(target = self.__announce_stopped_recvfrom)
        explorer_http_tracker_driver_control_announce_stopped_recvfrom_thread.setDaemon(True)
        explorer_http_tracker_driver_control_announce_stopped_recvfrom_thread.start()
        explorer_http_tracker_driver_control_scrape_recvfrom_thread = threading.Thread(target = self.__scrape_recvfrom)
        explorer_http_tracker_driver_control_scrape_recvfrom_thread.setDaemon(True)
        explorer_http_tracker_driver_control_scrape_recvfrom_thread.start()