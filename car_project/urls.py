from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = "ระบบจัดการยานพาหนะ (Vehicle System)"
admin.site.site_title = "Vehicle Admin"
admin.site.index_title = "ยินดีต้อนรับผู้ดูแลระบบ"
admin.site.site_url = "/dashboard-admin/"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)),
    path('', include('inspection.urls')),
]