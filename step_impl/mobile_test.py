from getgauge.python import step, before_scenario, after_scenario, data_store, before_suite, after_suite
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import subprocess

def force_stop_app():
    """强制停止应用"""
    try:
        subprocess.run(['adb', 'shell', 'am', 'force-stop', 'com.swaglabsmobileapp'], 
                      check=True, capture_output=True)
        print("Successfully force stopped the app")
    except subprocess.CalledProcessError as e:
        print(f"Error force stopping app: {e.stderr}")

# SwagLabs app capabilities
ANDROID_OPTIONS = UiAutomator2Options()
ANDROID_OPTIONS.platform_name = 'Android'
ANDROID_OPTIONS.automation_name = 'UiAutomator2'
ANDROID_OPTIONS.device_name = 'ZL5227R9TD'
ANDROID_OPTIONS.platform_version = '10'
ANDROID_OPTIONS.app_package = 'com.swaglabsmobileapp'
ANDROID_OPTIONS.app_activity = '.MainActivity'
ANDROID_OPTIONS.no_reset = True
ANDROID_OPTIONS.auto_grant_permissions = True
ANDROID_OPTIONS.set_capability('newCommandTimeout', 300)

# Element locators
LOCATORS = {
    'username_field': (AppiumBy.ACCESSIBILITY_ID, 'test-Username'),
    'password_field': (AppiumBy.ACCESSIBILITY_ID, 'test-Password'),
    'login_button': (AppiumBy.ACCESSIBILITY_ID, 'test-LOGIN'),
    'products_title': (AppiumBy.XPATH, "//android.widget.TextView[@text='PRODUCTS']")
}

@before_suite
def before_suite_hook():
    # 确保在套件开始前强制停止应用
    force_stop_app()

@before_scenario
def init():
    data_store.scenario.clear()
    # 确保在场景开始前强制停止应用
    force_stop_app()

@step("Start SwagLabs mobile app")
def start_app():
    try:
        # Create driver instance with options
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            options=ANDROID_OPTIONS
        )
        driver.implicitly_wait(10)  # Add implicit wait
        data_store.scenario["driver"] = driver
        print("Successfully connected to Appium server and started the app")
    except Exception as e:
        print(f"Failed to start app: {str(e)}")
        raise

@step("Enter username <username>")
def enter_username(username):
    driver = data_store.scenario["driver"]
    try:
        # Wait for username field and enter text
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(LOCATORS['username_field'])
        )
        username_field.clear()
        username_field.send_keys(username)
    except Exception as e:
        driver.save_screenshot("username_error.png")
        raise Exception(f"Failed to enter username: {str(e)}")

@step("Enter password <password>")
def enter_password(password):
    driver = data_store.scenario["driver"]
    try:
        # Wait for password field and enter text
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(LOCATORS['password_field'])
        )
        password_field.clear()
        password_field.send_keys(password)
    except Exception as e:
        driver.save_screenshot("password_error.png")
        raise Exception(f"Failed to enter password: {str(e)}")

@step("Click login button")
def click_login():
    driver = data_store.scenario["driver"]
    try:
        # Wait for login button and click
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(LOCATORS['login_button'])
        )
        login_button.click()
    except Exception as e:
        driver.save_screenshot("login_error.png")
        raise Exception(f"Failed to click login button: {str(e)}")

@step("Verify successful login")
def verify_login():
    driver = data_store.scenario["driver"]
    try:
        # Wait for products title to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(LOCATORS['products_title'])
        )
    except TimeoutException:
        driver.save_screenshot("verify_login_error.png")
        raise Exception("Login verification failed - Products title not found")

@step("Close mobile app")
def close_app():
    if "driver" in data_store.scenario:
        try:
            driver = data_store.scenario["driver"]
            if driver:
                driver.quit()
                print("Successfully closed the mobile app")
        except Exception as e:
            print(f"Error closing app: {str(e)}")
        finally:
            del data_store.scenario["driver"]
            force_stop_app()

@after_scenario
def cleanup():
    # 确保在场景结束后关闭应用
    if "driver" in data_store.scenario:
        try:
            driver = data_store.scenario["driver"]
            if driver:
                driver.quit()
                print("Successfully closed the mobile app in cleanup")
        except Exception as e:
            print(f"Error in cleanup: {str(e)}")
        finally:
            del data_store.scenario["driver"]
            force_stop_app()

@after_suite
def after_suite_hook():
    # 确保在套件结束后清理所有资源
    if hasattr(data_store.suite, 'driver'):
        try:
            data_store.suite.driver.quit()
        except:
            pass
        finally:
            delattr(data_store.suite, 'driver')
            force_stop_app()
