from ...application.command.announce_peer import announce_peer
from ...application.command.find_node import find_node
from ...application.command.get_peers import get_peers
from ...application.command.ping import ping
from ...application.command.sample_infohashes import sample_infohashes
from ...application.command.commander import commander

class application_command_loader:
    def launch(self):
        announce_peer().start()
        find_node().start()
        get_peers().start()
        ping().start()
        sample_infohashes().start()
        commander().start()