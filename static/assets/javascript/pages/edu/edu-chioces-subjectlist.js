
function choices_subject_list(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var session_id=document.getElementById('id_session_id').value
    var student_roll=document.getElementById('id_student_roll').value
    postdata={
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        session_id:session_id,
        student_roll:student_roll
    }
    if(academic_year && class_id){
        loder_Spinner(true)
    $.ajax({
        url: '/edu-choices-subjectlist-view',
        data: postdata,
        type: 'post',
        dataType: 'json',
        success: function (data) {
              document.getElementById('table-data').innerHTML=data.html_form
              loder_Spinner(false)
        }
    })
    }else{
        Swal.fire({
            position: 'top-center',
            icon: 'error',
            title: 'Academic year and Class Required',
            showConfirmButton: false,
            timer: 1500
          })
    }
}


// function choices_subject_edit(){
//     var roll=document.getElementById('button').value
//     $.ajax({
//         url: 'edu-choicesubject-edit/'+roll,
//         type: 'get',
//         dataType: 'json',
//         beforeSend: function () {
//             $('#edit_model').modal('show');
//         },
//         success: function (data) {
//             $('#edit_model .modal-content').html(data.html_form);
//         }
//     })
// }

$(document).ready(() => {
    // Select 2 
$('select').select2()
})

function editChoice(id){
    let academic_year = $('#id_academic_year').val()
    let class_id = $('#id_class_id').val()
    let data_string={
        academic_year:academic_year,
        class_id:class_id,
        student_roll:id
    }
        $.ajax({
            url: '/edu-choicesubject-edit',
            type: 'get',
            data:data_string,
            dataType: 'json',
            beforeSend: function () {
                $('#edit_model').modal('show');
            },
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
}

function update_choice(student_roll){
    let academic_year = $('#id_academic_year').val()
    let class_id = $('#id_class_id').val()
    let total_subject = $('#total_subject').val()
    let subject_list =document.querySelectorAll('.class_subject')
    let subjects=[]
    subject_list.forEach(s => {
        let subject_id=s.value
        let new_data=[subject_id,0,0]
        if(s.checked){
            new_data=[subject_id,1,0]
            if(document.getElementById("is_main"+subject_id)){  
                if(document.getElementById("is_main"+subject_id).checked){
                    new_data=[subject_id,1,1]
                }
            }             
        }
        subjects.push(new_data)
    });
    let data_string={
        academic_year:academic_year,
        class_id:class_id,
        student_roll:student_roll,
        total_subject:total_subject,
        subject:subjects
    }
    
    console.log(data_string)
        $.ajax({
            url: 'edu-choicesubject-edit/',
            type: 'post',
            data:data_string,
            dataType: 'json',
            success: function (data) {
                $('#edit_model').modal('hide');
                choices_subject_list()
                console.log(data)
            }
        })

}

$('#id_class_id').change(function(){
    class_group_filter()
    class_student_filter()
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


function class_student_filter(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var session_id=document.getElementById('id_session_id').value
    datastring={
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        session_id:session_id,
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