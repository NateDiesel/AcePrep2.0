
import os, stripe
from fastapi import Request
from types import SimpleNamespace

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")

def create_checkout_session(request: Request):
    if not (stripe.api_key and PRICE_ID):
        return SimpleNamespace(url=str(request.base_url) + "form")
    origin = str(request.base_url).rstrip("/")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": PRICE_ID, "quantity": 1}],
        mode="payment",
        success_url=f"{origin}/success",
        cancel_url=f"{origin}/form",
    )
    return session
