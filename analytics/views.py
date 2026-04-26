from django.db.models import Count, Sum, Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from reviews.models import Review
from menu.models import FoodItem # Ensure this is imported

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    # 1. Get Analytics IDs and basic info first
    liked_query = (
        Review.objects.values("food_id", "food__name", "food__price", "food__description")
        .annotate(avg_rating=Avg("rating"), total_reviews=Count("id"))
        .order_by("-avg_rating")[:6]
    )

    trending_query = (
        OrderItem.objects.values("food_id", "food__name", "food__price", "food__description")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:6]
    )

    # 2. Helper to attach the first image to each result manually
    def attach_images(item_list):
        for item in item_list:
            food = FoodItem.objects.filter(id=item['food_id']).first()
            first_image = food.images.first() if food else None
            item['food__images__image'] = first_image.image.url if first_image else None
        return item_list

    mostly_liked = attach_images(list(liked_query))
    trending = attach_images(list(trending_query))

    # User-specific stats
    user_orders = Order.objects.filter(user=user)
    total_spent = user_orders.aggregate(total=Sum("total_price"))["total"] or 0

    return Response({
        "total_orders_overall": Order.objects.count(),
        "mostly_liked_foods": mostly_liked,
        "trending_foods": trending,
        "total_orders": user_orders.count(),
        "total_spent": float(total_spent),
    })