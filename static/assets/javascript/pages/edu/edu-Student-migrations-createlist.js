$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function update_selected_students() {
    loder_Spinner(true)
    let academic_year = $('#id_to_accademic_year').val()
    let class_id = $('#id_to_class').val()
    let class_group = $('#id_to_class_group').val()
    let section = $('#id_to_section').val()
    let comments = $('#id_comments').val()

    var students = document.querySelectorAll('.selectedstudents')
    var selected_students = []
    students.forEach(element => {
        if (element.checked) {
            selected_students.push(element.value)
        }
    });

    let data_string = {
        academic_year: academic_year,
        class_id: class_id,
        class_group: class_group,
        section: section,
        comments: comments,
        selected_students: selected_students
    }
    if (academic_year && class_id && selected_students.length > 0) {
        $.ajax({
            url: 'edu-selected-students-update',
            type: 'post',
            data: data_string,
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    loder_Spinner(false)
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                    $("#student_list div").remove();
                } else {
                    loder_Spinner(false)
                    Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: data.error_message,
                        showConfirmButton: true,
                    })
                }

            }
        })
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Targeted Academic Year, Class Name and at least one student Required',
            showConfirmButton: true,
            // timer: 1500
        })
    }



}


$(document).ready(function () {
    $('#id_from_accademic_year').select2();
    $('#id_from_class').select2();
    $('#id_to_accademic_year').select2();
    $('#id_to_class').select2();
    $('#id_from_class_group').select2();
    $('#id_from_section').select2();
    $('#id_to_section').select2();
    $('#id_to_section').select2();
    $('#id_to_class_group').select2();
    $('#id_student_roll').select2();

})


$('#id_from_class').change(function () {
    from_class_group_filter()
})

function from_class_group_filter() {
    var class_id = document.getElementById('id_from_class').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_from_class_group option").remove();
            $("#id_from_class_group").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_from_class_group").append('<option value="' + element.class_group_id + '">' + element.class_group_name + '</option>');
            });
        }
    })
}

$('#id_to_class').change(function () {
    class_group_filter()
})


function class_group_filter() {
    var class_id = document.getElementById('id_to_class').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_to_class_group option").remove();
            $("#id_to_class_group").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_to_class_group").append('<option value="' + element.class_group_id + '">' + element.class_group_name + '</option>');
            });
        }
    })
}


function class_student_filter() {
    loder_Spinner(true)
    var branch_code = document.getElementById('id_branch_code').value
    var academic_year = document.getElementById('id_from_accademic_year').value
    var class_id = document.getElementById('id_from_class').value
    var class_group_id = document.getElementById('id_from_class_group').value
    var session_id = document.getElementById('id_from_section').value
    datastring = {
        academic_year: academic_year,
        branch_code: branch_code,
        class_id: class_id,
        class_group_id: class_group_id,
        session_id: session_id,
    }
    if (branch_code && academic_year && class_id) {
        $.ajax({
            url: "apiedu-studentinfo-api/",
            data: datastring,
            type: 'get',
            datatype: 'json',
            success: function (data) {
                $("#student_list div").remove();
                $("#student_list").append(`<div class="form-check">
                                <input class="form-check-input" type="checkbox" value="" onchange="select_all()" id="all_select">
                                <label class="form-check-label" for="all_select">
                                    All Select
                                </label>
                                </div><hr>`);

                let checkBox = `<div class="row">`;
                let mid = Math.ceil(data.length / 2)
                checkBox += `<div class="col-md-6">`
                for (let i = 0; i < mid; i++) {
                    let element = data[i]
                    checkBox += `<div class="form-check">
                                <input class="form-check-input selectedstudents" type="checkbox" value="${element.student_roll}" id="${element.student_roll}">
                                <label class="form-check-label" for="${element.student_roll}">
                                    ${element.student_roll + '-' + element.student_name}
                                </label>
                                </div>`
                }
                checkBox += `</div>`
                if (mid < data.length) {
                    checkBox += `<div class="col-md-6">`
                    for (let j = mid; j < data.length; j++) {
                        let element = data[j]
                        checkBox += `<div class="form-check">
                                <input class="form-check-input selectedstudents" type="checkbox" value="${element.student_roll}" id="${element.student_roll}">
                                <label class="form-check-label" for="${element.student_roll}">
                                    ${element.student_roll + '-' + element.student_name}
                                </label>
                                </div>`
                    }
                    checkBox += `</div>`
                }

                checkBox += `</div>`
                $("#student_list").append(checkBox);
                loder_Spinner(false)
            }
        })
    } else {
        // loder_Spinner(false)
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Branch Name, Academic Year and Class Name Required',
            showConfirmButton: true,
            // timer: 1500
        })
    }
}

function select_all() {
    var selectTogole = document.getElementById('all_select')
    var students = document.querySelectorAll('.selectedstudents')
    students.forEach(element => {
        element.checked = selectTogole.checked;
    });

}
$('select').select2()