"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (let i = 0; i < props.length; i++) { let descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

let table_data

const fn_data_table =
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
                let academic_year = $('#id_academic_year').val();
                let class_id = $('#id_class_id').val();
                let road_map_id = $('#id_road_map_id').val();
                let trans_status = $('#id_trans_status').val();
                let to_date = $('#id_to_date').val();
                let from_date = $('#id_from_date').val();
                let student_roll = $('#id_student_roll').val();
                let location_info_id = $('#id_location_info_id').val();
                const search_url = "/apitransport-use-summery-api/?academic_year="+academic_year+"&class_id="+class_id+"&road_map_id="+road_map_id+"&trans_status="+trans_status+"&to_date="+to_date+"&from_date="+from_date+"&student_roll="+student_roll+"&location_info_id="+location_info_id+"";
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": ""
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
                    language: {
                        paginate: {
                            previous: '<i class="fa fa-lg fa-angle-left"></i>',
                            next: '<i class="fa fa-lg fa-angle-right"></i>'
                        }
                    },
                    columns: [
                        { data: 'academic_year.academic_year' },
                        { data: 'class_id.class_name' },
                        { data: 'student_roll.student_name' },
                        { data: 'student_roll.student_roll' },
                        { data: 'road_map_id.road_map_name' },
                        { data: 'location_info_id.location_name' },
                        { data: 'trans_status' },
                        { "data": 'date_time',
                        "render": function(data, type, row, meta){
                                moment.defaultFormat = "DD.MM.YYYY HH:mm";
                                // format the date string with the new defaultFormat then parse
                               let date_f= moment(data).format("DD MMM YY, h:mm A")
                            //    let display_date=moment(date_f, moment.format()).toDate() 
                            return date_f;
                        }
                        },
                       
                        {
                            "data": 'trans_status',
                            "render": function (data, type, row) {
                               let row_date= moment(new Date(row.date_time)).format('YYYY-MM-DD')
                               let today= moment(new Date()).format('YYYY-MM-DD')
                               console.log(today)
                                // console.log(new Date().toISOString())
                                if (data == 'Pickup' && row_date == today) {
                                    return '<button type="button" class="btn btn-success btn-sm">Drop</button>\
                                    <button type="button" class="btn btn-info btn-sm">Edit</button>';
                                }
                                else {
                                    return '<button type="button" class="btn btn-info btn-sm">Edit</button>';
                                }
                        }  
                            
                    }
                    ],
                   
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

$('#btnSearch').click(

    function () {
        //if (branch_code === "") {
        //   alert('Please Enter Branch Code!');
        // } else {
        new fn_data_table();
        //  }
    }

);

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['id']
        }
        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
        if (class_name == 'btn btn-success btn-sm') {
            Quicl_drop(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: 'transport-use-summery-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#edit_model').modal('show');
            },
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }

    function Quicl_drop(id) {
        $.ajax({
            url: 'transport-quick-drop/' + id,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                table_data.ajax.reload();
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
    }
});

$('#btnAddRecord').click(function () {
    post_tran_table_data();
});

function post_tran_table_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                document.getElementById("tran_table_data").reset();
                $('select').val('').trigger('change');
                table_data.ajax.reload();
                alert(data.success_message);
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}



$('select').select2();
