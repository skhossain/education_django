$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});



function fn_student_data(){
    var branch_code=document.getElementById('id_branch_code').value
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var session_id=document.getElementById('id_session_id').value
    var student_roll=document.getElementById('id_student_roll').value
    postdata={
        branch_code:branch_code,
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        session_id:session_id,
        student_roll:student_roll
    }
    if(branch_code && class_id && academic_year){
    $.ajax({
                
        url:'/edu-subjectchoice-searchstudent/',
        data:postdata,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            // document.getElementById('auto_row').innerHTML = data
            $('#auto_row').html(data.html_form);
            // console.log(data.html_form)
        }
    })
}else{
    Swal.fire(
        'Data Missing!',
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

function allselect(source) {
    var checkboxes = document.querySelectorAll('.student');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}
function all_sub_select(source) {
    var checkboxes = document.querySelectorAll('.subject');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}


function save_choices_subject(){
    var branch_code=document.getElementById('id_branch_code').value
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var session_id=document.getElementById('id_session_id').value
    if(branch_code && class_id && academic_year){
        var subjects=[]
        var students=[]
        document.querySelectorAll('.subject').forEach(s =>{
            if(s.checked){
                let sub={subject_id:s.value,is_main:0}
                if(document.getElementById("is_main"+s.value)){ 
                    if(document.getElementById("is_main"+s.value).checked){
                        sub={subject_id:s.value,is_main:1}
                    }
                } 
                subjects.push(JSON.stringify(sub))
            }
        })
        document.querySelectorAll('.student').forEach(S =>{
            if(S.checked){
                students.push(S.value)
            }
        })
    postdata={
        branch_code:branch_code,
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        session_id:session_id,
        student_roll:students,
        subjects:subjects
    }
        
    loder_Spinner(true)
    $.ajax({
        url: '/edu-subchoice-insert/',
        data:postdata,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            loder_Spinner(false)
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