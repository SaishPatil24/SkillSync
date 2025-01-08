import requests
from bs4 import BeautifulSoup
import logging
import time
import sys
print(sys.path)  # This will print the list of directories where Python is searching for modules
# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to fetch URL and return BeautifulSoup object
def fetch_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        else:
            logging.error(f"Failed to retrieve URL {url} with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return None

# Function to scrape job listings from multiple sources
def scrape_jobs(query: str, location: str):
    query = query.replace(" ", "+")  # Format query for URL
    jobs = []

    # URLs for multiple job sources
    urls = {
        'Indeed': f"https://www.indeed.com/jobs?q={query}&l={location}",
        'Upwork': f"https://www.upwork.com/freelance-jobs/",
        'Monster': f"https://www.monster.com/jobs/search/?q={query}&where={location}"
    }

    for site, url in urls.items():
        logging.info(f"Scraping {site} for {query} in {location}...")
        soup = fetch_url(url)
        if soup:
            if site == "Indeed":
                for job_card in soup.find_all("div", class_="job_seen_beacon"):
                    title = job_card.find("h2", class_="jobTitle").text if job_card.find("h2", class_="jobTitle") else None
                    company = job_card.find("span", class_="companyName").text if job_card.find("span", class_="companyName") else None
                    location = job_card.find("div", class_="companyLocation").text if job_card.find("div", class_="companyLocation") else None
                    summary = job_card.find("div", class_="job-snippet").text.strip() if job_card.find("div", class_="job-snippet") else None
                    jobs.append({"Title": title, "Company": company, "Location": location, "Summary": summary})
            
            elif site == "Upwork":
                for job_card in soup.find_all("div", class_="job-title"):
                    title = job_card.find("a").text if job_card.find("a") else None
                    jobs.append({"Title": title, "Company": None, "Location": None, "Summary": None})
            
            elif site == "Monster":
                for job_card in soup.find_all("section", class_="card-content"):
                    title = job_card.find("h2").text if job_card.find("h2") else None
                    company = job_card.find("div", class_="company-name").text if job_card.find("div", class_="company-name") else None
                    location = job_card.find("div", class_="location").text if job_card.find("div", class_="location") else None
                    summary = job_card.find("div", class_="summary").text.strip() if job_card.find("div", class_="summary") else None
                    jobs.append({"Title": title, "Company": company, "Location": location, "Summary": summary})

        else:
            logging.error(f"Failed to retrieve data from {site}")
        
        # Add a small delay to avoid overloading the server (good practice)
        time.sleep(2)

    return jobs