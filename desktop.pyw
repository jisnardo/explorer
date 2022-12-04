from explorer_web_server.cache import application_cache
from explorer_web_server.memory import memory
from explorer_web_server.web_server import application
import explorer_database
import explorer_http_tracker
import explorer_krpc_v4
import explorer_krpc_v6
import explorer_peer_wire_v4
import explorer_peer_wire_v6
import explorer_spider
import explorer_udp_tracker_v4
import explorer_udp_tracker_v6
import gc
import sys
import webview

explorer_spider.launch(
    explorer_database,
    explorer_http_tracker,
    explorer_krpc_v4,
    explorer_krpc_v6,
    explorer_peer_wire_v4,
    explorer_peer_wire_v6,
    explorer_udp_tracker_v4,
    explorer_udp_tracker_v6
)
gc.enable()
memory.explorer_database = explorer_database
memory.explorer_krpc_v4 = explorer_krpc_v4
memory.explorer_krpc_v6 = explorer_krpc_v6
memory.explorer_peer_wire_v4 = explorer_peer_wire_v4
memory.explorer_peer_wire_v6 = explorer_peer_wire_v6
memory.explorer_spider = explorer_spider
webview.create_window(
    title = 'Explorer',
    url = application,
    width = 1024,
    height = 768,
    resizable = False,
    text_select = True
)
webview.start()
application_cache.clear()
sys.exit(0)