
var edu_count_edit=0;

function get_edu_degrees(){
    // apiedu-degree-api/
    $.ajax({
        url: "apiedu-degree-api/",
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var select_option='<option value="">------</option>'
            data.forEach(option=>{
                select_option+='<option value="'+option.degree_id+'">'+option.degree_name+'</option>'
            })

            sessionStorage.setItem("degree_list", select_option);
        }
    })
}

function get_institute(){
    // apiedu-degree-api/
    $.ajax({
        url: "apiedu-education-institute-api/",
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var select_option='<option value="">------</option>'
            data.forEach(option=>{
                select_option+='<option value="'+option.institute_id+'">'+option.institute_name+'</option>'
            })
			sessionStorage.setItem("institute_list", select_option);
        }
    })
}
get_edu_degrees()
get_institute()
var edu_degree_list_edit=sessionStorage.getItem("degree_list");
var institute_list_edit=sessionStorage.getItem("institute_list");

function new_education_field(){
    edu_count_edit+=1;
    $('#id_edu_count-edit').val(edu_count_edit)
    var html_data='<div class="form-row">\
    <div class="form-group col-md-2 mb-0">\
        <label>Degree Name</label>\
        <select name="degree'+edu_count_edit+'" class="form-control edu_degree_list">'+edu_degree_list_edit+'</select>\
    </div>\
    <div class="form-group col-md-3 mb-0">\
        <label>Board Name</label>\
        <input type="text" name="board'+edu_count_edit+'" placeholder="Dhaka" class="form-control">\
    </div>\
    <div class="form-group col-md-1 mb-0">\
        <label>Point</label>\
        <input type="number" name="point'+edu_count_edit+'" placeholder="5.00" class="form-control">\
    </div>\
    <div class="form-group col-md-1 mb-0">\
        <label>Grate</label>\
        <input type="text" name="grate'+edu_count_edit+'" placeholder="A+" class="form-control">\
    </div>\
    <div class="form-group col-md-2 mb-0">\
        <label>Passing Year</label>\
        <input type="text" name="year'+edu_count_edit+'" placeholder="2018" class="form-control">\
    </div>\
    <div class="form-group col-md-3 mb-0">\
        <label>Institute Name</label>\
        <select name="institute'+edu_count_edit+'" class="form-control edu_degree_list">'+institute_list_edit+'</select>\
    </div>\
</div>'
document.getElementById('Edu-qualification-edit').innerHTML+=html_data
}

var json_data=document.getElementById("get-education-qualification").innerText
	education_data=JSON.parse(json_data)
	count=education_data.length
	document.getElementById('id_edu_count-edit').value=count
	education_data.forEach((value,index) => {
		edu_count_edit=index+1
    var html_data='<div class="form-row">\
    <div class="form-group col-md-2 mb-0">\
        <label>Degree Name</label>\
        <select name="degree'+edu_count_edit+'" id="degree'+edu_count_edit+'" class="form-control edu_degree_list">'+edu_degree_list_edit+'</select>\
    </div>\
    <div class="form-group col-md-3 mb-0">\
        <label>Board Name</label>\
        <input type="text" name="board'+edu_count_edit+'" value="'+value.board_name+'" class="form-control">\
    </div>\
    <div class="form-group col-md-1 mb-0">\
        <label>Point</label>\
        <input type="number" name="point'+edu_count_edit+'" value="'+value.result_point+'" class="form-control">\
    </div>\
    <div class="form-group col-md-1 mb-0">\
        <label>Grate</label>\
        <input type="text" name="grate'+edu_count_edit+'" value="'+value.result_grate+'" class="form-control">\
    </div>\
    <div class="form-group col-md-2 mb-0">\
        <label>Passing Year</label>\
        <input type="text" name="year'+edu_count_edit+'" value="'+value.passing_year+'" class="form-control">\
    </div>\
    <div class="form-group col-md-3 mb-0">\
        <label>Institute Name</label>\
        <select name="institute'+edu_count_edit+'" id="institute'+edu_count_edit+'" class="form-control edu_degree_list">'+institute_list_edit+'</select>\
    </div>\
</div>'

document.getElementById('Edu-qualification-edit').innerHTML+=html_data


	var degree_potions=document.getElementById('degree'+edu_count_edit+'').options
for (let index = 0; index < degree_potions.length; index++) {
	if(degree_potions[index] && value.degree_id==degree_potions[index].value){
		degree_potions[index].setAttribute("selected","selected")
	}	
}

var institute_potions=document.getElementById('institute'+edu_count_edit+'').options
for (let index = 0; index < degree_potions.length; index++) {
	if(institute_potions[index] && value.institute_id==institute_potions[index].value){
		institute_potions[index].setAttribute("selected","selected")
	}	
}

});


// $(document).ready(function() {
//     $('#get-education-qualification select').select2();
//     $('#id_class_id').select2({placeholder: " Select a class "});
//     $('#id_class_group_id').select2({placeholder: " Select a degree name "});
// });