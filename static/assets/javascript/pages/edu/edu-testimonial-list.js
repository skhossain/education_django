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
    get_board_names()
    get_certificate_names()
});
let board_list=[]
let certificate_list=[]

$('#id_branch_code').on('change', function () {
    certificateName_filter()
    get_board_names()
    get_certificate_names()
})
function get_board_names() {
    let branch_code = document.getElementById('id_branch_code').value
    $.ajax({
        url: "apiedu-board-name-api/",
        type: 'get',
        data: { branch_code },
        datatype: 'json',
        success: function (data) {
            board_list=data
        }
    })
}
function get_certificate_names() {
    let branch_code = document.getElementById('id_branch_code').value
    $.ajax({
        url: "apiedu-certificat-name-api/",
        type: 'get',
        data: { branch_code },
        datatype: 'json',
        success: function (data) {
            certificate_list=data
        }
    })
}
function certificateName_filter() {
    let branch_code = document.getElementById('id_branch_code').value
    $.ajax({
        url: "apiedu-certificat-name-api/?branch_code=" + branch_code,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $('#id_cerfificate_name').empty()
            data.forEach(element => {
                var newOption = new Option(element.certificat_full_name, element.id, false, false);
                $('#id_cerfificate_name').append(newOption).trigger('change');
            });
        }
    })
}

$('#btnSearch').on('click', function () {
    let branch_code = document.getElementById('id_branch_code').value
    let student_roll = document.getElementById('id_student_roll').value
    let testimonial_id = document.getElementById('id_testimonial_id').value
    let academic_year = document.getElementById('id_academic_year').value
    let cerfificate_name = document.getElementById('id_cerfificate_name').value
    if (branch_code) {
        $.ajax({
            url: "apiedu-testimonial-api/",
            type: 'get',
            data: { branch_code, student_roll, testimonial_id, academic_year, cerfificate_name },
            datatype: 'json',
            success: function (data) {
                $('#testimonial_tr tr').remove()
                data.forEach(testimonial => {
                    let tr = `<tr>`
                    tr += `<td>${testimonial.testmonial_id}</td>`
                    tr += `<td>${testimonial.student_roll.student_roll}</td>`
                    tr += `<td>${testimonial.student_roll.student_name}</td>`
                    tr += `<td>${testimonial.cert_name_id.certificat_full_name}</td>`
                    tr += `<td>
                        <button class="btn btn-sm btn-info" onclick="testimonial_print('${testimonial.testmonial_id}')">Print</button>
                        <button class="btn btn-sm btn-info" onclick="testimonial_edit('${testimonial.testmonial_id}')">Edit</button>
                        </td>`
                    tr += `</tr>`
                    $('#testimonial_tr').append(tr)
                });
            }
        })
    }
})

function testimonial_edit(id) {
    $.ajax({
        url: "apiedu-testimonial-api/",
        type: 'get',
        data: { testimonial_id:id },
        datatype: 'json',
        success: function (data) {
            const testimonial=data[0]
            let boardOptions = ``
            let certificateNames=``
            board_list.forEach(board => {
                boardOptions += `<option value="${board.id}" ${testimonial.education_board_id == board.id ? "selected":"" }>${board.board_full_name}</option>`
            });
            certificate_list.forEach(cert => {
                certificateNames += `<option value="${cert.id}" ${testimonial.cert_name_id.id == cert.id ? "selected" : ""}>${cert.certificat_full_name}</option>`
            });
            let html = `<form id="test_edit"><div class="card p-3">
            <div class="card-heade">
            <h5>Edit Testimonial</h5>
            </div>
            <div class="card-body">
             <div class="form-row pb-3" >
                <input type="hidden" name="testmonial_id" id="edit_testmonial_id" value="${testimonial.testmonial_id}">
            
                <div class="form-group col-md-3 mb-0">
                    <label>Education Board</label>
                    <select class="form-control" name="education_board_id">
                        ${boardOptions}
                    </select>
                </div>
                <div class="form-group col-md-3 mb-0">
                    <label>Certificate Name</label>
                    <select class="form-control" name="cert_name_id">
                        ${certificateNames}
                    </select>
                </div>
                <div class="form-group col-md-3 mb-0">
                    <label>Year</label>
                    <input type="number" class="form-control" name="academic_year" value="${testimonial.academic_year}">
                </div>
                <div class="form-group col-md-3 mb-0">
                    <label>Group Name</label>
                    <input type="text" class="form-control" name="group_name" value="${testimonial.group_name}">
                </div>
                <div class="form-group col-md-3 mb-0">
                    <label>Board Roll</label>
                    <input type="text" class="form-control" name="board_roll" value="${testimonial.board_roll}">
                </div>
                <div class="form-group col-md-3 mb-0">
                    <label>Registration No</label>
                    <input type="text" class="form-control" name="board_reg" value="${testimonial.board_reg}">
                </div>
                <div class="form-group col-md-3 mb-0">
                    <label>Grade Point</label>
                    <input type="number" step="0.1" class="form-control" name="grade_point" value="${testimonial.grade_point}">
                </div>
                <div class="form-group col-md-3 mb-0">
                    <label>Grade Later</label>
                    <input type="text" class="form-control" name="grade_name" value="${testimonial.grade_name}">
                </div>
                <div class="col-12 py-3">
                <button type="button" class="btn btn-info" onclick="testimonial_edit_submit('${testimonial.testmonial_id}')">Save Change</button>
                </div>
            </div>
            </div>
            </div></form>` 
            $('#edit_model').modal('show');
            $('#edit_model .modal-content').html(html);
        }
    })
}

function testimonial_edit_submit() {
    const data_string = $("#test_edit").serialize();
    let testmonial_id = $('#edit_testmonial_id').val()
    const data_url = '/edu-edit-testimonial/' + testmonial_id;
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            $('#page_loading').modal('hide');
            $('#edit_model').modal('hide');
        }
    })
    
}

function testimonial_print(id) {
    const url = location.protocol + '//' + location.host + '/edu-student-testimonial/' + id;
    console.log(url)
    window.open(url)
}