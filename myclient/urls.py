from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('pojistenci/vyhledat/', views.vyhledat_pojistence, name='vyhledat_pojistence'),
    path('pojistenci/vytvor/', views.vytvor_pojistence, name='vytvor_pojistence'),
    path('vysledky_vyhledavani/', views.vysledky_vyhledavani, name='vysledky_vyhledavani'),
    path('myclient/', views.login_view, name='login'),
    path('smazat_pojistence/<int:cislo_pojistence>/', views.smazat_pojistence, name='smazat_pojistence'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('vytvor_bydliste_pro_klienta/<int:pojistenec_id>/', views.vytvor_bydliste_pro_klienta, name='vytvor_bydliste_pro_klienta'),
    path('vytvor_smlouvy/<int:pojistenec_id>/', views.vytvor_smlouvu, name='vytvor_smlouvy'),
    path('narozeniny_dnes/', views.narozeniny_dnes, name='narozeniny_dnes'),
    path('vypsat_vse/', views.vypsat_vse, name='vypsat_vse'),
    path('pojistenec/<int:cislo_pojistence>/', views.detail_pojistence, name='detail_pojistence'),
    path('editovat_pojistence/<int:cislo_pojistence>/', views.editovat_pojistence, name='editovat_pojistence'),

]

