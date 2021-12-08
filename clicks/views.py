from django.shortcuts import render
from os import name
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


# Create your views here.
#Function login in the user
def user_login(request):
    message = 'Sign In!'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request,f" Hello, {username} welcome to clicksgram")
            return redirect('homepage')
        else:
            messages.success(request,"sorry,try login in again")
            return render(request,'registration/login.html')
    else:
        return render(request, 'registration/login.html',{"message":message})
#Function for signing out
def user_logout(request):
    logout(request)
    messages.success(request,("You have sussessfully signed out"))
    return redirect('login')
# Function for creating an account

def user_signup(request):
    
    message = 'CREATE ACCOUNT !'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,("Your account has  succesfully been created!"))
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html',{"message":message, "form":form})
# function for displaying all photos


def homepage(request):
    images = Image.objects.all()
    return render(request, 'home.html', {"images":images})

#function for displaying user profile

def profile(request):
    current_user = request.user
    images = Image.objects.filter(user_id=current_user.id)
    profile = Profile.objects.filter(username=current_user).first()
    return render(request,'profile.html', {"images":images, "profile":profile})
#function for displayinf likes per photo
def like_image(request, id):
    likes = Likes.objects.filter(image_id=id).first()
    if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():
        likes.delete()
        image = Image.objects.get(id=id)
        if image.total_likes == 0:
            image.total_likes = 0
            image.save()
        else:
            image.total_likes -= 1
            image.save()
        return redirect('/')
    else:
        likes = Likes(image_id=id, user_id=request.user.id)
        likes.save()
        image = Image.objects.get(id=id)
        image.total_likes = image.total_likes +1
        image.save()
        return redirect('/')
#function for displaying comments per photo
def image_comments(request, id):
    image = Image.objects.get(id=id)
    related_images = Image.objects.filter(user_id=image.user_id)
    title = image.name
    if Image.objects.filter(id=id).exists():
        comments = Comments.objects.filter(image_id=id)
        return render(request,'photos.html',
        {'image':image, 
        'comments':comments, 
        'images':related_images,
        'title':title}) 
    else:
        return redirect('/')
#function for saving comments
def save_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        image_id = request.POST['image_id']
        image = Image.objects.get(id=image_id)
        user = request.user
        comment = Comments(comment=comment, image_id=image_id, user_id=user.id)
        comment.save_comment()
        image.total_comments = image.total_comments + 1
        image.save()
        return redirect('/photocomment/'+str(image_id))
    else:
        return redirect('/')
#function for displaying a specific user
def user_profile(request,id):

    if User.objects.filter(id=id).exists():
        user = User.objects.get(id=id)
        images = Image.objects.filter(user_id=id)
        profile = Profile.objects.filter(username_id=id).first()
        return render(request,'user.html',{'images':images,'profile':profile, 'user':user})
    else:
        return redirect('/')
#function for searching for a photo

def search_images(request):
    
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get ('search').lower()
        images = Image.search_by_image(search_term)
        message = f'{search_term}'
        title = message

        return render(request, 'search.html', {'success':message, 'images':images, "title":title})
    else:
        message = 'Invalid Search'
        return render(request,'search.html',{'danger':message})
#Function for updating the user profile

def update_profile(request):
    if request.method =='POST':
        current_user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        bio = request.POST['bio']
    

        user = User.objects.get(id=current_user.id)

        if Profile.objects.filter(user_id=current_user.id).exists():
            profile = Profile.objects.get(user_id=current_user.id)
            profile.bio = bio
            profile.save()
        else:
            profile = Profile.objects.get(user_id=current_user.id, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        return redirect('/profile',{'success': 'Profile Update Successfull'})
    else:
        return render(request,'profile.html',{'danger': 'Failed to update profile'})
def save_image(request):
    """Function for saving image"""
    if request.method == 'POST':
        image_name = request.POST['image_name']
        image_caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        image_url = image_file['url']
        image = Image(image_name=image_name,image_caption=image_caption,image=image_url,user_id=request.POST['user_id'])
        image.save_image()
        return redirect('/homepage',{'success': 'Image Upload Successful'})
    else:
        return render(request,'profile.html', {'danger': 'Image upload Failed'})        
 
