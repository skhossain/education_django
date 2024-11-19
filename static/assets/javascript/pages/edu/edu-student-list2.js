"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) {
    for (let i = 0; i < props.length; i++) {
        let descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }
var global_branch_code = ""
$(window).on('load', function() {
    global_branch_code = document.getElementById('id_global_branch_code').value;
});
let table_data

const fn_data_table =
    function() {
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
                let academic_year = document.getElementById('id_academic_year').value
                let class_id = document.getElementById('id_class_id').value
                let class_roll = document.getElementById('id_class_roll').value
                let class_group_id = document.getElementById('id_class_group_id').value
                let student_roll = document.getElementById('id_student_roll').value
                let catagory_id = document.getElementById('id_catagory_id').value
                let student_phone = document.getElementById('id_student_phone').value
                let branch_code = document.getElementById('id_branch_code').value
                const search_url = "apiedu-studentinfo-api/?academic_year=" + academic_year + "&class_id=" + class_id + "&class_roll=" + class_roll + "&class_group_id=" + class_group_id + "&student_roll=" + student_roll + "&catagory_id=" + catagory_id + "&student_phone=" + student_phone + "&branch_code=" + branch_code;


                table_data = $('#dt-table-list').DataTable({
                    "serverSide": true,
                    destroy: true,
                    // "iDisplayLength": 85,
                    "paging": true,
                    'ordering': true,
                    'searchinng': true,

                    "ajax": {
                        "processing": true,
                        url: search_url,
                        type: 'GET',
                        data: function(data) {
                            data.page = data.draw;
                            // delete data.draw;
                            data.limit = data.length;
                            data.page_size = data.limit;
                            // delete data.length;
                            data.search = data.search.value;
                            // console.log(data.search, '--------')
                            data.offset = data.start;
                            // delete data.start;
                            return data;
                        },
                        dataFilter: function(data) {
                            var json = jQuery.parseJSON(data);
                            json.recordsTotal = json.count;
                            json.recordsFiltered = json.count;
                            json.data = json.results;
                            delete json.results;
                            return JSON.stringify(json); // return JSON string
                        },
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n        <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",


                    columns: [
                        { data: 'student_roll' },
                        { data: 'student_name' },
                        { data: 'student_father_name' },
                        { data: 'class_id.class_name' },
                        { data: 'student_date_of_birth' },
                        { data: 'student_phone' },
                        {
                            "data": 'student_roll',
                            "render": function (data, type, row, meta) {
                                data = `
                                <a class="testi btn btn-info btn-sm" href="/edu-create-testimonial/${row.student_roll}/${row.branch_code}">Testimonial</a> 
                                <button type="button" class="tc btn btn-info btn-sm d-none">TC</button>
                                `;
                                return data;
                            }
                        }
                    ],
                    columnDefs: [{
                        "defaultContent": "-",
                        "targets": "_all"
                    }],
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

$('#btnSearch').click(

    function() {
        let academic_year = document.getElementById('id_academic_year').value
        if (academic_year.length) {
            new fn_data_table();
        } else {
            Swal.fire({
                position: 'top-center',
                icon: 'error',
                title: 'Academic Year must select!',
                showConfirmButton: false,
                timer: 1800
            })
        }
    }

);

$(function() {

    $('#dt-table-list').on('click', 'button', function() {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['student_roll']
        } catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['student_roll']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
        if (class_name == 'print btn btn-info btn-sm') {
            print_all_info(id);
        }
        
        if (class_name == 'tc btn btn-info btn-sm') {
            print_tc(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/edu-studentinfo-list-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function() {
                $('#edit_model').modal('show');
            },
            success: function(data) {
                console.log(data.status, '-----------')
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }

});


function print_all_info(id) {
    var branch_code = document.getElementById('id_branch_code').value
    var academic_year = document.getElementById('id_academic_year').value
    var class_id = document.getElementById('id_class_id').value
    var student_roll = document.getElementById('id_student_roll').value

    var postdata = {
        branch_code: branch_code,
        academic_year: academic_year,
        class_id: class_id,
        student_roll: student_roll,
    }
    $.ajax({
        url: 'edu-studentinfo-print/' + id,
        data: postdata,
        type: 'get',
        datatype: 'json',
        beforeSend: function() {
            $('#edit_model').modal('show');
        },
        success: function (data) {
            $('#edit_model .modal-content').html("");
            $('#edit_model .modal-content').html(data);
        }
    })
}

function print_tc(id) {
    $.ajax({
        url: 'edu-student-tc/' + id,
        datatype: 'json',
        beforeSend: function() {
            $('#edit_model').modal('show');
        },
        success: function(data) {
            $('#edit_model .modal-content').html("");
            $('#edit_model .modal-content').html(data);
        }
    })
}


$('#id_class_id').change(function() {
    class_group_filter()
})

function class_group_filter() {
    var class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function(data) {
            $("#id_class_group_id option").remove();
            $("#id_class_group_id").append('<option value="">----------</option>');
            data.forEach(element => {
                $("#id_class_group_id").append('<option value="' + element.class_group_id + '">' + element.class_group_name + '</option>');
            });
        }
    })
}


$(document).ready(() => {
    // Select 2 
    $('select').select2()
})