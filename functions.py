import requests as req
import selectorlib

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def scrape(url):
    """Scrape page source from URL"""
    response = req.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source, file_store, data):
    """Extract data using selector template"""
    extractor = selectorlib.Extractor.from_yaml_file(file_store)
    value = extractor.extract(source)[data]
    return value

def store(extracted, data_store):
    """Store temperature data with timestamp"""
    with open(data_store, 'a') as file:
        file.write(f"{extracted}\n")

def read(data_store):
    """Read all temperature data"""
    with open(data_store, 'r') as file:
        return [line.strip() for line in file.readlines()]