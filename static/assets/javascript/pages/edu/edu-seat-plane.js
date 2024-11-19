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
                let class_id = $('#id_class_id').val()
                let academic_year = $('#id_academic_year').val()
                let class_group_id = $('#id_class_group_id').val()
                let student_roll = $('#id_student_roll').val()
                const search_url = "/apiedu-seatplane-api/?class_id="+class_id+"&academic_year="+academic_year+"&class_group_id="+class_group_id+"&student_roll="+student_roll;
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
                        { data: 'class_id.class_name' },
                        { data: 'class_group_id.class_group_name' },
                        { data: 'academic_year.academic_year' },
                        { data: 'term_id.term_name' },
                        { data: 'branch_code' },
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
            url: '/edu-seat-plane-edit/' + id,
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
let academic_info=""
$.ajax({
    url: 'apiedu-academic-info-api/',
    type: 'GET',
    dataType: 'json',
    success: function (data) {
        academic_info=data[0]
    }
})

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

$(document).ready(function() {
    $('#id_student_roll').select2({placeholder: " Select a Student "});
    $('#id_class_id').select2({placeholder: " Select a Class "});
    $('#id_academic_year').select2({placeholder: " Select a Year "});
    $('#id_class_group_id').select2({placeholder: " Select a Group "});
});



$('#PDFCreate').click(function () {
    let class_id = $('#id_class_id').val()
    let academic_year_id = $('#id_academic_year').val()
    let class_group_id = $('#id_class_group_id').val()
    let student_roll = $('#id_student_roll').val()
    var pdf = new jsPDF('p', 'mm', 'a4');
    let logo=""
    let download=false;
    if(class_id && academic_year_id){
        toDataURL(academic_info.academic_logo, function(dataUrl) {
            if(isImage(dataUrl)){
            logo=dataUrl
            }
        })
       let  data_string={
        class_id:class_id,
        academic_year:academic_year_id,
        class_group_id:class_group_id,
        }
        $.ajax({
            url: '/apiedu-seatplane-api/?',
            data: data_string,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
            if(data.length>0){
            let y=3;
            let x=0;
            let row=1;
            data.forEach((student,index) => {
                pdf.rect(10+x,4+y, 88,45)
                pdf.addImage(logo,'png',11+x,7+y,10,10)
                pdf.setFontSize(11)
                pdf.setFontStyle('bold');
                pdf.text(academic_info.academic_name.toUpperCase(),59+x,12+y,{align: 'center'})
                pdf.setFontStyle('normal');
                pdf.setFontSize(9)
                pdf.text(academic_info.academic_address,59+x,15+y,{align: 'center'})
                pdf.setFontStyle('bold');
                pdf.setFontSize(11)
                
                pdf.text("Exam: "+student.term_id.term_name,55+x,22+y,{align: 'center'})
                pdf.setFontStyle('normal');
                pdf.setFontSize(10)
                pdf.text("Student ID",20+x,28+y)
                pdf.text(": "+student.student_roll.student_roll,40+x,28+y)
                pdf.text("Class",20+x,32+y)
                pdf.text(": "+student.class_id.class_name,40+x,32+y)
                pdf.text("Year",20+x,36+y)
                pdf.text(": "+student.academic_year.academic_year,40+x,36+y)
                pdf.text("Class Roll",20+x,40+y)
                pdf.text(": "+student.student_roll.class_roll,40+x,40+y)
                if(student.class_group_id){
                    pdf.text("Group",20+x,44+y)
                    pdf.text(": "+student.class_group_id.class_group_name,40+x,44+y)
                }

                x=x+95
                if((index+1)%2 == 0){
                    x=0
                    y=(row*55)+3
                    row+=1
                }
                   
                if(row == 6){
                    y=3
                    row=1
                    pdf.addPage("a4");
                }
                
                    if(data.length==index+1){
                        setTimeout(() => {  
                            pdf.save("seat-plane"+Date.now()+'.pdf')
                        }, 100);
                    }     
            });
           
            }
        else{
            Swal.fire({
                position: 'center',
                icon: 'error',
                title: 'There is no data in this filter .',
                showConfirmButton: true,
                })
        }
        }
        })
    }
    else{
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Please Select Year and Class .',
            showConfirmButton: true,
            })
    }

});

function toDataURL(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
       var reader = new FileReader();
       reader.onloadend = function() {
          callback(reader.result);
       }
       reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();    
 }
 
 function isImage(data){
     let mim=data.split(';')
     mim[0].slice(5)
     let image_exe=['image/gif', 'image/png', 'image/jpeg','image/jpg', 'image/bmp', 'image/webp']
     if(image_exe.indexOf(mim[0].slice(5))<0){
         return false
     }else{
         return true
     }
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

$('#id_class_id').change(function(){
    class_student_filter()
})
function class_student_filter(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var student_roll=document.getElementById('id_student_roll').value
    var datastring={
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        student_roll:student_roll,
    }
    $.ajax({
        url: "apiedu-studentinfo-api/",
        data:datastring,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_student_roll option").remove();
            $("#id_student_roll").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_student_roll").append('<option value="'+element.student_roll+'">'+element.student_roll+'-'+element.student_name+'</option>');
            });
        }
    })
}
