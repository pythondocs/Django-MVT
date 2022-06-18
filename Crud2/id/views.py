from genericpath import exists
from multiprocessing import context
from urllib.request import Request
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView, View
from id.models import Person
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Create your views here.

def view(request):
     return render('home.html')


def welcome_page(request):
    return render(request, 'id/welcome.html')


def index(request):
    return render(request, 'id/home.html', context={})


def login(request):
    return render(request, 'id/login.html', context={})


def data(request):
    return render(request, 'id/table.html', context={})




# Registration Page
def form_data(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        company_name = request.POST['company']
        Email_id = request.POST['Email']
        phone_number = request.POST['Phone']
        password = make_password(request.POST['Password'])
        if Person.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "phone number already exists")
            return redirect('/')
        elif Person.objects.filter(Email_id=Email_id).exists():
            messages.error(request, "Email id already exists")
            return redirect('/')
        else:
            Person.objects.create(first_name=first_name,
                                  last_name=last_name, company_name=company_name,
                                  Email_id=Email_id, phone_number=phone_number, password=password)
            return redirect('/login/')

# create login form
def loginform(request):
    if request.method == 'POST':
        phone_number = request.POST['Phone']
        User_Password = request.POST['password']
        if Person.objects.filter(phone_number=phone_number).exists():
            obj = Person.objects.get(phone_number=phone_number)
            password = obj.password
            if check_password(User_Password, password):
                return redirect('/welcome/')
            else:
                return HttpResponse('password incorrect')
        else:
            return HttpResponse('phone number is not registered')

# Data import in Table
def dataform(request):
    person = Person.object.filter(is_active=True).order_by('id')
    return render(request, 'id/table.html', context={
        'Request': request,
        'Person': person,
    })
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
