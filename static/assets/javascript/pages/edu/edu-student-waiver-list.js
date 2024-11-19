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
                
                let student_roll = document.getElementById('id_student_roll').value
                let fees_month = document.getElementById('id_fees_month').value
                let fees_year = document.getElementById('id_fees_year').value
                let branch_code = document.getElementById('id_branch_code').value
                let effective_date = document.getElementById('id_effective_date').value
                let head_code = document.getElementById('id_head_code').value
                const search_url = "apiedu-feeswaiverstudent-api/?fees_month=" + fees_month + "&fees_year=" + fees_year + "&effective_date=" + effective_date + "&head_code=" + head_code + "&student_roll=" + student_roll + "&branch_code=" + branch_code;


                table_data = $('#dt-table-list').DataTable({
                    ajax: {
                        url: search_url,
                        dataSrc: ''
                    },
                    columns: [
                        { data: 'student_roll.student_roll' },
                        { data: 'student_roll.student_name' },
                        {
                            data: 'head_code',
                            render: function (data, type, row) {
                                let head_data = find_fees_head(data)
                                return head_data.head_name;
                            }
                        },
                        { data: 'effective_date' },
                        { data: 'fee_amount' },
                        { data: 'waive_amount' },
                        { data: 'waive_percentage' },
                        {
                            data: 'fees_month',
                            render: function (data, type, row) {
                                let month_name = moment(data, 'M').format('MMM')
                                return month_name + " " + row.fees_year;
                            }
                            
                        },
                        
                        { data: 'cancel_by' },
                        {
                        data: 'cancel_by',
                            render: function (data, type, row) {
                                let html = ""
                                if (row.cancel_by == null) {
                                    html +='<button type="button" class="btn btn-danger btn-sm">Cancel</button>'
                                }
                                return html;
                        }
                        }                        
                    ],
                    columnDefs: [{
                        "defaultContent": "-",
                        "targets": "_all"
                    }],
                    "createdRow": function (row, data, dataIndex) {
                       
                        if ( data.cancel_by != null ) {
                        $(row).addClass( 'table-danger' );
                        }
                    }
                });
            }
        }]);
        return fn_data_table;
    }();

let id = 0

$('#btnSearch').click(
    function () {
    $("#dt-table-list").DataTable().clear().destroy();
       new fn_data_table();
    }

);

$(function() {

    $('#dt-table-list').on('click', 'button', function() {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['id']
        } catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-danger btn-sm') {
            cancle_waiver(id);
        }
        
    })

    function cancle_waiver(id) {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, cancel it!'
            }).then((result) => {
                if (result.isConfirmed) {
                $.ajax({
                    url: '/edu-feeswaivestudent-edit/' + id,
                    type: 'post',
                    dataType: 'json',
                    success: function (data) {
                        $("#dt-table-list").DataTable().clear().destroy();
                        new fn_data_table();
                        Swal.fire(
                        'Cancel!',
                        'Cancel Success.',
                        'success'
                        )
                    }
        })

                
            }
            })
        
    }

});

let fees_heads = ""
function get_fees_heads() {
    $.ajax({
        url: '/apiedu-feesheadsetting-api',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            fees_heads = data;
        }
    })

}
get_fees_heads();

function find_fees_head(head_code){
    let fees_head = fees_heads.find(fh => fh.head_code == head_code);
    return fees_head;
}

$(document).ready(() => {
    // Select 2 
    $('select').select2()
})