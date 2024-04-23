from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def setup_driver():
    # Set path to your WebDriver
    driver = webdriver.Chrome()
    driver.get("http://sdetchallenge.fetch.com/")
    return driver


def enter_bars(driver, left_bars, right_bars):
    for i, bar in enumerate(left_bars):
        left_input = driver.find_element(By.ID, f'left_{i}')
        left_input.clear()
        left_input.send_keys(str(bar))

    for i, bar in enumerate(right_bars):
        right_input = driver.find_element(By.ID, f'right_{i}')
        right_input.clear()
        right_input.send_keys(str(bar))


def click_button(driver, button_id):
    # Press the button as needed
    try:
        # Wait until the button is clickable, which indicates that it's ready for a user action.
        button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, button_id)))
        button.click()
    except TimeoutException:
        print(f"Button {button_id} was not clickable after 5 seconds.")
    except Exception as e:
        print(f"An error occurred while clicking {button_id}: {e}")

def click_second_reset_button(driver):
    try:
        # Execute JavaScript to get the second reset button element
        reset_button = driver.execute_script("return document.querySelectorAll('.button#reset')[1];")
        # Simulate a click event on the second reset button element
        driver.execute_script("arguments[0].click();", reset_button)
    except Exception as e:
        print(f"An error occurred while clicking the second reset button: {e}")

def read_balance_result(driver):
    try:
        # Wait for the result list to be visible
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".game-info ol li"))
        )
        # Get the innerHTML content of the last result (last <li> element)
        last_result_html = results[-1].get_attribute("innerHTML")
        return last_result_html
    except TimeoutException:
        print("Loading took too much time or element not found")
        return None


def read_balance_result2(driver):
    game_info_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'game-info'))
    )
    # Find the <ol> element within the game-info element
    ol_element = game_info_element.find_element(By.TAG_NAME, 'ol')
    # Wait for the second <li> element to be present
    second_li_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.game-info ol li:nth-child(2)'))
    )
    return second_li_element.text

def find_fake_bar(driver):
    # Define groups of bars
    groups = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]

    # First Weighing
    enter_bars(driver, groups[0], groups[1])
    click_button(driver, 'weigh')
    result = read_balance_result(driver)
    click_second_reset_button(driver)

    if "<" in result or "lt" in result:
        suspect_group = groups[0]
    elif ">" in result or "gt" in result:
        suspect_group = groups[1]
    else:
        suspect_group = groups[2]

    # Second Weighing
    #print(result)
    enter_bars(driver, [suspect_group[0]], [suspect_group[1]])
    click_button(driver, 'weigh')

    # Retrieve the text content of the second <li> element
    result = read_balance_result2(driver)
    #print(result)
    if "<" in result:
        suspect_group_final = suspect_group[0]
    elif ">" in result:
        suspect_group_final = suspect_group[1]
    else:
        suspect_group_final = suspect_group[2]

    return suspect_group_final


def main():
    driver = setup_driver()
    try:
        fake_bar = find_fake_bar(driver)
        print(f"Fake bar is: {fake_bar}")
        click_button(driver, f'coin_{fake_bar}')
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        print(f"Alert message: {alert_text}")
        time.sleep(100)
    finally:
        time.sleep(2)  # Let the user see everything before closing
        driver.quit()


if __name__ == '__main__':
    main()
