#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FB Marketplace + OLX WebStore Lead Agent
Automated lead extraction, messaging, and Google Sheets integration
With Chrome Extension and WebStore support
"""

import os
import json
import time
import requests
import logging
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from utilities import extract_phone, extract_year, extract_km, extract_brand, is_owner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LeadAgent:
    def __init__(self, config_path='config.json'):
        """
        Initialize Lead Agent with configuration
        """
        self.config = self.load_config(config_path)
        self.driver = None
        self.webhook_url = self.config.get('webhook_url')
        self.chrome_driver_path = self.setup_chromedriver()
        logger.info("Lead Agent initialized")
        
    def load_config(self, config_path):
        """
        Load configuration from JSON file
        """
        if not os.path.exists(config_path):
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self.get_default_config()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_default_config(self):
        """
        Return default configuration
        """
        return {
            "webhook_url": "",
            "platforms": ["facebook", "olx_webstore"],
            "auto_message": True,
            "message_delay": 2,
            "owner_patterns": [
                "aap khud chalate ho?",
                "Direct owner?",
                "Owner driving?"
            ],
            "dealer_patterns": [
                "Dealer ho ya owner?",
                "Business h ya apni?"
            ]
        }
    
    def setup_chromedriver(self):
        """
        Automatically download and setup ChromeDriver
        Returns path to ChromeDriver
        """
        try:
            logger.info("Setting up ChromeDriver...")
            driver_path = ChromeDriverManager().install()
            logger.info(f"ChromeDriver setup complete: {driver_path}")
            return driver_path
        except Exception as e:
            logger.error(f"Error setting up ChromeDriver: {e}")
            raise
    
    def create_driver(self):
        """
        Create Selenium WebDriver with Chrome options
        """
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment for headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        try:
            service = Service(self.chrome_driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome driver created successfully")
            return self.driver
        except Exception as e:
            logger.error(f"Error creating Chrome driver: {e}")
            raise
    
    def extract_leads_facebook(self):
        """
        Extract leads from Facebook Marketplace
        Returns list of lead dictionaries
        """
        logger.info("Starting Facebook Marketplace lead extraction")
        leads = []
        
        try:
            # Navigate to Facebook (manual login required)
            self.driver.get("https://www.facebook.com/marketplace")
            logger.info("Navigated to Facebook Marketplace")
            
            # Wait for user to manually login and load marketplace
            input("Please login to Facebook and open desired marketplace listings. Press Enter when ready...")
            
            # Extract listing information
            listings = self.driver.find_elements(By.CSS_SELECTOR, "[role='article']")
            logger.info(f"Found {len(listings)} listings")
            
            for listing in listings[:10]:  # Process first 10 listings
                try:
                    lead_data = self.parse_facebook_listing(listing)
                    if lead_data:
                        leads.append(lead_data)
                        logger.info(f"Extracted lead: {lead_data.get('phone')}")
                except Exception as e:
                    logger.warning(f"Error parsing Facebook listing: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting Facebook leads: {e}")
        
        return leads
    
    def parse_facebook_listing(self, listing_element):
        """
        Parse individual Facebook listing element
        """
        try:
            title = listing_element.find_element(By.CSS_SELECTOR, "h2").text
            price = listing_element.find_element(By.CSS_SELECTOR, "span[class*='price']").text
            seller_info = listing_element.find_element(By.CSS_SELECTOR, "[class*='seller']").text
            
            return {
                "platform": "Facebook",
                "title": title,
                "price": price,
                "seller_name": seller_info,
                "phone": extract_phone(seller_info),
                "year": extract_year(title),
                "km": extract_km(title),
                "brand": extract_brand(title),
                "is_owner": is_owner(seller_info),
                "extracted_date": datetime.now().isoformat(),
                "source": "Facebook Marketplace"
            }
        except Exception as e:
            logger.warning(f"Error parsing listing: {e}")
            return None
    
    def extract_leads_olx_webstore(self):
        """
        Extract leads from OLX WebStore
        Returns list of lead dictionaries
        """
        logger.info("Starting OLX WebStore lead extraction")
        leads = []
        
        try:
            # Navigate to OLX WebStore
            self.driver.get("https://www.olx.in/autos/cars/")
            logger.info("Navigated to OLX Cars section")
            
            # Wait for user interaction if needed
            time.sleep(2)
            
            # Extract listings
            listings = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='ad-card']")
            logger.info(f"Found {len(listings)} OLX listings")
            
            for listing in listings[:10]:  # Process first 10 listings
                try:
                    lead_data = self.parse_olx_listing(listing)
                    if lead_data:
                        leads.append(lead_data)
                        logger.info(f"Extracted OLX lead: {lead_data.get('phone')}")
                except Exception as e:
                    logger.warning(f"Error parsing OLX listing: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting OLX leads: {e}")
        
        return leads
    
    def parse_olx_listing(self, listing_element):
        """
        Parse individual OLX listing element
        """
        try:
            # Extract listing details
            title = listing_element.find_element(By.CSS_SELECTOR, "span[class*='title']").text
            
            try:
                price = listing_element.find_element(By.CSS_SELECTOR, "span[class*='price']").text
            except:
                price = "N/A"
            
            try:
                location = listing_element.find_element(By.CSS_SELECTOR, "span[class*='location']").text
            except:
                location = "N/A"
            
            return {
                "platform": "OLX WebStore",
                "title": title,
                "price": price,
                "location": location,
                "year": extract_year(title),
                "km": extract_km(title),
                "brand": extract_brand(title),
                "extracted_date": datetime.now().isoformat(),
                "source": "OLX WebStore"
            }
        except Exception as e:
            logger.warning(f"Error parsing OLX listing: {e}")
            return None
    
    def send_to_sheets(self, lead):
        """
        Send lead data to Google Sheets via webhook
        """
        if not self.webhook_url:
            logger.warning("Webhook URL not configured")
            return False
        
        try:
            # Prepare data according to Google Sheets columns
            payload = {
                "DATE": lead.get('extracted_date', datetime.now().isoformat()),
                "NAME": lead.get('seller_name', 'N/A'),
                "MOBILE": lead.get('phone', 'N/A'),
                "REG_NO": lead.get('reg_no', 'N/A'),
                "CAR_MODEL": lead.get('brand', 'N/A'),
                "VARIANT": lead.get('variant', 'N/A'),
                "YEAR": lead.get('year', 'N/A'),
                "KM": lead.get('km', 'N/A'),
                "ADDRESS": lead.get('location', 'N/A'),
                "FOLLOW_UP": "Pending",
                "SOURCE": lead.get('source', 'N/A'),
                "CONTEXT": f"Owner: {lead.get('is_owner', 'N/A')}",
                "LICENSE": "Verified",
                "REMARK": lead.get('title', 'N/A')
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code in [200, 201]:
                logger.info(f"Lead sent to sheets successfully: {lead.get('phone')}")
                return True
            else:
                logger.warning(f"Failed to send lead: {response.status_code}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending lead to sheets: {e}")
            return False
    
    def run(self):
        """
        Main execution function
        """
        try:
            self.create_driver()
            all_leads = []
            
            # Extract from configured platforms
            if "facebook" in self.config.get('platforms', []):
                fb_leads = self.extract_leads_facebook()
                all_leads.extend(fb_leads)
            
            if "olx_webstore" in self.config.get('platforms', []):
                olx_leads = self.extract_leads_olx_webstore()
                all_leads.extend(olx_leads)
            
            # Send all leads to Google Sheets
            for lead in all_leads:
                self.send_to_sheets(lead)
                time.sleep(self.config.get('message_delay', 2))
            
            logger.info(f"Processed {len(all_leads)} total leads")
        
        except Exception as e:
            logger.error(f"Error in main execution: {e}")
        
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Chrome driver closed")

def main():
    """
    Entry point
    """
    agent = LeadAgent()
    agent.run()

if __name__ == "__main__":
    main()
