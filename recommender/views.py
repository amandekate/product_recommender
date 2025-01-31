from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Count, F
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer

# ==================== API ViewSets ====================
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    pagination_class = None  

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('order_items__product')
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.annotate(
            total_products=Count('order_items', distinct=True)
        )

# ==================== Recommendation Logic ====================
@api_view(['POST'])
def recommend_products(request):
    try:
        product_ids = list(map(int, request.data.get('product_ids', [])))
    except (ValueError, TypeError):
        return Response(
            {"error": "Invalid product IDs format"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not product_ids:
        return Response(
            {"error": "No product IDs provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Find products bought together using OrderItem relationships
    recommendations = Product.objects.filter(
        order_items__order__order_items__product_id__in=product_ids
    ).exclude(
        id__in=product_ids
    ).annotate(
        frequency=Count('order_items__order', distinct=True)
    ).order_by('-frequency')[:5]

    serializer = ProductSerializer(recommendations, many=True)
    return Response(serializer.data)

# ==================== Dashboard & Analytics ====================
def dashboard(request):
    """Render dashboard with product analytics"""
    return render(request, "recommender/dashboard.html")

@api_view(['GET'])
def get_chart_data(request):
    """Get data for frequently bought together products"""
    pairs = OrderItem.objects.filter(
        order__order_items__isnull=False
    ).values(
        product1_id=F('product__id'),
        product2_id=F('order__order_items__product__id')
    ).filter(
        product1_id__lt=F('product2_id') 
    ).annotate(
        count=Count('id', distinct=True)
    ).order_by('-count')[:5]

    products = Product.objects.in_bulk()
    data = {
        "labels": [],
        "values": []
    }

    for pair in pairs:
        try:
            p1 = products[pair['product1_id']].name
            p2 = products[pair['product2_id']].name
            data['labels'].append(f"{p1} & {p2}")
            data['values'].append(pair['count'])
        except KeyError:
            continue  

    return Response(data)
@api_view(['GET'])
def category_distribution(request):
    """Product distribution by category"""
    distribution = Product.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return Response({
        'labels': [item['category'] for item in distribution],
        'values': [item['count'] for item in distribution]
    })

@api_view(['GET'])
def sales_trend(request):
    """Orders trend for last 30 days"""
    from django.utils import timezone
    from django.db.models.functions import TruncDay
    
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=30)
    
    trend_data = Order.objects.filter(
        order_date__gte=start_date
    ).annotate(
        day=TruncDay('order_date')
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    return Response({
        'labels': [item['day'].strftime('%Y-%m-%d') for item in trend_data],
        'values': [item['count'] for item in trend_data]
    })

@api_view(['GET'])
def top_products(request):
    """Top selling products by quantity"""
    from django.db.models import Sum
    
    top_products = Product.objects.annotate(
        total_sold=Sum('order_items__quantity')
    ).order_by('-total_sold')[:10]
    
    return Response({
        'labels': [p.name for p in top_products],
        'values': [p.total_sold or 0 for p in top_products]
    })