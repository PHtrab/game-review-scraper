import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import your_original_script as scraper  # Import your original script

st.title("Game Review Scraper")

url = st.text_input("Enter the Metacritic URL for the game:")

if st.button("Scrape Reviews"):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    urls = scraper.get_review_urls(driver, url)
    st.write(f"Found {len(urls)} review URLs")
    
    reviews = []
    for i, review_url in enumerate(urls, 1):
        st.write(f"Processing URL {i} of {len(urls)}: {review_url}")
        game_reviews = scraper.scrape_reviews(driver, review_url)
        reviews.extend(game_reviews)
    
    driver.quit()
    
    st.download_button(
        label="Download Reviews",
        data="\n\n".join(reviews),
        file_name="scraped_reviews.txt",
        mime="text/plain"
    )

st.write("Note: This process may take several minutes. Please be patient.")
