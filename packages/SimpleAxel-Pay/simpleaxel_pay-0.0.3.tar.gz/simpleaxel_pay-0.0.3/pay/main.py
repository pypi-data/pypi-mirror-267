from flask import Blueprint, redirect, request
from simplesdk.internal import AlphacrmSDK, AulaSDK
from os import environ
from dotenv import load_dotenv
import stripe
from simplesdk.translations import translation, language

load_dotenv()
loc = translation(
    environ.get("ET_TRANSLATIONS")
    or "https://git.tech.eus/EuskadiTech/Translations/raw/branch/main/SimpleAxel.json"
)

stripe.api_key = environ["ET_STRIPE_API_KEY"]


app = Blueprint("pay", __name__, url_prefix="/pay", template_folder="templates")
client = AlphacrmSDK(environ["ET_USER"], environ["ET_PASSWORD"], environ["ET_BASEURL"])
client2 = AulaSDK(environ["ET_USER"], environ["ET_PASSWORD"], environ["ET_BASEURL"])


def login_session():
    user = client.login_with_session(request.cookies.get("et_auth_session"))
    return user


DOMAIN = environ["ET_DOMAIN"]  # "http://localhost:4242"


def start_payment_session(
    PRICE_ID: str,
    PROD_CODE: str,
    PROD_PLAN_COMB: str,
    TYPE: str = "subscription",
    QUANTITY: int = 1,
):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price": PRICE_ID,
                    "quantity": QUANTITY,
                },
            ],
            mode=TYPE,
            allow_promotion_codes=True,
            success_url=DOMAIN
            + f"/pay/flow/{PROD_CODE}/success/DE:AD:BE:EF:FE:ED/{PROD_PLAN_COMB}",
            cancel_url=DOMAIN + "/pay/canceled",
            automatic_tax={"enabled": True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route("/flow/<prod>/start_payment/<plan>")
def flow__start_payment(prod, plan):
    user = login_session()
    if user == None:
        return redirect("/auth/login")
    pid = ":".join((prod, plan))
    producto = next(
        (p for p in client.productos() if p["0(productos)"]["codigo"] == pid), None
    )
    if producto == None:
        return redirect("/")
    return start_payment_session(
        producto["0(productos)"]["stripe_id"],
        prod,
        pid,
        producto["0(productos)"]["type"],
    )


#
@app.route("/flow/<prod>/success/DE:AD:BE:EF:FE:ED/<name>")
def flow__paid(prod, name):
    user = login_session()
    if user == None:
        return redirect("/auth/login")
    p = str(user["0(clientes)"]["products"]).split()
    p.append(prod)
    p.append(name)
    user["0(clientes)"]["products"] = " ".join(p)
    client.register(user)
    producto = next(
        p for p in client.productos() if p["0(productos)"]["codigo"] == name
    )
    return redirect(producto["0(productos)"]["redirect"])
