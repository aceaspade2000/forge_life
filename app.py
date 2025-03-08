from flask import Flask, render_template, send_from_directory
import os
import stripe

app = Flask(__name__)

# 🔹 Replace with your actual Stripe Secret Key
stripe.api_key = "sk_test_51QyOWHPvCYOqqYFs79i4NQKW3DOVyPKysOvj6QJmO6MxRSb7IRJpUUiQABDrJYQSNRxPevs6EfweUDL8QVQlPpv5002nOcaMLt"

# Product Details
PRODUCT_NAME = "Forge Life - Stainless Steel Scraper"
PRODUCT_PRICE = 1999  # Price in cents ($19.99)
CURRENCY = "usd"

@app.route('/')
def home():
    return render_template('home.html')

# ✅ Explicitly Serve Static Files (Fixes CSS Issues)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/checkout', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': CURRENCY,
                    'product_data': {'name': PRODUCT_NAME},
                    'unit_amount': PRODUCT_PRICE,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="http://127.0.0.1:5000/success",
            cancel_url="http://127.0.0.1:5000/cancel",
        )
        return {'id': session.id}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/success')
def success():
    return "✅ Payment Successful! Thank you for your order."

@app.route('/cancel')
def cancel():
    return "❌ Payment Canceled."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

