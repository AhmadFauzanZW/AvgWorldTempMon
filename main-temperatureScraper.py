import functions
import time

URL = "https://programmer100.pythonanywhere.com/"
DATA_STORE = 'data-temp.txt'

while True:
    scraped = functions.scrape(URL)
    extracted = functions.extract(scraped, file_store='extract-temp.yaml', data='temperature')
    date = time.strftime('%A, %d-%b-%y %H.%M')

    print(date)
    print(extracted)

    content = functions.read(extracted, DATA_STORE)
    functions.store(extracted, DATA_STORE)

    print("Temperature data captured!")

    time.sleep(5)

