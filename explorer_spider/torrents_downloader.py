from .database import insert
from .save_torrent_files import save_torrent_files
import getuseragent
import hashlib
import httpx
import pyben
import queue
import threading
import time

class torrents_downloader:
    spider_torrents_downloader_messages = queue.Queue()

    def __get_torrent(self, explorer_database):
        while True:
            info_hash = self.spider_torrents_downloader_messages.get()
            database_count_info_hash_messages = explorer_database.count_info_hash(info_hash)
            if database_count_info_hash_messages['result'] == 0:
                headers = {
                    'Connection': 'close',
                    'User-Agent': getuseragent.UserAgent().Random()
                }
                url = 'https://itorrents.org/torrent/{}.torrent'.format(info_hash.upper())
                with httpx.Client() as client:
                    try:
                        response = client.get(url = url, headers = headers)
                        response.raise_for_status()
                        if response.status_code == 200:
                            torrent_data = pyben.loads(response.content)
                            info = pyben.dumps(torrent_data['info'])
                            new_info_hash = hashlib.sha1(info).hexdigest()
                            if info_hash == new_info_hash:
                                insert.spider_database_insert_messages.put({
                                    'info': torrent_data['info']
                                })
                                save_torrent_files.spider_save_torrent_files_messages.put({
                                    'info': torrent_data['info']
                                })
                    except httpx.HTTPError:
                        pass
                    except Exception:
                        pass
                    finally:
                        locals().clear()
                time.sleep(60)

    def start(self, explorer_database):
        explorer_spider_torrents_downloader_get_torrent_thread = threading.Thread(target = self.__get_torrent, args = (explorer_database,))
        explorer_spider_torrents_downloader_get_torrent_thread.setDaemon(True)
        explorer_spider_torrents_downloader_get_torrent_thread.start()