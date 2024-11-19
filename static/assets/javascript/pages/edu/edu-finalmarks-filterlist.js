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




function filtering_student() {
    class_id=document.getElementById('class_list').value
    postdata={
        class_id:class_id,      
    }
    $.ajax({
        url: '/edu-finalmarks-filtertable',
        data: postdata,
        type: 'POST',
        success: function (data) {
            document.getElementById('table-data').innerHTML=data
            //filtering_subjectlist()
            // filtering_shift()
        }
    })
}




function filtering_finalMarks(roll){
    
    if(roll){
        postdata={
            student_roll:roll
        }
        $.ajax({
            url: "/edu-finalmark-insert",
            type: 'POST',
            data: postdata,
            success: function (data) {
                $('#total_mark'+roll).text(data.total_marks)
                $('#obtain_mark_inroll'+roll).text(data.obtain_marks)
                $('#grade_point_inroll'+roll).text(data.result_grade)
                $('#grade_inroll'+roll).text(data.grade_point) 
            }
        })
    }
}


