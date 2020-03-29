from django.urls import path, include
from .views import IndexView, addReservation
urlpatterns = [
   # path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('reservate/', addReservation)
]