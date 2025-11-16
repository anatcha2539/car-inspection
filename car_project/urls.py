from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from inspection.views import login_router_view 

admin.site.site_header = "ระบบตรวจเช็คสภาพรถ"
admin.site.site_title = "Vehicle Admin"
admin.site.index_title = "ยินดีต้อนรับผู้ดูแลระบบ"
admin.site.site_url = "/dashboard-admin/"
real_admin_index = admin.site.index
admin.site.index = login_router_view

urlpatterns = [
    path('admin/main/', real_admin_index, name='admin_main_index'),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)),
    path('', include('inspection.urls')),
    
]