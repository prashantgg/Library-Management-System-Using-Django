from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    is_librarian = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=30, default=" ")
    
    #if there is multiple roles
    # roles = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True) 


    profile_pic = models.ImageField(upload_to="profile_pic", blank=True, null=True) 

    '''blank = True means the field in form can be left emply and
    null= True means the value will be set null if the profile pic left empty'''
    
    created_at = models.DateTimeField(auto_now_add=True)
    '''auto_now_add = True means when the time when the object is added'''

    updated_at = models.DateTimeField(auto_now=True)
    '''auto_now = True means the time when the object is updated'''

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Book(models.Model):
    book_name = models.CharField(max_length=50)
    book_author = models.CharField(max_length=50)
    college_class = models.CharField(max_length=50)
    book_stock = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.book_name} by {self.book_author}"
    
class BookISBN(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name="isbn")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.book_name}| ISBN No : {self.id} "
    
class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name= "checkouts")
    book_isbn = models.ForeignKey(BookISBN, on_delete=models.DO_NOTHING, null= True, related_name="checkouts")
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    issued_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name ="checkouts_done")


    def set_expiry_date(self):
        self.expiry_date = self.created_at + datetime.timedelta(days=14)

    def set_issued_by(self,user):
        self.issued_by = user

    def __str__(self):
        return f"{self.book_isbn}-{self.user.username}"
    
    def save(self,*args,**kwargs):
        self.set_expiry_date()
        # self.set_issued_by()

        super(Checkout,self).save(*args, **kwargs)

class BookRequest (models.Model):
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING, related_name= "user")
    book = models.ForeignKey(Book,  on_delete= models.DO_NOTHING, related_name= "book")
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requested {self.book.book_name}"
