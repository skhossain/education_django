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
                const search_url = "/apiedu-fees-processing-api/";
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
                        { data: 'academic_year?.academic_year' },
                        { data: 'class_id?.class_name' },
                        { data: 'class_group_id?.class_group_name' },
                        { data: 'section_id?.section_name' },
                        { data: 'student_roll?.student_roll' },
                        { data: 'process_date' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger btn-sm">Delete</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

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
        //if (branch_code === "") {
        //   alert('Please Enter Branch Code!');
        // } else {
        new fn_data_table();
        //  }
    }

);

$(function() {

    $('#dt-table-list').on('click', 'button', function() {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['process_id']
        } catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['process_id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
        if (class_name == 'btn btn-danger btn-sm') {
            active_delete_button(id);
        }
    })



    function active_delete_button(id) {
        $.ajax({
            url: '/edu-fees-processing-delete/' + id,
            type: 'get',
            dataType: 'json',
            success: function(data) {
                if (data.success_message) {
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                    table_data.ajax.reload();
                }
            }
        })
    }

});

$('#btnAddRecord').click(function() {
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
        success: function(data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                document.getElementById("tran_table_data").reset();
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


$('#id_class_id').change(function() {
    class_group_filter()
})

function class_group_filter() {
    var class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function(data) {
            $("#id_class_group_id option").remove();
            $("#id_class_group_id").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_class_group_id").append('<option value="' + element.class_group_id + '">' + element.class_group_name + '</option>');
            });
        }
    })
}
$('#id_class_id').change(function() {
    class_section_filter()
})

function class_section_filter() {
    var class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-sectioninfo-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function(data) {
            $("#id_section_id option").remove();
            $("#id_section_id").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_section_id").append('<option value="' + element.section_id + '">' + element.section_name + '</option>');
            });
        }
    })
}
$(document).ready(function () {
    $('select').select2();
});