from django.urls import path
from .views import MapView  # Import your map view

urlpatterns = [
    # project urls
    path('map/', MapView.as_view(), name='map'),  # Define URL pattern for map view
    # Add other URL patterns as needed
]
