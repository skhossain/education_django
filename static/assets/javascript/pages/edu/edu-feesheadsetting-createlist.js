"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (let i = 0; i < props.length; i++) { let descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

let table_data

const fn_data_table =
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
                const search_url = "/apiedu-feesheadsetting-api/";
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": ""
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
                    language: {
                        paginate: {
                            previous: '<i class="fa fa-lg fa-angle-left"></i>',
                            next: '<i class="fa fa-lg fa-angle-right"></i>'
                        }
                    },
                    columns: [
                        { data: 'head_code' },
                        { data: 'head_name' },
                        { data: 'parent_head' },
                        { data: 'head_ledger' },
                        { data: 'is_main_head' },
                        { data: 'head_comments' },
                        { data: 'is_active' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button> <button type="button" class="btn btn-danger btn-sm">Delete</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

$(document).ready(function () {
    $('#id_head_ledger').select2();
    $('#id_parent_head').select2();
	refresh_ledger_list();
});

function refresh_ledger_list() {
	var url = '/finance-choice-allledgerlist';
	$.ajax({
		url: url,
		success: function (data) {
			$("#id_head_ledger").html(data);
		}
	});
	return false;
}


$('#btnSearch').click(
    function () {
        new fn_data_table();
    }
);

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['head_code']
        }
        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['head_code']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
        if (class_name == 'btn btn-danger btn-sm') {
            active_is_delete(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/edu-feesheadsetting-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#edit_model').modal('show');
            },
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }



    function active_is_delete(id) {
        $.ajax({
            url: '/edu-feesheadsetting-delete/' + id,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if(data.success_message){
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                      })
                }
            }
        })
    }

});

$('#btnAddRecord').click(function () {
    post_tran_table_data();
});

function post_tran_table_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                document.getElementById("tran_table_data").reset();
                table_data.ajax.reload();
                if(data.success_message){
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                };
                location.reload();
            } else {
                $('#page_loading').modal('hide');
                if(data.error_message){
                    Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: data.error_message,
                        showConfirmButton: true,
                        })
                    };
            }
        }
    })
    return false;
}