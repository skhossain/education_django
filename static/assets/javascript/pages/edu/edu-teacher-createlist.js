


function fn_student_data(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var teacher_id=document.getElementById('id_teacher_id').value
    var student_roll=document.getElementById('id_student_roll').value
    
    postdata={
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        teacher_id:teacher_id,
        student_roll:student_roll
    }
   
    if(class_id && academic_year && teacher_id){
    $.ajax({
        url:'/edu-teacherchoice-searchstudent/',
        type: 'POST',
        data:postdata,
        datatype: 'json',
        success: function (data) {
            $('#auto_row').html(data.html_form);
        }
    })
}else{
    Swal.fire(
        'Please select-academic year,class and teacher',
        'value is null.',
        'error'
      )
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
            $("#id_student_roll option").remove();
            $("#id_student_roll").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_student_roll").append('<option value="'+element.student_roll+'">'+element.student_roll+'-'+element.student_name+'</option>');
            });
        }
    })
}

function allselect(source) {
    var checkboxes = document.querySelectorAll('.student');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}


function save_choices_students(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var teacher_id=document.getElementById('id_teacher_id').value
    if(class_id && academic_year){
        var students=[]
        document.querySelectorAll('.student').forEach(S =>{

            let stu={student_roll:S.value,student_status:'I'}
            if(S.checked){
                stu={student_roll:S.value,student_status:'A'}
            }
            students.push(JSON.stringify(stu))
        })
    postdata={
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        student_roll:students,
        teacher_id:teacher_id,
    }
    $.ajax({
        url: '/edu-studentschoice-insert/',
        data:postdata,
        type: 'POST',
        datatype: 'json',
        success: function (data) {
            if (data.error_message){
                Swal.fire(
                    'Data Save!',
                    data.error_message,
                    'error'
                  )
            }else{
            Swal.fire(
                'Data Save!',
                data.success_message,
                'success'
              )
            }
        }
    })
}
else{
    Swal.fire(
        'Data Missing!',
        'value is null.',
        'error'
      )
}
}


$(document).ready(() => {
    // Select 2 
$('select').select2()
})