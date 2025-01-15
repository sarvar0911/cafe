from django.db import models

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('done', 'Done'),
        ('paid', 'Paid'),
    ]
    id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()
    items = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def calculate_total_price(self):
        if isinstance(self.items, list):
            return sum(item.get('price', 0) for item in self.items)
        return 0.00

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "order"
        ordering = ['table_number']
