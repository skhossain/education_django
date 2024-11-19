$(function() {
    $('#btnSubmit').click(function() {
        post_edit_form_data();
    });
});

function post_edit_form_data() {
    const data_string = $("#edit_form").serialize();
    console.log(data_string);
    const data_url = $("#edit_form").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            if (data.form_is_valid) {
                $("#page_loading").modal("hide");
                $("#edit_model").modal("hide");
                Swal.fire({
                    position: "top-center",
                    icon: "success",
                    title: data.success_message,
                    showConfirmButton: false,
                    timer: 1500,
                });
                table_data.ajax.reload();
            } else {
                $('#page_loading').modal('hide');
                if (data.error_message) {
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