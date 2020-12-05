import os

from dotenv import load_dotenv

load_dotenv()

class StripeConfig(object):
    """
    StripeConfig is the configuration for the stripe service.
    """
    PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
    SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

    IMAGE_URL = "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=2167&q=80"
    PAYMENT_SUCCESS_URL = "http://example.com/successful"
    PAYMENT_CANCEL_URL = "http://example.com/cancelled"
    ACCOUNT_RETURN_URL = "http://localhost:8000/"
    ACCOUNT_REFRESH_URL = "http://localhost:8000/"
