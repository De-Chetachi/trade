import streamlit as st
from request import posts
import os

# Streamlit app title
st.title("Twitter Data Fetcher")

# Description
st.write("This app retrieves and processes tweets from a specified Twitter user.")

twitter = st.sidebar.text_input("Enter Twitter api key", "")
gecko = st.sidebar.text_input("Enter coin_gecko api key", "")
mongo = st.sidebar.text_input("Enter mongo_connection string", "")

os.environ["TWITTER_TOKEN"] = twitter
os.environ["GECKO_KEY"] = gecko
os.environ["MONGO_URL"] = mongo

# Input fields
username = st.text_input("Enter the Twitter username:", "")
days = st.number_input("Enter the number of days to look back:", min_value=1, max_value=30, value=7)

# Button to trigger the process
if st.button("Fetch Tweets"):
    if username:
        try:
            st.write(f"Fetching tweets for user: {username} over the past {days} days...")
            data = posts(username, days)
            st.write(data)
            st.success("Tweets fetched and processed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid Twitter username.")