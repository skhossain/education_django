

$('#id_class_id').change(function(){
    filtering_students()
})

function filtering_students(){
    let class_id=document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-studentinfo-api/?class_id="+class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#id_student_roll option").remove();
            $("#id_student_roll").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#id_student_roll").append('<option value="'+element.student_id+'">'+element.student_name+'</option>')
            });
            console.log(data)
        }
    })
}
$('#id_road_map_id').change(function(){
    filter_locat()
})

function filter_locat(){
    let road_map_id=document.getElementById('id_road_map_id').value
    console.log(road_map_id)
    $.ajax({
        url: "apitransport-roadmapdtl-api/?road_map_id="+road_map_id,
        type: 'get',
        datatype: 'json',
        
        success: function (data) { 
            $("#id_location_info_id option").remove();
            $("#id_location_info_id").append('<option value="">------------</option>');
            list=[]
            data.forEach(element => {
               
                var loca={
                    'location_info_id':element.location_info_id.location_info_id,
                    'location_name':element.location_info_id.location_name
                }
                    if (!list.includes(loca)){
                       list.push(loca)
                    }
               
            });
            list.forEach(element=>{
               let html = '<tr>\
               <th>Location Name</th>\
               <th>Check</th>\
               </tr>'
               html += '<tr>\
                <td>'+element.location_name+'</td>\
                <td>\
                <input type="checkbox" id="location'+element.location_info_id+'" vlaue="'+element.location_info_id+'" onclick="student_list()">\
                </td>\
                <td></td>\
                </tr>'
                $('#location-list').html(html)
            });
        }
    })
}


function student_list(){
    let location_info_id=document.getElementById('id_location_info_id').value
    console.log(location_info_id)
    $.ajax({
        url: "apitransport-admit-transportation-api/?location_info_id="+location_info_id,
        type: 'get',
        datatype: 'json',
        success: function (data) { 
            $("#id_student_roll option").remove();
            $("#id_student_roll").append('<option value="">------------</option>');
            list=[]
            data.forEach(element => {
               
                var loca={
                    'student_roll':element.student_roll.student_roll,
                    'student_name':element.student_roll.student_name
                }
                    if (!list.includes(loca)){
                       list.push(loca)
                    }
               
            });
            list.forEach(element=>{
               let html = '<tr>\
               <th>Student Name</th>\
               <th>Check</th>\
               </tr>'
               html += '<tr>\
                <td>'+element.student_name+'</td>\
                <td>\
                <input type="checkbox" id="student'+element.student_roll+'" vlaue="'+element.student_roll+'">\
                </td>\
                </tr>'
                $('#student-list').html(html)
            });
        }
    })
}

$(document).ready(function() {
    $('#id_academic_year').select2({placeholder: " Select a year "});
    $('#id_class_id').select2({placeholder: " Select a class "});
    $('#id_month_no').select2({placeholder: " Select a month "});
    $('#id_student_roll').select2({placeholder: " Select a student "});
    $('#id_road_map_id').select2({placeholder: " Select a road map "});
});