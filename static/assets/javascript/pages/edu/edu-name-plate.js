function fn_student_data() {
    var academic_year = document.getElementById('id_academic_year').value
    var class_id = document.getElementById('id_class_id').value
    var class_group_id = document.getElementById('id_class_group_id').value
    var student_roll = document.getElementById('id_student_roll').value

    postdata = {
        academic_year: academic_year,
        class_id: class_id,
        class_group_id: class_group_id,
        student_roll: student_roll
    }

    if (class_id && academic_year) {
        $.ajax({
            url: '/edu-nameplate-searchstudent',
            type: 'POST',
            data: postdata,
            datatype: 'json',
            success: function (data) {
                $('#auto_row').html(data.html_form);
            }
        })
    } else {
        Swal.fire(
            'Please select-academic year and class ',
            'value is null.',
            'error'
        )
    }
}



function allselect(source) {
    var checkboxes = document.querySelectorAll('.student');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}


function save_choices_students() {
    var academic_year = document.getElementById('id_academic_year').value
    var class_id = document.getElementById('id_class_id').value
    var class_group_id = document.getElementById('id_class_group_id').value
    var slogan = document.getElementById('id_slogan').value
    if (class_id && academic_year) {
        var students = []
        document.querySelectorAll('.student').forEach(S => {

            let stu = { student_roll: S.value, student_status: 'I' }
            if (S.checked) {
                stu = { student_roll: S.value, student_status: 'A' }
            }
            students.push(JSON.stringify(stu))
        })
        postdata = {
            academic_year: academic_year,
            class_id: class_id,
            class_group_id: class_group_id,
            student_roll: students,
            slogan: slogan,
        }
        $.ajax({
            url: '/edu-nameplate-studentinsert',
            data: postdata,
            type: 'POST',
            datatype: 'json',
            success: function (data) {
                if (data.error_message) {
                    Swal.fire(
                        'Data Save!',
                        data.error_message,
                        'error'
                    )
                } else {
                    Swal.fire(
                        'Data Save!',
                        data.success_message,
                        'success'
                    )
                }
            }
        })
    } else {
        Swal.fire(
            'Data Missing!',
            'value is null.',
            'error'
        )
    }
}



$(document).ready(function () {
    $('#id_student_roll').select2({ placeholder: " Select a Student " });
    $('#id_class_id').select2({ placeholder: " Select a Class " });
    $('#id_academic_year').select2({ placeholder: " Select a Year " });
    $('#id_class_group_id').select2({ placeholder: " Select a Group " });
});


let academic_info = ""
$.ajax({
    url: 'apiedu-academic-info-api/',
    type: 'GET',
    dataType: 'json',
    success: function (data) {
        academic_info = data[0]
    }
})


$('#PDFCreate').click(function () {
    let class_id = $('#id_class_id').val()
    let academic_year_id = $('#id_academic_Year').val()
    let class_group_id = $('#id_class_group_id').val()
    let student_roll = $('#id_student_roll').val()
    var pdf = new jsPDF('p', 'mm', 'a4');
    let logo = ""
    let download = false;

    let data_string = {
        class_id: class_id,
        academic_year: academic_year_id,
        class_group_id: class_group_id,
        student_roll: student_roll,
    }
    $.ajax({
        url: '/apiedu-nameplate-api/?',
        data: data_string,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.length > 0) {
                let y = 3;
                let x = 0;
                let row = 1;
                data.forEach((student, index) => {
                    pdf.rect(10 + x, 4 + y, 75, 40)
                    pdf.setFontStyle('bold');
                    pdf.setFontSize(11)
                    pdf.text(student.student_roll.student_name, 45 + x, 10 + y, { align: 'center' })
                    pdf.setFontSize(10)
                    pdf.setFontStyle('normal');
                    pdf.text('ID ', 12 + x, 16 + y)
                    pdf.text(': ' + student.student_roll.student_roll, 30 + x, 16 + y)
                    let class_roll = student.student_roll.class_roll ? student.student_roll.class_roll : ''
                    pdf.text('Class Roll ', 12 + x, 20 + y)
                    pdf.text(': ' + class_roll, 30 + x, 20 + y)
                    pdf.text('Class ', 12 + x, 24 + y)
                    pdf.text(': ' + student.class_id.class_name, 30 + x, 24 + y)
                    let group_name = student.class_group_id ? student.class_group_id.class_group_name : ''
                    pdf.text('Group ', 12 + x, 28 + y)
                    pdf.text(': ' + group_name, 30 + x, 28 + y)
                    pdf.line(10 + x, 30 + y, 85 + x, 30 + y)

                    if (student.slogan.length) {
                        pdf.setFontSize(9)
                        let myArray = student.slogan.split(";");
                        pdf.text(myArray, 45 + x, 34 + y, { align: 'center' })
                    }

                    x = x + 85
                    if ((index + 1) % 2 == 0) {
                        x = 0
                        y = (row * 45) + 3
                        row += 1
                    }

                    if (row == 7) {
                        y = 3
                        row = 1
                        pdf.addPage("a4");
                    }

                    if (data.length == index + 1) {
                        setTimeout(() => {
                            pdf.save("nameplate" + Date.now() + '.pdf')
                        }, 100);
                    }
                });

            } else {
                Swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: 'There is no data in this filter .',
                    showConfirmButton: true,
                })
            }
        }
    })

});

function toDataURL(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () {
        var reader = new FileReader();
        reader.onloadend = function () {
            callback(reader.result);
        }
        reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
}

function isImage(data) {
    let mim = data.split(';')
    mim[0].slice(5)
    let image_exe = ['image/gif', 'image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/webp']
    if (image_exe.indexOf(mim[0].slice(5)) < 0) {
        return false
    } else {
        return true
    }
}



$('#id_class_id').change(function () {
    class_group_filter()
})

function class_group_filter() {
    var class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_class_group_id option").remove();
            $("#id_class_group_id").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_class_group_id").append('<option value="' + element.class_group_id + '">' + element.class_group_name + '</option>');
            });
        }
    })
}

$('#id_class_id').change(function () {
    class_student_filter()
})

function class_student_filter() {
    var academic_year = document.getElementById('id_academic_year').value
    var class_id = document.getElementById('id_class_id').value
    var class_group_id = document.getElementById('id_class_group_id').value
    var student_roll = document.getElementById('id_student_roll').value
    var datastring = {
        academic_year: academic_year,
        class_id: class_id,
        class_group_id: class_group_id,
        student_roll: student_roll,
    }
    $.ajax({
        url: "apiedu-studentinfo-api/",
        data: datastring,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_student_roll option").remove();
            $("#id_student_roll").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_student_roll").append('<option value="' + element.student_roll + '">' + element.student_roll + '-' + element.student_name + '</option>');
            });
        }
    })
}