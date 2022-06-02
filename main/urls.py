from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main.views import DownloadView,OperationalListView, UploadFile,OperationalRegisterView,ClientRegisterView,UserListView,LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload', UploadFile.as_view() ),
    path('register/ops', OperationalRegisterView.as_view() ),
    path('ops', OperationalListView.as_view() ),
    path('register/client', ClientRegisterView.as_view() ),
    path('user', UserListView.as_view() ),
    path('login', LoginView.as_view() ),
    path('download/<int:pk>', DownloadView.as_view() ),
    path('list_updated_files', OperationalListView.as_view() ),
    #  path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]
# <int:pk>'



if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)