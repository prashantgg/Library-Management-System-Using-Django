from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib.auth import authenticate, login, logout
from.import models
from .decorators import has_to_be_librarian, has_to_be_user



@login_required
def dashboard(request):

    return render(request, "lms/dashboard.html")

def home(request):
    return render(request, "lms/home.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request, "User Loged In Successfully")
            return redirect("lms:dashboard", permanent=True)
        else:
            messages.error(request,"Please enter the valid username or password")
            return redirect("lms:login_user",permanent=True)
    return render(request, "lms/login_page.html")


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        
        # Check if username and password length is greater than or equal to 6
        if len(username) < 6 or len(password) < 6:
            messages.error(request, "Username and password must be at least 6 characters long.")
            return redirect("lms:signup_user",permanent=True)
        
        # Password validation
        if not re.search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', password):
            messages.error(request, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@$!%*?&).")
            return redirect("lms:signup_user",permanent=True)

            # Check if user with the same username
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Person with the username | {username} | already exists.")
            return redirect("lms:signup_user",permanent=True)
        else:
        # Create new user
            user = User.objects.create_user(username=username, email=None, password=password)
            user.save()
            messages.success(request, "User created successfully.")
            return redirect("lms:signup_user", permanent=True)

    return render(request, "lms/signup_user.html")


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("lms:login_user", permanent=True)


@login_required
def update_profile(request):
    if request.method == "POST":
        f_name = request.POST.get("First Name")
        l_name = request.POST.get("Last Name")
        email = request.POST.get("Email")
        phone_number = request.POST.get("Phone Number")
        user = request.user

        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, "Phone number must be exactly 10 digits and numeric.")
            return redirect("lms:update_profile")
        
        user.first_name = f_name
        user.last_name = l_name
        user.email = email
        user.save()
 
        
        # Check if the profile exists
        if models.Profile.objects.filter(user=user).exists():
            # Profile exists, update it
            profile = models.Profile.objects.get(user=user)
            profile.phone_number = phone_number
            profile.save()
        else:
            # Profile does not exist, create it
            models.Profile.objects.create(user=user, phone_number=phone_number)
        
        return redirect('lms:update_profile')  # or any other success URL

    
    return render(request, "lms/update_profile.html")

@login_required
@has_to_be_librarian
def add_books(request):
    if request.method == "POST":
        book_name = request.POST.get("book_name")
        book_author = request.POST.get("book_author")
        c_class = request.POST.get("c_class")
        book_stock = request.POST.get("stock")
        book_description = request.POST.get("description")
        book_category = request.POST.get("category")
        book =  models.Book.objects.create(book_name=book_name,book_author=book_author,college_class= c_class, book_stock=book_stock,description=book_description,category=book_category)
        for i in range(0,int(book_stock)):
            models.BookISBN.objects.create(book=book)
        messages.success(request, "Books added successfully, auto added ISBNs")
        return redirect("lms:add_books")
    return render(request, "lms/add_books.html")

@login_required
def view_books(request):#for displaying books


    book = models.Book.objects.all()
    context={
        "book":book
    }
    return render(request, "lms/view_books.html",context)
@login_required
def view_books_user(request):#for displaying books


    book = models.Book.objects.all()
    context={
        "book":book
    }
    return render(request, "lms/view_books_user.html",context)

@login_required
@has_to_be_librarian
def delete_books(request, book_id):
    book = models.Book.objects.get(id=book_id)
    book.delete()
    messages.success(request, f"Book : {book} || has been deleted ")
    return redirect("lms:view_books")


@login_required
@has_to_be_librarian
def detail_books(request, book_id):
    book = models.Book.objects.get(id=book_id)
    context = {
        "book":book
    }
    return render(request, "lms/detail_books.html",context)
@login_required
@has_to_be_librarian
def update_books(request, book_id):
    if request.method == "POST":
        book_name = request.POST.get("book_name")
        book_author = request.POST.get("book_author")
        c_class = request.POST.get("c_class")
        book_stock = request.POST.get("stock")
        book_description = request.POST.get("description")
        book_category = request.POST.get("category")

        book = models.Book.objects.get(id=book_id)
        book.book_name = book_name
        book.book_author = book_author
        book.college_class = c_class
        book.book_stock = book_stock
        book.description = book_description
        book.category = book_category
        book.save()
        messages.success(request, f"Book : {book} || has been updated ")
        return redirect ("lms:view_books")
    books = models.Book.objects.get(id=book_id)
    context ={
        "book_name":books.book_name,
        "book_author":books.book_author,
        "book_class":books.college_class,
        "book_stock":books.book_stock,
        "book_description":books.description,
        "book_category":books.category

    }

   
    return render(request, "lms/update_books.html",context)

@require_http_methods(["POST"]) 
@login_required

def profile_pic_upload(request):
    if request.method == "POST":
        profile_pic = request.FILES.get("profile_img")
        if profile_pic:
            try:
                profile = models.Profile.objects.get(user=request.user)
            except models.Profile.DoesNotExist:
                profile = models.Profile.objects.create(user=request.user)
            if profile:
                profile.profile_pic = profile_pic
                profile.save()
                messages.success(request, "Porfile picture updated successfully")
                return redirect("lms:update_profile")
            else:
                messages.error(request, "Profile not found")
                return redirect("lms:update_profile")

        else:
            messages.error(request, "Error updating profile picture")
            return redirect("lms:update_profile")
        
@login_required
def change_password(request):
    if request.method == "POST":
        o_pass = request.POST.get("o_pass")
        n_pass = request.POST.get("n_pass")
        c_pass = request.POST.get("c_pass")
        user = request.user
        if not re.search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', n_pass):
            messages.error(request, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@$!%*?&).")
            return redirect("lms:update_profile",permanent=True)
        
        if n_pass == c_pass:
            if user.check_password(o_pass):
                user.set_password(n_pass)
                user.save()
                messages.success(request, "Password has been changed successfully")
                return redirect ("lms:update_profile")
            else:
                messages.warning(request, "Your old password is wrong write the correct one")

        else:
                messages.error(request, "New password and confrim password did not match")
    return render (request, "lms/update_profile.html")



@login_required
@has_to_be_user
def add_book_request(request, book_id):
    book = models.Book.objects.get(id=book_id)
    
    # Check if the user has already requested this book
    if models.BookRequest.objects.filter(user=request.user, book=book).exists():
        messages.error(request, "Book Already Requested")
        return redirect("lms:view_books_user")
    
    # Create a new book request
    models.BookRequest.objects.create(user=request.user, book=book)
    messages.success(request, "Book Requested Successfully")
    return redirect("lms:view_books_user")

@login_required
@has_to_be_librarian
def book_request_librarian(request):
    book_request_librarian = models.BookRequest.objects.all()
    context = {"book_req": book_request_librarian
               }
    return render (request, "lms/book_request_librarian.html", context)

@login_required
@has_to_be_librarian
def checkout_book(request):
    return render(request, "lms/checkout_book.html")

