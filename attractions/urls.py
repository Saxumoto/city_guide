from django.urls import path
from .views import (
    AttractionListView,
    AttractionDetailView,
    AttractionCreateView,
    AttractionUpdateView,
    AttractionDeleteView,
    RegisterView,
    MyAttractionListView,
    ReviewCreateView, # Imported new view
)

urlpatterns = [
    # AUTHENTICATION ROUTES
    path('register/', RegisterView.as_view(), name='register'),
    
    # USER DASHBOARD ROUTE
    path('my-contributions/', MyAttractionListView.as_view(), name='my_attractions'),
    
    # REVIEW ROUTE (Submit a review for a specific attraction ID)
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    
    # CRUD ROUTES
    path('', AttractionListView.as_view(), name='attraction_list'),
    path('add/', AttractionCreateView.as_view(), name='attraction_create'),
    path('<int:pk>/', AttractionDetailView.as_view(), name='attraction_detail'),
    path('<int:pk>/edit/', AttractionUpdateView.as_view(), name='attraction_update'),
    path('<int:pk>/delete/', AttractionDeleteView.as_view(), name='attraction_delete'),
]