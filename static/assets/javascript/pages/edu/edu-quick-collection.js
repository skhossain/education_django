$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


let fees_data = ""
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
                dueDate=new Date(fee.due_date)
                let tr = `<tr>
                <td>
                ${fee.head_name}
                </td>
                <td>${dueDate.getDate()} ${dueDate.toLocaleString('en-us', { month: 'short' })} ${dueDate.getFullYear().toString().slice(2)} </td>
                <td>${fee.fees_due?fee.fees_due:0.0}</td>
                <td>${fee.fine_due?fee.fine_due:0.0}</td>
                <td>${fee.total_waive?fee.total_waive:0.0}</td>
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
                <td><input type="number" class="paid_amount" id="paid_amount_${fee.id}" data-id="${fee.id}" onchange="paid_amount_change(this)"></td>
                <td>${fee.total_overdue}</td>
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
    $('#paid_amount_'+id).val(Number(due))
    $.ajax({
        url: '/edu-quick-collection-update-temp?taka='+Number(due)+'&id='+id,
        type: 'get',
        datatype: 'json',
        success: function (data) {

        }
    })
}
function set_zero(id){
    $('#paid_amount_'+id).val(0)
    $.ajax({
        url: '/edu-quick-collection-update-temp?taka=0&id='+id,
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

$('#btnFeesSubmit').click(function () {
    new save_payment();
});

function paid_amount_change(tag) {
    let taka = tag.value
    let id = $(tag).attr('data-id')
    var postdata = {
        taka: taka,
        id: id,
    }
    $.ajax({
        url: '/edu-quick-collection-update-temp',
        data: postdata,
        type: 'get',
        datatype: 'json',
        success: function (data) {

        }
    })
}

function save_payment() {
    var student_roll = document.getElementById('id_student_roll').value
    var receive_date = document.getElementById('id_receive_date').value
    var branch_code = document.getElementById('id_branch_code').value
    var postdata = {
        student_roll: student_roll,
        receive_date: receive_date,
        branch_code: branch_code,
    }
    $.ajax({
        url: '/edu-quick-collection-submit',
        data: postdata,
        type: 'get',
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
                print_voucher(data.transaction_id,branch_code);
                $('#body_tr tr').remove()
            } else {
                alert(data.error_message);
            }
        }
    })
}

function student_others_payment_model() {
    var student_roll = document.getElementById('id_student_roll').value
    var receive_date = document.getElementById('id_receive_date').value
    if (student_roll) {
        $('#edit_model').modal('show')
        $.ajax({
            url: '/edu-one-time-fees-receive/' + student_roll+"?receive_date="+receive_date,
            type: 'get',
            datatype: 'json',
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form)
                // console.log(data)
            }
        })
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Student ID required!',
        })
    }
}

function student_others_payment_received() {
    const data_string = $("#edit_form").serialize();
    const data_url = $("#edit_form").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            $('#page_loading').modal('hide');
            $('#edit_model').modal('hide');
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: data.success_message,
                showConfirmButton: false,
                timer: 1500
            })
        }
    })
    return false;
}


function print_voucher(p_transaction_id,branch_code) {
    var data_url = 'appauth-report-submit/';
    var report_name = 'edu_quickreceive_voucher';
    var report_data = { 'p_transaction_id': p_transaction_id };
    report_data = JSON.stringify(report_data);
    console.log(report_data)
    $.ajax({
        url: data_url,
        data: {
            'report_name': report_name,
            "report_data": report_data,
            "branch_code":branch_code
        },
        cache: "false",
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                window.open(data.report_urls + '/edu-quick-collection-printview?branch_code='+branch_code, "_blank");
            }
            else {
                alert(data.error_message)
            }
        }
    })
    return false;
}

$('#id_academic_year').change(function () {
    let branch_code =$('#id_branch_code').val();
    let academic_year = $('#id_academic_year').val();
    if (branch_code && academic_year) {
        students_filter(branch_code,academic_year)
    }
});

$('#id_branch_code').change(function () {
    let branch_code =$('#id_branch_code').val();
    let academic_year = $('#id_academic_year').val();
    if (branch_code && academic_year) {
        students_filter(branch_code,academic_year)
    }
});

function students_filter(branch_code, academic_year) {
    loder_Spinner(true)
    $.ajax({
        url: "apiedu-studentinfo-api/?branch_code=" + branch_code+"&academic_year="+academic_year,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_student_roll option").remove();
            $('#id_student_roll').select2('destroy');
            let selce2Data=[{id:'',text:'----------------'}]
            data.forEach(element => {
                option= {id:element.student_roll,text:element.student_roll + "-" + element.student_name}
                selce2Data.push(option)
            });
            $('#id_student_roll').select2({ data: selce2Data });
            loder_Spinner(false)
        }
    })
}
$("#id_student_roll option").remove();

setInterval(() => {
    let paid_inputTegs = document.querySelectorAll('.paid_amount')
    if (paid_inputTegs.length) {
        let total = 0;
        paid_inputTegs.forEach(input => {
            total += Number(input.value)
        });
        document.getElementById("total_paidAmount").textContent = total;  
    }
}, 300);