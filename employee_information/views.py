from django.shortcuts import redirect, render
from django.http import HttpResponse
# from employee_information.models import Department, Position, Employees
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json




from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import base64
from django.core.files.base import ContentFile
from .models import Staff
from .serializers import StaffRegistrationSerializer, StaffSerializer, StaffUpdateSerializer
# from rest_framework.permissions import IsAuthenticated

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    lookup_field = 'employee_number'  # Use employee_number as the primary identifier
    serializer_class = StaffSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return StaffRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return StaffUpdateSerializer
        return StaffSerializer
    
    def destroy(self, request, *args, **kwargs):
        employee_number = kwargs.get('employee_number')
        staff_instance = self.get_object()
        try:
            staff_instance.delete()  # Perform the deletion
            return Response({'status': 'success'}, status=status.HTTP_200_OK)  # Return 200 with JSON
        except Exception as e:
            return Response({'status': 'failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def handle_id_photo_upload(self, photo_file):
        """
        Converts the uploaded photo file to a Base64-encoded string.
        """
        if photo_file:
            photo_data = photo_file.read()
            return base64.b64encode(photo_data).decode('utf-8')
        return None

    def perform_create(self, serializer):
        """
        Handles the creation of a new staff record and processes the id_photo field.
        """
        id_photo = self.request.FILES.get('id_photo')  # Get the file from the request
        if id_photo:
            base64_photo = self.handle_id_photo_upload(id_photo)  # Convert to Base64
            serializer.save(id_photo=base64_photo)  # Save the Base64 string as id_photo
        else:
            serializer.save()  # Save normally if no photo is uploaded

    def perform_update(self, serializer):
        """
        Handles updating an existing staff record, including the id_photo.
        """
        id_photo = self.request.FILES.get('id_photo')
        if id_photo:
            base64_photo = self.handle_id_photo_upload(id_photo)
            serializer.save(id_photo=base64_photo)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'status': 'success', 'staff': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'status': 'success', 'staff': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def list_staff(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put', 'patch'])
    def update_staff(self, request, employee_number=None):
        return super().update(request, employee_number)

    @action(detail=True, methods=['get'])
    def retrieve_staff(self, request, employee_number=None):
        return self.retrieve(request, employee_number)
        








# employees = [

#     {
#         'code':1,
#         'name':"John D Smith",
#         'contact':'09123456789',
#         'address':'Sample Address only'
#     },{
#         'code':2,
#         'name':"Claire C Blake",
#         'contact':'09456123789',
#         'address':'Sample Address2 only'
#     }

# ]
# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.
@login_required
def home(request):
    context = {
        'page_title':'Home',
        'employees':employees,
        # 'total_department':len(Department.objects.all()),
        # 'total_position':len(Position.objects.all()),
        # 'total_employee':len(Employees.objects.all()),
    }
    return render(request, 'employee_information/home.html',context)


# def about(request):
#     context = {
#         'page_title':'About',
#     }
#     return render(request, 'employee_information/about.html',context)

# # Departments
# @login_required
# def departments(request):
#     department_list = Department.objects.all()
#     context = {
#         'page_title':'Departments',
#         'departments':department_list,
#     }
#     return render(request, 'employee_information/departments.html',context)
# @login_required
# def manage_departments(request):
#     department = {}
#     if request.method == 'GET':
#         data =  request.GET
#         id = ''
#         if 'id' in data:
#             id= data['id']
#         if id.isnumeric() and int(id) > 0:
#             department = Department.objects.filter(id=id).first()
    
#     context = {
#         'department' : department
#     }
#     return render(request, 'employee_information/manage_department.html',context)

# @login_required
# def save_department(request):
#     data =  request.POST
#     resp = {'status':'failed'}
#     try:
#         if (data['id']).isnumeric() and int(data['id']) > 0 :
#             save_department = Department.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
#         else:
#             save_department = Department(name=data['name'], description = data['description'],status = data['status'])
#             save_department.save()
#         resp['status'] = 'success'
#     except:
#         resp['status'] = 'failed'
#     return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
# def delete_department(request):
#     data =  request.POST
#     resp = {'status':''}
#     try:
#         Department.objects.filter(id = data['id']).delete()
#         resp['status'] = 'success'
#     except:
#         resp['status'] = 'failed'
#     return HttpResponse(json.dumps(resp), content_type="application/json")

# # Positions
# @login_required
# def positions(request):
#     position_list = Position.objects.all()
#     context = {
#         'page_title':'Positions',
#         'positions':position_list,
#     }
#     return render(request, 'employee_information/positions.html',context)
# @login_required
# def manage_positions(request):
#     position = {}
#     if request.method == 'GET':
#         data =  request.GET
#         id = ''
#         if 'id' in data:
#             id= data['id']
#         if id.isnumeric() and int(id) > 0:
#             position = Position.objects.filter(id=id).first()
    
#     context = {
#         'position' : position
#     }
#     return render(request, 'employee_information/manage_position.html',context)

# @login_required
# def save_position(request):
#     data =  request.POST
#     resp = {'status':'failed'}
#     try:
#         if (data['id']).isnumeric() and int(data['id']) > 0 :
#             save_position = Position.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
#         else:
#             save_position = Position(name=data['name'], description = data['description'],status = data['status'])
#             save_position.save()
#         resp['status'] = 'success'
#     except:
#         resp['status'] = 'failed'
#     return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
# def delete_position(request):
#     data =  request.POST
#     resp = {'status':''}
#     try:
#         Position.objects.filter(id = data['id']).delete()
#         resp['status'] = 'success'
#     except:
#         resp['status'] = 'failed'
#     return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
# Employees
def employees(request):
    # employee_list = Employees.objects.all()
    context = {
        'page_title':'Employees',
        # 'employees':employee_list,
    }
    return render(request, 'employee_information/employees.html',context)
@login_required
def manage_employees(request):
    employee = {}
    # departments = Department.objects.filter(status = 1).all() 
    # positions = Position.objects.filter(status = 1).all() 
    # if request.method == 'GET':
    #     data =  request.GET
    #     id = ''
    #     if 'id' in data:
    #         id= data['id']
    #     if id.isnumeric() and int(id) > 0:
            # employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employee,
    #     'departments' : departments,
    #     'positions' : positions
    }
    return render(request, 'employee_information/manage_employee.html',context)

@login_required
def save_employee(request):
    data =  request.POST
    resp = {'status':'failed'}
    if (data['id']).isnumeric() and int(data['id']) > 0:
        check  = Employees.objects.exclude(id = data['id']).filter(code = data['code'])
    else:
        check  = Employees.objects.filter(code = data['code'])

    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            dept = Department.objects.filter(id=data['department_id']).first()
            pos = Position.objects.filter(id=data['position_id']).first()
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_employee = Employees.objects.filter(id = data['id']).update(code=data['code'], firstname = data['firstname'],middlename = data['middlename'],lastname = data['lastname'],dob = data['dob'],gender = data['gender'],contact = data['contact'],email = data['email'],address = data['address'],department_id = dept,position_id = pos,date_hired = data['date_hired'],salary = data['salary'],status = data['status'])
            else:
                save_employee = Employees(code=data['code'], firstname = data['firstname'],middlename = data['middlename'],lastname = data['lastname'],dob = data['dob'],gender = data['gender'],contact = data['contact'],email = data['email'],address = data['address'],department_id = dept,position_id = pos,date_hired = data['date_hired'],salary = data['salary'],status = data['status'])
                save_employee.save()
            resp['status'] = 'success'
        except Exception:
            resp['status'] = 'failed'
            print(Exception)
            print(json.dumps({"code":data['code'], "firstname" : data['firstname'],"middlename" : data['middlename'],"lastname" : data['lastname'],"dob" : data['dob'],"gender" : data['gender'],"contact" : data['contact'],"email" : data['email'],"address" : data['address'],"department_id" : data['department_id'],"position_id" : data['position_id'],"date_hired" : data['date_hired'],"salary" : data['salary'],"status" : data['status']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_employee(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Employees.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_employee(request):
    employee = {}
    departments = Department.objects.filter(status = 1).all() 
    positions = Position.objects.filter(status = 1).all() 
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employee,
        'departments' : departments,
        'positions' : positions
    }
    return render(request, 'employee_information/view_employee.html',context)