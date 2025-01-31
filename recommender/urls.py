from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet, OrderViewSet,
                    recommend_products, dashboard, get_chart_data, category_distribution, sales_trend, top_products)

# REST Framework Router
router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')

# URLs
urlpatterns = [
    path('', include(router.urls)),  
    path('recommend/', recommend_products,name='recommend-products'),  
    path('dashboard/', dashboard, name='dashboard'),  
    path('chart-data/', get_chart_data, name='chart-data'),  
    path('category-distribution/', category_distribution, name='category-distribution'),
    path('sales-trend/', sales_trend, name='sales-trend'),
    path('top-products/', top_products, name='top-products'),

]
