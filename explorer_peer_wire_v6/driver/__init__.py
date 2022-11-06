from ..driver.control import control
from ..driver.memory import memory
from ..driver.transmitter import transmission
import random

class driver_loader:
    def __get_self_peer_id(self):
        peer_id_prefix = '-EP0361-'
        number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        small_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        big_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        special_characters = ['~', '!', '@', '#', '$', '%', '^', '&', '*']
        random_string = ''
        for i in range(3):
            random_string = random_string + random.choice(number)
            random_string = random_string + random.choice(small_letter)
            random_string = random_string + random.choice(big_letter)
            random_string = random_string + random.choice(special_characters)
        peer_id = bytes(peer_id_prefix + random_string, encoding = 'utf-8').hex()
        return peer_id

    def launch(self):
        memory.peer_id = self.__get_self_peer_id()
        control().start()
        transmission().start()