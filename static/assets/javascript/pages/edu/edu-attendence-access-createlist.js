

function filtering_data(){
    let academic_year=document.getElementById('academic_yearl').value
    let month_number=document.getElementById('month_list').value
    let class_id=document.getElementById('class_names').value
    let class_group_id=document.getElementById('group_list').value
    let section_id=document.getElementById('section_name').value
    let subject_id=document.getElementById('subject_list').value
                
    $.ajax({
                
        url:"/edu-attendance-list-modifierview?academic_year="+academic_year+"&month_number="+month_number+"&class_id="+class_id+"&class_group_id="+class_group_id+"&section_id="+section_id+"&subject_id"+subject_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            document.getElementById('table-list').innerHTML = data  
        }
    })
}
                


$('#class_names').change(function(){
    $.when(get_group_list()).then(
        filtering_subjectlist()
    );  
})

function get_group_list(){
    let class_id=$('#class_names').val()
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id="+class_id,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#group_list option').remove();
            $("#group_list").append('<option value="">------------</option>');
            data.forEach(G=>{
                $("#group_list").append('<option value="'+G.class_group_id+'">'+G.class_group_name+'</option>');
            })
        }
    })
}

$('#group_list').change(function(){
    filtering_subjectlist()  
})

function filtering_subjectlist(){
    let class_id=document.getElementById('class_names').value
    let class_group_id=document.getElementById('group_list').value
    $.ajax({
        url: "apiedu-sublist-api/?class_id="+class_id+"&class_group_id="+class_group_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#subject_list option").remove();
            $("#subject_list").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#subject_list").append('<option value="'+element.subject_id+'">'+element.subject_name+'</option>')
            });
        }
    })
}

$('#class_names').change(function(){
    filtering_section()
})

function filtering_section(){
    let class_id=document.getElementById('class_names').value
    $.ajax({
        url: "apiedu-sectioninfo-api/?class_id="+class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#section_name option").remove();
            $("#section_name").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#section_name").append('<option value="'+element.section_id+'">'+element.section_name+'</option>')
            });
           
        }
    })
}

// Select 2
$('#class_names').select2({placeholder: "Select a class"})
$('#month_list').select2({placeholder: "Select a month"})
$('#academic_yearl').select2({placeholder: "Select a year"})
$('#group_list').select2({placeholder: "Select a class group"})
$('#section_name').select2({placeholder: "Select a section"})
$('#subject_list').select2({placeholder: "Select a subject"})
$('#teacher_list').select2({placeholder: "Select a teacher"})

function check_all(source) {
    var checkboxes = document.querySelectorAll('.present_sheet');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}

function apply_sheet(){
    var employee_id = $("#teacher_list").val();
    var present_sheets= document.querySelectorAll('.present_sheet')
    var present_sheet_info_ids=[]
    present_sheets.forEach(id => {
        let value = {id:id.value,status:id.checked}
        present_sheet_info_ids.push(JSON.stringify(value))
    });
    var data_string={
        employee_id:employee_id,
        present_sheet_info_ids:present_sheet_info_ids
    }
    if(present_sheet_info_ids.length !=0 && employee_id){
         $.ajax({
        url: "/edu-attendance-access-insert",
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if(data.success_message){
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Apply Successfully',
                    showConfirmButton: false,
                    timer: 1000
                  })
            }
            if(data.error_message){
                Swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: data.error_message,
                    showConfirmButton: false,
                    timer: 1500
                  })
                  filtering_data()
            }
        }
    })
    }else{
        Swal.fire(
            'Data Missing!',
            'value is null.',
            'error'
          )
    }
   
    return false;
    
}

