from ..application.bootstrap_nodes import bootstrap_nodes
from ..database.distributed_hash_table import distributed_hash_table
from ..driver.memory import memory
import faker
import IPy
import multiping
import random
import threading
import time

class discovery_nodes:
    application_discovery_nodes_udp_port_list = [6881, 51413]

    def __append_bootstrap_nodes(self):
        time.sleep(300)
        while True:
            distributed_hash_table.database_query_nodes_number_messages_recvfrom.put(
                0
            )
            nodes_number = distributed_hash_table.database_query_nodes_number_messages_send.get()
            if nodes_number == 0:
                if IPy.IP(memory.ip_address).iptype() == 'PUBLIC':
                    ping_ip_address = [
                        '8.8.8.8'
                    ]
                    ping_event = multiping.MultiPing(ping_ip_address)
                    ping_event.send()
                    responses, no_responses = ping_event.receive(2)
                    for i in responses.keys():
                        if i == '8.8.8.8':
                            for j in range(0, 25):
                                nodes_ip_address = faker.Faker().ipv4(network = False, address_class = None, private = False)
                                nodes_udp_port = random.choice(self.application_discovery_nodes_udp_port_list)
                                bootstrap_nodes.application_bootstrap_nodes.append([nodes_ip_address, nodes_udp_port])
            time.sleep(600)

    def start(self):
        explorer_krpc_v4_application_discovery_nodes_append_bootstrap_nodes_thread = threading.Thread(target = self.__append_bootstrap_nodes)
        explorer_krpc_v4_application_discovery_nodes_append_bootstrap_nodes_thread.setDaemon(True)
        explorer_krpc_v4_application_discovery_nodes_append_bootstrap_nodes_thread.start()