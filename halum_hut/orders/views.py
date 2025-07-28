from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
# Local Imports
from .models import Order, OrderItem, ShippingAddress, Payment
from .serializers import ShippingAddressSerializer
from cart.models import CartItem
from products.models import ProductVariant  # if using variants


class CreateOrderWithCOD(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Validate shipping address
        shipping_data = request.data.get('shipping_address')
        if not shipping_data:
            return Response({"error": "Shipping address is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Create shipping address
        addr_serializer = ShippingAddressSerializer(data=shipping_data)
        addr_serializer.is_valid(raise_exception=True)
        shipping_address = addr_serializer.save(user=user)

        # Get cart items
        cart_items = CartItem.objects.filter(cart__user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                total_price=0, # will calculate below
                status='confirmed',  # COD is usually considered "confirmed" immediately
            )

            total = 0

            for item in cart_items:
                product_variant = item.variant

                # Validate stock
                if product_variant.stock < item.quantity:
                    raise ValueError(f"Not enough stock for product_variant: {product_variant.product.name}")

                # Calculate price & create OrderItem
                price = product_variant.price  # snapshot price
                subtotal = price * item.quantity

                OrderItem.objects.create(
                    order=order,
                    product_variant=product_variant,
                    quantity=item.quantity,
                    price=price,
                    subtotal=subtotal
                )

                # Update product_variant stock
                product_variant.stock -= item.quantity
                product_variant.save()

                total += subtotal

            order.total_price = total
            order.save()

            # Create payment record
            Payment.objects.create(
                order=order,
                user=user,
                method='cod',
                status='initiated',
                paid_at=None,
            )

            # Clear cart
            cart_items.delete()

        return Response({
            "order_id": order.id,
            "status": order.status,
            "payment_method": "cod"
        }, status=status.HTTP_201_CREATED)
