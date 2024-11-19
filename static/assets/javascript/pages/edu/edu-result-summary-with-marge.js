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
            url: 'edu-result-marge-summary-data',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                let grade = []
                data.result_grades.forEach(lg => {
                    let name = {}
                    name[lg.grade_name] = 0
                    grade.push(name)
                });

                let total_male = 0;
                let total_female = 0;
                data.results.forEach(result => {
                    if (result.gander == 'M') {
                        total_male += 1;
                    }
                    if (result.gander == 'F') {
                        total_female += 1;
                    }
                    let grade_info = data.result_grades.find(g => g.grade_name == result.result_grade)
                    grade.forEach(g => {
                        if (Object.keys(g)[0] == grade_info.grade_name) {
                            g[grade_info.grade_name] += 1
                        }

                    });

                });
                let total_pass = 0
                let grade_samary_row = ``
                grade.forEach(g => {
                    grade_samary_row += `<tr>
                    <td>${Object.keys(g)[0]}</td>
                    <td>${g[Object.keys(g)[0]]}</td>
                    <td>${(100 / (data.results.length / (g[Object.keys(g)[0]]))).toFixed(2)}%</td>
                    <tr>`
                    if (Object.keys(g)[0] == 'F') {
                        total_pass = data.results.length - g['F']
                    }
                });


                let div = `<div class="row">
                <div class="col-6">
                <h5>Class Student Information</h5>
                    <table class="table table-sm">
                    <tr>
                    <th>Total Student</th>
                    <td>${data.results.length}</td>
                    </tr>
                    <tr>
                    <th>Male </th>
                    <td>${total_male}</td>
                    </tr>
                    <tr>
                    <th>Female </th>
                    <td>${total_female}</td>
                    </tr>
                    </table>
                    <br>
                    <h5>Total Pass of Students:<br> ${total_pass} - ${(100 / (data.results.length / total_pass)).toFixed(2)}%</h5>
                </div>
                <div class="col-6">
                <h5>Grade wise Result</h5>
                <table class="table table-sm">
                <tr>
                <th>Grade Name</th>
                <th>Count</th>
                <th>Percent</th>
                </tr>
                ${grade_samary_row}
                </table>
                </div>
                </div>`
                $('#body_div').append(div)
                console.log(data)
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

// setInterval(() => {
//     var elements = document.getElementsByClassName('final-row'); // get all elements
//     for (var i = 0; i < elements.length; i++) {
//         if (i % 2 == 0) {
//             elements[i].style.backgroundColor = "#FE8985";
//         } else {
//             elements[i].style.backgroundColor = "#85E6FE";
//         }
//     }
// }, 1000);