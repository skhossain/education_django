function filtering_alldata(){
    let academic_year=document.getElementById('academic_yearl').value
    let month_number=document.getElementById('month_list').value
    let class_id=document.getElementById('class_names').value
    let class_group_id=document.getElementById('group_list').value
    let section_id=document.getElementById('section_name').value
    let subject_id=document.getElementById('subject_list').value
                
    $.ajax({
                
        url:"/edu-allstudents-attendencelist?academic_year="+academic_year+"&month_number="+month_number+"&class_id="+class_id+"&class_group_id="+class_group_id+"&section_id="+section_id+"&subject_id"+subject_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            document.getElementById('table-list').innerHTML = data  
        }
    })
}
                


$('#class_names').change(function(){
    $.when(get_group_list()).then(
        filtering_subjectlist()
    );  
})

function get_group_list(){
    let class_id=$('#class_names').val()
    $.ajax({
        url: "apiedu-academicgroup-api/?class_id="+class_id,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#group_list option').remove();
            $("#group_list").append('<option value="">------------</option>');
            data.forEach(G=>{
                $("#group_list").append('<option value="'+G.class_group_id+'">'+G.class_group_name+'</option>');
            })
        }
    })
}

$('#group_list').change(function(){
    filtering_subjectlist()  
})

function filtering_subjectlist(){
    let class_id=document.getElementById('class_names').value
    let class_group_id=document.getElementById('group_list').value
    $.ajax({
        url: "apiedu-sublist-api/?class_id="+class_id+"&class_group_id="+class_group_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#subject_list option").remove();
            $("#subject_list").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#subject_list").append('<option value="'+element.subject_id+'">'+element.subject_name+'</option>')
            });
        }
    })
}

$('#class_names').change(function(){
    filtering_section()
})

function filtering_section(){
    let class_id=document.getElementById('class_names').value
    $.ajax({
        url: "apiedu-sectioninfo-api/?class_id="+class_id,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#section_name option").remove();
            $("#section_name").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#section_name").append('<option value="'+element.section_id+'">'+element.section_name+'</option>')
            });
           
        }
    })
}


$('#academic_yearl').change(function(){
    filtering_classes()
})

function filtering_classes(){
    let academic_year=document.getElementById('academic_yearl').value
    $.ajax({
        url: "apiedu-academicclass-api/?academic_year="+academic_year,
        type: 'get',
        datatype: 'json',
        success: function (data) {
            $("#class_names option").remove();
            $("#class_names").append('<option value="">------------</option>');
            data.forEach(element => {
                $("#class_names").append('<option value="'+element.class_id+'">'+element.class_name+'</option>')
            });
           
        }
    })
}

// Select 2
$('#class_names').select2({placeholder: "Select a class"})
$('#month_list').select2({placeholder: "Select a month"})
$('#academic_yearl').select2({placeholder: "Select a year"})
$('#group_list').select2({placeholder: "Select a class group"})
$('#section_name').select2({placeholder: "Select a section"})
$('#subject_list').select2({placeholder: "Select a subject"})

function attendence_sheet(){
    var academic_year = $("#academic_yearl").val();
    var academic_year=Number(academic_year)
    var month_name = $("#month_list").val();
    var class_id = $("#class_names").val();
    var class_group_id = $("#group_list").val();
    var section_id = $("#section_name").val();
    var subject_id = $("#subject_list").val();

    var data_string={
        academic_year:academic_year,
        month_name:month_name,
        class_id:class_id,
        class_group_id:class_group_id,
        section_id:section_id,
        subject_id:subject_id,

    }
    
    $.ajax({
        url: "/edu-stu-attendencesheet-insert",
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if(data.success_message){
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Created Successfully',
                    showConfirmButton: false,
                    timer: 1500
                  })
                    filtering_data()
                    $('#class_names').val('').trigger('change')
                    $('#month_list').val('').trigger('change')
                    $('#academic_yearl').val('').trigger('change')
                    $('#group_list').val('').trigger('change')
                    $('#section_name').val('').trigger('change')
                    $('#subject_list').val('').trigger('change')
            }
            if(data.error_message){
                Swal.fire({
                    position: 'center',
                    icon: 'error',
                    title: data.error_message,
                    showConfirmButton: false,
                    timer: 1500
                  })
                  filtering_data()
            }
        }
    })
    return false;
    
}


function generate_pdf(id,yr,month,cls,grp,sec,sub){
    
    const doc = new jsPDF("p", "mm", "a4");
    let counter=1
    Academic_Info=""
    $.ajax({
        url: "/apiedu-academic-info-api",
        type: 'get',
        dataType: 'json',
        success: function (data) {
            Academic_Info=data[0]
        }
    });

    function header(){
    doc.setFontSize(10)
    doc.text("Academic Year",9,30)
    doc.text(": "+yr,35 ,30)
    doc.text("Month", 50, 30)
    doc.text(" : "+month,60,30)
    doc.text("Class",85,30);
    doc.text(" : "+cls,95,30)
    doc.text("Group", 115, 30)
    if(grp !== "None"){
        doc.text(" : "+grp,125,30)
    }else{
        doc.text(" : ",125,30)
    }
    doc.text("Section", 145, 30)
    if(sec !== "None"){
        doc.text(" : "+sec,157,30)
    }else{
        doc.text(" : ",157,30)
    }
    
    doc.text("Subject", 170, 30)
    
    if(sub !== "None"){
        doc.text(" : "+sub, 183, 30)
    }else{
        doc.text(" : ", 183, 30)
    }

    doc.setFontSize(16)
    doc.setFontType("bold");
    doc.text(Academic_Info.academic_name,105,10, 'center')
    doc.setFontSize(10)
    doc.setFontType("normal");
    doc.text(Academic_Info.academic_address,105,14, 'center')
    doc.text("Mobile: "+Academic_Info.academic_mobile_1,105,18, 'center')
    doc.setFontSize(12)
    doc.text("Student Attendence Sheet",105,22,'center')
    doc.line(10, 24, 200, 24, 'S')
    }
  setTimeout(() => {

    $.ajax({
        url: "/edu-attendance-sheet-pdf/"+id,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if(data.attendance.length){
            header()
            let x=0;
            let y=0;
            doc.setFontSize(9)
            function top_row(){
                doc.line(5, 40, 50+(5*data.attendance[0].day.day) , 40, 'S')
                doc.setFontSize(9)
                doc.text("Name",7,44)
                let z=0;
                for (let j = 1; j <= data.attendance[0].day.day; j++) {
                    doc.line(50+z,40,50+z,47,'S')
                    doc.text(String(j),(50+z)+1,44)
                    z+=5
                    
                    if(j==data.attendance[0].day.day){
                        z=0
                    }
                }
            }
                        
            data.attendance.forEach((td,index)=>{   
                doc.setFontSize(10)
                doc.text(td.student.student_roll__student_name,7,52+y)
                y=counter*7
                doc.line(5, 40+y, 50+(5*td.day.day), 40+y, 'S')             
                   
                for (let i = 1; i <= td.day.day; i++) {
                    doc.line(50+x,40+y,50+x,47+y,'S')
                    x+=5
                    if(i== td.day.day){
                        x=0
                    }
                    
                  }
                if(index == 0){
                    top_row()
                }
                if((index+1)%2==0){
                    doc.line(5, 47+counter*7, 50+(5*td.day.day), 47+counter*7, 'S')
                    doc.line(5, 40, 5, 47+counter*7, 'S')
                    doc.line(50+(5*td.day.day), 40, 50+(5*td.day.day), 47+counter*7, 'S')
                    y=0;
                    counter=1;
                    doc.addPage()
                    header()
                    top_row()
                }else{  
                    counter+=1
                } 
            
                if(data.attendance.length == index+1){
                    doc.line(5, 40+counter*7, 50+(5*td.day.day), 40+counter*7, 'S')
                    doc.line(5, 40, 5, 40+counter*7, 'S')
                    doc.line(50+(5*td.day.day), 40, 50+(5*td.day.day), 40+counter*7, 'S')
                    var currentdate = new Date(); 
                    var datetime = currentdate.getDate() + "-"
                                + (currentdate.getMonth()+1)  + "-" 
                                + currentdate.getFullYear() + " ("  
                                + currentdate.getHours() + "-"  
                                + currentdate.getMinutes() + "-" 
                                + currentdate.getSeconds()+ ")";
                    doc.save("Attendence Sheet-"+datetime+".pdf");
                }
            });
              
        }
    }
    })
}, 1000);

}    

