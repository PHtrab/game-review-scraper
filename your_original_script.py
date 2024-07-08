from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

def get_review_urls(driver, metacritic_url):
    print(f"Attempting to get review URLs from {metacritic_url}")
    driver.get(metacritic_url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "c-siteReview_externalLink"))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    review_links = soup.find_all('a', class_='c-siteReview_externalLink')
    if not review_links:
        print(f"No review links found on {metacritic_url}")
    return [urljoin(metacritic_url, link['href']) for link in review_links]

def scrape_reviews(driver, url, min_word_count=30):
        print(f"Attempting to scrape reviews from {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        main_content = soup.find('article', class_='article') or soup.find('div', class_='content') or soup.find('div', class_='article-body')
        
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

# The rest of the script (the part that actually runs the scraping) should be removed or commented out
