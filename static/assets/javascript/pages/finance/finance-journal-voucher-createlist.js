"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data

var fn_data_table =
    function () {
        function fn_data_table() {
            _classCallCheck(this, fn_data_table);

            this.init();
        }

        _createClass(fn_data_table, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    "ajax": {
                        "url": "/apifinance-journal-voucher-api/",
                        "type": "GET",
                        "dataSrc": ""
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n        <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
                    language: {
                        paginate: {
                            previous: '<i class="fa fa-lg fa-angle-left"></i>',
                            next: '<i class="fa fa-lg fa-angle-right"></i>'
                        }
                    },
                    columns: [
                        { data: 'gl_code' },
                        { data: 'gl_name' },
                        { data: 'tran_amount' },
                        { data: 'transaction_comments' },
                        { data: 'tran_document_number' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger show-form-update"> <span class="glyphicon glyphicon-pencil"></span>Remove</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0

$(document).on('theme:init', function () {
    new fn_data_table();
});

$(document).ready(function () {
    $("#id_batch_gl_code").select2();
    $("#id_gl_code").select2();
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
    transaction_cashnbanklist_list();
    refresh_ledger_list();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function transaction_cashnbanklist_list(branch_code) {
    var url = '/finance-choice-cashnbanklist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_batch_gl_code").html(data);
        }
    });
    return false;
}

function refresh_ledger_list() {
    var url = '/finance-choice-allledgerlist';
    $.ajax({
        url: url,
        success: function (data) {
            $("#id_gl_code").html(data);
        }
    });
    return false;
}

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['id']
        } catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
        }

        var class_name = $(this).attr('class');
        if (class_name == 'btn btn-warning show-form-update') {
            show_edit_product_data(id)
        }

        if (class_name == 'btn btn-danger show-form-update') {
            if (confirm('Are you sure you want to remove this item?') == true) {
                temp_details_delete(id)
            }
        }

    })

    function temp_details_delete(id) {
        $.ajax({
            url: '/finance-journal-voucher-delete/' + id,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#id_total_amount').val(data.total_amount);
                    table_data.ajax.reload();
                } else {
                    table_data.ajax.reload();
                }
            }
        })
        return false;
    }

});

$(function () {
    $('#btnAddItem').click(function () {
        post_tran_table_data();

    });
});

$(function () {
    $('#btn_voucher_post').click(function () {
        post_journal_master_data();

    });
});

function post_tran_table_data() {
    var data_string = $("#voucher_insert").serialize();
    var data_url = $("#voucher_insert").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                document.getElementById("voucher_insert").reset();
                $('#id_total_amount').val(data.total_amount);
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
                $('#id_tran_amount').val('');
                $('#id_gl_code').val('');
                var gl_code = document.getElementById("select2-id_gl_code-container");
                gl_code.textContent = "------------";
            } else {
                Swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: data.error_message,
                })
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
            }
        }
    })
    return false;
}

function post_journal_master_data() {
    var data_string = $("#voucher_post").serialize();
    var data_url = $("#voucher_post").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                alert(data.message);
                document.getElementById("voucher_post").reset();
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
                var global_branch_code = document.getElementById('id_global_branch_code').value;
                $('#id_branch_code').val(global_branch_code);
                var batch_gl_code = document.getElementById("select2-id_batch_gl_code-container");
                batch_gl_code.textContent = "-----------";
                $('#id_total_amount').val(0.00);
            } else {
                Swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: data.error_message,
                })
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
            }
        }
    })
    return false;
}

function temp_details_delete_all() {
    if (confirm('Are you sure you want to remove all items?') == true) {
        $.ajax({
            url: '/finance-journal-voucher-delete-all',
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#id_total_amount').val(0.00);
                    table_data.ajax.reload();
                } else {
                    table_data.ajax.reload();
                }
            }
        })
        return false;
    }
}