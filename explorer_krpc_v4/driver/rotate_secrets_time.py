from ..driver.memory import memory
import binascii
import crc32c
import faker
import getuseragent
import httpx
import IPy
import os
import random
import socket
import threading
import time

class rotate_secrets_time:
    def __get_self_lan_ip_address(self):
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_server.connect(('8.8.8.8', 80))
            ip_address = socket_server.getsockname()[0]
        except:
            ip_address = faker.Faker().ipv4(network = False, address_class = None, private = True)
        finally:
            socket_server.close()
            return ip_address

    def __get_self_node_id(self):
        time.sleep(14400)
        while True:
            lan_ip_address = self.__get_self_lan_ip_address()
            ip_address_type = IPy.IP(lan_ip_address).iptype()
            if ip_address_type == 'PUBLIC':
                memory.ip_address = lan_ip_address
            else:
                wan_ip_address = self.__get_self_wan_ip_address()
                if wan_ip_address == '':
                    memory.ip_address = lan_ip_address
                else:
                    memory.ip_address = wan_ip_address
            ip_address = memory.ip_address
            ip_address_type = IPy.IP(ip_address).iptype()
            if ip_address_type == 'PUBLIC':
                rand = random.randint(0, 255) & 0xff
                r = rand & 0x7
                network_byte_order_ip_address = socket.inet_pton(socket.AF_INET, ip_address)
                hexadecimal_ip_address = binascii.hexlify(network_byte_order_ip_address)
                decimal_ip_address = int(hexadecimal_ip_address, 16)
                binary_ip_address = bin(decimal_ip_address)
                decimal_ip_address = int(binary_ip_address, 2)
                decimal_number = (decimal_ip_address & 0x030f3fff) | (r << 29)
                hexadecimal_number = hex(decimal_number).replace('0x', '').encode('ascii')
                if (len(hexadecimal_number) % 2) == 0:
                    network_byte_order_number = binascii.unhexlify(hexadecimal_number)
                    crc = crc32c.crc32c(network_byte_order_number)
                    node_id = ''
                    node_id = node_id + hex((crc >> 24) & 0xff).replace('0x', '').zfill(2)
                    node_id = node_id + hex((crc >> 16) & 0xff).replace('0x', '').zfill(2)
                    node_id = node_id + hex(((crc >> 8) & 0xf8) | (random.randint(0, 255) & 0x7)).replace('0x', '').zfill(2)
                    for i in range(0, 16):
                        node_id = node_id + hex(random.randint(0, 255)).replace('0x', '').zfill(2)
                    node_id = node_id + hex(rand).replace('0x', '').zfill(2)
                    memory.node_id = node_id
                    time.sleep(14400)
            else:
                memory.node_id = os.urandom(20).hex()
                time.sleep(14400)

    def __get_self_token(self):
        time.sleep(900)
        while True:
            memory.token = os.urandom(4)
            time.sleep(900)

    def __get_self_wan_ip_address(self):
        ip_address = ''
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = 'https://ipv4.jsonip.com'
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    data = response.json()
                    ip_address = data['ip']
            except httpx.HTTPError:
                pass
            except Exception:
                pass
            finally:
                locals().clear()
        return ip_address

    def start(self):
        explorer_krpc_v4_driver_rotate_secrets_time_get_self_node_id_thread = threading.Thread(target = self.__get_self_node_id)
        explorer_krpc_v4_driver_rotate_secrets_time_get_self_node_id_thread.setDaemon(True)
        explorer_krpc_v4_driver_rotate_secrets_time_get_self_node_id_thread.start()
        explorer_krpc_v4_driver_rotate_secrets_time_get_self_token_thread = threading.Thread(target = self.__get_self_token)
        explorer_krpc_v4_driver_rotate_secrets_time_get_self_token_thread.setDaemon(True)
        explorer_krpc_v4_driver_rotate_secrets_time_get_self_token_thread.start()