from .control import control
from .mysql import mysql

def check():
    '''

    explorer_database.check()

    Args:
        None

    Returns:
        For example:

        True

    '''
    control.control_check_messages_recvfrom.put(
        0
    )
    result = control.control_check_messages_send.get()
    return result

def count_all():
    '''

    explorer_database.count_all()

    Args:
        None

    Returns:
        For example:

        47

    '''
    control.control_count_all_messages_recvfrom.put(
        0
    )
    result = control.control_count_all_messages_send.get()
    return result

def count_discovered_on_with_day(day):
    '''

    explorer_database.count_discovered_on_with_day()

    Args:
        day: day('2022-09-10').

    Returns:
        For example:

        {
            'result': 4476,
            'header': {
                'day': '2022-09-10'
            }
        }

    '''
    control.control_count_discovered_on_with_day_messages_recvfrom.put(
        [day]
    )
    result = control.control_count_discovered_on_with_day_messages_send.get()
    return result

def count_discovered_on_with_month(month):
    '''

    explorer_database.count_discovered_on_with_month()

    Args:
        month: month('2022-09').

    Returns:
        For example:

        {
            'result': 125403,
            'header': {
                'month': '2022-09'
            }
        }

    '''
    control.control_count_discovered_on_with_month_messages_recvfrom.put(
        [month]
    )
    result = control.control_count_discovered_on_with_month_messages_send.get()
    return result

def count_info_hash(info_hash):
    '''

    explorer_database.count_info_hash()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        For example:

        {
            'result': 1,
            'header': {
                'info_hash': '59abaad8e68806ebac108bd69b13d7e9a38be5fb'
            }
        }

    '''
    control.control_count_info_hash_messages_recvfrom.put(
        [info_hash]
    )
    result = control.control_count_info_hash_messages_send.get()
    return result

def insert(info_hash, torrent_name, torrent_contents, torrent_size):
    '''

    explorer_database.insert()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').
        torrent_name: torrent file name.
        torrent_contents: torrent file contents.
        torrent_size: torrent file size.

    Returns:
        For example:

        {
            'result': True,
            'header': {
                'info_hash': 'b44a0e20fa5b7cecb77156333b4268dfd7c30afb',
                'torrent_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                'torrent_contents': {
                    '0': {
                        'file_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                        'file_size': 1331691520
                    }
                },
                'torrent_size': 1331691520
            }
        }

    '''
    control.control_insert_messages_recvfrom.put(
        [info_hash, torrent_name, torrent_contents, torrent_size]
    )
    result = control.control_insert_messages_send.get()
    return result

def query_all():
    '''

    explorer_database.query_all()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        For example:

        {
            'result': {
                '0': {
                    'info_hash': 'b44a0e20fa5b7cecb77156333b4268dfd7c30afb',
                    'torrent_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                    'torrent_contents': {
                        '0': {
                            'file_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                            'file_size': 1331691520
                        }
                    },
                    'torrent_size': 1331691520,
                    'discovered_on': 1649768393
                }
            }
        }

    '''
    control.control_query_all_messages_recvfrom.put(
        0
    )
    result = control.control_query_all_messages_send.get()
    return result

def query_discovered_on_with_day(day):
    '''

    explorer_database.query_discovered_on_with_day()

    Args:
        day: day('2022-09-10').

    Returns:
        For example:

        {
            'result': {
                '0': {
                    'info_hash': 'b44a0e20fa5b7cecb77156333b4268dfd7c30afb',
                    'torrent_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                    'torrent_contents': {
                        '0': {
                            'file_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                            'file_size': 1331691520
                        }
                    },
                    'torrent_size': 1331691520,
                    'discovered_on': 1649768393
                }
            },
            'header': {
                'day': '2022-09-10'
            }
        }

    '''
    control.control_query_discovered_on_with_day_messages_recvfrom.put(
        [day]
    )
    result = control.control_query_discovered_on_with_day_messages_send.get()
    return result

def query_info_hash(info_hash):
    '''

    explorer_database.query_info_hash()

    Args:
        info_hash: hexadecimal string of length 40('59abaad8e68806ebac108bd69b13d7e9a38be5fb').

    Returns:
        For example:

        {
            'result': {
                '0': {
                    'info_hash': 'b44a0e20fa5b7cecb77156333b4268dfd7c30afb',
                    'torrent_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                    'torrent_contents': {
                        '0': {
                            'file_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                            'file_size': 1331691520
                        }
                    },
                    'torrent_size': 1331691520,
                    'discovered_on': 1649768393
                }
            },
            'header': {
                'info_hash': 'b44a0e20fa5b7cecb77156333b4268dfd7c30afb'
            }
        }

    '''
    control.control_query_info_hash_messages_recvfrom.put(
        [info_hash]
    )
    result = control.control_query_info_hash_messages_send.get()
    return result

def query_like(keyword):
    '''

    explorer_database.query_like()

    Args:
        keyword: string.

    Returns:
        For example:

        {
            'result': {
                '0': {
                    'info_hash': 'b44a0e20fa5b7cecb77156333b4268dfd7c30afb',
                    'torrent_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                    'torrent_contents': {
                        '0': {
                            'file_name': 'ubuntu-20.04.4-live-server-amd64.iso',
                            'file_size': 1331691520
                        }
                    },
                    'torrent_size': 1331691520,
                    'discovered_on': 1649768393
                }
            },
            'header': {
                'keyword': 'ubuntu'
            }
        }

    '''
    control.control_query_like_messages_recvfrom.put(
        [keyword]
    )
    result = control.control_query_like_messages_send.get()
    return result

def query_torrent_size():
    '''

    explorer_database.query_torrent_size()

    Args:
        None

    Returns:
        For example:

        {
            'result': {
                '0': {
                    'torrent_size': 1331691520
                }
            }
        }

    '''
    control.control_query_torrent_size_messages_recvfrom.put(
        0
    )
    result = control.control_query_torrent_size_messages_send.get()
    return result

def query_torrent_size_with_day(day):
    '''

    explorer_database.query_torrent_size_with_day()

    Args:
        day: day('2022-09-10').

    Returns:
        For example:

        {
            'result': {
                '0': {
                    'torrent_size': 1331691520
                }
            },
            'header': {
                'day': '2022-09-10'
            }
        }

    '''
    control.control_query_torrent_size_with_day_messages_recvfrom.put(
        [day]
    )
    result = control.control_query_torrent_size_with_day_messages_send.get()
    return result

control().start()
mysql().start()