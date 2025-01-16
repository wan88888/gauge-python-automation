from getgauge.python import step, before_scenario, after_scenario, data_store
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

@before_scenario
def init():
    data_store.scenario.clear()

@step("Open browser <browser_type>")
def open_browser(browser_type):
    if browser_type.lower() == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser_type.lower() == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    driver.maximize_window()
    data_store.scenario["driver"] = driver

@step("Navigate to Baidu")
def navigate_to_baidu():
    driver = data_store.scenario["driver"]
    driver.get("https://www.baidu.com")
    # Wait for the page to be fully loaded
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    # Wait for the search box to be present and interactable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "kw"))
    )

@step("Search for <query>")
def search(query):
    driver = data_store.scenario["driver"]
    try:
        # Wait for the search box to be clickable
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "kw"))
        )
        # Try to interact with the element
        search_box.click()
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
    except (TimeoutException, ElementNotInteractableException) as e:
        # Take screenshot for debugging
        driver.save_screenshot("search_error.png")
        raise Exception(f"Failed to interact with search box: {str(e)}")

@step("Verify search results are displayed")
def verify_search_results():
    driver = data_store.scenario["driver"]
    try:
        # Wait for search results to be present and visible
        results = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "content_left"))
        )
        assert results.is_displayed(), "Search results are not displayed"
    except TimeoutException:
        # Take screenshot for debugging
        driver.save_screenshot("results_error.png")
        raise Exception("Search results did not appear within timeout")

@step("Close browser")
def close_browser():
    driver = data_store.scenario["driver"]
    if driver:
        driver.quit()

@after_scenario
def cleanup():
    # Ensure browser is closed even if test fails
    if "driver" in data_store.scenario:
        try:
            data_store.scenario["driver"].quit()
        except:
            pass
