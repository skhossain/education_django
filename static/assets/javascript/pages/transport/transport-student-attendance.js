function student_list(){
    var academic_year = $("#id_academic_year").val();
    var class_id = $("#id_class_id").val();
    var road_map_id = $("#id_road_map_id").val();
    var trans_status = $("#id_trans_status").val();
    var data_string={
        academic_year:academic_year,
        class_id:class_id,
        road_map_id:road_map_id,
        trans_status:trans_status
    }          
    $.ajax({      
        url: "/transport-student-list-ajax",
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            document.getElementById('data-div').innerHTML = data.html_form 
        }
    })
}

$(document).ready(function() {
    $('#id_academic_year').select2({placeholder: " Select a year "});
    $('#id_class_id').select2({placeholder: " Select a class "});
    $('#id_road_map_id').select2({placeholder: " Select a road map "});
});

function select_location(){
    var students = document.getElementById('all-student').value.replace('[','').replace(']','').replace(/'/g, '"').split('},')
    var locations= document.querySelectorAll('.location')
    html=""
    locations.forEach(L => {
        if(L.checked){
            students.forEach(s => {
                var st = s+'}'
                var student= JSON.parse(st.replace('}}','}'))
               
                if(student.location_info_id === L.value){
                    html+='<div class="form-check">\
                    <input class="form-check-input student" type="checkbox" value="'+student.student_roll+'" id="stu'+student.student_roll+'">\
                    <label class="form-check-label" for="stu'+student.student_roll+'">\
                        '+student.student_name+'\
                    </label>\
                  </div>'
                  
                }
            });
        }
    });
    document.getElementById('student_list').innerHTML=html
    
}

function saveForm(){
    var road_map_id = document.getElementById('id_road_map_id').value
    var trans_status = document.getElementById('id_trans_status').value
    if(road_map_id && trans_status){
    var locations=[]
    var students=[]
    document.querySelectorAll('.location').forEach(l =>{
        if(l.checked){
        locations.push(l.value)
        }
    })
    document.querySelectorAll('.student').forEach(S =>{
        if(S.checked){
            students.push(S.value)
        }
    })
    data_string={
        road_map_id:road_map_id,
        trans_status:trans_status,
        students:students
    }
    console.log(data_string)
    $.ajax({      
        url: "/transport-student-attendance-insert",
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.error_message){
                Swal.fire(
                    'Data Save!',
                    data.error_message,
                    'error'
                  )
            }else{
            Swal.fire(
                'Data Save!',
                data.success_message,
                'success'
              )
            }
        }
    })
}else{
    Swal.fire(
        'Data Missing!',
        'Road map and Status value is null.',
        'error'
      )
}
}