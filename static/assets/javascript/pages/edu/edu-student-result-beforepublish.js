
$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$('#id_academic_year').change(function () {
    active_button()    
})
$('#id_term_id').change(function () {
    active_button()    
})
$('#id_class_id').change(function () {
    active_button()
    filtering_grouplist()
    
})

// $('#id_class_group_id').change(function(){
//    filtering_subjectlist()
// })




function filtering_subjectlist(){
    let class_id=document.getElementById('id_class_id').value
    let class_group_id=document.getElementById('id_class_group_id').value
    let academic_year=document.getElementById('id_academic_year').value

    $.ajax({
        url: "apiedu-sublist-api/?class_id="+class_id+"&class_group_id="+class_group_id+"&academic_year="+academic_year,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#subject-list option").remove();
            $("#subject-list").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#subject-list").append('<option value="'+element.subject_id+'">'+element.subject_name+'</option>')
            });
        }
    })
}
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

function all_student_result_sub() {
    loder_Spinner(true)
    var branch_code=document.getElementById('id_branch_code').value
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var term_id=document.getElementById('id_term_id').value
    var limit=document.getElementById('limit').value
    var page=document.getElementById('page').value
    postdata={
        branch_code:branch_code,
        academic_year:academic_year,
        term_id:term_id,
        class_id:class_id,
        class_group_id:class_group_id,
        limit:limit,
        page:page,
    }
    $.ajax({
        url: 'edu-student-result-before-publish-data',
        type: 'POST',
        data:postdata,
        datatype:'jason',
        success: function (data) {
            document.getElementById('table-data').innerHTML = data
            loder_Spinner(false)
        }
    })
}

function all_student_marksheet() {
    loder_Spinner(true)
    let position_check=false
    if ($('#maritposition').is(':checked')) { 
        position_check=true
    }
    var branch_code=document.getElementById('id_branch_code').value
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var term_id=document.getElementById('id_term_id').value
    var limit=document.getElementById('limit').value
    var page=document.getElementById('page').value
    postdata={
        branch_code:branch_code,
        academic_year:academic_year,
        term_id:term_id,
        class_id:class_id,
        class_group_id:class_group_id,
        limit:limit,
        page: page,
        json: true,
        with_position:position_check
    }
    var pdf = new jsPDF('p', 'mm', 'a4');

    $.ajax({
        url: 'edu-student-result-before-publish-data',
        type: 'POST',
        data:postdata,
        datatype:'jason',
        success: function (data) {
            let class_name=""
            
            data.students_results.forEach((student_result, index) => {
                //Header
                pdf.setFontSize(16)
                pdf.text(data.institute[0].academic_name, 105, 15, 'center');
                pdf.setFontSize(10)
                pdf.text(data.institute[0].text_one?data.institute[0].text_one:"", 105, 22, 'center');
                pdf.text(data.institute[0].text_two?data.institute[0].text_two:"", 105, 26, 'center');
                pdf.text(data.institute[0].text_three?data.institute[0].text_three:"", 105, 30, 'center');
                pdf.text(data.institute[0].text_four?data.institute[0].text_four:"", 105, 34, 'center');
                pdf.text(data.institute[0].text_five ? data.institute[0].text_five : "", 105, 38, 'center');
                
                pdf.setFontSize(11)
                pdf.setFont(undefined, 'bold')
                pdf.text("Mark Sheet", 105, 70, 'center');
                pdf.line(95,71,115,71)
                pdf.text(data.term+' - '+data.academic_year, 105, 75, 'center');
                
                //Student Info
                pdf.setFontSize(11)
                pdf.setFont(undefined, 'bold')
                pdf.text("ID", 10, 45);
                pdf.text(":", 40, 45);
                pdf.setFont(undefined, 'normal')
                pdf.text(student_result.student_roll, 45, 45);

                pdf.setFont(undefined, 'bold')
                pdf.text("Name", 10, 49);
                pdf.text(":", 40, 49);
                pdf.setFont(undefined, 'normal')
                pdf.text(student_result.student_roll__student_name, 45, 49);

                pdf.setFont(undefined, 'bold')
                pdf.text("Father's Name", 10, 53);
                pdf.text(":", 40, 53);
                pdf.setFont(undefined, 'normal')
                pdf.text(student_result.student_roll__student_father_name, 45, 53);

                pdf.setFont(undefined, 'bold')
                pdf.text("Mother's Name", 10, 57);
                pdf.text(":", 40, 57);
                pdf.setFont(undefined, 'normal')
                pdf.text(student_result.student_roll__student_mother_name, 45, 57);

                pdf.setFont(undefined, 'bold')
                pdf.text("Date of Birth", 10, 61);
                pdf.text(":", 40, 61);
                pdf.setFont(undefined, 'normal')
                let d = new Date(student_result.student_roll__student_date_of_birth);
                pdf.text(d.toLocaleDateString("en-US", {day: 'numeric', month: 'long',year: 'numeric' }), 45, 61);
                
                pdf.setFont(undefined, 'bold')
                pdf.text("Class", 10, 65);
                pdf.text(":", 40, 65);
                pdf.setFont(undefined, 'normal')
                pdf.text(student_result.student_roll__class_id__class_name, 45, 65);
                
                if (student_result.class_group_id__class_group_name) {
                    pdf.setFont(undefined, 'bold')
                    pdf.text("Group", 10, 70);
                    pdf.text(":", 40, 70);
                    pdf.setFont(undefined, 'normal')
                    pdf.text(student_result.class_group_id__class_group_name, 45, 70);
                }
                if (student_result.position) {
                    let ph = 70;
                    if (student_result.class_group_id__class_group_name) {
                        ph = 75
                    }
                    pdf.setFont(undefined, 'bold')
                    pdf.text("Position", 10, ph);
                    pdf.text(":", 40, ph);
                    pdf.setFont(undefined, 'normal')
                    let leter = 'th'
                    if (student_result.position == 1) {
                        leter = 'st';
                    } else if (student_result.position == 2) {
                        leter = 'nd';
                    }else if (student_result.position == 3) {
                        leter = 'rd';
                    }
                    pdf.text(student_result.position.toString()+leter, 45, ph);
                }
                class_name = student_result.student_roll__class_id__class_name;
                
                //Result Grate
                
                gy = -9;
                 pdf.setFontSize(8)
                data.grade_list.forEach(el => {
                    pdf.line(160,gy+50,200,gy+50)
                    pdf.line(160, gy+55, 200, gy+55)
                    pdf.line(160, gy+50, 160, gy+55)
                    pdf.line(200, gy + 50, 200, gy + 55)

                    pdf.text(el.highest_mark.toString().split(".")[0], 162, gy+53,);
                    pdf.text(" - "+el.lowest_mark.toString().split(".")[0], 167, gy+53,);
                    pdf.line(178, gy + 50, 178, gy + 55)
                    
                    pdf.text(el.result_gpa.toString(), 180, gy+53,);
                    pdf.line(188, gy + 50, 188, gy + 55)
                    
                    pdf.text(el.grade_name, 190, gy+53,);

                    gy += 5;
                });
      
                //Subject Result
                let sub_count = 1;
                y = 10;
                pdf.setFontSize(10)
                pdf.line(10,y+75,200,y+75)
                pdf.line(10, y+85, 200, y+85)
                pdf.line(10, y+75, 10, y+85)
                pdf.line(200, y+75, 200, y+85)
                
                pdf.text("SL NO", 12, y+82,);
                pdf.line(24, y+75, 24, y+85)
                pdf.text("Subject Name", 25, y+82);
                pdf.line(117, y+75, 117, y+85)
                pdf.text("GPA", 120, y+82);
                pdf.line(132, y+75, 132, y+85)
                pdf.text("Grade", 135, y+82);
                pdf.line(148, y+75, 148, y+85)
                pdf.text("Total Marks", 150, y+82);
                pdf.line(170, y+75, 170, y+85)
                pdf.text("Obtain Marks", 174, y+82);
                
                
                data.subject_results.forEach(subResult => {
                    if (subResult.student_roll == student_result.student_roll) {
                        
                        pdf.line(10, y+95, 200, y+95)
                        pdf.line(10, y+85, 10, y+95)
                        pdf.line(200, y+85, 200, y+95)
                        pdf.text(sub_count.toString(), 12, y+92);
                        pdf.line(24, y+85, 24, y+95)
                        pdf.text(subResult.subject_id__subject_name, 25, y+92);
                        pdf.line(117, y+85, 117, y+95)
                        pdf.text(subResult.gpa?subResult.gpa.toString():'0', 120, y+92);
                        pdf.line(132, y+85, 132, y+95)
                        pdf.text(subResult.lg?subResult.lg:'F', 135, y+92);
                        pdf.line(148, y+85, 148, y+95)
                        pdf.text(subResult.subject_id__maximum_marks.toString(), 150, y+92);
                        pdf.line(170, y+85, 170, y+95)
                        pdf.text(subResult.obtain?subResult.obtain.split(".")[0]:"", 190, y+92,"center");
                        sub_count += 1;
                        y += 10;
                    }
                    
                });
                //Total
                pdf.line(10, y+85.2, 200, y+85.2)
                pdf.line(10, y+85.4, 200, y+85.4)
                pdf.line(10, y+95, 200, y+95)
                pdf.line(10, y+85, 10, y+95)
                pdf.line(200, y+85, 200, y+95)
                pdf.text("Total", 12, y+92);
                pdf.line(117, y + 85, 117, y + 95)
                
                pdf.text(student_result.gpa, 120, y+92);
                pdf.line(132, y+85, 132, y+95)
                pdf.text(student_result.lg, 135, y+92);
                pdf.line(148, y+85, 148, y+95)
                pdf.text(student_result.total.toString(), 150, y+92);
                pdf.line(170, y+85, 170, y+95)
                pdf.text(student_result.obtain?student_result.obtain.split(".")[0]:"", 190, y + 92, "center");
                
                //Bottom
                pdf.text("Class Teacher", 30, y + 125);
                pdf.text("Principal/Head Master", 150, y + 125);
                if (data.students_results.length != index + 1) {
                    pdf.addPage();
                }
            });
            
            pdf.save('Result- Class '+class_name+data.page_info);
            loder_Spinner(false)
        }
    })
}


function show_blank_form() {
    
      $.ajax({
          url: '/edu-student-result-allsubjets',
          type: 'get',
          beforeSend: function () {
              $('#edit_model').modal('show');
          },
          success: function (data) {
              $('#edit_model .modal-content').html(data);
          }
      })
  }


 function show_marksheet(roll,m_position){
    var academic_year=document.getElementById('id_academic_year').value
    var term_id=document.getElementById('id_term_id').value
    var class_id=document.getElementById('id_class_id').value
    var student_roll=roll
    postdata={
        academic_year:academic_year,
        term_id:term_id,
        class_id:class_id,
        student_roll:student_roll,
        m_position:m_position
    }
    $.ajax({
        url: 'edu-onestudent-result-allsubjects',
        type: 'get',
        data:postdata,
        datatype:'jason',
        success: function (data) {
            console.log(data)
            $('#edit_model').modal('show');
            document.getElementById('edit_model').innerHTML = data
        }
    })
     
 }
function close_modal(){
    $('#edit_model').modal('hide');
    new stepsDemo();
}

function show_exam_mark(roll,subject){
    var academic_year=document.getElementById('id_academic_year').value
    var term_id=document.getElementById('id_term_id').value
    var class_id=document.getElementById('id_class_id').value
    var student_roll=roll
    postdata={
        subject_id:subject,
        academic_year:academic_year,
        term_id:term_id,
        class_id:class_id,
        student_roll:student_roll
    }
    $.ajax({
        url: 'edu-onesubject-allexammark',
        type: 'get',
        data:postdata,
        datatype:'jason',
        success: function (data) {
            console.log(data)
            $('#edit_model').modal('show');
            document.getElementById('edit_model').innerHTML = data
        }
    })
     
 }


// ((result publish button))

function result_publish_button(){
    var academic_year=document.getElementById('id_academic_year').value
    var term_id=document.getElementById('id_term_id').value
    var class_id=document.getElementById('id_class_id').value
    // console.log(academic_year,class_id)
    var group_id=document.getElementById('id_class_group_id').value
    var subject_id=document.getElementById('subject-list').value
    postdata={
        subject_id:subject_id,
        academic_year:academic_year,
        term_id:term_id,
        class_id:class_id,
        class_group_id:group_id
    }
    $.ajax({
        url: 'edu-result-publish-button',
        type: 'POST',
        data:postdata,
        datatype:'jason',
        success: function (data) {
            if(data.success_message){
                all_student_result_sub()
                Swal.fire({
                    position: 'top-center',
                    icon: 'success',
                    title: 'Your result published',
                    showConfirmButton: false,
                    timer: 1800
                  })
            }
            else if(data.error_message){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.error_message,
                  })
            }
            // $('#edit_model').modal('show');
            // document.getElementById('edit_model').innerHTML = data
        }
    })
}

$('#subject-list').change(function(){
    publish_button_control()
})

$('#confirm_publish').click(function() {
    publish_button_control()
});

function publish_button_control(){
    var subject=$('#subject-list').val()
    var confirm=$('#confirm_publish')
    if (subject=='' && confirm.is(':checked')){
        $('#btnAddRecord').removeAttr('disabled')
    }
    else{
        $('#btnAddRecord').attr('disabled','disabled')
    }
}

function examTerm(){
    $.ajax({
        url: '/apiedu-examterm-api/',
        type: 'get',
        datatype:'jason',
        success: function (data) {
            data.forEach(t=>{
                $("#id_term_id").append('<option value="'+t.id+'">'+t.term_name+'</option>');
            })
        }
    })
}
examTerm()

// function Out_Of(){
//     $.ajax({
//         url: '/apiedu-result-grade-api/',
//         type: 'get',
//         datatype:'jason',
//         success: function (data) {
//             console.log(data)
//             data.forEach(t=>{
//                 $("#out_of").append('<option value="'+t.out_of+'">'+t.out_of+'</option>');
//             })
//         }
//     })
// }
// Out_Of()

function active_button() {
    let data_url = $('#listView').attr('data-url')
    let academic_year = $('#id_academic_year').val();
    let term_id = $('#id_term_id').val();
    let limit = $('#limit').val();
    let page = $('#page').val();
    let class_id = $('#id_class_id').val();
    if (academic_year && term_id && limit && page && class_id) {
        $('#listView').prop("disabled", false);
    }
}

function list_view() {
    let data_url = $('#listView').attr('data-url')
    var branch_code=document.getElementById('id_branch_code').value
    let academic_year = $('#id_academic_year').val();
    let term_id = $('#id_term_id').val();
    let limit = $('#limit').val();
    let page = $('#page').val();
    let class_id = $('#id_class_id').val();
    if (academic_year && term_id && limit && page && class_id) {
        $('#listView').prop("disabled", false);
    }
    let class_group_id = $('#id_class_group_id').val();
    let url = data_url + '?branch_code='+branch_code+'&academic_year='+academic_year+'&term_id=' + term_id +'&limit=' + limit +'&page=' + page +'&class_id=' + class_id + '&class_group_id=' + class_group_id
    window.open(url, "_blank");
}

$(document).ready(function () {
    $('select').select2();
    $('#id_academic_year').select2({placeholder: " Select a year "});
    $('#id_class_id').select2({placeholder: " Select a class "});
    $('#id_class_group_id').select2({placeholder: " Select a group "});
    $('#subject-list').select2({placeholder: " Select a subject name "});
});