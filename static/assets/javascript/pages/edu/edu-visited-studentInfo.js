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
                let class_id=document.getElementById('id_class_id').value
                let class_group_id=document.getElementById('id_class_group_id').value
                let student_phone=document.getElementById('id_student_phone').value
                const search_url = "/apiedu-visited-studentInfo-api/?class_id="+class_id+"&class_group_id="+class_group_id+"&student_phone="+student_phone;
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
                    columnDefs: [{
                        "defaultContent": "-",
                        "targets": "_all"
                    }],
                    columns: [
                        { data: 'student_name' },
                        { data: 'class_id.class_name' },
                        { data: 'class_group_id.class_group_name' },
                        { data: 'student_present_address' },
                        { data: 'student_phone' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-dark btn-sm"> <i class="fas fa-eye"></i> </button>\
                            <button type="button" class="btn btn-info btn-sm"> <i class="fas fa-edit"></i> </button>\
                            <button type="button" class="admit btn btn-info btn-sm"> <i class="fas fa-plus"></i> </button>\
                            <button type="button" class="deleted_button btn btn-danger btn-sm"> <i class="fas fa-trash"></i> </button>'
                    
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
            id = table_row['id']
        }
        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-dark btn-sm') {
            fn_view(id);
        }
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
        if (class_name == 'admit btn btn-info btn-sm') {
            goto_student_info(id);
        }
        if (class_name == 'deleted_button btn btn-danger btn-sm') {
            fn_deleted_row(id);
        }
    })
function fn_view(id){
    $.ajax({
        url: '/edu-visited-studentinfo-view/' + id,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
            $('#view_model').modal('show');
        },
        success: function (data) {
            $('#view_model .modal-content').html(data.html_form);
        }
    })
}

    function show_edit_form(id) {
        $.ajax({
            url: '/edu-visited-studentinfo-edit/' + id,
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

    function goto_student_info(id) {
        window.location.href='/edu-studentinfo-createlist?visited=' + id
    }

    function fn_deleted_row(id){
        $.ajax({
            url: '/edu-visited-studentinfo-delete/' + id,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                table_data.ajax.reload();
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
    class_group_filter()
})

function class_group_filter(){
var class_id=document.getElementById('id_class_id').value
$.ajax({
    url: "apiedu-academicgroup-api/?class_id="+class_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_class_group_id option").remove();
        $("#id_class_group_id").append('<option value="">----------</option>');
        data.forEach(element => {
            $("#id_class_group_id").append('<option value="'+element.class_group_id+'">'+element.class_group_name+'</option>');
        });
    }
})
}

var edu_degree_list=""
var institute_list=""
function get_edu_degrees(){
    // apiedu-degree-api/
    $.ajax({
        url: "apiedu-degree-api/",
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var select_option='<option value="">------</option>'
            data.forEach(option=>{
                select_option+='<option value="'+option.degree_id+'">'+option.degree_name+'</option>'
            })
            edu_degree_list=select_option;
            $('#id_edu_degree_list').append(edu_degree_list)
        }
    })
}

function get_institute(){
    // apiedu-degree-api/
    $.ajax({
        url: "apiedu-education-institute-api/",
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var select_option='<option value="">------</option>'
            data.forEach(option=>{
                select_option+='<option value="'+option.institute_id+'">'+option.institute_name+'</option>'
            })
            institute_list=select_option;
            $('#id_institute_list1').append(institute_list)
        }
    })
}
get_edu_degrees()
get_institute()
var edu_count=1;
$('#addnewEdu').click(function (){
    edu_count+=1;
    $('#id_edu_count').val(edu_count)
    var html_data='<div class="form-row">\
    <div class="form-group col-md-2 mb-0">\
        <label>Degree Name</label>\
        <select name="degree'+edu_count+'" class="form-control edu_degree_list">'+edu_degree_list+'</select>\
    </div>\
    <div class="form-group col-md-2 mb-0">\
        <label>Board Name</label>\
        <input type="text" name="board'+edu_count+'" placeholder="Dhaka" class="form-control">\
    </div>\
    <div class="form-group col-md-1 mb-0">\
        <label>Point</label>\
        <input type="number" name="point'+edu_count+'" placeholder="5.00" class="form-control">\
    </div>\
    <div class="form-group col-md-1 mb-0">\
        <label>Grate</label>\
        <input type="text" name="grate'+edu_count+'" placeholder="A+" class="form-control">\
    </div>\
    <div class="form-group col-md-2 mb-0">\
        <label>Passing Year</label>\
        <input type="text" name="year'+edu_count+'" placeholder="2018" class="form-control">\
    </div>\
    <div class="form-group col-md-4 mb-0">\
        <label>Institute Name</label>\
        <div class="d-flex">\
            <select name="institute'+edu_count+'" id="id_institute_list'+edu_count+'" class="form-control edu_degree_list institute_name">'+institute_list+'</select>\
            <button class="btn btn-dark" data-value="'+edu_count+'" style="margin: 0px 5px;" type="button" onclick="show_blank_form(this)"><i class="fas fa-plus"></i></button>\
        </div>\
    </div>\
</div>'
$('#Edu-qualification').append(html_data)
$('#Edu-qualification select').select2();
})

// New Education Institute
function show_blank_form(button) {
    let button_number = $(button).attr('data-value')
      $.ajax({
          url: '/edu-visited-institute',
          type: 'get',
          beforeSend: function () {
              $('#edit_model').modal('show');
          },
          success: function (data) {
              $('#edit_model .modal-content').html(data);
              $('#new-institute').val(button_number)
          }
      })
  }

function New_institute(){
    var institute = $("#id_institute_name").val();
    var institute_code = $("#id_institute_code").val();
    var institute_address = $("#id_institute_address").val();
    var institute_contact = $("#id_institute_mobile").val();
    var lowest_degree = $("#id_lower_degree").val();
    var highest_degree = $("#id_higher_degree").val();

    var data_string={
        institute:institute,
        institute_code:institute_code,
        institute_address:institute_address,
        institute_contact:institute_contact,
        lowest_degree:lowest_degree,
        highest_degree:highest_degree

    }
    
    $.ajax({
        url: "/edu-visited-institute-insert",
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if(data.success_message){
                let row_id=$('#new-institute').val()
                let button_number=Number(row_id)
                $('#edit_model').modal('hide')
                let option2='<option value="'+data.new_institute.institute_id+'">'+data.new_institute.institute_name+'</option>'
                $('.institute_name').append(option2)
                institute_list+=option2
                if(button_number>0){
                    var institute_options=document.getElementById("id_institute_list"+button_number).options
                    console.log(institute_options)
                    for (let index = 0; index < institute_options.length; index++) {
                    if(institute_options[index] && data.new_institute.institute_id==institute_options[index].value){
                        institute_options[index].setAttribute("selected","selected")
                    }	
                }
                }
            }
        }
    })
    return false;
}


$(document).ready(function() {
    $('#Edu-qualification select').select2();
    $('#id_class_id').select2({placeholder: " Select a class "});
    $('#id_class_group_id').select2({placeholder: " Select a group name "});
});