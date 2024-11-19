$('#class_names').change(function(){
    filtering_student()
})

function filtering_student(){
    let class_id=document.getElementById('class_names').value
    let academic_year=document.getElementById('academic_yearl').value
    $.ajax({
        url: "apiedu-studentinfo-api/?academic_year="+academic_year+"&class_id="+class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_student_id option").remove();
            $("#id_student_id").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#id_student_id").append('<option value="'+element.student_roll+'">('+element.student_roll+") "+element.student_name+'</option>')
            });
           
        }
    })
}

// Select 2
$('#class_names').select2({placeholder: "Select a class"})
$('#academic_yearl').select2({placeholder: "Select a year"})
$('#id_student_id').select2({placeholder: "Select a student"})

function add_student(){
    let class_id=document.getElementById('class_names').value
    let academic_year=document.getElementById('academic_yearl').value
    let student_roll=document.getElementById('id_student_id').value
    let dta_list={
        academic_year:academic_year,
        class_id:class_id,
        student_roll:student_roll
    }
    if (class_id && academic_year && student_roll){
    $.ajax({
        url: "/edu-attendence-addstudent-insert",
        type: 'POST',
        data:dta_list,
        datatype: 'json',
        success: function (data) {
            if(data.success_message){
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: data.success_message,
                    showConfirmButton: false,
                    timer: 1500
                  })
                }
        }
    })
}
}