# Re-import necessary libraries after execution state reset
import json
import random
import pandas as pd
import sqlite3

# Predefined data for UK cities and other details
cities = ["London", "Manchester", "Birmingham", "Glasgow", "Liverpool", "Edinburgh", "Bristol", "Leeds", "Cardiff", "Sheffield"]
times = ["morning", "afternoon", "evening", "night"]
refund_reasons = ["train cancellation", "delayed train", "personal reasons", "incorrect booking"]

# Expanded query and response variations
schedule_queries = [
    "What is the train schedule from {from_city} to {to_city} in the {time}?",
    "Can you tell me the departure times for trains from {from_city} to {to_city}?",
    "When is the next available train from {from_city} to {to_city}?",
    "Are there any evening trains running from {from_city} to {to_city}?",
    "What time does the last train leave from {from_city} to {to_city}?",
    "How frequently do trains run between {from_city} and {to_city}?",
    "Is there an early morning train from {from_city} to {to_city}?",
    "Can I check the full train timetable from {from_city} to {to_city}?",
    "Do you have weekend train schedules for {from_city} to {to_city}?",
    "Is there a direct train from {from_city} to {to_city}?"
]

schedule_responses = [
    "The train schedule is available on our website or mobile app.",
    "The next available train departs at 07:30 AM. Would you like to book a ticket?",
    "Trains from {from_city} to {to_city} run every hour during peak times.",
    "The last train from {from_city} to {to_city} leaves at 10:45 PM.",
    "Weekend schedules may vary. Please check online for accurate timings.",
    "Yes, there is a direct train available at 09:15 AM.",
    "The next evening train departs at 06:30 PM.",
    "Trains run every 30 minutes during weekdays.",
    "You can find the full timetable on our official site.",
    "There are multiple direct and connecting trains available. Check online for details."
]

booking_queries = [
    "How can I book a train ticket from {from_city} to {to_city}?",
    "What is the process for booking a train ticket?",
    "Can I book a ticket online from {from_city} to {to_city}?",
    "Do you have any discounts on train tickets?",
    "How much does a ticket from {from_city} to {to_city} cost?",
    "Can I reserve a seat on the train from {from_city} to {to_city}?",
    "What are the payment options for train ticket booking?",
    "Can I book tickets for multiple passengers?",
    "Is there a mobile app for booking train tickets?",
    "Can I modify my train ticket booking?"
]

booking_responses = [
    "You can book a ticket via our website, mobile app, or at the station.",
    "To book a train ticket, visit our official site and follow the steps provided.",
    "Yes, online booking is available for all routes.",
    "We offer discounts for students, seniors, and early bookings.",
    "The ticket price depends on the route and time of travel. Please check online for exact fares.",
    "Yes, seat reservations are available at an extra charge.",
    "We accept credit cards, debit cards, and online banking for payments.",
    "Yes, you can book tickets for multiple passengers in a single transaction.",
    "Our mobile app allows easy ticket booking and management.",
    "Modifications to bookings can be made up to 24 hours before departure."
]

refund_queries = [
    "I would like a refund due to {reason}. What is the process?",
    "Can I get a full refund if my train is canceled?",
    "What is the refund policy for delayed trains?",
    "How long does it take to process a refund?",
    "Can I cancel my ticket and get a refund?",
    "Is there a cancellation fee for ticket refunds?",
    "Can I get a refund if I miss my train?",
    "What happens if I need to change my travel date?",
    "Are refunds available for non-refundable tickets?",
    "Where can I apply for a train ticket refund?"
]

refund_responses = [
    "Refunds can be processed within 3-5 business days. Please check our refund policy for details.",
    "Yes, full refunds are available for canceled trains.",
    "If your train is delayed by more than 30 minutes, you may be eligible for a partial refund.",
    "Refunds are typically processed within 5 business days.",
    "You can cancel your ticket online and request a refund.",
    "A small cancellation fee may apply depending on the ticket type.",
    "Unfortunately, refunds are not available for missed trains.",
    "You may be able to reschedule your ticket instead of canceling.",
    "Non-refundable tickets cannot be refunded, but you might get travel credit.",
    "You can apply for a refund through our website or customer service."
]

# Function to generate diverse queries
def generate_queries(num_queries=30):
    queries = []
    
    for _ in range(num_queries // 3):
        from_city, to_city = random.sample(cities, 2)
        time = random.choice(times)
        reason = random.choice(refund_reasons)

        queries.append({
            "query": random.choice(schedule_queries).format(from_city=from_city, to_city=to_city, time=time),
            "response": random.choice(schedule_responses).format(from_city=from_city, to_city=to_city)
        })
        queries.append({
            "query": random.choice(booking_queries).format(from_city=from_city, to_city=to_city),
            "response": random.choice(booking_responses).format(from_city=from_city, to_city=to_city)
        })
        queries.append({
            "query": random.choice(refund_queries).format(reason=reason),
            "response": random.choice(refund_responses)
        })

    return queries

# Generate and save the dataset
dataset = generate_queries(30)
dataset = pd.DataFrame(dataset)
print(dataset.head())
print(dataset.shape)
dataset.to_csv("data/chatbot_queries.csv", index=False)
# Connect to SQLite database (or create it if not exists)
conn = sqlite3.connect("data/train_chatbot.db")

# Create a table for chatbot queries (if not exists)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS chatbot_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    response TEXT NOT NULL
)
""")

# Insert data into the table
dataset.to_sql("chatbot_queries", conn, if_exists="replace", index=False)

# Commit and close connection
conn.commit()
conn.close()

print("Dataset successfully saved to SQLite database!")
