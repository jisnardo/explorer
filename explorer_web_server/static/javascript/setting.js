document.onreadystatechange = function () {
    if(document.readyState == 'interactive') {
        loadjs([
            'css!https://cdn.jsdelivr.net/npm/overlayscrollbars@latest/css/OverlayScrollbars.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap@latest/dist/css/bootstrap.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-icons@latest/font/bootstrap-icons.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/css/fileinput.css',
            'css!https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@latest/css/all.css',
            'css!./static/css/setting.css',
            'https://cdn.jsdelivr.net/npm/jquery@latest/dist/jquery.js',
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
            'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@latest/js/all.js',
            'https://cdn.jsdelivr.net/npm/overlayscrollbars@latest/js/OverlayScrollbars.js',
            'https://cdn.jsdelivr.net/npm/validator@latest/validator.js',
            'https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.js',
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
                $.ajax({
                    async: true,
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'token': window.token
                    }),
                    dataType: 'json',
                    type: 'post',
                    url: window.location.protocol + '//' + window.location.host + '/api_database_check',
                    success: function (api_database_check) {
                        if(api_database_check.data == false) {
                            $('#database_application_warning_alert').removeClass('visually-hidden');
                        };
                    }
                });
                $('#page_back').click(function () {
                    window.history.back();
                });
                $('#page_refresh').click(function () {
                    window.location.reload();
                });
                $.ajax({
                    async: true,
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'token': window.token
                    }),
                    dataType: 'json',
                    type: 'post',
                    url: window.location.protocol + '//' + window.location.host + '/api_setting_database_config_json_read',
                    success: function (api_setting_database_config_json_read) {
                        var database_config_json_editor = new JSONEditor(document.getElementById('database_config_json'), {
                            disable_edit_json: true,
                            disable_properties: true,
                            iconlib: 'fontawesome5',
                            schema: api_setting_database_config_json_read.data,
                            theme: 'bootstrap4'
                        });
                        database_config_json_editor.on('change', () => {
                            $.ajax({
                                async: true,
                                contentType: 'application/json',
                                data: JSON.stringify({
                                    'file_data': database_config_json_editor.getValue(),
                                    'token': window.token
                                }),
                                dataType: 'json',
                                type: 'post',
                                url: window.location.protocol + '//' + window.location.host + '/api_setting_database_config_json_write'
                            });
                        });
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
                    url: window.location.protocol + '//' + window.location.host + '/api_setting_save_torrent_files_folder_config_json_read',
                    success: function (api_setting_save_torrent_files_folder_config_json_read) {
                        var save_torrent_files_folder_config_json_editor = new JSONEditor(document.getElementById('save_torrent_files_folder_config_json'), {
                            disable_edit_json: true,
                            disable_properties: true,
                            iconlib: 'fontawesome5',
                            schema: api_setting_save_torrent_files_folder_config_json_read.data,
                            theme: 'bootstrap4'
                        });
                        save_torrent_files_folder_config_json_editor.on('change', () => {
                            $.ajax({
                                async: true,
                                contentType: 'application/json',
                                data: JSON.stringify({
                                    'file_data': save_torrent_files_folder_config_json_editor.getValue(),
                                    'token': window.token
                                }),
                                dataType: 'json',
                                type: 'post',
                                url: window.location.protocol + '//' + window.location.host + '/api_setting_save_torrent_files_folder_config_json_write'
                            });
                        });
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
                    url: window.location.protocol + '//' + window.location.host + '/api_setting_tracker_list_config_json_read',
                    success: function (api_setting_tracker_list_config_json_read) {
                        var tracker_list_config_json_editor = new JSONEditor(document.getElementById('tracker_list_config_json'), {
                            disable_edit_json: true,
                            disable_properties: true,
                            iconlib: 'fontawesome5',
                            schema: api_setting_tracker_list_config_json_read.data,
                            theme: 'bootstrap4'
                        });
                        tracker_list_config_json_editor.on('change', () => {
                            $.ajax({
                                async: true,
                                contentType: 'application/json',
                                data: JSON.stringify({
                                    'file_data': tracker_list_config_json_editor.getValue(),
                                    'token': window.token
                                }),
                                dataType: 'json',
                                type: 'post',
                                url: window.location.protocol + '//' + window.location.host + '/api_setting_tracker_list_config_json_write'
                            });
                        });
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