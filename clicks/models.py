from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField


#Model the user profile"""
class Profile(models.Model):
    profilepic = ImageField('image')
    bio = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    signup_date = models.DateTimeField(auto_now_add= True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    
    def __str__(self):
        return self.name

# Method for followers
    def total_followers(self):
        return self.followers.count()
    def save_profile(self):
        self.save()

 #Method for updating profile
    def update_profile(self, new):
        self.username = new.username
        self.bio = new.bio
        self.profilephoto = new.profilephoto
        self.save()

#Method for getting the users following
        @classmethod
        def get_following(cls, user):
            following = user.followers.all()
            users = []
            for profile in following:
                user = user.objects.get(profile = profile)
                users.append(user)
            return users

 #Method for returning specific user profile
        @classmethod
        def search_profile(cls, search_term):
            profiles = cls.objects.filter(username_icontains = search_term)
            return profiles

#Model for likes on a photo
class Likes(models.Model):
    likes = models.IntegerField(default=0)

  #Model for photos
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = ImageField('images')
    image_name = models.CharField(max_length=25)
    caption = models.CharField(max_length=150)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    likes = models.ForeignKey(Likes, on_delete=CASCADE, default=None)
    comment = models.CharField(max_length=150)
    time_posted = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

#Method for saving images
    def save_images(self):
        self.save()

#Method for deleting image
    def delete_image(self):
        self.delete()

#Method for adding user
    def like_image(self, user):
        self.likes.add(user)

 #Method for getting total number of image likes
    def gettottal_likes(self):
       return self.likes.count()

 #Method for updating photo caption
    def update_caption(self, caption):
        self.caption = caption
        self.save()

#Method for getting an image
    @classmethod
    def get_images(cls, users):
        posts = []
        for user in users:
            images = Image.objects.filter(user = user)
            for image in images:
                posts.append(image)
        return posts

#Method for getting comments on a photo
    @classmethod
    def get_comments(self):
        comments = Comments.objects.filter(image = self)
        return comments

 #Model class for comments on a photo
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment



