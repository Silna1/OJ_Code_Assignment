from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
import json

from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ImageSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


# Create your views here.

def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }

    return Response(api_urls)


class PhotoItemViews(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        print(user)
        image = request.data['image']
        category = Category.objects.get(id=request.data['category'])
        print(category)
        description = request.data['description'],

        image = Photo.objects.create(category=category,
                                     description=description, image=image)
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)

    def get(self, request):
        user = request.user
        photo = Photo.objects.filter(category__user=user)
        serializer = ImageSerializer(photo, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)


@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category is None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos, 'user': user}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
