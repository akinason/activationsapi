from . import models
from rest_framework import serializers


class DescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Description
        exclude = ['software', "created_on", "updated_on"]


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'first_name', "last_name", 'website', 'email', 'mobile']


class LicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.License
        exclude = ['software', "created_on", "updated_on"]


class SoftwareSerializer(serializers.ModelSerializer):

    licenses = LicenseSerializer(many=True, read_only=True)
    author = AuthorSerializer()
    descriptions = DescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Software
        exclude = ['is_active']


class OrderSerializer(serializers.ModelSerializer):
    reference = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    software = SoftwareSerializer()
    license = LicenseSerializer()

    class Meta:
        model = models.Order
        fields = [
            "id", "software", "license", "amount", "currency", "name", "email", "address", "mobile", "country",
            "reference", "payment_response"
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    reference = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    amount = serializers.DecimalField(decimal_places=2, max_digits=10)
    payment_response = serializers.ReadOnlyField()

    class Meta:
        model = models.Order
        fields = [
            "id", "software", "license", "amount", "currency", "name", "email", "address", "mobile", "country",
            "reference", "payment_response"
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Order
        fields = ["id", "payment_response"]
