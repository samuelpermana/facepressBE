from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .profile.views import ProfilMahasiswaAPIView, MahasiswaProfileUpdateView
from .mata_kuliah.views import MataKuliahMahasiswaListAPIView, KelasViewSet

router = DefaultRouter()
router.register(r'kelas', KelasViewSet, basename='kelas')  # Fix here

urlpatterns = [
    path('profil-user/', ProfilMahasiswaAPIView.as_view(), name='profil-mahasiswa'),
    path('mata-kuliah/', MataKuliahMahasiswaListAPIView.as_view(), name='list-mata-kuliah'),
    path('profile/update/', MahasiswaProfileUpdateView.as_view(), name='mahasiswa-profile-update'),

    path('', include(router.urls)),
]
