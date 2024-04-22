from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def setup_driver():
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.get("http://sdetchallenge.fetch.com/")
    return driver  # Return the driver object


def main():
    driver = setup_driver()  # Initialize WebDriver and get the driver object

    # Keep the script running until user closes the browser manually
    while True:
        time.sleep(10)  # Add a delay to prevent the script from consuming CPU resources unnecessarily


if __name__ == '__main__':
    main()
