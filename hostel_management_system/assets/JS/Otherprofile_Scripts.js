var pos_count = 0
var ad_count = 0
$('document').ready(function () {
    pos_count = document.getElementsByClassName('poslist').length
    ad_count = document.getElementsByClassName('adlist').length
    $('#editinfo').css("display", "block")
    $('textarea').prop('disabled', true)
    $("textarea").addClass('disabled')
    $('i').prop('disabled', true)
    $('i').addClass('disabled')
    $('.adbutton').prop('disabled', true)
    $('.adbutton').addClass('disabled')
    $("#editinfo").on('click', function () {
        $('textarea').prop('disabled', false)
        $("textarea").removeClass('disabled')
        $('i').prop('disabled', false)
        $('i').removeClass('disabled')
        $('.adbutton').prop('disabled', false)
        $('.adbutton').removeClass('disabled')
        $("#nextbeforesubmit").css("display", "none")
        $("#formsubmitbtn").css("display", "block")
        $('#editinfo').css("display", "none")
    });
});
$('#exitform').on('submit', function (e) {

    document.getElementById('pos_hid_id').value = pos_count

    document.getElementById('ad_hid_id').value = ad_count

    document.getElementById('formsubmitbtn').innerHTML="Saving...."


    $("#exitform").submit();
    e.preventDefault();
});
function deletelist(bool, remove_id, hid_id) {
    document.getElementById(remove_id).remove()
    if (bool == "pos") {
        document.getElementById('deleting_pos_values').value += document.getElementById(hid_id).value + ","
    }
    else if (bool == "ad") {
        document.getElementById('deleting_ad_values').value += document.getElementById(hid_id).value + ","
    }

}
function Add_Details(holder_element, maker_element, input_name, classname) {
    var holder = document.getElementById(holder_element)
    if (pos_count > 6) {
        alert("Sorry !!! You can add only 7 Positions of Responsibilities in order to build a Good looking Resume")
        document.getElementById(maker_element).value = ""
    }
    if (ad_count > 6) {
        alert("Sorry !!! You can add only 7 Details in order to build a Good looking Resume")
        document.getElementById(maker_element).value = ""
    }
    else {
        if (pos_count > 3 || ad_count > 3) {
            alert("Please Add Only Limited number of details.Too many may reject your application")
        }
        var maker = document.getElementById(maker_element)
        if (maker.value != "") {
            var input = document.createElement("input")

            input.type = "hidden"

            input.value = maker.value
            input.name = input_name
            document.getElementById('inputholder').appendChild(input)
            var li = document.createElement("li")
            li.classList.add(classname, "listelement")

            li.appendChild(document.createTextNode(maker.value))

            var i = document.createElement("i")

            i.classList.add("fas", "fa-trash-alt", "btn", "btn-outline-primary")
            i.style.marginLeft = "10px"

            i.addEventListener("click", function () {
                li.remove()
                input.remove()
                pos_count = document.getElementsByClassName('poslist').length
                ad_count = document.getElementsByClassName('adlist').length
            })
            li.appendChild(i)
            maker.value = ""

            holder.appendChild(li)

            if (input_name == "posname")
                pos_count++
            else
                ad_count++
        }
    }
}