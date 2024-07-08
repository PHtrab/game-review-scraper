import streamlit as st

st.title("Game Review Scraper")

st.write("This is a test to see if the app is running.")

url = st.text_input("Enter the Metacritic URL for the game:")

if st.button("Test Button"):
    st.write(f"You entered: {url}")
