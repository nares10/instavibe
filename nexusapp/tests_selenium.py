"""
Selenium UI Tests for Nexus Application
Browser-based automation testing
Requires: pip install selenium

Note: Download ChromeDriver from https://chromedriver.chromium.org/
Or use webdriver-manager: pip install webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from .models import Profile


class SeleniumUITestBase(LiveServerTestCase):
    """Base class for Selenium tests with common setup"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Chrome options
        chrome_options = Options()
        # Uncomment to run headless (no UI):
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            # Try using webdriver-manager (recommended)
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        except ImportError:
            # Fallback to system chromedriver
            cls.driver = webdriver.Chrome(options=chrome_options)
        
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        Profile.objects.create(user=self.user)


class SeleniumAuthTests(SeleniumUITestBase):
    """Test authentication flows in browser"""
    
    def test_login_with_browser(self):
        """Test login flow in real browser"""
        # Navigate to login page
        self.driver.get(f'{self.live_server_url}/login/')
        
        # Find and fill username field
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('testuser')
        
        # Find and fill password field
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('TestPass123!')
        
        # Find and click login button
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for redirect to home page
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/home/')
        )
        
        # Verify we're on home page
        self.assertIn('/home/', self.driver.current_url)
    
    def test_logout_with_browser(self):
        """Test logout flow in real browser"""
        # Login first
        self.driver.get(f'{self.live_server_url}/login/')
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('testuser')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('TestPass123!')
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/home/')
        )
        
        # Find and click logout
        logout_button = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logout_button.click()
        
        # Wait for redirect
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/')
        )


class SeleniumProfileTests(SeleniumUITestBase):
    """Test profile interactions in browser"""
    
    def test_view_profile_in_browser(self):
        """Test viewing profile page"""
        # Login
        self.driver.get(f'{self.live_server_url}/login/')
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('testuser')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('TestPass123!')
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Navigate to profile
        self.driver.get(f'{self.live_server_url}/profile/testuser/')
        
        # Wait for profile page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'profile'))
        )
        
        # Verify username is displayed
        username_text = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('testuser', username_text)
    
    def test_edit_profile_in_browser(self):
        """Test editing profile"""
        # Login
        self.driver.get(f'{self.live_server_url}/login/')
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('testuser')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('TestPass123!')
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Navigate to edit profile
        self.driver.get(f'{self.live_server_url}/edit_profile/')
        
        # Wait for form to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'bio'))
        )
        
        # Fill bio field
        bio_field = self.driver.find_element(By.NAME, 'bio')
        bio_field.clear()
        bio_field.send_keys('Updated bio from Selenium test')
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Verify redirect
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/profile/')
        )


class SeleniumPostTests(SeleniumUITestBase):
    """Test post interactions in browser"""
    
    def test_create_post_in_browser(self):
        """Test creating a post through UI"""
        # Login
        self.driver.get(f'{self.live_server_url}/login/')
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('testuser')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('TestPass123!')
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Navigate to create post
        self.driver.get(f'{self.live_server_url}/create_post/')
        
        # Wait for form
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'caption'))
        )
        
        # Fill caption
        caption_field = self.driver.find_element(By.NAME, 'caption')
        caption_field.send_keys('Test post from Selenium')
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Wait for redirect
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/feed/')
        )


class SeleniumNavigationTests(SeleniumUITestBase):
    """Test navigation and page loading"""
    
    def test_navigation_menu_in_browser(self):
        """Test that navigation menu works"""
        # Login
        self.driver.get(f'{self.live_server_url}/login/')
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('testuser')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('TestPass123!')
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/home/')
        )
        
        # Test navigation to explore
        explore_link = self.driver.find_element(By.LINK_TEXT, 'Explore')
        explore_link.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/explore/')
        )
        
        # Test navigation to notifications
        notifications_link = self.driver.find_element(By.LINK_TEXT, 'Notifications')
        notifications_link.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('/notifications/')
        )


# Run tests with: python manage.py test nexusapp.tests_selenium
# Installation requirements:
# pip install selenium webdriver-manager
# 
# Run headless (no browser window):
# - Uncomment chrome_options.add_argument("--headless") in setUpClass
