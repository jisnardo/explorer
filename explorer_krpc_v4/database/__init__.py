from ..database.distributed_hash_table import distributed_hash_table
from ..database.find_node import find_node
from ..database.peer_database import peer_database
from ..database.ping import ping
from ..database.token_manager import token_manager

class database_loader:
    def launch(self):
        distributed_hash_table().start()
        peer_database().start()
        token_manager().start()
        find_node().start()
        ping().start()