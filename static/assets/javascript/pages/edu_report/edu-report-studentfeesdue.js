$(function () {
	$('#btnSubmit').click(function () {
		save_and_show_report();
	});
});

function save_and_show_report() {
	var data_url = $("#report_data").attr('data-url');
	var report_data = {
		'p_branch_code': $('#id_branch_code').val(), 'p_student_roll': $('#id_student_roll').val(),
		'p_from_date': $('#id_from_date').val(), 'p_upto_date': $('#id_upto_date').val(),
		'p_class_id': $('#id_class_id').val(), 'p_class_group_id': $('#id_class_group_id').val(),
		'p_section_id': $('#id_section_id').val(), 'p_fees_head_code': $('#id_head_code').val(),
	};
	var report_url = $('#report_url').val();
	report_data = JSON.stringify(report_data);
	$('#page_loading').modal('show');
	$.ajax({
		url: data_url,
		data: {
			'report_name': $('#report_name').val(),
			"report_data": report_data
		},
		cache: "false",
		type: 'POST',
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				$('#page_loading').modal('hide');
				window.open(data.report_urls + "/" + report_url, "_blank");
			}
			else {
				$('#page_loading').modal('hide');
				if (data.error_message) {
					Swal.fire({
						position: 'center',
						icon: 'error',
						title: data.error_message,
						showConfirmButton: true,
					})
				};
			}
		}
	})
	return false;
}

let report_screen = 'STUDENTS_FEES_DUE';

$(document).ready(function () {
	$("#id_report_list").select2();
	$("#id_branch_code").select2();
	$("#id_class_id").select2();
	$("#id_class_group_id").select2();
	$("#id_section_id").select2();
	$("#id_head_code").select2();
	refresh_branch_list('');
	refresh_report_list(report_screen);
	edu_choice_classlist('');
	edu_choice_classgrouplist('');
	edu_choice_subjectlist('');
	edu_choice_feesheadlist('');
	edu_choice_sectionlist('');
});


$(window).on('load', function () {
	var global_branch_code = document.getElementById('id_global_branch_code').value;
	$('#id_branch_code').val(global_branch_code);
});

function refresh_branch_list(branch_code) {
	var url = '/finance-choice-branchlist';
	$.ajax({
		url: url,
		data: {
			'branch_code': branch_code
		},
		success: function (data) {
			$("#id_branch_code").html(data);
		}
	});
	return false;
}


$("#id_report_list").on("change", function () {
	var report_id = document.getElementById('id_report_list').value;
	set_report_url(report_id, report_screen);
});


$("#id_class_id").on("change", function () {
	var class_id = document.getElementById('id_class_id').value;
	edu_choice_classgrouplist(class_id);
	edu_choice_sectionlist(class_id);
});


$("#id_class_group_id").on("change", function () {
	var class_group_id = document.getElementById('id_class_group_id').value;
	edu_choice_classgrouplist(class_group_id);
});