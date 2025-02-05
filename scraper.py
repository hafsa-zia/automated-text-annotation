import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

THREAD_COUNT = 50
MAX_RETRIES = 3
TIMEOUT = 90
BASE_URL = "https://papers.nips.cc"
OUTPUT_DIR = "C:/Users/hafsa/Desktop/scraped2-pdfs/"

# Create the output directory and metadata file if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "metadata.csv")

def create_metadata_file():
    # Create CSV file and write headers if it doesn't exist
    if not os.path.exists(CSV_OUTPUT_PATH):
        with open(CSV_OUTPUT_PATH, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Paper Title", "Paper URL", "PDF URL", "Download Timestamp"])
            print(f"Metadata file created at: {CSV_OUTPUT_PATH}")

def get_year_links():
    print(f"Connecting to main page: {BASE_URL}")
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    soup = BeautifulSoup(response.content, "html.parser")
    year_links = soup.select("a[href^='/paper_files/paper/']")
    print(f"Found {len(year_links)} paper archive links.")
    return [BASE_URL + link['href'] for link in year_links]

def get_paper_links(year_url):
    print(f"Processing paper archive: {year_url}")
    response = requests.get(year_url, timeout=TIMEOUT)
    soup = BeautifulSoup(response.content, "html.parser")
    paper_links = soup.select("ul.paper-list li a[href$='Abstract-Conference.html']")
    print(f"Found {len(paper_links)} paper links in year: {year_url}")
    return [BASE_URL + link['href'] for link in paper_links]

def process_paper(paper_url, writer):
    attempts = 0
    success = False
    while attempts < MAX_RETRIES and not success:
        try:
            print(f"Processing paper: {paper_url} (Attempt {attempts + 1})")
            response = requests.get(paper_url, timeout=TIMEOUT)
            soup = BeautifulSoup(response.content, "html.parser")
            
            paper_title = soup.select_one("title").text
            sanitized_title = sanitize_filename(paper_title)
            
            pdf_link = soup.select_one("a[href$='Paper-Conference.pdf']")
            if pdf_link:
                pdf_url = BASE_URL + pdf_link['href']
                print(f"Found PDF link: {pdf_url}")
                
                download_pdf(pdf_url, sanitized_title)
                download_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Write metadata to CSV
                with open(CSV_OUTPUT_PATH, mode="a", newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([paper_title, paper_url, pdf_url, download_timestamp])
                    file.flush()
                success = True
            else:
                print(f"No PDF link found for paper: {paper_url}")
                success = True
        except requests.exceptions.RequestException as e:
            print(f"Failed to process paper: {paper_url} (Attempt {attempts + 1})")
            print(e)
            attempts += 1
            if attempts >= MAX_RETRIES:
                print(f"Giving up on paper: {paper_url} after {MAX_RETRIES} attempts.")

def download_pdf(pdf_url, file_name):
    response = requests.get(pdf_url, stream=True, timeout=TIMEOUT)
    file_path = os.path.join(OUTPUT_DIR, f"{file_name}.pdf")
    
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    print(f"Saved PDF: {file_path}")

def sanitize_filename(filename):
    # Sanitize filename for invalid characters
    return filename.replace("\\", "_").replace("/", "_").replace(":", "_").replace("*", "_") \
                   .replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")

def main():
    create_metadata_file()
    
    with open(CSV_OUTPUT_PATH, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        
        year_links = get_year_links()
        
        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            for year_url in year_links:
                paper_links = get_paper_links(year_url)
                for paper_url in paper_links:
                    executor.submit(process_paper, paper_url, writer)

if __name__ == "__main__":
    main()
