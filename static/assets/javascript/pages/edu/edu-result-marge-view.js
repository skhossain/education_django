
function gen_pdf(){
    var students=document.querySelectorAll('.student')
    var institute_name = document.getElementById("institute_name").textContent
    var address = document.getElementById("address").textContent
    var exam_title = document.getElementById("exam_title").textContent
    var class_id = document.getElementById("id_class_id").getAttribute('data-class_id')
    var pdf = new jsPDF('p', 'pt', 'a4');
    let LG=""
    let class_info=""
    $.ajax({
        url: '/apiedu-academicclass-api/?class_id='+class_id,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            class_info=data[0]
            $.ajax({
                url: '/apiedu-result-grade-api/?out_of='+data[0].out_of,
                type: 'get',
                dataType: 'json',
                success: function (data) {
                    LG=data
                }
            })
        }
    })
    

    
    students.forEach((student,index) => {
        $('#page_create').modal('show') 
        let student_id = student.getAttribute("data-id")
        student.childNodes[1].childNodes[0].cells[0].textContent=""
        student.style.fontWeight='bold'
        let student_info=""
        $.ajax({
            url: '/apiedu-studentinfo-api/?student_roll='+student_id,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                student_info=data[0]
            }
        })
        html2canvas(student,{scrollX: window.scrollX}).then(canvas=>{            
            pdf.setFontSize(16)
            pdf.text(institute_name,300,60,{align: 'center'})
            pdf.setFontSize(10)
            pdf.text(address,300,70,{align: 'center'})
            pdf.text(exam_title,300,80,{align: 'center'})
            pdf.setFontSize(16)
            pdf.text('Marks Sheet',300,95,{align: 'center'})
            
            pdf.setFontSize(10)
            pdf.text("Student's ID ",30,130)
            pdf.text(": "+student_info.student_roll,115,130)
            pdf.text("Student's Name ",30,145)
            pdf.text(": "+student_info.student_name,115,145)
            pdf.text('Class Name ',30,160)
            pdf.text(":"+class_info.class_name,115,160)
            pdf.text("Father's Name ",30,175)
            pdf.text(": "+student_info.student_father_name,115,175)
            pdf.text("Mother's Name ",30,190)
            pdf.text(": "+student_info.student_mother_name,115,190)
            pdf.text('Date of Birth ',30,205)
            let birth= moment(student_info.student_date_of_birth).format('MMM DD, YYYY');
            
            pdf.text(": "+birth,115,205)
            
            pdf.setFontSize(8)
            pdf.setFontType("bold")
            pdf.text('Grade Table',470,100)
            pdf.setFontStyle("normal")
            LG.forEach((g,index) => {
            pdf.line(430, 103+(index*10), 560, 103+(index*10));
            pdf.text(Number(g.highest_mark).toFixed(0)+"-"+Number(g.lowest_mark).toFixed(0),435,111+(index*10))
            pdf.text(g.result_gpa,480,111+(index*10))
            pdf.text(g.grade_name,520,111+(index*10))
            });
            pdf.line(430, 103, 430, 103+LG.length*10);
            pdf.line(475, 103, 475, 103+LG.length*10);
            pdf.line(515, 103, 515, 103+LG.length*10);
            pdf.line(560, 103, 560, 103+LG.length*10);
            pdf.line(430, 103+(LG.length*10), 560, 103+(LG.length*10));
            var img = canvas.toDataURL("image/png");
            pdf.addImage(img, 'npg',15,220,canvas.width*0.3,canvas.height*0.35);

            pdf.text('Prepared By',100,220+(canvas.height*0.35)+100)
            pdf.text('Class Teacher',250,220+(canvas.height*0.35)+100)
            pdf.text('Principal/Head Master',400,220+(canvas.height*0.35)+100)
            if(students.length>index+1){
            pdf.addPage("a4");
            $('#page_create_count').text(index+1)
            }else{
                var currentdate = new Date(); 
                var datetime = currentdate.getDate() + "-"
                            + (currentdate.getMonth()+1)  + "-" 
                            + currentdate.getFullYear() + " ("  
                            + currentdate.getHours() + "-"  
                            + currentdate.getMinutes() + "-" 
                            + currentdate.getSeconds()+ ")";
                pdf.save(datetime+'.pdf')
                $('#page_create').modal('hide')
                // location.reload()
            }
        });
    });
    
            
}

function page_print(){
    window.print()
}

function save_and_publish(){
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#03ff37',
        confirmButtonText: 'Yes, Publish it!'
      }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/edu-published-result-marge-publish'+window.location.search,
                type: 'get',
                dataType: 'json',
                success: function (data) {
                    if(data.success_message){
                        Swal.fire({
                            icon: 'success',
                            title: data.success_message,
                            showConfirmButton: false,
                            timer: 1500
                          })
                    }else{
                        Swal.fire({
                            icon: 'error',
                            title: data.error_message,
                            // showConfirmButton: false,
                            // timer: 1500
                          })
                    }
                    
                }
            })
        }
      })
}