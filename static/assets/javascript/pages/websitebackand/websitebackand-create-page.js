$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
    show_massage();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function show_massage() {
    var status = $('#create_status').val();
    var mass = $('#massage').val();
    if (mass) {
        Swal.fire({
            position: 'top-center',
            icon: status=='True'?'success':'error',
            title: mass,
            showConfirmButton: status == 'True' ? false : true,
            timer: status == 'True' ? 1500 : 5000
        })
    }
}
