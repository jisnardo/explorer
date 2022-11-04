from ..application.bootstrap_nodes import bootstrap_nodes
from ..application.client import client
from ..application.command import application_command_loader
from ..application.discovery_nodes import discovery_nodes
from ..application.error import error
from ..application.neighbor_nodes import neighbor_nodes
from ..application.server import server
import dns.resolver
import IPy
import os
import pyben
import socket
import struct
import threading

class application_loader:
    def __append_bootstrap_nodes_list_1(self):
        bootstrap_nodes_list = [
            ['dht.transmissionbt.com', 6881],
            ['router.utorrent.com', 6881],
            ['router.bittorrent.com', 6881],
            ['router.silotis.us', 6881],
            ['dht.aelitis.com', 6881],
            ['dht.filecxx.com', 10112],
            ['dht.libtorrent.org', 25401]
        ]
        for i in bootstrap_nodes_list:
            domain_name = i[0]
            udp_port = i[1]
            ip_address_list = self.__query_bootstrap_nodes_ip_address(domain_name)
            for j in ip_address_list:
                ip_address = j
                ip_address_type = IPy.IP(ip_address).iptype()
                if ip_address_type == 'PUBLIC':
                    bootstrap_nodes.application_bootstrap_nodes.append([ip_address, udp_port])

    def __append_bootstrap_nodes_list_2(self):
        if os.path.exists(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/database/dht.dat'):
            with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/database/dht.dat', mode = 'rb') as file:
                dht_file = file.read()
                dht_file_data = pyben.loads(dht_file)
                if 'nodes' in dht_file_data:
                    if type(dht_file_data.get('nodes')) == bytes:
                        for i in range(0, len(dht_file_data.get('nodes')), 6):
                            nodes_ip_address = socket.inet_ntop(socket.AF_INET, dht_file_data.get('nodes')[i:i + 4])
                            nodes_udp_port = struct.unpack_from('!H', dht_file_data.get('nodes')[i + 4:i + 6])[0]
                            ip_address_type = IPy.IP(nodes_ip_address).iptype()
                            if ip_address_type == 'PUBLIC':
                                bootstrap_nodes.application_bootstrap_nodes.append([nodes_ip_address, nodes_udp_port])

    def __query_bootstrap_nodes_ip_address(self, domain_name):
        ip_address_list = []
        try:
            for i in dns.resolver.query(domain_name, 'A').response.answer:
                for j in i.items:
                    if j.rdtype == 1:
                        ip_address_list.append(j.address)
            return ip_address_list
        except:
            return ip_address_list

    def launch(self):
        client().start()
        server().start()
        error().start()
        bootstrap_nodes().start()
        neighbor_nodes().start()
        discovery_nodes().start()
        application_command_loader().launch()
        explorer_krpc_v4_application_init_append_bootstrap_nodes_list_1_thread = threading.Thread(target = self.__append_bootstrap_nodes_list_1)
        explorer_krpc_v4_application_init_append_bootstrap_nodes_list_1_thread.setDaemon(True)
        explorer_krpc_v4_application_init_append_bootstrap_nodes_list_1_thread.start()
        explorer_krpc_v4_application_init_append_bootstrap_nodes_list_2_thread = threading.Thread(target = self.__append_bootstrap_nodes_list_2)
        explorer_krpc_v4_application_init_append_bootstrap_nodes_list_2_thread.setDaemon(True)
        explorer_krpc_v4_application_init_append_bootstrap_nodes_list_2_thread.start()