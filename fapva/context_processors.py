from django.db.models import Sum

from api.order.models import UserWallet


def wallet_detail(request):
    user_id = request.user.id
    balance = UserWallet.objects.filter(user_id=user_id).aggregate(total=Sum("balance"))['total']
    return {
        "balance": balance if balance else 0
    }
