from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .dashboard.views import ProfilDosenView, JadwalTerdekatView
from .mata_kuliah.views import MataKuliahViewSet
from .kelas.views import KelasViewSet
from .jadwal.views import JadwalKelasViewSet
from .presensi.views import detail_jadwal_dan_mahasiswa, set_presensi_status

router = DefaultRouter()

router.register(r'mata-kuliah', MataKuliahViewSet, basename='admin-mata_kuliah')
router.register(r'kelas', KelasViewSet, basename='kelas')
router.register(r'jadwal', JadwalKelasViewSet, basename='admin-jadwal_kelas')

urlpatterns = [
    path('profil-dosen/', ProfilDosenView.as_view(), name='profil-dosen'),
    path('jadwal-terdekat/', JadwalTerdekatView.as_view(), name='jadwal-terdekat'),
    path('presensi/<int:jadwal_id>/', detail_jadwal_dan_mahasiswa, name='detail_jadwal_dan_mahasiswa'),
    path('presensi/<int:presensi_id>/set-status/', set_presensi_status, name='set_presensi_status'),



    path('', include(router.urls)),
]
