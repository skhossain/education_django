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
                const search_url = "/apitransport-admit-transportation-api/";
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
                        { data: 'admit_transportation_id' },
                        { data: 'transportation_id.transportation_name' },
                        { data: 'academic_year' },
                        { data: 'class_id.class_name' },
                        { data: 'student_roll' },
                        { data: 'location_info_id' },
                        { data: 'transportation_fees' },
                        { data: 'discount' },
                        { data: 'starting_date' },
                        { data: 'status' },
                        { data: 'comments' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>'
                        }
                    ],
                    columnDefs: [{
                        "defaultContent": "-",
                        "targets": "_all"
                    }],
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

$('#btnSearch').click(

    function () {
        //if (branch_code === "") {
        //   alert('Please Enter Branch Code!');
        // } else {
        new fn_data_table();
        //  }
    }

);

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['admit_transportation_id']
        }
        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['admit_transportation_id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/transport-admit-transportation-edit/' + id,
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

});

$('#btnAddRecord').click(function () {
    post_tran_table_data();
});
// Select 2
$('#id_transportation_id').select2({placeholder: "Select a transportation name"})
$('#id_academic_year').select2({placeholder: "Select a year"})
$('#id_class_id').select2({placeholder: "Select a class"})
$('#id_student_roll').select2({placeholder: "Select a class"})

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
                // document.getElementById("tran_table_data").reset();
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
                // $('#id_transportation_id').val('').trigger('change')
                // $('#id_academic_year').val('').trigger('change')
                // $('#id_class_id').val('').trigger('change')
                // $('#id_student_roll').val('').trigger('change')
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





$('#id_class_id').change(function(){
    filtering_studentsroll()
})


function filtering_studentsroll(){
var class_id=document.getElementById('id_class_id').value

$.ajax({
    url: "apiedu-studentinfo-api/?class_id="+class_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_student_roll option").remove();
        data.forEach(element => {
            $("#id_student_roll").append('<option value="'+element.student_roll+'">'+element.student_name+'</option>');
        });
        // console.log(data)
    }
})
}


$('#id_class_id').change(function(){
    filtering_students()
})


function filtering_students(){
var class_id=document.getElementById('id_class_id').value

$.ajax({
    url: "apiedu-studentinfo-api/?class_id="+class_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_student_roll option").remove();
        $("#id_student_roll").append('<option value="">-------------</option>');
        data.forEach(element => {
            $("#id_student_roll").append('<option value="'+element.student_roll+'">'+element.student_name+'-'+element.student_roll+'</option>');
        });
        // console.log(data)
    }
})
}

$('#id_academic_year').change(function(){
    filtering_roll()
})


function filtering_roll(){
var academic_year=document.getElementById('id_academic_year').value

$.ajax({
    url: "apiedu-studentinfo-api/?academic_year="+academic_year,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_student_roll option").remove();
        data.forEach(element => {
            $("#id_student_roll").append('<option value="'+element.student_roll+'">'+element.student_name+'</option>');
        });
        // console.log(data)
    }
})
}
