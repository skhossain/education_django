$(document).ready(function () {
    refresh_branch_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_ledger_list('IBR_TRAN', 'IBR', global_branch_code);
    $('#id_res_branch_code').val(global_branch_code);
    $('#id_org_branch_code').val(global_branch_code);
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_res_branch_code').val(global_branch_code);
    $('#id_org_branch_code').val(global_branch_code);
});

function refresh_branch_list(branch_code) {
    var url = 'appauth-choice-branchlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_res_branch_code").html(data);
            $("#id_org_branch_code").html(data);
        }
    });
    return false;
}

function refresh_ledger_list(transaction_screen, tran_type, branch_code) {
    var url = '/finance-choice-cashnbanklist';
    $.ajax({
        url: url,
        data: {
            'tran_screen': transaction_screen, 'tran_type': tran_type, 'branch_code': branch_code
        },
        success: function (data) {
            $("#id_res_gl_code").html(data);
        }
    });
    return false;
}

$("#id_org_branch_code").on("change paste keyup", function () {
    var org_branch_code = document.getElementById('id_org_branch_code').value;
    refresh_ledger_list('IBR_TRAN', 'IBR', org_branch_code);
});

$(function () {

    $(function () {
        $('#btnAddItem').click(function () {
            post_tran_table_data();

        });
    });

    function post_tran_table_data() {
        var data_string = $("#tran_table_data").serialize();
        var data_url = $("#tran_table_data").attr('data-url');
        $('#page_loading').modal('show');
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
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
                    document.getElementById("tran_table_data").reset();
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
        return false;
    }

});

