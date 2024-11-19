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
                var branch_code = document.getElementById('id_branch_code').value;
                var from_date = document.getElementById('id_from_date').value;
                var upto_date = document.getElementById('id_upto_date').value;
                var student_roll = document.getElementById('id_student_roll').value;
                var search_url = "/apiedu-quickreceive-api/?student_roll=" + student_roll + "&from_date=" + from_date + "&upto_date=" + upto_date
                    + "&branch_code=" + branch_code;
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
                        { data: 'student_roll.student_roll' },
                        { data: 'student_roll.student_name' },
                        { data: 'receive_date' },
                        { data: 'receive_amount' },
                        { data: 'cancel_by' },
                        { data: 'cancel_on' },
                        { data: 'app_user_id' },
                        { data: 'app_data_time' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Print</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-danger btn-sm">Cancel</button>'

                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

let transaction_id = 0
let w_branch_code = 0;
let id = 0

$(document).ready(function () {
   if ($("#id_branch_code").prop("tagName") == 'SELECT') {
		$("#id_branch_code").select2();
	}
    refresh_branch_list('');
    let branch_code = document.getElementById('id_global_branch_code').value;
    w_branch_code = branch_code
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
    w_branch_code = global_branch_code
});

$("#id_branch_code").on("change", function () {
    let branch_code = document.getElementById('id_branch_code').value;
    w_branch_code = branch_code;
});

$('#btnSearch').click(

    function () {
        //if (branch_code === "") {
        //   alert('Please Enter Branch Code!');
        // } else {
        new fn_data_table();
        //  }
    }

);

$('#dt-table-list').on('click', 'button', function () {
    try {
        const table_row = table_data.row(this).data();
        transaction_id = table_row['transaction_id']
        id = table_row['id']
    }
    catch (e) {
        const table_row = table_data.row($(this).parents('tr')).data();
        transaction_id = table_row['transaction_id']
        id = table_row['id']
    }
    var class_name = $(this).attr('class');
    if (class_name == 'btn btn-info btn-sm') {
        print_voucher(transaction_id);
    }
    if (class_name == 'btn btn-danger btn-sm') {
        cancel_transaction(id);
    }
})

function cancel_transaction(id) {
    $("#page_loading").modal("show");
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, Cancel it!',
      }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: "/edu-quick-collection-cancel/" + id,
                type: "POST",
                success: function (data) {
                    if (data.form_is_valid) {
                        $("#page_loading").modal("hide");
                        Swal.fire(
                            'Cancel!',
                            data.success_message,
                            'success'
                          )
                        table_data.ajax.reload();
                    } else {
                        $("#page_loading").modal("hide");
                        Swal.fire(
                            'Cancel!',
                            data.error_message,
                            'error'
                          )
                        table_data.ajax.reload();
                    }
                },
            });
        }else{
            $("#page_loading").modal("hide");
        }
      })
        Swal.getConfirmButton().blur()
        Swal.getCancelButton().focus()


}

function print_voucher(p_transaction_id) {
    var data_url = 'appauth-report-submit/';
    var report_name = 'edu_quickreceive_voucher';
    var report_data = { 'p_transaction_id': p_transaction_id };
    report_data = JSON.stringify(report_data);
    console.log(report_data)
    $.ajax({
        url: data_url,
        data: {
            'report_name': report_name,
            "report_data": report_data
        },
        cache: "false",
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                window.open(data.report_urls + '/edu-quick-collection-printview', "_blank");
            }
            else {
                alert(data.error_message)
            }
        }
    })
    return false;
}
