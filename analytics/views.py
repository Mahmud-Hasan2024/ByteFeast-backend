from django.db.models import Count, Sum, Avg, Case, When, F, DecimalField
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from reviews.models import Review
from menu.models import FoodItem

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    try:
        user = request.user

        # 1. Base Query with effective_price logic added via Annotation
        # This mirrors your model's @property logic for the database
        base_food_query = FoodItem.objects.annotate(
            actual_price=Case(
                When(is_special=True, discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField(),
            )
        )

        # 2. Get Analytics
        liked_stats = (
            Review.objects.values("food_id")
            .annotate(avg_rating=Avg("rating"), total_reviews=Count("id"))
            .order_by("-avg_rating")[:6]
        )

        trending_stats = (
            OrderItem.objects.values("food_id")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:6]
        )

        # 3. Helper to build the ProductItem-ready dictionary
        def get_product_details(stat_list):
            results = []
            for stat in stat_list:
                food = base_food_query.filter(id=stat['food_id']).first()
                if food:
                    first_img = food.images.first()
                    results.append({
                        "id": food.id,
                        "name": food.name,
                        "price": float(food.actual_price), # Matches effective_price
                        "description": food.description,
                        "image_url": first_image.image.url if (first_img := food.images.first()) else None,
                        "avg_rating": stat.get('avg_rating'),
                        "total_quantity": stat.get('total_quantity')
                    })
            return results

        mostly_liked = get_product_details(liked_stats)
        trending = get_product_details(trending_stats)

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
    except Exception as e:
        return Response({"error": str(e)}, status=500)