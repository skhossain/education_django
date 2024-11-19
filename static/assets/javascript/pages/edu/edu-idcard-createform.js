$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code).trigger('change');
});

import { ansiFont as fontKalpurush } from '../../fonts/kalpurush-normal-font.js'

//=====================================================
"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) {
    for (let i = 0; i < props.length; i++) {
        let descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}

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
                let class_id = $('#id_class_id').val()
                let academic_year = $('#id_academic_Year').val()
                let class_group_id = $('#id_class_group_id').val()
                let student_roll = $('#id_student_roll').val()
                let branch_code = $('#id_branch_code').val()
                let expire_date = $('#id_expire_date').val()
                const search_url = "/apiedu-idcard-api/?class_id=" + class_id + "&academic_year=" + academic_year + "&class_group_id=" + class_group_id + "&student_roll=" + student_roll + "&branch_code=" + branch_code + "&expire_date=" + expire_date;
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
                        { data: 'academic_Year.academic_year' },
                        { data: 'expire_date' },
                        { data: 'back_text' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>'
                        }
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
            id = table_row['id_card_no']
        } catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id_card_no']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/edu-idcard-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#edit_model').modal('show');
            },
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }

});

$('#btnAddRecord').click(function () {
    post_tran_table_data();
});
$('#btnUpdateRecord').click(function () {
    post_update_data();
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
                table_data.ajax.reload();
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

function post_update_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = '/edu-idcard-update';
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                table_data.ajax.reload();
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
    $('#id_student_roll').select2({ placeholder: " Select a Student " });
    $('#id_class_id').select2({ placeholder: " Select a Class " });
    $('#id_academic_Year').select2({ placeholder: " Select a Year " });
    $('#id_session_id').select2({ placeholder: " Select a Session " });

});


let idCard_info = ''

function idcard_data_get() {
    let branch_code = document.getElementById('id_branch_code').value;
    $.ajax({
        url: '/apiedu-idcard-form-header-api/?branch_code=' + branch_code,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // console.log(idCard_info)
            idCard_info = data[0]

        }
    })
}

$('#PDFCreate').click(function () {
    idcard_data_get()

    let class_id = $('#id_class_id').val()
    let academic_year_id = $('#id_academic_Year').val()
    let class_group_id = $('#id_class_group_id').val()
    let student_roll = $('#id_student_roll').val()
    let branch_code = $('#id_branch_code').val()
    let expire_date = $('#id_expire_date').val()
    var pdf = new jsPDF('p', 'mm', 'a4', { filters: ["ASCIIHexEncode"] });

    var pdf = new jsPDF('p', 'mm', 'a4');
    let logo = ""
    let sing = ""
    let download = false;

    if (class_id && academic_year_id) {
        setTimeout(() => {

            if (idCard_info.logo) {
                toDataURL(idCard_info.logo, function (dataUrl) {
                    if (isImage(dataUrl)) {
                        logo = dataUrl
                    }
                })

            }

            if (idCard_info.sing) {
                toDataURL(idCard_info.sing, function (dataUrl) {
                    if (isImage(dataUrl)) {
                        sing = dataUrl
                    }
                })

            }

            let data_string = {
                class_id: class_id,
                academic_year: academic_year_id,
                class_group_id: class_group_id,
                student_roll: student_roll,
                branch_code: branch_code,
                expire_date: expire_date
            }
            $.ajax({
                url: '/apiedu-idcard-api/?',
                data: data_string,
                type: 'GET',
                dataType: 'json',
                success: function (data) {

                    //QR Code
                    data.forEach((student, index) => {
                        let qr_codeDiv = `<div id="qr_${student.student_roll.student_roll}">${student.student_roll.student_roll}</div>`
                        $('#QRCode-div').append(qr_codeDiv)
                        generateqr(student.student_roll.student_roll)
                    });

                    setTimeout(() => {
                        if (data.length > 0) {
                            let y = 0;
                            let row = 1;
                            data.forEach((student, index) => {
                                toDataURL(student.student_roll.profile_image, function (dataUrl) {
                                    pdf.setFillColor(255, 255, 255);
                                    pdf.setDrawColor(0, 0, 139);
                                    pdf.rect(10, 5 + y, 86, 54, 'FD')
                                    pdf.setFillColor(0, 0, 139);
                                    pdf.setDrawColor(0, 0, 139);
                                    pdf.rect(10, 5 + y, 86, 14, 'FD')
                                    if (logo) {
                                        pdf.addImage(logo, 'png', 11, 6 + y, 12, 12)
                                    }

                                    pdf.setFontSize((10 * 29) / idCard_info.academic_name.length)
                                    pdf.setTextColor('#FFFFFF')
                                    pdf.setFontStyle('bold');
                                    pdf.text(idCard_info.academic_name.toUpperCase(), 59, 12 + y, { align: 'center' })
                                    //Student info
                                    // console.log(dataUrl)
                                    if (isImage(dataUrl)) {
                                        pdf.addImage(dataUrl, 'png', 11, 20 + y, 15, 15)
                                    }
                                    pdf.setFontStyle('normal');
                                    pdf.setTextColor('#0000FF')
                                    pdf.text(student.student_roll.student_name, 30, 25 + y)
                                    pdf.setFontSize(8)
                                    pdf.setTextColor('#000000')
                                    pdf.text("Student ID", 30, 28 + y)
                                    pdf.text(": " + student.student_roll.student_roll, 50, 28 + y)
                                    pdf.text("Class", 30, 31 + y)
                                    pdf.text(": " + student.class_id.class_name, 50, 31 + y)

                                    if (student.class_group_id && student.section_id && student.session_id) {
                                        pdf.text("Group", 30, 34 + y)
                                        pdf.text(": " + student.class_group_id.class_group_name, 50, 34 + y)
                                        pdf.text("Section", 30, 37 + y)
                                        pdf.text(": " + student.section_id.section_name, 50, 37 + y)
                                        pdf.text("Session", 30, 40 + y)
                                        pdf.text(": " + student.session_id.session_name, 50, 40 + y)
                                        pdf.text("Blood Group", 30, 43 + y)
                                        pdf.text(": " + student.student_roll.student_blood_group, 50, 43 + y)
                                        pdf.text("Father's Name", 30, 46 + y)
                                        pdf.text(": " + student.student_roll.student_father_name, 50, 46 + y)
                                        pdf.text("Mother's Name", 30, 49 + y)
                                        pdf.text(": " + student.student_roll.student_mother_name, 50, 49 + y)
                                    } else if (student.class_group_id && student.section_id) {
                                        pdf.text("Group", 30, 34 + y)
                                        pdf.text(": " + student.class_group_id.class_group_name, 50, 34 + y)
                                        pdf.text("Section", 30, 37 + y)
                                        pdf.text(": " + student.section_id.section_name, 50, 37 + y)

                                        pdf.text("Blood Group", 30, 40 + y)
                                        pdf.text(": " + student.student_roll.student_blood_group, 50, 40 + y)
                                        pdf.text("Father's Name", 30, 43 + y)
                                        pdf.text(": " + student.student_roll.student_father_name, 50, 43 + y)
                                        pdf.text("Mother's Name", 30, 46 + y)
                                        pdf.text(": " + student.student_roll.student_mother_name, 50, 46 + y)
                                    } else if (student.class_group_id) {
                                        pdf.text("Group", 30, 34 + y)
                                        pdf.text(": " + student.class_group_id.class_group_name, 50, 34 + y)

                                        pdf.text("Blood Group", 30, 37 + y)
                                        pdf.text(": " + student.student_roll.student_blood_group, 50, 37 + y)
                                        pdf.text("Father's Name", 30, 40 + y)
                                        pdf.text(": " + student.student_roll.student_father_name, 50, 40 + y)
                                        pdf.text("Mother's Name", 30, 43 + y)
                                        pdf.text(": " + student.student_roll.student_mother_name, 50, 43 + y)
                                    } else {
                                        pdf.text("Blood Group", 30, 34 + y)
                                        pdf.text(": " + student.student_roll.student_blood_group, 50, 34 + y)
                                        pdf.text("Father's Name", 30, 37 + y)
                                        pdf.text(": " + student.student_roll.student_father_name, 50, 37 + y)
                                        pdf.text("Mother's Name", 30, 40 + y)
                                        pdf.text(": " + student.student_roll.student_mother_name, 50, 40 + y)
                                    }
                                    pdf.setFillColor(80, 15, 0, 0);
                                    pdf.setDrawColor(0, 0, 139);
                                    pdf.rect(10, 49 + y, 86, 10, 'FD')

                                    pdf.setTextColor('#000000')
                                    pdf.text("Principal", 15, 58 + y)
                                    if (sing) {
                                        pdf.addImage(sing, 'png', 15, 51 + y, 15, 4)
                                    }

                                    pdf.setTextColor('#19017F')
                                    pdf.setFontStyle('bold');
                                    pdf.text("IDENTITY CARD", 72, 56 + y)

                                    //Back Side
                                    // pdf.line(98,0,98,1100,'S')
                                    pdf.setFillColor(255, 255, 255);
                                    pdf.setDrawColor(0, 0, 139);
                                    pdf.rect(110, 5 + y, 86, 54, 'FD')
                                    pdf.text("Validity Date : " + moment(student.expire_date).format('MMM DD, YYYY'), 135, 10 + y)
                                    var splitTitle = pdf.splitTextToSize(student.back_text, 75);

                                    //QR Code
                                    let qrCodeImage = $('#qr_' + student.student_roll.student_roll + ' img').attr('src');
                                    pdf.addImage(qrCodeImage, 'png', 115, 35 + y, 20, 20);

                                    //Bangla font set
                                    pdf.addFileToVFS('kalpurush.ttf', fontKalpurush);
                                    pdf.addFont('kalpurush.ttf', 'kalpurush', 'normal');

                                    // console.log('fonts', pdf.getFontList());
                                    // pdf.setFont('kalpurush','normal');

                                    pdf.text(splitTitle, 153, 14 + y, { align: 'center' })
                                    // pdf.text("মাইক্রোসফট আফিস ট্রেনিং গাইড",153,14+y)

                                    pdf.setFont('Helvetica');
                                    pdf.text(splitTitle, 153, 14 + y, { align: 'center' })
                                    pdf.line(140, 32 + y, 190, 32 + y)
                                    if (idCard_info.address.length) {
                                        let myArray = idCard_info.address.split(";");
                                        pdf.text(myArray, 165, 36 + y, { align: 'center' })
                                    }


                                    y = row * 69
                                    row += 1
                                    if (row == 5) {
                                        y = 0
                                        row = 1
                                        pdf.addPage("a4");
                                    }

                                    if (data.length == index + 1) {
                                        setTimeout(() => {
                                            pdf.save("ID-Card-" + Date.now() + '.pdf')
                                        }, 1000);
                                    }
                                })
                            });

                        } else {
                            Swal.fire({
                                position: 'center',
                                icon: 'error',
                                title: 'There is no data in this filter .',
                                showConfirmButton: true,
                            })
                        }
                    }, 200);
                }
            })
        }, 300);
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Please Select Year and Class .',
            showConfirmButton: true,
        })
    }

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
    var academic_year = document.getElementById('id_academic_Year').value
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

$('#qrGen').on('click', function () {
    let data = generateqr("1234557456")
    console.log(data)
})

function generateqr(student_roll) {
    var qrcode = new QRCode(document.getElementById(`qr_${student_roll}`), {
        width: 128,
        height: 128,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });

    var qrdata = student_roll;
    if (qrdata) {
        qrcode.makeCode(qrdata)
    } else {

    }
}