from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
def get_review_urls(driver, metacritic_url):
    driver.get(metacritic_url)

    # Wait for the review links to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "c-siteReview_externalLink"))
    )

    # Get the page source after JavaScript has loaded the content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    review_links = soup.findall('a', class='c-siteReview_externalLink')
    if not review_links:
        print(f"No review links found on {metacritic_url}")
    return [urljoin(metacritic_url, link['href']) for link in review_links]
def scrape_reviews(driver, url, min_word_count=30):
    try:
        driver.get(url)
        # Wait for the content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        maincontent = soup.find('article', class='article') or soup.find('div', class='content') or soup.find('div', class='article-body')

        if not main_content:
            paragraphs = soup.find_all('p')
        else:
            paragraphs = main_content.find_all('p')

        seen_content = set()
        review_texts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text.split()) >= min_word_count and text not in seen_content:
                review_texts.append(text)
                seen_content.add(text)

        return review_texts
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return []
# Set up the Chrome driver
service = Service('chromedriver.exe')  # Update this path
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)
driver = webdriver.Chrome(service=service, options=options)
# Metacritic URL for the game
metacritic_url = 'https://www.metacritic.com/game/monster-hunter-stories/critic-reviews/'
# Get the list of review URLs from Metacritic
print(f"Fetching review URLs from {metacritic_url}")
urls = get_review_urls(driver, metacritic_url)
print(f"Found {len(urls)} review URLs")
# Scrape the reviews and save to file
with open('scraped_reviews.txt', 'w', encoding='utf-8') as f:
    for i, url in enumerate(urls, 1):
        print(f"\nProcessing URL {i} of {len(urls)}: {url}")
        website_name = urlparse(url).netloc.replace('www.', '')
        game_reviews = scrape_reviews(driver, url)

        if game_reviews:
            f.write(f"Review from {website_name}:\n\n")
            for review in game_reviews:
                f.write(f"{review}\n\n")

            f.write("\n" + "="*50 + "\n\n")  # Separator between reviews

            # Print summary to console
            print(f"Successfully scraped review from {website_name}")
            print(f"Total paragraphs scraped: {len(game_reviews)}")
        else:
            print(f"No content scraped from {website_name}")

        # Add a small delay between requests
        time.sleep(2)
# Close the browser
driver.quit()
print("\nAll reviews have been saved to 'scraped_reviews.txt'")