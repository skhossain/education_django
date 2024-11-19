let ans_count=0;
"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (let i = 0; i < props.length; i++) { let descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

let table_data

const fn_data_table =
    function () {
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
                const search_url = "/apiedu-online-exam-api/";
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": ""
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
                    language: {
                        paginate: {
                            previous: '<i class="fa fa-lg fa-angle-left"></i>',
                            next: '<i class="fa fa-lg fa-angle-right"></i>'
                        }
                    },
                    columns: [
                        { data: 'online_exam_id' },
                        { data: 'exam_name' },
                        { data: 'basic_info' },
                        { data: 'exam_date' },
                        { data: 'exam_start_time' },
                        { data: 'exam_end_time' },
                        { data: 'question_patten' },
                        { data: 'publish_status' },
                        { data: 'total_marks' },
                        {
                            "data": 'online_exam_id',
                            "render": function(data, type, row, meta){
                                data = '<a class="btn btn-info" href="/edu-online-exam-edit/'+data+'" target="_blank">Edit</a>';
                                return data;
                             }
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

let id = 0

$('#btnSearch').click(

    function () {
        //if (branch_code === "") {
        //   alert('Please Enter Branch Code!');
        // } else {
        new fn_data_table();
        //  }
    }

);

tinymce.init({ 
    selector: '.tinymce',
    plugins: 'table link autoresize fullscreen image code imagetools lists insertdatetime',
    menubar: 'file edit insert format table',
    toolbar: 'undo redo | styleselect | bold italic underline | forecolor backcolor | alignleft aligncenter alignright alignjustify | outdent indent numlist bullist table image link insertdatetime code fullscreen',
    images_upload_url: 'filebrowser/',
    file_picker_types: 'image',
    automatic_uploads: false
 });

 setTimeout(() => {
    let ty=$('#id_question_type').val();
    if(ty=='MCQ' || ty=='MCQS'){
        $('#btn-choices').css('display','block');
    }else{
        $('#btn-choices').css('display','none');
    }
 }, 300);

$(".fc").children('input').addClass("form-control");
$(".fc").children('select').addClass("form-control");
$(".fc").children('select').attr("disabled", true);
$('#id_question_type').change(
    function(){
        let ty=$('#id_question_type').val();
        if(ty=='MCQ' || ty=='MCQS'){
            $('#btn-choices').css('display','block');
        }else{
            $('#btn-choices').css('display','none');
        }
        ans_count=0
        $('#answer_input').empty()
        $('#id_answer_count').val(ans_count)
    }
    )

$('#btn-choices').click(
    function (){
        let que_type=$('#id_question_type').val();
        let que_id = $('#id_question_id').val()
        // edu-online-exam-create-mcq-answer-field
        $.ajax({
            url: '/edu-online-exam-create-mcq-answer-field/'+que_id,
            type: 'GET',
            success: function (data) {
                location.reload();
            }
        })
        
    }
)

function ans_change(val,id){
    const data_string ={
        ansChange:'yes',
        value:val,
    }
    const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
        }
    })
}
function rightAns_change(val,id){
    const data_string ={
        ansChange:'no',
        value:val,
    }
    const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
        }
    })
}
function MultiRightAns_change(val,id){
    if ($(val).is(':checked')) {
        const data_string ={
            ansChange:'multiAns',
            value:1,
        }
        const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";    
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                console.log(data)
            }
        })
      }else{
        const data_string ={
            ansChange:'multiAns',
            value:0,
        }
        const data_url = "/edu-online-exam-mcq-answer-edit/"+id+"";    
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                console.log(data)
            }
        })
      }
    
}

function deleteAnswer(ans,id){
    $('#deleteAnswerModal').modal('show')
    $('.deleteAnswerModal').text(ans)
    $('#deleteAnswerConfrimeBtn').attr('data-val',id)
}
function deleteAnswerConfirmed(){
let id= $('#deleteAnswerConfrimeBtn').attr('data-val')
$.ajax({
    url: '/edu-online-exam-answer-delete/'+id,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
        $('#deleteAnswerModal').modal('hide')
        location.reload();
    }
})
}