from . import views

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

app_name = 'main'

urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product_list'),
]