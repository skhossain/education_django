let fees_data=""
function student_profile_details() {
    var student_roll = document.getElementById('id_student_roll').value
    var due_date = document.getElementById('id_due_date').value
    var postdata = {
        student_roll: student_roll,
        due_date: due_date,
    }
    $.ajax({
        url: '/edu-quick-collection-student-info',
        data: postdata,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $('#student_id_show').text(data.student_info.student_roll)
            $('#profile_img').attr('src', '/media/' + data.student_info.profile_image)
            $('#student_name_show').text(data.student_info.student_name)
            $('#class_name_show').text(data.student_info.class_id__class_name)
            $('#class_roll_show').text(data.student_info.class_roll)
            $('#class_session_show').text(data.student_info.session_id__session_name)
            $('#class_group_show').text(data.student_info.class_group_id__class_group_name)
            $('#father_name_show').text(data.student_info.student_father_name)
            $('#category_show').text(data.student_info.catagory_id__catagory_name)
            $('#mobile_show').text(data.student_info.student_phone)
            $('#body_tr tr').remove()
            let full_check=$('#all_f').is(':checked')
            fees_data=data.fees
            data.fees.forEach(fee => {
                let tr = `<tr>
                <td>
                ${fee.head_name}
                </td>
                <td>${fee.due_date}</td>
                <td>${fee.fees_due?fee.fees_due:0.0}</td>
                <td>${fee.fine_due?fee.fine_due:0.0}</td>
                <td><span id="total_due_${fee.id}">${fee.total_due?fee.total_due:0.0}</span></td>
                <td>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" onclick="set_full(${fee.id})" name="paid_a_toggle_${fee.id}" value="" id="f_${fee.id}">
                        <label class="form-check-label" for="f_${fee.id}">
                            F
                        </label>
                        </div>
                </td>
                <td>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" onclick="set_zero(${fee.id})" name="paid_a_toggle_${fee.id}" value="" id="z_${fee.id}" checked>
                        <label class="form-check-label" for="z_${fee.id}">
                            Z
                        </label>
                        </div>
                </td>
                <td><input type="number" id="set_waive_${fee.id}" data-id="${fee.id}" onchange="set_waive_change(this)"></td>
               
            </tr>`
                $('#body_tr').append(tr)
            });

        }
    })
}
$('#id_student_roll').select2({ placeholder: " Select a student " })

//Functions
function set_full(id){
    let due=$('#total_due_'+id).text()
    $('#set_waive_'+id).val(Number(due))
    $.ajax({
        url: '/edu-feeswaivestudent-update-temp?taka='+Number(due)+'&id='+id,
        type: 'get',
        datatype: 'json',
        success: function (data) {

        }
    })
}
function set_zero(id){
    $('#set_waive_'+id).val(0)
    $.ajax({
        url: '/edu-feeswaivestudent-update-temp?taka=0&id='+id,
        type: 'get',
        datatype: 'json',
        success: function (data) {

        }
    })
}

function set_all_full(){
    fees_data.forEach(element => {
        set_full(element.id) 
        $('#z_'+element.id).prop("checked", false);
        $('#f_'+element.id).prop("checked", true);
    });
}
function set_all_zero(){
    fees_data.forEach(element => {
        set_zero(element.id)
        $('#f_'+element.id).prop("checked", false);
        $('#z_'+element.id).prop("checked", true);
    });
}


function set_waive_change(tag) {
    let taka = tag.value
    let id = $(tag).attr('data-id')
    var postdata = {
        taka: taka,
        id: id,
    }
    $.ajax({
        url: '/edu-feeswaivestudent-update-temp',
        data: postdata,
        type: 'get',
        datatype: 'json',
        success: function (data) {

        }
    })
}

function create_or_save() {
   
    // var branch_code = document.getElementById('id_branch_code').value
    var student_roll = document.getElementById('id_student_roll').value
    var effective_date = document.getElementById('id_due_date').value
    var postdata = {
        student_roll: student_roll,
        effective_date: effective_date,
        // branch_code: branch_code,
    }
    $.ajax({
        url: '/edu-feeswaivestudent-insert',
        data: postdata,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: data.success_message,
                    showConfirmButton: false,
                    timer: 1500
                })
                // print_voucher(data.transaction_id);
                $('#body_tr tr').remove()
            } else {
                alert(data.error_message);
            }
        }
    })
}
