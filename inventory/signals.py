from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import StockMovement, InventoryStock

@receiver(post_save, sender=StockMovement)
def update_inventory_stock(sender, instance, created, **kwargs):
    """
    Tự động cập nhật tồn kho khi có movement
    """
    if created:
        with transaction.atomic():
            # Lấy hoặc tạo inventory stock
            stock, stock_created = InventoryStock.objects.get_or_create(
                warehouse=instance.warehouse,
                product=instance.product,
                defaults={'quantity': 0}
            )
            
            # Cập nhật số lượng dựa trên loại movement
            if instance.movement_type in ['inbound', 'in']:
                stock.quantity += instance.quantity
            elif instance.movement_type in ['outbound', 'out']:
                stock.quantity -= instance.quantity
            elif instance.movement_type == 'adjustment':
                # Với adjustment, quantity có thể âm hoặc dương
                stock.quantity += instance.quantity
            elif instance.movement_type == 'transfer':
                # Transfer out từ kho này
                stock.quantity -= instance.quantity
            elif instance.movement_type in ['damaged', 'expired']:
                # Hàng hỏng/hết hạn - giảm tồn
                stock.quantity -= instance.quantity
            
            # Đảm bảo quantity không âm
            if stock.quantity < 0:
                stock.quantity = 0
                
            stock.save()
