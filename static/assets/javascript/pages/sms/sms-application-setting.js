$(document).ready(function () {
    set_value()
  });

    function set_value() {
        $.ajax({
            url: '/apisms-application-setting-api/',
            type: 'get',
            dataType: 'json',
            
            success: function (data) {
                console.log(data)
                $('#id_messaging_auth_url').val(data[0].messaging_auth_url);
                $('#id_messaging_url').val(data[0].messaging_url);
                $('#id_messaging_username').val(data[0].messaging_username);
                $('#id_messaging_password').val(data[0].messaging_password);
                $('#id_total_message_limit').val(data[0].total_message_limit);
                if(data[0].is_messaging_on){
                    $('#id_is_messaging_on').prop("checked",true);

                }
                $('#id_total_message_sent').val(data[0].total_message_sent);
                $('#id_senderid').val(data[0].senderid);
                $('#id_api_key').val(data[0].api_key);
                $('#id_is_headers_require').val(data[0].is_headers_require);
                $('#id_messaging_error').val(data[0].messaging_error);
            }
        })
    }


    function saved_data() {
        var data_string = $("#tran_table_data").serialize();
        var data_url = $("#tran_table_data").attr('data-url');
        console.log(data_url)
        $('#page_loading').modal('show');
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    document.getElementById("tran_table_data").reset();
                    $('#page_loading').modal('hide');
                    alert(data.success_message);
                    set_value()
                } else {
                    $('#page_loading').modal('hide');
                    set_value()
                    alert(data.error_message);

                }
            }
        })
        return false;
    }