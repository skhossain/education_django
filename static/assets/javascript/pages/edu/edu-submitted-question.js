function search_question(){
    var academic_year=document.getElementById('year_list').value
    var class_id=document.getElementById('class_list').value
    var exam_id=document.getElementById('exam_list').value
    postdata={
        academic_year:academic_year,
        class_id:class_id,
        online_exam_id:exam_id,
    }
    $.ajax({
        url: "/edu-submitted-questionlist",
        type: 'get',
        data: postdata,
        success: function (data) {
            console.log(data)
            $('#questionlist').html(data)
        }//end outer success function             
    });
}

$('#submit_confirm').change(function (){
    if($(this).is(":checked")){
        $('#submit_button').removeAttr('disabled')
    }else{
        $('#submit_button').attr('disabled','disabled')
    }
})

function onlineexam_result_publish(){
    var academic_year=document.getElementById('year_list').value
    var class_id=document.getElementById('class_list').value
    var exam_id=document.getElementById('exam_list').value
    postdata={
        academic_year:academic_year,
        class_id:class_id,
        online_exam_id:exam_id,
    }
    $.ajax({
        url: "/edu-onlineexam-result-publish",
        type: 'get',
        data: postdata,
        success: function (data) {
           if(data.success){
               location.reload();
           }
        }//end outer success function             
    });
}


$(document).ready(function() {
    $('#year_list').select2({placeholder: " Select a year "});
    $('#class_list').select2({placeholder: " Select a class "});
    $('#exam_list').select2({placeholder: " Select a exam name "});
});