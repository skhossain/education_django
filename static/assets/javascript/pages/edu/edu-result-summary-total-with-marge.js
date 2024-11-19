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
    const session_id = urlParams.get('session_id')
    const marge_tilte = urlParams.get('marge_tilte')
    const term_1 = urlParams.get('term_1')
    const term_2 = urlParams.get('term_2')
    const term_3 = urlParams.get('term_3')
    const template = urlParams.get('template')
    let data_string = {
        branch_code: branch_code,
        academic_year: academic_year,
        session_id: session_id,
        marge_tilte: marge_tilte,
        term_1: term_1,
        term_2: term_2,
        term_3: term_3,
        csrfmiddlewaretoken: csrftoken

    }
    if (branch_code && academic_year && term_1 && term_2) {
        $.ajax({
            url: 'edu-result-marge-summary-total-data',
            data: data_string,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                let total_student=0;
                let total_grade_result=[]
                let lg = ``
                data.results[0][1].forEach(g => {
                    lg += `<th class="text-center">${g.grade_name}</th>`
                    total_grade_result.push({ grade_name: g.grade_name, grade_count:0})
                });
                let row =`<tr>
                            <th>SL</th>
                            <th>Class Name</th>
                            <th>Group Name</th>
                            <th class="text-center">Examinee</th>
                            ${lg}
                            <th class="text-center">Pass</th>
                            <th class="text-center">Pass Rate</th>
                        </tr>`
                $('#summery_table').append(row)
                let counter = 1;
                data.results.forEach(class_result => {
                    let class_and_group_result=[]
                    let class_and_group = []
                    
                    class_result[0].forEach(result => {
                        let obj = { class_name: result.class_name, class_group: result.class_group }
                        if (!class_and_group.find(r => r.class_name == result.class_name && r.class_group == result.class_group)) {
                            class_and_group.push(obj)
                        }
                        class_result[1].forEach(grade => {
                            if (grade.grade_name == result.result_grade) {
                                let find_summery = class_and_group_result.find(r => r.class_name == result.class_name && r.class_group == result.class_group && r.grade == grade.grade_name)
                                if (!find_summery){
                                    let r_obj = { class_name: result.class_name, class_group: result.class_group, grade: grade.grade_name, grade_count: 1 }
                                    class_and_group_result.push(r_obj)
                                } else {
                                    find_summery.grade_count +=1 
                                }
                            }
                        });
                        let g_result = total_grade_result.find(gr => gr.grade_name == result.result_grade)
                        g_result.grade_count +=1;
                        total_student +=1;
                    });
                                        
                    class_and_group.forEach(classs => {
                        let classGroupResult = class_result[0].filter(cr => cr.class_name == classs.class_name && cr.class_group == classs.class_group)
                        let result_row = `<tr>`
                        result_row += `<th class="text-center">${counter}</th>`
                        result_row += `<th>${classs.class_name}</th>`
                        result_row += `<th>${classs.class_group ? classs.class_group:""}</th>`
                        result_row += `<th class="text-center">${classGroupResult.length}</th>`
                        
                        data.results[0][1].forEach(g => {
                            let get_lg = class_and_group_result.find(r => r.class_name == classs.class_name && r.class_group == classs.class_group && r.grade == g.grade_name)
                            result_row += `<th class="text-center">${get_lg ? get_lg.grade_count:0}</th >`
                        });
                        let faild_count = class_and_group_result.find(r => r.class_name == classs.class_name && r.class_group == classs.class_group && r.grade == 'F')
                        result_row += `<th class="text-center">${classGroupResult.length - (faild_count ? faild_count.grade_count : 0)}</th>`
                        result_row += `<th class="text-center">${(((classGroupResult.length-(faild_count ? faild_count.grade_count : 0)) / classGroupResult.length)*100).toFixed(2)}%</th>`
                        result_row += `</tr>`
                        $('#summery_table').append(result_row)
                        counter += 1;
                    });
                    
                });
                let total_row=`<tr>
                <th colspan="3">Total</th>
                <th class="text-center">${total_student}</th>`
                total_grade_result.forEach(g => {
                    total_row += `<th class="text-center">${g.grade_count}</th >`
                });
                let total_f = total_grade_result.find(gr=> gr.grade_name == 'F')
                total_row += `<th class="text-center">${total_student - total_f.grade_count}</th >`
                total_row += `<th class="text-center">${(((total_student - total_f.grade_count) / total_student)*100).toFixed(2)}%</th > </tr>`
                $('#summery_table').append(total_row)
                
                // console.log(data)
            }
        })

    } else {
        // Swal.fire({
        //     position: 'center',
        //     icon: 'error',
        //     title: 'Branch code, Year, Class Name and Exam Term is required. ',
        //     showConfirmButton: true,
        //     //timer: 1500
        // })
    }
});

setInterval(() => {
    let th = document.getElementsByTagName('th')
    for (let index = 0; index < th.length; index++) {
        th[index].style.fontSize = '12px'        
    }
    let td = document.getElementsByTagName('td')
    for (let index = 0; index < td.length; index++) {
        td[index].style.fontSize = '12px'
    }
}, 1000);