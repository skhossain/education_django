//selec2 uses
$('#id_academic_year').select2({placeholder: " Select a year "})
$('#id_class_id').select2({placeholder: " Select a class "})
$('#id_class_group_id').select2({placeholder: " Select a group "})
// $('#id_subject_id').select2({placeholder: " Select a subject "})
$('#id_teacher_id').select2({placeholder: " Select Teacher "})
$('#id_room_id').select2({placeholder: " Select a room "})
$('#id_routine_id').select2({placeholder: " Select a routine name "})
$('#id_shift_id').select2({placeholder: " Select a shift "})
$('#id_section_id').select2({placeholder: " Select a Section "})
$('#id_day').select2({placeholder: " Select days "})
$('#reset_form').click(function(){
    $('select').val('').trigger('change')
})

$('#btnSearch').click(function(){
    let view_type=$('input[name="routine_view"]:checked').val();
    let r_data=null
    let field_name=null
    if(view_type == 1){
        r_data=$('#id_teacher_id').val();
        field_name='Teacher Name'
    }
    if(view_type == 2){
        r_data=$('#id_class_id').val();
        field_name='Class Name'
    }
    if(view_type == 3){
        r_data=$('#id_day').val();
        field_name='Day Name'
    }
    let routine_id =$('#id_routine_id').val();
    let room_id =$('#id_room_id').val();
    
    if(routine_id && r_data){
        const data_string = $("#tran_table_data").serialize();
        const data_url = $("#tran_table_data").attr('data-url');
        loder_Spinner(true)
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                    loder_Spinner(false)
                    // Swal.fire({
                    //     position: 'center',
                    //     icon: 'error',
                    //     title: data.error_message,
                    //     showConfirmButton: false,
                    //     timer: 1500
                    //   })
                    $('#table_data').html(data.html_form)
            }
        })
    }else{
        Swal.fire(
            'Data Missing!',
            'Routine Name and '+field_name+' is required.',
            'error'
          )
    }
})


$('#id_class_id').change(function(){
    filtering_subjectlist()
    get_group_list()
    get_section_list()
})
$('#id_class_group_id').change(function(){
    filtering_subjectlist()  
})
function filtering_subjectlist(){
    let class_id=document.getElementById('id_class_id').value
    let class_group_id=document.getElementById('id_class_group_id').value
    $.ajax({
        url: "apiedu-sublist-api/?class_id="+class_id+"&class_group_id="+class_group_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_subject_id option").remove();
            $("#id_subject_id").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#id_subject_id").append('<option value="'+element.subject_id+'">'+element.subject_name+'</option>')
            });
        }
    })
}

function get_group_list(){
    let class_id=$('#id_class_id').val()
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id="+class_id,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#id_class_group_id option').remove();
            $("#id_class_group_id").append('<option value="">------------</option>');
            data.forEach(G=>{
                $("#id_class_group_id").append('<option value="'+G.class_group_id+'">'+G.class_group_name+'</option>');
            })
        }
    })
}
function get_section_list(){
    let class_id=$('#id_class_id').val()
    $.ajax({
        url: "apiedu-sectioninfo-api/?class_id="+class_id,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#id_section_id option').remove();
            $("#id_section_id").append('<option value="">------------</option>');
            data.forEach(G=>{
                $("#id_section_id").append('<option value="'+G.section_id+'">'+G.section_name+'</option>');
            })
        }
    })
}


$('#pdf-create').click(function(){
    let view_type=$('input[name="routine_view"]:checked').val();
    let r_data=null
    let field_name=null
    if(view_type == 1){
        r_data=$('#id_teacher_id').val();
        field_name='Teacher Name'
    }
    if(view_type == 2){
        r_data=$('#id_class_id').val();
        field_name='Class Name'
    }
    if(view_type == 3){
        r_data=$('#id_day').val();
        field_name='Day Name'
    }
    let routine_id =$('#id_routine_id').val();
    let room_id =$('#id_room_id').val();
    
    if(routine_id){
        const data_string = $("#tran_table_data").serialize();
        location.href="/edu-routine-query-pdf?"+data_string
    }else{
        Swal.fire(
            'Data Missing!',
            'Routine Name and '+field_name+' is required.',
            'error'
          )
    }
})