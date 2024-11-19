// // $('#que_pre').click(function(){
// //     online_exam_question_preview();
// // })
// // function online_exam_question_preview(){
// //     $.ajax({
// //         url: '/apiedu-online-exam-question',
// //         type: 'get',
// //         success: function (data) {
// //             document.getElementById('preview_push').innerHTML = data
            
// //         }
// //     })
// // }


// // $(".fc").children('input').addClass("form-control");
// // $(".fc").children('select').addClass("form-control");
// // $(".fc").children('select').attr("disabled", true);
// // $('#id_question_type').change(
// //     function(){
// //         let ty=$('#id_question_type').val();
// //         if(ty=='MCQ' || ty=='MCQS'){
// //             $('#btn-choices').css('display','block');
// //         }else{
// //             $('#btn-choices').css('display','none');
// //         }
// //         ans_count=0
// //         $('#answer_input').empty()
// //         $('#id_answer_count').val(ans_count)
// //     }
// //     )

// // $('#btn-choices').click(
// //     function (){
// //         let que_type=$('#id_question_type').val();
// //         let que_id = $('#id_question_id').val()
// //         // edu-online-exam-create-mcq-answer-field
// //         $.ajax({
// //             url: '/edu-online-exam-create-mcq-answer-field/'+que_id,
// //             type: 'GET',
// //             success: function (data) {
// //                 location.reload();
// //             }
// //         })
        
// //     }
// // )

// function ans_change(val,id){
//     const data_string ={
//         ansChange:'yes',
//         value:val,
//     }
//     const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";
//     $.ajax({
//         url: data_url,
//         data: data_string,
//         type: 'POST',
//         dataType: 'json',
//         success: function (data) {
//             console.log(data)
//         }
//     })
// }
// function mcq_rightAns(val,id){
//     console.log(val)
//     console.log(id)
//     // const data_string ={
//     //     ansChange:'no',
//     //     value:val,
//     // }
//     // const data_url = "/edu-online-exam-ans-by-student/"+id+"";
//     // $.ajax({
//     //     url: data_url,
//     //     data: data_string,
//     //     type: 'POST',
//     //     dataType: 'json',
//     //     success: function (data) {
//     //         console.log(data)
//     //     }
//     // })
// }
// function MultiRightAns_change(val,id){
//     if ($(val).is(':checked')) {
//         const data_string ={
//             ansChange:'multiAns',
//             value:1,
//         }
//         const data_url = "/edu-online-student-exam/"+id+"";    
//         $.ajax({
//             url: data_url,
//             data: data_string,
//             type: 'POST',
//             dataType: 'json',
//             success: function (data) {
//                 console.log(data)
//             }
//         })
//       }else{
//         const data_string ={
//             ansChange:'multiAns',
//             value:0,
//         }
//         const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";    
//         $.ajax({
//             url: data_url,
//             data: data_string,
//             type: 'POST',
//             dataType: 'json',
//             success: function (data) {
//                 console.log(data)
//             }
//         })
//       }
    
// }


