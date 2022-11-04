from ..application.http_tracker_announce_completed import http_tracker_announce_completed
from ..application.http_tracker_announce_none import http_tracker_announce_none
from ..application.http_tracker_announce_started import http_tracker_announce_started
from ..application.http_tracker_announce_stopped import http_tracker_announce_stopped
from ..application.http_tracker_scrape import http_tracker_scrape

class application_loader:
    def launch(self):
        http_tracker_announce_completed().start()
        http_tracker_announce_none().start()
        http_tracker_announce_started().start()
        http_tracker_announce_stopped().start()
        http_tracker_scrape().start()