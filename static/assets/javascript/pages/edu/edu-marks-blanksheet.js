$(document).ready(function () {
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$(document).ready(function () {
    $('select').select2();
});


let academic_info = ""


$('#PDFCreate').click(function () {
    let branch_code = $('#id_branch_code').val()
    let class_id = $('#id_class_id').val()
    let class_group_id = $('#id_class_group_id').val()
    let academic_year = $('#id_academic_year').val()
    let shift_id = $('#id_shift_id').val()
    let section_id = $('#id_section_id').val()
    var pdf = new jsPDF('p', 'mm', 'a4');
    let page_counter=0;
    let data_string={
        branch_code: branch_code,
        class_id:class_id,
        class_group_id: class_group_id,
        academic_year:academic_year,
        shift_id:shift_id,
        section_id:section_id,
    }
    $.ajax({
        url: 'apiedu-admission-form-header-api/?branch_code=' + branch_code,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            academic_info = data[0]
            console.log(academic_info)
        }
    })
    $.ajax({
        url: '/apiedu-studentinfo-api/',
        data: data_string,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // $('#page_create').modal('show')
            // $('#page_create_count').text(page_counter)
            if (data.length) {
                pdf.setFontStyle('bold')
                pdf.text(academic_info.academic_name.toUpperCase(), 105, 20, { align: 'center' })
                pdf.setFontStyle('normal')
                pdf.setFontSize(9)
                pdf.text(academic_info.text_one, 105, 24, { align: 'center' })
                pdf.text(academic_info.text_two, 105, 27, { align: 'center' })
                pdf.text(academic_info.text_three, 105, 30, { align: 'center' })
                pdf.text(academic_info.text_four, 105, 33, { align: 'center' })
                pdf.text(academic_info.text_five, 105, 36, { align: 'center' })
                pdf.setFontSize(12)
                pdf.setFontStyle('bold')
                pdf.text("Exam Name: ", 50, 42)
                pdf.line(10, 46, 200, 46, "S")
                pdf.setFontStyle('normal')
                pdf.setFontSize(9)
                pdf.text("Class Name: ", 10, 50)
                pdf.text(data[0].class_id ? data[0].class_id.class_name:"", 30, 50)
                pdf.text("Group Name: ", 10, 55)
                pdf.text(data[0].class_group_id ? data[0].class_group_id.class_group_name : "", 32, 55)
                pdf.text("Session: ", 10, 60)
                pdf.text("Year: ", 105, 50)
                pdf.text(academic_year, 115, 50)
                pdf.text("Subject Name: ", 105, 55)

                let x=0;
                let y=0;
                let line_height_y=62
                let text_height_y=67
                let par_page_student_count=0
                for (let i = 0; i<=data.length; i++) {
                    function par_page_info(){
                        pdf.setFontStyle('bold')
                        pdf.line(10,line_height_y+y,200,line_height_y+y,"S")
                        pdf.line(10,line_height_y+y+8,200,line_height_y+y+8,"S")
                        pdf.setFontSize(11)
                        pdf.line(10,line_height_y+y,10,line_height_y+y+8,"S")
                        pdf.text("SL.",12,text_height_y+y)
                        pdf.line(20,line_height_y+y,20,line_height_y+y+8,"S")
                        pdf.text("ID",32,text_height_y+y)
                        pdf.line(50,line_height_y+y,50,line_height_y+y+8,"S")
                        pdf.text("Student's Name",69,text_height_y+y)
                        pdf.line(115,line_height_y+y,115,line_height_y+y+8,"S")
                        pdf.text("CL. Roll",117,text_height_y+y)
                        pdf.line(135,line_height_y+y,135,line_height_y+y+8,"S")
                        pdf.text("WR",140,text_height_y+y)
                        pdf.line(151,line_height_y+y,151,line_height_y+y+8,"S")
                        pdf.text("MCQ",154,text_height_y+y)
                        pdf.line(166,line_height_y+y,166,line_height_y+y+8,"S")
                        pdf.line(183,line_height_y+y,183,line_height_y+y+8,"S")
                        pdf.line(200,line_height_y+y,200,line_height_y+y+8,"S")
                        pdf.setFontStyle('normal')
                        pdf.line(150,280,190,280,"DF")
                        pdf.text("Signature & Date",158,284)
                    }
                    if(data[i]){
                        pdf.line(10,line_height_y+y+8,200,line_height_y+y+8,"S")
                        pdf.line(10,line_height_y+y+16,200,line_height_y+y+16,"S")

                        pdf.setFontSize(11)
                        pdf.setFontStyle('normal')
                        pdf.line(10,line_height_y+y+8,10,line_height_y+y+16,"S")
                        pdf.text((i+1).toString(),12,line_height_y+y+12)
                        pdf.line(20,line_height_y+y+8,20,line_height_y+y+16,"S")
                        pdf.text(data[i].student_roll,22,line_height_y+y+12)
                        pdf.line(50,line_height_y+y+8,50,line_height_y+y+16,"S")
                        pdf.text(data[i].student_name,52,line_height_y+y+12)
                        pdf.line(115,line_height_y+y+8,115,line_height_y+y+16,"S")
                        pdf.text(data[i].class_roll?data[i].class_roll.toString():" ",123,line_height_y+y+12)
                        pdf.line(135,line_height_y+y+8,135,line_height_y+y+16,"S")
                        pdf.line(151,line_height_y+y+8,151,line_height_y+y+16,"S")
                        pdf.line(166,line_height_y+y+8,166,line_height_y+y+16,"S")
                        pdf.line(183,line_height_y+y+8,183,line_height_y+y+16,"S")
                        pdf.line(200,line_height_y+y+8,200,line_height_y+y+16,"S")
                    
                    } //Last if statement

                    
                    if(i==0){
                        par_page_info()
                    }
                    if((i+1) == 23 || (i+1-23)%28 == 0){
                        pdf.addPage()
                        y=0
                        line_height_y=21
                        text_height_y=26
                        par_page_student_count=0
                        page_counter+=1
                        par_page_info()
                    }else{
                        par_page_student_count+=1
                        y=par_page_student_count*8
                    }
                }//for statement
                // $('#page_create').modal('hide')
                pdf.save('Blank Mark Sheet')
                
            }// first if statement
            else{
                Swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: 'There is no data under this category.',
                    showConfirmButton: true,
                    })
            }

        }
    })
})



$(document).ready(function() {
    $('#id_shift_id').select2({placeholder: " Select a Shift "});
    $('#id_class_id').select2({placeholder: " Select a Class "});
    $('#id_academic_year').select2({placeholder: " Select a Year "});
    $('#id_section_id').select2({placeholder: " Select a Section "});
});

$('#id_class_id').change(function () {
    class_group_filter()
    section_filter()
})

function section_filter(){
var class_id=document.getElementById('id_class_id').value
$.ajax({
    url: "apiedu-sectioninfo-api/?class_id="+class_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_section_id option").remove();
        $("#id_section_id").append('<option value="">----------</option>');
        data.forEach(element => {
            $("#id_section_id").append('<option value="'+element.section_id+'">'+element.section_name+'</option>');
        });
    }
})
}


function class_group_filter() {
    let class_id = document.getElementById('id_class_id').value
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id=" + class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $('#id_class_group_id').empty()
            var newOption = new Option('-----------', "", false, false);
            $('#id_class_group_id').append(newOption);
            data.forEach(element => {
                var newOption = new Option(element.class_group_name, element.class_group_id, false, false);
                $('#id_class_group_id').append(newOption).trigger('change');
            });
        }
    })
}