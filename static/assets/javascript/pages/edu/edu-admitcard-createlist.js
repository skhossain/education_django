$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});
"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (let i = 0; i < props.length; i++) { let descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

let table_data

const fn_data_table =
    function () {
        function fn_data_table() {
            _classCallCheck(this, fn_data_table);

            this.init();
        }

        _createClass(fn_data_table, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                const search_url = "/apiedu-admitcard-api/";
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": ""
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
                    language: {
                        paginate: {
                            previous: '<i class="fa fa-lg fa-angle-left"></i>',
                            next: '<i class="fa fa-lg fa-angle-right"></i>'
                        }
                    },
                    columns: [
                        { data: 'student_roll.student_roll' },
                        { data: 'student_roll.student_name' },
                        { data: 'class_id.class_name' },
                        { data: 'class_group_id.class_group_name' },
                        { data: 'academic_year.academic_year' },
                        { data: 'session_id.session_name' },

                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

$('#btnSearch').click(

    function () {
        //if (branch_code === "") {
        //   alert('Please Enter Branch Code!');
        // } else {
        new fn_data_table();
        //  }
    }

);

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['admit_card_id']
        }
        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['admit_card_id']
        }
    })



});

$('#btnAddRecord').click(function () {
    post_tran_table_data();
});
$('#btnUpdateRecord').click(function () {
    update_data();
});

function update_data() {
    let branch_code = $('#id_branch_code').val()
    let class_id = $('#id_class_id').val()
    let academic_year_id = $('#id_academic_year').val()
    let class_group_id = $('#id_class_group_id').val()
    let student_roll = $('#id_student_roll').val()
    let session_id = $('#id_session_id').val()
    let exam_term_id = $('#id_exam_term_id').val()
    let trams_con = $('#id_trams_con').val()
    let data_string = {
        branch_code: branch_code,
        class_id: class_id,
        academic_year_id: academic_year_id,
        class_group_id: class_group_id,
        student_roll: student_roll,
        session_id: session_id,
        exam_term_id: exam_term_id,
        trams_con: trams_con,
    }
    $.ajax({
        url: 'edu-admitcard-update',
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
            };
        }
    })
}
let academic_info = ""
$.ajax({
    url: 'apiedu-academic-info-api/',
    type: 'GET',
    dataType: 'json',
    success: function (data) {
        academic_info = data[0]
    }
})

function post_tran_table_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                // document.getElementById("tran_table_data").reset();
                // table_data.ajax.reload();
                if (data.success_message) {
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                };
            } else {
                $('#page_loading').modal('hide');
                if (data.error_message) {
                    Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: data.error_message,
                        showConfirmButton: true,
                    })
                };
            }
        }
    })
    return false;
}

$(document).ready(function () {
    $('select').select2();
    $('#id_student_roll').select2({ placeholder: " Select a Student " });
    $('#id_class_id').select2({ placeholder: " Select a Class " });
    $('#id_academic_year').select2({ placeholder: " Select a Year " });
    $('#id_session_id').select2({ placeholder: " Select a Session " });
});

$('#PDFCreate').click(function () {
    let template = $('.template')
    let tem = 0;

    for (let i = 0; template.length > i; i++) {
        if (template[i].checked) {
            tem = template[i].value
        }
    }
    if (tem == 1) {
        let branch_code = $('#id_branch_code').val()
        let class_id = $('#id_class_id').val()
        let academic_year_id = $('#id_academic_year').val()
        let class_group_id = $('#id_class_group_id').val()
        let student_roll = $('#id_student_roll').val()
        let session_id = $('#id_session_id').val()
        let exam_term_id = $('#id_exam_term_id').val()
        var pdf = new jsPDF('p', 'mm', 'a4');
        let page_counter = 0;
        let y = 0;

        let data_string = {
            branch_code: branch_code,
            class_id: class_id,
            academic_year_id: academic_year_id,
            class_group_id: class_group_id,
            student_roll: student_roll,
            session_id: session_id,
            exam_term_id: exam_term_id,
        }
        //Get Branch form header
        let form_header = ""
        let AC_logo = ""
        let principal_sin = ""
        $.ajax({
            url: 'apiedu-idcard-form-header-api/?branch_code=' + branch_code,
            type: 'GET',
            dataType: 'json',
            success: function (formHeader) {
                form_header = formHeader[0]
                toDataURL(form_header.logo, function (dataUrl) {
                    if (isImage(dataUrl)) {
                        AC_logo = dataUrl
                    }
                })
                toDataURL(form_header.sing, function (dataUrl) {
                    if (isImage(dataUrl)) {
                        principal_sin = dataUrl
                    }
                })
            }
        })
        $.ajax({
            url: '/apiedu-admitcard-api/',
            data: data_string,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#page_create').modal('show')
                $('#page_create_count').text(page_counter)
                data.forEach((st, index1) => {
                    toDataURL(st.student_roll.profile_image, function (dataUrl) {
                        if (isImage(AC_logo)) {
                            pdf.addImage(AC_logo, 'webp', 20, 20 + y, 20, 20)
                        }

                        pdf.setFontSize(16)
                        pdf.text(form_header.academic_name.toUpperCase(), 105, 20 + y, { align: 'center' })
                        pdf.setFontSize(9)
                        if (form_header.address.length) {
                            let myArray = form_header.address.split(";");
                            pdf.text(myArray, 105, 24 + y, { align: 'center' })
                        }
                        pdf.setFontSize(12).setFont(undefined, 'bold')
                        pdf.text("Admit Card", 105, 40 + y, { align: 'center' })
                        pdf.setFontSize(10).setFont(undefined, 'bold')
                        pdf.text(st.exam_term_id.term_name + "-" + st.academic_year.academic_year.toString(), 105, 46 + y, { align: 'center' })

                        pdf.setFontSize(10).setFont(undefined, 'normal')
                        pdf.rect(150, 35 + y, 40, 40, 'S')
                        pdf.text("Student's Image", 157, 50 + y)
                        // console.log(dataUrl)
                        if (isImage(dataUrl)) {
                            pdf.addImage(dataUrl, 'webp', 150, 35 + y, 40, 40)
                        }

                        pdf.text("Student's Name", 20, 55 + y)
                        pdf.text(": " + st.student_roll.student_name, 50, 55 + y)
                        pdf.text("Student's ID", 20, 60 + y)
                        pdf.text(": " + st.student_roll.student_roll, 50, 60 + y)
                        //pdf.text("Student's Reg.", 20, 60)
                        //pdf.text(": " + (st.student_roll.student_reg ? st.student_roll.student_reg : "xxxxxxxx"), 50, 60)
                        pdf.text("Class Roll", 20, 65 + y)
                        pdf.text(": " + (st.student_roll.class_roll ? st.student_roll.class_roll : ""), 50, 65 + y)
                        pdf.text("Class", 20, 70 + y)
                        pdf.text(": " + st.class_id.class_name, 50, 70 + y)
                        let group = 0
                        if (st.class_group_id) {
                            pdf.text("Class Group", 20, 75 + y)
                            pdf.text(": " + st.class_group_id.class_group_name, 50, 75 + y)
                            group = 5
                        }
                        pdf.text("Father's Name", 20, 75 + group + y)
                        pdf.text(": " + (st.student_roll.student_father_name ? st.student_roll.student_father_name : "xxxxx"), 50, 75 + group + y)
                        pdf.text("Mother's Name", 20, 80 + group + y)
                        pdf.text(": " + (st.student_roll.student_mother_name ? st.student_roll.student_mother_name : "xxxxx"), 50, 80 + group + y)
                        pdf.text("D.O.B.", 20, 85 + group + y)
                        pdf.text(": " + (st.student_roll.student_date_of_birth ? st.student_roll.student_date_of_birth : "xxxxx"), 50, 85 + group + y)
                        if (st.session_id) {
                            pdf.text("Session", 20, 90 + group + y)
                            pdf.text(": " + (st.session_id ? st.session_id : "xxxxx"), 50, 90 + group + y)
                        }
                        //INSSTRUCTIONS TO THE CANDIDATE 

                        if (st.trams_con.length) {
                            let myArray = st.trams_con.split(";");
                            pdf.text(myArray, 20, 95 + group + y)
                        }

                        pdf.line(20, 130 + y, 65, 130 + y, "S")
                        pdf.text("Issuer", 32, 134 + y)
                        // pdf.line(88, 260, 130, 260, "S")
                        // pdf.text("Register", 100, 264)
                        // principal_sin
                        if (isImage(principal_sin)) {
                            pdf.addImage(principal_sin, 'webp', 150, 118 + y, 50, 10)
                        }
                        pdf.line(150, 130 + y, 190, 130 + y, "S")
                        pdf.text("Principal", 163, 134 + y)

                        page_counter += 1;
                        y = 140;
                        $('#page_create_count').text(page_counter)

                        if (data.length == page_counter) {
                            setTimeout(() => {
                                $('#page_create').modal('hide')
                                pdf.save('Admid Card-' + st.class_id.class_name + '.pdf')
                            }, 1000);
                        }
                        else {
                            if ((page_counter - 1) % 2) {
                                pdf.addPage()
                                y = 0;
                            }
                        }

                    })
                });
            }
        })
    } else if (tem == 2) {
        let class_id = $('#id_class_id').val()
        let academic_year_id = $('#id_academic_year').val()
        let class_group_id = $('#id_class_group_id').val()
        let student_roll = $('#id_student_roll').val()
        let session_id = $('#id_session_id').val()
        var pdf = new jsPDF('p', 'mm', 'a4');
        let page_counter = 0;
        let data_string = {
            class_id: class_id,
            academic_year_id: academic_year_id,
            class_group_id: class_group_id,
            student_roll: student_roll,
            session_id: session_id,
        }
        $.ajax({
            url: '/apiedu-admitcard-api/',
            data: data_string,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#page_create').modal('show')
                $('#page_create_count').text(page_counter)
                data.forEach((st, index1) => {
                    toDataURL(st.student_roll.profile_image, function (dataUrl) {
                        $.ajax({
                            url: '/apiedu-subjectchoice-api/?student_roll=' + st.student_roll.student_roll,
                            type: 'GET',
                            dataType: 'json',
                            success: function (subjects) {
                                let x = 0;
                                let y = 0;

                                for (let i = 0; i < subjects.length; i++) {

                                    if (i == 0) {
                                        pdf.setFontSize(10)
                                        pdf.text("Subject's Code", 30, 105 + y)
                                        pdf.text("Subject's Name", 110, 105 + y)

                                        pdf.line(20, 100 + y, 200, 100 + y, "S")

                                        pdf.line(20, 100 + y, 20, 108 + y, "S")
                                        pdf.line(100, 100 + y, 100, 108 + y, "S")
                                        pdf.line(200, 100 + y, 200, 108 + y, "S")
                                    }

                                    pdf.line(20, 108 + y, 200, 108 + y, "S")

                                    pdf.line(20, 108 + y, 20, 116 + y, "S")
                                    pdf.line(100, 108 + y, 100, 116 + y, "S")
                                    pdf.line(200, 108 + y, 200, 116 + y, "S")
                                    pdf.setFontSize(9)
                                    pdf.text((subjects[i].subject_id.subject_code ? (subjects[i].subject_id.subject_code).toString() : "xxxx"), 30, 113 + y)
                                    pdf.text((subjects[i].subject_id.subject_name), 110, 113 + y)
                                    y = (i + 1) * 8
                                    if (subjects.length == i + 1) {
                                        page_counter += 1
                                    }
                                }
                                pdf.line(20, 108 + subjects.length * 8, 200, 108 + subjects.length * 8, 'S')

                                pdf.setFontSize(18)
                                pdf.text(academic_info.academic_name.toUpperCase(), 105, 20, { align: 'center' })
                                pdf.setFontSize(9)
                                pdf.text(academic_info.academic_address, 105, 24, { align: 'center' })
                                pdf.text(academic_info.academic_mobile_1 + (academic_info.academic_mobile_2 ? "," : "") + (academic_info.academic_mobile_2 ? academic_info.academic_mobile_2 : ""), 105, 28, { align: 'center' })
                                pdf.text((academic_info.academic_email ? academic_info.academic_email : ""), 105, 32, { align: 'center' })
                                pdf.text((academic_info.academic_website ? academic_info.academic_website : ""), 105, 36, { align: 'center' })

                                pdf.setFontSize(10)
                                pdf.text("Student's Image", 160, 55)
                                if (isImage(dataUrl)) {
                                    pdf.addImage(dataUrl, 'webp', 158, 50, 30, 30)
                                }

                                pdf.text("Student's Name", 20, 50)
                                pdf.text(": " + st.student_roll.student_name, 50, 50)
                                pdf.text("Student's Roll", 20, 55)
                                pdf.text(": " + st.student_roll.student_roll, 50, 55)
                                //pdf.text("Student's Reg.", 20, 60)
                                //pdf.text(": " + (st.student_roll.student_reg ? st.student_roll.student_reg : "xxxxxxxx"), 50, 60)
                                pdf.text("Class Roll", 20, 60)
                                pdf.text(": " + (st.student_roll.class_roll ? st.student_roll.class_roll : ""), 50, 60)
                                pdf.text("Student's Class", 20, 65)
                                pdf.text(": " + st.class_id.class_name, 50, 65)
                                pdf.text("Father's Name", 20, 70)
                                pdf.text(": " + (st.student_roll.student_father_name ? st.student_roll.student_father_name : "xxxxx"), 50, 70)
                                pdf.text("Mother's Name", 20, 75)
                                pdf.text(": " + (st.student_roll.student_mother_name ? st.student_roll.student_mother_name : "xxxxx"), 50, 75)
                                pdf.text("D.O.B.", 20, 80)
                                pdf.text(": " + (st.student_roll.student_date_of_birth ? st.student_roll.student_date_of_birth : "xxxxx"), 50, 80)
                                if (st.session_id) {
                                    pdf.text("Session", 20, 85)
                                    pdf.text(": " + (st.session_id ? st.session_id : "xxxxx"), 50, 85)
                                }

                                pdf.line(20, 260, 65, 260, "S")
                                pdf.text("Student's Signature", 28, 264)
                                pdf.line(88, 260, 130, 260, "S")
                                pdf.text("Register", 100, 264)
                                pdf.line(150, 260, 190, 260, "S")
                                pdf.text("Principal", 163, 264)
                                $('#page_create_count').text(page_counter)
                                if (data.length == page_counter) {
                                    setTimeout(() => {
                                        pdf.save('admit.pdf')
                                    }, 1000);
                                }
                                else {
                                    pdf.addPage()
                                    $('#page_create').modal('hide')
                                }
                            }
                        })

                    })
                });
            }
        })
    }
})
function toJpeg(imgurl, callback) {
    /*
    * Create a new XMLHttpRequest to request image to get image Base64
    * Repeat requests will occur here, but are cached :)
    */
    var xhr = new XMLHttpRequest();
    xhr.open("get", imgurl);
    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status == 200) {
            // Here get the binary code of the file and read out contents
            var blob = this.response;

            var oFileReader = new FileReader();
            oFileReader.onloadend = function (e) {
                // Create a new Image Obj
                var newImg = new Image();
                // Set crossOrigin Anonymous (That's important, otherwise it will not be read)
                newImg.crossOrigin = "Anonymous";
                newImg.onload = function () {
                    // Create a new Canvas
                    var canvas = document.createElement("canvas");
                    // Set 2D context
                    var context = canvas.getContext("2d");
                    // Set crossOrigin Anonymous (That's important, otherwise it will not be read)
                    canvas.crossOrigin = "anonymous";
                    // Set Width/Height
                    canvas.width = newImg.width;
                    canvas.height = newImg.height;
                    // Start
                    context.drawImage(newImg, 0, 0);
                    // Get jpeg Base64
                    let base64 = canvas.toDataURL("image/jpeg");
                    // console.log(base64)
                    callback(base64);
                };
                // Load Webp Base64
                //newImg.src = e.target.result;
            };
            oFileReader.readAsDataURL(blob);
        } else {
            return
        }
    };
    xhr.send();
}
const get64 = url => fetch(url)
    .then(response => response.blob())
    .then(blob => new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(blob)
    }))

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
    var session_id = document.getElementById('id_session_id').value
    var datastring = {
        academic_year: academic_year,
        class_id: class_id,
        class_group_id: class_group_id,
        session_id: session_id,
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
