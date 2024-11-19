$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
// above functon used is csrf token

function search_and_filter() {
    loder_Spinner(true)
    $.when(filtering_student()).then(
        setTimeout(() => {
            filtering_all_exam()
        }, 1000)
    );

}

$('#id_class_id').change(function () {
    filtering_groups()
    filtering_subjectlist()
})

$('#id_class_group_id').change(function () {
    filtering_subjectlist()
    // $.when(filtering_student()).then(
    //     filtering_subjectlist()
    // );
})


// $('#id_academic_year').change(function(){
//     $.when(filtering_student()).then(
//         filtering_subjectlist()
//     ); 
// })


function filtering_student() {
    let academic_year = document.getElementById('id_academic_year').value
    let class_id = document.getElementById('id_class_id').value
    let term_id = document.getElementById('id_term_id').value
    let class_group_id = document.getElementById('id_class_group_id').value
    let subject_id = document.getElementById('subject-list').value
    let branch_code = document.getElementById('id_branch_code').value
    let session_id = document.getElementById('id_session_id').value
    postdata = {
        academic_year: academic_year,
        class_id: class_id,
        class_group_id: class_group_id,
        subject_id: subject_id,
        branch_code: branch_code,
        session_id: session_id
    }
    if (academic_year && class_id && term_id) {
        $.ajax({
            url: '/edu-marksdetails-filtertable',
            data: postdata,
            type: 'POST',
            success: function (data) {
                document.getElementById('table-data').innerHTML = data
                //filtering_subjectlist()
                // filtering_shift()
            }
        })
    } else {
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Year,Term and Class name requeued!',
            // showConfirmButton: false,
            // timer: 1500
        })
    }
}


function filtering_subjectlist() {
    let class_id = document.getElementById('id_class_id').value
    let class_group_id = document.getElementById('id_class_group_id').value

    $.ajax({
        url: "apiedu-sublist-api/?class_id=" + class_id + "&class_group_id=" + class_group_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#subject-list option").remove();
            $("#subject-list").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#subject-list").append('<option value="' + element.subject_id + '">' + element.subject_name + '</option>');
            });
        }
    })
}
function filtering_groups() {
    let class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $('#id_class_group_id').empty()
            data.forEach(element => {
                var newOption = new Option(element.class_group_name, element.class_group_id, false, false);
                $('#id_class_group_id').append(newOption).trigger('change');
            });
        }
    })
}

function filtering_all_exam() {
    let student_rolls = eval($('#get_student_rolls').val())
    let class_id = document.getElementById('id_class_id').value
    let academic_year = document.getElementById('id_academic_year').value
    let term_id = document.getElementById('id_term_id').value
    let subject_id = document.getElementById('subject-list').value
    let branch_code = document.getElementById('id_branch_code').value
    let session_id = document.getElementById('id_session_id').value

    if (branch_code && class_id && academic_year && term_id && subject_id) {
        $.ajax({
            url: '/apiedu-examsetup-api/?branch_code=' + branch_code + '&class_id=' + class_id + '&academic_year=' + academic_year + '&term_id=' + term_id + '&subject_id=' + subject_id + '&session_id=' + session_id,
            datatype: 'json',
            type: 'GET',
            success: function (examsetup_apidata) {
                student_rolls.forEach((roll, idx) => {
                    $('#show_exam_inroll' + roll).empty()
                    var total_mark = 0// one subject total marks
                    examsetup_apidata.forEach(exam => {
                        var box = "<div class='row' id='exam_box" + exam.exam_id + roll + "'></div>"
                        $('#show_exam_inroll' + roll).append(box)
                        for (let index = 1; index <= exam.no_of_exam; index++) {
                            let label = `<label>${exam.exam_name}</label>`
                            if (exam.exam_name == 'None') {
                                label = ''
                            } else if (exam.exam_name == 'Null') {
                                label = ''
                            } else if (exam.exam_name == 'Nthing') {
                                label = ''
                            }

                            let item = "<div class='col'>" + label + "<input type='text' placeholder='" + exam.total_exam_marks + "' class='form-control' data-value='" + exam.exam_id + "," + index + "," + exam.total_exam_marks + "," + roll + "'id='each_input" + exam.exam_id + index + roll + "' onchange='obtain_mark_insert(this)'></div>"
                            $('#exam_box' + exam.exam_id + roll + '').append(item)
                            $.ajax({
                                url: 'apiedu-markdetails-api/?student_roll=' + roll + '&exam_id=' + exam.exam_id + '&exam_no=' + index + '&class_id=' + class_id + '&academic_year=' + academic_year + '&subject_id=' + subject_id + '',
                                type: 'get',
                                datatype: 'json',
                                success: function (markdetails_api_data) {
                                    if (markdetails_api_data[0]) {
                                        $('#each_input' + exam.exam_id + index + roll + '').val(markdetails_api_data[0].obtain_marks)
                                    } //if end
                                } //end success function
                            }) //ajax end  
                        }  //for end
                        let mark_item = "<div class='col-1'><table class='table-sm text-right'><tr><td><br></td></tr><tr><td><span id='each_exam_obtain" + exam.exam_id + roll + "'></span>/<span id='each_exam_total" + exam.exam_id + roll + "'></span></td></table></div>"
                        $('#exam_box' + exam.exam_id + roll + '').append(mark_item)
                        var each_to_mark = Number(exam.total_exam_marks)//one subject each exam fixed total marks
                        $('#each_exam_total' + exam.exam_id + roll + '').text(each_to_mark)
                        total_mark += Number(exam.total_exam_marks)//subject total marks

                        $.ajax({
                            url: 'edu-get-single-exam-mark?student_roll=' + roll + '&exam_id=' + exam.exam_id + '&subject_id=' + subject_id + '',
                            type: 'get',
                            datatype: 'json',
                            success: function (data) {
                                if (data.mark) {
                                    $('#each_exam_obtain' + exam.exam_id + roll + '').text(data.mark.obtain_marks)
                                }
                            } //end success function
                        }) //ajax end 
                    });//end exam foreach
                    $(".total_mark").text(total_mark)
                    $.ajax({
                        url: 'edu-get-single-subject-exam-mark?student_roll=' + roll + '&academic_year=' + academic_year + '&term_id=' + term_id + '&class_id=' + class_id + '&subject_id=' + subject_id + '',
                        type: 'get',
                        datatype: 'json',
                        success: function (data) {
                            $('#grade_point_inroll' + roll).text(data.result[1])
                            $('#grade_inroll' + roll).text(data.result[0])
                        } //end success function
                    }) //ajax end 

                    if (idx + 1 == student_rolls.length) {
                        loder_Spinner(false)
                    }
                });//end roll foreach

            } //end function 

        }) //end ajax
    } else {
        loder_Spinner(false)
    }//end if
}//end function

function obtain_mark_insert(alldata) {
    var branch_code = document.getElementById('id_branch_code').value
    var session_id = document.getElementById('id_session_id').value
    var class_id = document.getElementById('id_class_id').value
    var class_group_id = document.getElementById('id_class_group_id').value
    var subject_id = document.getElementById('subject-list').value
    var academic_year = document.getElementById('id_academic_year').value
    var term_id = document.getElementById('id_term_id').value
    let obtain_marks = alldata.value
    var no_of_exam_string = $(alldata).attr('data-value')
    var exam_no_array = no_of_exam_string.split(",")
    var exam_id = exam_no_array[0]
    var exam_no = exam_no_array[1]
    var total_exam_marks = exam_no_array[2]
    var student_roll = exam_no_array[3]
    postdata = {
        branch_code: branch_code,
        session_id: session_id,
        class_id: class_id,
        class_group_id: class_group_id,
        subject_id: subject_id,
        academic_year: academic_year,
        term_id: term_id,
        student_roll: student_roll,
        obtain_marks: obtain_marks,
        exam_id: exam_id,
        exam_no: exam_no,
        total_exam_marks: total_exam_marks
    }
    $.ajax({
        url: "/edu-studentmark-insert",
        type: 'POST',
        data: postdata,
        success: function (data) {
            if (data.error_message) {
                Swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: data.error_message,
                    showConfirmButton: true,
                })
            }//end if
            else {
                $('#each_exam_obtain' + exam_id + student_roll + '').text(Number(data.exam_result[1]).toFixed(2))
                $.ajax({
                    url: 'edu-get-single-subject-exam-mark?student_roll=' + student_roll + '&academic_year=' + academic_year + '&term_id=' + term_id + '&class_id=' + class_id + '&subject_id=' + subject_id + '',
                    type: 'get',
                    datatype: 'json',
                    success: function (grad_data) {
                        $('#grade_point_inroll' + student_roll).text(grad_data.result[1])
                        $('#grade_inroll' + student_roll).text(grad_data.result[0])
                    } //end success function
                }) //ajax end 
            }//end else
        }//end outer success function             
    }); //end outer ajax
}//end main function

function examTerm() {
    $.ajax({
        url: '/apiedu-examterm-api/',
        type: 'get',
        datatype: 'jason',
        success: function (data) {
            $("#id_term_id").append('<option value="">---------------------</option>');
            data.forEach(t => {
                $("#id_term_id").append('<option value="' + t.id + '">' + t.term_name + '</option>');
            })
        }
    })
}
examTerm()

$(document).ready(function () {
    $('select').select2();
    $('#id_academic_year').select2({ placeholder: " Select a year " });
    $('#id_class_id').select2({ placeholder: " Select a class " });
    $('#id_class_group_id').select2({ placeholder: " Select a group " });
    $('#subject-list').select2({ placeholder: " Select a subject name " });
});