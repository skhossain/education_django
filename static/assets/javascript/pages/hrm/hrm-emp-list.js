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
        let employee_id = '';
          let employee_ids = $("#id_employee_id").val();
        if (employee_ids && employee_ids !== "-------") {
          employee_id=employee_ids
        }
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
            {
              data: "profile_image",
              render: function (data) {
                return (
                  '<img src="' +
                  data +
                  '" class="avatar" width="50" height="50"/>'
                );
              },
            },

            { data: "employee_name" },
            { data: "employee_father_name" },
            { data: "employee_mother_name" },
            { data: "employee_blood_group" },
            { data: "employee_sex" },
            { data: "employee_religion" },
            { data: "employee_marital_status" },
            { data: "employee_national_id" },
            { data: "country_id.country_name" },
            { data: "division_id.division_name" },
            { data: "district_id.district_name" },
            { data: "upozila_id.upozila_name" },
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
            // { data: "emptype_id" },
            { data: "salscale.salscale_name" },
            { data: "designation_id" },
            { data: "email_official" },
            { data: "reporting_to" },
            { data: "current_shift.shift_name" },
            { data: "office_location.office_name" },
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
            // {
            //   data: "employee_signature",
            //   render: function (data) {
            //     return (
            //       '<img src="' +
            //       data +
            //       '" class="avatar" width="50" height="50"/>'
            //     );
            //   },
            // },
  {
                            "data": 'employee_id',
                            "render": function(data, type, row, meta){
                                data =
                                  '<a class="btn btn-info btn-sm" href="/hrm-employee-list-edit/' +
                                  data +
                                  '" target="_blank">Edit</a>';
                                return data;
                             }
                        }
         
          ],
          columnDefs: [{
            "defaultContent": "-",
            "targets": "_all"
        }],
        });
      },
    },
  ]);

  return fn_data_table;
})();

let id = 0;

$("#btnSearch").click(function () {
  console.log();

    new fn_data_table();

});

$(document).ready(function () {
  $("#id_employee_id").select2()
    fn_set_emp_info();
  
});


const emptyForm = ()=>{
       $("#id_company_name").val("")
      $("#id_company_address").val("")
   $("#id_company_type").val("")
    $("#id_position").val("")
    $("#id_department").val("")
      $("#id_responsibility").val("")
      $("#id_achievement").val("")
      $("#id_phone_number").val("")
    $("id_#email").val("")
      $("#id_contact_person").val("")
   $("#id_start_date").val("")
     $("#id_end_date").val("")
}

var data_list_experience = []
$("#experinceListAdd").click(function () {
  let company_name = $("#id_company_name").val();
  let start_date = $("#id_start_date").val();
  let end_date = $("#id_end_date").val();
  let address = $("#id_company_address").val()
  if (
    company_name === "" ||
    start_date === "" ||
    end_date === "" ||
    address === ""
  ) {
    return alert("please fill up the form properly");
  }
  // var count+1;
  let jsonData = {
    company_name: company_name,
    company_address: address,
    company_type: $("#id_company_type").val(),
    position: $("#id_position").val(),
    department: $("#id_department").val(),
    responsibility: $("#id_responsibility").val(),
    achievement: $("#id_achievement").val(),
    phone_number: $("#id_phone_number").val(),
    email: $("id_#email").val(),
    contact_person: $("#id_contact_person").val(),
    start_date: start_date,
    end_date: end_date,
  };
  data_list_experience.push(jsonData);
  let template = Handlebars.compile(document.querySelector("#myTemplate").innerHTML);
  let filled = template(data_list_experience);
  document.querySelector("#custom-data-table").innerHTML=filled;
emptyForm()
});

function fnDeleteFromList (e) {
  let index = $(e).data("index");
  data_list_experience.splice(index, 1);
  var template = Handlebars.compile(
    document.querySelector("#myTemplate").innerHTML
  );
  var filled = template(data_list_experience);
  document.querySelector("#custom-data-table").innerHTML = filled;
  
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
    if (class_name == "btn btn-danger btn-sm") {
      show_image_edit_form(id);
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
  function show_image_edit_form (id) {
    $("#image_edit_model").modal("show");
    $("#id_emp_id").val(id);
    // $.ajax({
    //   url: "/hrm-employee-info-edit/" + id,
    //   type: "get",
    //   dataType: "json",
    //   beforeSend: function () {
    //     $("#edit_model").modal("show");
    //   },
    //   success: function (data) {
    //     $("#edit_model .modal-content").html(data.html_form);
    //   },
    // });
  }
});

function fn_set_emp_info(id=0) {
  $.ajax({
    url: "apihrm-employee-api",
    success: function (data) {
      let selectop = [`<option>-------</option>`];
      let option = data.map(
        (emp) =>
          `<option value=${emp.employee_id}>${emp.employee_name}</option>`
      );
     

      if (id) {
        $(`#id_employee_id${id}`).html([...selectop, ...option]);
      } else {
        $("#id_employee_id").html([...selectop, ...option]);
      }
    },
  });
}



// Crop and image upload

var $modal = $('#image_model');
var image = document.getElementById('pro_image');
var cropper;
var canvas;
var url
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
                console.log(data);
                $("#profile-photo").attr("src", base64data);
                $modal.modal("hide");
                alert("Crop image successfully uploaded");
              },
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
            $.ajax({
              type: "POST",
              dataType: "json",
              url: "/hrm-employee-signature-image-temp",
              data: { signature: base64data },
              success: function (data) {
                $("#profile-sign").attr("src", base64data);
                $singModal.modal("hide");
                alert("Crop signature successfully uploaded");
              },
            });
        }
    });
})


$("#btnAddRecord").click(function () {
  post_tran_table_data();
});

function post_tran_table_data() {
  const emp_id = $("#id_emp_id").val();
  $("#page_loading").modal("show");
  $.ajax({
    url: "hrm-employee-info-edit-image/" + emp_id,
    data: {},
    type: "POST",
    dataType: "json",
    success: function (data) {
      if (data.form_is_valid) {
        $("#page_loading").modal("hide");
    $("#image_edit_model").modal("hide");

        // document.getElementById("stepper-form").reset();
        table_data.ajax.reload();
        alert(data.success_message + " " + data.id);
      } else {
        $("#page_loading").modal("hide");
        alert(data.error_message);
      }
    },
  });
  return false;
}
