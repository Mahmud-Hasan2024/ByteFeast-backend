from django.db.models import Count, Sum, Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from reviews.models import Review
from menu.models import FoodItem # Ensure FoodItem is imported

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    # 1. Fetch Analytics using values()
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

    # 2. Helper function to safely attach the first image URL to each item
    def attach_food_assets(items):
        item_list = list(items)
        for item in item_list:
            food = FoodItem.objects.filter(id=item['food_id']).first()
            if food:
                # Get the first image object if it exists
                first_img = food.images.first()
                # Use .url to get the Cloudinary or local path
                item['image_url'] = first_img.image.url if first_img else None
            else:
                item['image_url'] = None
        return item_list

    mostly_liked = attach_food_assets(liked_query)
    trending = attach_food_assets(trending_query)

    # 3. User-specific stats
    user_orders = Order.objects.filter(user=user)
    total_spent = user_orders.aggregate(total=Sum("total_price"))["total"] or 0

    return Response({
        "total_orders_overall": Order.objects.count(),
        "mostly_liked_foods": mostly_liked,
        "trending_foods": trending,
        "total_orders": user_orders.count(),
        "total_spent": float(total_spent),
    })