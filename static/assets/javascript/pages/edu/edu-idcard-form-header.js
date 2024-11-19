$(document).ready(function() {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function() {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    console.log(global_branch_code)
    $('#id_branch_code').val(global_branch_code).trigger('change');
});

function show_logo_input() {
    document.getElementById('ap_logo').style.display = 'none';
    let form_row = document.getElementById('ap_input_form');
    let html = '<div class="form-group col-md-3 mb-0">\
       <label>Logo</label>\
       <input type="file" name="logo" class="form-control">\
       </div>'
    form_row.innerHTML += html
}