import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SignUpPageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Assuming Chrome WebDriver
        self.driver.get("https://dashboard.zenwel.com/sign-up")  # Replace with actual URL

    def tearDown(self):
        self.driver.quit()

    def test_signup_form_elements(self):
        # Test presence of main form elements
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".signup-container"))
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "form[ref='loginForm']"))

    def test_tab1_elements(self):
        # Test elements in the first tab
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "input[name='name']"))
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "input[name='email']"))
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "input[name='password']"))
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".v-facebook-login"))

    def test_tab2_elements(self):
        # Switch to tab 2 (you may need to implement a method to switch tabs)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-block").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='company_name']"))
        )

        # Test elements in the second tab
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "input[name='company_name']"))
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "select[name='business_type_id']"))
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".signup-map-container"))

    def test_language_selector(self):
        # Test presence of language selector
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".switch-lang-footer"))

    def test_form_submission(self):
        # Fill out the form (you'll need to add more fields)
        self.driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test User")
        self.driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("test@example.com")
        self.driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("password123")

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-block").click()

        # Check for success message or next step (adjust based on your app's behavior)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".el-message--success"))
        )

if __name__ == "__main__":
    unittest.main()