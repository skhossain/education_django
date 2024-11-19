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
                const mobile_number = document.getElementById('id_mobile_number').value;
                const search_url = "/apisms-que-api/?mobile_number=" + mobile_number;
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
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
                        { data: 'mobile_number' },
                        { data: 'text_message' },
                        { data: 'app_user_id' },
                        { data: 'app_data_time' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-danger btn-sm">Delete</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

$('#btnSearch').click(

    function () {

        new fn_data_table();
    }

);

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['id']
        }
        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }

        if (class_name == 'btn btn-danger btn-sm') {
            delete_request(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/sms-que-form-edit/' + id,
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

    function delete_request(id) {
        if (confirm('Are you sure you want to delete this Request?') == true) {
            $('#page_loading').modal('show');
            $.ajax({
                url: "/sms-que-delete/" + id,
                type: "POST",
                success: function (data) {
                    if (data.form_is_valid) {
                        $('#page_loading').modal('hide');
                        Swal.fire({
                            position: 'top-center',
                            icon: 'success',
                            title: data.success_message,
                            showConfirmButton: false,
                            timer: 1500
                        })
                    } else {
                        $('#page_loading').modal('hide');
                        Swal.fire({
                            position: 'top-center',
                            icon: 'error',
                            title: data.error_message,
                        })
                    }
                    table_data.ajax.reload();
                }
            })
        }
    }


});

$('#btnAddItem').click(function () {
    post_tran_table_data();
});

function post_tran_table_data() {
    var data_string = $("#tran_table_data").serialize();
    var data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_sms_balance').val(data.balance);
                document.getElementById("tran_table_data").reset();
                $('#page_loading').modal('hide');
                alert(data.success_message);
                table_data.ajax.reload();
            } else {
                $('#page_loading').modal('hide');
                $('#id_sms_balance').val(data.balance);
                alert(data.error_message);

            }
        }
    })
    return false;
}
