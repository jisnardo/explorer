import getuseragent
import httpx
import pyben
import urllib.parse

class scrape:
    def scrape(self, domain_url, info_hash):
        http_escape_character_info_hash = urllib.parse.quote_from_bytes(bytes.fromhex(info_hash))
        headers = {
            'Connection': 'close',
            'User-Agent': getuseragent.UserAgent().Random()
        }
        url = '{}/scrape?info_hash={}'.format(
            domain_url, http_escape_character_info_hash
        )
        with httpx.Client() as client:
            try:
                response = client.get(url = url, headers = headers)
                response.raise_for_status()
                if response.status_code == 200:
                    message = pyben.loads(response.content)
                    complete = 0
                    downloaded = 0
                    incomplete = 0
                    if 'files' in message:
                        if bytes.fromhex(info_hash) in message.get('files'):
                            if 'complete' in message['files'].get(bytes.fromhex(info_hash)):
                                complete = message['files'][bytes.fromhex(info_hash)].get('complete')
                            if 'downloaded' in message['files'].get(bytes.fromhex(info_hash)):
                                downloaded = message['files'][bytes.fromhex(info_hash)].get('downloaded')
                            if 'incomplete' in message['files'].get(bytes.fromhex(info_hash)):
                                incomplete = message['files'][bytes.fromhex(info_hash)].get('incomplete')
                    result = {
                        'complete': complete,
                        'downloaded': downloaded,
                        'incomplete': incomplete,
                        'state': True
                    }
                    return result
                else:
                    result = {
                        'error': response.status_code,
                        'state': False
                    }
                    return result
            except httpx.HTTPError as error:
                result = {
                    'error': error,
                    'state': False
                }
                return result
            except Exception as error:
                result = {
                    'error': error,
                    'state': False
                }
                return result
            finally:
                locals().clear()