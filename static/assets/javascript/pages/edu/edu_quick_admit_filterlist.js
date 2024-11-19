$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


function quick_rigi_data(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var class_group_id=document.getElementById('id_class_group_id').value
    var catagory_id=document.getElementById('id_catagory_id').value
    var student_roll=document.getElementById('id_student_roll').value
    var session_id=document.getElementById('id_session_id').value
    var postdata={
        academic_year:academic_year,
        class_id:class_id,
        class_group_id:class_group_id,
        catagory_id:catagory_id,
        student_roll:student_roll,
        session_id:session_id
    }
    if(academic_year && class_id){
    $.ajax({
        url: 'apiedu-studentinfo-api/',
        data: postdata,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var html=""
            data.forEach((element, index) => {
                html+='<tr>\
            <td><input type="text" name="class_roll'+index+'" value="'+element.class_roll+'" class="form-control">\
            <input type="hidden" name="student_roll'+index+'" value="'+element.student_roll+'"></td>\
            <td><input type="text" name="student_reg'+index+'" value="'+element.student_reg+'" class="form-control" required></td>\
            <td><input type="text" name="student_name'+index+'" value="'+element.student_name+'" class="form-control" required></td>\
            <td><input type="text" name="f_name'+index+'" value="'+element.student_father_name+'" class="form-control" required></td>\
            <td><input type="text" name="m_name'+index+'" value="'+element.student_mother_name+'" class="form-control" required></td>\
            <td><input type="text" name="mobile_no'+index+'" value="'+element.student_phone+'" class="form-control" required></td>\
            <td width="110px">\
            <select class="form-control" name="gender'+index+'" required>\
                <option value="M"'+(element.student_gender === "M"?"selected": "")+'>M</option>\
                <option value="F" '+(element.student_gender === "F"?"selected": "")+'>F</option>\
                <option value="O" '+(element.student_gender === "O"?"selected": "")+'>O</option>\
            </select> \
            </td>\
            <td><input style="width:160px" id="j-date'+index+'" type="date" name="admission'+index+'" value="'+element.student_joining_date+'" class="form-control" required></td>\
            <td><input style="width:160px" id="b-date'+index+'" type="date" name="birthday'+index+'" value="'+element.student_date_of_birth+'" class="form-control" required></td>\
            </tr>'
            });
            
                
            var table='<p style="color:red;background-color:#dddddd; padding:10px;margin-bottom: 0rem;text-align:center">Students Information (Edit All Necessary Fields)</p>\
                <table class="table table-bordered table-sm">\
                <tr>\
                <td>Class/Board Roll</td>\
                <td>Registration</td>\
                <td>Student Name <sup class="text-danger">*</sup></td>\
                <td>Fathers Name <sup class="text-danger">*</sup></td>\
                <td>Mothers Name <sup class="text-danger">*</sup></td>\
                <td>Mobile No. <sup class="text-danger">*</sup></td>\
                <td>Gender <sup class="text-danger">*</sup></td>\
                <td>Admission Date <sup class="text-danger">*</sup></td>\
                <td>Birthday <sup class="text-danger">*</sup></td>\
            </tr>\
            '+html+'\
            </table>\
            <button type="button" class="float-right btn btn-info" onclick="Save_data()">Save Info</button>'
            document.getElementById('auto_row').innerHTML = table
            $("table").resizableColumns();
        }
    })
}else{
    Swal.fire({
        position: 'center',
        icon: 'error',
        title: 'Academic Year and Class name required.',
        showConfirmButton: true,
      })
}
      
}



function Save_data(){
    var academic_year=document.getElementById('id_academic_year').value
    var class_id=document.getElementById('id_class_id').value
    var rows =$('.table tr').length
    $('#row_number').val(rows)
    const data_string = $("#tran_table_data").serialize();
    if(academic_year && class_id){
    $.ajax({
        url: 'edu-quick-admit-editinsert',
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if(data.error_message){
            Swal.fire({
                position: 'center',
                icon: 'error',
                title: data.error_message,
                showConfirmButton: true,
                })
            }
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
}else{
    Swal.fire({
        position: 'center',
        icon: 'error',
        title: 'Academic Year and Class name required.',
        showConfirmButton: true,
      })
}
      
}




$('#id_class_id').change(function(){
    filtering_grouplist()  
})

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


$(document).ready(() => {
    // Select 2 
$('select').select2()
})
