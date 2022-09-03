var dcount = document.getElementsByClassName("degree").length
var scount = document.getElementsByClassName("alert").length
$('document').ready(function () {
    /* var input_tags=document.getElementsByTagName('input')
     var i=0
     for(i=0;i<input_tags.length;i++)
     {
         input_tags[i].classList.add('disabled')
         input_tags[i].disabled=true
     }*/
    $('#editinfo').css("display", "block")
    $('input').prop('disabled', true)
    $('input').addClass("disabled")
    $(".close").prop('disabled', true)
    $(".degreetrash").prop('disabled', true)
    $("#editinfo").on('click', function () {
        $('input').prop('disabled', false)
        $('input').removeClass("disabled")
        $(".close").prop('disabled', false)
        $(".degreetrash").prop('disabled', false)
        $("#nextbeforesubmit").css("display", "none")
        $("#formsubmitbtn").css("display", "block")
        $('#editinfo').css("display", "none")
    });
});
$('#edinfo_form').on('submit', function (e) {
    var cont=document.getElementById('maincontainer')
    cont.style.opacity="0.6"
    cont.style.pointerEvents="none"
    document.getElementById('animloaderdiv').style.display="block"
    document.getElementById('animloadertext').style.display="block"
    var i = 0
    for (i = 1; i <= 5; i++) {
        if (document.getElementById('radio' + i).checked == true) {
            document.getElementById('radio_co').value = document.getElementById('radio_label' + i).innerHTML
        }
        else if (document.getElementById('radio6').checked == true) {
            document.getElementById('radio_co').value = document.getElementById('radio_label6').value
        }
    }
    document.getElementById('dcount_val').value = dcount

    var spans = document.getElementsByClassName("alert")
    for (i = 0; i < spans.length; i++) {
        var str = spans[i].innerHTML
        str = str.slice(0, str.indexOf('<'))

        document.getElementById('uskills').value += str + ','
    }
    $("#edinfo_form").submit();
    e.preventDefault();
});
function selectco() {
    if (document.getElementById('radio6').checked == true) {
        document.getElementById('radio_label6').style.display = "block";
    }
    else
        document.getElementById('radio_label6').style.display = "none";
}
function addegree() {
    if (dcount > 4) {
        alert("Sorry In order to make a Good Looking Resume We cannot add More than 5 Degrees")
    }
    else {
        if (dcount > 2) {
            alert("Please make sure that your Resume Should not be clumpsy")
        }
        var parent = document.getElementById('educationaldetails')
        var after = document.getElementById('addegree')
        var d = document.createElement('div')
        d.classList.add('row', 'degree')
        var child_div1 = createdivs("Degree Name", "degreename")
        var child_div2 = createdivs("College Name", "degreeclgname")
        var child_div3 = createdivs("Percentage", "degreepercent")
        var child_div4 = createdivs("Year Of Passing", "degreeyop")
        d.appendChild(child_div1)
        d.appendChild(child_div2)
        d.appendChild(child_div3)
        d.appendChild(child_div4)
        parent.insertBefore(d, after)
        dcount++
    }
}
function createdivs(place, name) {
    var di = document.createElement('div')
    di.classList.add('col-sm')
    var input = document.createElement('input')
    input.type = "text"
    input.classList.add('form-control')
    input.placeholder = place
    input.name = name
    input.required = true
    di.appendChild(input)
    return di
}
function hide_elements(bool, degreeid, hid_id) {
    if (bool == true) {
        dcount--
        document.getElementById('deleting_degree__id').value += document.getElementById(hid_id).value + ","
        document.getElementById(degreeid).remove()
    }
    else {
        scount--;
        document.getElementById('deleting_skill_id').value += document.getElementById(hid_id).value + ","
    }
}
function addskill() {
    if (scount > 9) {
        alert("Sorry !!! You can add only 10 Skills in order to build a Good looking Resume")
        document.getElementById('skillvalue').value = ""
    }
    else {
        if (scount > 6) {
            alert("Please Add Only Required Skills by the Employer.Too many skills may reject your application")
        }
        var skill = document.getElementById('skillvalue')
        skill.value = skill.value.toLowerCase()
        if (skill.value != "") {
            var sp = document.createElement('span')
            sp.classList.add("alert", "alert-primary", "alert-dismissible", "fade", "show")
            sp.style.display = "inline-block"
            sp.style.height = "50px"
            sp.style.width = "auto"
            sp.id = "span" + scount
            var p = document.createTextNode(skill.value)
            sp.appendChild(p)
            var b = document.createElement('button')
            b.type = "button"
            b.addEventListener("click", function () {
                scount--
            }, false)
            b.classList.add("close")
            b.setAttribute("data-dismiss", "alert")
            b.innerHTML = "&times;"
            sp.appendChild(b)
            skill.value = ""
            document.getElementById('skilllist').appendChild(sp)
            scount++
        }
    }
}