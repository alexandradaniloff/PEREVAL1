from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from project import views
from project.yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewset, basename='users')
router.register(r'coords', views.CoordsViewset, basename='coords')
router.register(r'levels', views.LevelViewset, basename='levels')
router.register(r'images', views.ImagesViewset, basename='images')
router.register(r'perevals', views.PerevalViewset, basename='perevals')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
urlpatterns += doc_urls
