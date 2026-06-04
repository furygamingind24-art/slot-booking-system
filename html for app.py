<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Appointment Scheduler</title>
    <style>
        :root {
            --bg-color: #121214;
            --card-bg: #1e1e24;
            --accent-color: #4f46e5;
            --accent-hover: #4338ca;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border-color: #374151;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .container {
            width: 100%;
            max-width: 800px;
        }

        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-weight: 600;
        }

        p.subtitle {
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 30px;
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 15px;
            margin-bottom: 40px;
        }

        .slot-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .slot-card:hover {
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }

        .slot-card.selected {
            background-color: var(--accent-color);
            border-color: var(--accent-color);
        }

        .slot-time {
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .slot-status {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        .slot-card.selected .slot-status {
            color: #e0e7ff;
        }

        /* Booking Form Modal Card */
        .booking-box {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 30px;
            display: none;
            margin-top: 20px;
        }

        .booking-box.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        input {
            width: 100%;
            padding: 12px;
            background-color: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-main);
            font-size: 1rem;
            box-sizing: border-box;
        }

        input:focus {
            outline: none;
            border-color: var(--accent-color);
        }

        .btn-submit {
            width: 100%;
            padding: 14px;
            background-color: var(--accent-color);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }

        .btn-submit:hover {
            background-color: var(--accent-hover);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Select an Appointment Slot</h1>
        <p class="subtitle">Click an available time window below to request a booking notification via WhatsApp.</p>

        <div class="calendar-grid">
            <div class="slot-card" onclick="selectSlot(this, '09:00 AM - 10:00 AM')">
                <div class="slot-time">09:00 AM</div>
                <div class="slot-status">Available</div>
            </div>
            <div class="slot-card" onclick="selectSlot(this, '11:00 AM - 12:00 PM')">
                <div class="slot-time">11:00 AM</div>
                <div class="slot-status">Available</div>
            </div>
            <div class="slot-card" onclick="selectSlot(this, '02:00 PM - 03:00 PM')">
                <div class="slot-time">02:00 PM</div>
                <div class="slot-status">Available</div>
            </div>
            <div class="slot-card" onclick="selectSlot(this, '04:00 PM - 05:00 PM')">
                <div class="slot-time">04:00 PM</div>
                <div class="slot-status">Available</div>
            </div>
        </div>

        <div class="booking-box" id="bookingBox">
            <h3 style="margin-top: 0; margin-bottom: 20px;">Confirm Details for <span id="selectedTimeLabel" style="color: #818cf8;"></span></h3>

            <div class="form-group">
                <label for="userName">Your Full Name</label>
                <input type="text" id="userName" placeholder="John Doe" required>
            </div>

            <div class="form-group">
                <label for="userPhone">Contact Phone Number</label>
                <input type="tel" id="userPhone" placeholder="+1 234 567 8900" required>
            </div>

            <button class="btn-submit" onclick="submitBooking()">Request Booking</button>
        </div>
    </div>

    <script>
        let selectedTimeSlot = "";

        function selectSlot(element, timeString) {
            // Remove active 'selected' classes from all cards
            document.querySelectorAll('.slot-card').forEach(card => {
                card.classList.remove('selected');
            });

            // Highlight chosen card element
            element.classList.add('selected');
            selectedTimeSlot = timeString;

            // Show input form section below
            document.getElementById('selectedTimeLabel').innerText = timeString;
            document.getElementById('bookingBox').classList.add('active');

            // Auto scroll cleanly to the input box layout area
            document.getElementById('bookingBox').scrollIntoView({ behavior: 'smooth' });
        }

        function submitBooking() {
            const name = document.getElementById('userName').value.trim();
            const phone = document.getElementById('userPhone').value.trim();

            if (!name || !phone) {
                alert("Please fill out all input parameter text boxes!");
                return;
            }

            // Create JSON data payload block to send across the network
            const payload = {
                name: name,
                phone: phone,
                timeSlot: selectedTimeSlot
            };

            // Post package forward to Flask server route mapping
            fetch('/book-slot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert("🎉 Slot Requested successfully! Check your phone for the automated WhatsApp alert.");
                    // Reset page look state parameters
                    document.getElementById('userName').value = "";
                    document.getElementById('userPhone').value = "";
                    document.getElementById('bookingBox').classList.remove('active');
                    document.querySelectorAll('.slot-card').forEach(card => card.classList.remove('selected'));
                } else {
                    alert("Server Error occurred: " + data.message);
                }
            })
            .catch(err => {
                console.error("Networking Failure:", err);
                alert("Could not connect to Flask application container server processing hub.");
            });
        }
    </script>
</body>
</html>
