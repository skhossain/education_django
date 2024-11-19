$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
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


// $('#meal_list').change(function(){
//     $.when(filtering_info()).then(
//         filtering_student_list()
//     );
// })




// $('#meal_list').change(function(){
//     filtering_info()  
// })

// function filtering_info() {
//     let meal_id=document.getElementById('meal_list').value
//     postdata={
//         meal_id:meal_id,
//     }
//     $.ajax({
//         url: '/hostel-dailymeal-filterlist',
//         data: postdata,
//         type: 'get',
//         success: function (data) {
//             document.getElementById('table-data').innerHTML = data
//         }
//     })
// }


// function daily_meal_info_submit(){
//     const data_string = $("#insert_data").serialize();
//     const data_url = $("#insert_data").attr('data-url');
//         $.ajax({
//             url: data_url,
//             data: data_string,
//             type: 'POST',
//             dataType: 'json',
//             success: function (data) {
//                 console.log(data)
//                 if(data.error_message){
//                     alert(data.error_message)
//                 }
//                 if(data.success_message){
//                     alert(data.success_message)
//                 }
//             }
//     })
// }


// $('#meal_list').change(function(){
//     filtering_meal_student_list()  
// })
// $('#student_list').change(function(){
//     filtering_meal_student_list()  
// })

function filtering_meal_student_list(){
    let meal_id=document.getElementById('meal_list').value
    let student_roll=document.getElementById('student_list').value
    let start_date=document.getElementById('start_date').value
    let end_date=document.getElementById('end_date').value
    postdata={
        meal_id:meal_id,
        student_roll:student_roll,
        start_date:start_date,
        end_date:end_date,
    }

    $.ajax({
        url: "hostel-dailymeal-studentfilterlist",
        data:postdata,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            document.getElementById('table-data').innerHTML = data.html_form
        }
    })
}


function daily_meal_short_summary(){
    let meal_id=document.getElementById('meal_list').value
    let student_roll=document.getElementById('student_list').value
    let start_date=document.getElementById('start_date').value
    let end_date=document.getElementById('end_date').value
    postdata={
        meal_id:meal_id,
        student_roll:student_roll,
        start_date:start_date,
        end_date:end_date,
    }

    $.ajax({
        url: "hostel-dailymeal-shortsummary",
        data:postdata,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            document.getElementById('table-data').innerHTML = data.html_form
        }
    })
}

function search_for_cancel(){
    let meal_id=document.getElementById('meal_list').value
    let student_roll=document.getElementById('student_list').value
    let start_date=document.getElementById('start_date').value
    let end_date=document.getElementById('end_date').value
    postdata={
        meal_id:meal_id,
        student_roll:student_roll,
        start_date:start_date,
        end_date:end_date,
    }

    $.ajax({
        url: "hostel-dailymeal-search-cancel",
        data:postdata,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            document.getElementById('table-data').innerHTML = data.html_form
        }
    })
}

function cancle_meal(el){
    date=el.getAttribute('data-date')
    data_info=el.getAttribute('data-info').split(",")
    meal_id=data_info[0]
    qty=data_info[1]
    student_roll=data_info[2]
    postdata={
        meal_id:meal_id,
        date:date,
        qty:qty,
        student_roll:student_roll
    }
    $.ajax({
        url: "hostel-dailymeal-cancel",
        data:postdata,
        type: 'post',
        datatype: 'json',
        success: function (data) {
            search_for_cancel()
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: data.success_message,
                showConfirmButton: false,
                timer: 1500
            })

        }
    })
    
}

$(document).ready(function() {
    $('#meal_list').select2({placeholder: " Select a meal name "});
    $('#student_list').select2({placeholder: " Select a student "});
});



 
