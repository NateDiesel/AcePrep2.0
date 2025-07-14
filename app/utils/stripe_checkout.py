
import os
import stripe
from fastapi.responses import RedirectResponse
from fastapi import Request
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")

def create_checkout_session(request: Request):
    origin = str(request.base_url).rstrip("/")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": PRICE_ID,
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{origin}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{origin}/",
    )
    return RedirectResponse(session.url, status_code=303)
