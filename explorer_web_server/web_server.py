from .api import api_blueprint
from .cache import application_cache
from .data_converter import data_conversion
from .memory import memory
import flask
import json
import os
import re
import validators
import webview

application = flask.Flask(
    __name__,
    static_folder = os.path.dirname(os.path.abspath(__file__)) + '/static',
    template_folder = os.path.dirname(os.path.abspath(__file__)) + '/templates'
)
application_cache.init_app(application)
application.register_blueprint(api_blueprint)

@application.route('/about', methods = ['GET'])
@application_cache.cached()
def about():
    result = data_conversion().explorer_database_check()
    if result is True:
        user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
        if user_language is None:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'about.html',
                    about = user_language_data_config['about'],
                    application_information = user_language_data_config['application_information'],
                    author_name = user_language_data_config['author_name'],
                    back = user_language_data_config['back'],
                    copyright = user_language_data_config['copyright'],
                    database = user_language_data_config['database'],
                    id = user_language_data_config['id'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    license = user_language_data_config['license'],
                    network = user_language_data_config['network'],
                    notice = user_language_data_config['notice'],
                    open_source_project = user_language_data_config['open_source_project'],
                    open_source_project_thanks_information = user_language_data_config['open_source_project_thanks_information'],
                    protocol_name = user_language_data_config['protocol_name'],
                    protocol_number = user_language_data_config['protocol_number'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    source_code = user_language_data_config['source_code'],
                    source_code_url = user_language_data_config['source_code_url'],
                    spider = user_language_data_config['spider'],
                    supported_protocols_information = user_language_data_config['supported_protocols_information'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value'],
                    version = user_language_data_config['version']
                )
        elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'about.html',
                    about = user_language_data_config['about'],
                    application_information = user_language_data_config['application_information'],
                    author_name = user_language_data_config['author_name'],
                    back = user_language_data_config['back'],
                    copyright = user_language_data_config['copyright'],
                    database = user_language_data_config['database'],
                    id = user_language_data_config['id'],
                    item = user_language_data_config['item'],
                    language = user_language,
                    license = user_language_data_config['license'],
                    network = user_language_data_config['network'],
                    notice = user_language_data_config['notice'],
                    open_source_project = user_language_data_config['open_source_project'],
                    open_source_project_thanks_information = user_language_data_config['open_source_project_thanks_information'],
                    protocol_name = user_language_data_config['protocol_name'],
                    protocol_number = user_language_data_config['protocol_number'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    source_code = user_language_data_config['source_code'],
                    source_code_url = user_language_data_config['source_code_url'],
                    spider = user_language_data_config['spider'],
                    supported_protocols_information = user_language_data_config['supported_protocols_information'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value'],
                    version = user_language_data_config['version']
                )
        else:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'about.html',
                    about = user_language_data_config['about'],
                    application_information = user_language_data_config['application_information'],
                    author_name = user_language_data_config['author_name'],
                    back = user_language_data_config['back'],
                    copyright = user_language_data_config['copyright'],
                    database = user_language_data_config['database'],
                    id = user_language_data_config['id'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    license = user_language_data_config['license'],
                    network = user_language_data_config['network'],
                    notice = user_language_data_config['notice'],
                    open_source_project = user_language_data_config['open_source_project'],
                    open_source_project_thanks_information = user_language_data_config['open_source_project_thanks_information'],
                    protocol_name = user_language_data_config['protocol_name'],
                    protocol_number = user_language_data_config['protocol_number'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    source_code = user_language_data_config['source_code'],
                    source_code_url = user_language_data_config['source_code_url'],
                    spider = user_language_data_config['spider'],
                    supported_protocols_information = user_language_data_config['supported_protocols_information'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value'],
                    version = user_language_data_config['version']
                )
    else:
        return flask.redirect(flask.url_for('setting'))

@application.route('/database', methods = ['GET'])
@application_cache.cached()
def database():
    result = data_conversion().explorer_database_check()
    if result is True:
        user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
        if user_language is None:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'database.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    discovery_of_the_day_data = user_language_data_config['discovery_of_the_day_data'],
                    discovery_of_the_day_number = user_language_data_config['discovery_of_the_day_number'],
                    id = user_language_data_config['id'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    torrent_name = user_language_data_config['torrent_name'],
                    torrent_size = user_language_data_config['torrent_size'],
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
        elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'database.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    discovery_of_the_day_data = user_language_data_config['discovery_of_the_day_data'],
                    discovery_of_the_day_number = user_language_data_config['discovery_of_the_day_number'],
                    id = user_language_data_config['id'],
                    item = user_language_data_config['item'],
                    language = user_language,
                    network = user_language_data_config['network'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    torrent_name = user_language_data_config['torrent_name'],
                    torrent_size = user_language_data_config['torrent_size'],
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
        else:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'database.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    discovery_of_the_day_data = user_language_data_config['discovery_of_the_day_data'],
                    discovery_of_the_day_number = user_language_data_config['discovery_of_the_day_number'],
                    id = user_language_data_config['id'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    torrent_name = user_language_data_config['torrent_name'],
                    torrent_size = user_language_data_config['torrent_size'],
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
    else:
        return flask.redirect(flask.url_for('setting'))

@application.route('/default', methods = ['GET'])
@application_cache.cached()
def default():
    result = data_conversion().explorer_database_check()
    if result is True:
        user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
        if user_language is None:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'default.html',
                    about = user_language_data_config['about'],
                    card_subtitle_1 = user_language_data_config['card_subtitle_1'],
                    card_subtitle_2 = user_language_data_config['card_subtitle_2'],
                    database = user_language_data_config['database'],
                    file_size = user_language_data_config['file_size'],
                    info_hash = user_language_data_config['info_hash'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button']
                )
        elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'default.html',
                    about = user_language_data_config['about'],
                    card_subtitle_1 = user_language_data_config['card_subtitle_1'],
                    card_subtitle_2 = user_language_data_config['card_subtitle_2'],
                    database = user_language_data_config['database'],
                    file_size = user_language_data_config['file_size'],
                    info_hash = user_language_data_config['info_hash'],
                    language = user_language,
                    network = user_language_data_config['network'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button']
                )
        else:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'default.html',
                    about = user_language_data_config['about'],
                    card_subtitle_1 = user_language_data_config['card_subtitle_1'],
                    card_subtitle_2 = user_language_data_config['card_subtitle_2'],
                    database = user_language_data_config['database'],
                    file_size = user_language_data_config['file_size'],
                    info_hash = user_language_data_config['info_hash'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button']
                )
    else:
        return flask.redirect(flask.url_for('setting'))

@application.route('/', methods = ['GET'])
@application_cache.cached()
def main():
    return flask.redirect(flask.url_for('default'), code = 301)

@application.route('/network', methods = ['GET'])
@application_cache.cached()
def network():
    result = data_conversion().explorer_database_check()
    if result is True:
        user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
        if user_language is None:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'network.html',
                    about = user_language_data_config['about'],
                    append_bootstrap_nodes = user_language_data_config['append_bootstrap_nodes'],
                    append_bootstrap_nodes_failure = user_language_data_config['append_bootstrap_nodes_failure'],
                    append_bootstrap_nodes_success = user_language_data_config['append_bootstrap_nodes_success'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    dht_network_ipv4_information = user_language_data_config['dht_network_ipv4_information'],
                    dht_network_ipv4_peer_database = user_language_data_config['dht_network_ipv4_peer_database'],
                    dht_network_ipv4_router_table = user_language_data_config['dht_network_ipv4_router_table'],
                    dht_network_ipv6_information = user_language_data_config['dht_network_ipv6_information'],
                    dht_network_ipv6_peer_database = user_language_data_config['dht_network_ipv6_peer_database'],
                    dht_network_ipv6_router_table = user_language_data_config['dht_network_ipv6_router_table'],
                    id = user_language_data_config['id'],
                    info_hash = user_language_data_config['info_hash'],
                    ip_address = user_language_data_config['ip_address'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    node_id = user_language_data_config['node_id'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    udp_port = user_language_data_config['udp_port'],
                    update_time = user_language_data_config['update_time'],
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
        elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'network.html',
                    about = user_language_data_config['about'],
                    append_bootstrap_nodes = user_language_data_config['append_bootstrap_nodes'],
                    append_bootstrap_nodes_failure = user_language_data_config['append_bootstrap_nodes_failure'],
                    append_bootstrap_nodes_success = user_language_data_config['append_bootstrap_nodes_success'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    dht_network_ipv4_information = user_language_data_config['dht_network_ipv4_information'],
                    dht_network_ipv4_peer_database = user_language_data_config['dht_network_ipv4_peer_database'],
                    dht_network_ipv4_router_table = user_language_data_config['dht_network_ipv4_router_table'],
                    dht_network_ipv6_information = user_language_data_config['dht_network_ipv6_information'],
                    dht_network_ipv6_peer_database = user_language_data_config['dht_network_ipv6_peer_database'],
                    dht_network_ipv6_router_table = user_language_data_config['dht_network_ipv6_router_table'],
                    id = user_language_data_config['id'],
                    info_hash = user_language_data_config['info_hash'],
                    ip_address = user_language_data_config['ip_address'],
                    item = user_language_data_config['item'],
                    language = user_language,
                    network = user_language_data_config['network'],
                    node_id = user_language_data_config['node_id'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    udp_port = user_language_data_config['udp_port'],
                    update_time = user_language_data_config['update_time'],
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
        else:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'network.html',
                    about = user_language_data_config['about'],
                    append_bootstrap_nodes = user_language_data_config['append_bootstrap_nodes'],
                    append_bootstrap_nodes_failure = user_language_data_config['append_bootstrap_nodes_failure'],
                    append_bootstrap_nodes_success = user_language_data_config['append_bootstrap_nodes_success'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    dht_network_ipv4_information = user_language_data_config['dht_network_ipv4_information'],
                    dht_network_ipv4_peer_database = user_language_data_config['dht_network_ipv4_peer_database'],
                    dht_network_ipv4_router_table = user_language_data_config['dht_network_ipv4_router_table'],
                    dht_network_ipv6_information = user_language_data_config['dht_network_ipv6_information'],
                    dht_network_ipv6_peer_database = user_language_data_config['dht_network_ipv6_peer_database'],
                    dht_network_ipv6_router_table = user_language_data_config['dht_network_ipv6_router_table'],
                    id = user_language_data_config['id'],
                    info_hash = user_language_data_config['info_hash'],
                    ip_address = user_language_data_config['ip_address'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    node_id = user_language_data_config['node_id'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    udp_port = user_language_data_config['udp_port'],
                    update_time = user_language_data_config['update_time'],
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
    else:
        return flask.redirect(flask.url_for('setting'))

@application.route('/report', methods = ['GET'])
@application_cache.cached(timeout = 2)
def report():
    info_hash = flask.request.args.get('info_hash')
    result = data_conversion().explorer_database_check()
    if result is True:
        user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
        if user_language is None:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'report.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    file_name = user_language_data_config['file_name'],
                    file_size = user_language_data_config['file_size'],
                    id = user_language_data_config['id'],
                    info_hash_contents = user_language_data_config['info_hash_contents'],
                    info_hash_information = user_language_data_config['info_hash_information'],
                    info_hash_report = user_language_data_config['info_hash_report'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    sheet_name = info_hash,
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
        elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'report.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    file_name = user_language_data_config['file_name'],
                    file_size = user_language_data_config['file_size'],
                    id = user_language_data_config['id'],
                    info_hash_contents = user_language_data_config['info_hash_contents'],
                    info_hash_information = user_language_data_config['info_hash_information'],
                    info_hash_report = user_language_data_config['info_hash_report'],
                    item = user_language_data_config['item'],
                    language = user_language,
                    network = user_language_data_config['network'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    sheet_name = info_hash,
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
        else:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'report.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    file_name = user_language_data_config['file_name'],
                    file_size = user_language_data_config['file_size'],
                    id = user_language_data_config['id'],
                    info_hash_contents = user_language_data_config['info_hash_contents'],
                    info_hash_information = user_language_data_config['info_hash_information'],
                    info_hash_report = user_language_data_config['info_hash_report'],
                    item = user_language_data_config['item'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    sheet_name = info_hash,
                    spider = user_language_data_config['spider'],
                    token = webview.token,
                    upload_button = user_language_data_config['upload_button'],
                    value = user_language_data_config['value']
                )
    else:
        return flask.redirect(flask.url_for('setting'))

@application.route('/search', methods = ['GET'])
@application_cache.cached(timeout = 2)
def search():
    keyword = flask.request.args.get('keyword')
    result = data_conversion().explorer_database_check()
    if result is True:
        keyword = keyword.strip()
        keyword = re.sub('\s+', ' ', keyword)
        blacklist = ['~', '!', '@', '#', '$', '%', '^', '&', '*']
        for i in blacklist:
            keyword = keyword.replace(i, '')
        if validators.length(keyword, min = 2, max = 30) is True:
            user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
            if user_language is None:
                with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                    user_language_data_config = file.read()
                    user_language_data_config = json.loads(user_language_data_config)
                    return flask.render_template(
                        'search.html',
                        about = user_language_data_config['about'],
                        back = user_language_data_config['back'],
                        database = user_language_data_config['database'],
                        id = user_language_data_config['id'],
                        language = 'en-US',
                        network = user_language_data_config['network'],
                        refresh = user_language_data_config['refresh'],
                        search_button = user_language_data_config['search_button'],
                        search_button_title = user_language_data_config['search_button_title'],
                        search_input_title = user_language_data_config['search_input_title'],
                        search_results = user_language_data_config['search_results'],
                        setting = user_language_data_config['setting'],
                        sheet_name = keyword,
                        spider = user_language_data_config['spider'],
                        token = webview.token,
                        torrent_name = user_language_data_config['torrent_name'],
                        torrent_size = user_language_data_config['torrent_size'],
                        upload_button = user_language_data_config['upload_button']
                    )
            elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
                with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                    user_language_data_config = file.read()
                    user_language_data_config = json.loads(user_language_data_config)
                    return flask.render_template(
                        'search.html',
                        about = user_language_data_config['about'],
                        back = user_language_data_config['back'],
                        database = user_language_data_config['database'],
                        id = user_language_data_config['id'],
                        language = user_language,
                        network = user_language_data_config['network'],
                        refresh = user_language_data_config['refresh'],
                        search_button = user_language_data_config['search_button'],
                        search_button_title = user_language_data_config['search_button_title'],
                        search_input_title = user_language_data_config['search_input_title'],
                        search_results = user_language_data_config['search_results'],
                        setting = user_language_data_config['setting'],
                        sheet_name = keyword,
                        spider = user_language_data_config['spider'],
                        token = webview.token,
                        torrent_name = user_language_data_config['torrent_name'],
                        torrent_size = user_language_data_config['torrent_size'],
                        upload_button = user_language_data_config['upload_button']
                    )
            else:
                with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                    user_language_data_config = file.read()
                    user_language_data_config = json.loads(user_language_data_config)
                    return flask.render_template(
                        'search.html',
                        about = user_language_data_config['about'],
                        back = user_language_data_config['back'],
                        database = user_language_data_config['database'],
                        id = user_language_data_config['id'],
                        language = 'en-US',
                        network = user_language_data_config['network'],
                        refresh = user_language_data_config['refresh'],
                        search_button = user_language_data_config['search_button'],
                        search_button_title = user_language_data_config['search_button_title'],
                        search_input_title = user_language_data_config['search_input_title'],
                        search_results = user_language_data_config['search_results'],
                        setting = user_language_data_config['setting'],
                        sheet_name = keyword,
                        spider = user_language_data_config['spider'],
                        token = webview.token,
                        torrent_name = user_language_data_config['torrent_name'],
                        torrent_size = user_language_data_config['torrent_size'],
                        upload_button = user_language_data_config['upload_button']
                    )
        else:
            return flask.redirect(flask.url_for('default'))
    else:
        return flask.redirect(flask.url_for('setting'))

@application.route('/setting', methods = ['GET'])
@application_cache.cached()
def setting():
    user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
    if user_language is None:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
            user_language_data_config = file.read()
            user_language_data_config = json.loads(user_language_data_config)
            return flask.render_template(
                'setting.html',
                about = user_language_data_config['about'],
                back = user_language_data_config['back'],
                database = user_language_data_config['database'],
                database_application_danger_alert = user_language_data_config['database_application_danger_alert'],
                language = 'en-US',
                network = user_language_data_config['network'],
                refresh = user_language_data_config['refresh'],
                search_button = user_language_data_config['search_button'],
                search_button_title = user_language_data_config['search_button_title'],
                search_input_title = user_language_data_config['search_input_title'],
                setting = user_language_data_config['setting'],
                spider = user_language_data_config['spider'],
                token = webview.token,
                upload_button = user_language_data_config['upload_button']
            )
    elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
            user_language_data_config = file.read()
            user_language_data_config = json.loads(user_language_data_config)
            return flask.render_template(
                'setting.html',
                about = user_language_data_config['about'],
                back = user_language_data_config['back'],
                database = user_language_data_config['database'],
                database_application_danger_alert = user_language_data_config['database_application_danger_alert'],
                language = user_language,
                network = user_language_data_config['network'],
                refresh = user_language_data_config['refresh'],
                search_button = user_language_data_config['search_button'],
                search_button_title = user_language_data_config['search_button_title'],
                search_input_title = user_language_data_config['search_input_title'],
                setting = user_language_data_config['setting'],
                spider = user_language_data_config['spider'],
                token = webview.token,
                upload_button = user_language_data_config['upload_button']
            )
    else:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
            user_language_data_config = file.read()
            user_language_data_config = json.loads(user_language_data_config)
            return flask.render_template(
                'setting.html',
                about = user_language_data_config['about'],
                back = user_language_data_config['back'],
                database = user_language_data_config['database'],
                database_application_danger_alert = user_language_data_config['database_application_danger_alert'],
                language = 'en-US',
                network = user_language_data_config['network'],
                refresh = user_language_data_config['refresh'],
                search_button = user_language_data_config['search_button'],
                search_button_title = user_language_data_config['search_button_title'],
                search_input_title = user_language_data_config['search_input_title'],
                setting = user_language_data_config['setting'],
                spider = user_language_data_config['spider'],
                token = webview.token,
                upload_button = user_language_data_config['upload_button']
            )

@application.route('/spider', methods = ['GET'])
@application_cache.cached()
def spider():
    result = data_conversion().explorer_database_check()
    if result is True:
        user_language = flask.request.accept_languages.best_match(memory.application_support_languages)
        if user_language is None:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'spider.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    id = user_language_data_config['id'],
                    info_hash = user_language_data_config['info_hash'],
                    ip_address = user_language_data_config['ip_address'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    peer_wire_ipv4_ut_metadata_progress_table = user_language_data_config['peer_wire_ipv4_ut_metadata_progress_table'],
                    peer_wire_ipv6_ut_metadata_progress_table = user_language_data_config['peer_wire_ipv6_ut_metadata_progress_table'],
                    progress = user_language_data_config['progress'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    status = user_language_data_config['status'],
                    token = webview.token,
                    torrent_name = user_language_data_config['torrent_name'],
                    torrent_size = user_language_data_config['torrent_size'],
                    upload_button = user_language_data_config['upload_button']
                )
        elif os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json'):
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/' + user_language + '.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'spider.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    id = user_language_data_config['id'],
                    info_hash = user_language_data_config['info_hash'],
                    ip_address = user_language_data_config['ip_address'],
                    language = user_language,
                    network = user_language_data_config['network'],
                    peer_wire_ipv4_ut_metadata_progress_table = user_language_data_config['peer_wire_ipv4_ut_metadata_progress_table'],
                    peer_wire_ipv6_ut_metadata_progress_table = user_language_data_config['peer_wire_ipv6_ut_metadata_progress_table'],
                    progress = user_language_data_config['progress'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    status = user_language_data_config['status'],
                    token = webview.token,
                    torrent_name = user_language_data_config['torrent_name'],
                    torrent_size = user_language_data_config['torrent_size'],
                    upload_button = user_language_data_config['upload_button']
                )
        else:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/languages/en-US.json', mode = 'r', encoding = 'utf-8') as file:
                user_language_data_config = file.read()
                user_language_data_config = json.loads(user_language_data_config)
                return flask.render_template(
                    'spider.html',
                    about = user_language_data_config['about'],
                    back = user_language_data_config['back'],
                    database = user_language_data_config['database'],
                    id = user_language_data_config['id'],
                    info_hash = user_language_data_config['info_hash'],
                    ip_address = user_language_data_config['ip_address'],
                    language = 'en-US',
                    network = user_language_data_config['network'],
                    peer_wire_ipv4_ut_metadata_progress_table = user_language_data_config['peer_wire_ipv4_ut_metadata_progress_table'],
                    peer_wire_ipv6_ut_metadata_progress_table = user_language_data_config['peer_wire_ipv6_ut_metadata_progress_table'],
                    progress = user_language_data_config['progress'],
                    refresh = user_language_data_config['refresh'],
                    search_button = user_language_data_config['search_button'],
                    search_button_title = user_language_data_config['search_button_title'],
                    search_input_title = user_language_data_config['search_input_title'],
                    setting = user_language_data_config['setting'],
                    spider = user_language_data_config['spider'],
                    status = user_language_data_config['status'],
                    token = webview.token,
                    torrent_name = user_language_data_config['torrent_name'],
                    torrent_size = user_language_data_config['torrent_size'],
                    upload_button = user_language_data_config['upload_button']
                )
    else:
        return flask.redirect(flask.url_for('setting'))