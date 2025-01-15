from rest_framework import serializers
from cafeapp.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']
        read_only_fields = ['id', 'total_price']

    def validate_items(self, value):
        if not isinstance(value, list) or not all(isinstance(item, dict) and 'price' in item for item in value):
            raise serializers.ValidationError("Items must be a list of dictionaries with 'name' and 'price'.")
        return value

    def create(self, validated_data):
        items = validated_data.get('items', [])
        total_price = sum(item.get('price', 0) for item in items)
        validated_data['total_price'] = total_price
        return super().create(validated_data)
