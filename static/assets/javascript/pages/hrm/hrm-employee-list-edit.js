"use strict";

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _defineProperties(target, props) {
  for (let i = 0; i < props.length; i++) {
    let descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ("value" in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  return Constructor;
}

let table_data;

const fn_data_table = (function () {
  function fn_data_table() {
    _classCallCheck(this, fn_data_table);

    this.init();
  }

  _createClass(fn_data_table, [
    {
      key: "init",
      value: function init() {
        this.table = this.table();
      },
    },
    {
      key: "table",
      value: function table() {
        const employee_id = "";
        const search_url = "/apihrm-employee-api?employee_id=" + employee_id;
        table_data = $("#dt-table-list").DataTable({
          processing: true,
          destroy: true,
          ajax: {
            url: search_url,
            type: "GET",
            dataSrc: "",
          },
          responsive: true,
          dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
          language: {
            paginate: {
              previous: '<i class="fa fa-lg fa-angle-left"></i>',
              next: '<i class="fa fa-lg fa-angle-right"></i>',
            },
          },
          columns: [
            { data: "employee_name" },
            { data: "employee_father_name" },
            { data: "employee_mother_name" },
            { data: "employee_blood_group" },
            { data: "employee_sex" },
            { data: "employee_religion" },
            { data: "employee_marital_status" },
            { data: "employee_national_id" },
            { data: "country_id" },
            { data: "division_id" },
            { data: "district_id" },
            { data: "upozila_id" },
            { data: "employee_present_address" },
            { data: "employee_permanent_address" },
            { data: "employee_phone_own" },
            { data: "employee_phone_office" },
            { data: "employee_phone_home" },
            { data: "passport_no" },
            { data: "driving_licence" },
            { data: "employee_tin" },
            { data: "email_personal" },
            { data: "employee_joining_date" },
            { data: "employee_date_of_birth" },
            { data: "employee_status" },
            { data: "eme_contact_name" },
            { data: "eme_contact_relation" },
            { data: "eme_contact_phone" },
            { data: "eme_contact_address" },
            { data: "office_id" },
            { data: "emptype_id" },
            { data: "salscale" },
            { data: "designation_id" },
            { data: "email_official" },
            { data: "reporting_to" },
            { data: "current_shift" },
            { data: "office_location" },
            { data: "card_number" },
            { data: "salary_bank" },
            { data: "salary_bank_ac" },
            { data: "contract_start_date" },
            { data: "contract_exp_date" },
            { data: "last_inc_date" },
            { data: "next_inc_date" },
            { data: "service_end_date" },
            { data: "last_transfer_date" },
            { data: "next_transfer_date" },
            { data: "job_confirm_date" },
            { data: "pf_confirm_date" },
            { data: "gf_confirm_date" },
            { data: "wf_confirm_date" },
            { data: "last_promotion_date" },

            {
              data: null,
              defaultContent:
                '<button type="button" class="btn btn-info btn-sm">Edit</button>',
            },
          ],
        });
      },
    },
  ]);

  return fn_data_table;
})();

let id = 0;

$("#btnSearch").click(function () {
  new fn_data_table();
});

$(document).ready(function () {
  fn_set_degree_info();
  get_experience_data();
});

const emptyForm = () => {
  $("#id_company_name").val("");
  $("#id_company_address").val("");
  $("#id_company_type").val("");
  $("#id_position").val("");
  $("#id_department").val("");
  $("#id_responsibility").val("");
  $("#id_achievement").val("");
  $("#id_phone_number").val("");
  $("#id_email").val("");
  $("#id_contact_person").val("");
  $("#id_start_date").val("");
  $("#id_end_date").val("");
  $("#id_employee_experience_id").val("");
};

var data_list_experience = [];
$("#experinceListAdd").click(function () {
  let employee_id = $("#seted_employee_id").val();
  let experience_id = $("#id_employee_experience_id").val();
  let company_name = $("#id_company_name").val();
  let start_date = $("#id_start_date").val();
  let end_date = $("#id_end_date").val();
  let address = $("#id_company_address").val();
  let company_type = $("#id_company_type").val();
  let position = $("#id_position").val();
  let department = $("#id_department").val();
  let responsibility = $("#id_responsibility").val();
  let achievement = $("#id_achievement").val();
  let phone_number = $("#id_phone_number").val();
  let email = $("#id_email").val();
  let contact_person = $("#id_contact_person").val();
  let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  let jsonData = {
    company_name: company_name,
    company_address: address,
    company_type: company_type,
    position: position,
    department: department,
    responsibility: responsibility,
    achievement: achievement,
    phone_number: phone_number,
    email: email,
    contact_person: contact_person,
    start_date: start_date,
    end_date: end_date,
  };
  if (experience_id) {
    $.ajax({
      url: "/apihrm-employeeExperience-edit-api/" + experience_id,
      type: "PUT",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
      data: JSON.stringify(jsonData),
      beforeSend: function () {},
      success: function (data) {
        if (data.success) {
          get_experience_data({ edited: true });
          emptyForm();
        } else {
          alert("Something is wrong!");
        }
      },
    });
  } else {
    if (
      company_name === "" ||
      start_date === "" ||
      end_date === "" ||
      address === ""
    ) {
      return alert("please fill up the form properly");
    }
    jsonData.employee_id = employee_id;

    $.ajax({
      url: "/apihrm-employeeExperience-create-api",
      type: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
      data: JSON.stringify(jsonData),
      beforeSend: function () {},
      success: function (data) {
        get_experience_data({ edited: true });
        emptyForm();
      },
    });

    // data_list_experience.push(jsonData);
    // let template = Handlebars.compile(
    //   document.querySelector("#myTemplate").innerHTML
    // );
    // let filled = template(data_list_experience);
    // document.querySelector("#custom-data-table").innerHTML = filled;
    // emptyForm();
  }
});

function fnDeleteFromList(e) {
  let index = $(e).data("index");
  let selected = data_list_experience.map((e, i) => {
    if (i == index) {
      return e;
    }
  });
  let data = selected[index];
  let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

  $.ajax({
    url: "/apihrm-employeeExperience-edit-api/" + data.experience_id,
    type: "DELETE",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    beforeSend: function () {},
    success: function (data) {
      get_experience_data({ edited: true });
      emptyForm();
    },
  });
  // data_list_experience.splice(index, 1);
  // var template = Handlebars.compile(
  //   document.querySelector("#myTemplate").innerHTML
  // );
  // var filled = template(data_list_experience);
  // document.querySelector("#custom-data-table").innerHTML = filled;
}

function get_experience_data(props = {}) {
  let employee_id = $("#seted_employee_id").val();
  let url = "/apihrm-employeeExperiance-api?employee_id=" + employee_id;
  $.ajax({
    url: url,
    type: "get",
    dataType: "json",
    beforeSend: function () {},
    success: function (data) {
      let json_data = data.map((data) => {
        return {
          experience_id: data.id,
          company_name: data.company_name,
          company_address: data.company_address,
          company_type: data.company_type,
          position: data.position,
          department: data.department,
          responsibility: data.responsibility,
          achievement: data.achievement,
          phone_number: data.phone_number,
          email: data.email,
          contact_person: data.contact_person,
          start_date: data.start_date,
          end_date: data.end_date,
        };
      });
      if (props.edited == true) {
        data_list_experience = [];
        data_list_experience.push(...json_data);
      } else {
        data_list_experience.push(...json_data);
      }
      var template = Handlebars.compile(
        document.querySelector("#myTemplate").innerHTML
      );
      var filled = template(data_list_experience);
      document.querySelector("#custom-data-table").innerHTML = filled;
    },
  });
}

function fnEditFromList(e) {
  let index = $(e).data("index");
  let selected = data_list_experience.map((e, i) => {
    if (i == index) {
      return e;
    }
  });
  let data = selected[index];
  if (data) {
    data_list_experience.splice(index, 1);
    var template = Handlebars.compile(
      document.querySelector("#myTemplate").innerHTML
    );
    var filled = template(data_list_experience);
    document.querySelector("#custom-data-table").innerHTML = filled;
    $("#id_company_name").val(data.company_name);
    $("#id_company_address").val(data.company_address);
    $("#id_company_type").val(data.company_type);
    $("#id_position").val(data.position);
    $("#id_department").val(data.department);
    $("#id_responsibility").val(data.responsibility);
    $("#id_achievement").val(data.achievement);
    $("#id_phone_number").val(data.phone_number);
    $("#id_email").val(data.email);
    $("#id_contact_person").val(data.contact_person);
    $("#id_start_date").val(data.start_date);
    $("#id_end_date").val(data.end_date);
    $("#id_employee_experience_id").val(data.experience_id);
  }
}

$(function () {
  $("#dt-table-list").on("click", "button", function () {
    try {
      const table_row = table_data.row(this).data();
      id = table_row["employee_id"];
    } catch (e) {
      const table_row = table_data.row($(this).parents("tr")).data();
      id = table_row["employee_id"];
    }

    const class_name = $(this).attr("class");
    if (class_name == "btn btn-info btn-sm") {
      show_edit_form(id);
    }
  });

  function show_edit_form(id) {
    $.ajax({
      url: "/hrm-employee-info-edit/" + id,
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#edit_model").modal("show");
      },
      success: function (data) {
        $("#edit_model .modal-content").html(data.html_form);
      },
    });
  }
});

function fn_set_degree_info(id = 0) {
  $.ajax({
    url: "/apiedu-degree-api/",
    success: function (data) {
      let selectop = [`<option>-------</option>`];
      let option = data.map(
        (degree) =>
          `<option value=${degree.degree_name}>${degree.degree_name}</option>`
      );

      if (id) {
        $(`#degree_id${id}`).html([...selectop, ...option]);
      }
    },
  });
}
$("#addnewEdu").click(function () {
  var edu_count = parseInt($("#eduId").val());
  edu_count += 1;
  $("#eduId").val(edu_count);
  $("#id_edu_count").val(edu_count);
  var html_form = `	<div id="eduqationDivId${edu_count}" class="form-row">
                <input type="hidden" readonly id="emp_education_id${edu_count}">
                <div class="form-group col-md-2 mb-0">
                    <div class="p-0 m-0">
                        <div id="div_id_degree_name" class="form-group">
                            <label for="id_degree_name" class=" requiredField">
                                degree Name<span class="asteriskField">*</span>
                            </label>
                                <select name="degree_name${edu_count}"
                                onchange="edit_education(null,null,null,${edu_count})"
                                        class="form-control" id="degree_id${edu_count}">
                                    </select>
                        </div>
                    </div>
                </div>
    
                <div class="form-group col-md-2 mb-0">
                    <div class="p-0 m-0">
                        <div id="div_id_board_name" class="form-group">
        
                            <label for="id_board_name" class="">
                                Board Name
                            </label>
                                <input type="text" name="board_name${edu_count}" maxlength="200" 
                                class="textinput textInput form-control"
                                onchange="edit_education(null,null,null,${edu_count})"
                                    id="board_name${edu_count}">
                        </div>
                    </div>
                </div>

                <div class="form-group col-md-1 mb-0">
                    <div class="p-0 m-0">
                        <div id="div_id_result_point" class="form-group">
                            <label for="id_result_point" class="">
                                 Point
                            </label>	
                                <input type="text" name="result_point" maxlength="100" class="textinput textInput form-control"
																				onchange="edit_education(null,null,null,${edu_count})"
                                    id="result_point${edu_count}">
                        </div>	
                    </div>
                </div>

                <div class="form-group col-md-1 mb-0">
                    <div class="p-0 m-0">	
                        <div id="div_id_result_grate" class="form-group">
                            <label for="id_result_grate" class="">
                                 Grade
                            </label>
                                <input type="text" name="result_grate${edu_count}"
                                 maxlength="100" 
                                class="textinput textInput form-control"
                                onchange="edit_education(null,null,null,${edu_count})"
                                    id="result_grate${edu_count}">
                            </div>
                        </div>	
                    </div>
                
                <div class="form-group col-md-2 mb-0">
                    <div class="p-0 m-0">
                        <div id="div_id_passing_year" class="form-group">
        
                            <label for="id_passing_year" class="">
                                Passing year
                            </label>
                                <input type="text" name="passing_year${edu_count}"
                                onchange="edit_education(null,null,null,${edu_count})"
                                 maxlength="500" 
                                 class="textinput textInput form-control"

                                    id="passing_year${edu_count}">
                        </div>
                    </div>
                </div>
                <div class="form-group col-md-2 mb-0">
                    <div class="p-0 m-0">
                        <div id="div_id_institute_name" class="form-group">
                            <label for="id_institute_name" class="">
                                Institute Name
                            </label>
                                <input type="text" name="institute_name${edu_count}" maxlength="100"
                                onchange="edit_education(null,null,null,${edu_count})"
                                    class="textinput textInput form-control" id="institute_name${edu_count}">
                        </div>
                    </div>
                </div>
                	<div class="form-group col-md-1 mb-0">
                    <div class="p-0 mt-4 mb-4">
                        <div id="div_id_delete_button" class="form-group">
                        <label for="id_institute_name" class=""></label>
                            <button class="btn btn-danger" style="margin: 0px 5px;" type="button"
                                onclick="delete_form(this.parentElement.parentElement.parentElement,${edu_count},{edu_id:null,edu_count:${edu_count}})"><i class="fa fa-trash"></i></button>
                        </div>
                    </div>
                </div>
        </div>`;
  $("#education_qualification").append(html_form);
  //   $("#Edu-qualification select").select2();
  fn_set_degree_info(edu_count);
});
function delete_form(row, id, props) {
  console.log(props.edu_count);
  console.log(props.edu_id);
  let edu_id = props.edu_id;
  let edu_count = props.edu_count;
  try {
    if (edu_count) {
      let emp_education_id = $(`#emp_education_id${edu_count}`).val();
      deleteEducationAjax(emp_education_id);
    } else {
      deleteEducationAjax(edu_id);
    }
    $(`#eduqationDivId${id}`).remove();
    var button_number = $(row);
    button_number.find("input").val("");
    button_number.find("select").val("");
    button_number.addClass("d-none");
  } catch (e) {}
}

// Crop and image upload

var $modal = $("#image_model");
var image = document.getElementById("pro_image");
var cropper;
var canvas;
var url;
$("#profile-image").on("change", function (e) {
  var files = e.target.files;
  var done = function (url) {
    image.src = url;
    $modal.modal("show");
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
$modal
  .on("shown.bs.modal", function () {
    cropper = new Cropper(image, {
      aspectRatio: 1,
      viewMode: 3,
      preview: ".preview",
    });
  })
  .on("hidden.bs.modal", function () {
    cropper.destroy();
    cropper = null;
  });
$("#crop").click(function () {
  canvas = cropper.getCroppedCanvas({
    width: 600,
    height: 600,
  });
  canvas.toBlob(function (blob) {
    url = URL.createObjectURL(blob);
    var reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function () {
      var base64data = reader.result;
      $.ajax({
        type: "POST",
        dataType: "json",
        url: "/hrm-employee-profile-image-temp",
        data: { image: base64data },
        success: function (data) {
          $("#profile-photo").attr("src", base64data);
          $modal.modal("hide");
          imageUpdate();
        },
      });
    };
  });
});

//student signature upload

var $singModal = $("#sing_model");
var sing_image = document.getElementById("sing_image");
var cropper_sing;
$("#profile-signatur").on("change", function (e) {
  var files = e.target.files;
  var done = function (url) {
    sing_image.src = url;
    $singModal.modal("show");
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
$singModal
  .on("shown.bs.modal", function () {
    cropper_sing = new Cropper(sing_image, {
      aspectRatio: 3 / 1,
      viewMode: 1,
      preview: ".singPreview",
    });
  })
  .on("hidden.bs.modal", function () {
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
      $.ajax({
        type: "POST",
        dataType: "json",
        url: "/hrm-employee-signature-image-temp",
        data: { signature: base64data },
        success: function (data) {
          $("#profile-sign").attr("src", base64data);
          $singModal.modal("hide");
          imageUpdate();
        },
      });
    };
  });
});

function imageUpdate() {
  let employee_id = $("#seted_employee_id").val();
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/hrm-employee-info-edit-image/" + employee_id,
    data: {},
    success: function (data) {
      if (data.form_is_valid) alert("Edited Image successfully uploaded");
    },
  });
}

function edit_education(employee_id, edu_id, serial_no, edu_count = null) {
  console.log(employee_id, edu_id, serial_no, edu_count);
  let degree_name = document.getElementById(
    "degree_id" + (edu_id != null ? edu_id : edu_count)
  ).value;
  let board_name = document.getElementById(
    "board_name" + (edu_id != null ? edu_id : edu_count)
  ).value;
  let result_point = document.getElementById(
    "result_point" + (edu_id != null ? edu_id : edu_count)
  ).value;
  let result_grate = document.getElementById(
    "result_grate" + (edu_id != null ? edu_id : edu_count)
  ).value;
  let passing_year = document.getElementById(
    "passing_year" + (edu_id != null ? edu_id : edu_count)
  ).value;
  let institute_name = document.getElementById(
    "institute_name" + (edu_id != null ? edu_id : edu_count)
  ).value;
  let jsonData = {
    degree_name: degree_name,
    board_name: board_name,
    result_point: result_point,
    result_grate: result_grate,
    passing_year: passing_year,
    institute_name: institute_name,
  };
  if (edu_id) {
    console.log(jsonData);

    updateEducationAjax(edu_id, jsonData);
  } else {
    let employee_id = $("#seted_employee_id").val();
    jsonData.employee_id = employee_id;
    if (edu_count) {
      let emp_education_id = $(`#emp_education_id${edu_count}`).val();
      if (emp_education_id) {
        updateEducationAjax(emp_education_id, jsonData);
        console.log(edu_count, jsonData);
      } else {
        createEducationAjax(edu_count, jsonData);
        console.log(edu_count, jsonData);
      }
    }
  }
}
$("#id_is_teacher").on("click", function () {
  let checked = $("#id_is_teacher").prop("checked");
  console.log(checked);
  if (checked) {
    $("#id_is_teacher").val("A");
  } else {
    $("#id_is_teacher").val("I");
  }
});

function updateEducationAjax(edu_id, jsonData) {
  let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
    url: "/apihrm-employeeEducation-edit-delete-api/" + edu_id,
    type: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    data: JSON.stringify(jsonData),
    beforeSend: function () {},
    success: function (data) {
      console.log(data);
    },
  });
}

function deleteEducationAjax(edu_id) {
  let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
    url: "/apihrm-employeeEducation-edit-delete-api/" + edu_id,
    type: "DELETE",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    beforeSend: function () {},
    success: function (data) {
      console.log(data);
    },
  });
}

function createEducationAjax(edu_count, jsonData) {
  let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
    url: "/apihrm-employeeEducation-create-api",
    type: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    data: JSON.stringify(jsonData),
    beforeSend: function () {},
    success: function (data) {
      console.log(data.id);
      $(`#emp_education_id${edu_count}`).val(data.id);
    },
  });
}
