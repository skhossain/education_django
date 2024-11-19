

$('#reset').click(function () {
    $('select').val('').trigger('change')
    $('input[type=time]').val('')
});
$('#btnAddRecord').click(function () {
    post_tran_table_data();
});

//selec2 uses
$('#id_academic_year').select2({placeholder: " Select a year "})
$('#id_class_id').select2({placeholder: " Select a class "})
$('#id_class_group_id').select2({placeholder: " Select a group "})
$('#id_subject_id').select2({placeholder: " Select a subject "})
$('#id_teacher_id').select2({placeholder: " Select Teacher "})
$('#id_room_id').select2({placeholder: " Select a room "})
$('#id_routine_id').select2({placeholder: " Select a routine name "})
$('#id_shift_id').select2({placeholder: " Select a shift "})
$('#id_section_id').select2({placeholder: " Select a Section "})
$('#id_day').select2({placeholder: " Select days "})

function post_tran_table_data() {
    let routine_id =$('#id_routine_id').val();
    let academic_year =$('#id_academic_year').val();
    let class_id =$('#id_class_id').val();
    let subject_id =$('#id_subject_id').val();
    let teacher_id =$('#id_teacher_id').val();
    let room_id =$('#id_room_id').val();
    let start_time =$('#id_start_time').val();
    let end_time =$('#id_end_time').val();
    let day =$('#id_day').val();
    if(routine_id && academic_year && class_id && subject_id && teacher_id && room_id && start_time && end_time && day){
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
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: data.success_message,
                    showConfirmButton: false,
                    timer: 1500
                  })
                // $('#id_academic_year').val('').trigger('change')
                // $('#id_class_id').val('').trigger('change')
                $('#id_class_group_id').val('').trigger('change')
                $('#id_subject_id').val('').trigger('change')
                $('#id_teacher_id').val('').trigger('change')
                // $('#id_room_id').val('').trigger('change')
                // $('#id_routine_id').val('').trigger('change')
            } else {
                loder_Spinner(false)
                Swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: data.error_message,
                    showConfirmButton: false,
                    timer: 1500
                  })
            }
        }
    })
}else{
    Swal.fire(
        'Data Missing!',
        'Some value is null.',
        'error'
      )
}
    return false;
}

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

//Search and Edit

$('#btnSearch').click(function(){
    search_routine()
})
function search_routine(){
    let routine_id =$('#id_routine_id').val();
    let academic_year =$('#id_academic_year').val();
    let class_id =$('#id_class_id').val();
    let subject_id =$('#id_subject_id').val();
    let teacher_id =$('#id_teacher_id').val();
    let room_id =$('#id_room_id').val();
    let start_time =$('#id_start_time').val();
    let end_time =$('#id_end_time').val();
    let day =$('#id_day').val();
    let class_group_id =$('#id_class_group_id').val();
    let shift_id =$('#id_shift_id').val();
    let section_id =$('#id_section_id').val();

    let data_set={
        routine_id:routine_id,
        academic_year:academic_year,
        class_id:class_id,
        subject_id:subject_id,
        teacher_id:teacher_id,
        room_id:room_id,
        start_time:start_time,
        end_time:end_time,
        day:day.toString(),
        class_group_id:class_group_id,
        shift_id:shift_id,
        section_id:section_id
    }
    if(routine_id){
    $.ajax({
        url: "/edu-routinedetails-list",
        type: 'GET',
        data:data_set,
        dataType: 'json',
        success: function (data) {
            $('#data-table').html(data.html_form)
        }
    })
}else{
    Swal.fire(
        'Data Missing!',
        'Routine name is required.',
        'error'
      )
}
}

function delete_routine(id){
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: "/edu-routinedetails-delete/"+id,
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    Swal.fire(
                        'Deleted!',
                        'Your record has been deleted.',
                        'success'
                      )
                      search_routine()
                }
            })
        }
      })
}