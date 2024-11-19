$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$(document).ready(function () {
    $('select').select2();
});
click_enable = 1;
$('#btnAddRecord').on('click', function () {
    if (click_enable) {
        click_enable = 0;
        submit_record();
    }
    setTimeout(function () {
        click_enable = 1;
    }, 1000); //Time before execution

})

$('#btnSearch').on('click', function () {
    if (click_enable) {
        click_enable = 0;
        search_record();
    }
    setTimeout(function () {
        click_enable = 1;
    }, 1000); //Time before execution
})

function submit_record() {
    document.getElementById('btnAddRecord').disabled = true;
    let branch_code = $('#id_branch_code').val();
    let academic_year = $('#id_academic_year').val();
    let session_id = $('#id_session_id').val();
    let class_id = $('#id_class_id').val();
    let class_group_id = $('#id_class_group_id').val();
    let term_id = $('#id_term_id').val();
    let short_number = $('#id_short_number').val();
    let subject_one_id = $('#id_subject_one_id').val();
    let subject_two_id = $('#id_subject_two_id').val();
    let subject_three_id = $('#id_subject_three_id').val();

    if (branch_code && academic_year && class_id && term_id && subject_one_id) {
        let data_string = {
            branch_code: branch_code,
            academic_year: academic_year,
            session_id: session_id,
            class_id: class_id,
            class_group_id: class_group_id,
            term_id: term_id,
            short_number: short_number,
            subject_one_id: subject_one_id,
            subject_two_id: subject_two_id,
            subject_three_id: subject_three_id,
        }

        $.ajax({
            url: 'edu-result-view-setting',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (data.success_message) {
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                    document.getElementById('btnAddRecord').disabled = false;
                };
            }
        })
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: "Branch Name, Year, Class Name, Term and Subject One is required.",
            showConfirmButton: false,
            timer: 1500
        })
        document.getElementById('btnAddRecord').disabled = false;
    }
}

function search_record() {
    let branch_code = $('#id_branch_code').val();
    let academic_year = $('#id_academic_year').val();
    let session_id = $('#id_session_id').val();
    let class_id = $('#id_class_id').val();
    let class_group_id = $('#id_class_group_id').val();
    let term_id = $('#id_term_id').val();

    let data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        session_id: session_id,
        class_id: class_id,
        class_group_id: class_group_id,
        term_id: term_id,


    }
    $.ajax({
        url: 'apiedu-result-view-setting-api/',
        data: data_string,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            let table = `<table class="table table-sm"></tr>
        <th>Year</th>
        <th>Session</th>
        <th>Class</th>
        <th>Class Group</th>
        <th>Exam</th>
        <th>Subject One</th>
        <th>Subject Two</th>
        <th>Subject Three</th>
        <th>Sort by</th>
        <th>Action</th>
        </tr>
        `
            data.forEach(element => {
                table += `<tr id="${element.result_view_id}">
            <td>${element.academic_year.academic_year}</td>
            <td>${element.session_id ? element.session_id.session_name : ""}</td>
            <td>${element.class_id.class_name}</td>
            <td>${element.class_group_id ? element.class_group_id.class_group_name : ""}</td>
            <td>${element.term_id.term_name}</td>
            <td>${element.subject_one_id ? element.subject_one_id.subject_name : ""}</td>
            <td>${element.subject_two_id ? element.subject_two_id.subject_name : ""}</td>
            <td>${element.subject_three_id ? element.subject_three_id.subject_name : ""}</td>
            <td>${element.short_number}</td>
            <td>
            <button class="btn btn-sm btn-danger" onclick="delete_setting('${element.result_view_id}')">Delete</button>
            </td>
            </tr>`
            });
            table += `</table>`
            $('#view-list table').remove()
            $('#view-list').append(table)

        }
    })
}
function delete_setting(id) {
    $.ajax({
        url: "/edu-result-view-setting-delete",
        type: 'post',
        data: { id: id },
        datatype: 'json',
        success: function (data) {
            if (data.success_message) {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: data.success_message,
                    showConfirmButton: false,
                    timer: 1500
                })
                $('#' + id).remove()
            }
        }
    })
}

$('#id_class_id').change(function () {
    class_group_filter()
    filtering_subjectlist()
})
$('#id_class_group_id').change(function () {
    filtering_subjectlist()
})

function class_group_filter() {
    let class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $('#id_class_group_id').empty()
            data.forEach(element => {
                var newOption = new Option(element.class_group_name, element.class_group_id, false, false);
                $('#id_class_group_id').append(newOption).trigger('change');
            });
        }
    })
}

function filtering_subjectlist() {
    let class_id = document.getElementById('id_class_id').value
    let class_group_id = document.getElementById('id_class_group_id').value

    $.ajax({
        url: "apiedu-sublist-api/?class_id=" + class_id + "&class_group_id=" + class_group_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_subject_one_id option").remove();
            $("#id_subject_two_id option").remove();
            $("#id_subject_three_id option").remove();
            $("#id_subject_one_id").append('<option value="">------------</option>');
            $("#id_subject_two_id").append('<option value="">------------</option>');
            $("#id_subject_three_id").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#id_subject_one_id").append('<option value="' + element.subject_id + '">' + element.subject_name + '</option>');
                $("#id_subject_two_id").append('<option value="' + element.subject_id + '">' + element.subject_name + '</option>');
                $("#id_subject_three_id").append('<option value="' + element.subject_id + '">' + element.subject_name + '</option>');
            });
        }
    })
}