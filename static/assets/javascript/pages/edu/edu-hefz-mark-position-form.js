
$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
    $('select').select2();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$('#id_academic_year').change(function () {   
})
$('#id_term_id').change(function () {  
})


// loder_Spinner(false)



//edu-hefz-mark-process


function result_process() {
    let branch_code = $('#id_branch_code').val();
    let academic_year = $('#id_academic_year').val();
    let class_name = $('#id_class_id').val();
    let term_id = $('#id_term_id').val();
    if (branch_code && academic_year && class_name && term_id) {
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
    }
    else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Branch code, Year, Class Name and Exam Term is required. ',
            showConfirmButton: true,
            //timer: 1500
        })
    }

}

function Result_process_submit(process_id) {
    var branch_code = document.getElementById('id_branch_code').value
    var academic_year = document.getElementById('id_academic_year').value
    var term_id = document.getElementById('id_term_id').value
    var class_name = document.getElementById('id_class_id').value
    var subject_element = document.querySelectorAll('.subject_name')
    var subjects_list = []
    subject_element.forEach(element => {
        if (element.checked) {
            console.log(element.checked)
            priority = document.getElementById('subp_' + element.value).value
            console.log(element.value)
            subjects_list.push({ 'subject': element.value, 'priority': priority })
        }
    });
    subjects_list.sort((a, b) => parseFloat(a.priority) - parseFloat(b.priority));

   let subjects = []
    subjects_list.forEach(sub => {
        subjects.push(JSON.stringify(sub))
    });
    console.log(subjects)
    data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        term_id: term_id,
        class_name: class_name,
        process_id: process_id,
        subjects: subjects,
    }
    if (branch_code && academic_year && class_name && term_id) {
        $.ajax({
            url: 'edu-hefz-mark-position-process',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (data.success_message) {
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: true,
                        //                    timer: 1500
                    })
                    
                };
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
//edu-hefz-mark-final-data
function result_view() {
    var branch_code = document.getElementById('id_branch_code').value
    var academic_year = document.getElementById('id_academic_year').value
    var term_id = document.getElementById('id_term_id').value
    var class_name = document.getElementById('id_class_id').value
    var template = 1
    if ($('#template1').is(':checked')) {
        template=1
    }
    if ($('#template2').is(':checked')) {
        template = 2
    }

    data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        term_id: term_id,
        class_name: class_name,
    }
    if (branch_code && academic_year && class_name && term_id) {
        let data_url = $('#resultView').attr('data-url')
        if (academic_year && term_id && class_name) {
            $('#listView').prop("disabled", false);
        }
        let url = data_url + '?branch_code=' + branch_code + '&academic_year=' + academic_year + '&term_id=' + term_id + '&class_name=' + class_name + '&template=' + template
        window.open(url, "_blank");
    }
    else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Branch code, Year, Class Name and Exam Term is required. ',
            showConfirmButton: true,
            //timer: 1500
        })
    }

}

function MarkSheet_download() {
    var branch_code = document.getElementById('id_branch_code').value
    var academic_year = document.getElementById('id_academic_year').value
    var term_id = document.getElementById('id_term_id').value
    var class_name = document.getElementById('id_class_id').value

    data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        term_id: term_id,
        class_name: class_name
    }
    if (branch_code && academic_year && class_name && term_id) {
        $.ajax({
            url: 'edu-hefz-marksheet-data',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                console.log(data)
                var pdf = new jsPDF('p', 'mm', 'a4');
                let logo = ""
                let download = false;
                toDataURL(data.logo, function (dataUrl) {
                    if (isImage(dataUrl)) {
                        logo = dataUrl
                    }
                    let count=0
                    data.final_results.forEach(result => {
                        let profile=""
                        toDataURL("/media/" + result.img, function (dataUrl) {
                            if (isImage(dataUrl)) {
                                profile = dataUrl
                            }
                            pdf.setFontSize((18 * 29) / data.form_header.academic_name ? data.form_header.academic_name.length : 20)
                            // pdf.setTextColor('#FFFFFF')
                            pdf.setFontStyle('bold');
                            pdf.setTextColor(0, 125, 96);
                            pdf.text(data.form_header.academic_name.toUpperCase(), 105, 12, { align: 'center' })
                            pdf.setFontSize(10)
                            pdf.setTextColor(0, 0, 0);
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
                            //Profile Image
                            if (profile) {
                                pdf.addImage(profile, 'png', 15, 20, 20, 20)
                            }
                            // Header
                            pdf.setFontSize(11)
                            pdf.setTextColor(58, 3, 97);
                            pdf.setFontStyle('bold')
                            pdf.text("Academic Transcript".toUpperCase(), 105, 70, 'center');
                            pdf.line(83, 71, 127, 71)
                            pdf.setTextColor(0, 125, 96);
                            pdf.text(result.term_id__term_name + ' - ' + result.academic_year, 105, 75, 'center');
                            
                            //Student Info
                            pdf.setFontSize(9)
                            pdf.setTextColor(0, 0, 0);
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
                            pdf.text(result.class_roll ? result.class_roll.toString() : "", 45, 70);

                       
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
                            let sub_count = 1;
                            let header_print = true
                            y = 10;
                            pdf.setFontSize(9)
                            function table_header1(y) {
                                pdf.line(10, y + 75, 200, y + 75)
                                pdf.line(10, y + 85, 200, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)

                                pdf.text("SL NO", 12, y + 82,);
                                pdf.line(24, y + 75, 24, y + 85)
                                pdf.text("Name of Subject", 25, y + 82);
                                pdf.line(130, y + 75, 130, y + 85)
                                pdf.text(["Marks", "Obtained"], 140, y + 80, { align: 'center' });
                                pdf.line(150, y + 75, 150, y + 85)
                                pdf.text(["Letter", "Grade"], 158, y + 80, { align: 'center' });
                                pdf.line(165, y + 75, 165, y + 85)
                                pdf.text(["Grade", "Point"], 170, y + 80, { align: 'center' });
                                pdf.line(180, y + 75, 180, y + 85)
                                pdf.text("GPA", 184, y + 82);
                            }
                            //Subject Result
                            subject_results = data.subject_results.filter(sr =>
                                sr.student_roll == result.student_roll
                            )
                            let total_point = 0
                            let total_section = 0
                            for (let index = 0; index < subject_results.length; index++) {
                                const sub = subject_results[index];
                                let ngs_subject = data.none_group_subjects.find(ngs => ngs == sub.subject_name)
                                if (ngs_subject) {
                                    continue
                                }
                                if (header_print) {
                                    table_header1(y)
                                    header_print = false
                                }
                                total_section = 1
                                y += 10;
                                pdf.line(10, y + 75, 165, y + 75)
                                pdf.line(10, y + 85, 165, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)
                                pdf.text(sub_count.toString(), 12, y + 82,);
                                pdf.line(24, y + 75, 24, y + 85)
                                pdf.text(sub.subject_name ? sub.subject_name : "", 25, y + 82);
                                pdf.line(130, y + 75, 130, y + 85)
                                pdf.text(sub.obtain_marks ? sub.obtain_marks.toString() : "", 140, y + 80, { align: 'center' });
                                pdf.line(150, y + 75, 150, y + 85)
                                pdf.text(sub.result_grade ? sub.result_grade : "", 158, y + 80, { align: 'center' });
                                pdf.line(165, y + 75, 165, y + 85)
                                pdf.text(sub.grade_point_average ? sub.grade_point_average : "", 170, y + 80, { align: 'center' });
                                total_point += sub.grade_point_average ? Number(sub.grade_point_average) : 0
                                pdf.line(180, y + 75, 180, y + 85)
                                // pdf.text("GPA", 184, y + 82);
                                sub_count += 1
                        
                            }
                        
                            //Total
                            if (total_section == 1) {
                                y += 10
                                pdf.line(10, y + 75, 200, y + 75)
                                pdf.line(10, y + 85, 200, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)
                                pdf.text("Total", 15, y + 80);
                                pdf.text(result.obtain_marks ? result.obtain_marks.toString() : "", 140, y + 80, { align: 'center' });
                                pdf.text(total_point.toString(), 170, y + 80, { align: 'center' });
                                pdf.text(result.grade_point_average ? result.grade_point_average.toString() : "", 184, (y + 82) - ((sub_count / 2) * 10));
                            }
                            //Arabic Result
                            if (data.none_group_subjects.length) {
                                sub_count = 1;
                                y += 20;
                                pdf.setFontSize(12)
                                pdf.setFontStyle('bold')
                                pdf.text("Arabic Subjects", 12, y + 82,);
                                y += 10
                                pdf.setFontSize(9)
                                pdf.setFontStyle('normal')
                                pdf.line(10, y + 75, 200, y + 75)
                                pdf.line(10, y + 85, 200, y + 85)
                                pdf.line(10, y + 75, 10, y + 85)
                                pdf.line(200, y + 75, 200, y + 85)

                                pdf.text("SL NO", 12, y + 82,);
                                pdf.line(24, y + 75, 24, y + 85)
                                pdf.text("Name of Subject", 25, y + 82);
                                pdf.line(130, y + 75, 130, y + 85)
                                pdf.text(["Marks", "Obtained"], 140, y + 80, { align: 'center' });
                                pdf.line(150, y + 75, 150, y + 85)
                                pdf.text(["Letter", "Grade"], 158, y + 80, { align: 'center' });
                                pdf.line(165, y + 75, 165, y + 85)
                                pdf.text("Grade Point", 185, y + 80, { align: 'center' });
                                // pdf.line(180, y + 75, 180, y + 85)
                                // pdf.text("GPA", 184, y + 82);

                                for (let index = 0; index < subject_results.length; index++) {
                                    const sub = subject_results[index];
                                    let ngs_subject = data.none_group_subjects.find(ngs => ngs == sub.subject_name)
                                    if (ngs_subject) {
                                        total_section = 1
                                        y += 10;
                                        pdf.line(10, y + 75, 200, y + 75)
                                        pdf.line(10, y + 85, 200, y + 85)
                                        pdf.line(10, y + 75, 10, y + 85)
                                        pdf.line(200, y + 75, 200, y + 85)
                                        pdf.text(sub_count.toString(), 12, y + 82,);
                                        pdf.line(24, y + 75, 24, y + 85)
                                        pdf.text(sub.subject_name ? sub.subject_name : "", 25, y + 82);
                                        pdf.line(130, y + 75, 130, y + 85)
                                        pdf.text(sub.obtain_marks ? sub.obtain_marks.toString() : "", 140, y + 80, { align: 'center' });
                                        pdf.line(150, y + 75, 150, y + 85)
                                        pdf.text(sub.result_grade ? sub.result_grade : "", 158, y + 80, { align: 'center' });
                                        pdf.line(165, y + 75, 165, y + 85)
                                        pdf.text(sub.grade_point_average ? sub.grade_point_average : "", 185, y + 80, { align: 'center' });
                                        // pdf.line(180, y + 75, 180, y + 85)
                                        // pdf.text("GPA", 184, y + 82);
                                        sub_count += 1
                                    }
                            
                                }
                            }
                            //Bottom
                            pdf.text("Class Teacher", 30, y + 125);
                            pdf.text("Principal/Head Master", 150, y + 125);
                            pdf.addPage("a4");
                            count += 1;
                            if (data.final_results.length == count) {
                                pdf.save("Result-" + Date.now() + '.pdf')
                            }
                        })
                    });
                    
                })
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