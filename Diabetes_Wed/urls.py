from django.contrib import admin
from django.urls import path
from diabetes import views  # 確保你有匯入 views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.predict_view, name='predict'),  # 設首頁為預測功能
]