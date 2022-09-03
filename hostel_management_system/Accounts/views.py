import random as r
import time
from urllib import request
from datetime import date,datetime

from django.contrib import messages
from django.contrib.auth.models import auth
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .models import Authentication, bill_payments,student_details,Hostel,Floor,Room,Fines
from HostelServices.models import student_leaves,student_grievances

# Create your views here.

otpdict={}

registerotpdict = {}

attemptsdict={}

def register(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        college_id = request.POST['college_id']
        username=request.POST["E-mail"]
        gender=request.POST["Gender"]
        dob = request.POST['dob']
        course_name = request.POST['course_name']
        yos = request.POST['yos']
        address = request.POST['address']
        fname = request.POST['father_name']
        hostel_selected = request.POST['hostel_selected']
        mname = request.POST['mother_name']
        parent_number = request.POST['parent_number']
        student_number = request.POST['student_number']
        passwd=request.POST["passwd"]
        confirmedpassword=request.POST["confirmpassword"]
        if Authentication.objects.filter(username=username).exists():
            messages.error(request,"You have already registered with us")
            return redirect("register")
        elif passwd!=confirmedpassword:
            messages.warning(request,"Passwords Not Matched Please Try again")
            return redirect("register")
        else:
            user=Authentication.objects.create_user(username=username,password=passwd,first_name=first_name,mobile_number = student_number,is_student = True,is_supervisor = False)
            user.save()
            hostel = Hostel.objects.get(hostel_id  = hostel_selected)
            student = student_details.objects.create(student_mail = user,student_id = college_id,gender = gender,father_name = fname,
            mother_name = mname,parent_mobile_number = parent_number,date_of_birth = dob,yos = yos,course = course_name,
            address = address,verified_by_supervisor = False,hostel_id = hostel)
            student.save()
            messages.success(request,"Your account has been created and waiting for confirmation from supervisor")
            return redirect("login")
    else:
        hostels = Hostel.objects.all()
        args = {
            'hostels':hostels,
        }
        return render(request,"User_Registration_form.html",args)

def dashboard(request): 
    if request.user.is_authenticated:
        usertype = Authentication.objects.get(username = request.user)
        if usertype.is_student:
            student = student_details.objects.get(student_mail = request.user)
            student_hostel = Hostel.objects.get(hostel_id = str(student.hostel_id))
            floor = Floor.objects.get(floor_id = student.yos,hostel_id = student.hostel_id)
            rooms = Room.objects.filter(floor_id = student.yos,hostel_id = student.hostel_id)
            leave_applications = student_leaves.objects.filter(student_email = usertype)
            grievance_applications = student_grievances.objects.filter(student_email  = usertype)

            args = {
                'name':usertype.first_name,
                'cnum':usertype.mobile_number,
                'student':student,
                'floor':floor,
                'rooms':rooms,
                'leaveapplications':leave_applications,
                'grievanceapplications':grievance_applications,
                'hostel':student_hostel,
            }
            if student_hostel.month_deadline != None:
                today = date.today()
                dateformat = r"%Y-%m-%d"
                date1 = datetime.strptime(str(today),dateformat)
                date2 = datetime.strptime(str(student_hostel.month_deadline),dateformat)
                if int(str(date2-date1).split(' ')[0]) > 0:
                    args['deadline_completed'] = False
                else:
                    args['deadline_completed'] = True
                    args['difference'] = abs(int(str(date2-date1).split(' ')[0]))

            if student_leaves.objects.filter(student_email = usertype).exists():
                args['leave'] = student_leaves.objects.latest('student_email')
            else:
                args['leave'] = None
            if student_grievances.objects.filter(student_email = usertype).exists():
                args['grievance'] = student_grievances.objects.latest('student_email')
            else:
                args['grievance'] = None
            if bill_payments.objects.filter(student_email = usertype).exists():
                bills = bill_payments.objects.get(student_email = usertype)
                args['bills']=bills
            else:
                args['bills'] = None
            if Fines.objects.filter(student_email = usertype).exists():
                fines = Fines.objects.filter(student_email = usertype)
                fines_list = []
                for fine in fines:
                    today = date.today()
                    dateformat = r"%Y-%m-%d"
                    date1 = datetime.strptime(str(today),dateformat)
                    date2 = datetime.strptime(str(fine.fine_deadline),dateformat)
                    diff = abs(int(str(date2-date1).split(' ')[0]))
                    temp = {}
                    temp['fine_month'] = fine.fine_month
                    temp['fine_amount'] = fine.fine_amount
                    temp['fine_deadline'] = fine.fine_deadline
                    temp['total_amount'] = int(fine.fine_amount) + ( int(diff) * 100 )
                    fines_list.append(temp)
                args['fines']=fines_list
            else:
                args['fines'] = None
            return render(request,'student_dashboard.html',args)
        elif usertype.is_supervisor:
            hostel = Hostel.objects.get(supervisor_mail = request.user)
            students = student_details.objects.filter(verified_by_supervisor = False,hostel_id = hostel.hostel_id)
            bill_verifications = bill_payments.objects.filter(payment_paid = True,payment_accepted = False)
            floors = Floor.objects.filter(hostel_id = hostel.hostel_id)
            rooms = Room.objects.filter(hostel_id = hostel.hostel_id)
            leaves = student_leaves.objects.filter(is_accepted = False,allow_new_leave = False)
            student_leave_details = []
            for leave in leaves:
                st_user =  Authentication.objects.get(username = leave.student_email)
                student = student_details.objects.get(student_mail = st_user)
                stud = {}
                stud['name'] = st_user.first_name
                stud['roomid'] = student.assigned_room
                stud['mail'] = leave.student_email
                stud['regno'] = student.student_id
                stud['pnum'] = student.parent_mobile_number
                stud['sdate'] = leave.startdate
                stud['edate'] = leave.enddate
                stud['reason'] = leave.reason
                stud['accepted']  = leave.is_accepted
                student_leave_details.append(stud)
            grievances = student_grievances.objects.filter(is_completed = False,is_rejected = False)
            student_greivance = []
            for grievance in grievances:
                st_user =  Authentication.objects.get(username = grievance.student_email)
                student = student_details.objects.get(student_mail = st_user)
                stud = {}
                stud['name'] = st_user.first_name
                stud['regno'] = student.student_id
                stud['mail'] = grievance.student_email
                stud['roomid'] = student.assigned_room
                stud['complaint'] = grievance.grievance
                stud['accepted']  = grievance.is_accepted
                student_greivance.append(stud)
            bills_list = []
            for bill in bill_verifications:
                applied_student = student_details.objects.get(student_mail = bill.student_email)
                temp = {}
                temp['name'] = bill.student_email.first_name
                temp['email'] = bill.student_email
                temp['regno'] = applied_student.student_id
                temp['room'] = applied_student.assigned_room
                temp['floor'] = applied_student.yos
                temp['tid'] = bill.transaction_id
                temp['pdate'] = bill.paid_date
                temp['adate'] = bill.applied_date
                temp['proof'] = bill.transaction_image
                bills_list.append(temp)
            args = {
                'regstudents':students,
                'floors':floors,
                'rooms':rooms,
                'hostel':hostel,
                'leaves':student_leave_details,
                'grievances':student_greivance,
                'bills':bills_list,
            }
            return render(request,'supervisor_dashboard.html',args)
        else:
            messages.error(request,'Your account is not successfully created please contact admin')
            return redirect('/')

    else:
        messages.error(request,'you are not authenticated please login to continue')
        return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=="POST":
        username=request.POST["username"]
        passwd=request.POST["passwd"]

        user=auth.authenticate(username=username,password=passwd)
        if Authentication.objects.filter(username=username).exists():

            if user is not None:
                login_user =  Authentication.objects.get(username = username)
                if login_user.is_supervisor:
                    auth.login(request,user)
                    return redirect('dashboard')
                elif login_user.is_student:
                    student = student_details.objects.get(student_mail = login_user)
                    if student.verified_by_supervisor:
                        auth.login(request,user)
                        return redirect('dashboard')
                    else:
                        messages.warning(request,'Your account is not yet verified please contact supervisor')
                        return redirect('login')
                #return render(request,"After_login_page.html")
            else:
                messages.error(request,"Username and Password is not matched")
                return redirect("login")
        else:
            messages.warning(request,"Sorry We Couldn't find you ....Connect with us first")
            return redirect('login')
    else:
        return render(request,"login.html")

def logout(request):
    auth.logout(request)
    messages.info(request,"You have been logged out Successfully")
    return redirect("/")

def acceptuser(request,mail):
    if request.method == "GET":
        if request.user.is_authenticated and request.user.is_supervisor:
            user = Authentication.objects.get(username = mail)
            student = student_details.objects.get(student_mail = user)
            if student.verified_by_supervisor:
                messages.error(request,'Student is alredy verified')
                return redirect('login')
            else:
                student.verified_by_supervisor = True
                student.save()
                hostel = Hostel.objects.get(hostel_id = str(student.hostel_id))
                bill = bill_payments.objects.create(student_email = user,hostel_id = hostel,transaction_id = None,transaction_image = None,paid_date = None)
                bill.save()
                messages.success(request,'Student has been successfully verified')
                return redirect('login')
        else:
            messages.error(request,'You are not authorized to accept any user')
            return redirect('login')
    else:
        messages.warning(request,'Bad request, cannot be processed')
        return redirect('login')

def rejectuser(request,mail):
    if request.method == "GET":
        if request.user.is_authenticated and request.user.is_supervisor:
            user = Authentication.objects.get(username = mail)
            user.delete()
            messages.success(request,'Student has been successfully verified')
            return redirect('login')
        else:
            messages.error(request,'You are not authorized to accept any user')
            return redirect('login')
    else:
        messages.warning(request,'Bad request, cannot be processed')
        return redirect('login')

'''def ContactUs(request):
    if request.method=="POST":
        username=request.POST["useremail"]
        firstname=request.POST["userfirstname"]
        lastname=request.POST['userlastname']
        number=request.POST['usermobilenumber']
        message=request.POST['usermessage']
        if Contact_Messages.objects.filter(username=username).exists():
            user=Contact_Messages.objects.get(username=username)
            msg=user.message+'\n$#!  '+message
            user.user_firstname=firstname
            user.user_lastname=lastname
            user.user_mobilenumber=number
            user.message=msg
            user.save()
            messages.success(request, "You have sent "+str(msg.count('$#!'))+" messages we will definitely look into it Please wait for us to take action")
            return render(request,'contact_us.html')
        else:
            message="$#!  "+message
            Contact_Messages.objects.create(username=username,user_firstname=firstname,
            user_lastname=lastname,user_mobilenumber=number,message=message)
            messages.success(request, "You Message has been sent we will definitely respond to it via Email within in a day check out your Email")
            return render(request,'contact_us.html')
    else:
        return render(request,"contact_us.html")'''

def forgotpassword(request):
    # function for otp generation
    if(request.method=="POST"):
        otp=""
        for _ in range(6):
            otp+=str(r.randint(1,9))
        receiver=request.POST["receiver_name"]
        if Authentication.objects.filter(username=receiver).exists():
            userdetails=Authentication.objects.get(username=receiver)
            firstname=userdetails.first_name
            send_mail('[College Toolkit]Please Reset Your Password','Hello '+ str(firstname) +' , Warm Regards \n'+'\nIt seems you have forgotten your Account Password\n'+'\nBut don\'t worry You can Reset your Password  Using OTP below :\n'+'\n\t\t\t\t\tYour Otp to reset password is '+str(otp)+'\n\n\n\nThanks,\nThe College Toolkit Team','owner.collegetoolkit@gmail.com',
            [receiver,],fail_silently=False)
            otpdict[receiver]=otp
            attemptsdict[receiver]=3
            messages.info(request,"OTP has been sent to your registered Email Id or Username")
            return render(request,"otp_verification.html",{'name':receiver})
        else:
            messages.error(request,"Username doesn't exist.Please Enter Valid Username")
            return redirect("forgotpassword")
    else:
        return render(request,'forgotpassword.html')

def verifyotp(request):
    if(request.method=="POST"):
        user_otp=request.POST["user_otp"]
        receiver=request.POST["receiver"]
        try:
            otp=otpdict[receiver]
            if attemptsdict[receiver]>0:

                if(otp==user_otp):
                    del(otpdict[receiver])
                    attemptsdict[receiver]=0
                    return render(request,"change_passwd.html",{'name':receiver})
                else:
                    messages.error(request,"Otp is not matched Please Try Again")
                    atemptstr="Remaining Attempts : "+str(attemptsdict[receiver])
                    attemptsdict[receiver]-=1
                    return render(request,"otp_verification.html",{'name':receiver,'attempts':atemptstr})
            elif attemptsdict[receiver]==0:
                messages.error(request,"Otp Attempts limit reached . Please Generate Again")
                return redirect("forgotpassword")
        except KeyError:
            messages.error(request,"The otp generated has expired or deleted Please regenerate again")
            return redirect("forgotpassword")
    else:
        return render(request,"otp_verification.html")

def changepassword(request):
    if(request.method=="POST"):
        requested_user=request.POST["change_requested_user"]
        passwd=request.POST["npasswd"]
        cnfrmpasswd=request.POST["cnfrmpasswd"]
        if passwd==cnfrmpasswd:
            user=Authentication.objects.get(username=requested_user)
            user.set_password(passwd)
            user.save()
            auth.logout(request)
            firstname=user.first_name
            send_mail('[College Toolkit]Password Changed','Hello '+str(firstname)+' , Security Threat \n'+'\nYour password for the the account '+str(requested_user[:3])+'*'*int(len(str(requested_user)))+str(requested_user[::-1][:3][::-1]) +' has changed recently \n'+'\nIf you don\'t change your password contact us Immediately with your details'+'\n\n If this was you simply ignore this email '+'\n\n\n\nThanks,\nThe College Toolkit Team','owner.collegetoolkit@gmail.com',
            [requested_user,],fail_silently=False)
            messages.success(request,"Your password has been successfully changed Please login again")
            return redirect("login")
        else:
            messages.warning(request,"Passwords Not Matched")
            return render(request,"change_passwd.html",{'name':requested_user})
    else:
        return render(request,"change_passwd.html")

def changepasswordafterlogin(request):
    if request.method == "POST":
        curpasswd=request.POST["oldpasswd"]
        username=request.user
        userauth=auth.authenticate(username=username,password=curpasswd)
        if userauth is None:
            messages.error(request,"Current Password not matched Please try again or reset it by signing out")
            return redirect('changepasswordafterlogin')
        else:
            passwd=request.POST["newpasswd"]
            cnfrmpasswd=request.POST["cnfrmpasswd"]
            if passwd==cnfrmpasswd:
                user=Authentication.objects.get(username=username)
                user.set_password(passwd)
                user.save()
                auth.logout(request)
                firstname=user.first_name
                send_mail('[College Toolkit]Password Changed','Hello '+str(firstname)+' , Security Threat \n'+'\nYour password for the the account '+str(username)+' has changed recently \n'+'\nIf you don\'t change your password contact us Immediately with your details'+'\n\n If this was you simply ignore this email '+'\n\n\n\nThanks,\nThe College Toolkit Team','owner.collegetoolkit@gmail.com',
                [username,],fail_silently=False)
                messages.success(request,"Your password has been successfully changed Please login again")
                return redirect("login")
            else:
                messages.error(request,"Passwords not matched Please try again")
                return redirect('changepasswordafterlogin')
    else:
        return render(request,'chngpasswdaftrlgn.html')

def deleteaccount(request):
    if request.method=="POST":
        username=request.user

        userpasswd=request.POST['reqpasswd']

        userauth=auth.authenticate(username=username,password=userpasswd)

        if userauth is None:
            messages.error(request,'Password not matched with your account')

            return render(request,'deleteaccount.html',{'username':username})

        else:
            auth.logout(request)

            user=Authentication.objects.get(username=username)

            deletedtuple=user.delete()

            totalsavings=deletedtuple[0]

            messages.warning(request,'we have deleted '+str(totalsavings)+' fields of you , If you face any problems feel free to contact us')
            return redirect("/")


    else:
        return render(request,'deleteaccount.html',{'username':request.user})

def checkusername(request):
    username = request.GET['username']

    if Authentication.objects.filter(username=username).exists():
            time.sleep(2)
            data = {
                'error':True,
                'msg':'Username already exists Please try again',
            }
            return JsonResponse(data)
    
    else:
        otp=""
        for i in range(6):
            otp+=str(r.randint(1,9))
        time.sleep(1)
        print(otp)
        # send_mail('[College Toolkit]Verify Email','Please give the below OTP in order to verify your account registered with College Toolkit'+'\nOTP is '+str(otp)+'\n\n\n\nThanks,\nThe College Toolkit Team','owner.collegetoolkit@gmail.com',
        #         [username,],fail_silently=False)
        registerotpdict[username] = otp

        data = {
            'error':False,
            'msg':'OTP has been sent to your mail',
        }

        return JsonResponse(data)

def verifyregistrationotp(request):
    otp = request.GET['registerotp']

    username = request.GET['username']

    if username in registerotpdict.keys():
        time.sleep(2)
        if registerotpdict[username] == otp:
            data = {
                'error':False,
            }
            del(registerotpdict[username])
        else:
            data = {
                'error':True,
                'msg':'OTP is not matched or Invalid Please try again'
            }
    else:
        time.sleep(1)
        data = {
            'error':True,
            'msg':'OTP is not generated for this mail Please generate again'
        }

    return JsonResponse(data)

def checkloginusername(request):
    username = request.GET['username']

    time.sleep(1)

    if Authentication.objects.filter(username=username).exists():
        data = {
            'error':False
        }
    else:
        data = {
            'error':True,
            'msg':"Username doesn't exists or has been deleted by supervisor \n please try again if the problem persists contact supervisor"
        }

    return JsonResponse(data)
