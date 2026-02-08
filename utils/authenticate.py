"""PFF authentication helpers using Selenium."""

import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


def login_to_pff() -> webdriver.Chrome:
    """Log into auth.pff.com and return an authenticated Chrome driver."""
    signinurl = "https://auth.pff.com"
    email = os.environ.get("PFF_EMAIL")
    pw = os.environ.get("PFF_PASSWORD")
    email_input = '//*[@id="login-form_email"]'
    pw_input = '//*[@id="login-form_password"]'
    login_submit = '//*[@id="sign-in"]'

    driver = webdriver.Chrome()
    driver.get(signinurl)

    driver.find_element("xpath", email_input).send_keys(email)
    driver.find_element("xpath", pw_input).send_keys(pw)

    time.sleep(3)

    driver.find_element("xpath", login_submit).click()

    return driver


def navigate_and_sign_in(driver: webdriver.Chrome, url: str) -> None:
    """Navigate to a PFF page and click the sign-in button if prompted."""
    driver.get(url)

    # Wait for the "Sign In" button to appear and click it
    try:
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "g-btn--green")]'))
        )
        sign_in_button.click()
        time.sleep(3)  # Allow time for the sign-in process to complete if necessary
    except Exception as e:
        logger.info("Sign In button not found or not needed for this page: %s", e)
