
$('#id_class_id').change(function(){
    filtering_subjectlist()  
})

$('#id_class_group_id').change(function(){
    filtering_subjectlist()  
})

$('#id_class_id').change(function () {
    filtering_grouplist()
   filtering_subjectlist()
})

$('#id_class_group_id').change(function(){
   filtering_subjectlist()
})


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
            // console.log(data)
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
            console.log(data)
        }
    })
}

function all_student_filtering_result() {
    var academic_year=document.getElementById('id_academic_year').value
    var term_id=document.getElementById('id_term_id').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var student_roll=document.getElementById('student_list').value
    var subject_id=document.getElementById('subject-list').value
    postdata={
        academic_year:academic_year,
        term_id:term_id,
        class_id: class_id,
        class_group_id:class_group_id,
        student_roll:student_roll,
        subject_id:subject_id,
    }
    $.ajax({
        url: '/edu-published-result-filter',
        type: 'get',
        data:postdata,
        datatype:'jason',
        success: function (data) {
            document.getElementById('table-data').innerHTML = data
        }
    })
}

// function filterin_student_result() {
//     var academic_year=document.getElementById('id_academic_year').value
//     var class_id=document.getElementById('id_class_id').value
//     // var subject_id=document.getElementById('subject-list').value
//     var student_roll=document.getElementById('student_list').value
//     postdata={
//         academic_year:academic_year,
//         class_id:class_id,
//         // subject_id:subject_id,
//         student_roll:student_roll,
//     }
//     $.ajax({
//         url: 'edu-student-filtering-roll-wises',
//         type: 'get',
//         data:postdata,
//         datatype:'jason',
//         success: function (data) {
//             document.getElementById('table-data').innerHTML = data
//         }
//     })
// }

// function show_blank_form() {
//     $.ajax({
//         url: '/edu-student-result-allsubjets',
//         type: 'get',
//         beforeSend: function () {
//             $('#edit_model').modal('show');
//         },
//         success: function (data) {
//             $('#edit_model .modal-content').html(data);
//         }
//     })
// }


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
        url: '/edu-published-result-student_roll',
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

function show_exam_mark(roll,subject){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var term_id=document.getElementById('id_term_id').value
    postdata={
        subject_id:subject,
        academic_year:academic_year,
        class_id:class_id,
        student_roll:roll,
        term_id:term_id,
    }
    $.ajax({
        url: '/edu-published-result-subject',
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
 function examTerm(){
    $.ajax({
        url: '/apiedu-examterm-api/',
        type: 'get',
        datatype:'jason',
        success: function (data) {
            $("#id_term_id").append('<option value="">---------------------</option>');
            data.forEach(t=>{
                $("#id_term_id").append('<option value="'+t.id+'">'+t.term_name+'</option>');
            })
        }
    })
}
examTerm()


 
$(document).ready(function() {
    $('#id_academic_year').select2({placeholder: " Select a year "});
    $('#id_class_id').select2({placeholder: " Select a class "});
    $('#id_class_group_id').select2({placeholder: " Select a group "});
    $('#subject-list').select2({placeholder: " Select a subject name "});
    $('#student_list').select2({placeholder: " Select a student "});
});


// ((result publish button))

// function result_publish_button(){
//     var academic_year=document.getElementById('id_academic_year').value
//     var class_id=document.getElementById('id_class_id').value
//     // console.log(academic_year,class_id)
//     var group_id=document.getElementById('id_class_group_id').value
//     var subject_id=document.getElementById('subject-list').value
//     postdata={
//         subject_id:subject_id,
//         academic_year:academic_year,
//         class_id:class_id,
//         class_group_id:group_id
//     }
//     $.ajax({
//         url: 'edu-result-publish-button',
//         type: 'POST',
//         data:postdata,
//         datatype:'jason',
//         success: function (data) {
//             if(data.success_message){
//                 all_student_result_sub()
//                 Swal.fire({
//                     position: 'top-center',
//                     icon: 'success',
//                     title: 'Your result published',
//                     showConfirmButton: false,
//                     timer: 1800
//                   })
//             }
//             else if(data.error_message){
//                 Swal.fire({
//                     icon: 'error',
//                     title: 'Oops...',
//                     text: data.error_message,
//                   })
//             }
//             // $('#edit_model').modal('show');
//             // document.getElementById('edit_model').innerHTML = data
//         }
//     })
// }

// $('#subject-list').change(function(){
//     var subject=$('#subject-list').val()
//     if (subject==''){
//         $('#btnAddRecord').removeAttr('disabled')
//     }
//     else{
//         $('#btnAddRecord').attr('disabled','disabled')
//     }
// })




$('#id_class_id').change(function(){
    class_student_filter()
})
$('#id_class_group_id').change(function(){
    class_student_filter()
})
function class_student_filter(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    datastring={
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
    }
    $.ajax({
        url: "apiedu-studentinfo-api/",
        data:datastring,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#student_list option").remove();
            $("#student_list").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#student_list").append('<option value="'+element.student_roll+'">'+element.student_roll+'-'+element.student_name+'</option>');
            });
        }
    })
}




