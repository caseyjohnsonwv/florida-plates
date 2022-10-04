import csv
from os import getenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

remote_host = getenv('REMOTE_HOST')
volume_path = getenv('VOLUME_PATH')
input_file = getenv('INPUT_FILE')
output_file = getenv('OUTPUT_FILE')

# wait for selenium container to start chrome
sleep(3)

# selenium / chromium configs
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# create output file
with open(f"{volume_path}/{output_file}", 'w') as out_f:
    writer = csv.writer(out_f, delimiter=',')
    headers = ["PLATE", "LENGTH", "AVAILABLE"]
    writer.writerow(headers)

    # load florida vanity plates page
    with webdriver.Remote(remote_host, options=chrome_options) as wd:
        wd.get('https://services.flhsmv.gov/MVCheckPersonalPlate/PlateInquiryView.aspx')

        # loop through test cases
        with open(f"{volume_path}/{input_file}", 'r') as in_f:
            reader = csv.reader(in_f, delimiter=',')
            for row in reader:
                test = row[0].upper()

                # validate test case ourselves
                if len(test) > 7:
                    print(f"Plate '{test}' is too long!")
                    continue

                # input our test
                input_field = wd.find_element(by=By.ID, value="MainContent_txtInputRowOne")
                input_field.clear()
                input_field.send_keys(test)

                # submit it
                submit_button = wd.find_element(by=By.ID, value="MainContent_btnSubmit")
                submit_button.click()

                # get output
                output_value = wd.find_element(by=By.ID, value="MainContent_lblOutPutRowOne").text
                result = output_value.strip().lower() == "available"

                # save result
                row = [test, len(test), result]
                writer.writerow(row)
                print(f"{test} -> {result}")
