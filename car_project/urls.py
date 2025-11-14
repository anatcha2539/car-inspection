from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# (1) Import ตัวแยกทางของเรามา
from inspection.views import login_router_view 

admin.site.site_header = "ระบบตรวจเช็คสภาพรถ"
admin.site.site_title = "Vehicle Admin"
admin.site.index_title = "ยินดีต้อนรับผู้ดูแลระบบ"
admin.site.site_url = "/dashboard-admin/"

# (2) เก็บหน้า Admin จริงไว้ในตัวแปร
real_admin_index = admin.site.index

# (3) ไฮแจ็คหน้า /admin/ ให้เป็นทางแยก (นี่คือท่าไม้ตาย)
admin.site.index = login_router_view

urlpatterns = [
    # (4) สร้าง "ประตูหลัง" (admin/main/) ให้ชี้ไปที่หน้า Admin จริง
    path('admin/main/', real_admin_index, name='admin_main_index'),
    
    # (5) โหลด URL อื่นๆ ของ Admin (เช่น login, logout, ฯลฯ)
    path('admin/', admin.site.urls),
    
    # (6) ดักหน้าแรกสุด ('') ให้เด้งไปหน้า Admin Login
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)),
    
    # (7) โหลด URL ของแอพ (เช่น /dashboard/, /inspect/)
    path('', include('inspection.urls')), 
]