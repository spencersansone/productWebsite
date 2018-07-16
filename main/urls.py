from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product_list'),
    url(r'^api/products/$', views.ProductAPIList.as_view(), name="product_API_list"),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^verificationCode/$', views.verificationCode, name='verification_code'),
    url(r'^resendVerificationCode/$', views.resendVerificationCode, name='resend_verification_code'),
]