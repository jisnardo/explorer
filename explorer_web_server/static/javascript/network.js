document.onreadystatechange = function () {
    if(document.readyState == 'interactive') {
        loadjs([
            'css!https://cdn.jsdelivr.net/npm/overlayscrollbars@latest/css/OverlayScrollbars.css',
            'css!https://cdn.jsdelivr.net/npm/jquery-treegrid@latest/css/jquery.treegrid.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap@latest/dist/css/bootstrap.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-icons@latest/font/bootstrap-icons.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/css/fileinput.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/bootstrap-table.css',
            'css!https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@latest/css/all.css',
            'css!./static/css/network.css',
            'https://cdn.jsdelivr.net/npm/jquery@latest/dist/jquery.js',
            'https://cdn.jsdelivr.net/npm/tableexport.jquery.plugin@latest/tableExport.min.js',
            'https://cdn.jsdelivr.net/npm/jquery-treegrid@latest/js/jquery.treegrid.min.js',
            'https://cdn.jsdelivr.net/npm/bootstrap@latest/dist/js/bootstrap.bundle.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/fileinput.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/ar.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/az.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/bg.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/ca.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/cr.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/cs.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/da.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/de.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/el.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/es.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/et.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/fa.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/fi.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/fr.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/gl.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/he.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/hu.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/id.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/it.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/LANG.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/ja.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/ka.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/kr.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/kz.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/lt.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/lv.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/nl.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/no.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/pl.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/pt.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/pt-BR.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/ro.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/ru.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/sk.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/sl.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/sr-latn.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/sv.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/th.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/tr.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/uk.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/uz.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/uz-Cy.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/vi.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/zh.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/js/locales/zh-TW.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/bootstrap-table.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/bootstrap-table-locale-all.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/extensions/auto-refresh/bootstrap-table-auto-refresh.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/extensions/export/bootstrap-table-export.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/extensions/page-jump-to/bootstrap-table-page-jump-to.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/extensions/treegrid/bootstrap-table-treegrid.js',
            'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@latest/js/all.js',
            'https://cdn.jsdelivr.net/npm/overlayscrollbars@latest/js/OverlayScrollbars.js',
            'https://cdn.jsdelivr.net/npm/validator@latest/validator.js',
            'https://cdn.jsdelivr.net/npm/js-cookie@latest/dist/js.cookie.js',
            'https://cdn.jsdelivr.net/npm/moment@latest/moment.js',
            'https://cdn.jsdelivr.net/npm/moment-timer@latest/lib/moment-timer.js'
        ], {
            async: false,
            error: function () {
                window.location.reload();
            },
            success: function () {
                var instance = $('body').overlayScrollbars({
                    className: 'os-theme-dark'
                }).overlayScrollbars();
                var nav_timer = new moment.duration(60000).timer({loop: true, wait: 1000, executeAfterWait: true}, function () {
                    $.ajax({
                        async: true,
                        contentType: 'application/json',
                        data: JSON.stringify({
                            'token': window.token
                        }),
                        dataType: 'json',
                        type: 'post',
                        url: window.location.protocol + '//' + window.location.host + '/api_database_query_info_hash_number',
                        success: function (api_database_query_info_hash_number) {
                            $('#info_hash_count').html(api_database_query_info_hash_number.data);
                        }
                    });
                    $.ajax({
                        async: true,
                        contentType: 'application/json',
                        data: JSON.stringify({
                            'token': window.token
                        }),
                        dataType: 'json',
                        type: 'post',
                        url: window.location.protocol + '//' + window.location.host + '/api_database_query_info_hash_file_size',
                        success: function (api_database_query_info_hash_file_size) {
                            $('#file_size_count').html(api_database_query_info_hash_file_size.data);
                        }
                    });
                });
                nav_timer.start();
                $('#about').click(function () {
                    window.location.href = window.location.protocol + '//' + window.location.host + '/about';
                });
                $('#database').click(function () {
                    Cookies.set('database_card_view', false);
                    Cookies.set('database_page_number', 1);
                    Cookies.set('database_page_size', 10);
                    Cookies.set('database_search_text', '');
                    Cookies.set('database_sort_name', '');
                    Cookies.set('database_sort_order', '');
                    window.location.href = window.location.protocol + '//' + window.location.host + '/database';
                });
                $('#network').click(function () {
                    window.location.href = window.location.protocol + '//' + window.location.host + '/network';
                });
                $('#setting').click(function () {
                    window.location.href = window.location.protocol + '//' + window.location.host + '/setting';
                });
                $('#spider').click(function () {
                    window.location.href = window.location.protocol + '//' + window.location.host + '/spider';
                });
                $('#upload_modal').overlayScrollbars({
                    className: 'os-theme-light'
                });
                var os_instance = OverlayScrollbars(document.querySelectorAll('body'), { });
                $('#upload_modal').on('show.bs.modal', function () {
                    instance.options({
                        className: null
                    });
                    setTimeout(function () {
                        var os_content_elm = $(os_instance.getElements().content);
                        var backdrop_elms = $('body > .modal-backdrop');
                        backdrop_elms.each(function (index, elm) {
                            os_content_elm.append(elm);
                        });
                    }, 1);
                });
                $('#upload_modal').on('hidden.bs.modal', function () {
                    instance.options({
                        className: 'os-theme-dark'
                    });
                });
                var language = navigator.language;
                switch (language) {
                    case 'en-GB':
                        language = 'en';
                        break;
                    case 'en-US':
                        language = 'en';
                        break;
                    case 'zh-CN':
                        language = 'zh';
                        break;
                    case 'zh-HK':
                        language = 'zh-TW';
                        break;
                    case 'zh-SG':
                        language = 'zh';
                        break;
                    case 'zh-TW':
                        language = 'zh-TW';
                        break;
                    default:
                        language = 'en';
                };
                $('#torrent_upload').fileinput({
                    allowedFileExtensions: ['torrent'],
                    enctype: 'multipart/form-data',
                    language: language,
                    maxFileCount: 10000,
                    minFileCount: 1,
                    uploadAsync: true,
                    uploadExtraData: {
                        'token': window.token
                    },
                    uploadUrl: window.location.protocol + '//' + window.location.host + '/api_database_query_insert',
                    validateInitialCount: true
                });
                $('[data-toggle=\'search_button_tooltip\']').tooltip();
                $('[data-toggle=\'search_input_tooltip\']').tooltip();
                $('#search_button').click(function () {
                    var search_input_string = $('#search_input').val().replace(/^\s+|\s+$/g, '');
                    var search_input_string = validator.blacklist(search_input_string, '~!@#$%^&*');
                    if(validator.isLength(search_input_string, {min: 2, max: 30}) == true) {
                        Cookies.set('search_card_view', false);
                        Cookies.set('search_page_number', 1);
                        Cookies.set('search_page_size', 10);
                        Cookies.set('search_search_text', '');
                        Cookies.set('search_sort_name', '');
                        Cookies.set('search_sort_order', '');
                        window.location.href = window.location.protocol + '//' + window.location.host + '/search?search_input=' + encodeURIComponent(search_input_string);
                    } else {
                        $('#search_input').css('background-color', '#fff3cd');
                    };
                });
                $('#search_input').each(function () {
                    $(this).keypress(function (event) {
                        if(event.which == 13) {
                            var search_input_string = $('#search_input').val().replace(/^\s+|\s+$/g, '');
                            var search_input_string = validator.blacklist(search_input_string, '~!@#$%^&*');
                            if(validator.isLength(search_input_string, {min: 2, max: 30}) == true) {
                                Cookies.set('search_card_view', false);
                                Cookies.set('search_page_number', 1);
                                Cookies.set('search_page_size', 10);
                                Cookies.set('search_search_text', '');
                                Cookies.set('search_sort_name', '');
                                Cookies.set('search_sort_order', '');
                                window.location.href = window.location.protocol + '//' + window.location.host + '/search?search_input=' + encodeURIComponent(search_input_string);
                            } else {
                                $('#search_input').css('background-color', '#fff3cd');
                            };
                        };
                    });
                });
                $('#page_back').click(function () {
                    window.history.back();
                });
                $('#page_refresh').click(function () {
                    window.location.reload();
                });
                $('#dht_network_ipv4_information_table').bootstrapTable({
                });
                $('#dht_network_ipv4_ping').click(function () {
                    $('#dht_network_ipv4_ping_success_alert').toggleClass('visually-hidden', true);
                    $('#dht_network_ipv4_ping_warning_alert').toggleClass('visually-hidden', true);
                    dht_network_ipv4_ping_ip_address = $('#dht_network_ipv4_ping_ip_address').val();
                    dht_network_ipv4_ping_udp_port = $('#dht_network_ipv4_ping_udp_port').val();
                    if(validator.isIP(dht_network_ipv4_ping_ip_address, 4) == true) {
                        if(validator.isPort(dht_network_ipv4_ping_udp_port) == true) {
                            $('#dht_network_ipv4_ping').attr('disabled', '');
                            $.ajax({
                                async: true,
                                contentType: 'application/json',
                                data: JSON.stringify({
                                    'ip_address': dht_network_ipv4_ping_ip_address,
                                    'udp_port': dht_network_ipv4_ping_udp_port,
                                    'token': window.token
                                }),
                                dataType: 'json',
                                type: 'post',
                                url: window.location.protocol + '//' + window.location.host + '/api_krpc_v4_ping',
                                success: function (api_krpc_v4_ping) {
                                    if(api_krpc_v4_ping.data == true) {
                                        $('#dht_network_ipv4_ping_success_alert').removeClass('visually-hidden');
                                    };
                                    if(api_krpc_v4_ping.data == false) {
                                        $('#dht_network_ipv4_ping_warning_alert').removeClass('visually-hidden');
                                    };
                                    $('#dht_network_ipv4_ping').removeAttr('disabled');
                                },
                                error: function () {
                                    $('#dht_network_ipv4_ping_warning_alert').removeClass('visually-hidden');
                                    $('#dht_network_ipv4_ping').removeAttr('disabled');
                                }
                            });
                        } else {
                            $('#dht_network_ipv4_ping_udp_port').css('background-color', '#fff3cd');
                        };
                    } else {
                        $('#dht_network_ipv4_ping_ip_address').css('background-color', '#fff3cd');
                    };
                });
                $('#dht_network_ipv4_router_table').bootstrapTable({
                    idField: 'id',
                    parentIdField: 'pid',
                    showColumns: true,
                    treeShowField: 'node_id',
                    onPostBody: function () {
                        var columns = $('#dht_network_ipv4_router_table').bootstrapTable('getOptions').columns;
                        if(columns && columns[0][1].visible) {
                            $('#dht_network_ipv4_router_table').treegrid({
                                treeColumn: 0,
                                onChange: function () {
                                    $('#dht_network_ipv4_router_table').bootstrapTable('resetView');
                                }
                            });
                        };
                    }
                });
                $('#dht_network_ipv4_peer_database_table').bootstrapTable({
                    onLoadSuccess: function (data) {
                        var index = 0;
                        var rowspan = 0;
                        var info_hash = '';
                        for(var i = 0; i < data.length; i = i + 1) {
                            if(info_hash == data[i]['info_hash']) {
                                rowspan = rowspan + 1;
                                $('#dht_network_ipv4_peer_database_table').bootstrapTable('mergeCells', {
                                    index: index,
                                    field: 'info_hash',
                                    colspan: 1,
                                    rowspan: rowspan
                                });
                            } else {
                                index = i;
                                rowspan = 1;
                                info_hash = data[i]['info_hash'];
                            };
                        };
                    }
                });
                $('#dht_network_ipv6_information_table').bootstrapTable({
                });
                $('#dht_network_ipv6_ping').click(function () {
                    $('#dht_network_ipv6_ping_success_alert').toggleClass('visually-hidden', true);
                    $('#dht_network_ipv6_ping_warning_alert').toggleClass('visually-hidden', true);
                    dht_network_ipv6_ping_ip_address = $('#dht_network_ipv6_ping_ip_address').val();
                    dht_network_ipv6_ping_udp_port = $('#dht_network_ipv6_ping_udp_port').val();
                    if(validator.isIP(dht_network_ipv6_ping_ip_address, 6) == true) {
                        if(validator.isPort(dht_network_ipv6_ping_udp_port) == true) {
                            $('#dht_network_ipv6_ping').attr('disabled', '');
                            $.ajax({
                                async: true,
                                contentType: 'application/json',
                                data: JSON.stringify({
                                    'ip_address': dht_network_ipv6_ping_ip_address,
                                    'udp_port': dht_network_ipv6_ping_udp_port,
                                    'token': window.token
                                }),
                                dataType: 'json',
                                type: 'post',
                                url: window.location.protocol + '//' + window.location.host + '/api_krpc_v6_ping',
                                success: function (api_krpc_v6_ping) {
                                    if(api_krpc_v6_ping.data == true) {
                                        $('#dht_network_ipv6_ping_success_alert').removeClass('visually-hidden');
                                    };
                                    if(api_krpc_v6_ping.data == false) {
                                        $('#dht_network_ipv6_ping_warning_alert').removeClass('visually-hidden');
                                    };
                                    $('#dht_network_ipv6_ping').removeAttr('disabled');
                                },
                                error: function () {
                                    $('#dht_network_ipv6_ping_warning_alert').removeClass('visually-hidden');
                                    $('#dht_network_ipv6_ping').removeAttr('disabled');
                                }
                            });
                        } else {
                            $('#dht_network_ipv6_ping_udp_port').css('background-color', '#fff3cd');
                        };
                    } else {
                        $('#dht_network_ipv6_ping_ip_address').css('background-color', '#fff3cd');
                    };
                });
                $('#dht_network_ipv6_router_table').bootstrapTable({
                    idField: 'id',
                    parentIdField: 'pid',
                    showColumns: true,
                    treeShowField: 'node_id',
                    onPostBody: function () {
                        var columns = $('#dht_network_ipv6_router_table').bootstrapTable('getOptions').columns;
                        if(columns && columns[0][1].visible) {
                            $('#dht_network_ipv6_router_table').treegrid({
                                treeColumn: 0,
                                onChange: function () {
                                    $('#dht_network_ipv6_router_table').bootstrapTable('resetView');
                                }
                            });
                        };
                    }
                });
                $('#dht_network_ipv6_peer_database_table').bootstrapTable({
                    onLoadSuccess: function (data) {
                        var index = 0;
                        var rowspan = 0;
                        var info_hash = '';
                        for(var i = 0; i < data.length; i = i + 1) {
                            if(info_hash == data[i]['info_hash']) {
                                rowspan = rowspan + 1;
                                $('#dht_network_ipv6_peer_database_table').bootstrapTable('mergeCells', {
                                    index: index,
                                    field: 'info_hash',
                                    colspan: 1,
                                    rowspan: rowspan
                                });
                            } else {
                                index = i;
                                rowspan = 1;
                                info_hash = data[i]['info_hash'];
                            };
                        };
                    }
                });
            }
        });
    };
    if(document.readyState == 'complete') {
        $('body').css('display', '');
        $('#page').css('margin-top', $('#nav').outerHeight(true) + 10 + 'px');
        $('#page').css('margin-bottom', $('#footer').outerHeight(true) + 'px');
        $(window).resize(function () {
            $('#page').css('margin-top', $('#nav').outerHeight(true) + 10 + 'px');
            $('#page').css('margin-bottom', $('#footer').outerHeight(true) + 'px');
        });
    };
};

function ajax_request_krpc_v4_parameter_read (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_krpc_v4_parameter_read',
        success: function (api_krpc_v4_parameter_read) {
            params.success(api_krpc_v4_parameter_read.data);
        },
        error: function () {
            params.success([]);
        }
    });
};

function ajax_request_krpc_v4_peer_database_read (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_krpc_v4_peer_database_read',
        success: function (api_krpc_v4_peer_database_read) {
            params.success(api_krpc_v4_peer_database_read.data);
        },
        error: function () {
            params.success([]);
        }
    });
};

function ajax_request_krpc_v4_router_table_read (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_krpc_v4_router_table_read',
        success: function (api_krpc_v4_router_table_read) {
            router_table_treegrid_contents = [];
            k_bucket = api_krpc_v4_router_table_read.data[0]['k_bucket'];
            for(var i in api_krpc_v4_router_table_read.data[1]) {
                router_table_treegrid_contents.push({
                    'id': Number(i) + 1,
                    'pid': 0,
                    'node_id': k_bucket + ' (' + (Number(i) + 1).toString() + ') ' + '<span class=\'badge bg-secondary\'>' + (Object.keys(api_krpc_v4_router_table_read.data[1][i]).length) + '</span>',
                    'ip_address': '',
                    'update_time': ''
                });
                for(var j in api_krpc_v4_router_table_read.data[1][i]) {
                    router_table_treegrid_contents.push({
                        'id': router_table_treegrid_contents.length + 160,
                        'pid': Number(i) + 1,
                        'node_id': api_krpc_v4_router_table_read.data[1][i][j]['node_id'],
                        'ip_address': api_krpc_v4_router_table_read.data[1][i][j]['ip_address'] + ':' + api_krpc_v4_router_table_read.data[1][i][j]['udp_port'],
                        'update_time': '<span class=\'badge bg-secondary\'>' + api_krpc_v4_router_table_read.data[1][i][j]['update_time'] + '</span>'
                    });
                };
            };
            params.success(router_table_treegrid_contents);
        },
        error: function () {
            params.success([]);
        }
    });
};

function ajax_request_krpc_v6_parameter_read (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_krpc_v6_parameter_read',
        success: function (api_krpc_v6_parameter_read) {
            params.success(api_krpc_v6_parameter_read.data);
        },
        error: function () {
            params.success([]);
        }
    });
};

function ajax_request_krpc_v6_peer_database_read (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_krpc_v6_peer_database_read',
        success: function (api_krpc_v6_peer_database_read) {
            params.success(api_krpc_v6_peer_database_read.data);
        },
        error: function () {
            params.success([]);
        }
    });
};

function ajax_request_krpc_v6_router_table_read (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_krpc_v6_router_table_read',
        success: function (api_krpc_v6_router_table_read) {
            router_table_treegrid_contents = [];
            k_bucket = api_krpc_v6_router_table_read.data[0]['k_bucket'];
            for(var i in api_krpc_v6_router_table_read.data[1]) {
                router_table_treegrid_contents.push({
                    'id': Number(i) + 1,
                    'pid': 0,
                    'node_id': k_bucket + ' (' + (Number(i) + 1).toString() + ') ' + '<span class=\'badge bg-secondary\'>' + (Object.keys(api_krpc_v6_router_table_read.data[1][i]).length) + '</span>',
                    'ip_address': '',
                    'update_time': ''
                });
                for(var j in api_krpc_v6_router_table_read.data[1][i]) {
                    router_table_treegrid_contents.push({
                        'id': router_table_treegrid_contents.length + 160,
                        'pid': Number(i) + 1,
                        'node_id': api_krpc_v6_router_table_read.data[1][i][j]['node_id'],
                        'ip_address': '[' + api_krpc_v6_router_table_read.data[1][i][j]['ip_address'] + ']:' + api_krpc_v6_router_table_read.data[1][i][j]['udp_port'],
                        'update_time': '<span class=\'badge bg-secondary\'>' + api_krpc_v6_router_table_read.data[1][i][j]['update_time'] + '</span>'
                    });
                };
            };
            params.success(router_table_treegrid_contents);
        },
        error: function () {
            params.success([]);
        }
    });
};