var training_count = 0
var job_count = 0
var intern_count = 0
var project_count = 0
var location_id_count = 1, edate_count = 1

$('document').ready(function () {
    /* var input_tags=document.getElementsByTagName('input')
     var i=0
     for(i=0;i<input_tags.length;i++)
     {
         input_tags[i].classList.add('disabled')
         input_tags[i].disabled=true
     }*/
    training_count = document.getElementsByClassName("training").length
    job_count = document.getElementsByClassName("job").length
    intern_count = document.getElementsByClassName("internship").length
    project_count = document.getElementsByClassName("project").length
    $('#editinfo').css("display", "block")
    $('input').prop('disabled', true)
    $('input').addClass("disabled")
    $(".adbutton").prop('disabled', true)
    $(".adbutton").addClass('disabled')
    $(".btn-outline-warning").addClass('disabled')
    $(".btn-outline-warning").prop('disabled', true)
    $('textarea').prop('disabled', true)
    $("textarea").addClass('disabled')
    $("#editinfo").on('click', function () {
        $('input').prop('disabled', false)
        $('input').removeClass("disabled")
        $(".adbutton").removeClass('disabled')
        $(".adbutton").prop('disabled', false)
        $('textarea').prop('disabled', false)
        $("textarea").removeClass('disabled')
        $(".btn-outline-warning").prop('disabled', false)
        $(".btn-outline-warning").removeClass('disabled')
        $("#nextbeforesubmit").css("display", "none")
        $("#formsubmitbtn").css("display", "block")
        $('#editinfo').css("display", "none")
    });
});

$('#formsubmit').on('submit', function (e) {

    var cont=document.getElementById('maincontainer')
    cont.style.opacity="0.5"
    cont.style.pointerEvents="none"

    var dl=document.getElementById('animballloader')
    dl.style.display="block"

    var animtext=document.getElementById('animloadertext')
    animtext.style.display="block"

    document.getElementById('tcount').value = training_count

    document.getElementById('pcount').value = project_count

    document.getElementById('jcount').value = job_count

    document.getElementById('icount').value = intern_count

    animtext.innerHTML="Saving Your Details Hang tight......"

    animtext.style.color="#0033cc"

    $("#formsubmit").submit();
    e.preventDefault();
});
function hide_elements(bool, degreeid, hid_id) {
    if (bool == "training") {
        training_count--
        document.getElementById('deleting_training__id').value += document.getElementById(hid_id).value + ","
        document.getElementById(degreeid).remove()
    }
    else if (bool == "project") {
        project_count--
        document.getElementById('deleting_project__id').value += document.getElementById(hid_id).value + ","
        document.getElementById(degreeid).remove()
    }
    if (bool == "job") {
        job_count--
        document.getElementById('deleting_job__id').value += document.getElementById(hid_id).value + ","
        document.getElementById(degreeid).remove()
    }
    if (bool == "internship") {
        intern_count--
        document.getElementById('deleting_internship__id').value += document.getElementById(hid_id).value + ","
        document.getElementById(degreeid).remove()
    }
}
function Add_Details(parent_block, button_block, block_name, label1, label2) {
    var parent = document.getElementById(parent_block)
    var after_id = document.getElementById(button_block)
    var d = document.createElement('div')
    d.classList.add("row", block_name)
    d.style.display = "block"
    d.style.margin = 0
    var div1 = document.createElement('div')
    div1.style.width = "100%"
    div1.classList.add("row")
    var input1 = createdivs(block_name, "text", block_name + "name")
    var input2 = createdivs("Organization", "text", block_name + "org")
    var input3 = createdivs("Location", "text", block_name + "loc")
    var checkbox = document.createElement("input")
    checkbox.type = "checkbox"
    checkbox.addEventListener("change", function () {
        if (this.checked == true) {
            var box = document.getElementById(input3.children[0].id)
            if (block_name == "training") {
                box.value = "Online"
            }
            else
                box.value = "Work From Home"
        }
        else {
            var box = document.getElementById(input3.children[0].id)
            box.value = ""
            box.placeholder = "Location"
        }
    })
    var text = document.createTextNode(label1)
    input3.appendChild(checkbox)
    input3.appendChild(text)
    div1.appendChild(input1)
    div1.appendChild(input2)
    div1.appendChild(input3)
    d.appendChild(div1)
    var div2 = document.createElement('div')
    div2.classList.add("row")
    div2.style.width = "100%"
    var input4 = createdivs("Choose your Start date", "date", block_name + "sdate")
    input4.insertBefore(document.createTextNode("Start Date"), input4.firstChild)
    var input5 = createdivs("Choose your End date", "date", block_name + "edate")
    input5.insertBefore(document.createTextNode("End Date"), input5.firstChild)
    var checkbox = document.createElement("input")
    checkbox.type = "checkbox"
    checkbox.addEventListener("change", function () {
        var box = document.getElementById(input5.children[0].id)
        if (this.checked == true) {
            box.type = "text"
            box.value = "Present"
        }
        else {
            box.value = ""
            box.type = "date"
        }
    })
    var text = document.createTextNode(label2)
    input5.appendChild(checkbox)
    input5.appendChild(text)
    div2.appendChild(input4)
    div2.appendChild(input5)
    d.appendChild(div2)
    var div3 = document.createElement("div")
    div3.classList.add("row")
    var col_div = document.createElement('div')
    col_div.classList.add("col-sm-11")
    var input6 = document.createElement("textarea")
    input6.name = block_name + "desc"
    input6.style.width = "100%"
    input6.classList.add("form-control")
    input6.placeholder = block_name + " Description"
    col_div.appendChild(input6)
    div3.appendChild(col_div)
    var col_div2 = document.createElement("div")
    col_div2.classList.add("col-sm-1")
    var icon = document.createElement("i")
    icon.classList.add("fas", "fa-trash-alt")
    var button = document.createElement("button")
    button.classList.add("btn", "btn-outline-warning", "deletebutton")
    button.appendChild(icon)
    if (block_name == "training") {
        d.id = block_name + training_count
        training_count++
    }
    else if (block_name == "job") {
        d.id = block_name + job_count
        job_count++
    }
    else if (block_name == "internship") {
        d.id = block_name + intern_count
        intern_count++
    }
    button.addEventListener("click", function () {
        document.getElementById(d.id).remove()
        training_count = document.getElementsByClassName('training').length
        job_count = document.getElementsByClassName('job').length
        intern_count = document.getElementsByClassName("internship").length
        edate--
        location_id_count--
    })
    col_div2.appendChild(button)
    div3.appendChild(col_div2)
    d.appendChild(div3)
    d.appendChild(document.createElement("hr"))
    parent.insertBefore(d, after_id)
}
function createdivs(placehold, type, name) {
    var di = document.createElement("div")
    di.classList.add("col-sm")
    di.style.width = "100%"
    var input = document.createElement("input")
    if (placehold == "Location") {
        input.id = "location" + location_id_count
        location_id_count++
    }
    if (type == "date") {
        input.type = "text"
        input.required == true
        input.placeholder = placehold
        input.addEventListener("mouseenter", function () {
            this.type = "date"
        })
        input.id = "edate" + edate_count
        edate_count++
        input.style.width = "100%"
    }
    else {
        input.type = type
        input.placeholder = placehold
        input.style.width = "100%"
    }
    input.classList.add("form-control")
    input.name = name
    input.required = true
    di.appendChild(input)
    return di
}
function Add_Project() {
    var parent = document.getElementById('projectsblock')
    var after_id = document.getElementById('adproject')

    var main_div = document.createElement("div")
    main_div.classList.add("row", "project")
    main_div.id = "project" + project_count
    main_div.style.display = "block"
    main_div.style.margin = 0

    var div1 = document.createElement("div")
    div1.classList.add("row")
    var input = document.createElement("input")
    input.name = "projectname"
    input.required = true
    input.classList.add("form-control")
    input.placeholder = "Project name"
    div1.appendChild(input)
    main_div.appendChild(div1)

    var div2 = document.createElement("div")
    div2.classList.add("row")
    var pcol_div1 = createdivs("Choose your Start date", "date", "projectsdate")
    pcol_div1.insertBefore(document.createTextNode("Start Date"), pcol_div1.firstChild)
    var pcol_div2 = createdivs("Choose your End date", "date", "projectedate")
    pcol_div2.insertBefore(document.createTextNode("End Date"), pcol_div2.firstChild)
    var checkbox = document.createElement("input")
    checkbox.type = "checkbox"
    checkbox.addEventListener("change", function () {
        var box = document.getElementById(pcol_div2.children[0].id)
        if (this.checked == true) {
            box.type = "text"
            box.value = "Present"
        }
        else {
            box.value = ""
            box.type = "date"
        }
    })
    var text = document.createTextNode("Currently Ongoing")
    pcol_div2.appendChild(checkbox)
    pcol_div2.appendChild(text)
    div2.appendChild(pcol_div1)
    div2.appendChild(pcol_div2)
    main_div.appendChild(div2)

    var div4 = document.createElement("div")
    div4.classList.add("row")
    var ta = document.createElement("textarea")
    ta.name = "projectdesc"
    ta.classList.add("form-control")
    ta.style.width = "100%"
    ta.placeholder = "Project description"
    div4.appendChild(ta)
    main_div.appendChild(div4)

    var div3 = document.createElement("div")
    div3.classList.add("row")
    var col_div = document.createElement('div')
    col_div.classList.add("col-sm-11")
    var input6 = document.createElement("input")
    input6.name = "projectlink"
    input6.style.width = "100%"
    input6.classList.add("form-control")
    input6.placeholder = "Project Link"
    col_div.appendChild(input6)
    div3.appendChild(col_div)
    var col_div2 = document.createElement("div")
    col_div2.classList.add("col-sm-1")
    var icon = document.createElement("i")
    icon.classList.add("fas", "fa-trash-alt")
    var button = document.createElement("button")
    button.classList.add("btn", "btn-outline-warning", "deletebutton")
    button.appendChild(icon)
    button.addEventListener("click", function () {
        document.getElementById(main_div.id).remove()
        training_count = document.getElementsByClassName('training').length
        job_count = document.getElementsByClassName('job').length
        intern_count = document.getElementsByClassName("internship").length
        project_count = document.getElementsByClassName("project").length
        edate--
    })
    col_div2.appendChild(button)
    div3.appendChild(col_div2)
    main_div.appendChild(div3)
    project_count++
    main_div.appendChild(document.createElement("hr"))
    parent.insertBefore(main_div, after_id)
}