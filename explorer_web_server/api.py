from .cache import application_cache
from .data_converter import data_conversion
from .memory import memory
import flask
import flask_restful
import webview

api_blueprint = flask.Blueprint('api', __name__)
api = flask_restful.Api(api_blueprint)

class api_database_check(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_database_check()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_discovery_of_the_day_data(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_database_query_discovery_of_the_day_data()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_discovery_of_the_day_number(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_database_query_discovery_of_the_day_number(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_every_day_discovery_info_hash_number(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_database_query_every_day_discovery_info_hash_number(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_info_hash_contents(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                info_hash = flask.request.args.get('info_hash')
                result = data_conversion().explorer_database_query_info_hash_contents(info_hash)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_info_hash_file_size(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_database_query_info_hash_file_size()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_info_hash_information(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                info_hash = flask.request.args.get('info_hash')
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_database_query_info_hash_information(info_hash, user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_info_hash_number(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_database_query_info_hash_number()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_insert(flask_restful.Resource):
    def post(self):
        torrent_file = flask.request.files.get('torrent_data')
        token = flask.request.form.get('token')
        if token is not None:
            if token == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_database_query_insert(torrent_file, user_language)
                if result is True:
                    return {}
                else:
                    return {
                        'error': result[1]
                    }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_like(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                like_string = flask.request.args.get('like_string')
                result = data_conversion().explorer_database_query_like(like_string)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_database_query_monthly_discovery_info_hash_number(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_database_query_monthly_discovery_info_hash_number(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v4_parameter_read(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_krpc_v4_parameter_read(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v4_peer_database_read(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_krpc_v4_peer_database_read()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v4_ping(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                if 'ip_address' in json_data:
                    if 'udp_port' in json_data:
                        ip_address = json_data['ip_address']
                        udp_port = int(json_data['udp_port'])
                        result = data_conversion().explorer_krpc_v4_ping(ip_address, udp_port)
                        return {
                            'data': result
                        }
                    else:
                        return {
                            'data': False
                        }
                else:
                    return {
                        'data': False
                    }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v4_router_table_read(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_krpc_v4_router_table_read(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v6_parameter_read(flask_restful.Resource):
    @application_cache.cached()
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_krpc_v6_parameter_read(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v6_peer_database_read(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_krpc_v6_peer_database_read()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v6_ping(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                if 'ip_address' in json_data:
                    if 'udp_port' in json_data:
                        ip_address = json_data['ip_address']
                        udp_port = int(json_data['udp_port'])
                        result = data_conversion().explorer_krpc_v6_ping(ip_address, udp_port)
                        return {
                            'data': result
                        }
                    else:
                        return {
                            'data': False
                        }
                else:
                    return {
                        'data': False
                    }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_krpc_v6_router_table_read(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().explorer_krpc_v6_router_table_read(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_peer_wire_v4_ut_metadata_progress_table_read(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_peer_wire_v4_ut_metadata_progress_table_read()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_peer_wire_v6_ut_metadata_progress_table_read(flask_restful.Resource):
    @application_cache.cached(timeout = 2)
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                result = data_conversion().explorer_peer_wire_v6_ut_metadata_progress_table_read()
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_setting_database_config_json_read(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().setting_database_config_json_read(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_setting_database_config_json_write(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                file_data = json_data['file_data']
                result = data_conversion().setting_database_config_json_write(file_data)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_setting_save_torrent_files_folder_config_json_read(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().setting_save_torrent_files_folder_config_json_read(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_setting_save_torrent_files_folder_config_json_write(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                file_data = json_data['file_data']
                result = data_conversion().setting_save_torrent_files_folder_config_json_write(file_data)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_setting_tracker_list_config_json_read(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
                result = data_conversion().setting_tracker_list_config_json_read(user_language)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

class api_setting_tracker_list_config_json_write(flask_restful.Resource):
    def post(self):
        json_data = flask.request.get_json()
        if 'token' in json_data:
            if json_data['token'] == webview.token:
                file_data = json_data['file_data']
                result = data_conversion().setting_tracker_list_config_json_write(file_data)
                return {
                    'data': result
                }
            else:
                return {
                    'error': 'Authentication error'
                }
        else:
            return {
                'error': 'Authentication error'
            }

api.add_resource(api_database_check, '/api_database_check')
api.add_resource(api_database_query_discovery_of_the_day_data, '/api_database_query_discovery_of_the_day_data')
api.add_resource(api_database_query_discovery_of_the_day_number, '/api_database_query_discovery_of_the_day_number')
api.add_resource(api_database_query_every_day_discovery_info_hash_number, '/api_database_query_every_day_discovery_info_hash_number')
api.add_resource(api_database_query_info_hash_contents, '/api_database_query_info_hash_contents')
api.add_resource(api_database_query_info_hash_file_size, '/api_database_query_info_hash_file_size')
api.add_resource(api_database_query_info_hash_information, '/api_database_query_info_hash_information')
api.add_resource(api_database_query_info_hash_number, '/api_database_query_info_hash_number')
api.add_resource(api_database_query_insert, '/api_database_query_insert')
api.add_resource(api_database_query_like, '/api_database_query_like')
api.add_resource(api_database_query_monthly_discovery_info_hash_number, '/api_database_query_monthly_discovery_info_hash_number')
api.add_resource(api_krpc_v4_parameter_read, '/api_krpc_v4_parameter_read')
api.add_resource(api_krpc_v4_peer_database_read, '/api_krpc_v4_peer_database_read')
api.add_resource(api_krpc_v4_ping, '/api_krpc_v4_ping')
api.add_resource(api_krpc_v4_router_table_read, '/api_krpc_v4_router_table_read')
api.add_resource(api_krpc_v6_parameter_read, '/api_krpc_v6_parameter_read')
api.add_resource(api_krpc_v6_peer_database_read, '/api_krpc_v6_peer_database_read')
api.add_resource(api_krpc_v6_ping, '/api_krpc_v6_ping')
api.add_resource(api_krpc_v6_router_table_read, '/api_krpc_v6_router_table_read')
api.add_resource(api_peer_wire_v4_ut_metadata_progress_table_read, '/api_peer_wire_v4_ut_metadata_progress_table_read')
api.add_resource(api_peer_wire_v6_ut_metadata_progress_table_read, '/api_peer_wire_v6_ut_metadata_progress_table_read')
api.add_resource(api_setting_database_config_json_read, '/api_setting_database_config_json_read')
api.add_resource(api_setting_database_config_json_write, '/api_setting_database_config_json_write')
api.add_resource(api_setting_save_torrent_files_folder_config_json_read, '/api_setting_save_torrent_files_folder_config_json_read')
api.add_resource(api_setting_save_torrent_files_folder_config_json_write, '/api_setting_save_torrent_files_folder_config_json_write')
api.add_resource(api_setting_tracker_list_config_json_read, '/api_setting_tracker_list_config_json_read')
api.add_resource(api_setting_tracker_list_config_json_write, '/api_setting_tracker_list_config_json_write')