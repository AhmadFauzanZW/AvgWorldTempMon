import requests as req
import selectorlib

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Fungsi untuk scraping page source dari URL"""
    response = req.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source, file_store, data):
    extractor = selectorlib.Extractor.from_yaml_file(file_store)
    value = extractor.extract(source)[data]
    return value

def store(extracted, data_store):
    with open(data_store, 'a') as file:
        file.write(extracted + '\n')

def read(extracted, data_store):
    with open(data_store, 'r') as file:
        return file.read()

def send_mail():
    print("Email berhasil dikirim!")