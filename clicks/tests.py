from django.test import TestCase
from .models import Profile, Image,Likes
from django.contrib.auth.models import User


class ProfileTestClass(TestCase):
    from django.contrib.auth.models import User
    def setUp(self):
        self.user = User(username='synthia')
        self.user.save()
        self.profile = Profile(id=1,user=self.user,profilepic='foodA.jpg',bio='am synthia', name='person')
        self.profile.save_profile()
    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        Image.objects.all().delete()
    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
        self.assertTrue(isinstance(self.profile, Profile))
    def test_save_method(self):
        self.profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile) > 0)

class ImageTestClass(TestCase):
    def setUp(self):
        self.profile = Profile(user=User(username='synthia'))
        self.profile.user.save()
        self.profile.save()
        self.image = Image(user=self.profile,image='foodA.jpg', name='person', caption='i love it')
        self.image.save_image()
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))
        self.assertTrue(isinstance(self.image, Image))
    def test_save_image(self):
        self.image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)
   

        
