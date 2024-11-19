
function ans_change(val,id){
    const data_string ={
        ansChange:'yes',
        value:val,
    }
    const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
        }
    })
}
function rightAns_change(val,id){
    const data_string ={
        ansChange:'no',
        value:val,
    }
    const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
        }
    })
}
function MultiRightAns_change(val,id){
    if ($(val).is(':checked')) {
        const data_string ={
            ansChange:'multiAns',
            value:1,
        }
        const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";    
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                console.log(data)
            }
        })
      }else{
        const data_string ={
            ansChange:'multiAns',
            value:0,
        }
        const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";    
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                console.log(data)
            }
        })
      }
    
}

function deleteAnswer(ans,id){
    $('#deleteAnswerModal').modal('show')
    $('.deleteAnswerModal').text(ans)
    $('#deleteAnswerConfrimeBtn').attr('data-val',id)
}
function deleteAnswerConfirmed(){
let id= $('#deleteAnswerConfrimeBtn').attr('data-val')
$.ajax({
    url: '/edu-online-exam-answer-delete/'+id,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
        $('#deleteAnswerModal').modal('hide')
        location.reload();
    }
})
}
function disable_edit(){
    let value=document.getElementById("question-status").value
    if (value != 'Locked'){
        $('#question_preview input:radio').attr('disabled','disabled');
        $('#question_preview input:checkbox').attr('disabled','disabled');
        $('#question_preview input').attr('readonly','readonly');
        $('#question_preview textarea').attr('readonly','readonly');
        $('#question_preview .fa-times-circle').addClass('d-none');
    }

}
disable_edit()

// var question_count=document.querySelectorAll('.que_tinymce')
// // console.log(typeof(question_count)
// if(question_count){
// question_count.forEach(element => {
//     console.log(element)
// });
// }

function question_change(id){
    var question= tinymce.get('que_text'+id).getContent()
    var data={
        'question':question
    }

    $.ajax({
        url: '/edu-online-exam-question-update/'+id,
        type: 'POST',
        data:data,
        dataType: 'json',
        success: function (data) {
            Swal.fire({
                position: 'top-center',
                icon: 'success',
                title: data.success,
                showConfirmButton: false,
                timer: 1000
              })
              setTimeout(() => {
                location.reload();
              }, 1000);
        }
    })

}

tinymce.init({ 
    selector: '.que_tinymce',
    plugins: 'table link autoresize fullscreen image code imagetools lists insertdatetime',
    menubar: 'file edit insert format table',
    toolbar: 'undo redo | styleselect | bold italic underline | forecolor backcolor | alignleft aligncenter alignright alignjustify | outdent indent numlist bullist table image link insertdatetime code fullscreen',
    images_upload_url: 'filebrowser/',
    file_picker_types: 'image',
    automatic_uploads: false
 });

function question_delete(id){
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/edu-online-exam-question-delete/'+id,
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    Swal.fire(
                        'Deleted!',
                        'This question has been deleted.',
                        'success'
                      )
                      location.reload();
                }
            })
          
        }
      })
}