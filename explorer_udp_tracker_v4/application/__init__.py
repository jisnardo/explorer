from ..application.udp_tracker_announce_completed import udp_tracker_announce_completed
from ..application.udp_tracker_announce_none import udp_tracker_announce_none
from ..application.udp_tracker_announce_started import udp_tracker_announce_started
from ..application.udp_tracker_announce_stopped import udp_tracker_announce_stopped
from ..application.udp_tracker_scrape import udp_tracker_scrape

class application_loader:
    def launch(self):
        udp_tracker_announce_completed().start()
        udp_tracker_announce_none().start()
        udp_tracker_announce_started().start()
        udp_tracker_announce_stopped().start()
        udp_tracker_scrape().start()