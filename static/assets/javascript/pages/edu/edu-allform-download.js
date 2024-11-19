$(document).ready(function () {
  var w_branch_code = document.getElementById('id_global_branch_code').value;
  refresh_branch_list('');
});

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code).trigger('change');
});
//============================= PDF for Admission =========================


let academic_info=""
let admission_form_info=""
$.ajax({
  url: 'apiedu-academic-info-api/',
  type: 'GET',
  dataType: 'json',
  success: function (data) {
      academic_info=data[0]
  }
})



$('#admission').click(function () {
  $.ajax({
    url: 'apiedu-admission-form-header-api/?branch_code='+$('#id_branch_code').val(),
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      admission_form_info=data[0]
    }
  })
  setTimeout(() => {
    var pdf = new jsPDF('p', 'mm', 'a4');
    let y=0;
    console.log(admission_form_info)
    toDataURL(admission_form_info.logo, function(dataUrl) {
      pdf.setFontSize(16)
      pdf.setFontStyle('bold')
      pdf.text(admission_form_info.academic_name.toUpperCase(),105,20,{align: 'center'})
      if(isImage(dataUrl)){
        pdf.addImage(dataUrl,'png',11,24,28,28)
      }
      pdf.setFontSize(10)
      pdf.setFontStyle('normal')
      pdf.text(admission_form_info.text_one?admission_form_info.text_one:"",105,25,{align: 'center'})
      pdf.text(admission_form_info.text_two?admission_form_info.text_two:"",105,29,{align: 'center'})
      pdf.text(admission_form_info.text_three?admission_form_info.text_three:"",105,33,{align: 'center'})
      pdf.text(admission_form_info.text_four?admission_form_info.text_four:"",105,37,{align: 'center'})
      pdf.text(admission_form_info.text_five?admission_form_info.text_five:"",105,41,{align: 'center'})
      /////
      pdf.setFontSize(14)
      pdf.setFontStyle('bold')
      pdf.text(admission_form_info.form_name,105,50,{align: 'center'})
      pdf.line(60,44,150,44)
      pdf.line(60,53,150,53)
      pdf.line(60,44,60,53)
      pdf.line(150,44,150,53)
      //picture box
      pdf.setFontSize(11)
      pdf.setFontStyle('normal')
      pdf.line(160,25,195,25)
      pdf.line(160,57,195,57)
      pdf.line(160,25,160,57)
      pdf.line(195,25,195,57)
      pdf.text("Photo",173,42)
      //input data field start
      pdf.text("Form No.:",10,65)
      pdf.text("----------------------",28,66)
      pdf.text("Serial No.:",60,65)
      pdf.text("----------------------------",80,66)
      pdf.text("Admission Date:",120,65)
      pdf.text("-----------------------------",150,66)

       // willing to be admitted
       pdf.setFontSize(10)
       pdf.setFontStyle('bold')
       pdf.rect(8,75,188,30)
       pdf.text("1. Willing To Be Admitted: ",8,74)
       pdf.setFontSize(11)
       pdf.setFontStyle('normal')
       pdf.text("Class",10,81)
       pdf.text(": ................................................................................................................................................",35,81)
       pdf.text("Class Roll",10,88)
       pdf.text(": ..........................................................",35,88)
       
       pdf.text("Group",102,88)
       pdf.text(": ............................................................",126,88)
       pdf.text("Shift",10,95)
       pdf.text(": ..........................................................",35,95)
       pdf.text("Section",102,95)
       pdf.text(": ............................................................",126,95)
       pdf.text("Category",10,102)
       pdf.text(": ................................................................................................................................................",35,102)
       
       //NB
       pdf.line(8,110,195,110)
       let nb =["* NB:","i) Students who wish to be admitted into Maktab, Nazera and Hefz, will write Maktab, Nazera and Hefz in the ",
       "Class Name cell/ part. Group Name will be filled in accordingly as One, Two, Three, etc.",
       "ii) The 'Student's Mobile Number' part should be filled in with the Legal Guardian's Number (in case of ","unavailability of the Student's mobile number)."]
       pdf.text(nb,8,115)

      //Student Info
       pdf.text("2. Student's Name & Nic Name",8,143)
      pdf.text(": ........................................................................................................",80,143)
      pdf.text("3. Student's NID No.",8,150)
      pdf.text(": ........................................................................................................",80,150)
      pdf.text("4. Birth Certificate No.",8,157)
      pdf.text(": ........................................................................................................",80,157)
      pdf.text("5. Date of Birth",8,164)
      pdf.text(": ........................................................................................................",80,164)
      
     
      pdf.text("6. Permanent Address",8,175)
      pdf.text(": Vill:...................................................P.O:........................................",80,175)
      pdf.text(": P.S:..................................................Dist:........................................",80,182)
      
      pdf.text("7. Present Address",8,192)
      pdf.text(": Vill:...................................................P.O:........................................",80,192)
      pdf.text(": P.S:..................................................Dist:........................................",80,199)
      pdf.text("8. Last Institute Name and Code",8,213)
      pdf.text(": ........................................................................................................",80,213)
      
      pdf.text("9. TC Date and No.(If changed institute)",8,227)
      pdf.text(": ........................................................................................................",80,227)
      pdf.text("10. Student's Contact Number",8,234)
      pdf.text(": ........................................................................................................",80,234)
      pdf.text("11. Student's Email Address",8,241)
      pdf.text(": ........................................................................................................",80,241)
      pdf.text("12. Student's Gender",8,248)
      pdf.text(": Male",80,248)
      pdf.rect(92,245,4,4)
      pdf.text("Female",110,248)
      pdf.rect(125,245,4,4)
      pdf.text("Other's",135,248)
      pdf.rect(150,245,4,4)
      pdf.text("13. Student's Marital Status",8,255)
      pdf.text(": Married",80,255)
      pdf.rect(97,252,4,4)
      pdf.text("Unmarried",110,255)
      pdf.rect(130,252,4,4)
      pdf.text("14. Student's Blood Group",8,262)
      pdf.text(": .......................",80,262)
      pdf.text("15. Student's Religion",110,262)
      pdf.text(": ......................................",152,262)
      pdf.text("16. Information of Latest Obtained Certificate:",8,269)
      pdf.line(15,270,85,270)
      //row
      pdf.line(10,272,195,272)
      pdf.line(10,279,195,279)
      pdf.line(10,286,195,286)
      //column
      pdf.setFontSize(10)
      pdf.setFontStyle('bold')
      pdf.line(10,272,10,286)
      pdf.text("Name of Degree",11,276)
      pdf.line(40,272,40,286)
      pdf.text("Board",42,276)
      pdf.line(65,272,65,286)
      pdf.text("Point",68,276)
      pdf.line(80,272,80,286)
      pdf.text("Grade",82,276)
      pdf.line(95,272,95,286)
      pdf.text("Passing Year",97,276)
      pdf.line(122,272,122,286)
      pdf.text("Institute",145,276)
      pdf.line(195,272,195,286)

      
     
      
      //2nd Page
      pdf.addPage()
      pdf.setFontSize(12)
      pdf.setFontStyle('bold')
      pdf.text("Parents Information",105,20,'center')
      
      pdf.setFontSize(11)
      pdf.setFontStyle('normal')
      pdf.text("17. Father's Name & Phone No.",8,27)
      pdf.text(": ........................................................................................................",80,27)
      pdf.text("18. Father's Occupation",8,34)
      pdf.text(": ........................................................................................................",80,34)
      pdf.text("19. Father's Email Address",8,41)
      pdf.text(": ........................................................................................................",80,41)
      pdf.text("20. Father's NID No.",8,48)
      pdf.text(": ........................................................................................................",80,48)
      pdf.text("21. Father's Address",8,55)
      pdf.text(": ........................................................................................................",80,55)
      pdf.text("22. SMS To Father",8,62)
      pdf.text(": Yes",80,62)
      pdf.rect(90,59,4,4)

      // Mother's Name & Phone No.
      pdf.text("23. Mother's Name & Phone No.",8,75)
      pdf.text(": ........................................................................................................",80,75)
      pdf.text("24. Mother's Occupation",8,82)
      pdf.text(": ........................................................................................................",80,82)
      pdf.text("25. Mother's Email Address",8,89)
      pdf.text(": ........................................................................................................",80,89)
      pdf.text("26. Mother's NID No.",8,96)
      pdf.text(": ........................................................................................................",80,96)
      pdf.text("27. Mother's Address",8,103)
      pdf.text(": ........................................................................................................",80,103)
      pdf.text("28. SMS To Mother",8,110)
      pdf.text(": Yes",80,110)
      pdf.rect(90,107,4,4)
      
      
      pdf.rect(0,115,210,.2)
      pdf.text("29. Legal Guardian's Name & Phone No.",8,123)
      pdf.text(": ........................................................................................................",80,123)
      pdf.text("30. Legal Guardian's Occupation",8,130)
      pdf.text(": ........................................................................................................",80,130)
      pdf.text("31. Legal Guardian's Relation",8,137)
      pdf.text(": ........................................................................................................",80,137)
      pdf.text("32. Legal Guardian's NID No.",8,144)
      pdf.text(": ........................................................................................................",80,144)
      pdf.text("33. Legal Guardian's Address.",8,151)
      pdf.text(": ........................................................................................................",80,151)
      
      pdf.rect(0,158,210,.2)
      pdf.text("34. Local Guardian's Name & Phone No.",8,165)
      pdf.text(": ........................................................................................................",80,165)
      pdf.text("35. Local Guardian's Occupation",8,172)
      pdf.text(": ........................................................................................................",80,172)
      pdf.text("36. Local Guardian's Relation",8,179)
      pdf.text(": ........................................................................................................",80,179)
      pdf.text("37. Local Guardian's NID No.",8,186)
      pdf.text(": ........................................................................................................",80,186)
      pdf.text("38. Local Guardian's Address",8,193)
      pdf.text(": ........................................................................................................",80,193)
      
      //Bottom
      pdf.text("Student's Signature",15,275)
      pdf.text(": .................................",51,275)
      pdf.text("Date",15,282)
      pdf.text(": .................................",24,282)
      pdf.text("Principal's Signature",120,275)
      pdf.text(": .................................",155,275)
      pdf.text("Date",120,282)
      pdf.text(": .................................",129,282)
      pdf.save('Admission_form.pdf')
    })
    
  }, 100);
 
})

//Employee's Registration PDF Form

$('#employee').click(function () {
  var pdf = new jsPDF('p', 'mm', 'a4');
  let y=0;
  toDataURL(academic_info.academic_logo, function(dataUrl) {
    pdf.setFontSize(16)
    pdf.setFontStyle('bold')
    pdf.text(academic_info.academic_name.toUpperCase(),105,20,{align: 'center'})
    if(isImage(dataUrl)){
      pdf.addImage(dataUrl,'png',11,24,28,28)
    }
    pdf.setFontSize(10)
    pdf.setFontStyle('normal')
    pdf.text("Madrasah Code No.: "+academic_info.academic_code+" "+"EIIN No.: "+academic_info.eiin_number,105,25,{align: 'center'})
    pdf.text(academic_info.academic_address,105,29,{align: 'center'})
    pdf.text("Mobile: "+academic_info.academic_mobile_1+","+academic_info.academic_mobile_2,105,41,{align: 'center'})
    pdf.text("Email: "+academic_info.academic_email,105,33,{align: 'center'})
    pdf.text("Web: "+academic_info.academic_website,105,37,{align: 'center'})
    /////
    pdf.setFontSize(14)
    pdf.setFontStyle('bold')
    pdf.text("Employee Registration Form ",105,50,{align: 'center'})
    pdf.line(60,44,150,44)
    pdf.line(60,53,150,53)
    pdf.line(60,44,60,53)
    pdf.line(150,44,150,53)
    //picture box
    pdf.setFontSize(11)
    pdf.setFontStyle('normal')
    pdf.line(160,25,195,25)
    pdf.line(160,57,195,57)
    pdf.line(160,25,160,57)
    pdf.line(195,25,195,57)
    pdf.text("Photo",173,42)
    //input data field start
    pdf.text("Form No.:",10,65)
    pdf.text("----------------------",28,66)
    pdf.text("Serial No.:",60,65)
    pdf.text("----------------------------",80,66)
    pdf.text("Joining Date:",120,65)
    pdf.text("-----------------------------",145,66)

    pdf.text("1. Employee Name",10,73)
    pdf.text(": ........................................................................................................",80,73)
    pdf.text("2. Father's Name",10,80)
    pdf.text(": ........................................................................................................",80,80)
    pdf.text("3. Mother's Name",10,87)
    pdf.text(": ........................................................................................................",80,87)
    pdf.text("4. Date of Birth",10,94)
    pdf.text(": ........................................................................................................",80,94)
    pdf.text("5. Blood Group",10,101)
    pdf.text(": ........................................................................................................",80,101)
    pdf.text("6. Nationality",10,108)
    pdf.text(": ........................................................................................................",80,108)
    pdf.text("7. Permanent Address",10,115)
    pdf.text(": Vill:...................................................P.O:........................................",80,115)
    pdf.text(": P.S:..................................................Dist:........................................",80,122)
    pdf.text("8. Present Address",10,129)
    pdf.text(": Vill:...................................................P.O:........................................",80,129)
    pdf.text(": P.S:..................................................Dist:........................................",80,136)
    pdf.text("9. Personal Phone No.",10,143)
    pdf.text(": ........................................................................................................",80,143)
    pdf.text("10. Office Phone No.",8,150)
    pdf.text(": ........................................................................................................",80,150)
    pdf.text("11. Home Phone No.",8,157)
    pdf.text(": ........................................................................................................",80,157)
    pdf.text("12. Personal Email Address",8,164)
    pdf.text(": ........................................................................................................",80,164)
    pdf.text("13. Tin No.",8,171)
    pdf.text(": ........................................................................................................",80,171)
    pdf.text("14. Gender",8,178)
    pdf.text(": Male",80,178)
    pdf.rect(92,175,4,4)
    pdf.text("Female",105,178)
    pdf.rect(119,175,4,4)
    pdf.text("Other's",129,178)
    pdf.rect(142,175,4,4)
    pdf.text("15. Marital Status",8,185)
    pdf.text(": Married",80,185)
    pdf.rect(97,182,4,4)
    pdf.text("Unmarried",110,185)
    pdf.rect(130,182,4,4)
    pdf.text("16. Employee Status",8,192)
    pdf.text(": ........................................................................................................",80,192)
    pdf.text("17. Employee's Educational Qualification:",8,199)
    pdf.line(15,200,85,200)
    //row
    pdf.line(10,202,195,202)
    pdf.line(10,209,195,209)
    pdf.line(10,216,195,216)
    pdf.line(10,223,195,223)
    pdf.line(10,230,195,230)
    pdf.line(10,237,195,237)
    pdf.line(10,244,195,244)
    //column
    pdf.setFontSize(10)
    pdf.setFontStyle('bold')
    pdf.line(10,202,10,244)
    pdf.text("Name of Degree",11,206)
    pdf.line(40,202,40,244)
    pdf.text("Board Name",42,206)
    pdf.line(65,202,65,244)
    pdf.text("Point",68,206)
    pdf.line(80,202,80,244)
    pdf.text("Grade",82,206)
    pdf.line(95,202,95,244)
    pdf.text("Passing Year",97,206)
    pdf.line(122,202,122,244)
    pdf.text("Institute Name",145,206)
    pdf.line(195,202,195,244)

    pdf.setFontSize(11)
    pdf.setFontStyle('normal')
    pdf.text("18. Optional Contact Name",8,252)
    pdf.text(": ........................................................................................................",80,252)
    pdf.text("19. Optional Contact Relation",8,259)
    pdf.text(": ........................................................................................................",80,259)
    pdf.text("20. Optional Contact Phone No.",8,266)
    pdf.text(": ........................................................................................................",80,266)
    pdf.text("21. Optional Contact Address",8,273)
    pdf.text(": ........................................................................................................",80,273)

    pdf.addPage()
    pdf.text("22. Employee's Office ID",8,20)
    pdf.text(": ........................................................................................................",80,20)
    pdf.text("23. Employee Type",8,27)
    pdf.text(": ........................................................................................................",80,27)
    pdf.text("24. Salary Scale",8,34)
    pdf.text(": ........................................................................................................",80,34)
    pdf.text("25. Designation",8,41)
    pdf.text(": ........................................................................................................",80,41)
    pdf.text("26. Office Email",8,48)
    pdf.text(": ........................................................................................................",80,48)
    pdf.text("27. Reporting To",8,55)
    pdf.text(": ........................................................................................................",80,55)
    pdf.text("28. Take Classes?",8,62)
    pdf.text(": Yes",80,62)
    pdf.rect(90,59,4,4)
    pdf.text("No",105,62)
    pdf.rect(111,59,4,4)
    pdf.text("29. Current Shift",8,69)
    pdf.text(": ........................................................................................................",80,69)
    pdf.text("30. Office Location",8,76)
    pdf.text(": ........................................................................................................",80,76)
    pdf.text("31. Card Number",8,83)
    pdf.text(": ........................................................................................................",80,83)
    pdf.text("32. Passport No.",8,90)
    pdf.text(": ........................................................................................................",80,90)
    pdf.text("33. Salary Bank?",8,97)
    pdf.text(": Yes",80,97)
    pdf.rect(90,94,4,4)
    pdf.text("No",105,97)
    pdf.rect(111,94,4,4)
    pdf.text("34. Bank Account No.",8,104)
    pdf.text(": ........................................................................................................",80,104)
    pdf.text("35. Driving License",8,111)
    pdf.text(": ........................................................................................................",80,111)
    pdf.text("36. Employee Experience Information",8,118)
    pdf.line(15,119,73,119)
    pdf.text("a. Institute Name",15,126)
    pdf.text(": ........................................................................................................",80,126)
    pdf.text("b. Institute Address",15,133)
    pdf.text(": ........................................................................................................",80,133)
    pdf.text("c. Institute Type",15,140)
    pdf.text(": ........................................................................................................",80,140)
    pdf.text("d. Position",15,147)
    pdf.text(": ........................................................................................................",80,147)
    pdf.text("e. Department",15,154)
    pdf.text(": ........................................................................................................",80,154)
    pdf.text("f. Responsibility",15,161)
    pdf.text(": ........................................................................................................",80,161)
    pdf.text("g. Achievement",15,168)
    pdf.text(": ........................................................................................................",80,168)
    pdf.text("h. Institute Phone No.",15,175)
    pdf.text(": ........................................................................................................",80,175)
    pdf.text("i. Institute Email",15,182)
    pdf.text(": ........................................................................................................",80,182)
    pdf.text("j. Contact Person",15,189)
    pdf.text(": ........................................................................................................",80,189)
    pdf.text("k. Start Date",15,196)
    pdf.text(": ........................................................................................................",80,196)
    pdf.text("l. End Date",15,203)
    pdf.text(": ........................................................................................................",80,203)
    pdf.text("36. Employee's Reference Information",8,210)
    pdf.line(15,211,73,211)
    pdf.text("a. Name of Reference",15,218)
    pdf.text(": ........................................................................................................",80,218)
    pdf.text("b. Father's Name",15,225)
    pdf.text(": ........................................................................................................",80,225)
    pdf.text("c. Mother's Name",15,232)
    pdf.text(": ........................................................................................................",80,232)
    pdf.text("d. Date Of Birth",15,239)
    pdf.text(": ........................................................................................................",80,239)
    pdf.text("e. NID No.",15,246)
    pdf.text(": ........................................................................................................",80,246)
    pdf.text("f. Religion",15,253)
    pdf.text(": ........................................................................................................",80,253)
    pdf.text("g. Blood Group",15,260)
    pdf.text(": ........................................................................................................",80,260)
    pdf.text("h. Phone No.",15,267)
    pdf.text(": ........................................................................................................",80,267)
    pdf.text("i. Gender",15,274)
    pdf.text(": Male",80,274)
    pdf.rect(92,271,4,4)
    pdf.text("Female",105,274)
    pdf.rect(119,271,4,4)
    pdf.text("Other's",129,274)
    pdf.rect(142,271,4,4)

    pdf.addPage()
    pdf.text("j. Permanent Address",15,20)
    pdf.text(": Vill:...................................................P.O:........................................",80,20)
    pdf.text(": P.S:..................................................Dist:........................................",80,27)
    pdf.text("k. Present Address",15,34)
    pdf.text(": Vill:...................................................P.O:........................................",80,34)
    pdf.text(": P.S:..................................................Dist:........................................",80,41)
    
    pdf.text("Principal's Signature",15,275)
    pdf.text(": .................................",51,275)
    pdf.text("Date",15,282)
    pdf.text(": .................................",24,282)
    pdf.text("Employee's Signature",120,275)
    pdf.text(": .................................",158,275)
    pdf.text("Date",120,282)
    pdf.text(": .................................",129,282)
    pdf.save('employeeform.pdf')
  })
})





function toDataURL(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.onload = function() {
     var reader = new FileReader();
     reader.onloadend = function() {
        callback(reader.result);
     }
     reader.readAsDataURL(xhr.response);
  };
  xhr.open('GET', url);
  xhr.responseType = 'blob';
  xhr.send();    
}

function isImage(data){
   let mim=data.split(';')
   mim[0].slice(5)
   let image_exe=['image/gif', 'image/png', 'image/jpeg','image/jpg', 'image/bmp', 'image/webp']
   if(image_exe.indexOf(mim[0].slice(5))<0){
       return false
   }else{
       return true
   }
}



