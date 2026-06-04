from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import sqlite3

app = Flask(__name__)
DB_FILE = "bookings.db"

# =====================================================================
# TWILIO CREDENTIALS CONFIGURATION
# =====================================================================
# Replace these with your actual Twilio account parameters
TWILIO_ACCOUNT_SID = ""  # Your SID
TWILIO_AUTH_TOKEN = ""  # Your Auth Token
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Standard Twilio Sandbox Number

# Put your personal WhatsApp number here (include country code, e.g., +91 for India)
MY_PERSONAL_NUMBER = "whatsapp:"


def init_db():
    """Initializes a local SQLite database file to track slot bookings."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS appointments
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       phone
                       TEXT
                       NOT
                       NULL,
                       time_slot
                       TEXT
                       NOT
                       NULL,
                       status
                       TEXT
                       DEFAULT
                       'Pending'
                   )
                   ''')
    conn.commit()
    conn.close()


# Initialize our database structure immediately on server launch
init_db()


@app.route('/')
def home():
    """Serves your frontend calendar webpage directly from the templates folder."""
    return render_template('index.html')


@app.route('/book-slot', methods=['POST'])
def book_slot():
    """Endpoint that captures slot data from your website and triggers the WhatsApp engine."""
    try:
        data = request.get_json()

        name = data.get('name')
        phone = data.get('phone')
        time_slot = data.get('timeSlot')

        if not name or not phone or not time_slot:
            return jsonify({"status": "error", "message": "All form fields are mandatory!"}), 400

        # 1. Save booking details locally into our database file
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (name, phone, time_slot, status) VALUES (?, ?, ?, 'Pending')",
            (name, phone, time_slot)
        )
        conn.commit()
        conn.close()

        # 2. Structure your WhatsApp notification text look
        alert_message = (
            f"🔔 *NEW BOOKING REQUEST RECEIVED* 🔔\n\n"
            f"👤 *Name:* {name}\n"
            f"📞 *Phone:* {phone}\n"
            f"📅 *Selected Slot:* {time_slot}\n\n"
            f"Reply with 'Accept {name}' to confirm this session!"
        )

        # 3. Request Twilio's API to forward this notification to your phone
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=alert_message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=MY_PERSONAL_NUMBER
        )

        print(f"\n[SUCCESS]: Notification successfully sent! SID: {message.sid}")
        return jsonify({"status": "success", "message": "Slot requested successfully!"})

    except Exception as e:
        print(f"\n[SERVER ERROR]: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Start our backend app on port 5000
    app.run(debug=True, port=5000)
