function online_exam_que_del(id){
    $('#deleteQueModal').modal('show');
    // apiedu-online-exam-question/?id=000050
    $.ajax({
        url: '/apiedu-online-exam-question/?id='+id,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('.deleteQueModal').html(data[0].question);
            $('#deleteQuestionConfirmedBtn').attr('data-val',id)
        }
    })
    
}

function online_exam_que_del_confirmed(){
    let id=$('#deleteQuestionConfirmedBtn').attr('data-val')
    $.ajax({
        url: '/edu-online-exam-question-delete/'+id,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if(data.success_message){
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: data.success_message,
                    showConfirmButton: false,
                    timer: 1500
                })
            };
            location.reload();
        }
    })
}