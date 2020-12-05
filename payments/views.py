import stripe
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response

from config import StripeConfig

stripe.api_key = StripeConfig.SECRET_KEY


class HomePageView(TemplateView):
    template_name = 'home.html'


class StripeConfigView(APIView):
    """
    StripeConfigView is the API of configs resource, and
    responsible to handle the requests of /config/ endpoint.
    """
    def get(self, request, format=None):
        config = {
            "publishable_key": str(StripeConfig.PUBLISHABLE_KEY)
        }
        return Response(config)


class StripeSessionView(APIView):
    """
    StripeSessionView is the API of sessions resource, and
    responsible to handle the requests of /session/ endpoint.
    """
    def get(self, request, format=None):
        print(request.body.decode('utf-8'))
        pay_data = {
            "price_data": {
                "currency": "usd",
                "unit_amount": 50,
                "product_data": {
                    "name": "product_name",
                    "images": [StripeConfig.IMAGE_URL],
                }
            },
            "quantity": 50,
        }

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=StripeConfig.PAYMENT_SUCCESS_URL,
                cancel_url=StripeConfig.PAYMENT_CANCEL_URL,
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    pay_data,
                ]
            )
            print(checkout_session["payment_intent"])
            return Response({'sessionId': checkout_session['id']})
        except Exception as e:
            return Response({'error': str(e)})


class StripeWebhookView(APIView):
    """
    StripeWebhookView is responsible to handle the webhook
    events of /webhook/ endpoint.
    """
    def post(self, request, format=None):
        endpoint_secret = StripeConfig.WEBHOOK_SECRET
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                request.body, sig_header, endpoint_secret
            )
        except ValueError as e:
            print(e)
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            print(e)
            return Response(status=400)

        if event['type'] == 'checkout.session.completed':
            print(event["data"]["object"]["payment_intent"])

        return Response(status=200)

class StripeAccountView(APIView):
    """
    StripeAccountView is the API of account resource, and
    responsible to handle the requests of /account/ endpoint.
    """
    def get(self, request, format=None):
        account = stripe.Account.create(
            country='US',
            type='custom',
            capabilities={
                'card_payments': {
                    'requested': True,
                },
                'transfers': {
                    'requested': True,
                },
            },
        )
        account_links = stripe.AccountLink.create(
            account=account["id"],
            refresh_url=StripeConfig.ACCOUNT_REFRESH_URL,
            return_url=StripeConfig.ACCOUNT_RETURN_URL,
            type='account_onboarding',
        )
        return redirect(account_links["url"])
