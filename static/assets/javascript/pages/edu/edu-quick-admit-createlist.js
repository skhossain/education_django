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
                const search_url = "/apiedu-studentinfo-api/";
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
                        { data: 'branch_code' },
                        { data: 'academic_year.academic_year' },
                        { data: 'session_id.session_name' },
                        { data: 'catagory_id.catagory_name' },
                        { data: 'student_roll' },
                        { data: 'class_roll' },
                        { data: 'student_reg' },
                        { data: 'student_name' },
                        { data: 'student_nick_name' },
                        { data: 'class_id' },
                        { data: 'class_group_id' },
                        { data: 'shift_id' },
                        { data: 'last_institute_id' },
                        { data: 'student_type' },
                        { data: 'student_referred_by' },
                        { data: 'student_father_name' },
                        { data: 'father_occupation_id' },
                        { data: 'father_email_address' },
                        { data: 'father_phone_number' },
                        { data: 'father_nid' },
                        { data: 'father_address' },
                        { data: 'sms_to_father' },
                        { data: 'student_mother_name' },
                        { data: 'mother_occupation_id' },
                        { data: 'mother_email_address' },                        
                        { data: 'mother_phone_number' },
                        { data: 'mother_nid' },
                        { data: 'mother_address' },
                        { data: 'sms_to_mother' },
                        { data: 'student_blood_group' },
                        { data: 'student_gender' },
                        { data: 'student_religion' },
                        { data: 'student_marital_status' },
                        { data: 'student_national_id' },
                        { data: 'student_birth_cert' },
                        { data: 'student_present_address' },
                        { data: 'student_permanent_address' },
                        { data: 'student_phone' },
                        
                        { data: 'student_email' },
                        { data: 'student_joining_date' },
                        { data: 'student_date_of_birth' },
                        { data: 'student_status' },
                        { data: 'student_comments' },
                        { data: 'legal_guardian_name' },
                        { data: 'legal_guardian_contact' },
                        { data: 'legal_guardian_relation' },
                        { data: 'legal_guardian_nid' },
                        { data: 'legal_guardian_occupation_id' },
                        { data: 'legal_guardian_address' },
                        { data: 'local_guardian_name' },
                        { data: 'local_guardian_contact' },
                        { data: 'local_guardian_relation' },
                        { data: 'local_guardian_nid' },
                        { data: 'local_guardian_occupation_id' },
                        { data: 'local_guardian_address' },
                        { 
                            "data": 'student_roll',
                            "render": function(data, type, row, meta){
                            data = '<a class="btn btn-info btn-sm" href="/edu-studentinfo-list-edit/'+data+'" target="_blank">Edit</a>';
                            return data;
                         }
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

$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['student_roll']
        }
        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['student_roll']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/edu-registrationform-edit/' + id,
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

function post_tran_table_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    loder_Spinner(true)
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                document.getElementById("tran_table_data").reset();
                $('select').val('').trigger('change')
                loder_Spinner(false)
                if(data.success_message){
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                }
                document.getElementById('auto_row').innerHTML =""
            } else {
                $('#page_loading').modal('hide');
                loder_Spinner(false)
                alert(data.error_message);
            }
        }
    })
    return false;
}


function auto_row_create(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var catagory_id=document.getElementById('id_catagory_id').value
    var session_id=document.getElementById('id_session_id').value
    var row_no_id=document.getElementById('row_no_id').value
    let new_row=parseInt(row_no_id)   
      
    
    if (academic_year && class_id && new_row<=50 ){
        var html=""
        for (let text = 1; text <= new_row; text++) {
            html+='<tr>\
      <td><input type="text" name="class_roll'+text+'" class="form-control" placeholder="2021012"></td>\
      <td><input type="text" name="student_name'+text+'" class="form-control" placeholder="Monir Hossain" required></td>\
      <td><input type="text" name="f_name'+text+'" class="form-control" placeholder="Afjal Miya" required></td>\
      <td><input type="text" name="m_name'+text+'" class="form-control" placeholder="Monira Sultana" required></td>\
      <td><input type="text" name="mobile_no'+text+'" class="form-control" placeholder="01xxxxxxx" required></td>\
      <td width="110px">\
      <select class="form-control" name="gender'+text+'" required>\
          <option value="M">Male</option>\
          <option value="F">Female</option>\
          <option value="O">Other</option>\
      </select> \
        </td>\
      <td><input style="width:160px" id="j-date'+text+'" type="date" name="admission'+text+'" class="form-control" required></td>\
      <td><input style="width:160px" id="b-date'+text+'" type="date" name="birthday'+text+'" class="form-control" required></td>\
      </tr>'
            }
           
        var table='<p style="color:red;background-color:#dddddd; padding:10px;margin-bottom: 0rem;">Students Information (Fill-up All Required Fields)</p>\
        <table class="table table-sm table-responsive table-bordered">\
          <tr>\
              <td>Roll No.</td>\
              <td>Student Name <sup class="text-danger">*</sup></td>\
              <td>Fathers Name <sup class="text-danger">*</sup></td>\
              <td>Mothers Name <sup class="text-danger">*</sup></td>\
              <td>Mobile No. <sup class="text-danger">*</sup></td>\
              <td>Gender <sup class="text-danger">*</sup></td>\
              <td>Admission Date <sup class="text-danger">*</sup></td>\
              <td>Birthday <sup class="text-danger">*</sup></td>\
          </tr>\
          '+html+'\
          </table>\
          <button type="button" class="float-right btn btn-info" onclick="post_tran_table_data()">Save Info</button>'
          document.getElementById('auto_row').innerHTML = table
          for (let text = 1; text <= new_row; text++){
            off_future_date('j-date'+text)
            off_future_date('b-date'+text)
          }
    }
    else{
        var error='<h1 style="color:red;background-color:#dddddd;padding:10px;">Please Check Necessary Field</h1>'
        document.getElementById('auto_row').innerHTML=error
    }
}

$('#id_class_id').change(function(){
    filtering_grouplist()  
})


function filtering_grouplist(){
    let class_id=document.getElementById('id_class_id').value
    let academic_year=document.getElementById('id_academic_year').value

    $.ajax({
        url: "apiedu-academicgroup-api/?class_id="+class_id+"&academic_year="+academic_year,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_class_group_id option").remove();
            $("#id_class_group_id").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#id_class_group_id").append('<option value="'+element.class_group_id+'">'+element.class_group_name+'</option>')
            });
        }
    })
}


$(document).ready(() => {
    // Select 2 
$('select').select2()
})