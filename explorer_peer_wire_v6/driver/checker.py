import hashlib
import pyben

class check:
    def extension_ut_metadata(self, torrent_data, info_hash):
        info = pyben.dumps(torrent_data['info'])
        new_info_hash = hashlib.sha1(info).hexdigest()
        if info_hash == new_info_hash:
            return True
        else:
            return False