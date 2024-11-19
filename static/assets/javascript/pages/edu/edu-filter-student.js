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
var global_branch_code = ""
$(window).on('load', function() {
    global_branch_code = document.getElementById('id_global_branch_code').value;
});

$("#btnAddRecord").click(function () {
      students_report();
});

function students_report() {
  const data_url = $("#tran_table_data").attr("data-url");
  let id_academic_year = $("#id_academic_year").val();
  let id_class_name = $("#id_class_name").val();
  let id_class_group_id = $("#id_class_group_id").val();
  let id_gender = $("#id_gender").val();
  let id_branch_code = $("#id_branch_code").val();
  if(id_branch_code){
  let dataurl = (
    data_url +
    "?gender=" +
    id_gender +
    "&academic_year=" +
    id_academic_year +
    "&class_name=" +
    id_class_name +
    "&id_class_group_id=" +
    id_class_group_id+
    "&branch_code=" +
    id_branch_code );
  window.open(dataurl, "_blank");
  }else{
    Swal.fire('Please select a Branch')
  }
}

$(document).ready(function() {
  $('#id_academic_year').select2({placeholder: " Select a Year "});
  $('#id_class_name').select2({placeholder: " Select a Class "});
  $('#id_class_group_id').select2({placeholder: " Select a Class Group "});
  $('#id_branch_code').select2({placeholder: " Select a Branch "});
});

$('#id_class_name').on('change', function(){
  class_group_filter()
})


function class_group_filter(){
var class_id=document.getElementById('id_class_name').value
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


//============================= PDF Start =========================


let academic_info=""
$.ajax({
    url: 'apiedu-academic-info-api/',
    type: 'GET',
    dataType: 'json',
    success: function (data) {
        academic_info=data[0]
    }
})

$('#PDF').click(function () {
    let class_id = $('#id_class_name').val()
    let academic_year = $('#id_academic_year').val()
    let class_group_id = $('#id_class_group_id').val()
    var pdf = new jsPDF('p', 'mm', 'a4');
    let page_counter=0;
    if(class_id && academic_year){
    let data_string={
        class_id:class_id,
        academic_year:academic_year,
        class_group_id:class_group_id,
        }
    $.ajax({
        url: '/apiedu-studentinfo-api/',
        data: data_string,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#page_create').modal('show')
            if (data.length){
                pdf.setFontSize(16)
                pdf.setFontStyle('bold')
                pdf.text(academic_info.academic_name.toUpperCase(),105,20,{align: 'center'})
                pdf.setFontSize(13)
                pdf.text(academic_info.academic_address,105,24,{align: 'center'})
                pdf.text(academic_info.academic_email,105,28,{align: 'center'})
                pdf.text("Academic Year:",22,42)
                pdf.text("Class:",75,42)
                pdf.text("Class Group:",130,42)
                pdf.setFontStyle('normal')
                pdf.text(String(data[0].academic_year.academic_year),57,42)
                pdf.text(data[0].class_id.class_name,90,42)
                if(data[0].class_group_id){
                    pdf.text(data[0].class_group_id.class_group_name,155,42)
                }
                let y=0
                let line_height_y=48
                let text_height_y=53
                    
                
                let par_page_student_count=0
                for (let i = 0; i<=data.length; i++) {
                  function par_page_info(){
                    pdf.setFontStyle('bold')
                    pdf.line(10,line_height_y+y,200,line_height_y+y,"S")
                    pdf.line(10,line_height_y+y+8,200,line_height_y+y+8,"S")
                    pdf.line(10,line_height_y+y,10,line_height_y+y+8,"S")
                    pdf.line(200,line_height_y+y,200,line_height_y+y+8,"S")
                    pdf.setFontSize(11)
                    pdf.text("SL.",12,text_height_y+y)
                    pdf.line(20,line_height_y+y,20,line_height_y+y+8,"S")
                    pdf.text("Student's ID,Name & phone",23,text_height_y+y)
                    pdf.line(80,line_height_y+y,80,line_height_y+y+8,"S")
                    pdf.text("Guardian's Name and Phone",82,text_height_y+y)
                    pdf.line(135,line_height_y+y,135,line_height_y+y+8,"S")
                    pdf.text("Address",155,text_height_y+y)

                  }
                  if(data[i]){
                    pdf.setFontStyle('normal')
                    //start dynamic row
                    pdf.line(10,line_height_y+y+8,200,line_height_y+y+8,"S")
                    pdf.line(10,line_height_y+y+21,200,line_height_y+y+21,"S")
                    //start dynamic column
                    pdf.line(10,line_height_y+y+8,10,line_height_y+y+21,"S")
                    pdf.line(20,line_height_y+y+8,20,line_height_y+y+21,"S")
                    pdf.line(80,line_height_y+y+8,80,line_height_y+y+21,"S")
                    pdf.line(135,line_height_y+y+8,135,line_height_y+y+21,"S")
                    pdf.line(200,line_height_y+y+8,200,line_height_y+y+21,"S")
                    //start dynamic value
                    pdf.setFontSize(10)
                    pdf.text((i+1).toString(),12,line_height_y+y+15)
                    pdf.text(data[i].student_roll,22,line_height_y+y+12)
                    pdf.text(data[i].student_name,22,line_height_y+y+16)
                    pdf.text(data[i].student_phone,22,line_height_y+y+20)

                    pdf.text(data[i].student_father_name,82,line_height_y+y+12)
                    if (data[i].legal_guardian_contact){
                      pdf.text(data[i].legal_guardian_contact,82,line_height_y+y+16)
                    }
                    if(data[i].student_present_address){
                      pdf.text(data[i].student_present_address,137,line_height_y+y+12)
                    }
                    if(data[i].student_permanent_address){
                      pdf.text(data[i].student_permanent_address,137,line_height_y+y+16)
                    } 
                  }
                  if(i==0){
                    par_page_info()
                }
                  if((i+1) == 17 || (i+1-17)%20 == 0){
                    pdf.addPage()
                    y=0
                    line_height_y=21
                    text_height_y=26
                    par_page_student_count=0
                    page_counter+=1
                    par_page_info()
                }else{
                    par_page_student_count+=1
                    y=par_page_student_count*13
                }
                   
                }
                
                pdf.save(data[0].class_id.class_name+'-'+data[0].academic_year.academic_year+'.pdf')
                
                
          }// first if statement
          else{
            Swal.fire({
                position: 'center',
                icon: 'error',
                title: 'There is no data under this category.',
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
          title: 'Please Choice Academic Year and Class .',
          showConfirmButton: true,
          })
  }
})



