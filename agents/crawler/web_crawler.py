"""
Web Crawler Agent for ByteBreaker
"""
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime
import json

class WebCrawlerAgent:
    """Autonomous web crawler agent"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.visited_urls = set()
        self.discovered_urls = set()
        self.session = None
        self.results = []
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={"User-Agent": self.config.scanner.user_agent}
            )
        return self.session
    
    async def crawl(self, start_url: str, max_pages: int = 100, 
                   max_depth: int = 3, same_domain: bool = True) -> Dict[str, Any]:
        """Crawl website starting from URL"""
        self.visited_urls.clear()
        self.discovered_urls.clear()
        self.results = []
        
        start_domain = urlparse(start_url).netloc
        
        await self._crawl_recursive(start_url, start_domain, max_pages, max_depth, 0, same_domain)
        
        return {
            "start_url": start_url,
            "pages_crawled": len(self.visited_urls),
            "urls_discovered": len(self.discovered_urls),
            "results": self.results,
            "crawl_time": datetime.now().isoformat()
        }
    
    async def _crawl_recursive(self, url: str, domain: str, max_pages: int, 
                              max_depth: int, current_depth: int, same_domain: bool) -> None:
        """Recursive crawl function"""
        if current_depth >= max_depth:
            return
        
        if len(self.visited_urls) >= max_pages:
            return
        
        if url in self.visited_urls:
            return
        
        # Check domain restriction
        if same_domain and urlparse(url).netloc != domain:
            return
        
        self.visited_urls.add(url)
        
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    
                    if 'text/html' in content_type:
                        html = await response.text()
                        
                        # Extract information
                        page_info = await self._extract_page_info(url, html)
                        self.results.append(page_info)
                        
                        # Extract links
                        links = self._extract_links(html, url)
                        
                        # Crawl discovered links
                        for link in links:
                            if link not in self.discovered_urls:
                                self.discovered_urls.add(link)
                                
                                # Recursive crawl
                                await self._crawl_recursive(
                                    link, domain, max_pages, max_depth, 
                                    current_depth + 1, same_domain
                                )
                    
                    elif 'application/json' in content_type:
                        json_data = await response.json()
                        self.results.append({
                            "url": url,
                            "type": "json",
                            "data": json_data
                        })
        
        except Exception as e:
            self.logger.error(f"Crawl failed for {url}: {e}")
            self.results.append({
                "url": url,
                "type": "error",
                "error": str(e)
            })
    
    async def _extract_page_info(self, url: str, html: str) -> Dict[str, Any]:
        """Extract information from HTML page"""
        info = {
            "url": url,
            "type": "html",
            "title": self._extract_title(html),
            "meta_tags": self._extract_meta_tags(html),
            "forms": self._extract_forms(html),
            "scripts": self._extract_scripts(html),
            "emails": self._extract_emails(html),
            "links_count": len(self._extract_links(html, url))
        }
        return info
    
    def _extract_title(self, html: str) -> str:
        """Extract page title"""
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return match.group(1) if match else ""
    
    def _extract_meta_tags(self, html: str) -> Dict[str, str]:
        """Extract meta tags"""
        meta_tags = {}
        for match in re.finditer(r'<meta\s+name=["\']([^"\']+)["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE):
            meta_tags[match.group(1)] = match.group(2)
        return meta_tags
    
    def _extract_forms(self, html: str) -> List[Dict[str, Any]]:
        """Extract forms from HTML"""
        forms = []
        for match in re.finditer(r'<form.*?</form>', html, re.IGNORECASE | re.DOTALL):
            form_html = match.group(0)
            action = re.search(r'action=["\']([^"\']+)["\']', form_html, re.IGNORECASE)
            method = re.search(r'method=["\']([^"\']+)["\']', form_html, re.IGNORECASE)
            
            inputs = []
            for input_match in re.finditer(r'<input[^>]+>', form_html, re.IGNORECASE):
                input_html = input_match.group(0)
                input_type = re.search(r'type=["\']([^"\']+)["\']', input_html, re.IGNORECASE)
                input_name = re.search(r'name=["\']([^"\']+)["\']', input_html, re.IGNORECASE)
                
                inputs.append({
                    "type": input_type.group(1) if input_type else "text",
                    "name": input_name.group(1) if input_name else ""
                })
            
            forms.append({
                "action": action.group(1) if action else "",
                "method": method.group(1) if method else "GET",
                "inputs": inputs
            })
        
        return forms
    
    def _extract_scripts(self, html: str) -> List[str]:
        """Extract script sources"""
        scripts = []
        for match in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE):
            scripts.append(match.group(1))
        return scripts
    
    def _extract_emails(self, html: str) -> List[str]:
        """Extract email addresses"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return list(set(re.findall(email_pattern, html)))
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract and normalize links"""
        links = []
        for match in re.finditer(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE):
            link = match.group(1)
            if link.startswith('http'):
                links.append(link)
            elif link.startswith('/'):
                links.append(urljoin(base_url, link))
            elif not link.startswith('#') and not link.startswith('javascript:'):
                links.append(urljoin(base_url + '/', link))
        return list(set(links))
