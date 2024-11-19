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
                const search_url = "/apihostel-addmeal-api";
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
                        { data: 'meal_id.meal_name' },
                        { data: 'student_roll.student_roll' },
                        { data: 'student_roll.student_name' },
                        { data: 'meal_status' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>'
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
        const meal_id = document.getElementById('id_meal_id').value;
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
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/hostel-addmeal-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#edit_model').modal('show');
            },
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form);
                if(data.error_message){
                    Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: data.error_message,
                        showConfirmButton: true,
                        })
                    };
            }
        })
    }

});



// $('#id_student_roll').change(function(){
//     student_basic_info()
// })

// function student_list(){
//     $.ajax({
//         url: "apiedu-studentinfo-api",
//         type: 'get',
//         datatype: 'json',
//         success: function (data) {
//            let list = $('#id_student_roll')
//            $('#id_student_roll option').remove();
//            list.append('<option value="">-----------</option>')
//            data.forEach(element => {
//             list.append('<option value="'+element.student_roll+'">'+element.student_roll+'</option>')
//            });
//         }
//     })
// }
// student_list()

$('#id_student_roll').select2({placeholder: "Select a student"})
$('#id_meal_id').select2({placeholder: "Select a meal"})
function student_basic_info(){
    let student_roll=document.getElementById('id_student_roll').value
    console.log(student_roll)
    $.ajax({
        url: "apiedu-studentinfo-api/?student_roll="+student_roll,
        type: 'get',
        datatype: 'json',
        success: function (data) {
           var html='<div class="form-row">\
           <div class="form-group col-md-3 mb-0">\
             <strong>Student Roll</strong>\
           </div>\
           <div class="form-group col-md-3 mb-0">\
             <strong>Student Name</strong>\
           </div>\
           <div class="form-group col-md-3 mb-0">\
             <strong>Academic Year</strong>\
           </div>\
       </div>\
       <div class="form-row">\
           <div class="form-group col-md-3 mb-0">\
               '+data[0].student_roll+' \
           </div>\
           <div class="form-group col-md-3 mb-0">\
           '+data[0].student_name+'\
           </div>\
           <div class="form-group col-md-3 mb-0">\
           '+data[0].academic_year.academic_year+'\
           </div>'
           document.getElementById('table-data').innerHTML=html
        }
    })
} 



function add_meal_student_list(){
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    $.ajax({
        url: data_url,
        data:data_string,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            if(data.error_message){
                Swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: data.error_message,
                    showConfirmButton: true,
                    })
                }
            else{
                Swal.fire({
                position: 'top-center',
                icon: 'success',
                title: 'Student to Meal Adding Successfully',
                showConfirmButton: false,
                timer: 1000
              })

            
            $('#id_student_roll').val('').trigger('change')
            // $('#id_meal_id').val('').trigger('change')
            // student_list()
            setTimeout(() => {
                $('#id_student_roll').val('')
                document.getElementById('table-data').innerHTML="" //after adding info button click then value null
            }, 500);
        }
    }
    })
}
