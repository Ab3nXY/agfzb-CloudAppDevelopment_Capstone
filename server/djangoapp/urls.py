from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('', views.index, name="index"),
    # path for about view
    path('about/', views.about, name="about-us"),
    # path for contact us view
    path('contact/', views.contact, name="contact-us"),
    # path for registration
    path('registration/', views.registration_request, name="registration"),
    # path for login
    path('login/', views.login_request, name="login"),
    # path for logout
    path('logout/', views.logout_request, name="logout"),

    path(route='', view=views.get_dealerships, name='index'),

    # path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:id>/', view=views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path('dealer/<int:id>/review', views.add_review, name='add_review'),
    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)