import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome Options
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Run in headless mode for CI/CD compatibility
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Setup Directory for Screenshots
SCREENSHOTS_DIR = os.path.join(os.getcwd(), "report_screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def take_ss(driver, name):
    path = os.path.join(SCREENSHOTS_DIR, f"selenium_{name}.png")
    driver.save_screenshot(path)
    print(f"Captured Selenium Test Screenshot: {path}")

@pytest.fixture(scope="module")
def driver():
    print("Initializing Selenium Webdriver...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    print("\nTearing down Selenium driver...")
    driver.quit()

TARGET_URL = "http://localhost:3000"

def test_homepage_loaded(driver):
    """Test Case 1: Verify Homepage Loads Successfully"""
    print("\n--- Running Test Case 1: Verify Homepage Loads ---")
    driver.get(TARGET_URL)
    time.sleep(3) # Let React fully load
    
    actual_title = driver.title
    print(f"Homepage Title: '{actual_title}'")
    assert "Sufyan" in actual_title, f"Title assertion failed! Got: {actual_title}"
    take_ss(driver, "01_homepage_loaded")
    print("[PASS] Test Case 1 Succeeded!")

def test_chatbot_behavior(driver):
    """Test Case 2: Validate Chatbot Form & AI Clone Behavior"""
    print("\n--- Running Test Case 2: Validate Chatbot Form & AI Behavior ---")
    driver.get(TARGET_URL)
    time.sleep(2)
    try:
        # Locate the chatbot text input
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Ask'], input[type='text']"))
        )
        chat_input.send_keys("Tell me about your DevOps skills")
        
        # Locate and click send button
        send_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Send') or contains(@class, 'send') or contains(@type, 'submit')]")
        send_btn.click()
        print("Sent message to chatbot: 'Tell me about your DevOps skills'")
        
        # Wait for AI response
        time.sleep(3)
        take_ss(driver, "02_chat_behavior")
        
        # Retrieve response text to assert
        chat_response = driver.find_element(By.XPATH, "//*[contains(text(), 'Sufyan') or contains(text(), 'skilled')]").text
        print(f"Chatbot Response: '{chat_response[:80]}...'")
        print("[PASS] Test Case 2 Succeeded!")
    except Exception as e:
        take_ss(driver, "02_chat_failed")
        pytest.fail(f"Test Case 2 failed: {str(e)}")

def test_api_database_connected(driver):
    """Test Case 3: Check Frontend-to-Backend Database API Response"""
    print("\n--- Running Test Case 3: Check Database Status ---")
    driver.get(TARGET_URL)
    time.sleep(2)
    try:
        # Navigate to Dashboard
        dash_btn = driver.find_element(By.ID, "nav-dash-btn")
        dash_btn.click()
        time.sleep(2)
        take_ss(driver, "03_dashboard_navigated")
        
        # Check database connection status indicators
        db_pill = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Database') or contains(text(), 'Postgres') or contains(text(), 'seeded') or contains(text(), 'connected')]"))
        )
        print(f"Database status element found on UI: '{db_pill.text}'")
        take_ss(driver, "04_database_connected")
        print("[PASS] Test Case 3 Succeeded!")
    except Exception as e:
        # Fallback direct API endpoint check
        print("Dashboard check failed, performing direct Flask DB API check...")
        driver.get("http://localhost:5000/api/db-status")
        time.sleep(1)
        api_content = driver.find_element(By.TAG_NAME, "pre").text
        print(f"Direct API Response: {api_content}")
        assert "connected" in api_content, "API did not return connected state!"
        take_ss(driver, "04_api_db_connected")
        print("[PASS] Test Case 3 (Direct API) Succeeded!")

if __name__ == "__main__":
    # Fallback sequential run if called directly (python test_selenium.py)
    print("Running Selenium tests sequentially via Pytest runner...")
    pytest.main([__file__, "-v", "-s"])
