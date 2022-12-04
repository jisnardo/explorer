from .mysql import mysql
import json
import os
import queue
import threading
import time

class control:
    control_check_messages_recvfrom = queue.Queue()
    control_check_messages_send = queue.Queue()
    control_count_all_messages_recvfrom = queue.Queue()
    control_count_all_messages_send = queue.Queue()
    control_count_discovered_on_with_day_messages_recvfrom = queue.Queue()
    control_count_discovered_on_with_day_messages_send = queue.Queue()
    control_count_discovered_on_with_month_messages_recvfrom = queue.Queue()
    control_count_discovered_on_with_month_messages_send = queue.Queue()
    control_count_info_hash_messages_recvfrom = queue.Queue()
    control_count_info_hash_messages_send = queue.Queue()
    control_insert_messages_recvfrom = queue.Queue()
    control_insert_messages_send = queue.Queue()
    control_query_all_messages_recvfrom = queue.Queue()
    control_query_all_messages_send = queue.Queue()
    control_query_discovered_on_with_day_messages_recvfrom = queue.Queue()
    control_query_discovered_on_with_day_messages_send = queue.Queue()
    control_query_info_hash_messages_recvfrom = queue.Queue()
    control_query_info_hash_messages_send = queue.Queue()
    control_query_like_messages_recvfrom = queue.Queue()
    control_query_like_messages_send = queue.Queue()
    control_query_torrent_size_messages_recvfrom = queue.Queue()
    control_query_torrent_size_messages_send = queue.Queue()
    control_query_torrent_size_with_day_messages_recvfrom = queue.Queue()
    control_query_torrent_size_with_day_messages_send = queue.Queue()

    def __check(self):
        while True:
            self.control_check_messages_recvfrom.get()
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_check_messages_recvfrom.put(
                        0
                    )
                    result = mysql.mysql_check_messages_send.get()
                    self.control_check_messages_send.put(
                        result
                    )

    def __count_all(self):
        while True:
            self.control_count_all_messages_recvfrom.get()
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_count_all_messages_recvfrom.put(
                        0
                    )
                    result = mysql.mysql_count_all_messages_send.get()
                    if result is False:
                        self.control_count_all_messages_send.put(
                            0
                        )
                    else:
                        self.control_count_all_messages_send.put(
                            result[0][0]
                        )

    def __count_discovered_on_with_day(self):
        while True:
            control_count_discovered_on_with_day_messages_recvfrom = self.control_count_discovered_on_with_day_messages_recvfrom.get()
            day = control_count_discovered_on_with_day_messages_recvfrom[0]
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_count_discovered_on_with_day_messages_recvfrom.put(
                        day
                    )
                    result = mysql.mysql_count_discovered_on_with_day_messages_send.get()
                    if result is False:
                        self.control_count_discovered_on_with_day_messages_send.put({
                            'result': 0,
                            'header': {
                                'day': day
                            }
                        })
                    else:
                        self.control_count_discovered_on_with_day_messages_send.put({
                            'result': result[0][0],
                            'header': {
                                'day': day
                            }
                        })

    def __count_discovered_on_with_month(self):
        while True:
            control_count_discovered_on_with_month_messages_recvfrom = self.control_count_discovered_on_with_month_messages_recvfrom.get()
            month = control_count_discovered_on_with_month_messages_recvfrom[0]
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_count_discovered_on_with_month_messages_recvfrom.put(
                        month
                    )
                    result = mysql.mysql_count_discovered_on_with_month_messages_send.get()
                    if result is False:
                        self.control_count_discovered_on_with_month_messages_send.put({
                            'result': 0,
                            'header': {
                                'month': month
                            }
                        })
                    else:
                        self.control_count_discovered_on_with_month_messages_send.put({
                            'result': result[0][0],
                            'header': {
                                'month': month
                            }
                        })

    def __count_info_hash(self):
        while True:
            control_count_info_hash_messages_recvfrom = self.control_count_info_hash_messages_recvfrom.get()
            info_hash = control_count_info_hash_messages_recvfrom[0]
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_count_info_hash_messages_recvfrom.put(
                        info_hash
                    )
                    result = mysql.mysql_count_info_hash_messages_send.get()
                    if result is False:
                        self.control_count_info_hash_messages_send.put({
                            'result': 0,
                            'header': {
                                'info_hash': info_hash
                            }
                        })
                    else:
                        self.control_count_info_hash_messages_send.put({
                            'result': result[0][0],
                            'header': {
                                'info_hash': info_hash
                            }
                        })

    def __insert(self):
        while True:
            control_insert_messages_recvfrom = self.control_insert_messages_recvfrom.get()
            try:
                info_hash = control_insert_messages_recvfrom[0]
                torrent_name = control_insert_messages_recvfrom[1]
                torrent_contents = control_insert_messages_recvfrom[2]
                torrent_size = control_insert_messages_recvfrom[3]
                torrent_contents = json.dumps(torrent_contents)
                with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                    config = file.read()
                    default_database = json.loads(config)['default_database']
                    if default_database == 'mysql':
                        mysql.mysql_insert_messages_recvfrom.put(
                            [info_hash, torrent_name, torrent_contents, torrent_size]
                        )
                        result = mysql.mysql_insert_messages_send.get()
                        self.control_insert_messages_send.put({
                            'result': result,
                            'header': {
                                'info_hash': info_hash,
                                'torrent_name': torrent_name,
                                'torrent_contents': torrent_contents,
                                'torrent_size': torrent_size
                            }
                        })
            except:
                self.control_insert_messages_send.put({
                    'result': False,
                    'header': {
                        'info_hash': info_hash,
                        'torrent_name': torrent_name,
                        'torrent_contents': torrent_contents,
                        'torrent_size': torrent_size
                    }
                })

    def __query_all(self):
        while True:
            self.control_query_all_messages_recvfrom.get()
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_query_all_messages_recvfrom.put(
                        0
                    )
                    result = mysql.mysql_query_all_messages_send.get()
                    if result is False:
                        self.control_query_all_messages_send.put({
                            'result': False
                        })
                    elif len(result) > 0:
                        data = {}
                        for i in range(0, len(result)):
                            data.update({str(i): {}})
                            data[str(i)]['info_hash'] = result[i][1]
                            data[str(i)]['torrent_name'] = result[i][2]
                            torrent_contents = json.loads(result[i][3])
                            data[str(i)]['torrent_contents'] = torrent_contents
                            data[str(i)]['torrent_size'] = result[i][4]
                            discovered_on = result[i][5].timetuple()
                            discovered_on = time.mktime(discovered_on)
                            discovered_on = int(discovered_on)
                            data[str(i)]['discovered_on'] = discovered_on
                        self.control_query_all_messages_send.put({
                            'result': data
                        })
                    else:
                        self.control_query_all_messages_send.put({
                            'result': False
                        })

    def __query_discovered_on_with_day(self):
        while True:
            control_query_discovered_on_with_day_messages_recvfrom = self.control_query_discovered_on_with_day_messages_recvfrom.get()
            day = control_query_discovered_on_with_day_messages_recvfrom[0]
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_query_discovered_on_with_day_messages_recvfrom.put(
                        day
                    )
                    result = mysql.mysql_query_discovered_on_with_day_messages_send.get()
                    if result is False:
                        self.control_query_discovered_on_with_day_messages_send.put({
                            'result': False,
                            'header': {
                                'day': day
                            }
                        })
                    elif len(result) > 0:
                        data = {}
                        for i in range(0, len(result)):
                            data.update({str(i): {}})
                            data[str(i)]['info_hash'] = result[i][1]
                            data[str(i)]['torrent_name'] = result[i][2]
                            torrent_contents = json.loads(result[i][3])
                            data[str(i)]['torrent_contents'] = torrent_contents
                            data[str(i)]['torrent_size'] = result[i][4]
                            discovered_on = result[i][5].timetuple()
                            discovered_on = time.mktime(discovered_on)
                            discovered_on = int(discovered_on)
                            data[str(i)]['discovered_on'] = discovered_on
                        self.control_query_discovered_on_with_day_messages_send.put({
                            'result': data,
                            'header': {
                                'day': day
                            }
                        })
                    else:
                        self.control_query_discovered_on_with_day_messages_send.put({
                            'result': False,
                            'header': {
                                'day': day
                            }
                        })

    def __query_info_hash(self):
        while True:
            control_query_info_hash_messages_recvfrom = self.control_query_info_hash_messages_recvfrom.get()
            info_hash = control_query_info_hash_messages_recvfrom[0]
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_query_info_hash_messages_recvfrom.put(
                        info_hash
                    )
                    result = mysql.mysql_query_info_hash_messages_send.get()
                    if result is False:
                        self.control_query_info_hash_messages_send.put({
                            'result': False,
                            'header': {
                                'info_hash': info_hash
                            }
                        })
                    elif len(result) > 0:
                        data = {}
                        for i in range(0, len(result)):
                            data.update({str(i): {}})
                            data[str(i)]['info_hash'] = result[i][1]
                            data[str(i)]['torrent_name'] = result[i][2]
                            torrent_contents = json.loads(result[i][3])
                            data[str(i)]['torrent_contents'] = torrent_contents
                            data[str(i)]['torrent_size'] = result[i][4]
                            discovered_on = result[i][5].timetuple()
                            discovered_on = time.mktime(discovered_on)
                            discovered_on = int(discovered_on)
                            data[str(i)]['discovered_on'] = discovered_on
                        self.control_query_info_hash_messages_send.put({
                            'result': data,
                            'header': {
                                'info_hash': info_hash
                            }
                        })
                    else:
                        self.control_query_info_hash_messages_send.put({
                            'result': False,
                            'header': {
                                'info_hash': info_hash
                            }
                        })

    def __query_like(self):
        while True:
            control_query_like_messages_recvfrom = self.control_query_like_messages_recvfrom.get()
            keyword = control_query_like_messages_recvfrom[0]
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql.mysql_query_like_messages_recvfrom.put(
                        keyword
                    )
                    result = mysql.mysql_query_like_messages_send.get()
                    if result is False:
                        self.control_query_like_messages_send.put({
                            'result': False,
                            'header': {
                                'keyword': keyword
                            }
                        })
                    elif len(result) > 0:
                        data = {}
                        for i in range(0, len(result)):
                            data.update({str(i): {}})
                            data[str(i)]['info_hash'] = result[i][1]
                            data[str(i)]['torrent_name'] = result[i][2]
                            torrent_contents = json.loads(result[i][3])
                            data[str(i)]['torrent_contents'] = torrent_contents
                            data[str(i)]['torrent_size'] = result[i][4]
                            discovered_on = result[i][5].timetuple()
                            discovered_on = time.mktime(discovered_on)
                            discovered_on = int(discovered_on)
                            data[str(i)]['discovered_on'] = discovered_on
                        self.control_query_like_messages_send.put({
                            'result': data,
                            'header': {
                                'keyword': keyword
                            }
                        })
                    else:
                        self.control_query_like_messages_send.put({
                            'result': False,
                            'header': {
                                'keyword': keyword
                            }
                        })

    def __query_torrent_size(self):
        while True:
            self.control_query_torrent_size_messages_recvfrom.get()
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql().mysql_query_torrent_size_messages_recvfrom.put(
                        0
                    )
                    result = mysql().mysql_query_torrent_size_messages_send.get()
                    if result is False:
                        self.control_query_torrent_size_messages_send.put({
                            'result': False
                        })
                    elif len(result) > 0:
                        data = {}
                        for i in range(0, len(result)):
                            data.update({str(i): {}})
                            data[str(i)]['torrent_size'] = result[i][0]
                        self.control_query_torrent_size_messages_send.put({
                            'result': data
                        })
                    else:
                        self.control_query_torrent_size_messages_send.put({
                            'result': False
                        })

    def __query_torrent_size_with_day(self):
        while True:
            control_query_torrent_size_with_date_messages_recvfrom = self.control_query_torrent_size_with_day_messages_recvfrom.get()
            day = control_query_torrent_size_with_date_messages_recvfrom[0]
            with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
                config = file.read()
                default_database = json.loads(config)['default_database']
                if default_database == 'mysql':
                    mysql().mysql_query_torrent_size_with_day_messages_recvfrom.put(
                        day
                    )
                    result = mysql().mysql_query_torrent_size_with_day_messages_send.get()
                    if result is False:
                        self.control_query_torrent_size_with_day_messages_send.put({
                            'result': False,
                            'header': {
                                'day': day
                            }
                        })
                    elif len(result) > 0:
                        data = {}
                        for i in range(0, len(result)):
                            data.update({str(i): {}})
                            data[str(i)]['torrent_size'] = result[i][0]
                        self.control_query_torrent_size_with_day_messages_send.put({
                            'result': data,
                            'header': {
                                'day': day
                            }
                        })
                    else:
                        self.control_query_torrent_size_with_day_messages_send.put({
                            'result': False,
                            'header': {
                                'day': day
                            }
                        })

    def start(self):
        explorer_database_control_check_thread = threading.Thread(target = self.__check)
        explorer_database_control_check_thread.setDaemon(True)
        explorer_database_control_check_thread.start()
        explorer_database_control_count_all_thread = threading.Thread(target = self.__count_all)
        explorer_database_control_count_all_thread.setDaemon(True)
        explorer_database_control_count_all_thread.start()
        explorer_database_control_count_discovered_on_with_day_thread = threading.Thread(target = self.__count_discovered_on_with_day)
        explorer_database_control_count_discovered_on_with_day_thread.setDaemon(True)
        explorer_database_control_count_discovered_on_with_day_thread.start()
        explorer_database_control_count_discovered_on_with_month_thread = threading.Thread(target = self.__count_discovered_on_with_month)
        explorer_database_control_count_discovered_on_with_month_thread.setDaemon(True)
        explorer_database_control_count_discovered_on_with_month_thread.start()
        explorer_database_control_count_info_hash_thread = threading.Thread(target = self.__count_info_hash)
        explorer_database_control_count_info_hash_thread.setDaemon(True)
        explorer_database_control_count_info_hash_thread.start()
        explorer_database_control_insert_thread = threading.Thread(target = self.__insert)
        explorer_database_control_insert_thread.setDaemon(True)
        explorer_database_control_insert_thread.start()
        explorer_database_control_query_all_thread = threading.Thread(target = self.__query_all)
        explorer_database_control_query_all_thread.setDaemon(True)
        explorer_database_control_query_all_thread.start()
        explorer_database_control_query_discovered_on_with_day_thread = threading.Thread(target = self.__query_discovered_on_with_day)
        explorer_database_control_query_discovered_on_with_day_thread.setDaemon(True)
        explorer_database_control_query_discovered_on_with_day_thread.start()
        explorer_database_control_query_info_hash_thread = threading.Thread(target = self.__query_info_hash)
        explorer_database_control_query_info_hash_thread.setDaemon(True)
        explorer_database_control_query_info_hash_thread.start()
        explorer_database_control_query_like_thread = threading.Thread(target = self.__query_like)
        explorer_database_control_query_like_thread.setDaemon(True)
        explorer_database_control_query_like_thread.start()
        explorer_database_control_query_torrent_size_thread = threading.Thread(target = self.__query_torrent_size)
        explorer_database_control_query_torrent_size_thread.setDaemon(True)
        explorer_database_control_query_torrent_size_thread.start()
        explorer_database_control_query_torrent_size_with_day_thread = threading.Thread(target = self.__query_torrent_size_with_day)
        explorer_database_control_query_torrent_size_with_day_thread.setDaemon(True)
        explorer_database_control_query_torrent_size_with_day_thread.start()