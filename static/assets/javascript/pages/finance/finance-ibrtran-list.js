"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var id

var fn_data_table =

  function () {
    function fn_data_table() {
      _classCallCheck(this, fn_data_table);

      this.init();
    }

    _createClass(fn_data_table, [{
      key: "init",
      value: function init() {
        this.table = this.table();
      }
    }, {
      key: "table",
      value: function table() {
        var branch_code = document.getElementById('id_branch_code').value;
        var from_date = document.getElementById('id_from_date').value;
        var upto_date = document.getElementById('id_upto_date').value;
        var tran_status = document.getElementById('id_tran_status').value;
        var search_url = "/apifinance-ibrtran-api/?branch_code=" + branch_code + "&from_date=" + from_date + "&upto_date=" + upto_date + "&tran_status=" + tran_status;
        table_data = $('#dt-table-list').DataTable({
          "processing": true,
          destroy: true,
          "ajax": {
            "url": search_url,
            "type": "GET",
            "dataSrc": ""
          },
          responsive: true,
          dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n        <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
          language: {
            paginate: {
              previous: '<i class="fa fa-lg fa-angle-left"></i>',
              next: '<i class="fa fa-lg fa-angle-right"></i>'
            }
          },
          columns: [
            { data: 'org_branch_code' },
            { data: 'res_branch_code' },
            { data: 'transaction_id' },
            { data: 'transaction_date' },
            { data: 'tran_amount' },
            { data: 'tran_status' },
            { data: 'app_user_id' },
            { data: 'auth_by' },
            { data: 'cancel_by' },
            { data: 'cancel_remarks' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-info btn-sm">Approve</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-danger btn-sm">Reject</button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

$(function () {
  $('#btnSearch').click(function () {

    var branch_code = document.getElementById('id_branch_code').value;
    var from_date = document.getElementById('id_from_date').value;
    var upto_date = document.getElementById('id_upto_date').value;
    var tran_status = document.getElementById('id_tran_status').value;
    if (branch_code === "" & from_date === "" & upto_date === "" & tran_status === "") {
      alert("Please Enter Branch Code/Date/Transaction Status!")
    } else {
      new fn_data_table();
    }
  });
})

$(document).ready(function () {
  refresh_branch_list('');
});

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

$(function () {

  $('#dt-table-list').on('click', 'button', function () {

    try {
      var table_row = table_data.row(this).data();
      id = table_row['transaction_id'];
    }
    catch (e) {
      var table_row = table_data.row($(this).parents('tr')).data();
      id = table_row['transaction_id'];
    }

    var class_name = $(this).attr('class');

    if (class_name == 'btn btn-info btn-sm') {
      authorize_ibr_transaction(id);
    }

    if (class_name == 'btn btn-danger btn-sm') {
      reject_ibr_transaction(id);
    }

  })

  function reject_ibr_transaction(id) {
    if (confirm('Are you sure you want to reject this transaction?') == true) {
      $('#page_loading').modal('show');
      $.ajax({
        url: "/finance-ibrtran-reject/" + id,
        type: "POST",
        success: function (data) {
          if (data.form_is_valid) {
            $('#page_loading').modal('hide');
            if(data.success_message){
              Swal.fire({
                  position: 'center',
                  icon: 'success',
                  title: data.success_message,
                  showConfirmButton: false,
                  timer: 1500
              })
          };
            table_data.ajax.reload();
          } else {
            $('#page_loading').modal('hide');
            if(data.error_message){
              Swal.fire({
                  position: 'center',
                  icon: 'error',
                  title: data.error_message,
                  showConfirmButton: true,
                  })
              };
            table_data.ajax.reload();
          }
        }
      })
    }
  }

  function authorize_ibr_transaction(id) {
    $('#page_loading').modal('show');
    $.ajax({
      url: "/finance-ibrtran-auth/" + id,
      type: "POST",
      success: function (data) {
        if (data.form_is_valid) {
          $('#page_loading').modal('hide');
          alert(data.success_message);
          table_data.ajax.reload();
        } else {
          $('#page_loading').modal('hide');
          alert(data.error_message)
          table_data.ajax.reload();
        }
      }
    })
  }

})