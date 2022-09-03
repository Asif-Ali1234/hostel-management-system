from django.urls import path,include
from . import views

urlpatterns = [
    path('createroom',views.createroom,name="createroom"),
    path('acceptleave/<str:mail>',views.acceptleave,name="accept_student_leave"),
    path('rejectleave/<str:mail>',views.rejectleave,name="reject_student_leave"),
    path('assignroom',views.assignroom,name="assignroom"),
    path('applyleave',views.applyleave,name="applyleave"),
    path('applygrievance',views.applygrievance,name="applygrievance"),
    path('acceptgrievance/<str:mail>',views.acceptgrievance,name="acceptgrievance"),
    path('rejectgrievance/<str:mail>',views.rejectgrievance,name="rejectgrievance"),
    path('completegrievance/<str:mail>',views.completegrievance,name="completegrievance"),
    path('upload_bill',views.upload_bill,name="upload_bill"),
    path('accept_bill_payment/<str:mail>',views.accept_bill_payment,name="accept_bill_payment"),
    path('reject_bill_payment/<str:mail>',views.reject_bill_payment,name="reject_bill_payment"),
    path('assignbill',views.assignbill,name="assignbill")
]