$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const branch_code = urlParams.get('branch_code')
    const academic_year = urlParams.get('academic_year')
    const term_id = urlParams.get('term_id')
    const class_name = urlParams.get('class_name')
    const template = urlParams.get('template')
    
    let data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        class_name: class_name,
        term_id: term_id,
        csrfmiddlewaretoken: csrftoken

    }
    if (branch_code && academic_year && class_name && term_id) {
        $.ajax({
            url: 'edu-hefz-mark-final-data',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                console.log(data)
                if (template == 1) {
                    let row = `<tr>
                <th>LS</th>
				<th>Student Name</th>
				<th>ID</th>
				<th>Roll</th>
				<th>Total</th>
				<th>Obtain</th>
				<th>GPA</th>
				<th>LG</th>
				<th>Position</th>
                </tr>
                `
                    count = 0;
                    data.final_results.forEach(result => {
                        count += 1
                        row += `<tr><td>${count}</td>`
                        row += `<td>${result.student_roll__student_name}</td>`
                        row += `<td>${result.student_roll}</td>`
                        row += `<td>${result.student_roll__class_roll}</td>`
                        row += `<td>${result.total_exam_marks}</td>`
                        row += `<td>${result.obtain_marks}</td>`
                        row += `<td>${result.grade_point_average}</td>`
                        row += `<td>${result.result_grade}</td>`
                        row += `<td>${result.merit_position}</td>`
                        row += `</tr>`
                    });
                    $('#result_table').append(row)
                } else if (template == 2) {
                    let row = `<tr>
                <th>LS</th>
				<th>Student Name</th>
				<th>ID</th>
				<th>Roll</th>`
                data.subject_names.forEach(sub => {
                    row+=`<th>${sub}</th>`
                });
				row+=`<th>Total</th>
				<th>Obtain</th>
				<th>GPA</th>
				<th>LG</th>
				<th>Position</th>
                </tr>
                `
                    count = 0;
                    data.final_results.forEach(result => {
                        count += 1
                        row += `<tr><td>${count}</td>`
                        row += `<td>${result.student_roll__student_name}</td>`
                        row += `<td>${result.student_roll}</td>`
                        row += `<td>${result.student_roll__class_roll}</td>`
                        data.subject_names.forEach(sub => {
                            std_result = data.subject_results.find(sr =>
                                sr.subject_id__subject_name == sub && sr.student_roll == result.student_roll)
                            row += `<td>${std_result ? std_result.obtain_marks:0}</td>`
                        });
                        row += `<td>${result.total_exam_marks}</td>`
                        row += `<td>${result.obtain_marks}</td>`
                        row += `<td>${result.grade_point_average}</td>`
                        row += `<td>${result.result_grade}</td>`
                        row += `<td>${result.merit_position}</td>`
                        row += `</tr>`
                    });
                    $('#result_table').append(row)
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
});

