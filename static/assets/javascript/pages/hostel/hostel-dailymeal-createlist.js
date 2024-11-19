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




$('#meal_list').change(function(){
    filtering_info()  
})

function filtering_info() {
    let meal_id=document.getElementById('meal_list').value
    postdata={
        meal_id:meal_id,
    }
    $.ajax({
        url: '/hostel-dailymeal-filterlist',
        data: postdata,
        type: 'get',
        success: function (data) {
            document.getElementById('table-data').innerHTML = data
        }
    })
}


function daily_meal_info_submit(){
    const data_string = $("#insert_data").serialize();
    const data_url = $("#insert_data").attr('data-url');
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if(data.error_message){
                    Swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: data.error_message,
                        showConfirmButton: true,
                        })
                }
                if(data.success_message){
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: data.success_message,
                        showConfirmButton: false,
                        timer: 1500
                    })
                    window.location.reload()
                }
                
            }
    })
}

function allselect(source) {
    var checkboxes = document.querySelectorAll('.student');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
        check_single_student(checkboxes[i])
    }
}

$(document).ready(function() {
    $('#meal_list').select2({placeholder: " Select a meal name "});
});

function meal_number_change(source){
    if(source.value <= 0){
        let student_roll = source.name.split('eat_is')[1]
        let event = document.getElementById('roll'+student_roll)
        event.checked = false
    }
}

function check_single_student(source){
    if(source.checked){
        let student_roll = source.id.split('roll')[1]
        let event = document.getElementsByName('eat_is'+student_roll)
        if(event[0].value <= 0){
            event[0].value = 1
        }
    }
}
 
