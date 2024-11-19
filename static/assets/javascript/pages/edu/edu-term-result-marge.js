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
    let marge_tilte = $('#id_marge_tilte').val();
    let academic_year = $('#id_academic_year').val();
    let session_id = $('#id_session_id').val();
    let class_id = $('#id_class_id').val();
    let class_group_id = $('#id_class_group_id').val();
    let term_1 = $('#term_1').val();
    let term_2 = $('#term_2').val();
    let term_3 = $('#term_3');
    if (term_3) {
        term_3 = term_3.val()
    } else {
        term_3=""
    }


    if (branch_code && academic_year && class_id && term_1 && term_2) {
        let data_string = {
            branch_code: branch_code,
            academic_year: academic_year,
            session_id: session_id,
            class_id: class_id,
            class_group_id: class_group_id,
            term_1: term_1,
            term_2: term_2,
            term_3: term_3,
            marge_tilte: marge_tilte
        }
        
        $.ajax({
            url: 'edu-result-process_status_create',
            data: {},
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (data.error_message) {
                    Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: data.error_message,
                        showConfirmButton: true,
                    })
                };
                if (data.process_id) {
                    Result_process_submit(data.process_id)
                }
            }
        })
        function Result_process_submit(process_id) {
            data_string.process_id = process_id;
            $.ajax({
                url: '/edu-term-result-marge-insert',
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
        }
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
    let marge_tilte = $('#id_marge_tilte').val();
    let academic_year = $('#id_academic_year').val();
    let session_id = $('#id_session_id').val();
    let class_id = $('#id_class_id').val();
    let class_group_id = $('#id_class_group_id').val();
    let term_1 = $('#term_1').val();
    let term_2 = $('#term_2').val();
    let term_3 = $('#term_3');
    let template1 = $('#template1');
    let template2 = $('#template2');
    let template = 'template1';

    if (template2.is(':checked')) {
        template ='template2'
    }                      
    console.log(term_3)
    console.log(typeof(class_group_id))
    if (term_3) {
        term_3 = term_3.val()
    } else {
        term_3 = ""
    }
    if (branch_code && academic_year && class_id && term_1 && term_2) {

        let data_url = $('#markView').attr('data-url')
        $('#listView').prop("disabled", false);

        let url = data_url + '?branch_code=' + branch_code + '&academic_year=' + academic_year + '&term_1=' + term_1 + '&term_2=' + term_2 + '&term_3=' + term_3 + '&class_id=' + class_id + '&class_group_id=' + class_group_id + '&session_id=' + session_id + '&template=' + template
        window.open(url, "_blank");
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Branch code, Year, Class Name and Exam Term is required. ',
            showConfirmButton: true,
            //timer: 1500
        })
    }
}

$('#id_class_id').change(function () {
    class_group_filter()
})
// $('#id_class_group_id').change(function () {
//     filtering_subjectlist()
// })

function class_group_filter() {
    let class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $('#id_class_group_id').empty()
            var newOption = new Option('---------------', "", false, false);
            $('#id_class_group_id').append(newOption);
            data.forEach(element => {
                var newOption = new Option(element.class_group_name, element.class_group_id, false, false);
                $('#id_class_group_id').append(newOption).trigger('change');
            });
        }
    })
}


function MarkSheet_Download() {
    let branch_code = $('#id_branch_code').val();
    let marge_tilte = $('#id_marge_tilte').val();
    let academic_year = $('#id_academic_year').val();
    let session_id = $('#id_session_id').val();
    let class_id = $('#id_class_id').val();
    let class_group_id = $('#id_class_group_id').val();
    let term_1 = $('#term_1').val();
    let term_2 = $('#term_2').val();
    let term_3 = $('#term_3');
    if (term_3) {
        term_3 = term_3.val()
    } else {
        term_3 = ""
    }
    let template1 = $('#template1');
    let template2 = $('#template2');
    let template = 'template1';

    if (template2.is(':checked')) {
        template = 'template2'
    }
    let data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        session_id: session_id,
        class_id: class_id,
        class_group_id: class_group_id,
        term_1: term_1,
        term_2: term_2,
        term_3: term_3,

    }
    if (branch_code && academic_year && class_id && term_1 && term_2) {
        $.ajax({
            url: 'edu-result-marge-mark-sheet-data',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (template == 'template1') {
                    var pdf = new jsPDF('p', 'mm', 'a4');
                    let logo = ""
                    let download = false;
                    toDataURL(data.logo, function (dataUrl) {
                        if (isImage(dataUrl)) {
                            logo = dataUrl
                        }


                        data.results.forEach(result => {

                            pdf.setFontSize((18 * 29) / data.form_header.academic_name.length)
                            // pdf.setTextColor('#FFFFFF')
                            pdf.setFontStyle('bold');
                            pdf.text(data.form_header.academic_name.toUpperCase(), 105, 12, { align: 'center' })
                            pdf.setFontSize(10)
                            pdf.setFontStyle('normal');
                            pdf.text(data.form_header.text_one ? data.form_header.text_one : "", 105, 16, { align: 'center' })
                            pdf.text(data.form_header.text_two ? data.form_header.text_two : "", 105, 20, { align: 'center' })
                            pdf.text(data.form_header.text_three ? data.form_header.text_three : "", 105, 24, { align: 'center' })
                            pdf.text(data.form_header.text_four ? data.form_header.text_four : "", 105, 28, { align: 'center' })
                            pdf.text(data.form_header.text_five ? data.form_header.text_five : "", 105, 32, { align: 'center' })

                            //Logo
                            if (logo) {
                                pdf.addImage(logo, 'png', 95, 45, 20, 20)
                            }
                            // Header
                            pdf.setFontSize(11)
                            pdf.setFontStyle('bold')
                            pdf.text("Academic Transcript".toUpperCase(), 105, 70, 'center');
                            pdf.line(83, 71, 125, 71)
                            pdf.text(result.marge_tilte + ' - ' + result.year, 105, 75, 'center');

                            //Student Info
                            pdf.setFontSize(9)
                            pdf.setFontStyle('bold')
                            pdf.text("ID", 10, 45);
                            pdf.text(":", 40, 45);
                            pdf.setFontStyle('normal')
                            pdf.text(result.student_roll, 45, 45);

                            pdf.setFontStyle('bold')
                            pdf.text("Name", 10, 49);
                            pdf.text(":", 40, 49);
                            pdf.setFontStyle('normal')
                            pdf.text(result.student_name, 45, 49);

                            pdf.setFontStyle('bold')
                            pdf.text("Father's Name", 10, 53);
                            pdf.text(":", 40, 53);
                            pdf.setFontStyle('normal')
                            pdf.text(result.father_name, 45, 53);

                            pdf.setFontStyle('bold')
                            pdf.text("Mother's Name", 10, 57);
                            pdf.text(":", 40, 57);
                            pdf.setFontStyle('normal')
                            pdf.text(result.mother_name, 45, 57);

                            pdf.setFontStyle('bold')
                            pdf.text("Date of Birth", 10, 61);
                            pdf.text(":", 40, 61);
                            pdf.setFontStyle('normal')
                            let d = new Date(result.date_of_birth);
                            pdf.text(d.toLocaleDateString("en-US", { day: 'numeric', month: 'long', year: 'numeric' }), 45, 61);

                            pdf.setFontStyle('bold')
                            pdf.text("Class", 10, 65);
                            pdf.text(":", 40, 65);
                            pdf.setFontStyle('normal')
                            pdf.text(result.class_name, 45, 65);

                            pdf.setFontStyle('bold')
                            pdf.text("Class Roll", 10, 70);
                            pdf.text(":", 40, 70);
                            pdf.setFontStyle('normal')
                            pdf.text(result.class_roll.toString(), 45, 70);

                            if (result.class_group) {
                                pdf.setFontStyle('bold')
                                pdf.text("Group", 10, 75);
                                pdf.text(":", 40, 75);
                                pdf.setFontStyle('normal')
                                pdf.text(result.class_group, 45, 75);
                            }
                            if (result.merit_position) {
                                let ph = 75;
                                if (result.class_group) {
                                    ph = 80
                                }
                                pdf.setFontStyle('bold')
                                pdf.text("Position", 10, ph);
                                pdf.text(":", 40, ph);
                                pdf.setFontStyle('normal')
                                let leter = 'th'
                                if (result.merit_position == 1) {
                                    leter = 'st';
                                } else if (result.merit_position == 2) {
                                    leter = 'nd';
                                } else if (result.merit_position == 3) {
                                    leter = 'rd';
                                }
                                pdf.text(result.merit_position.toString() + leter, 45, ph);
                            }
                            class_name = result.class_name;

                            //Result Grate
                            gy = -4;
                            pdf.setFontSize(8)
                            pdf.line(160, 36, 200, 36)
                            pdf.line(160, 36, 160, 46)
                            pdf.line(178, 36, 178, 46)
                            pdf.line(188, 36, 188, 46)
                            pdf.line(200, 36, 200, 46)
                            pdf.text(['Class', 'Interval'], 169, 39, { align: 'center' });
                            pdf.text(['Grade', 'Point'], 183, 39, { align: 'center' });
                            pdf.text(['Latter', 'Grade'], 194, 39, { align: 'center' });
                            data.result_grades.forEach(el => {
                                pdf.line(160, gy + 50, 200, gy + 50)
                                pdf.line(160, gy + 55, 200, gy + 55)
                                pdf.line(160, gy + 50, 160, gy + 55)
                                pdf.line(200, gy + 50, 200, gy + 55)

                                pdf.text(el.highest_mark.toString().split(".")[0], 162, gy + 53,);
                                pdf.text(" - " + el.lowest_mark.toString().split(".")[0], 167, gy + 53,);
                                pdf.line(178, gy + 50, 178, gy + 55)

                                pdf.text(el.result_gpa.toString(), 180, gy + 53,);
                                pdf.line(188, gy + 50, 188, gy + 55)

                                pdf.text(el.grade_name, 190, gy + 53,);

                                gy += 5;
                            });

                            //Subject Result
                            let subjects_filter = data.subject_results.filter(r => r.student_roll == result.student_roll)
                            let Additional = subjects_filter.find(r => r.is_optional == 1)
                            if (Additional) {
                                let sub_count = 1;
                                y = 10;
                                pdf.setFontSize(9)
                                pdf.line(10, y + 75, 200, y + 75)
                                pdf.line(10, y + 85, 200, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)

                                pdf.text("SL NO", 12, y + 82,);
                                pdf.line(24, y + 75, 24, y + 85)
                                pdf.text("Name of Subject", 25, y + 82);
                                pdf.line(110, y + 75, 110, y + 85)
                                pdf.text(["Marks", "Obtained"], 118, y + 80, { align: 'center' });
                                pdf.line(128, y + 75, 128, y + 85)
                                pdf.text(["Letter", "Grade"], 134, y + 80, { align: 'center' });
                                pdf.line(142, y + 75, 142, y + 85)
                                pdf.text(["Grade", "Point"], 150, y + 80, { align: 'center' });
                                pdf.line(160, y + 75, 160, y + 85)
                                pdf.text("GPA", 168, y + 78);
                                pdf.setFontSize(6)
                                pdf.text(["Without Additional", "Subject"], 170, y + 81, { align: 'center' });
                                pdf.setFontSize(9)
                                pdf.line(180, y + 75, 180, y + 85)
                                pdf.text("GPA", 182, y + 82);


                                sub_count = 0;
                                subjects_filter.forEach(subResult => {
                                    if (subResult.student_roll == result.student_roll && subResult.is_optional == 0) {
                                        sub_count += 1;
                                        subject_one = data.subjects.filter(s => s.subject_id == subResult.subject_one_id)
                                        subject_two = data.subjects.filter(s => s.subject_id == subResult.subject_two_id)
                                        subject_three = data.subjects.filter(s => s.subject_id == subResult.subject_three_id)
                                        let subject_list = []
                                        let y_plus = 0;
                                        if (subject_one[0]) {
                                            subject_list.push(subject_one[0].subject_name);
                                        }
                                        if (subject_two[0]) {
                                            subject_list.push(subject_two[0].subject_name);
                                            y_plus += 3;
                                        }
                                        if (subject_three[0]) {
                                            subject_list.push(subject_three[0].subject_name);
                                            y_plus += 3;
                                        }
                                        pdf.text(subject_list, 25, y + 90);
                                        y += y_plus;

                                        pdf.line(200, y - y_plus + 85, 200, y + 95)
                                        pdf.text(sub_count.toString(), 12, y + 92);
                                        pdf.line(24, y - y_plus + 85, 24, y + 95)
                                        // pdf.line(110, y - y_plus + 85, 110, y + 95)
                                        let obtainMark = "0"
                                        if (subResult.obtain_marks) {
                                            let obn = Number(subResult.obtain_marks).toFixed(0)
                                            obtainMark = obn.toString()
                                        }
                                        // pdf.text(obtainMark, 118, y + 92, { align: 'center' });
                                        pdf.line(128, y - y_plus + 85, 128, y + 95)
                                        pdf.text(subResult.result_grade ? subResult.result_grade : 'F', 130, y + 92);
                                        pdf.line(142, y - y_plus + 85, 142, y + 95)
                                        pdf.text(subResult.grade_point.toString(), 145, y + 92);

                                        pdf.line(10, y + 95, 160, y + 95)
                                        pdf.line(10, y - y_plus + 85, 10, y + 95)
                                        pdf.line(160, y - y_plus + 85, 160, y + 95)
                                        pdf.line(180, y - y_plus + 85, 180, y + 95)
                                        y += 10;
                                    }
                                });
                                //Last line
                                pdf.line(10, y - 10 + 95, 180, y - 10 + 95)
                                pdf.text("Additional Subject", 12, y + 92);
                                pdf.text("GP above 2", 160, y + 92);
                                pdf.line(180, y + 85, 180, y + 95)
                                pdf.line(200, y + 85, 200, y + 95)
                                pdf.line(10, y + 95, 180, y + 95)
                                y += 10;
                                subjects_filter.forEach(subResult => {
                                    if (subResult.student_roll == result.student_roll && subResult.is_optional == 1) {
                                        sub_count += 1;
                                        subject_one = data.subjects.filter(s => s.subject_id == subResult.subject_one_id)
                                        subject_two = data.subjects.filter(s => s.subject_id == subResult.subject_two_id)
                                        subject_three = data.subjects.filter(s => s.subject_id == subResult.subject_three_id)
                                        pdf.line(10, y + 95, 160, y + 95)
                                        pdf.line(10, y + 85, 10, y + 95)
                                        pdf.line(200, y + 85, 200, y + 95)
                                        pdf.text(sub_count.toString(), 12, y + 92);
                                        pdf.line(24, y + 85, 24, y + 95)
                                        let subject_list = []
                                        let y_plus = 0;
                                        if (subject_one[0]) {
                                            subject_list.push(subject_one[0].subject_name);
                                        }
                                        if (subject_two[0]) {
                                            subject_list.push(subject_two[0].subject_name);
                                            y_plus += 3;
                                        }
                                        if (subject_three[0]) {
                                            subject_list.push(subject_three[0].subject_name);
                                            y_plus += 3;
                                        }
                                        pdf.text(subject_list, 25, y + 92);
                                        // pdf.line(110, y + 85, 110, y + 95)
                                        let obtainMark = "0"
                                        if (subResult.obtain_marks) {
                                            let obn = Number(subResult.obtain_marks).toFixed(0)
                                            obtainMark = obn.toString()
                                        }
                                        // pdf.text(obtainMark, 118, y + 92, { align: 'center' });
                                        pdf.line(128, y + 85, 128, y + 95)
                                        pdf.text(subResult.result_grade ? subResult.result_grade : 'F', 130, y + 92);
                                        pdf.line(142, y + 85, 142, y + 95)
                                        pdf.text(subResult.grade_point.toString(), 145, y + 92);
                                        pdf.line(160, y + 85, 160, y + 95)
                                        pdf.text(subResult.grade_point > 2 ? (subResult.grade_point - 2).toString() : "0", 162, y + 92);
                                        pdf.line(180, y + 85, 180, y + 95)
                                        y += 10;
                                    }
                                });
                                //Last line
                                pdf.line(10, y - 10 + 95, 200, y - 10 + 95)
                                //Final GPA
                                pdf.text(result.grade_point_without_furth.toString(), 162, (y / 2) + 82);
                                pdf.text(result.grade_point.toString(), 182, (y / 2) + 82);
                            } else {
                                let sub_count = 1;
                                y = 10;
                                pdf.setFontSize(9)
                                pdf.line(10, y + 75, 200, y + 75)
                                pdf.line(10, y + 85, 200, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)

                                pdf.text("SL", 12, y + 82,);
                                pdf.line(18, y + 75, 18, y + 85)
                                pdf.text("Name of Subject", 19, y + 82);
                                pdf.line(90, y + 75, 90, y + 85)
                                pdf.setFontSize(7)
                                pdf.text(["Total", "Obtained"], 100, y + 80, { align: 'center' });
                                pdf.line(110, y + 75, 110, y + 85)
                                pdf.text(["Total", "Obtained"], 120, y + 80, { align: 'center' });
                                pdf.line(130, y + 75, 130, y + 85)
                                pdf.setFontSize(9)
                                pdf.text(["Total", "Obtained"], 140, y + 80, { align: 'center' });
                                pdf.line(150, y + 75, 150, y + 85)
                                pdf.text(["Letter", "Grade"], 158, y + 80, { align: 'center' });
                                pdf.line(165, y + 75, 165, y + 85)
                                pdf.text(["Grade", "Point"], 170, y + 80, { align: 'center' });
                                pdf.line(180, y + 75, 180, y + 85)
                                pdf.text("GPA", 184, y + 82);


                                sub_count = 0;
                                subjects_filter.forEach(subResult => {
                                    if (subResult.student_roll == result.student_roll && subResult.is_optional == 0) {
                                        sub_count += 1;
                                        subject_one = data.subjects.filter(s => s.subject_id == subResult.subject_one_id)
                                        subject_two = data.subjects.filter(s => s.subject_id == subResult.subject_two_id)
                                        subject_three = data.subjects.filter(s => s.subject_id == subResult.subject_three_id)


                                        let subject_list = []
                                        let y_plus = 0;
                                        if (subject_one[0]) {
                                            subject_list.push(subject_one[0].subject_name);
                                        }
                                        if (subject_two[0]) {
                                            subject_list.push(subject_two[0].subject_name);
                                            y_plus += 3;
                                        }
                                        if (subject_three[0]) {
                                            subject_list.push(subject_three[0].subject_name);
                                            y_plus += 3;
                                        }
                                        
                                        y += y_plus;
                                        pdf.text(sub_count.toString(), 12, y + 92);
                                        pdf.line(18, y - y_plus + 85, 18, y + 95)
                                        pdf.text(subject_list, 19, y + 90);
                                        pdf.line(90, y - y_plus + 85, 90, y + 95)
                                        let one_obtainMark = '0';
                                        if (subResult.one_obtain_marks) {
                                            let one_obn = Number(subResult.one_obtain_marks).toFixed(0)
                                            one_obtainMark = one_obn.toString()
                                        }
                                        pdf.text(one_obtainMark, 100, y + 92, { align: 'center' });
                                        pdf.line(110, y - y_plus + 85, 110, y + 95)
                                        let two_obtainMark = '0';
                                        if (subResult.two_obtain_marks) {
                                            let two_obn = Number(subResult.two_obtain_marks).toFixed(0)
                                            two_obtainMark = two_obn.toString()
                                        }
                                        pdf.text(two_obtainMark, 120, y + 92, { align: 'center' });
                                        pdf.line(130, y - y_plus + 85, 130, y + 95)

                                        pdf.line(10, y + 95, 180, y + 95)
                                        pdf.line(10, y - y_plus + 85, 10, y + 95)
                                        pdf.line(200, y - y_plus + 85, 200, y + 95)
                                        let obtainMark = "0"
                                        if (subResult.obtain_marks) {
                                            let obn = Number(subResult.obtain_marks).toFixed(0)
                                            obtainMark = obn.toString()
                                        }
                                        
                                        pdf.text(obtainMark, 140, y + 92, { align: 'center' });
                                        pdf.line(150, y - y_plus + 85, 150, y + 95)
                                        pdf.text(subResult.result_grade ? subResult.result_grade : 'F', 156, y + 92);
                                        pdf.line(165, y - y_plus + 85, 165, y + 95)
                                        pdf.text(subResult.grade_point.toString(), 168, y + 92);
                                        pdf.line(180, y - y_plus + 85, 180, y + 95)
                                        y += 10;
                                    }
                                });
                                //Last line
                                pdf.line(10, y - 10 + 95, 200, y - 10 + 95)
                                //Final GPA
                                //pdf.text(result.point_without_optional.toString(), 162, (y / 2) + 82);
                                pdf.text(result.grade_point.toString(), 185, (y / 2) + 92);
                            }
                            //Bottom
                            pdf.text("Class Teacher", 30, y + 125);
                            pdf.text("Principal/Head Master", 150, y + 125);
                            pdf.addPage("a4");
                        });
                        pdf.save("Result-" + Date.now() + '.pdf')
                    })
                } else if (template == 'template2') {
                    var pdf = new jsPDF('p', 'mm', 'a4');
                    let logo = ""
                    let download = false;
                    toDataURL(data.logo, function (dataUrl) {
                        if (isImage(dataUrl)) {
                            logo = dataUrl
                        }


                        data.results.forEach(result => {

                            pdf.setFontSize((18 * 29) / data.form_header.academic_name.length)
                            // pdf.setTextColor('#FFFFFF')
                            pdf.setFontStyle('bold');
                            pdf.text(data.form_header.academic_name.toUpperCase(), 105, 12, { align: 'center' })
                            pdf.setFontSize(10)
                            pdf.setFontStyle('normal');
                            pdf.text(data.form_header.text_one ? data.form_header.text_one : "", 105, 16, { align: 'center' })
                            pdf.text(data.form_header.text_two ? data.form_header.text_two : "", 105, 20, { align: 'center' })
                            pdf.text(data.form_header.text_three ? data.form_header.text_three : "", 105, 24, { align: 'center' })
                            pdf.text(data.form_header.text_four ? data.form_header.text_four : "", 105, 28, { align: 'center' })
                            pdf.text(data.form_header.text_five ? data.form_header.text_five : "", 105, 32, { align: 'center' })

                            //Logo
                            if (logo) {
                                pdf.addImage(logo, 'png', 95, 45, 20, 20)
                            }
                            // Header
                            pdf.setFontSize(11)
                            pdf.setFontStyle('bold')
                            pdf.text("Academic Transcript".toUpperCase(), 105, 70, 'center');
                            pdf.line(83, 71, 125, 71)
                            pdf.text(result.marge_tilte + ' - ' + result.year, 105, 75, 'center');

                            //Student Info
                            pdf.setFontSize(9)
                            pdf.setFontStyle('bold')
                            pdf.text("ID", 10, 45);
                            pdf.text(":", 40, 45);
                            pdf.setFontStyle('normal')
                            pdf.text(result.student_roll, 45, 45);

                            pdf.setFontStyle('bold')
                            pdf.text("Name", 10, 49);
                            pdf.text(":", 40, 49);
                            pdf.setFontStyle('normal')
                            pdf.text(result.student_name, 45, 49);

                            pdf.setFontStyle('bold')
                            pdf.text("Father's Name", 10, 53);
                            pdf.text(":", 40, 53);
                            pdf.setFontStyle('normal')
                            pdf.text(result.father_name, 45, 53);

                            pdf.setFontStyle('bold')
                            pdf.text("Mother's Name", 10, 57);
                            pdf.text(":", 40, 57);
                            pdf.setFontStyle('normal')
                            pdf.text(result.mother_name, 45, 57);

                            pdf.setFontStyle('bold')
                            pdf.text("Date of Birth", 10, 61);
                            pdf.text(":", 40, 61);
                            pdf.setFontStyle('normal')
                            let d = new Date(result.date_of_birth);
                            pdf.text(d.toLocaleDateString("en-US", { day: 'numeric', month: 'long', year: 'numeric' }), 45, 61);

                            pdf.setFontStyle('bold')
                            pdf.text("Class", 10, 65);
                            pdf.text(":", 40, 65);
                            pdf.setFontStyle('normal')
                            pdf.text(result.class_name, 45, 65);

                            pdf.setFontStyle('bold')
                            pdf.text("Class Roll", 10, 70);
                            pdf.text(":", 40, 70);
                            pdf.setFontStyle('normal')
                            pdf.text(result.class_roll.toString(), 45, 70);

                            if (result.class_group) {
                                pdf.setFontStyle('bold')
                                pdf.text("Group", 10, 75);
                                pdf.text(":", 40, 75);
                                pdf.setFontStyle('normal')
                                pdf.text(result.class_group, 45, 75);
                            }
                            if (result.merit_position) {
                                let ph = 75;
                                if (result.class_group) {
                                    ph = 80
                                }
                                pdf.setFontStyle('bold')
                                pdf.text("Position", 10, ph);
                                pdf.text(":", 40, ph);
                                pdf.setFontStyle('normal')
                                let leter = 'th'
                                if (result.merit_position == 1) {
                                    leter = 'st';
                                } else if (result.merit_position == 2) {
                                    leter = 'nd';
                                } else if (result.merit_position == 3) {
                                    leter = 'rd';
                                }
                                pdf.text(result.merit_position.toString() + leter, 45, ph);
                            }
                            class_name = result.class_name;

                            //Result Grate
                            gy = -4;
                            pdf.setFontSize(8)
                            pdf.line(160, 36, 200, 36)
                            pdf.line(160, 36, 160, 46)
                            pdf.line(178, 36, 178, 46)
                            pdf.line(188, 36, 188, 46)
                            pdf.line(200, 36, 200, 46)
                            pdf.text(['Class', 'Interval'], 169, 39, { align: 'center' });
                            pdf.text(['Grade', 'Point'], 183, 39, { align: 'center' });
                            pdf.text(['Latter', 'Grade'], 194, 39, { align: 'center' });
                            data.result_grades.forEach(el => {
                                pdf.line(160, gy + 50, 200, gy + 50)
                                pdf.line(160, gy + 55, 200, gy + 55)
                                pdf.line(160, gy + 50, 160, gy + 55)
                                pdf.line(200, gy + 50, 200, gy + 55)

                                pdf.text(el.highest_mark.toString().split(".")[0], 162, gy + 53,);
                                pdf.text(" - " + el.lowest_mark.toString().split(".")[0], 167, gy + 53,);
                                pdf.line(178, gy + 50, 178, gy + 55)

                                pdf.text(el.result_gpa.toString(), 180, gy + 53,);
                                pdf.line(188, gy + 50, 188, gy + 55)

                                pdf.text(el.grade_name, 190, gy + 53,);

                                gy += 5;
                            });

                            //Subject Result
                            let subjects_filter = data.subject_results.filter(r => r.student_roll == result.student_roll)
                            let Additional = subjects_filter.find(r => r.is_optional == 1)
                            if (Additional) {
                                let sub_count = 1;
                                y = 10;
                                pdf.setFontSize(9)
                                pdf.line(10, y + 75, 200, y + 75)
                                pdf.line(10, y + 85, 200, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)

                                pdf.text("SL NO", 12, y + 82,);
                                pdf.line(24, y + 75, 24, y + 85)
                                pdf.text("Name of Subject", 25, y + 82);
                                // pdf.line(110, y + 75, 110, y + 85)
                                // pdf.text(["Marks", "Obtained"], 118, y + 80, { align: 'center' });
                                pdf.line(128, y + 75, 128, y + 85)
                                pdf.text(["Letter", "Grade"], 134, y + 80, { align: 'center' });
                                pdf.line(142, y + 75, 142, y + 85)
                                pdf.text(["Grade", "Point"], 150, y + 80, { align: 'center' });
                                pdf.line(160, y + 75, 160, y + 85)
                                pdf.text("GPA", 168, y + 78);
                                pdf.setFontSize(6)
                                pdf.text(["Without Additional", "Subject"], 170, y + 81, { align: 'center' });
                                pdf.setFontSize(9)
                                pdf.line(180, y + 75, 180, y + 85)
                                pdf.text("GPA", 182, y + 82);


                                sub_count = 0;
                                subjects_filter.forEach(subResult => {
                                    if (subResult.student_roll == result.student_roll && subResult.is_optional == 0) {
                                        sub_count += 1;
                                        subject_one = data.subjects.filter(s => s.subject_id == subResult.subject_one_id)
                                        subject_two = data.subjects.filter(s => s.subject_id == subResult.subject_two_id)
                                        subject_three = data.subjects.filter(s => s.subject_id == subResult.subject_three_id)
                                        let subject_list = []
                                        let y_plus = 0;
                                        if (subject_one[0]) {
                                            subject_list.push(subject_one[0].subject_name);
                                        }
                                        if (subject_two[0]) {
                                            subject_list.push(subject_two[0].subject_name);
                                            y_plus += 3;
                                        }
                                        if (subject_three[0]) {
                                            subject_list.push(subject_three[0].subject_name);
                                            y_plus += 3;
                                        }
                                        pdf.text(subject_list, 25, y + 90);
                                        y += y_plus;

                                        pdf.line(200, y - y_plus + 85, 200, y + 95)
                                        pdf.text(sub_count.toString(), 12, y + 92);
                                        pdf.line(24, y - y_plus + 85, 24, y + 95)
                                        // pdf.line(110, y - y_plus + 85, 110, y + 95)
                                        let obtainMark = "0"
                                        if (subResult.obtain_marks) {
                                            let obn = Number(subResult.obtain_marks).toFixed(0)
                                            obtainMark = obn.toString()
                                        }
                                        // pdf.text(obtainMark, 118, y + 92, { align: 'center' });
                                        pdf.line(128, y - y_plus + 85, 128, y + 95)
                                        pdf.text(subResult.result_grade ? subResult.result_grade : 'F', 130, y + 92);
                                        pdf.line(142, y - y_plus + 85, 142, y + 95)
                                        pdf.text(subResult.grade_point.toString(), 145, y + 92);

                                        pdf.line(10, y + 95, 160, y + 95)
                                        pdf.line(10, y - y_plus + 85, 10, y + 95)
                                        pdf.line(160, y - y_plus + 85, 160, y + 95)
                                        pdf.line(180, y - y_plus + 85, 180, y + 95)
                                        y += 10;
                                    }
                                });
                                //Last line
                                pdf.line(10, y - 10 + 95, 180, y - 10 + 95)
                                pdf.text("Additional Subject", 12, y + 92);
                                pdf.text("GP above 2", 160, y + 92);
                                pdf.line(180, y + 85, 180, y + 95)
                                pdf.line(200, y + 85, 200, y + 95)
                                pdf.line(10, y + 95, 180, y + 95)
                                y += 10;
                                subjects_filter.forEach(subResult => {
                                    if (subResult.student_roll == result.student_roll && subResult.is_optional == 1) {
                                        sub_count += 1;
                                        subject_one = data.subjects.filter(s => s.subject_id == subResult.subject_one_id)
                                        subject_two = data.subjects.filter(s => s.subject_id == subResult.subject_two_id)
                                        subject_three = data.subjects.filter(s => s.subject_id == subResult.subject_three_id)
                                        pdf.line(10, y + 95, 160, y + 95)
                                        pdf.line(10, y + 85, 10, y + 95)
                                        pdf.line(200, y + 85, 200, y + 95)
                                        pdf.text(sub_count.toString(), 12, y + 92);
                                        pdf.line(24, y + 85, 24, y + 95)
                                        let subject_list = []
                                        let y_plus = 0;
                                        if (subject_one[0]) {
                                            subject_list.push(subject_one[0].subject_name);
                                        }
                                        if (subject_two[0]) {
                                            subject_list.push(subject_two[0].subject_name);
                                            y_plus += 3;
                                        }
                                        if (subject_three[0]) {
                                            subject_list.push(subject_three[0].subject_name);
                                            y_plus += 3;
                                        }
                                        pdf.text(subject_list, 25, y + 92);
                                        // pdf.line(110, y + 85, 110, y + 95)
                                        let obtainMark = "0"
                                        if (subResult.obtain_marks) {
                                            let obn = Number(subResult.obtain_marks).toFixed(0)
                                            obtainMark = obn.toString()
                                        }
                                        // pdf.text(obtainMark, 118, y + 92, { align: 'center' });
                                        pdf.line(128, y + 85, 128, y + 95)
                                        pdf.text(subResult.result_grade ? subResult.result_grade : 'F', 130, y + 92);
                                        pdf.line(142, y + 85, 142, y + 95)
                                        pdf.text(subResult.grade_point.toString(), 145, y + 92);
                                        pdf.line(160, y + 85, 160, y + 95)
                                        pdf.text(subResult.grade_point > 2 ? (subResult.grade_point - 2).toString() : "0", 162, y + 92);
                                        pdf.line(180, y + 85, 180, y + 95)
                                        y += 10;
                                    }
                                });
                                //Last line
                                pdf.line(10, y - 10 + 95, 200, y - 10 + 95)
                                //Final GPA
                                pdf.text(result.grade_point_without_furth.toString(), 162, (y / 2) + 82);
                                pdf.text(result.grade_point.toString(), 182, (y / 2) + 82);
                            } else {
                                let sub_count = 1;
                                y = 10;
                                pdf.setFontSize(9)
                                pdf.line(10, y + 75, 200, y + 75)
                                pdf.line(10, y + 85, 200, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)

                                pdf.text("SL NO", 12, y + 82,);
                                pdf.line(24, y + 75, 24, y + 85)
                                pdf.text("Name of Subject", 25, y + 82);
                                // pdf.line(130, y + 75, 130, y + 85)
                                // pdf.text(["Marks", "Obtained"], 140, y + 80, { align: 'center' });
                                pdf.line(150, y + 75, 150, y + 85)
                                pdf.text(["Letter", "Grade"], 158, y + 80, { align: 'center' });
                                pdf.line(165, y + 75, 165, y + 85)
                                pdf.text(["Grade", "Point"], 170, y + 80, { align: 'center' });
                                pdf.line(180, y + 75, 180, y + 85)
                                pdf.text("GPA", 184, y + 82);


                                sub_count = 0;
                                subjects_filter.forEach(subResult => {
                                    if (subResult.student_roll == result.student_roll && subResult.is_optional == 0) {
                                        sub_count += 1;
                                        subject_one = data.subjects.filter(s => s.subject_id == subResult.subject_one_id)
                                        subject_two = data.subjects.filter(s => s.subject_id == subResult.subject_two_id)
                                        subject_three = data.subjects.filter(s => s.subject_id == subResult.subject_three_id)


                                        let subject_list = []
                                        let y_plus = 0;
                                        if (subject_one[0]) {
                                            subject_list.push(subject_one[0].subject_name);
                                        }
                                        if (subject_two[0]) {
                                            subject_list.push(subject_two[0].subject_name);
                                            y_plus += 3;
                                        }
                                        if (subject_three[0]) {
                                            subject_list.push(subject_three[0].subject_name);
                                            y_plus += 3;
                                        }
                                        console.log(subject_list)
                                        pdf.text(subject_list, 25, y + 90);
                                        y += y_plus;
                                        pdf.line(10, y + 95, 180, y + 95)
                                        pdf.line(10, y - y_plus + 85, 10, y + 95)
                                        pdf.line(200, y - y_plus + 85, 200, y + 95)
                                        pdf.text(sub_count.toString(), 12, y + 92);
                                        pdf.line(24, y - y_plus + 85, 24, y + 95)
                                        // pdf.line(130, y - y_plus + 85, 130, y + 95)
                                        let obtainMark = "0"
                                        if (subResult.obtain_marks) {
                                            let obn = Number(subResult.obtain_marks).toFixed(0)
                                            obtainMark = obn.toString()
                                        }
                                        // pdf.text(obtainMark, 140, y + 92, { align: 'center' });
                                        pdf.line(150, y - y_plus + 85, 150, y + 95)
                                        pdf.text(subResult.result_grade ? subResult.result_grade : 'F', 156, y + 92);
                                        pdf.line(165, y - y_plus + 85, 165, y + 95)
                                        pdf.text(subResult.grade_point.toString(), 168, y + 92);
                                        pdf.line(180, y - y_plus + 85, 180, y + 95)
                                        y += 10;
                                    }
                                });
                                //Last line
                                pdf.line(10, y - 10 + 95, 200, y - 10 + 95)
                                //Final GPA
                                //pdf.text(result.point_without_optional.toString(), 162, (y / 2) + 82);
                                pdf.text(result.grade_point.toString(), 185, (y / 2) + 92);
                            }
                            //Bottom
                            pdf.text("Class Teacher", 30, y + 125);
                            pdf.text("Principal/Head Master", 150, y + 125);
                            pdf.addPage("a4");
                        });
                        pdf.save("Result-" + Date.now() + '.pdf')
                    })
                }
            }
        })

    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Branch code, Year, Class Name and Exam Term is required. ',
            showConfirmButton: true,
            //timer: 1500
        })
    }
}

function Mark_Summary() {
    let branch_code = $('#id_branch_code').val();
    let academic_year = $('#id_academic_year').val();
    let session_id = $('#id_session_id').val();
    let class_id = $('#id_class_id').val();
    let class_group_id = $('#id_class_group_id').val();
    let term_1 = $('#term_1').val();
    let term_2 = $('#term_2').val();
    let term_3 = $('#term_3');
    let template1 = $('#template1');
    let template2 = $('#template2');
    let template = 'template1';

    if (template2.is(':checked')) {
        template = 'template2'
    }
    console.log(term_3)
    console.log(typeof (class_group_id))
    if (term_3) {
        term_3 = term_3.val()
    } else {
        term_3 = ""
    }
    if (branch_code && academic_year && class_id && term_1 && term_2) {
        let data_url = $('#MarkSummary').attr('data-url')

        let url = data_url + '?branch_code=' + branch_code + '&academic_year=' + academic_year + '&term_1=' + term_1 + '&term_2=' + term_2 + '&term_3=' + term_3 + '&class_id=' + class_id + '&class_group_id=' + class_group_id + '&session_id=' + session_id + '&template=' + template
        window.open(url, "_blank");
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Branch code, Year, Class Name and Exam Term is required. ',
            showConfirmButton: true,
            //timer: 1500
        })
    }
}
function Mark_Summary_Total() {
    let branch_code = $('#id_branch_code').val();
    let academic_year = $('#id_academic_year').val();
    let marge_tilte = $('#id_marge_tilte').val();
    let session_id = $('#id_session_id').val();
    let term_1 = $('#term_1').val();
    let term_2 = $('#term_2').val();
    let term_3 = $('#term_3');
    if (term_3) {
        term_3 = term_3.val()
    } else {
        term_3 = ""
    }
    if (branch_code && academic_year && term_1 && term_2) {
        let data_url = $('#MarkSummaryTotal').attr('data-url')

        let url = data_url + '?branch_code=' + branch_code + '&academic_year=' + academic_year + '&term_1=' + term_1 + '&term_2=' + term_2 + '&term_3=' + term_3 + '&session_id=' + session_id + '&marge_tilte=' + marge_tilte
        window.open(url, "_blank");
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Branch code, Year, Class Name and Exam Term is required. ',
            showConfirmButton: true,
            //timer: 1500
        })
    }
}
// function filtering_subjectlist() {
//     let class_id = document.getElementById('id_class_id').value
//     let class_group_id = document.getElementById('id_class_group_id').value

//     $.ajax({
//         url: "apiedu-sublist-api/?class_id=" + class_id + "&class_group_id=" + class_group_id,
//         type: 'get',
//         datatype: 'json',
//         success: function (data) {
//             $("#id_subject_one_id option").remove();
//             $("#id_subject_two_id option").remove();
//             $("#id_subject_one_id").append('<option value="">------------</option>');
//             $("#id_subject_two_id").append('<option value="">------------</option>');
//             data.forEach(element => {
//                 $("#id_subject_one_id").append('<option value="' + element.subject_id + '">' + element.subject_name + '</option>');
//                 $("#id_subject_two_id").append('<option value="' + element.subject_id + '">' + element.subject_name + '</option>');
//             });
//         }
//     })
// }

// term_list = []
// $(document).ready(function () {
//     let terms = $('#term_1 option')
//     term_list = terms
//     document.getElementById("term_2").setAttribute("disabled", "disabled");
// });


// $('#term_1').change(function () {
//     term_list_manage()
// })

// $('#term_2').change(function () {

// })

// function term_list_manage() {
//     let term_one = $('#term_1').val()
//     if (term_one) {
//         document.getElementById("term_2").removeAttribute("disabled");
//         remove_A_option("term_2", term_one)
//     } else {
//         document.getElementById("term_2").setAttribute("disabled", "disabled");
//         set_allOptions('term_2')
//     }
// }

// function set_allOptions() {
//     let term_one = $('#term_1 option')
//     var theSelect_1 = document.getElementById('term_1');
//     var theSelect_2 = document.getElementById('term_2');
//     function item_check_term_one(item_value) {
//         for (let i = 0; i < term_one.length; i++) {
//             const value = term_one[i].value;
//             if (item_value == value) {
//                 return true;
//             }

//         }
//     }
//     for (let index = 0; index < term_list.length; index++) {
//         const element = term_list[index];
//         let check = item_check(element.value)
//         if (!check) {
//             theSelect.appendChild(element);
//         }
//     }
// }
// function remove_A_option(selet_id, value) {
//     set_allOptions()
//     setTimeout(() => {
//         let terms = $('#' + selet_id + ' option')
//         var theSelect = document.getElementById(selet_id);
//         for (let index = 0; index < terms.length; index++) {
//             let c_val = terms[index].value
//             if (c_val == value) {
//                 theSelect.removeChild(terms[index]);
//             }
//         }

//     }, 200);

// }


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