from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.utils import timezone
from PIL import Image
from django.urls import reverse


from django.dispatch import receiver


# Create your models here.

class contact(models.Model):
    name = models.CharField(max_length=120)
    email= models.EmailField()
    phone= models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    discription = models.CharField(blank= True,max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)
    postimage   = models.ImageField(blank=True, upload_to ='images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like =  models.ManyToManyField(User, related_name='blog_like',blank=True)
    
    def number_of_likes(self):
        return self.like.count()
    
    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
class BlogComment(models.Model):
    blogpost_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)
    def get_date(self):
        time = datetime.now()
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        else:
            if self.created_at.month == time.month:
                return str(time.day - self.created_at.day) + " days ago"
            else:
                if self.created_at.year == time.year:
                    return str(time.month - self.created_at.month) + " months ago"
        return self.created_at
    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]
class profile(models.Model):
    user  = models.OneToOneField(User,  on_delete=models.CASCADE)
    image   = models.ImageField(default='default.png',upload_to='profile_pics',blank=True)
    caption = models.TextField()
    

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super(profile, self).save(*args, **kwargs)



        img = Image.open(self.image.path)

        if img.height > 800 or img.width >600:
            output_size = (800,600)
            img.thumbnail(output_size)
            img.save(self.image.path)


#@receiver(post_save, sender=User)
#def create_or_update_user_profile(sender, instance, created, **kwargs):
 #   if created:
  #      profile.objects.create(user=instance)
   # instance.profile.save()
    


