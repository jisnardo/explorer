from .memory import memory
import calendar
import datetime
import humanfriendly
import IPy
import json
import natsort
import os
import pathlib
import pyben
import threading
import time

class data_conversion:
    def __get_user_language_config(self, user_language):
        if user_language is None:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return user_language_data_config
        elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return user_language_data_config
        else:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return user_language_data_config

    def explorer_database_check(self):
        database_check_messages = memory.explorer_database.check()
        return database_check_messages

    def explorer_database_query_discovery_of_the_day_data(self):
        database_query_discovered_on_with_day_messages = memory.explorer_database.query_discovered_on_with_day(str(datetime.date.today()))
        if database_query_discovered_on_with_day_messages['result'] is False:
            return []
        else:
            result = []
            for i in database_query_discovered_on_with_day_messages['result'].keys():
                result.append({
                    'id': len(database_query_discovered_on_with_day_messages['result']) - int(i),
                    'torrent_name': '<a href="./report?info_hash=' +
                        database_query_discovered_on_with_day_messages['result'][i]['info_hash'] +
                        '" class="link-dark">' +
                        database_query_discovered_on_with_day_messages['result'][i]['torrent_name'] +
                        '</a>',
                    'torrent_size': humanfriendly.format_size(database_query_discovered_on_with_day_messages['result'][i]['torrent_size'], binary = True).replace('bytes', 'B')
                })
            result.reverse()
            return result

    def explorer_database_query_discovery_of_the_day_number(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        discovery_of_the_day_number_messages = {}
        database_count_discovered_on_with_day_messages = memory.explorer_database.count_discovered_on_with_day(str(datetime.date.today()))
        database_query_torrent_size_with_day_messages = memory.explorer_database.query_torrent_size_with_day(str(datetime.date.today()))
        if database_query_torrent_size_with_day_messages['result'] is False:
            info_hash_file_size = '0 B'
        else:
            info_hash_file_size = 0
            for i in database_query_torrent_size_with_day_messages['result'].keys():
                info_hash_file_size = info_hash_file_size + database_query_torrent_size_with_day_messages['result'][i]['torrent_size']
            info_hash_file_size = humanfriendly.format_size(info_hash_file_size, binary = True).replace('bytes', 'B')
        discovery_of_the_day_number_messages[user_language_data_config['day']] = str(datetime.date.today())
        discovery_of_the_day_number_messages[user_language_data_config['info_hash']] = database_count_discovered_on_with_day_messages['result']
        discovery_of_the_day_number_messages[user_language_data_config['file_size']] = info_hash_file_size
        result = []
        for i in discovery_of_the_day_number_messages.keys():
            result.append({
                'id': len(result) + 1,
                'item': i,
                'value': discovery_of_the_day_number_messages[i]
            })
        return result

    def explorer_database_query_every_day_discovery_info_hash_number(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        every_day = {}
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        this_month_calendar = calendar.monthcalendar(year, month)
        for i in this_month_calendar:
            for j in i:
                if not j == 0:
                    every_day[str(j)] = memory.explorer_database.count_discovered_on_with_day(str(year) + '-' + str(month) + '-' + str(j).zfill(2))['result']
        result = []
        result.append({
            'title': user_language_data_config['every_day_discovery_info_hash_number'],
        })
        for i in every_day.keys():
            result.append({
                'day': i,
                'number': every_day[i]
            })
        return result

    def explorer_database_query_info_hash_contents(self, info_hash):
        database_query_info_hash_messages = memory.explorer_database.query_info_hash(info_hash)
        if database_query_info_hash_messages['result'] is False:
            return []
        else:
            result = []
            for i in database_query_info_hash_messages['result'].keys():
                torrent_name = database_query_info_hash_messages['result'][i]['torrent_name']
                for j in database_query_info_hash_messages['result'][i]['torrent_contents'].keys():
                    result.append({
                        'id': len(result) + 1,
                        'file_name': database_query_info_hash_messages['result'][i]['torrent_contents'][j]['file_name'],
                        'file_size': database_query_info_hash_messages['result'][i]['torrent_contents'][j]['file_size']
                    })
            root_directory = []
            root_directory.append({
                'id': 1,
                'pid': 0,
                'file_name': '/',
                'file_size': 0,
                'path': '/',
                'category': 'directory',
                'file_number': 0
            })
            for i in result:
                path_parts = pathlib.PurePosixPath(i['file_name']).parts
                for j in range(len(path_parts)):
                    if not path_parts[j] == '/':
                        if j < len(path_parts) - 1:
                            parent_directory = ''
                            for k in range(j):
                                parent_directory = pathlib.PurePosixPath(parent_directory, path_parts[k])
                            for l in root_directory:
                                if l['path'] == str(parent_directory):
                                    pid = l['id']
                            path = ''
                            for m in range(j + 1):
                                path = pathlib.PurePosixPath(path, path_parts[m])
                            flag = False
                            for n in root_directory:
                                if n['path'] == str(path):
                                    flag = True
                            if flag is False:
                                root_directory.append({
                                    'id': len(root_directory) + 1,
                                    'pid': pid,
                                    'file_name': path_parts[j],
                                    'file_size': 0,
                                    'path': str(path),
                                    'category': 'directory',
                                    'file_number': 0
                                })
            for i in result:
                parent_directory = str(pathlib.PurePosixPath(i['file_name']).parent)
                if parent_directory == '.':
                    for j in root_directory:
                        if j['path'] == '/':
                            pid = j['id']
                    path = '/' + i['file_name']
                    flag = False
                    for k in root_directory:
                        if k['path'] == path:
                            flag = True
                    if flag is False:
                        root_directory.append({
                            'id': len(root_directory) + 1,
                            'pid': pid,
                            'file_name': pathlib.PurePosixPath(i['file_name']).name,
                            'file_size': i['file_size'],
                            'path': path,
                            'category': 'file'
                        })
                else:
                    for j in root_directory:
                        if j['path'] == parent_directory:
                            pid = j['id']
                    path = parent_directory + '/' + pathlib.PurePosixPath(i['file_name']).name
                    flag = False
                    for k in root_directory:
                        if k['path'] == path:
                            flag = True
                    if flag is False:
                        root_directory.append({
                            'id': len(root_directory) + 1,
                            'pid': pid,
                            'file_name': pathlib.PurePosixPath(i['file_name']).name,
                            'file_size': i['file_size'],
                            'path': path,
                            'category': 'file'
                        })
            for i in root_directory:
                if i['category'] == 'file':
                    for j in pathlib.PurePosixPath(i['path']).parents:
                        for k in root_directory:
                            if k['category'] == 'directory':
                                if k['path'] == str(j):
                                    k['file_size'] = k['file_size'] + i['file_size']
            for i in root_directory:
                i['file_size'] = humanfriendly.format_size(i['file_size'], binary = True).replace('bytes', 'B')
            for i in root_directory:
                if i['category'] == 'file':
                    for j in pathlib.PurePosixPath(i['path']).parents:
                        for k in root_directory:
                            if k['category'] == 'directory':
                                if k['path'] == str(j):
                                    k['file_number'] = k['file_number'] + 1
            new_root_directory = []
            all_directory_pid_list = []
            for i in root_directory:
                if i['category'] == 'directory':
                    pid = i['pid']
                    if pid not in all_directory_pid_list:
                        all_directory_pid_list.append(pid)
            all_directory_pid_list.sort()
            for i in all_directory_pid_list:
                all_directory_file_name_list = []
                for j in root_directory:
                    if j['category'] == 'directory':
                        if i == j['pid']:
                            all_directory_file_name_list.append(j['file_name'])
                all_directory_file_name_list = natsort.natsorted(all_directory_file_name_list)
                for k in all_directory_file_name_list:
                    for l in root_directory:
                        if l['category'] == 'directory':
                            if i == l['pid']:
                                if k == l['file_name']:
                                    new_root_directory.append({
                                        'id': l['id'],
                                        'pid': l['pid'],
                                        'file_name': l['file_name'],
                                        'file_size': l['file_size'],
                                        'path': l['path'],
                                        'category': l['category'],
                                        'file_number': l['file_number']
                                    })
            all_file_pid_list = []
            for i in root_directory:
                if i['category'] == 'file':
                    pid = i['pid']
                    if pid not in all_file_pid_list:
                        all_file_pid_list.append(pid)
            all_file_pid_list.sort()
            for i in all_file_pid_list:
                all_file_file_name_list = []
                for j in root_directory:
                    if j['category'] == 'file':
                        if i == j['pid']:
                            all_file_file_name_list.append(j['file_name'])
                all_file_file_name_list = natsort.natsorted(all_file_file_name_list)
                for k in all_file_file_name_list:
                    for l in root_directory:
                        if l['category'] == 'file':
                            if i == l['pid']:
                                if k == l['file_name']:
                                    new_root_directory.append({
                                        'id': l['id'],
                                        'pid': l['pid'],
                                        'file_name': l['file_name'],
                                        'file_size': l['file_size'],
                                        'path': l['path'],
                                        'category': l['category']
                                    })
            for i in new_root_directory:
                if i['category'] == 'directory':
                    if i['path'] == '/':
                        i['file_name'] = torrent_name + '&nbsp;<span class="badge bg-secondary">' + str(i['file_number']) + '</span>'
                    else:
                        i['file_name'] = i['file_name'] + '&nbsp;<span class="badge bg-secondary">' + str(i['file_number']) + '</span>'
            for i in new_root_directory:
                if i['category'] == 'directory':
                    i['file_name'] = '<span class="text-warning"><i class="fa-solid fa-folder fa-fw"></i></span>&nbsp;' + i['file_name']
                if i['category'] == 'file':
                    i['file_name'] = '<span class="text-muted"><i class="fa-solid fa-file fa-fw"></i></span>&nbsp;' + i['file_name']
            for i in new_root_directory:
                if i['category'] == 'directory':
                    del i['file_number']
            for i in new_root_directory:
                del i['path']
                del i['category']
            return new_root_directory

    def explorer_database_query_info_hash_file_size(self):
        database_query_torrent_size_messages = memory.explorer_database.query_torrent_size()
        if database_query_torrent_size_messages['result'] is False:
            return '0 B'
        else:
            info_hash_file_size = 0
            for i in database_query_torrent_size_messages['result'].keys():
                info_hash_file_size = info_hash_file_size + database_query_torrent_size_messages['result'][i]['torrent_size']
            return humanfriendly.format_size(info_hash_file_size, binary = True).replace('bytes', 'B')

    def explorer_database_query_info_hash_information(self, info_hash, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        database_query_info_hash_messages = memory.explorer_database.query_info_hash(info_hash)
        if database_query_info_hash_messages['result'] is False:
            return []
        else:
            result = []
            for i in database_query_info_hash_messages['result'].keys():
                result.append({
                    'id': len(result) + 1,
                    'item': user_language_data_config['torrent_name'],
                    'value': database_query_info_hash_messages['result'][i]['torrent_name']
                })
                result.append({
                    'id': len(result) + 1,
                    'item': user_language_data_config['torrent_size'],
                    'value': humanfriendly.format_size(database_query_info_hash_messages['result'][i]['torrent_size'], binary = True).replace('bytes', 'B')
                })
                result.append({
                    'id': len(result) + 1,
                    'item': user_language_data_config['discovered_on'],
                    'value': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(database_query_info_hash_messages['result'][i]['discovered_on']))
                })
                result.append({
                    'id': len(result) + 1,
                    'item': user_language_data_config['magnet_uri'],
                    'value': '<div id="copy_magnet_uri_success_alert" class="alert alert-success alert-dismissible fade show text-center visually-hidden" role="alert">' +
                        '<i class="fa-solid fa-circle-check">' +
                        '</i>' +
                        '&nbsp;' +
                        user_language_data_config['copy_magnet_uri_success'] +
                        '</div>' +
                        '<div id="copy_magnet_uri_danger_alert" class="alert alert-danger alert-dismissible fade show text-center visually-hidden" role="alert">' +
                        '<i class="fa-solid fa-triangle-exclamation">' +
                        '</i>' +
                        '&nbsp;' +
                        user_language_data_config['copy_magnet_uri_failure'] +
                        '</div>' +
                        '<button id="copy_magnet_uri" data-clipboard-text="magnet:?xt=urn:btih:' +
                        database_query_info_hash_messages['result'][i]['info_hash'] +
                        '" class="btn btn-link link-dark" type="button">' +
                        user_language_data_config['copy_magnet_uri'] +
                        '</button>'
                })
            return result

    def explorer_database_query_info_hash_number(self):
        database_count_all_messages = str(memory.explorer_database.count_all())
        return database_count_all_messages

    def explorer_database_query_insert(self, torrent_file, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        if torrent_file.filename.endswith('.torrent') is True:
            try:
                torrent_file_data = torrent_file.read()
                torrent_file_data = pyben.loads(torrent_file_data)
                torrent_information_parser_messages = memory.explorer_spider.torrent_parser(torrent_file_data)
                if torrent_information_parser_messages is not False:
                    info_hash = torrent_information_parser_messages[0]
                    torrent_name = torrent_information_parser_messages[1]
                    torrent_contents = torrent_information_parser_messages[2]
                    torrent_size = torrent_information_parser_messages[3]
                    database_count_info_hash_messages = memory.explorer_database.count_info_hash(info_hash)
                    if database_count_info_hash_messages['result'] == 0:
                        database_insert_messages = memory.explorer_database.insert(info_hash, torrent_name, torrent_contents, torrent_size)
                        if database_insert_messages['result'] is True:
                            return True
                        else:
                            return False, user_language_data_config['upload_failure_1']
                    else:
                        return False, user_language_data_config['upload_failure_1']
                else:
                    return False, user_language_data_config['upload_failure_2']
            except:
                return False, user_language_data_config['upload_failure_2']
        else:
            return False, user_language_data_config['upload_failure_2']

    def explorer_database_query_like(self, keyword):
        explorer_web_server_data_conversion_explorer_spider_get_info_hash_thread = threading.Thread(target = self.explorer_spider_get_info_hash, args = (keyword,))
        explorer_web_server_data_conversion_explorer_spider_get_info_hash_thread.setDaemon(True)
        explorer_web_server_data_conversion_explorer_spider_get_info_hash_thread.start()
        database_query_like_messages = memory.explorer_database.query_like(keyword)
        if database_query_like_messages['result'] is False:
            return []
        else:
            result = []
            for i in database_query_like_messages['result'].keys():
                result.append({
                    'id': len(database_query_like_messages['result']) - int(i),
                    'torrent_name': '<a href="./report?info_hash=' +
                        database_query_like_messages['result'][i]['info_hash'] +
                        '" class="link-dark">' +
                        database_query_like_messages['result'][i]['torrent_name'] +
                        '</a>',
                    'torrent_size': humanfriendly.format_size(database_query_like_messages['result'][i]['torrent_size'], binary = True).replace('bytes', 'B')
                })
            result.reverse()
            return result

    def explorer_database_query_monthly_discovery_info_hash_number(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        now_time = datetime.datetime.now()
        month = {}
        for i in range(1, 13):
            month[str(now_time.year) + '-' + str(i)] = memory.explorer_database.count_discovered_on_with_month(str(now_time.year) + '-' + str(i).zfill(2))['result']
        result = []
        result.append({
            'title': user_language_data_config['monthly_discovery_info_hash_number'],
        })
        for i in month.keys():
            result.append({
                'month': i.split('-')[1],
                'number': month[i]
            })
        return result

    def explorer_krpc_v4_parameter_read(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        krpc_v4_all_parameter_messages = {}
        krpc_v4_self_node_id_messages = memory.explorer_krpc_v4.self_node_id()
        krpc_v4_self_ip_address_messages = memory.explorer_krpc_v4.self_ip_address()
        krpc_v4_self_udp_port_messages = memory.explorer_krpc_v4.self_udp_port()
        krpc_v4_query_nodes_number_messages = memory.explorer_krpc_v4.query_nodes_number()
        spider_ipv4_network_connectivity_messages = memory.explorer_spider.ipv4_network_connectivity()
        krpc_v4_all_parameter_messages[user_language_data_config['node_id']] = krpc_v4_self_node_id_messages
        krpc_v4_all_parameter_messages[user_language_data_config['ip_address']] = krpc_v4_self_ip_address_messages
        krpc_v4_all_parameter_messages[user_language_data_config['udp_port']] = krpc_v4_self_udp_port_messages
        krpc_v4_all_parameter_messages[user_language_data_config['nodes_number']] = krpc_v4_query_nodes_number_messages
        if spider_ipv4_network_connectivity_messages is True:
            krpc_v4_all_parameter_messages[user_language_data_config['network_connectivity']] = '<div class="text-success"><i class="fa-solid fa-circle-check"></i></div>'
        if spider_ipv4_network_connectivity_messages is False:
            krpc_v4_all_parameter_messages[user_language_data_config['network_connectivity']] = '<div class="text-danger"><i class="fa-solid fa-circle-xmark"></i></div>'
        result = []
        for i in krpc_v4_all_parameter_messages.keys():
            result.append({
                'id': len(result) + 1,
                'item': i,
                'value': krpc_v4_all_parameter_messages[i]
            })
        return result

    def explorer_krpc_v4_peer_database_read(self):
        krpc_v4_query_announce_info_hashes_messages = memory.explorer_krpc_v4.query_announce_info_hashes()
        result = []
        for i in krpc_v4_query_announce_info_hashes_messages.keys():
            for j in krpc_v4_query_announce_info_hashes_messages[i]:
                if j[2] + 14400 - int(time.time()) > 0:
                    j[2] = time.strftime('%H:%M:%S', time.gmtime(j[2] + 14400 - int(time.time())))
                else:
                    j[2] = '00:00:00'
                result.append({
                    'info_hash': i,
                    'ip_address': j[0] + ':' + str(j[1]),
                    'update_time': '<span class="badge bg-secondary">' + j[2] + '</span>'
                })
        return result

    def explorer_krpc_v4_ping(self, ip_address, udp_port):
        ip_address_type = IPy.IP(ip_address).iptype()
        if ip_address_type == 'PUBLIC':
            if 1 <= udp_port <= 65535:
                result = memory.explorer_krpc_v4.ping(ip_address, udp_port)['result']
                return result
            else:
                return False
        else:
            return False

    def explorer_krpc_v4_router_table_read(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        krpc_v4_query_nodes_messages = memory.explorer_krpc_v4.query_nodes()
        result = []
        for i in range(0, 160):
            for j in range(0, 8):
                if krpc_v4_query_nodes_messages[str(i)][str(j)]['ip_address'] == '':
                    del krpc_v4_query_nodes_messages[str(i)][str(j)]
        for i in range(0, 160):
            if len(krpc_v4_query_nodes_messages[str(i)]) == 0:
                del krpc_v4_query_nodes_messages[str(i)]
        for i in krpc_v4_query_nodes_messages:
            for j in krpc_v4_query_nodes_messages[str(i)]:
                if krpc_v4_query_nodes_messages[str(i)][str(j)]['update_time'] + 900 - int(time.time()) > 0:
                    krpc_v4_query_nodes_messages[str(i)][str(j)]['update_time'] = time.strftime('%M:%S', time.gmtime(krpc_v4_query_nodes_messages[str(i)][str(j)]['update_time'] + 900 - int(time.time())))
                else:
                    krpc_v4_query_nodes_messages[str(i)][str(j)]['update_time'] = '00:00'
        result.append({
            'k_bucket': '<span class="text-muted"><i class="fa-solid fa-bucket fa-fw"></i></span>&nbsp;' + user_language_data_config['k_bucket']
        })
        result.append(krpc_v4_query_nodes_messages)
        return result

    def explorer_krpc_v6_parameter_read(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        krpc_v6_all_parameter_messages = {}
        krpc_v6_self_node_id_messages = memory.explorer_krpc_v6.self_node_id()
        krpc_v6_self_ip_address_messages = memory.explorer_krpc_v6.self_ip_address()
        krpc_v6_self_udp_port_messages = memory.explorer_krpc_v6.self_udp_port()
        krpc_v6_query_nodes_number_messages = memory.explorer_krpc_v6.query_nodes_number()
        spider_ipv6_network_connectivity_messages = memory.explorer_spider.ipv6_network_connectivity()
        krpc_v6_all_parameter_messages[user_language_data_config['node_id']] = krpc_v6_self_node_id_messages
        krpc_v6_all_parameter_messages[user_language_data_config['ip_address']] = krpc_v6_self_ip_address_messages
        krpc_v6_all_parameter_messages[user_language_data_config['udp_port']] = krpc_v6_self_udp_port_messages
        krpc_v6_all_parameter_messages[user_language_data_config['nodes_number']] = krpc_v6_query_nodes_number_messages
        if spider_ipv6_network_connectivity_messages is True:
            krpc_v6_all_parameter_messages[user_language_data_config['network_connectivity']] = '<div class="text-success"><i class="fa-solid fa-circle-check"></i></div>'
        if spider_ipv6_network_connectivity_messages is False:
            krpc_v6_all_parameter_messages[user_language_data_config['network_connectivity']] = '<div class="text-danger"><i class="fa-solid fa-circle-xmark"></i></div>'
        result = []
        for i in krpc_v6_all_parameter_messages.keys():
            result.append({
                'id': len(result) + 1,
                'item': i,
                'value': krpc_v6_all_parameter_messages[i]
            })
        return result

    def explorer_krpc_v6_peer_database_read(self):
        krpc_v6_query_announce_info_hashes_messages = memory.explorer_krpc_v6.query_announce_info_hashes()
        result = []
        for i in krpc_v6_query_announce_info_hashes_messages.keys():
            for j in krpc_v6_query_announce_info_hashes_messages[i]:
                if j[2] + 14400 - int(time.time()) > 0:
                    j[2] = time.strftime('%H:%M:%S', time.gmtime(j[2] + 14400 - int(time.time())))
                else:
                    j[2] = '00:00:00'
                result.append({
                    'info_hash': i,
                    'ip_address': '[' + j[0] + ']:' + str(j[1]),
                    'update_time': '<span class="badge bg-secondary">' + j[2] + '</span>'
                })
        return result

    def explorer_krpc_v6_ping(self, ip_address, udp_port):
        ip_address_type = IPy.IP(ip_address).iptype()[:9]
        if ip_address_type == 'ALLOCATED':
            if 1 <= udp_port <= 65535:
                result = memory.explorer_krpc_v6.ping(ip_address, udp_port)['result']
                return result
            else:
                return False
        else:
            return False

    def explorer_krpc_v6_router_table_read(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        krpc_v6_query_nodes_messages = memory.explorer_krpc_v6.query_nodes()
        result = []
        for i in range(0, 160):
            for j in range(0, 8):
                if krpc_v6_query_nodes_messages[str(i)][str(j)]['ip_address'] == '':
                    del krpc_v6_query_nodes_messages[str(i)][str(j)]
        for i in range(0, 160):
            if len(krpc_v6_query_nodes_messages[str(i)]) == 0:
                del krpc_v6_query_nodes_messages[str(i)]
        for i in krpc_v6_query_nodes_messages:
            for j in krpc_v6_query_nodes_messages[str(i)]:
                if krpc_v6_query_nodes_messages[str(i)][str(j)]['update_time'] + 900 - int(time.time()) > 0:
                    krpc_v6_query_nodes_messages[str(i)][str(j)]['update_time'] = time.strftime('%M:%S', time.gmtime(krpc_v6_query_nodes_messages[str(i)][str(j)]['update_time'] + 900 - int(time.time())))
                else:
                    krpc_v6_query_nodes_messages[str(i)][str(j)]['update_time'] = '00:00'
        result.append({
            'k_bucket': '<span class="text-muted"><i class="fa-solid fa-bucket fa-fw"></i></span>&nbsp;' + user_language_data_config['k_bucket']
        })
        result.append(krpc_v6_query_nodes_messages)
        return result

    def explorer_peer_wire_v4_ut_metadata_progress_table_read(self):
        peer_wire_v4_ut_metadata_progress_messages = memory.explorer_peer_wire_v4.ut_metadata_progress()
        result = []
        for i in peer_wire_v4_ut_metadata_progress_messages.keys():
            if peer_wire_v4_ut_metadata_progress_messages[i]['status'] is True:
                database_count_info_hash_messages = memory.explorer_database.count_info_hash(peer_wire_v4_ut_metadata_progress_messages[i]['info_hash'])
                if database_count_info_hash_messages['result'] == 0:
                    result.append({
                        'status': '<div class="text-warning"><i class="fa-solid fa-file-circle-xmark"></i></div>',
                        'info_hash': peer_wire_v4_ut_metadata_progress_messages[i]['info_hash'],
                        'ip_address': peer_wire_v4_ut_metadata_progress_messages[i]['ip_address'] + ':' + str(peer_wire_v4_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v4_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v4_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
                if database_count_info_hash_messages['result'] == 1:
                    result.append({
                        'status': '<div class="text-success"><i class="fa-solid fa-file-circle-check"></i></div>',
                        'info_hash': '<a href="./report?info_hash=' + peer_wire_v4_ut_metadata_progress_messages[i]['info_hash'] + '" class="link-dark">' + peer_wire_v4_ut_metadata_progress_messages[i]['info_hash'] + '</a>',
                        'ip_address': peer_wire_v4_ut_metadata_progress_messages[i]['ip_address'] + ':' + str(peer_wire_v4_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v4_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v4_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
            if peer_wire_v4_ut_metadata_progress_messages[i]['status'] is False:
                if '{:.2%}'.format(peer_wire_v4_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v4_ut_metadata_progress_messages[i]['all_piece_number']) == '100.00%':
                    result.append({
                        'status': '<div class="text-danger"><i class="fa-solid fa-file-circle-question"></i></div>',
                        'info_hash': peer_wire_v4_ut_metadata_progress_messages[i]['info_hash'],
                        'ip_address': peer_wire_v4_ut_metadata_progress_messages[i]['ip_address'] + ':' + str(peer_wire_v4_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v4_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v4_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
                else:
                    result.append({
                        'status': '<div class="text-primary"><i class="fa-solid fa-file-arrow-down"></i></div>',
                        'info_hash': peer_wire_v4_ut_metadata_progress_messages[i]['info_hash'],
                        'ip_address': peer_wire_v4_ut_metadata_progress_messages[i]['ip_address'] + ':' + str(peer_wire_v4_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v4_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v4_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
        result.reverse()
        return result

    def explorer_peer_wire_v6_ut_metadata_progress_table_read(self):
        peer_wire_v6_ut_metadata_progress_messages = memory.explorer_peer_wire_v6.ut_metadata_progress()
        result = []
        for i in peer_wire_v6_ut_metadata_progress_messages.keys():
            if peer_wire_v6_ut_metadata_progress_messages[i]['status'] is True:
                database_count_info_hash_messages = memory.explorer_database.count_info_hash(peer_wire_v6_ut_metadata_progress_messages[i]['info_hash'])
                if database_count_info_hash_messages['result'] == 0:
                    result.append({
                        'status': '<div class="text-warning"><i class="fa-solid fa-file-circle-xmark"></i></div>',
                        'info_hash': peer_wire_v6_ut_metadata_progress_messages[i]['info_hash'],
                        'ip_address': '[' + peer_wire_v6_ut_metadata_progress_messages[i]['ip_address'] + ']:' + str(peer_wire_v6_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v6_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v6_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
                if database_count_info_hash_messages['result'] == 1:
                    result.append({
                        'status': '<div class="text-success"><i class="fa-solid fa-file-circle-check"></i></div>',
                        'info_hash': '<a href="./report?info_hash=' + peer_wire_v6_ut_metadata_progress_messages[i]['info_hash'] + '" class="link-dark">' + peer_wire_v6_ut_metadata_progress_messages[i]['info_hash'] + '</a>',
                        'ip_address': '[' + peer_wire_v6_ut_metadata_progress_messages[i]['ip_address'] + ']:' + str(peer_wire_v6_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v6_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v6_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
            if peer_wire_v6_ut_metadata_progress_messages[i]['status'] is False:
                if '{:.2%}'.format(peer_wire_v6_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v6_ut_metadata_progress_messages[i]['all_piece_number']) == '100.00%':
                    result.append({
                        'status': '<div class="text-danger"><i class="fa-solid fa-file-circle-question"></i></div>',
                        'info_hash': peer_wire_v6_ut_metadata_progress_messages[i]['info_hash'],
                        'ip_address': '[' + peer_wire_v6_ut_metadata_progress_messages[i]['ip_address'] + ']:' + str(peer_wire_v6_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v6_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v6_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
                else:
                    result.append({
                        'status': '<div class="text-primary"><i class="fa-solid fa-file-arrow-down"></i></div>',
                        'info_hash': peer_wire_v6_ut_metadata_progress_messages[i]['info_hash'],
                        'ip_address': '[' + peer_wire_v6_ut_metadata_progress_messages[i]['ip_address'] + ']:' + str(peer_wire_v6_ut_metadata_progress_messages[i]['tcp_port']),
                        'progress': '{:.2%}'.format(peer_wire_v6_ut_metadata_progress_messages[i]['load_piece_number'] / peer_wire_v6_ut_metadata_progress_messages[i]['all_piece_number'])
                    })
        result.reverse()
        return result

    def explorer_spider_get_info_hash(self, keyword):
        result = memory.explorer_spider.get_info_hash(keyword)
        for i in result:
            memory.explorer_spider.add_info_hash(i)

    def setting_database_config_json_read(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/explorer_database/database_config.json', mode = 'r', encoding = 'utf-8') as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            database_config_json_schema = {
                'title': 'database_config.json',
                'type': 'object',
                'required': [
                    'default_database',
                    'mysql'
                ],
                'properties': {
                    'default_database': {
                        'type': 'string',
                        'description': user_language_data_config['database_application_name'],
                        'minLength': 1,
                        'default': file_data['default_database']
                    },
                    'mysql': {
                        'type': 'object',
                        'title': 'mysql',
                        'properties': {
                            'database' : {
                                'type': 'string',
                                'description': user_language_data_config['database_name'],
                                'minLength': 1,
                                'default': file_data['mysql']['database']
                            },
                            'host' : {
                                'type': 'string',
                                'description': user_language_data_config['database_application_ipv4_or_ipv6_address'],
                                'minLength': 1,
                                'default': file_data['mysql']['host']
                            },
                            'password' : {
                                'type': 'string',
                                'description': user_language_data_config['database_application_user_password'],
                                'minLength': 1,
                                'default': file_data['mysql']['password']
                            },
                            'port': {
                                'type': 'integer',
                                'description': user_language_data_config['database_application_port'],
                                'minLength': 1,
                                'default': file_data['mysql']['port']
                            },
                            'user': {
                                'type': 'string',
                                'description': user_language_data_config['database_application_user_name'],
                                'minLength': 1,
                                'default': file_data['mysql']['user']
                            }
                        }
                    }
                }
            }
            return database_config_json_schema

    def setting_database_config_json_write(self, file_data):
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/explorer_database/database_config.json', mode = 'w', encoding = 'utf-8') as file:
            file.write(json.dumps(file_data, indent = 4, ensure_ascii = False))
        return ''

    def setting_save_torrent_files_folder_config_json_read(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/explorer_spider/save_torrent_files_folder_config.json', mode = 'r', encoding = 'utf-8') as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            save_torrent_files_folder_config_json_schema = {
                'title': 'save_torrent_files_folder_config.json',
                'type': 'object',
                'required': [
                    'save_torrent_files_folder_path',
                    'save_torrent_files_name_with_info_hash',
                    'save_torrent_files_name_with_torrent_name'
                ],
                'properties': {
                    'save_torrent_files_folder_path': {
                        'type': 'string',
                        'description': user_language_data_config['save_torrent_files_folder_path'],
                        'minLength': 0,
                        'default': file_data['save_torrent_files_folder_path']
                    },
                    'save_torrent_files_name_with_info_hash': {
                        'type': 'boolean',
                        'description': user_language_data_config['save_torrent_with_infohash'],
                        'minLength': 1,
                        'default': file_data['save_torrent_files_name_with_info_hash']
                    },
                    'save_torrent_files_name_with_torrent_name': {
                        'type': 'boolean',
                        'description': user_language_data_config['save_torrent_with_torrent_name'],
                        'minLength': 1,
                        'default': file_data['save_torrent_files_name_with_torrent_name']
                    }
                }
            }
            return save_torrent_files_folder_config_json_schema

    def setting_save_torrent_files_folder_config_json_write(self, file_data):
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/explorer_spider/save_torrent_files_folder_config.json', mode = 'w', encoding = 'utf-8') as file:
            file.write(json.dumps(file_data, indent = 4, ensure_ascii = False))
        return ''

    def setting_tracker_list_config_json_read(self, user_language):
        user_language_data_config = self.__get_user_language_config(user_language)
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/explorer_spider/tracker_list_config.json', mode = 'r', encoding = 'utf-8') as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            tracker_list_config_json_schema = {
                'title': 'tracker_list_config.json',
                'type': 'object',
                'required': [
                    'http_tracker_list',
                    'udp_tracker_list'
                ],
                'properties': {
                    'http_tracker_list': {
                        'type': 'object',
                        'title': 'http_tracker_list',
                        'properties': {
                            '0': {
                                'type': 'string',
                                'description': user_language_data_config['http_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['http_tracker_list']['0']
                            },
                            '1': {
                                'type': 'string',
                                'description': user_language_data_config['http_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['http_tracker_list']['1']
                            },
                            '2': {
                                'type': 'string',
                                'description': user_language_data_config['http_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['http_tracker_list']['2']
                            },
                            '3': {
                                'type': 'string',
                                'description': user_language_data_config['http_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['http_tracker_list']['3']
                            }
                        }
                    },
                    'udp_tracker_list': {
                        'type': 'object',
                        'title': 'udp_tracker_list',
                        'properties': {
                            '0': {
                                'type': 'string',
                                'description': user_language_data_config['udp_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['udp_tracker_list']['0']
                            },
                            '1': {
                                'type': 'string',
                                'description': user_language_data_config['udp_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['udp_tracker_list']['1']
                            },
                            '2': {
                                'type': 'string',
                                'description': user_language_data_config['udp_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['udp_tracker_list']['2']
                            },
                            '3': {
                                'type': 'string',
                                'description': user_language_data_config['udp_tracker_api_url'],
                                'minLength': 1,
                                'default': file_data['udp_tracker_list']['3']
                            }
                        }
                    }
                }
            }
            return tracker_list_config_json_schema

    def setting_tracker_list_config_json_write(self, file_data):
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/explorer_spider/tracker_list_config.json', mode = 'w', encoding = 'utf-8') as file:
            file.write(json.dumps(file_data, indent = 4, ensure_ascii = False))
        return ''