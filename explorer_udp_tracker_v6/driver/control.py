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
            ip_address = driver_control_announce_completed_messages_recvfrom[0]
            udp_port = driver_control_announce_completed_messages_recvfrom[1]
            info_hash = driver_control_announce_completed_messages_recvfrom[2]
            downloaded = driver_control_announce_completed_messages_recvfrom[3]
            left = driver_control_announce_completed_messages_recvfrom[4]
            uploaded = driver_control_announce_completed_messages_recvfrom[5]
            tcp_port = driver_control_announce_completed_messages_recvfrom[6]
            application_http_tracker_announce_completed_keyword = driver_control_announce_completed_messages_recvfrom[7]
            explorer_udp_tracker_v6_driver_control_announce_completed_send_thread = threading.Thread(target = self.__announce_completed_send, args = (ip_address, udp_port, info_hash, uploaded, downloaded, left, tcp_port, application_http_tracker_announce_completed_keyword,))
            explorer_udp_tracker_v6_driver_control_announce_completed_send_thread.setDaemon(True)
            explorer_udp_tracker_v6_driver_control_announce_completed_send_thread.start()

    def __announce_completed_send(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_completed_keyword):
        result = announce().completed(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_completed_messages_send.put(
            [result, application_http_tracker_announce_completed_keyword]
        )
        locals().clear()

    def __announce_none_recvfrom(self):
        while True:
            driver_control_announce_none_messages_recvfrom = self.driver_control_announce_none_messages_recvfrom.get()
            ip_address = driver_control_announce_none_messages_recvfrom[0]
            udp_port = driver_control_announce_none_messages_recvfrom[1]
            info_hash = driver_control_announce_none_messages_recvfrom[2]
            downloaded = driver_control_announce_none_messages_recvfrom[3]
            left = driver_control_announce_none_messages_recvfrom[4]
            uploaded = driver_control_announce_none_messages_recvfrom[5]
            tcp_port = driver_control_announce_none_messages_recvfrom[6]
            application_http_tracker_announce_none_keyword = driver_control_announce_none_messages_recvfrom[7]
            explorer_udp_tracker_v6_driver_control_announce_none_send_thread = threading.Thread(target = self.__announce_none_send, args = (ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_none_keyword,))
            explorer_udp_tracker_v6_driver_control_announce_none_send_thread.setDaemon(True)
            explorer_udp_tracker_v6_driver_control_announce_none_send_thread.start()

    def __announce_none_send(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_none_keyword):
        result = announce().none(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_none_messages_send.put(
            [result, application_http_tracker_announce_none_keyword]
        )
        locals().clear()

    def __announce_started_recvfrom(self):
        while True:
            driver_control_announce_started_messages_recvfrom = self.driver_control_announce_started_messages_recvfrom.get()
            ip_address = driver_control_announce_started_messages_recvfrom[0]
            udp_port = driver_control_announce_started_messages_recvfrom[1]
            info_hash = driver_control_announce_started_messages_recvfrom[2]
            downloaded = driver_control_announce_started_messages_recvfrom[3]
            left = driver_control_announce_started_messages_recvfrom[4]
            uploaded = driver_control_announce_started_messages_recvfrom[5]
            tcp_port = driver_control_announce_started_messages_recvfrom[6]
            application_http_tracker_announce_started_keyword = driver_control_announce_started_messages_recvfrom[7]
            explorer_udp_tracker_v6_driver_control_announce_started_send_thread = threading.Thread(target = self.__announce_started_send, args = (ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_started_keyword,))
            explorer_udp_tracker_v6_driver_control_announce_started_send_thread.setDaemon(True)
            explorer_udp_tracker_v6_driver_control_announce_started_send_thread.start()

    def __announce_started_send(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_started_keyword):
        result = announce().started(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_started_messages_send.put(
            [result, application_http_tracker_announce_started_keyword]
        )
        locals().clear()

    def __announce_stopped_recvfrom(self):
        while True:
            driver_control_announce_stopped_messages_recvfrom = self.driver_control_announce_stopped_messages_recvfrom.get()
            ip_address = driver_control_announce_stopped_messages_recvfrom[0]
            udp_port = driver_control_announce_stopped_messages_recvfrom[1]
            info_hash = driver_control_announce_stopped_messages_recvfrom[2]
            downloaded = driver_control_announce_stopped_messages_recvfrom[3]
            left = driver_control_announce_stopped_messages_recvfrom[4]
            uploaded = driver_control_announce_stopped_messages_recvfrom[5]
            tcp_port = driver_control_announce_stopped_messages_recvfrom[6]
            application_http_tracker_announce_stopped_keyword = driver_control_announce_stopped_messages_recvfrom[7]
            explorer_udp_tracker_v6_driver_control_announce_stopped_send_thread = threading.Thread(target = self.__announce_stopped_send, args = (ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_stopped_keyword,))
            explorer_udp_tracker_v6_driver_control_announce_stopped_send_thread.setDaemon(True)
            explorer_udp_tracker_v6_driver_control_announce_stopped_send_thread.start()

    def __announce_stopped_send(self, ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port, application_http_tracker_announce_stopped_keyword):
        result = announce().stopped(ip_address, udp_port, info_hash, downloaded, left, uploaded, tcp_port)
        self.driver_control_announce_stopped_messages_send.put(
            [result, application_http_tracker_announce_stopped_keyword]
        )
        locals().clear()

    def __scrape_recvfrom(self):
        while True:
            driver_control_scrape_messages_recvfrom = self.driver_control_scrape_messages_recvfrom.get()
            ip_address = driver_control_scrape_messages_recvfrom[0]
            udp_port = driver_control_scrape_messages_recvfrom[1]
            info_hash = driver_control_scrape_messages_recvfrom[2]
            application_http_tracker_scrape_keyword = driver_control_scrape_messages_recvfrom[3]
            explorer_udp_tracker_v6_driver_control_scrape_send_thread = threading.Thread(target = self.__scrape_send, args = (ip_address, udp_port, info_hash, application_http_tracker_scrape_keyword))
            explorer_udp_tracker_v6_driver_control_scrape_send_thread.setDaemon(True)
            explorer_udp_tracker_v6_driver_control_scrape_send_thread.start()

    def __scrape_send(self, ip_address, udp_port, info_hash, application_http_tracker_scrape_keyword):
        result = scrape().scrape(ip_address, udp_port, info_hash)
        self.driver_control_scrape_messages_send.put(
            [result, application_http_tracker_scrape_keyword]
        )
        locals().clear()

    def start(self):
        explorer_udp_tracker_v6_driver_control_announce_completed_recvfrom_thread = threading.Thread(target = self.__announce_completed_recvfrom)
        explorer_udp_tracker_v6_driver_control_announce_completed_recvfrom_thread.setDaemon(True)
        explorer_udp_tracker_v6_driver_control_announce_completed_recvfrom_thread.start()
        explorer_udp_tracker_v6_driver_control_announce_none_recvfrom_thread = threading.Thread(target = self.__announce_none_recvfrom)
        explorer_udp_tracker_v6_driver_control_announce_none_recvfrom_thread.setDaemon(True)
        explorer_udp_tracker_v6_driver_control_announce_none_recvfrom_thread.start()
        explorer_udp_tracker_v6_driver_control_announce_started_recvfrom_thread = threading.Thread(target = self.__announce_started_recvfrom)
        explorer_udp_tracker_v6_driver_control_announce_started_recvfrom_thread.setDaemon(True)
        explorer_udp_tracker_v6_driver_control_announce_started_recvfrom_thread.start()
        explorer_udp_tracker_v6_driver_control_announce_stopped_recvfrom_thread = threading.Thread(target = self.__announce_stopped_recvfrom)
        explorer_udp_tracker_v6_driver_control_announce_stopped_recvfrom_thread.setDaemon(True)
        explorer_udp_tracker_v6_driver_control_announce_stopped_recvfrom_thread.start()
        explorer_udp_tracker_v6_driver_control_scrape_recvfrom_thread = threading.Thread(target = self.__scrape_recvfrom)
        explorer_udp_tracker_v6_driver_control_scrape_recvfrom_thread.setDaemon(True)
        explorer_udp_tracker_v6_driver_control_scrape_recvfrom_thread.start()