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
            'css!./static/css/report.css',
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
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/extensions/export/bootstrap-table-export.js',
            'https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/extensions/treegrid/bootstrap-table-treegrid.js',
            'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@latest/js/all.js',
            'https://cdn.jsdelivr.net/npm/overlayscrollbars@latest/js/OverlayScrollbars.js',
            'https://cdn.jsdelivr.net/npm/validator@latest/validator.js',
            'https://cdn.jsdelivr.net/npm/clipboard@latest/dist/clipboard.js',
            'https://cdn.jsdelivr.net/npm/js-cookie@latest/dist/js.cookie.js',
            'https://cdn.jsdelivr.net/npm/moment@latest/moment.js',
            'https://cdn.jsdelivr.net/npm/moment-timer@latest/lib/moment-timer.js',
            'https://cdn.jsdelivr.net/npm/js-url@latest/url.js'
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
                $('#info_hash_information_table').bootstrapTable({
                    onPostBody: function () {
                        var clipboard = new ClipboardJS('#copy_magnet_uri');
                        clipboard.on('success', function (e) {
                            $('#copy_magnet_uri_success_alert').removeClass('visually-hidden');
                            e.clearSelection();
                        });
                        clipboard.on('error', function (e) {
                            $('#copy_magnet_uri_danger_alert').removeClass('visually-hidden');
                        });
                    }
                });
                $('#info_hash_contents_table').bootstrapTable({
                    idField: 'id',
                    parentIdField: 'pid',
                    showColumns: true,
                    treeShowField: 'file_name',
                    onPostBody: function () {
                        var columns = $('#info_hash_contents_table').bootstrapTable('getOptions').columns;
                        if(columns && columns[0][1].visible) {
                            $('#info_hash_contents_table').treegrid({
                                treeColumn: 0,
                                initialState: 'collapsed',
                                onChange: function () {
                                    $('#info_hash_contents_table').bootstrapTable('resetView');
                                }
                            });
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

function ajax_request_database_query_info_hash_contents (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_database_query_info_hash_contents?info_hash=' + url('?')['info_hash'],
        success: function (api_database_query_info_hash_contents) {
            var work_blob = new Blob([`(${convert_info_hash_contents_data.toString ()})()`]);
            work_blob = new Blob([convert_info_hash_contents_data.toLocaleString().match(/(?:\/\*[\s\S]*?\*\/|\/\/.*?\r?\n|[^{])+\{([\s\S]*)\}$/)[1]]);
            var work_blob_url = URL.createObjectURL(work_blob);
            var worker = new Worker(work_blob_url);
            worker.postMessage(api_database_query_info_hash_contents.data);
            worker.onmessage = function (event) {
                params.success(event.data);
            };
            worker.onerror = function () {
                worker.terminate();
            };
        },
        error: function () {
            params.success([]);
        }
    });
};

function ajax_request_database_query_info_hash_information (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_database_query_info_hash_information?info_hash=' + url('?')['info_hash'],
        success: function (api_database_query_info_hash_information) {
            params.success(api_database_query_info_hash_information.data);
        },
        error: function () {
            params.success([]);
        }
    });
};

function convert_info_hash_contents_data () {
    onmessage = function (event) {
        var api_database_query_info_hash_contents_data = event.data;
        info_hash_contents = [];
        for(var i = 0; i < api_database_query_info_hash_contents_data.length; i = i + 1) {
            var j = api_database_query_info_hash_contents_data[i].file_name.indexOf('/');
            if(j == -1) {
                info_hash_content = ['/', api_database_query_info_hash_contents_data[i].file_name];
                info_hash_content.push(api_database_query_info_hash_contents_data[i].file_size);
                info_hash_contents.push(info_hash_content);
            } else {
                info_hash_content = api_database_query_info_hash_contents_data[i].file_name.split('/');
                info_hash_content[0] = '/';
                info_hash_content.push(api_database_query_info_hash_contents_data[i].file_size);
                info_hash_contents.push(info_hash_content);
            };
        };
        info_hash_treegrid_contents = [];
        for(var i = 0; i < info_hash_contents.length; i = i + 1) {
            for(var j = 0; j < info_hash_contents[i].length - 1; j = j + 1) {
                if(j == info_hash_contents[i].length - 2) {
                    info_hash_treegrid_contents.push({
                        'id': info_hash_treegrid_contents.length + 1,
                        'pid': j,
                        'file_name': info_hash_contents[i][j],
                        'file_size': info_hash_contents[i][j + 1]
                    });
                } else {
                    info_hash_treegrid_contents.push({
                        'id': info_hash_treegrid_contents.length + 1,
                        'pid': j,
                        'file_name': info_hash_contents[i][j],
                        'file_size': ''
                    });
                };
            };
        };
        directory_array = [];
        for(var i = 0; i < info_hash_treegrid_contents.length; i = i + 1) {
            if(info_hash_treegrid_contents[i].file_size == '') {
                directory_array.push(info_hash_treegrid_contents[i].file_name);
            };
        };
        for(var i = 0; i < directory_array.length; i = i + 1) {
            var current = directory_array[i];
            for (var j = i + 1; j < directory_array.length; j = j + 1) {
                if (current == directory_array[j]) {
                    directory_array.splice(j, 1);
                    j = j - 1;
                };
            };
        };
        directory_dictionary = {};
        for(var i = 0; i < directory_array.length; i = i + 1) {
            directory_dictionary[directory_array[i]] = 0;
        };
        for(var i = 0; i < directory_array.length; i = i + 1) {
            for(var j = info_hash_treegrid_contents.length - 1; j  > -1; j = j - 1) {
                if (directory_array[i] == info_hash_treegrid_contents[j].file_name) {
                    directory_dictionary[directory_array[i]] = j;
                };
            };
        };
        for(var i in directory_dictionary) {
            for(var j = directory_dictionary[i] + 1; j < info_hash_treegrid_contents.length; j = j + 1) {
                if(info_hash_treegrid_contents[j].file_name == i && info_hash_treegrid_contents[j].pid == info_hash_treegrid_contents[directory_dictionary[i]].pid) {
                    delete info_hash_treegrid_contents[j];
                };
            };
            temporary_info_hash_treegrid_contents = []
            for(var j = 0; j < info_hash_treegrid_contents.length; j = j + 1) {
                if(info_hash_treegrid_contents[j] != undefined) {
                    temporary_info_hash_treegrid_contents.push(info_hash_treegrid_contents[j]);
                };
            };
            info_hash_treegrid_contents = temporary_info_hash_treegrid_contents;
            for(var j = 0; j < directory_array.length; j = j + 1) {
                for(var k = info_hash_treegrid_contents.length - 1; k  > -1; k = k - 1) {
                    if(directory_array[j] == info_hash_treegrid_contents[k].file_name) {
                        directory_dictionary[directory_array[j]] = k;
                    };
                };
            };
        };
        for(var i = 0; i < info_hash_contents.length; i = i + 1) {
            for(var j = 0; j < info_hash_contents[i].length - 1; j = j + 1) {
                if(j != info_hash_contents[i].length - 2) {
                    for(var k in info_hash_treegrid_contents) {
                        if(info_hash_contents[i][j - 1] == info_hash_treegrid_contents[k].file_name && info_hash_treegrid_contents[k].file_size == '') {
                            for(var l in info_hash_treegrid_contents) {
                                if(info_hash_treegrid_contents[l].file_name == info_hash_contents[i][j] && info_hash_treegrid_contents[l].file_size == '') {
                                    info_hash_treegrid_contents[l].pid = info_hash_treegrid_contents[k].id;
                                };
                            };
                        };
                    };
                };
            };
        };
        info_hash_contents_array_length = 0;
        for(var i = 0; i < info_hash_contents.length; i = i + 1) {
            if(info_hash_contents[i].length > info_hash_contents_array_length) {
                info_hash_contents_array_length = info_hash_contents[i].length;
            };
        };
        for(var i = info_hash_contents_array_length; i > 2; i = i - 1) {
            for(var j = 0; j < info_hash_contents.length; j = j + 1) {
                if(info_hash_contents[j].length == i) {
                    for(var k in info_hash_treegrid_contents) {
                        if(info_hash_contents[j][i - 2] == info_hash_treegrid_contents[k].file_name && info_hash_contents[j][i - 1] == info_hash_treegrid_contents[k].file_size) {
                            for(var l in info_hash_treegrid_contents) {
                                if(info_hash_treegrid_contents[l].file_name == info_hash_contents[j][i - 3] && info_hash_treegrid_contents[l].file_size == '') {
                                    info_hash_treegrid_contents[k].pid = info_hash_treegrid_contents[l].id;
                                };
                            };
                        };
                    };
                };
            };
        };
        postMessage(info_hash_treegrid_contents);
    };
};