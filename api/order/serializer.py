import json

from rest_framework import serializers

from api.order.models import Order, UserWallet
from api.users.models import User
import datetime


class UserWalletSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    price = serializers.SerializerMethodField()
    date_time = serializers.SerializerMethodField()

    class Meta:
        model = UserWallet
        fields = ('id', 'price', 'date_time')

    def get_date_time(self,obj):
        resp = json.loads(obj.order.response_json)
        return datetime.datetime.strptime(resp['purchase_units'][0]['payments']['captures'][0]['create_time'],
                           '%Y-%m-%dT%H:%M:%S%z')

    def get_price(self,obj):
        if obj.balance == 0:
            return obj.order.price
        return obj.balance


class OrderDataTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


