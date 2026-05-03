"""
Job Description Web Scraper
Fetches and extracts job descriptions from popular job boards
Supports: LinkedIn, Naukri, Indeed, and other job portals
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)

# User agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def detect_job_board(url: str) -> Optional[str]:
    """Detect which job board the URL belongs to"""
    url_lower = url.lower()
    
    if 'linkedin.com' in url_lower:
        return 'linkedin'
    elif 'naukri.com' in url_lower:
        return 'naukri'
    elif 'indeed.com' in url_lower or 'indeed.co' in url_lower:
        return 'indeed'
    elif 'monster.com' in url_lower or 'monster.co' in url_lower:
        return 'monster'
    elif 'glassdoor.com' in url_lower or 'glassdoor.co' in url_lower:
        return 'glassdoor'
    else:
        return None


def extract_linkedin_jd(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    """Extract job description from LinkedIn"""
    try:
        # LinkedIn job title
        title_elem = soup.find('h1', {'class': re.compile(r'.*job.*title.*', re.I)}) or \
                     soup.find('h1') or \
                     soup.find('h2', {'class': re.compile(r'.*job.*title.*', re.I)})
        title = title_elem.get_text(strip=True) if title_elem else None
        
        # LinkedIn company name
        company_elem = soup.find('a', {'class': re.compile(r'.*company.*', re.I)}) or \
                       soup.find('span', {'class': re.compile(r'.*company.*', re.I)})
        company = company_elem.get_text(strip=True) if company_elem else None
        
        # LinkedIn job description
        desc_elem = soup.find('div', {'class': re.compile(r'.*description.*', re.I)}) or \
                    soup.find('section', {'class': re.compile(r'.*description.*', re.I)})
        
        if desc_elem:
            description = desc_elem.get_text(separator='\n', strip=True)
        else:
            # Fallback: get all text
            description = soup.get_text(separator='\n', strip=True)
        
        return {
            'title': title,
            'company': company,
            'raw_text': description
        }
    except Exception as e:
        logger.error(f"Error extracting LinkedIn JD: {e}")
        return {'title': None, 'company': None, 'raw_text': soup.get_text(separator='\n', strip=True)}


def extract_naukri_jd(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    """Extract job description from Naukri"""
    try:
        # Naukri job title
        title_elem = soup.find('h1', {'class': re.compile(r'.*job.*title.*', re.I)}) or \
                     soup.find('h1') or \
                     soup.find('span', {'class': 'jd-header-title'})
        title = title_elem.get_text(strip=True) if title_elem else None
        
        # Naukri company name
        company_elem = soup.find('a', {'class': 'comp-name'}) or \
                       soup.find('div', {'class': 'comp-name'}) or \
                       soup.find('span', {'class': re.compile(r'.*company.*', re.I)})
        company = company_elem.get_text(strip=True) if company_elem else None
        
        # Naukri job description
        desc_elem = soup.find('div', {'class': 'jd-desc'}) or \
                    soup.find('div', {'class': re.compile(r'.*description.*', re.I)}) or \
                    soup.find('section', {'class': re.compile(r'.*description.*', re.I)})
        
        if desc_elem:
            description = desc_elem.get_text(separator='\n', strip=True)
        else:
            description = soup.get_text(separator='\n', strip=True)
        
        return {
            'title': title,
            'company': company,
            'raw_text': description
        }
    except Exception as e:
        logger.error(f"Error extracting Naukri JD: {e}")
        return {'title': None, 'company': None, 'raw_text': soup.get_text(separator='\n', strip=True)}


def extract_indeed_jd(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    """Extract job description from Indeed"""
    try:
        # Indeed job title
        title_elem = soup.find('h1', {'class': re.compile(r'.*jobtitle.*', re.I)}) or \
                     soup.find('h1') or \
                     soup.find('h2', {'class': re.compile(r'.*jobtitle.*', re.I)})
        title = title_elem.get_text(strip=True) if title_elem else None
        
        # Indeed company name
        company_elem = soup.find('div', {'class': re.compile(r'.*company.*', re.I)}) or \
                       soup.find('span', {'class': re.compile(r'.*company.*', re.I)})
        company = company_elem.get_text(strip=True) if company_elem else None
        
        # Indeed job description
        desc_elem = soup.find('div', {'id': 'jobDescriptionText'}) or \
                    soup.find('div', {'class': re.compile(r'.*jobsearch-jobDescriptionText.*', re.I)}) or \
                    soup.find('div', {'class': re.compile(r'.*description.*', re.I)})
        
        if desc_elem:
            description = desc_elem.get_text(separator='\n', strip=True)
        else:
            description = soup.get_text(separator='\n', strip=True)
        
        return {
            'title': title,
            'company': company,
            'raw_text': description
        }
    except Exception as e:
        logger.error(f"Error extracting Indeed JD: {e}")
        return {'title': None, 'company': None, 'raw_text': soup.get_text(separator='\n', strip=True)}


def extract_generic_jd(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    """Generic fallback extraction for unknown job boards"""
    try:
        # Try to find title (usually in h1 or h2)
        title_elem = soup.find('h1') or soup.find('h2')
        title = title_elem.get_text(strip=True) if title_elem else None
        
        # Try to find company (common class names)
        company_elem = soup.find('span', {'class': re.compile(r'.*company.*', re.I)}) or \
                       soup.find('div', {'class': re.compile(r'.*company.*', re.I)}) or \
                       soup.find('a', {'class': re.compile(r'.*company.*', re.I)})
        company = company_elem.get_text(strip=True) if company_elem else None
        
        # Get all text as description
        description = soup.get_text(separator='\n', strip=True)
        
        return {
            'title': title,
            'company': company,
            'raw_text': description
        }
    except Exception as e:
        logger.error(f"Error extracting generic JD: {e}")
        return {'title': None, 'company': None, 'raw_text': soup.get_text(separator='\n', strip=True)}


def fetch_jd_from_url(url: str) -> Dict[str, any]:
    """
    Fetch and extract job description from a URL
    
    Returns:
        {
            'success': bool,
            'title': str or None,
            'company': str or None,
            'raw_text': str,
            'job_board': str or None,
            'error': str or None
        }
    """
    try:
        # Validate URL
        if not url or not url.startswith('http'):
            return {
                'success': False,
                'error': 'Invalid URL. Please provide a valid HTTP/HTTPS URL.'
            }
        
        # Detect job board
        job_board = detect_job_board(url)
        logger.info(f"Fetching JD from URL: {url} (detected: {job_board})")
        
        # Fetch the page
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract JD based on job board
        if job_board == 'linkedin':
            result = extract_linkedin_jd(soup)
        elif job_board == 'naukri':
            result = extract_naukri_jd(soup)
        elif job_board == 'indeed':
            result = extract_indeed_jd(soup)
        else:
            result = extract_generic_jd(soup)
        
        # Validate that we got some text
        if not result['raw_text'] or len(result['raw_text'].strip()) < 100:
            return {
                'success': False,
                'error': 'Could not extract sufficient job description text from the URL. The page may require authentication or the structure is not supported.'
            }
        
        return {
            'success': True,
            'title': result['title'],
            'company': result['company'],
            'raw_text': result['raw_text'],
            'job_board': job_board
        }
    
    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching URL: {url}")
        return {
            'success': False,
            'error': 'Request timed out. The job board may be slow or unavailable.'
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return {
            'success': False,
            'error': f'Error fetching the URL: {str(e)}'
        }
    except Exception as e:
        logger.error(f"Unexpected error fetching JD from URL {url}: {e}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }
