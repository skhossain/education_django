
$(document).ready(function () {
    off_future_date('id_student_date_of_birth')
    off_future_date('id_student_joining_date')
    get_group_list();
});
var academicgroup = []
// added student info js nessesary js
$("#id_class_id").change(function () {
    set_group_list();
});

function get_group_list() {
    $.ajax({
        url: "/apiedu-academicgroup-api",
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            academicgroup = data
        }
    })
}

function set_group_list() {
    let class_id = $('#id_class_id').val()
    $('#id_class_group_id option').remove();
    $("#id_class_group_id").append('<option value="">------------</option>');
    // $('#id_class_group_id').val('').trigger('change')
    let class_groups = academicgroup.filter(g =>
        g.class_id.class_id == class_id
    )
    class_groups.forEach(G => {
        $("#id_class_group_id").append('<option value="' + G.class_group_id + '">' + G.class_group_name + '</option>');
    })
}

function close_modal() {
    $('#edit_model').modal('hide');
    // new stepsDemo();
}
var edu_degree_list = ""
var institute_list = ""
function get_edu_degrees() {
    // apiedu-degree-api/
    $.ajax({
        url: "/apiedu-degree-api/",
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var select_option = '<option value="">------</option>'
            data.forEach(option => {
                select_option += '<option value="' + option.degree_id + '">' + option.degree_name + '</option>'
            })
            edu_degree_list = select_option;
            // $('#id_edu_degree_list').append(edu_degree_list)
        }
    })
}



// var e = document.getElementById("id_edu_degree_list");
// function show(){
//   var as = document.forms[0].id_edu_degree_list.value;
//   var strUser = e.options[e.selectedIndex].value;
//   console.log(as, strUser);
// }
// e.onchange=show;
// show();

function get_institute() {
    // apiedu-degree-api/
    $.ajax({
        url: "/apiedu-education-institute-api/",
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var select_option = '<option value="">------</option>'
            data.forEach(option => {
                select_option += '<option value="' + option.institute_id + '">' + option.institute_name + '</option>'
            })
            institute_list = select_option;
            // $('#id_institute_list1').append(institute_list)
        }
    })
}
get_edu_degrees()
get_institute()
var edu_count = 1;
function edit_education(roll, id = null) {
    if (id) {
        degree_id = document.getElementById('degree_id' + id).value
        board_name = document.getElementById('board_name' + id).value
        grate_point = document.getElementById('grate_point' + id).value
        grate_latter = document.getElementById('grate_latter' + id).value
        passing_year = document.getElementById('passing_year' + id).value
        institute_id = document.getElementById('id_institute_list' + id).value
        postdata = {
            student_roll: roll,
            id: id,
            degree_id: degree_id,
            board_name: board_name,
            result_point: grate_point,
            result_grate: grate_latter,
            passing_year: passing_year,
            institute_id: institute_id,
        }
    } else {
        postdata = {
            student_roll: roll,
            id: id,
        }
    }
    $.ajax({
        url: "/edu-studentInfo-education-edit/",
        type: 'POST',
        data: postdata,
        dataType: 'json',
        success: function (data) {
            if (id == null) {
                var html_data = '<div class="form-row" data-id="' + data.education_id + '">\
                <div class="form-group col-md-2 mb-0">\
                    <label>Degree Name</label>\
                    <select onchange="edit_education('+ roll + ',' + data.education_id + ')" id="degree_id' + data.education_id + '" class="form-control edu_degree_list">' + edu_degree_list + '</select>\
                </div>\
                <div class="form-group col-md-2 mb-0">\
                    <label>Board Name</label>\
                    <input type="text" onchange="edit_education('+ roll + ',' + data.education_id + ')" id="board_name' + data.education_id + '" placeholder="Dhaka" class="form-control">\
                </div>\
                <div class="form-group col-md-1 mb-0">\
                    <label>Point</label>\
                    <input type="number" onchange="edit_education('+ roll + ',' + data.education_id + ')" id="grate_point' + data.education_id + '" placeholder="5.00" class="form-control">\
                </div>\
                <div class="form-group col-md-1 mb-0">\
                    <label>Grate</label>\
                    <input type="text" onchange="edit_education('+ roll + ',' + data.education_id + ')" id="grate_latter' + data.education_id + '" placeholder="A+" class="form-control">\
                </div>\
                <div class="form-group col-md-2 mb-0">\
                    <label>Passing Year</label>\
                    <input type="text" onchange="edit_education('+ roll + ',' + data.education_id + ')" id="passing_year' + data.education_id + '" placeholder="2018" class="form-control">\
                </div>\
                <div class="form-group col-md-4 mb-0">\
                    <label>Institute Name</label>\
                    <div class="d-flex">\
                    <select onchange="edit_education('+ roll + ',' + data.education_id + ')" id="id_institute_list' + data.education_id + '" class="form-control edu_degree_list institute_name">' + institute_list + '</select>\
                    <button class="btn btn-dark"  style="margin: 0px 5px;" data-value="'+ data.education_id + '" type="button" onclick="show_blank_editform(this)"><i class="fas fa-plus"></i></button>\
                    <button class="btn btn-danger" style="margin: 0px 5px;" type="button" onclick="delete_form(this.parentElement.parentElement.parentElement)"><i class="fas fa-trash"></i></button>\
                    </div>\
                </div>\
            </div>'
                $('#Edu-qualification').append(html_data)
            }
        }
    })

}



function legal_guardian_change(val) {
    if (val.value == 'others') {
        $('#other_legal_guardian').removeClass('d-none')
    } else {
        $('#other_legal_guardian').addClass('d-none')
    }
}

function delete_form(row, id) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
    }).then((result) => {
        if (result.isConfirmed) {
            $(row).remove()
            $.ajax({
                url: '/edu-studentInfo-education-delete/' + id,
                type: 'get',
                success: function (data) {
                    Swal.fire({
                        title: 'Deleted!',
                        text: "Your data has been deleted.",
                        icon: 'success',
                        showConfirmButton: false,
                        timer: 1500
                    })
                }
            })
        }
    })
}
// New Education Institute
function show_blank_editform(button) {
    let button_number = $(button).attr('data-value')
    $.ajax({
        url: '/edu-last-institute',
        type: 'get',
        beforeSend: function () {
            $('#institute_model').modal('show');
        },
        success: function (data) {
            $('#institute_model .modal-content').html(data);
            $('#this-new-institute').val(button_number)
        }
    })
}

function Add_institute() {
    var institute = $("#id_institute_name").val();
    var institute_code = $("#id_institute_code").val();
    var institute_address = $("#id_institute_address").val();
    var institute_contact = $("#id_institute_mobile").val();
    var lowest_degree = $("#id_lower_degree").val();
    var highest_degree = $("#id_higher_degree").val();

    var data_string = {
        institute: institute,
        institute_code: institute_code,
        institute_address: institute_address,
        institute_contact: institute_contact,
        lowest_degree: lowest_degree,
        highest_degree: highest_degree

    }
    // $('#page_loading').modal('show');
    $.ajax({
        url: "/edu-new-education-insert",
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.success_message) {
                let row_id = $('#this-new-institute').val()
                let button_number = Number(row_id)
                $('#institute_model').modal('hide')
                let option2 = '<option value="' + data.new_institute.institute_id + '">' + data.new_institute.institute_name + '</option>'
                $('.institute_name').append(option2)
                institute_list += option2

                if (button_number == 0) {
                    var institute_options = document.getElementById("id_last_institute_id").options
                    for (let index = 0; index < institute_options.length; index++) {
                        if (institute_options[index] && data.new_institute.institute_id == institute_options[index].value) {
                            institute_options[index].setAttribute("selected", "selected")
                        }
                    }
                } else {
                    var institute_options = document.getElementById("id_institute_list" + button_number).options
                    for (let index = 0; index < institute_options.length; index++) {
                        if (institute_options[index] && data.new_institute.institute_id == institute_options[index].value) {
                            institute_options[index].setAttribute("selected", "selected")
                        }
                    }
                    let url = window.location.href
                    let roll = url.split('/')[4]
                    edit_education(roll, button_number)
                }
            }
        }
    })
    return false;
}

var call_fn=0
function addressFunction() {
    if(call_fn==0){
        call_fn=1
        setTimeout(() => {
        if (document.getElementById("id_same_as").checked) {
            
            $('#id_per_division_id').val($("#id_pre_division_id").val()).trigger('change');
            setTimeout(() => {    
                $('#id_per_district_id').val($("#id_pre_district_id").val()).trigger('change');
            }, 300);
            setTimeout(() => {   
                $('#id_per_upozila_id').val($("#id_pre_upozila_id").val()).trigger('change');
            }, 550);
            $("#id_student_permanent_address").val($("#id_student_present_address").val());
            document.getElementById("id_same_as").setAttribute("disabled", "disabled");
            setTimeout(() => {
                document.getElementById("id_same_as").removeAttribute("disabled");
            }, 550);

        } else {
            $('#id_per_division_id').val('').trigger('change');
            setTimeout(() => {
                $('#id_per_district_id').val('').trigger('change');
            }, 300);
            setTimeout(() => {
                $('#id_per_upozila_id').val('').trigger('change');
            }, 550);
            document.getElementById("id_same_as").setAttribute("disabled", "disabled");
            setTimeout(() => {
                document.getElementById("id_same_as").removeAttribute("disabled");
            }, 550);
            $("#id_student_permanent_address").val('');
        }
        call_fn=0
        }, 100);
    }
}

$(document).ready(() => {
    // Select 2 
    $('select').select2()
    $('#id_academic_year').select2({ placeholder: " Select a year " })
    $('#id_class_id').select2({ placeholder: "Select a Class" })
    $('#id_class_group_id').select2({ placeholder: "Select a Class Group" })
    $('#id_last_institute_id').select2({ placeholder: "Select a Institute" })
    $('#id_catagory_id').select2({ placeholder: "Select a Category" })

});


// Crop and image upload

var $modal = $('#image_model');
var image = document.getElementById('pro_image');
var cropper;
$("#profile-image").on("change", function (e) {
    var files = e.target.files;
    var done = function (url) {
        image.src = url;
        $modal.modal('show');
    };
    var reader;
    var file;
    var url;
    if (files && files.length > 0) {
        file = files[0];
        if (URL) {
            done(URL.createObjectURL(file));
        } else if (FileReader) {
            reader = new FileReader();
            reader.onload = function (e) {
                done(reader.result);
            };
            reader.readAsDataURL(file);
        }
    }
});
$modal.on('shown.bs.modal', function () {
    cropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 3,
        preview: '.preview'
    });
}).on('hidden.bs.modal', function () {
    cropper.destroy();
    cropper = null;
});
$("#crop").click(function () {
    canvas = cropper.getCroppedCanvas({
        width: 300,
        height: 300,
    });
    canvas.toBlob(function (blob) {
        url = URL.createObjectURL(blob);
        var reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function () {
            var base64data = reader.result;
            let student_roll = $('#student_roll').val()
            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/edu-studentinfo-profile-image/"+student_roll,
                data: {'image': base64data },
                success: function (data) {
                    $('#profile-photo').attr('src',base64data)
                    $modal.modal('hide');
                    alert("Crop image successfully uploaded");
                }
            });
        }
    });
})


//student signature upload

var $singModal = $('#sing_model');
var sing_image = document.getElementById('sing_image');
var cropper_sing;
$("#profile-signatur").on("change", function (e) {
    var files = e.target.files;
    var done = function (url) {
        sing_image.src = url;
        $singModal.modal('show');
    };
    var reader;
    var file;
    var url;
    if (files && files.length > 0) {
        file = files[0];
        if (URL) {
            done(URL.createObjectURL(file));
        } else if (FileReader) {
            reader = new FileReader();
            reader.onload = function (e) {
                done(reader.result);
            };
            reader.readAsDataURL(file);
        }
    }
});
$singModal.on('shown.bs.modal', function () {
    cropper_sing = new Cropper(sing_image, {
        aspectRatio: 3/1,
        viewMode: 1,
        preview: '.singPreview'
    });
}).on('hidden.bs.modal', function () {
    cropper_sing.destroy();
    cropper_sing = null;
});
$("#sing_crop").click(function () {
    canvas = cropper_sing.getCroppedCanvas({
        width: 300,
        height: 300,
    });
    canvas.toBlob(function (blob) {
        url = URL.createObjectURL(blob);
        var reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function () {
            var base64data = reader.result;
            let student_roll = $('#student_roll').val()
            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/edu-studentinfo-profile-signature/"+student_roll,
                data: {'signature': base64data },
                success: function (data) {
                    $('#profile-sign').attr('src',base64data)
                    $singModal.modal('hide');
                    alert("Crop signature successfully uploaded");
                }
            });
        }
    });
})



////present district and upazila address filter

$('#id_pre_division_id').change(function(){
    pre_district_filter()
    pre_upozila_filter()
})


function pre_district_filter(){
var pre_division_id=document.getElementById('id_pre_division_id').value
$.ajax({
    url: "/apiauth-district-api/?division_id="+pre_division_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_pre_district_id option").remove();
        $("#id_pre_district_id").append('<option value="">----------</option>');
        data.forEach(element => {
            $("#id_pre_district_id").append('<option value="'+element.district_id+'">'+element.district_name+'</option>');
        });
    }
})
}


$('#id_pre_district_id').change(function(){
    pre_upozila_filter()
})

function pre_upozila_filter(){
var pre_district_id=document.getElementById('id_pre_district_id').value
if(pre_district_id.length){
$.ajax({
    url: "/apiauth-upazila-api/?district_id="+pre_district_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_pre_upozila_id option").remove();
        $("#id_pre_upozila_id").append('<option value="">----------</option>');
        data.forEach(element => {
            $("#id_pre_upozila_id").append('<option value="'+element.upozila_id+'">'+element.upozila_name+'</option>');
        });
    }
})
}
}


////permanent district and upazila address filter


$('#id_per_division_id').change(function(){
    setTimeout(() => {
        per_district_filter()
        per_upozila_filter()
    }, 50);

})

function per_district_filter(){
var per_division_id=document.getElementById('id_per_division_id').value
$.ajax({
    url: "/apiauth-district-api/?division_id="+per_division_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_per_district_id option").remove();
        $("#id_per_district_id").append('<option value="">----------</option>');
        data.forEach(element => {
            $("#id_per_district_id").append('<option value="'+element.district_id+'">'+element.district_name+'</option>');
        });
    }
})
}



$('#id_per_district_id').change(function(){
    setTimeout(() => {
        per_upozila_filter()
    }, 50);
    
})

function per_upozila_filter(){
var per_district_id=document.getElementById('id_per_district_id').value
if(per_district_id.length){
$.ajax({
    url: "/apiauth-upazila-api/?district_id="+per_district_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_per_upozila_id option").remove();
        $("#id_per_upozila_id").append('<option value="">----------</option>');
        data.forEach(element => {
            $("#id_per_upozila_id").append('<option value="'+element.upozila_id+'">'+element.upozila_name+'</option>');
        });
    }
})
}
}

