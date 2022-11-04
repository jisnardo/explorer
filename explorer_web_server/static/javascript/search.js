document.onreadystatechange = function () {
    if(document.readyState == 'interactive') {
        loadjs([
            'css!https://cdn.jsdelivr.net/npm/overlayscrollbars@latest/css/OverlayScrollbars.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap@latest/dist/css/bootstrap.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-icons@latest/font/bootstrap-icons.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-fileinput@latest/css/fileinput.css',
            'css!https://cdn.jsdelivr.net/npm/bootstrap-table@latest/dist/bootstrap-table.css',
            'css!https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@latest/css/all.css',
            'css!./static/css/search.css',
            'https://cdn.jsdelivr.net/npm/jquery@latest/dist/jquery.js',
            'https://cdn.jsdelivr.net/npm/tableexport.jquery.plugin@latest/tableExport.min.js',
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
            'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@latest/js/all.js',
            'https://cdn.jsdelivr.net/npm/overlayscrollbars@latest/js/OverlayScrollbars.js',
            'https://cdn.jsdelivr.net/npm/validator@latest/validator.js',
            'https://cdn.jsdelivr.net/npm/xbytes@latest/dist/index.js',
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
                if(Cookies.get('search_card_view') == undefined) {
                    Cookies.set('search_card_view', false);
                };
                if(Cookies.get('search_page_number') == undefined) {
                    Cookies.set('search_page_number', 1);
                };
                if(Cookies.get('search_page_size') == undefined) {
                    Cookies.set('search_page_size', 10);
                };
                if(Cookies.get('search_search_text') == undefined) {
                    Cookies.set('search_search_text', '');
                };
                if(Cookies.get('search_sort_name') == undefined) {
                    Cookies.set('search_sort_name', '');
                };
                if(Cookies.get('search_sort_order') == undefined) {
                    Cookies.set('search_sort_order', '');
                };
                var search_card_view = JSON.parse(Cookies.get('search_card_view'));
                var search_page_number = Number(Cookies.get('search_page_number'));
                var search_page_size = Cookies.get('search_page_size');
                var search_search_text = Cookies.get('search_search_text');
                var search_sort_name = Cookies.get('search_sort_name');
                var search_sort_order = Cookies.get('search_sort_order');
                $('#search_results_table').bootstrapTable({
                    cardView: search_card_view,
                    pageNumber: search_page_number,
                    pageSize: search_page_size,
                    searchText: search_search_text,
                    sortName: search_sort_name,
                    sortOrder: search_sort_order,
                    onPageChange: function (pageNumber, pageSize) {
                        Cookies.set('search_page_number', pageNumber);
                        Cookies.set('search_page_size', pageSize);
                    },
                    onSearch: function (searchText) {
                        Cookies.set('search_search_text', searchText);
                    },
                    onSort: function (sortName, sortOrder) {
                        Cookies.set('search_sort_name', sortName);
                        Cookies.set('search_sort_order', sortOrder);
                    },
                    onToggle: function (cardView) {
                        Cookies.set('search_card_view', cardView);
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

function ajax_request (params) {
    $.ajax({
        async: true,
        contentType: 'application/json',
        data: JSON.stringify({
            'token': window.token
        }),
        dataType: 'json',
        type: 'post',
        url: window.location.protocol + '//' + window.location.host + '/api_database_query_like?like_string=' + encodeURIComponent(url('?')['search_input']),
        success: function (api_database_query_like) {
            params.success(api_database_query_like.data);
        },
        error: function () {
            params.success([]);
        }
    });
};

function torrent_name_sorter (a, b) {
    a = a.replace(/(<\/?a.*?>)|(<\/?span.*?>)/g, '');
    b = b.replace(/(<\/?a.*?>)|(<\/?span.*?>)/g, '');
    return a.localeCompare(b, navigator.language)
};

function torrent_size_sorter (a, b) {
    var a = xbytes.parseSize(a);
    var b = xbytes.parseSize(b);
    return a - b
};