from django.contrib import admin
from django.urls import path,include

from article.views import anasayfa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',anasayfa, name='anasayfa'),
    path('posts/',include('article.urls')),

]
