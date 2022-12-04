import tempfile

class memory:
    application_cache_config = {
        'CACHE_DEFAULT_TIMEOUT': 60,
        'CACHE_DIR': tempfile.gettempdir(),
        'CACHE_IGNORE_ERRORS': True,
        'CACHE_THRESHOLD': 1000,
        'CACHE_TYPE': 'filesystem'
    }
    application_support_languages = [
        'en-GB',
        'en-US',
        'zh-CN',
        'zh-HK',
        'zh-SG',
        'zh-TW'
    ]
    explorer_database = ''
    explorer_krpc_v4 = ''
    explorer_krpc_v6 = ''
    explorer_peer_wire_v4 = ''
    explorer_peer_wire_v6 = ''
    explorer_spider = ''