$('#disapprove').click( function(){
	console.log("disapprove")
   });
   
$('#btnSubmit').click( function(){
	console.log("approve")
	  });

$(function () {
	$('#btnSubmit').click(function () {
		let approve=true;
		
		post_edit_form_data(approve);
		
	});
});


$(function () {
	$('#disapprove').click(function () {
		let approve=false;
		
		post_edit_form_data(approve);
		
	});
});




function post_edit_form_data(approve) {
	let data_string = $("#edit_form").serialize();
	data_string = data_string+"&approve="+approve.toString()
	console.log(data_string)
	const data_url = $("#edit_form").attr('data-url');
	console.log("hello test");
	$('#page_loading').modal('show');
	$.ajax({
		url: data_url,
		data: data_string,
		type: 'POST',
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				$('#page_loading').modal('hide');
				$('#edit_model').modal('hide');
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


