function show_logo_input(){
     document.getElementById('ap_logo').style.display='none';
     let form_row=document.getElementById('ap_input_form');
     let html='<div class="form-group col-md-3 mb-0">\
        <label>Logo</label>\
        <input type="file" name="academic_logo" class="form-control">\
        </div>'
     form_row.innerHTML+=html
}
function show_banner_input(){
   document.getElementById('ap_banner').style.display='none';
     let form_row=document.getElementById('ap_input_form');
     let html='<div class="form-group col-md-3 mb-0">\
        <label>Website Banner</label>\
        <input type="file" name="web_header_banner" class="form-control">\
        </div>'
     form_row.innerHTML+=html
}