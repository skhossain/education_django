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
    const class_id = urlParams.get('class_id')
    const class_group_id = urlParams.get('class_group_id')
    const session_id = urlParams.get('session_id')
    const term_1 = urlParams.get('term_1')
    const term_2 = urlParams.get('term_2')
    const term_3 = urlParams.get('term_3')
    const template = urlParams.get('template')
    let data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        session_id: session_id,
        class_id: class_id,
        class_group_id: class_group_id,
        term_1: term_1,
        term_2: term_2,
        term_3: term_3,
        csrfmiddlewaretoken: csrftoken

    }
    if (branch_code && academic_year && class_id && term_1 && term_2) {
        $.ajax({
            url: 'edu-result-marge-mark-sheet-data',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (template == 'template1') {
                    let row = `<tr>
                    <th>LS</th>
                    <th>Student Name & ID</th>
                    <th>Roll</th>
                    `
                    data.result_view_setting.forEach(rvs => {
                        let sub_one = data.subjects.find(s => s.subject_id == rvs.subject_one_id_id)
                        let sub_two = data.subjects.find(s => s.subject_id == rvs.subject_two_id_id)
                        let sub_three = data.subjects.find(s => s.subject_id == rvs.subject_three_id_id)

                        row += `<th class="text-center" style="padding:2px">
                    ${sub_one.sort_name} ${sub_two ? ' - ' + sub_two.sort_name : ""} ${sub_three ? ' - ' + sub_three.sort_name : ""}
                    <table style="width:100%; border-left:0px !important;border-right:0px !important;border-bottom:0px !important">
										<tr>
											<th style="padding:2px;border:0px !important; width:30px; background:#ccc">OB</th>
											<th style="padding:2px;border:0px !important; width:35px">GPA</th>
											<th style="padding:2px;border:0px !important; width:30px">LG</th>
										</tr>
									</table>
                    </th>
                    `
                    });
                    row += `<th class="text-center">GPA</th>
						<th class="text-center">Grade</th>
						<th class="text-center">Position</th>
                        </tr>`
                    data.results.forEach((result, index) => {
                        row += `<tr>
                    <td class="text-center" >${index + 1}</td>
                    <td style="padding:2px;">${result.student_name}<br>${result.student_roll}</td>
                    <td class="text-center">${result.class_roll}</td>`

                        data.result_view_setting.forEach(rvs => {
                            let sub_result = data.subject_results.find(r => r.one_result_view_id == rvs.result_view_id && r.student_roll == result.student_roll)
                            let obMark = ""
                            if (sub_result) {
                                obMark = Number(sub_result.obtain_marks).toFixed(0).toString()

                            }
                            row += `<td>
                            <table style="width:100%; border:0px !important;">
                                <tr>
                                    <th style="padding:2px;border:0px !important; width:30px;background:#e6FFe6" >${obMark}</th>
                                    <th style="padding:2px;border:0px !important; width:35px;">${sub_result ? sub_result.grade_point : ""}</th>
                                    <th style="padding:2px;border:0px !important; width:30px;">${sub_result ? sub_result.result_grade : ""}</th>
                                </tr>
                            </table>
                        </td>`
                        });
                        let Additional_line = ""
                        let Additional = data.subject_results.filter(r => r.student_roll == result.student_roll)
                        for (let index = 0; index < Additional.length; index++) {
                            const element = Additional[index];
                            if (element.is_optional) {
                                Additional_line = `<br><span style="font-size:8px">Without Additional Subject = ${result.grade_point_without_furth}</span>`;
                                break;
                            }

                        }

                        row += `<td style="padding:2px">${result.grade_point} ${Additional_line}</td>
								<td class="text-center">${result.result_grade}</td>
								<td class="text-center">${result.merit_position}</td></tr>`


                    });

                    $('#result_table').append(row)
                } else if (template == 'template2') {
                    let row = `<tr>
                    <th>LS</th>
                    <th>Student Name & ID</th>
                    <th>Roll</th>
                    <th>Terms</th>
                    `
                    data.result_view_setting.forEach(rvs => {
                        let sub_one = data.subjects.find(s => s.subject_id == rvs.subject_one_id_id)
                        let sub_two = data.subjects.find(s => s.subject_id == rvs.subject_two_id_id)
                        let sub_three = data.subjects.find(s => s.subject_id == rvs.subject_three_id_id)

                        row += `<th class="text-center" style="padding:2px">
                    ${sub_one.sort_name} ${sub_two ? ' - ' + sub_two.sort_name : ""} ${sub_three ? ' - ' + sub_three.sort_name : ""}
                    <table style="width:100%; border-left:0px !important;border-right:0px !important;border-bottom:0px !important">
										<tr>
											<th style="padding:2px;border:0px !important; width:30px; background:#ccc">OB</th>
											<th style="padding:2px;border:0px !important; width:35px">GPA</th>
											<th style="padding:2px;border:0px !important; width:30px">LG</th>
										</tr>
									</table>
                    </th>
                    `
                    });
                    row += `<th class="text-center">GPA</th>
						<th class="text-center">Grade</th>
						<th class="text-center">Position</th>
                        </tr>`
                    
                    data.results.forEach((result, index) => {   
                        let term_1_row = `<tr>
                        <td class="text-center">${result.one_term_name}</td>`
                        let term_2_row = `<tr>
                        <td class="text-center">${result.two_term_name}</td>`
                        let term_3_row = ''
                        let final_row = `<tr class="final-row">
                        <td class="text-center" rowspan="3">${index + 1}</td>
                        <td style="padding:2px;" rowspan="3">${result.student_name}<br>${result.student_roll}</td>
                        <td class="text-center" rowspan="3">${result.class_roll}</td>
                        <td class="text-center">${result.marge_tilte}</td>`

                        
                       
                        data.result_view_setting.forEach(rvs => {
                            let sub_result = data.subject_results.find(r => r.one_result_view_id == rvs.result_view_id && r.student_roll == result.student_roll)
                            let oneObMark = ""
                            let twoObMark = ""
                            let threeObMark = ""
                            let ObMark = ""
                            if (sub_result) {
                                ObMark = Number(sub_result.obtain_marks).toFixed(0).toString()
                                oneObMark = Number(sub_result.one_obtain_marks).toFixed(0).toString()
                                twoObMark = Number(sub_result.two_obtain_marks).toFixed(0).toString()
                                threeObMark = Number(sub_result.three_obtain_marks).toFixed(0).toString()

                            }
                            term_1_row += `<td>
                            <table style="width:100%; border:0px !important;">
                                <tr>
                                    <th style="padding:2px;border:0px !important; width:30px;background:#e6FFe6" >${oneObMark}</th>
                                    <th style="padding:2px;border:0px !important; width:35px;">${sub_result ? sub_result.one_grade_point : ""}</th>
                                    <th style="padding:2px;border:0px !important; width:30px;">${sub_result ? sub_result.one_result_grade : ""}</th>
                                </tr>
                            </table>
                           
                        </td>`
                            term_2_row += `<td>
                            <table style="width:100%; border:0px !important;">
                                <tr>
                                    <th style="padding:2px;border:0px !important; width:30px;background:#e6FFe6" >${twoObMark}</th>
                                    <th style="padding:2px;border:0px !important; width:35px;">${sub_result ? sub_result.two_grade_point : ""}</th>
                                    <th style="padding:2px;border:0px !important; width:30px;">${sub_result ? sub_result.two_result_grade : ""}</th>
                                </tr>
                            </table>
                           
                        </td>`
                            final_row += `<td>
                            <table style="width:100%; border:0px !important;">
                                <tr>
                                    <th style="padding:2px;border:0px !important; width:30px;background:#e6FFe6" >${ObMark}</th>
                                    <th style="padding:2px;border:0px !important; width:35px;">${sub_result ? sub_result.grade_point : ""}</th>
                                    <th style="padding:2px;border:0px !important; width:30px;">${sub_result ? sub_result.result_grade : ""}</th>
                                </tr>
                            </table>
                           
                        </td>`
                            
                        });
                        let Additional_line = ""
                        let Additional = data.subject_results.filter(r => r.student_roll == result.student_roll)
                        for (let index = 0; index < Additional.length; index++) {
                            const element = Additional[index];
                            if (element.is_optional) {
                                Additional_line = `<br><span style="font-size:8px">Without Additional Subject = ${result.grade_point_without_furth}</span>`;
                                break;
                            }

                        }

                        term_1_row += `<td style="padding:2px">${result.one_grade_point ? result.one_grade_point:""}</td>
								<td class="text-center">${result.one_result_grade ? result.one_result_grade:""}</td></tr>`
                        term_2_row += `<td style="padding:2px">${result.two_grade_point ? result.two_grade_point:""}</td>
								<td class="text-center">${result.two_result_grade ? result.two_result_grade:""}</td></tr>`
                        
                        final_row += `<td style="padding:2px">${result.grade_point}</td>
								<td class="text-center">${result.result_grade}</td>
								<td class="text-center" rowspan="3">${result.merit_position}</td></tr>`
                        row += final_row;
                        row += term_1_row;
                        row += term_2_row;
                        
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

setInterval(() => {
    var elements = document.getElementsByClassName('final-row'); // get all elements
    for (var i = 0; i < elements.length; i++) {
        if (i % 2 == 0) {
            elements[i].style.backgroundColor = "#FE8985";
        } else {
            elements[i].style.backgroundColor = "#85E6FE";
        }
    }
}, 1000);