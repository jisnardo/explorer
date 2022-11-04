from .memory import memory
import multiping
import threading
import time

class ping:
    def __listen(self):
        while True:
            ping_ip_address = [
                '8.8.8.8',
                '8.8.4.4',
                '2001:4860:4860::8888',
                '2001:4860:4860::8844'
            ]
            ping_event = multiping.MultiPing(ping_ip_address)
            ping_event.send()
            responses, no_responses = ping_event.receive(2)
            for i in responses.keys():
                if i == '8.8.8.8':
                    memory.ipv4_network_connectivity = True
                if i == '8.8.4.4':
                    memory.ipv4_network_connectivity = True
                if i == '2001:4860:4860::8888':
                    memory.ipv6_network_connectivity = True
                if i == '2001:4860:4860::8844':
                    memory.ipv6_network_connectivity = True
            time.sleep(600)

    def start(self):
        explorer_spider_ping_listen_thread = threading.Thread(target = self.__listen)
        explorer_spider_ping_listen_thread.setDaemon(True)
        explorer_spider_ping_listen_thread.start()