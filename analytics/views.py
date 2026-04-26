from django.db.models import Count, Sum, Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from order.models import OrderItem, Order
from reviews.models import Review

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    # Overall analytics (shared for admin and users)
    total_orders = Order.objects.count()
    liked_reviews = (
        Review.objects.values("food_id", "food__name")
        .annotate(avg_rating=Avg("rating"), total_reviews=Count("id"))
        .order_by("-avg_rating")[:6]
    )
    trending_foods = (
        OrderItem.objects.values("food_id", "food__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:6]
    )

    # User-specific orders
    user_orders = Order.objects.filter(user=user).order_by("-created_at")
    user_total_orders = user_orders.count()
    total_spent = user_orders.aggregate(total=Sum("total_price"))["total"] or 0
    recent_orders = [
        {
            "id": order.id,
            "status": order.status,
            "total": order.total_price,
            "created_at": order.created_at,
        }
        for order in user_orders[:5]
    ]

    return Response({
        # Shared analytics
        "total_orders_overall": total_orders,
        "mostly_liked_foods": liked_reviews,
        "trending_foods": trending_foods,

        # User-specific stats
        "total_orders": user_total_orders,
        "total_spent": float(total_spent),
        "recent_orders": recent_orders,
    })
