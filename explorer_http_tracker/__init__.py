from .application import application_loader
from .application.http_tracker_announce_completed import http_tracker_announce_completed
from .application.http_tracker_announce_none import http_tracker_announce_none
from .application.http_tracker_announce_started import http_tracker_announce_started
from .application.http_tracker_announce_stopped import http_tracker_announce_stopped
from .application.http_tracker_scrape import http_tracker_scrape
from .driver import driver_loader
from .driver.memory import memory
import re

def announce_completed(domain_url, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_http_tracker.announce_completed()

    Args:
        domain_url: http://example.com:6969.
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        downloaded: decimal number.
        left: decimal number.
        uploaded: decimal number.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'complete': 1,
                'downloaded': 3,
                'incomplete': 0,
                'interval': 1994,
                'min_interval': 896,
                'peers': [],
                'peers6': [],
                'status': True
            },
            'header': {
                'domain_url': 'http://example.com:6969',
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        if 1 <= tcp_port <= 65535:
            http_tracker_announce_completed.application_http_tracker_announce_completed_messages_recvfrom.put(
                [domain_url, match.group(0), downloaded, left, uploaded, tcp_port]
            )
            result = http_tracker_announce_completed.application_http_tracker_announce_completed_messages_send.get()
            return result

def announce_none(domain_url, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_http_tracker.announce_none()

    Args:
        domain_url: http://example.com:6969.
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        downloaded: decimal number.
        left: decimal number.
        uploaded: decimal number.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'complete': 1,
                'downloaded': 3,
                'incomplete': 0,
                'interval': 1994,
                'min_interval': 896,
                'peers': [['8.8.4.4', 51413], ['8.8.8.8', 6881]],
                'peers6': [['2001:4860:4860::8844', 51413], ['2001:4860:4860::8888', 6881]],
                'status': True
            },
            'header': {
                'domain_url': 'http://example.com:6969',
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        if 1 <= tcp_port <= 65535:
            http_tracker_announce_none.application_http_tracker_announce_none_messages_recvfrom.put(
                [domain_url, match.group(0), downloaded, left, uploaded, tcp_port]
            )
            result = http_tracker_announce_none.application_http_tracker_announce_none_messages_send.get()
            return result

def announce_started(domain_url, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_http_tracker.announce_started()

    Args:
        domain_url: http://example.com:6969.
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        tcp_port: decimal number(1 - 65535).
        uploaded: decimal number.
        downloaded: decimal number.
        left: decimal number.

    Returns:
        For example:

        {
            'result': {
                'complete': 1,
                'downloaded': 3,
                'incomplete': 0,
                'interval': 1994,
                'min_interval': 896,
                'peers': [['8.8.4.4', 51413], ['8.8.8.8', 6881]],
                'peers6': [['2001:4860:4860::8844', 51413], ['2001:4860:4860::8888', 6881]],
                'status': True
            },
            'header': {
                'domain_url': 'http://example.com:6969',
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        if 1 <= tcp_port <= 65535:
            http_tracker_announce_started.application_http_tracker_announce_started_messages_recvfrom.put(
                [domain_url, match.group(0), downloaded, left, uploaded, tcp_port]
            )
            result = http_tracker_announce_started.application_http_tracker_announce_started_messages_send.get()
            return result

def announce_stopped(domain_url, info_hash, downloaded, left, uploaded, tcp_port):
    '''

    explorer_http_tracker.announce_stopped()

    Args:
        domain_url: http://example.com:6969.
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        uploaded: decimal number.
        downloaded: decimal number.
        left: decimal number.
        tcp_port: decimal number(1 - 65535).

    Returns:
        For example:

        {
            'result': {
                'complete': 1,
                'downloaded': 3,
                'incomplete': 0,
                'interval': 1994,
                'min_interval': 896,
                'peers': [],
                'peers6': [],
                'status': True
            },
            'header': {
                'domain_url': 'http://example.com:6969',
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6',
                'downloaded': 1024,
                'left': 0,
                'uploaded': 1024,
                'tcp_port': 6881
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        if 1 <= tcp_port <= 65535:
            http_tracker_announce_stopped.application_http_tracker_announce_stopped_messages_recvfrom.put(
                [domain_url, match.group(0), downloaded, left, uploaded, tcp_port]
            )
            result = http_tracker_announce_stopped.application_http_tracker_announce_stopped_messages_send.get()
            return result

def scrape(domain_url, info_hash):
    '''

    explorer_http_tracker.scrape()

    Args:
        domain_url: http://example.com:6969.
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        For example:

        {
            'result': {
                'complete': 1,
                'downloaded': 3,
                'incomplete': 0,
                'status': True
            },
            'header': {
                'domain_url': 'http://example.com:6969',
                'info_hash': 'cf0a537944c001ad86b1ca058e8d877f5f022fc6'
            }
        }

    '''
    pattern = re.compile(r'\b[0-9a-f]{40}\b')
    match = re.match(pattern, info_hash.lower())
    if match is not None:
        http_tracker_scrape.application_http_tracker_scrape_messages_recvfrom.put(
            [domain_url, match.group(0)]
        )
        result = http_tracker_scrape.application_http_tracker_scrape_messages_send.get()
        return result

def self_peer_id():
    '''

    explorer_http_tracker.self_peer_id()

    Args:
        None

    Returns:
        For example:

        '2d4550303030312d36634e5e356f4b2a3169592a'

    '''
    return memory().peer_id

driver_loader().launch()
application_loader().launch()