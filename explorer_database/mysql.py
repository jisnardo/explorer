import json
import os
import pymysql
import queue
import threading
import time

class mysql:
    mysql_check_messages_recvfrom = queue.Queue()
    mysql_check_messages_send = queue.Queue()
    mysql_count_all_messages_recvfrom = queue.Queue()
    mysql_count_all_messages_send = queue.Queue()
    mysql_count_discovered_on_with_day_messages_recvfrom = queue.Queue()
    mysql_count_discovered_on_with_day_messages_send = queue.Queue()
    mysql_count_discovered_on_with_month_messages_recvfrom = queue.Queue()
    mysql_count_discovered_on_with_month_messages_send = queue.Queue()
    mysql_count_info_hash_messages_recvfrom = queue.Queue()
    mysql_count_info_hash_messages_send = queue.Queue()
    mysql_insert_messages_recvfrom = queue.Queue()
    mysql_insert_messages_send = queue.Queue()
    mysql_query_all_messages_recvfrom = queue.Queue()
    mysql_query_all_messages_send = queue.Queue()
    mysql_query_discovered_on_with_day_messages_recvfrom = queue.Queue()
    mysql_query_discovered_on_with_day_messages_send = queue.Queue()
    mysql_query_info_hash_messages_recvfrom = queue.Queue()
    mysql_query_info_hash_messages_send = queue.Queue()
    mysql_query_like_messages_recvfrom = queue.Queue()
    mysql_query_like_messages_send = queue.Queue()
    mysql_query_torrent_size_messages_recvfrom = queue.Queue()
    mysql_query_torrent_size_messages_send = queue.Queue()
    mysql_query_torrent_size_with_day_messages_recvfrom = queue.Queue()
    mysql_query_torrent_size_with_day_messages_send = queue.Queue()

    def __check(self):
        while True:
            self.mysql_check_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                connection.close()
                self.mysql_check_messages_send.put(
                    True
                )
            except:
                self.mysql_check_messages_send.put(
                    False
                )

    def __count_all(self):
        while True:
            self.mysql_count_all_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute('select count(*) from `torrent_information_table`;')
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_count_all_messages_send.put(
                    result
                )

    def __count_discovered_on_with_day(self):
        while True:
            day = self.mysql_count_discovered_on_with_day_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute(
                    'select count(*) from `torrent_information_table` where date_format(`discovered_on`, \'%Y-%m-%d\') = \'{}\';'
                    .format(day)
                )
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_count_discovered_on_with_day_messages_send.put(
                    result
                )

    def __count_discovered_on_with_month(self):
        while True:
            month = self.mysql_count_discovered_on_with_month_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute(
                    'select count(*) from `torrent_information_table` where date_format(`discovered_on`, \'%Y-%m\') = \'{}\';'
                    .format(month)
                )
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_count_discovered_on_with_month_messages_send.put(
                    result
                )

    def __count_info_hash(self):
        while True:
            info_hash = self.mysql_count_info_hash_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute(
                    'select count(*) from `torrent_information_table` where `info_hash` = \'{}\';'
                    .format(info_hash)
                )
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_count_info_hash_messages_send.put(
                    result
                )

    def __insert(self):
        while True:
            mysql_insert_messages_recvfrom = self.mysql_insert_messages_recvfrom.get()
            info_hash = mysql_insert_messages_recvfrom[0]
            torrent_name = mysql_insert_messages_recvfrom[1]
            torrent_contents = mysql_insert_messages_recvfrom[2]
            torrent_size = mysql_insert_messages_recvfrom[3]
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute(
                    'lock tables `torrent_information_table` write;'
                )
                connection.commit()
                cursor.execute(
                    'alter table `torrent_information_table` auto_increment = 1;'
                )
                connection.commit()
                cursor.execute(
                    'insert ignore into `torrent_information_table`(`info_hash`, `torrent_name`, `torrent_contents`, `torrent_size`) values(\'{}\', \'{}\', \'{}\', \'{}\');'
                    .format(info_hash, pymysql.converters.escape_string(torrent_name), pymysql.converters.escape_string(torrent_contents), torrent_size)
                )
                connection.commit()
                cursor.execute(
                    'unlock tables;'
                )
                connection.commit()
                result = True
                cursor.close()
                connection.close()
            except:
                result = False
                if 'connection' in locals().keys():
                    if type(connection) is not None:
                        connection.rollback()
                        cursor.close()
                        connection.close()
            finally:
                self.mysql_insert_messages_send.put(
                    result
                )
            time.sleep(1)

    def __load_config(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/database_config.json', mode = 'r', encoding = 'utf-8') as file:
            config = file.read()
            database_config = json.loads(config)['mysql']
            return database_config

    def __query_all(self):
        while True:
            self.mysql_query_all_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute('select * from `torrent_information_table`;')
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_query_all_messages_send.put(
                    result
                )

    def __query_discovered_on_with_day(self):
        while True:
            day = self.mysql_query_discovered_on_with_day_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute(
                    'select * from `torrent_information_table` where date_format(`discovered_on`, \'%Y-%m-%d\') = \'{}\';'
                    .format(day)
                )
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_query_discovered_on_with_day_messages_send.put(
                    result
                )

    def __query_info_hash(self):
        while True:
            info_hash = self.mysql_query_info_hash_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute(
                    'select * from `torrent_information_table` where `info_hash` = \'{}\';'
                    .format(info_hash)
                )
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_query_info_hash_messages_send.put(
                    result
                )

    def __query_like(self):
        while True:
            keyword = self.mysql_query_like_messages_recvfrom.get()
            if keyword.find(' ') == -1:
                try:
                    connection = pymysql.connect(**self.__load_config())
                    cursor = connection.cursor()
                    cursor.execute(
                        'select * from `torrent_information_table` where `torrent_name` like \'%{}%\';'
                        .format(keyword)
                    )
                    connection.commit()
                    result = cursor.fetchall()
                    cursor.close()
                    connection.close()
                except:
                    result = False
                finally:
                    self.mysql_query_like_messages_send.put(
                        result
                    )
            else:
                keyword = keyword.split(' ')
                sql_statement = 'select * from `torrent_information_table` where `torrent_name` like \'%{}%\''.format(keyword[0])
                for i in range(1, len(keyword)):
                    sql_statement = sql_statement + 'and `torrent_name` like \'%{}%\''.format(keyword[i])
                    if i == len(keyword) - 1:
                        sql_statement = sql_statement + ';'
                try:
                    connection = pymysql.connect(**self.__load_config())
                    cursor = connection.cursor()
                    cursor.execute(sql_statement)
                    connection.commit()
                    result = cursor.fetchall()
                    cursor.close()
                    connection.close()
                except:
                    result = False
                finally:
                    self.mysql_query_like_messages_send.put(
                        result
                    )

    def __query_torrent_size(self):
        while True:
            self.mysql_query_torrent_size_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute('select `torrent_size` from `torrent_information_table`;')
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_query_torrent_size_messages_send.put(
                    result
                )

    def __query_torrent_size_with_day(self):
        while True:
            day = self.mysql_query_torrent_size_with_day_messages_recvfrom.get()
            try:
                connection = pymysql.connect(**self.__load_config())
                cursor = connection.cursor()
                cursor.execute(
                    'select `torrent_size` from `torrent_information_table` where date_format(`discovered_on`, \'%Y-%m-%d\') = \'{}\';'
                    .format(day)
                )
                connection.commit()
                result = cursor.fetchall()
                cursor.close()
                connection.close()
            except:
                result = False
            finally:
                self.mysql_query_torrent_size_with_day_messages_send.put(
                    result
                )

    def start(self):
        explorer_database_mysql_check_thread = threading.Thread(target = self.__check)
        explorer_database_mysql_check_thread.setDaemon(True)
        explorer_database_mysql_check_thread.start()
        explorer_database_mysql_count_all_thread = threading.Thread(target = self.__count_all)
        explorer_database_mysql_count_all_thread.setDaemon(True)
        explorer_database_mysql_count_all_thread.start()
        explorer_database_mysql_count_discovered_on_with_day_thread = threading.Thread(target = self.__count_discovered_on_with_day)
        explorer_database_mysql_count_discovered_on_with_day_thread.setDaemon(True)
        explorer_database_mysql_count_discovered_on_with_day_thread.start()
        explorer_database_mysql_count_discovered_on_with_month_thread = threading.Thread(target = self.__count_discovered_on_with_month)
        explorer_database_mysql_count_discovered_on_with_month_thread.setDaemon(True)
        explorer_database_mysql_count_discovered_on_with_month_thread.start()
        explorer_database_mysql_count_info_hash_thread = threading.Thread(target = self.__count_info_hash)
        explorer_database_mysql_count_info_hash_thread.setDaemon(True)
        explorer_database_mysql_count_info_hash_thread.start()
        explorer_database_mysql_insert_thread = threading.Thread(target = self.__insert)
        explorer_database_mysql_insert_thread.setDaemon(True)
        explorer_database_mysql_insert_thread.start()
        explorer_database_mysql_query_all_thread = threading.Thread(target = self.__query_all)
        explorer_database_mysql_query_all_thread.setDaemon(True)
        explorer_database_mysql_query_all_thread.start()
        explorer_database_mysql_query_discovered_on_with_day_thread = threading.Thread(target = self.__query_discovered_on_with_day)
        explorer_database_mysql_query_discovered_on_with_day_thread.setDaemon(True)
        explorer_database_mysql_query_discovered_on_with_day_thread.start()
        explorer_database_mysql_query_info_hash_thread = threading.Thread(target = self.__query_info_hash)
        explorer_database_mysql_query_info_hash_thread.setDaemon(True)
        explorer_database_mysql_query_info_hash_thread.start()
        explorer_database_mysql_query_like_thread = threading.Thread(target = self.__query_like)
        explorer_database_mysql_query_like_thread.setDaemon(True)
        explorer_database_mysql_query_like_thread.start()
        explorer_database_mysql_query_torrent_size_thread = threading.Thread(target = self.__query_torrent_size)
        explorer_database_mysql_query_torrent_size_thread.setDaemon(True)
        explorer_database_mysql_query_torrent_size_thread.start()
        explorer_database_mysql_query_torrent_size_with_day_thread = threading.Thread(target = self.__query_torrent_size_with_day)
        explorer_database_mysql_query_torrent_size_with_day_thread.setDaemon(True)
        explorer_database_mysql_query_torrent_size_with_day_thread.start()