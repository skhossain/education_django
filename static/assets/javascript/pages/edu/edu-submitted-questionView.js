
function disable_edit(){
    let value=document.getElementById("question-status").value
    console.log(value)
    if (value == 'Live' || value == 'Submitted' ){
        $('#question_preview input:radio').attr('disabled','disabled');
        $('#question_preview input:checkbox').attr('disabled','disabled');
        // $('#question_preview input').attr('readonly','readonly');
        $('#question_preview textarea').attr('readonly','readonly');
        // $('#question_preview .fa-times-circle').addClass('d-none');
    }else{
        $('#question_preview input').removeattr('readonly');
        $('#question_preview textarea').removeattr('readonly');
    }

}
disable_edit()


function question_marking(id,mark,question_mark){
   if (question_mark>=mark){
    postdata={
        obtain_marks:mark,
    }
    $.ajax({
        url: '/edu-onlineexam-queansmarking/'+id,
        type: 'POST',
        data:postdata,
        dataType: 'json',
        success: function (data) {
           
        }
    })
}else{
    Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Obtain mark largest to Question mark !',
      })
}
}