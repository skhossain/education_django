
let academic_info=""
$.ajax({
    url: 'apiedu-academic-info-api/',
    type: 'GET',
    dataType: 'json',
    success: function (data) {
        academic_info=data[0]
    }
})





$('#PDFCreate').click(function () {
    let class_id = $('#id_class_id').val()
    let academic_year_id = $('#id_academic_year').val()
    let class_group_id = $('#id_class_group_id').val()
    let term_id = $('#id_term_id').val()
    var pdf = new jsPDF('p', 'mm', 'a4');
    let page_counter=0;
    if(class_id && academic_year_id && term_id){
       let  data_string={
        class_id:class_id,
        academic_year:academic_year_id,
        class_group_id:class_group_id,
        term_id:term_id,
        }
        $.ajax({
            url: '/apiedu-finalmarks-api/?',
            data: data_string,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.length){
                    pdf.setFontSize(16)
                    pdf.setFontStyle('bold')
                    pdf.text(academic_info.academic_name.toUpperCase(),105,20,{align: 'center'})
                    pdf.setFontSize(10)
                    pdf.text(academic_info.academic_address,105,24,{align: 'center'})
                    pdf.text(academic_info.academic_mobile_1+","+academic_info.academic_mobile_2,105,28,{align: 'center'})
                    
                    pdf.text("Exam Name:"+data[0].term_id.term_name,198,32,{align: 'right'})

                    pdf.line(10,34,200,34,"S")

                    pdf.setFontSize(14)
                    pdf.setFillColor('#C3D6FD') //hexadecimal code just one in single quote
                    pdf.rect(10,35,190,8, 'F') //x,y,Distance,height
                    pdf.setTextColor('black')
                    pdf.text("Student Wise Final Result Sheet",60,40)
    
                    pdf.line(10,44,200,44,"S")
                    pdf.line(10,60,200,60,"S")
    
                    pdf.setFontSize(12)
                    pdf.setTextColor('#17202A')
                    pdf.setFontStyle('bold')
                    pdf.line(10,44,10,60,"S")
                    pdf.text("Academic Year",22,49)
                    pdf.line(60,44,60,60,"S")
                    pdf.text("Class",75,49)
                    pdf.line(100,44,100,60,"S")
                    pdf.text("Group (if any)",110,49)
                    pdf.line(150,44,150,60,"S")
                    pdf.text("Total Students",162,49)
                    pdf.line(200,44,200,60,"S")
    
                    pdf.setFontSize(12)
                    pdf.setFontStyle('normal')
                    pdf.line(10,52,200,52,"S")
                    pdf.text(data[0].academic_year.academic_year,28,57)
                    pdf.line(60,44,60,60,"S")
                    pdf.text(data[0].class_id.class_name,75,57) 
                    pdf.line(100,44,100,52,"S")
                    if(data[0].class_group_id){
                        pdf.text(data[0].class_group_id.class_group_name,115,57)
                    }
                    pdf.line(150,44,150,52,"S")
                    pdf.text((data.length).toString(), 174,57)
                    pdf.line(200,44,200,52,"S")
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
                            pdf.text("ID",30,text_height_y+y)
                            pdf.line(45,line_height_y+y,45,line_height_y+y+8,"S")
                            pdf.text("Name",77,text_height_y+y)
                            pdf.line(123,line_height_y+y,123,line_height_y+y+8,"S")
                            pdf.text("Total",127,text_height_y+y)
                            pdf.line(143,line_height_y+y,143,line_height_y+y+8,"S")
                            pdf.text("Obtain",146,text_height_y+y)
                            pdf.line(163,line_height_y+y,163,line_height_y+y+8,"S")
                            pdf.text("GPA",165,text_height_y+y)
                            pdf.line(175,line_height_y+y,175,line_height_y+y+8,"S")
                            pdf.text("LG",178,text_height_y+y)
                            pdf.line(185,line_height_y+y,185,line_height_y+y+8,"S")
                            pdf.text("Me.Po.",187,text_height_y+y)
                            pdf.line(200,line_height_y+y,200,line_height_y+y+8,"S")
                            pdf.setFontStyle('normal')
                            pdf.line(150,280,190,280,"DF")
                            pdf.text("Signature & Date",156,284)
                        }
                        if(data[i]){
                            pdf.line(10,line_height_y+y+8,200,line_height_y+y+8,"S")
                            pdf.line(10,line_height_y+y+16,200,line_height_y+y+16,"S")
    
                            pdf.setFontSize(10)
                            pdf.setFontStyle('normal')
                            pdf.line(10,line_height_y+y+8,10,line_height_y+y+16,"S")
                            pdf.text((i+1).toString(),13,line_height_y+y+12)
                            pdf.line(20,line_height_y+y+8,20,line_height_y+y+16,"S")
                            pdf.text(data[i].student_roll.student_roll,22,line_height_y+y+12)
                            pdf.line(45,line_height_y+y+8,45,line_height_y+y+16,"S")
                            pdf.text(data[i].student_roll.student_name,47,line_height_y+y+12)
                            pdf.line(123,line_height_y+y+8,123,line_height_y+y+16,"S")
                            pdf.text(data[i].total_exam_marks?data[i].total_exam_marks:"",127,line_height_y+y+12)
                            pdf.line(143,line_height_y+y+8,143,line_height_y+y+16,"S")
                            pdf.text(data[i].obtain_marks?data[i].obtain_marks:"",147,line_height_y+y+12)
                            pdf.line(163,line_height_y+y+8,163,line_height_y+y+16,"S")
                            pdf.text(data[i].grade_point_average,166,line_height_y+y+12)
                            pdf.line(175,line_height_y+y+8,175,line_height_y+y+16,"S")
                            pdf.text(data[i].result_grade,179,line_height_y+y+12)
                            pdf.line(185,line_height_y+y+8,185,line_height_y+y+16,"S")
                            pdf.text(data[i].merit_position.toString(),192,line_height_y+y+12)
                            pdf.line(200,line_height_y+y+8,200,line_height_y+y+16,"S")
                        
                        } //Last if statement
    
                        
                        if(i==0){
                            par_page_info()
                        }
                        console.log(page_counter)
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
                        if(data.length==i+1){
                            setTimeout(() => {  
                                pdf.save("resultsheet"+Date.now()+'.pdf')
                            }, 100);
                        }
                    }//for statement
                    
                }// first if statement
                
        else{
            Swal.fire({
                position: 'center',
                icon: 'error',
                title: 'There is no data in this filter .',
                showConfirmButton: true,
                })
        }
        }//innar ajax data 
       })//ajax
    }//after function if
    else{
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Please Select Year, Class and Exam.',
            showConfirmButton: true,
            })
    }

});



$('#id_class_id').change(function(){
    class_group_filter()
})

function class_group_filter(){
var class_id=document.getElementById('id_class_id').value
$.ajax({
    url: "apiedu-academicgroup-api/?class_id="+class_id,
    type: 'get',
    datatype: 'json',
    success: function (data) {
        $("#id_class_group_id option").remove();
        $("#id_class_group_id").append('<option value="">----------</option>');
        data.forEach(element => {
            $("#id_class_group_id").append('<option value="'+element.class_group_id+'">'+element.class_group_name+'</option>');
        });
    }
})
}


$(document).ready(function() {
    $('#id_student_roll').select2({placeholder: " Select a Student "});
    $('#id_class_id').select2({placeholder: " Select a Class "});
    $('#id_academic_year').select2({placeholder: " Select a Year "});
    $('#id_class_group_id').select2({placeholder: " Select a Group "});
});


