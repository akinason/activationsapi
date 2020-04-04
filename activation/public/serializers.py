from rest_framework import serializers
from activation.models import Order
from activation.serializers import LicenseSerializer, SoftwareSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer()
    license = LicenseSerializer()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = [
            "id", "license", "software", "reference", "license_key", "is_used", "is_paid", "amount", "currency", "name",
            "address", "email", "address", "mobile", "created_on"
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):
    reference = serializers.ReadOnlyField()
    license_key = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["reference", "license_key", "is_used"]
