from django.shortcuts import render
from django.http import HttpResponse
from details.models import Coursedetails
from details.models import Studentdetails
from details.models import Enrollment
from django.db import connection
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min, Sum

# Create your views here.

@login_required
def home(request):
    student = Studentdetails.objects.all()
    studentcount = len(student)
    averagegpa = Studentdetails.objects.aggregate(Avg('gpa'))
    seniorsum = Studentdetails.objects.filter(year='Senior').count()
    juniorsum = Studentdetails.objects.filter(year='Junior').count()
    sophomoresum = Studentdetails.objects.filter(year='Sophomore').count()
    freshmansum = Studentdetails.objects.filter(year='Freshman').count()
    context = {'enrolled':studentcount, 'averagegpa':averagegpa.get('gpa__avg'), 'seniorsum':seniorsum, 'juniorsum':juniorsum, 'sophomoresum':sophomoresum, 'freshmansum':freshmansum}
    return render(request, 'details/home.html', context)
    
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@login_required    
def studentdetails(request):
    student = Studentdetails.objects.all() # SELECT * FROM DETAILS_STUDENTDETAILS
    paginator = Paginator(student, 10)
    page = request.GET.get('page')
    studentdata = paginator.get_page(page)
    
    return render(request, 'details/studentdetails.html', {'data':studentdata})
    
@login_required    
def coursedetails(request):
    course = Coursedetails.objects.all() # SELECT * FROM DETAILS_COURSEDETAILS
    paginator = Paginator(course, 10)
    page = request.GET.get('page')
    coursedata = paginator.get_page(page)
    
    return render(request, 'details/coursedetails.html', {'data':coursedata})

@login_required     
def enrollment(request):
    student = Studentdetails.objects.all()
    course = Coursedetails.objects.all()
    enrolldata = Enrollment.objects.all()
    if('lastname' in request.session):
        enrolldata = Enrollment.objects.filter(lastname = request.session['lastname'])
    if('lname' in request.GET and 'cname' not in request.GET):
        lname = request.GET.get('lname')
        request.session['lastname'] = lname
        return HttpResponse('Success')
    if('lname' in request.GET and 'cname' in request.GET):
        lname = request.GET.get('lname')
        cname = request.GET.get('cname')
        enrolldata = Enrollment.objects.filter(lastname = lname)
        for row in enrolldata:
            if (row.enrollment == cname):
                return HttpResponse('Error')
        if len(enrolldata) >= 3:
            return HttpResponse('Error')
        else:
            newdata = Enrollment(lastname = lname, enrollment = cname)
            newdata.save()
        return HttpResponse("Success")
    return render(request, 'details/enrollment.html', {'student':student, 'course':course, 'enrollment':enrolldata})