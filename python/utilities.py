#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for lead extraction and data parsing
"""

import re
import logging

logger = logging.getLogger(__name__)

def extract_phone(text):
    """
    Extract phone numbers from text
    Supports Indian formats: 10-digit, with country code, with spaces, dashes
    """
    if not text:
        return "N/A"
    
    # Pattern for Indian phone numbers
    patterns = [
        r'\+91[-\s]?(\d{10})',  # +91 format
        r'91[-\s]?(\d{10})',     # 91 format
        r'(\d{10})',              # 10 digit format
        r'(\d{3}[-\s]?\d{3}[-\s]?\d{4})',  # xxx-xxx-xxxx format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            phone = match.group(1) if match.groups() else match.group(0)
            phone = re.sub(r'[^0-9]', '', phone)  # Remove non-digits
            if len(phone) >= 10:
                return phone[-10:]  # Return last 10 digits
    
    return "N/A"

def extract_year(text):
    """
    Extract year from text
    Looks for 4-digit numbers between 1900-2099
    """
    if not text:
        return "N/A"
    
    # Look for 4-digit year
    pattern = r'(19\d{2}|20\d{2})'
    matches = re.findall(pattern, text)
    
    if matches:
        # Return the most likely year (usually the last mentioned)
        year = matches[-1]
        year_int = int(year)
        
        # Validate year is reasonable (between 1990 and current year)
        if 1990 <= year_int <= 2025:
            return year
    
    return "N/A"

def extract_km(text):
    """
    Extract kilometers from text
    Looks for patterns like "50000 km", "50,000 km", "50k km"
    """
    if not text:
        return "N/A"
    
    patterns = [
        r'(\d{1,3}(?:,\d{3})*|\d+)\s*(?:km|KM|Km)',  # 50000 km or 50,000 km
        r'(\d+)\s*[kK]\s*(?:km|KM)',                   # 50k km
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            km = match.group(1)
            km = km.replace(',', '')  # Remove commas
            
            # Check if it's k format
            if match.group(0).lower().count('k') == 2:
                km = str(int(km) * 1000)
            
            try:
                km_int = int(km)
                if 0 <= km_int <= 500000:  # Valid km range
                    return km
            except ValueError:
                continue
    
    return "N/A"

def extract_brand(text):
    """
    Extract car brand/model from text
    Common Indian car brands
    """
    if not text:
        return "N/A"
    
    brands = [
        'Maruti', 'Hyundai', 'Mahindra', 'Tata', 'Toyota', 'Honda',
        'Renault', 'Kia', 'Skoda', 'Volkswagen', 'Ford', 'Suzuki',
        'Bajaj', 'Datsun', 'Chevrolet', 'Audi', 'BMW', 'Mercedes',
        'Jaguar', 'Land Rover', 'Audi', 'Porsche', 'MG', 'Citroen',
        'FORCE', 'Isuzu', 'Jeep', 'Ambassador', 'Hindustan',
    ]
    
    text_lower = text.lower()
    for brand in brands:
        if brand.lower() in text_lower:
            # Try to extract model name
            pattern = rf'{brand}\s+([\w\s]+?)(?:\d{{1,2}}|$)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{brand} {match.group(1).strip()}".strip()
            return brand
    
    return "N/A"

def is_owner(text):
    """
    Determine if seller is owner or dealer
    Returns: True if owner, False if dealer, None if unclear
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Owner indicators
    owner_keywords = [
        'owner', 'personal', 'single owner', 'first owner', 
        'original owner', 'used personally', 'khud use'
    ]
    
    # Dealer indicators
    dealer_keywords = [
        'dealer', 'showroom', 'dealership', 'automobile',
        'motors', 'auto sales', 'sale', 'business',
        'company', 'enterprise', 'shop',
    ]
    
    owner_count = sum(1 for kw in owner_keywords if kw in text_lower)
    dealer_count = sum(1 for kw in dealer_keywords if kw in text_lower)
    
    if owner_count > dealer_count:
        return True
    elif dealer_count > owner_count:
        return False
    else:
        return None

def extract_registration_number(text):
    """
    Extract vehicle registration number from text
    Indian format: 2 letters, 2 digits, 2 letters, 4 digits
    Example: DL01AB1234
    """
    if not text:
        return "N/A"
    
    # Indian vehicle registration pattern
    pattern = r'([A-Z]{2}[-\s]?\d{2}[-\s]?[A-Z]{2}[-\s]?\d{4})'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        reg_no = match.group(1).replace('-', '').replace(' ', '').upper()
        return reg_no
    
    return "N/A"

def extract_variant(text):
    """
    Extract car variant/trim level
    Examples: LXi, VXi, ZXi, MT, AT, etc.
    """
    if not text:
        return "N/A"
    
    variants = [
        'LXi', 'VXi', 'ZXi', 'ZXi+',
        'Asti', 'Alturas', 'XUV', 'TUV',
        'MT', 'AT', 'CVT', 'Automatic', 'Manual',
        'Plus', 'Pro', 'Max', 'Top',
        'Base', 'Standard', 'Limited',
    ]
    
    for variant in variants:
        if variant.lower() in text.lower():
            return variant
    
    return "N/A"

def sanitize_data(data):
    """
    Sanitize extracted data by removing extra spaces and standardizing format
    """
    if isinstance(data, str):
        return ' '.join(data.split())  # Remove extra whitespace
    return data

def validate_lead(lead):
    """
    Validate if lead has minimum required information
    """
    required_fields = ['phone', 'brand', 'year']
    
    for field in required_fields:
        if field not in lead or lead[field] == "N/A":
            return False
    
    return True
