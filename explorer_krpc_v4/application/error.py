from ..database.distributed_hash_table import distributed_hash_table
from ..driver.control import control
import IPy
import threading

class error:
    def __recvfrom(self):
        while True:
            driver_control_error_messages = control().driver_control_error_messages.get()
            ip_address = driver_control_error_messages[3]
            udp_port = driver_control_error_messages[4]
            ip_address_type = IPy.IP(ip_address).iptype()
            if ip_address_type == 'PUBLIC':
                distributed_hash_table.database_delete_node_messages.put(
                    [ip_address, udp_port]
                )

    def start(self):
        explorer_krpc_v4_application_error_recvfrom_thread = threading.Thread(target = self.__recvfrom)
        explorer_krpc_v4_application_error_recvfrom_thread.setDaemon(True)
        explorer_krpc_v4_application_error_recvfrom_thread.start()