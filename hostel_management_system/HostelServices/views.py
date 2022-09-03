from Accounts.models import Authentication, student_details,Room,Floor,Hostel,bill_payments,Fines
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import student_leaves as sl,student_grievances as sg

# Create your views here.
def createroom(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "POST":
            usertype= Authentication.objects.get(username = request.user)
            hostel = Hostel.objects.get(supervisor_mail = usertype)
            floor_id = request.POST['floorid']
            room_id = request.POST['roomid']
            room_capacity = request.POST['capacity']
            if Room.objects.filter(room_id = room_id,hostel_id = hostel.hostel_id).exists():
                floor = Floor.objects.get(hostel_id = hostel.hostel_id,floor_id = floor_id)
                room = Room.objects.get(room_id = room_id,hostel_id = hostel.hostel_id)
                room.floor_id = floor
                room.capacity = room_capacity
                room.save()
                messages.success(request,'Room details has been updated successfully')
                return redirect('login')
            else:
                floor = Floor.objects.get(hostel_id =hostel.hostel_id,floor_id = floor_id)
                room = Room.objects.create(room_id = room_id,floor_id = floor,hostel_id = hostel,capacity = room_capacity)
                room.save()
                messages.success(request,'Room has been successfully created')
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to create rooms please contact admin')
        return redirect('login')

def assignroom(request):
    if request.user.is_authenticated and request.user.is_student:
        if request.method == 'POST':
            user = Authentication.objects.get(username = request.user)
            student = student_details.objects.get(student_mail = user)
            floor = student.yos
            if floor != student.yos:
                floor = student.yos
            room = request.POST['roomnumber']
            if Room.objects.filter(room_id = room).exists():
                student_room = Room.objects.get(room_id = room)
                if student_room.no_of_students_occupied < student_room.capacity:
                    student_room.no_of_students_occupied+=1
                    student_room.save()
                    student.assigned_room = room
                    student.save()
                    messages.success(request,'Room has been successfully assigned to you')
                    return redirect('login')
                else:
                    messages.error(request,'Room has already completely occupied or has no vacancies')
                    return redirect('login')
            else:
                messages.error(request,'Sorry your selected room doesnt exist please try again')
                return redirect('login')
    else:
        messages.error(request,'You are not  authorized to Assign Room please contact Admin')
        return redirect('login')

def applyleave(request):
    if request.user.is_authenticated and request.user.is_student:
        if request.method == 'POST':
            user = Authentication.objects.get(username = request.user)
            startdate = request.POST['sdate']
            enddate = request.POST['edate']
            reason = request.POST['reason']
            if sl.objects.filter(student_email = user,startdate = startdate,enddate=enddate,is_accepted = True,allow_new_leave = True).exists():
                messages.warning(request,'Your leave from {} to {} has been already accepted by suervisor'.format(startdate,enddate))
                return redirect('login')
            if sl.objects.filter(student_email = user,startdate = startdate,enddate=enddate,is_accepted = False).exists():
                leave = sl.objects.get(student_email = user,startdate = startdate,enddate=enddate)
                leave.reason = reason
                leave.is_accepted = False
                leave.allow_new_leave = False
                leave.save()
                messages.success(request,'Leave has successfully applied and waiting for confirmation from supervisor')
                return redirect('login')
            else:
                leave = sl.objects.create(student_email = user,startdate = startdate,enddate=enddate,is_accepted = False,reason = reason,allow_new_leave = False,is_rejected = False)
                leave.save()
                messages.success(request,'Leave has successfully applied and waiting for confirmation from supervisor')
                return redirect('login')
    else:
        messages.error(request,'You are not  authorized to Assign Room please contact Admin')
        return redirect('login')

def applygrievance(request):
    if request.user.is_authenticated and request.user.is_student:
        if request.method == 'POST':
            user = Authentication.objects.get(username = request.user)
            compliant = request.POST['complaint']
            if sg.objects.filter(student_email = user,grievance = compliant,is_accepted = True,is_completed = True).exists():
                messages.warning(request,'Your grievance has been already  and completed by suervisor')
                return redirect('login')
            if sg.objects.filter(student_email = user,grievance = compliant).exists():
                leave = sg.objects.get(student_email = user,grievance = compliant)
                leave.is_accepted = False
                leave.is_completed = False
                leave.save()
                messages.success(request,'Grievance has successfully applied and waiting for confirmation from supervisor')
                return redirect('login')
            else:
                leave = sg.objects.create(student_email = user,grievance = compliant,is_accepted = False,is_completed = False,is_rejected = False)
                leave.save()
                messages.success(request,'Grievance has successfully applied and waiting for confirmation from supervisor')
                return redirect('login')
    else:
        messages.error(request,'You are not  authorized to Assign Room please contact Admin')
        return redirect('login')

def acceptleave(request,mail):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "GET":
            if Authentication.objects.filter(username = mail).exists():
                user = Authentication.objects.get(username = mail)
                if sl.objects.filter(student_email = user).exists():
                    leave= sl.objects.latest('applied_date')
                    leave.is_accepted = True
                    leave.is_rejected = False
                    leave.allow_new_leave = True
                    leave.save()
                    return redirect('login')
                else:
                    messages.error(request,'User have not applied for leave application')
                    return redirect('login')
            else:
                messages.error(request,'User with {} doesnt exist please contact admin'.format(mail))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to accept leave of students')
        return redirect('login')

def rejectleave(request,mail):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "GET":
            if Authentication.objects.filter(username = mail).exists():
                user = Authentication.objects.get(username = mail)
                if sl.objects.filter(student_email = user).exists():
                    leave = sl.objects.latest('applied_date')
                    leave.is_rejected = True
                    leave.is_accepted = False
                    leave.allow_new_leave = True
                    leave.save()
                    return redirect('login')
                else:
                    messages.error(request,'User have not applied for leave application')
                    return redirect('login')
            else:
                messages.error(request,'User with {} doesnt exist please contact admin'.format(mail))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to reject leave of students')
        return redirect('login')

def acceptgrievance(request,mail):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "GET":
            if Authentication.objects.filter(username = mail).exists():
                user = Authentication.objects.get(username = mail)
                if sg.objects.filter(student_email = user).exists():
                    grievance= sg.objects.latest('applied_date')
                    grievance.is_accepted = True
                    grievance.is_rejected = False
                    grievance.is_completed = False
                    grievance.save()
                    return redirect('login')
                else:
                    messages.error(request,'User have not submitted any grievance')
                    return redirect('login')
            else:
                messages.error(request,'User with {} doesnt exist please contact admin'.format(mail))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to accept grievance of students')
        return redirect('login')

def rejectgrievance(request,mail):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "GET":
            if Authentication.objects.filter(username = mail).exists():
                user = Authentication.objects.get(username = mail)
                if sg.objects.filter(student_email = user).exists():
                    grievance= sg.objects.latest('applied_date')
                    grievance.is_accepted = False
                    grievance.is_rejected = True
                    grievance.is_completed = False
                    grievance.save()
                    return redirect('login')
                else:
                   messages.error(request,'User have not submitted any grievance')
                   return redirect('login')
            else:
                messages.error(request,'User with {} doesnt exist please contact admin'.format(mail))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to accept grievance of students')
        return redirect('login')

def completegrievance(request,mail):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "GET":
            if Authentication.objects.filter(username = mail).exists():
                user = Authentication.objects.get(username = mail)
                if sg.objects.filter(student_email = user).exists():
                    grievance= sg.objects.latest('applied_date')
                    if grievance.is_accepted:
                        grievance.is_accepted = True
                        grievance.is_rejected = False
                        grievance.is_completed = True
                        grievance.save()
                        return redirect('login')
                    else:
                        messages.warning(request,'Grievance ia not accepted please first accept it before completing')
                        return redirect('login')
                else:
                    messages.error(request,'User have not submitted any grievance')
                    return redirect('login')
            else:
                messages.error(request,'User with {} doesnt exist please contact admin'.format(mail))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to accept grievance of students')
        return redirect('login')

def upload_bill(request):
    if request.user.is_authenticated and request.user.is_student:
        if request.method == "POST":
            transac_id = request.POST['tid']
            paiddate = request.POST['paid_date']
            if 'billimage' in request.FILES:
                bill_image = request.FILES['billimage']
                if bill_payments.objects.filter(student_email = request.user).exists():
                    bills = bill_payments.objects.get(student_email = request.user)
                    student = student_details.objects.get(student_mail = request.user)
                    hostel = Hostel.objects.get(hostel_id = str(student.hostel_id))
                    bills.transaction_id = transac_id
                    bills.paid_date = paiddate
                    bills.transaction_image = bill_image
                    bills.hostel_id = hostel
                    bills.payment_paid = True
                    bills.payment_accepted = False
                    bills.save()
                else:
                    usertype = Authentication.objects.get(username = request.user)
                    student = student_details.objects.get(student_mail = request.user)
                    hostel = Hostel.objects.get(hostel_id = str(student.hostel_id))
                    bills = bill_payments.objects.create(student_email = usertype,paid_date = paiddate,transaction_id = transac_id,transaction_image = bill_image,hostel_id = hostel)
                    bills.payment_paid = True
                    bills.payment_accepted = False
                    bills.save()
                messages.success(request,'Your bill has been successfully uploaded and waiting for confirmation by supervisor')
                return redirect('login')
            else:
                messages.error(request,'Your bill image is not uploaded properly please try again')
                return redirect('login')
        else:
            messages.warning(request,'Not a Post request cannot be processed')
            return redirect('login')
    else:
        messages.error(request,'You are not authorized to upload bills')
        return redirect('login')

def accept_bill_payment(request,mail):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "GET":
            if Authentication.objects.filter(username = mail).exists():
                user = Authentication.objects.get(username = mail)
                if bill_payments.objects.filter(student_email = user).exists():
                    bill= bill_payments.objects.get(student_email = mail)
                    bill.payment_accepted = True
                    bill.payment_rejected = False
                    bill.payment_paid = True
                    bill.save()
                    return redirect('login')
                else:
                    messages.error(request,'User have not uploaded bill yet')
                    return redirect('login')
            else:
                messages.error(request,'User with {} doesnt exist please contact admin'.format(mail))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to accept bills of students')
        return redirect('login')

def reject_bill_payment(request,mail):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "GET":
            if Authentication.objects.filter(username = mail).exists():
                user = Authentication.objects.get(username = mail)
                if bill_payments.objects.filter(student_email = user).exists():
                    bill = bill_payments.objects.get(student_email = mail)
                    bill.payment_accepted = False
                    bill.payment_rejected = True
                    bill.payment_paid = True
                    bill.save()
                    return redirect('login')
                else:
                    messages.error(request,'User have not applied for leave application')
                    return redirect('login')
            else:
                messages.error(request,'User with {} doesnt exist please contact admin'.format(mail))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to reject leave of students')
        return redirect('login')

def assignbill(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        if request.method == "POST":
            hostel = Hostel.objects.get(supervisor_mail = request.user)
            bill = request.POST['mess_bill']
            month = request.POST['mess_month']
            deadline = request.POST['mess_deadline']
            if hostel.month_name != '0' and hostel.month_bill != 0 and hostel.month_deadline != None:
                if hostel.month_name == month:
                    hostel.month_bill = bill
                    hostel.month_deadline = deadline
                    hostel.save()
                    messages.success(request,'Bill Already exists and has been updated ')
                else:
                    pending_students = bill_payments.objects.filter(payment_paid = False)
                    for student in pending_students:
                            usertype= Authentication.objects.get(username = student.student_email)
                            fine = Fines.objects.create(student_email = usertype,fine_month = hostel.month_name,fine_amount = hostel.month_bill,fine_deadline = hostel.month_deadline,hostel_id = hostel)
                            fine.save()
                    hostel.month_bill = bill
                    hostel.month_name = month
                    hostel.month_deadline = deadline
                    hostel.save()
                    students = bill_payments.objects.filter(hostel_id = hostel.hostel_id)
                    for student in students:
                        student.payment_paid = False
                        student.payment_accepted = False
                        student.payment_rejected = False
                        student.save()
                    messages.success(request,'Bill has been successfully assigned for the month {}'.format(month))
                return redirect('login')
            else:
                hostel.month_name = month
                hostel.month_bill = bill
                hostel.month_deadline = deadline
                hostel.save()
                messages.success(request,'Bill has been successfully assigned for the month {}'.format(month))
                return redirect('login')
    else:
        messages.error(request,'You are not authorized to create rooms please contact admin')
        return redirect('login')
