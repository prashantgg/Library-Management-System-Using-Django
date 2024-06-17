from django.urls import path
from.import views
app_name = "lms"

urlpatterns = [
    path("lms/dashboard/", views.dashboard,name="dashboard"),
    path("", views.home,name="home"),
    path("accounts/login/", views.login_user, name="login_user"),
    path("accounts/sigup/", views.signup_user, name = "signup_user"),
    path("accounts/logout/", views.logout_user, name = "logout_user"),
    path("update-profile/", views.update_profile, name = "update_profile"),
    path("profile-picture/upload/", views.profile_pic_upload, name = "profile_pic_upload"),
    path("add-books/", views.add_books, name = "add_books"),
    path("view-books", views.view_books, name = "view_books"),
    path("delete-books-<int:book_id>", views.delete_books, name = "delete_books"),
    path("detail-books-<int:book_id>", views.detail_books, name = "detail_books"),
    path("update-books-<int:book_id>", views.update_books, name = "update_books"),
    path("request-books-<int:book_id>", views.add_book_request, name = "add_book_request"),
    path("change-password/", views.change_password, name = "change_password"),
    path("view-book-user/", views.view_books_user, name = "view_books_user"),
    path("bookrequest-librarian/", views.book_request_librarian, name = "book_request_librarian"),
    path("checkout-book/", views.checkout_book, name = "checkout_book"),
    
    

]

