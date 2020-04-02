import json

import stripe


def lambda_handler(event, context):
    data = event['body']
    line_items = data["line_items"]
    company = data["company"]
    stripe_account_id = data["stripe_account"]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        success_url='http://localhost:4242',
        cancel_url='http://localhost:4242/cancel',
        stripe_account=stripe_account_id
    )

    response = {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            # 'Content-Type': 'application/json'
        },
        'body': session['id']
    }
    return response
    