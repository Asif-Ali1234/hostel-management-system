function reveal(id1, id2, id3) {
    const psswd1 = document.getElementById(id1)
    const psswd2 = document.getElementById(id3)
    id2.classList.toggle('fa-eye-slash')
    if (psswd1.type == "password") {
        psswd1.type = "text"
        psswd2.type = "text"
    } else {
        psswd1.type = "password"
        psswd2.type = "password"
    }
}

function blocksanimate(animationtime) {
    if(animationtime == 1 ){
        $('#verifyotp').removeClass('boxactive')
        $('#verifyotp').addClass('boxinactive')
        $('#genderdiv').removeClass('boxinactive')
        $('#genderdiv').addClass('boxactive')
    }
    else if(animationtime == 2){
        $('#verificationblock').removeClass('active')
        $('#verificationblock').addClass('inactive')
        $('#basicdetailsblock').removeClass('inactive')
        $('#basicdetailsblock').addClass('active')
    }
    else if(animationtime == 3){
        $('#basicdetailsblock').removeClass('active')
        $('#basicdetailsblock').addClass('inactive')
        $('#registrationblock').removeClass('inactive')
        $('#registrationblock').addClass('active')
    }
}

function validateemail() {
    const email = document.querySelector('#mailid')

    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if (email.value == "") {
        return {
            'error': true,
            'msg': 'Please Enter mail',
        }
    } else if (reg.test(email.value) == false) {
        return {
            'error': true,
            'msg': 'Please enter valid email',
        };
    }
    return {
        'error': false,
    };
}

function validateotp(input) {
    const value = input.value
    if (value == "") {
        return {
            'error': true,
            'msg': 'Please Enter OTP'
        }
    } else if (value.length != 6) {
        return {
            'error': true,
            'msg': 'Please enter 6 digits OTP'
        }
    } else
        return {
            'error': false
        }
}

$('document').ready(() => {
    $('#otpdiv').removeClass('boxactive')
    $('#otpdiv').addClass('boxinactive')
    $('#otplabel').css('opacity','0')
    /*document.oncontextmenu = function(){
        return false
    }*/
    $('.emailbtn').on('click', () => {
        const result = validateemail()
        if (!result['error']) {
            $('.emailbtn').html(`<i class="fas fa-spinner btnloader"></i>`)
            $('.emailbtn').prop('disabled', true)
            $('.emailbtn + span').html("Verifying Mail<span class='dotspan'>...</span>")
            $('.emailbtn + span').css("color", "orange")
            $.ajax({
                type:'get',
                url:'checkusername',
                data: {
                    'username':$('#mailid').val(),
                },
                success:function(response){
                    if(!response['error']){
                        $('.emailbtn + span').html("<i class='fas fa-check-circle'></i> "+response['msg'])
                        $('.emailbtn + span').css("color","green")
                        $('.emailbtn').html('RESEND EMAIL')
                        $('.emailbtn').prop('disabled',false)
                        $('#otpdiv').removeClass('boxinactive')
                        $('#otpdiv').addClass('boxactive')
                        $('#otplabel').css('opacity', '1')
                    }
                    else{
                        $('.emailbtn + span').html("<i class='fas fa-times-circle'></i> "+response['msg'])
                        $('.emailbtn + span').css("color","red")
                        $('.emailbtn').html('VERIFY EMAIL')
                        $('.emailbtn').prop('disabled',false)
                    }
                },
                error:function(){
                    alert('Error Occured')
                    $('.emailbtn').html("VERIFY EMAIL")
                    $('.emailbtn').prop('disabled',false)
                    $('.emailbtn + span').html("")
                }
            })
        } else {
            $('#register_mail_errormessage').html('<i class="fas fa-times-circle"></i> ' + result['msg'])
        }



    })

    $('#otpbtn').on('click', () => {
        const otp = document.querySelector('#otpinput')
        const result = validateotp(otp)
        const usermail = $('#mailid').val()
        document.getElementById('usermail').value=usermail
        if (result['error']) {
            $('#otp_errormessage').html('<i class="fas fa-times-circle"></i> ' + result['msg'])
            $('#otp_errormessage').css('color', 'red')
        } else {
            $('#mailid').prop('disabled', true)
            $('#otpinput').prop('disabled', true)
            $('#otpbtn').html(`<img src="{% static 'Images/833.gif' %}" width=25px  height=25px  alt="loading">`)
            $('#otpbtn').prop('disabled', true)
            $('#otpbtn + span').html("Verifying OTP<span class='dotspan'>...</span>")
            $('#otpbtn + span').css("color", "orange")
            $.ajax({
                type:'get',
                url:'verifyregistrationotp',
                data: {
                    registerotp:$('#otpinput').val(),
                    username:usermail

                },
                success:function(response){
                    if(!response['error']){
                        $('#otpbtn + span').html("")
                        $('#otpbtn + span').css("color","green")
                        $('#otpbtn').html('VERIFY OTP')
                        $('#otpbtn').prop('disabled',false)
                        $('#otpinput').prop('disabled', true)
                        blocksanimate(1)
                    }
                    else{
                        $('#otpbtn + span').html("<i class='fas fa-times-circle'></i> "+response['msg'])
                        $('#otpbtn + span').css("color","red")
                        $('#otpbtn').html('VERIFY OTP')
                        $('#otpbtn').prop('disabled',false)
                        $('#otpinput').prop('disabled', false)
                    }
                },
                error:function(){
                    alert('Error Occured')
                    $('#otpbtn').html("VERIFY EMAIL")
                    $('#otpbtn').prop('disabled',false)
                    $('#otpbtn + span').html("")
                    $('#otpinput').prop('disabled', false)
                }
            })
        }
    })

    $('#nextblockbtn').on('click',()=>{
        let usergender = ""
        const genders = document.getElementsByName('Gender')
        genders.forEach(gender =>{
            if(gender.checked){
                usergender = gender.value
            }
        })
        if($('input[name="first_name"]').val() == "")
        {
            $('#firstname_error').html('<i class="fas fa-times-circle"></i> Please Enter your name')
        }
        else if($('input[name="college_id"]').val() == ""){
            $('#collegeid_errormessage').html('<i class="fas fa-times-circle"></i> Please Enter College ID')
        }
        else if(usergender == "")
        {
            $('#gender_errormessage').html('<i class="fas fa-times-circle"></i> Please Select Gender')
        }
        if($('input[name="first_name"]').val() != "")
        {
            $('#firstname_error').html("")
        }
        if($('input[name="college_id"]').val() != ""){
            $('#collegeid_errormessage').html("")
        }
        if(usergender != "")
        {
            $('#gender_errormessage').html("")
        }
        if($('input[name=first_name]').val() != ""&&usergender!=""&&$('input[name="college_id"]').val() != ""){
            blocksanimate(2)
            $('#circle1').css('background-color','white')
            $('#circle2').css('background-color','gray')
        }
    })

    $('#onemoreclickbtn').on('click',()=>{
        if($('input[name="dob"]').val() == ""){
            $('#dob_errormessage').html('<i class="fas fa-times-circle"></i> Please select Date of Birth')
        }
        else if($('input[name="course_name"]').val() == ""){
            $('#course_errormessage').html('<i class="fas fa-times-circle"></i> Please enter your course name')
        }
        else if($('input[name="yos"]').val() == ""){
            $('#yos_errormessage').html('<i class="fas fa-times-circle"></i> Please enter your year of study')
        }
        else if($('textarea').val() == ""){
            $('#address_errormessage').html('<i class="fas fa-times-circle"></i> Please enter your address')
        }
        if($('input[name="dob"]').val() != ""){
            $('#dob_errormessage').html('')
        }
        if($('input[name="course_name"]').val() != ""){
            $('#course_errormessage').html('')
        }
        if($('input[name="yos"]').val() != ""){
            $('#yos_errormessage').html('')
        }
        if($('textarea').val() != ""){
            $('#address_errormessage').html('')
        }

        if($('input[name="dob"]').val() != "" && $('input[name="course_name"]').val() != "" && $('input[name="yos"]').val() != "" && $('textarea').val() != ""){
            blocksanimate(3)
            $('#circle2').css('background-color','white')
            $('#circle3').css('background-color','gray')
        }
    })
})