from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Stock URLs
    path('stock/', views.StockListView.as_view(), name='stock'),
    path('stock/create/', views.StockCreateView.as_view(), name='stock_create'),
    path('stock/<int:pk>/', views.StockDetailView.as_view(), name='stock_detail'),
    path('stock/<int:pk>/update/', views.StockUpdateView.as_view(), name='stock_update'),
    path('stock/<int:pk>/delete/', views.StockDeleteView.as_view(), name='stock_delete'),
    
    # Warehouse URLs
    path('warehouses/', views.WarehouseListView.as_view(), name='warehouses'),
    path('warehouses/create/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouses/<int:pk>/update/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouses/<int:pk>/delete/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),
    
    # Movement URLs
    path('movements/', views.MovementListView.as_view(), name='movements'),
    path('movements/create/', views.MovementCreateView.as_view(), name='movement_create'),
    
    # Stock Taking URLs
    path('stock-taking/', views.StockTakingListView.as_view(), name='stock_taking'),
    
    # API endpoints
    path('api/warehouses/list/', views.WarehouseAPIListView.as_view(), name='warehouse_api_list'),
    path('api/warehouses/create/', views.WarehouseAPICreateView.as_view(), name='warehouse_api_create'),
    path('api/warehouses/<int:pk>/', views.WarehouseAPIDetailView.as_view(), name='warehouse_api_detail'),
    path('api/movements/create/', views.StockMovementAPICreateView.as_view(), name='movement_api_create'),
    path('api/movements/list/', views.StockMovementAPIListView.as_view(), name='movement_api_list'),
    path('api/movements/<int:movement_id>/', views.StockMovementAPIDetailView.as_view(), name='movement_api_detail'),
]
