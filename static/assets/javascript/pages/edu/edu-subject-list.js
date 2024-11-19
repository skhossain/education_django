
$('#id_class_id').change(function() {
    filtering_grouplist()
})

    function filtering_grouplist() {
        let class_id = document.getElementById('id_class_id').value

        $.ajax({
            url: "apiedu-academicgroup-api/?class_id=" + class_id,
            type: 'get',
            datatype: 'json',
            success: function(data) {
                $("#id_class_group_id option").remove();
                $("#id_class_group_id").append('<option value="">------------</option>');
                data.forEach(element => {
                    $("#id_class_group_id").append('<option value="' + element.class_group_id + '">' + element.class_group_name + '</option>')
                });
                console.log(data)
            }
        })
    }

    function view_subjectList() {
        const data_url = $("#tran_table_data").attr("data-url");
        let class_id = $('#id_class_id').val();
        let class_group_id = $('#id_class_group_id').val();
        let url = data_url + '?class_id=' + class_id + '&class_group_id=' + class_group_id
        window.open(url, "_blank");
    }


    //Select2
    $(document).ready(function() {
        $('#id_class_id').select2({ placeholder: " Select a class " });
        $('#id_class_group_id').select2({ placeholder: " Select a group " });
    })
