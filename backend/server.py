import stripe
import json

from flask_cors import CORS
from flask import (
    Flask,
    render_template,
    request,
)

app = Flask(__name__, static_folder="./static/",
            static_url_path="", template_folder="./templates/")
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
CORS(app)

@app.route('/', methods=['GET'])
def get_example():
    # Display landing page.
    # return render_template('/home/ryan.hatter/personal/tribe/templates/index.html')
    # return render_template('./templates/index.html')
    print("Hello, World!")
    return 'Hello, World!'

@app.route("/donate", methods=["POST"])
def donate():
    data = request.json
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

    return session['id']

    
# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_dtDd08wdjqq6IUFlhcFQlhiO'

@app.route("/connect/oauth", methods=["GET"])
def handle_oauth_redirect():
    # Assert the state matches the state you provided in the OAuth link (optional).
    state = request.args.get("state")

    if not state_matches(state):
        return json.dumps({"error": "Incorrect state parameter: " + state}), 403

    # Send the authorization code to Stripe's API.
    code = request.args.get("code")
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=code,)
    except stripe.oauth_error.OAuthError as e:
        return json.dumps({"error": "Invalid authorization code: " + code}), 400
    except Exception as e:
        return json.dumps({"error": "An unknown error occurred."}), 500

    connected_account_id = response["stripe_user_id"]
    save_account_id(connected_account_id)
    
    # Render some HTML or redirect to a different page.
    return get_example()


def state_matches(state_parameter):
    # Load the same state value that you randomly generated for your OAuth link.
    # saved_state = "{{ STATE }}"
    saved_state = "TRIBETEST"
    return saved_state == state_parameter


def save_account_id(account_id):
    # Save the connected account ID from the response to your database.
    # TODO: Save to DDB
    print(f"Connected account ID: {account_id}")

if __name__ == "__main__":
    app.run(port=4242)