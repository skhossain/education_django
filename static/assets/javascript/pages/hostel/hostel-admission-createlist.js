$(document).ready(function() {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function() {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) {
    for (let i = 0; i < props.length; i++) {
        let descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

let table_data

const fn_data_table =
    function() {
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
                let student_roll = document.getElementById('id_student_roll').value;
                let academic_year = document.getElementById('id_academic_year').value;
                let branch_code = document.getElementById('id_branch_code').value;
                const search_url = "/apihostel-admission-api/?academic_year=" + academic_year + "&student_roll=" + student_roll + "&branch_code=" + branch_code;
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
                        {
                            data: 'admit_date',
                            "render": function(data, type, row, meta) {
                                let newDate = moment(data).format('MMMM Do YYYY');
                                return newDate;
                            }
                        },
                        { data: 'admit_fees' },
                        { data: 'admit_status' },
                        { data: 'discount' },
                        { data: 'cancel_by' },
                        { data: 'cancel_on' },
                        { data: 'app_user_id' },
                        { data: 'app_data_time' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger btn-sm">Cancel</button>' + '&nbsp' +
                                '<button type="button" class="btn btn-primary btn-sm">Edit</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

let admit_id = 0
$(document).ready(function() {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function() {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});
$('#btnSearch').click(

    function() {
        const academic_year = document.getElementById('id_academic_year').value;
        let branch_code = document.getElementById('id_branch_code').value;

        if (academic_year && branch_code) {
            new fn_data_table();
        } else {
            alert("Please Select Academic Year and Branch!");
        }
    }

);

$(function() {

    $('#dt-table-list').on('click', 'button', function() {

        try {
            const table_row = table_data.row(this).data();
            admit_id = table_row['admit_id']
        } catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            admit_id = table_row['admit_id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-danger btn-sm') {
            cancel_transaction(admit_id);
        }

        if (class_name == 'btn btn-primary btn-sm') {
            show_edit_form(admit_id);
        }
    })


    function show_edit_form(id) {
        $.ajax({
            url: 'hostel-admission-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function() {
                $('#edit_model').modal('show');
            },
            success: function(data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }

    function cancel_transaction(admit_id) {
        Swal.fire({
            title: 'Are you sure?',
            text: "Are you sure you want to cancel this Admission?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, cancel it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $("#page_loading").modal("show");
                $.ajax({
                    url: "/hostel-admission-cancel/" + admit_id,
                    type: "POST",
                    success: function(data) {
                        if (data.form_is_valid) {
                            $("#page_loading").modal("hide");
                            Swal.fire(
                                'Canceled!',
                                data.success_message,
                                'success'
                            )
                            table_data.ajax.reload();
                        } else {
                            $("#page_loading").modal("hide");
                            Swal.fire(
                                'Sorry!',
                                data.error_message,
                                'error'
                            )
                            table_data.ajax.reload();
                        }
                    },
                });

            }
        })
    }


});

$('#btnAddRecord').click(function() {
    post_tran_table_data();
});

// Select 2
$('#id_academic_year').select2({ placeholder: "Select a year" })
$('#id_student_roll').select2({ placeholder: "Select a student" })
$('#id_branch_code').select2({ placeholder: "Select a Branch" })


function post_tran_table_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                // document.getElementById("tran_table_data").reset();
                $('#id_admit_fees').val('')
                $('#id_discount').val('')
                $('#id_student_roll').val('').trigger('change')
                table_data.ajax.reload();
                if (data.success_message) {
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                };

            } else {
                $('#page_loading').modal('hide');
                if (data.error_message) {
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


var student_roll = ''
$('#id_academic_year').change(function() {
    var academic_year = document.getElementById('id_academic_year').value
    if (academic_year) {
        $.ajax({
            url: '/apiedu-studentinfo-api/?academic_year=' + academic_year,
            type: "GET",
            success: function(data) {
                var test_data = [];
                data.forEach((element, index) => {
                    let item = {
                        id: element.student_roll,
                        text: element.student_roll
                    }
                    test_data.push(item)
                    if (data.length == index + 1) {
                        $('#id_student_roll').val(null).trigger('change');
                        $("#id_student_roll").select2({
                            data: test_data
                        })
                    }
                });
            },
        });
    }
})