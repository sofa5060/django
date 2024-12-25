from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage  # Ensure this import is present
from django.views.decorators.csrf import csrf_protect
from django.core.files.base import ContentFile
import base64
from .form import ImageUploadForm
from .models import ImageUpload
from django.contrib.auth.models import User
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Car, ImageUpload
from .form import ImageUploadForm
import os

@login_required
def home(request):
    cars = Car.objects.filter(user=request.user)  # Fetch all cars for the user
    return render(request, 'home.html', {'cars': cars})

@login_required
def add_car(request):
    if request.method == 'POST':
        car_count = Car.objects.filter(user=request.user).count()
        car_name = f"Car {car_count + 1}"

        car = Car.objects.create(name=car_name, user=request.user)
        return redirect('base:home')
    return render(request, 'add_car.html')

@login_required
def car_page_empty(request, car_id):
    car = Car.objects.get(id=car_id, user=request.user)
    return render(request, 'page_empty.html', {'car': car})

    return render(request, 'add_car.html')
@login_required
def car_page_one(request, car_id):
    car = Car.objects.get(id=car_id, user=request.user)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.source = 'manual'
            image.car = car  # Associate with the car
            image.save()
            return redirect('base:car_page_three', car_id=car.id)
    else:
        form = ImageUploadForm()
    return render(request, 'page_one.html', {'form': form, 'car': car})

@login_required
def car_page_two(request, car_id):
    car = Car.objects.get(id=car_id, user=request.user)
    images = ImageUpload.objects.filter(user=request.user, source='face_recognition', car=car)
    return render(request, 'page_two.html', {'images': images, 'car': car})

@login_required
def car_page_three(request, car_id):
    car = Car.objects.get(id=car_id, user=request.user)
    images = ImageUpload.objects.filter(user=request.user, source='manual', car=car)
    return render(request, 'page_three.html', {'images': images, 'car': car})

@login_required
def page_two(request, car_id):
    # Get the car object for the current user
    try:
        car = Car.objects.get(id=car_id, user=request.user)  # Ensure the car belongs to the user
    except Car.DoesNotExist:
        return render(request, 'page_two.html', {'error': 'Car not found or you do not own this car.'})

    # Folder path for images related to the user and car
    user_car_folder = os.path.join('media', 'unknown_faces', str(request.user.id), str(car.id))

    # Check if the user's car folder exists
    if os.path.exists(user_car_folder):
        for f in os.listdir(user_car_folder):
            file_path = os.path.join(user_car_folder, f)
            if os.path.isfile(file_path) and f.lower().endswith('.jpg'):
                # Check if the image is already saved in the database
                relative_path = f'unknown_faces/{request.user.id}/{car.id}/{f}'  # Path relative to MEDIA_ROOT
                if not ImageUpload.objects.filter(user=request.user, car=car, image=relative_path).exists():
                    # Save the image record in the database without moving the file
                    ImageUpload.objects.create(
                        user=request.user,
                        car=car,
                        image=relative_path,
                        source='face_recognition'
                    )

    # Fetch all images uploaded for face recognition by the current user and car
    images = ImageUpload.objects.filter(user=request.user, car=car, source='face_recognition')

    return render(request, 'page_two.html', {'images': images, 'car': car})

def logout_view(request):
    logout(request)
    return redirect('login')

def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})

@csrf_exempt
def upload_unknown_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        user_id = request.POST.get('user_id')
        car_id = request.POST.get('car_id')

        # Ensure the user and car exist
        user = User.objects.get(id=user_id)
        car = Car.objects.get(id=car_id, user=user)  # Ensure the car belongs to the user

        # Define the path where the image will be saved
        user_car_folder = os.path.join('media', 'unknown_faces', str(user.id), str(car.id))
        os.makedirs(user_car_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Save the image with the desired path
        fs = FileSystemStorage(location=user_car_folder)
        file_name = fs.save(image.name, image)
        file_url = fs.url(file_name)

        # Save the image record in the database
        relative_path = f'unknown_faces/{user.id}/{car.id}/{file_name}'  # Path relative to MEDIA_ROOT
        ImageUpload.objects.create(
            user=user,
            car=car,
            image=relative_path,
            source='face_recognition'
        )

        return JsonResponse({"message": "Image uploaded successfully", "file_url": file_url}, status=201)

    return JsonResponse({"error": "No image uploaded"}, status=400)


@login_required
def get_user_images(request, user_id, car_id):
    images = ImageUpload.objects.filter(user_id=user_id, car_id=car_id, source='manual').values("image", "uploaded_at")
    return JsonResponse(list(images), safe=False)