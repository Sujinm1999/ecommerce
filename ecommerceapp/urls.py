from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name='ecommerceapp'
urlpatterns = [
    path('login/',views.allProdCat,name='allProdCat'),
    path('<slug:c_slug>/',views.allProdCat,name='products_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/',views.ProdCatDetail,name='ProdCatDetail'),
    path('register/r',views.register,name='register'),
    path('',views.login,name='login'),
    path('logout',views.logout,name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)