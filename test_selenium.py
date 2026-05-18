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
if os.environ.get("CI") == "true":
    chrome_options.add_argument("--headless=new")  # Headless mode for CI/CD compatibility
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

TARGET_URL = "http://20.255.118.236"

def test_homepage_loaded(driver):
    """Test Case 1: Verify Homepage Loads Successfully"""
    print("\n--- Running Test Case 1: Verify Homepage Loads ---")
    driver.get(TARGET_URL)
    time.sleep(2)  # Let React fully load
    
    actual_title = driver.title
    print(f"Homepage Title: '{actual_title}'")
    assert "Sufyan" in actual_title or "Digital Twin" in actual_title, f"Title assertion failed! Got: {actual_title}"
    take_ss(driver, "01_homepage_loaded")
    print("[PASS] Test Case 1 Succeeded!")

def test_dashboard_loaded(driver):
    """Test Case 2: Navigate to Dashboard and Wait for Postgres Seed Data"""
    print("\n--- Running Test Case 2: Navigate to Dashboard ---")
    driver.get(TARGET_URL)
    time.sleep(2)
    
    try:
        # Navigate to Dashboard
        dash_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-dash-btn"))
        )
        dash_btn.click()
        
        # Pause 3 seconds to let React fetch dynamic projects from PostgreSQL
        print("Waiting 3 seconds for dynamic Postgres project cards to load...")
        time.sleep(3)
        
        take_ss(driver, "02_dashboard_loaded")
        
        # Verify that project elements are loaded on the screen
        project_cards = driver.find_elements(By.CLASS_NAME, "project-card")
        print(f"Found {len(project_cards)} project cards loaded from PostgreSQL database container!")
        assert len(project_cards) > 0, "No projects loaded from the database container!"
        print("[PASS] Test Case 2 Succeeded!")
    except Exception as e:
        take_ss(driver, "02_dashboard_failed")
        pytest.fail(f"Test Case 2 failed: {str(e)}")

def test_about_loaded(driver):
    """Test Case 3: Navigate to About and Wait for Timeline Experience Data"""
    print("\n--- Running Test Case 3: Navigate to About ---")
    
    try:
        # Navigate to About
        about_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-about-btn"))
        )
        about_btn.click()
        
        # Pause 3 seconds to let React fetch dynamic timeline experience from PostgreSQL
        print("Waiting 3 seconds for dynamic timeline experience items to load...")
        time.sleep(3)
        
        take_ss(driver, "03_about_loaded")
        
        # Verify experience timeline block
        timeline_items = driver.find_elements(By.CLASS_NAME, "exp-card")
        print(f"Found {len(timeline_items)} timeline items loaded from PostgreSQL database container!")
        assert len(timeline_items) > 0, "No experience items loaded from the database container!"
        print("[PASS] Test Case 3 Succeeded!")
    except Exception as e:
        take_ss(driver, "03_about_failed")
        pytest.fail(f"Test Case 3 failed: {str(e)}")

def test_chatbot_behavior(driver):
    """Test Case 4: Validate Chatbot Form & AI Clone Behavior"""
    print("\n--- Running Test Case 4: Validate Chatbot Form & AI Behavior ---")
    driver.get(TARGET_URL)
    time.sleep(2)
    
    try:
        # Locate the chatbot text input using ID
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "chat-input"))
        )
        chat_input.send_keys("Tell me about your DevOps skills")
        
        # Locate and click send button using ID
        send_btn = driver.find_element(By.ID, "send-btn")
        send_btn.click()
        print("Sent message to chatbot: 'Tell me about your DevOps skills'")
        
        # Wait 3 seconds for AI response
        time.sleep(3)
        take_ss(driver, "04_chat_behavior")
        
        # Retrieve message list
        bubbles = driver.find_elements(By.CLASS_NAME, "msg-bubble")
        assert len(bubbles) > 1, "Chatbot response bubble was not rendered!"
        print(f"Chatbot returned a total of {len(bubbles) - 1} response message bubbles.")
        print("[PASS] Test Case 4 Succeeded!")
    except Exception as e:
        take_ss(driver, "04_chat_failed")
        pytest.fail(f"Test Case 4 failed: {str(e)}")

if __name__ == "__main__":
    print("Running Selenium tests sequentially via Pytest runner...")
    pytest.main([__file__, "-v", "-s"])
