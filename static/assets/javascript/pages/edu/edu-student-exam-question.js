function ExamStartPermission(){
    // var academic_year=document.getElementById('id_academic_year').value
    // var class_id=document.getElementById('id_class_id').value
    var student_roll=document.getElementById('id_student_roll').value
    var exam_id=document.getElementById('exam_list').value
    postdata={
        // academic_year:academic_year,
        // class_id:class_id,
        student_roll:student_roll,
        online_exam_id:exam_id,
    }
    console.log(postdata)
    $.ajax({
        url: "/edu-exam-question-html",
        type: 'get',
        data: postdata,
        success: function (data) {
            // console.log(data)
            $('#preview_push').html(data)
        }//end outer success function             
    });
}

function mcq_rightAns(val,id){
    let data_string = {
        question_type:'MCQ',
        value:val
    }
    let data_url = '/edu-online-exam-ans-by-student/'+id;
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
     
        }
    })
}

function mcqs_rightAns(val,id){
    if ($(val).is(':checked')) {
        const data_string ={
            question_type:'MCQS',
            value:1,
        }
        const data_url = '/edu-online-exam-ans-by-student/'+id;   
      $.ajax({
          url: data_url,
          data: data_string,
          type: 'POST',
          dataType: 'json',
          success: function (data) {
          }
      })
      }else{
        const data_string ={
            question_type:'MCQS',
            value:0,
        }
        const data_url = '/edu-online-exam-ans-by-student/'+id;   
      $.ajax({
          url: data_url,
          data: data_string,
          type: 'POST',
          dataType: 'json',
          success: function (data) {
          }
      })
      }
      
}

function text_answer(val,id){
    const data_string ={
        question_type:'Short',
        value:val,
    }
    const data_url = '/edu-online-exam-ans-by-student/'+id;   
  $.ajax({
      url: data_url,
      data: data_string,
      type: 'POST',
      dataType: 'json',
      success: function (data) {
      }
  })
}



$(document).ready(function() {
    $('#exam_list').select2({placeholder: " Select a exam name "});
});