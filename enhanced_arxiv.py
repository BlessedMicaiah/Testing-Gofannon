#!/usr/bin/env python3
"""
Enhanced ArXiv Search Module
This module extends the ArXiv search capabilities with better formatting and additional features.
"""
import os
import re
import json
import logging
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

class EnhancedArxivSearch:
    """Enhanced ArXiv search with better formatting and additional features"""
    
    def __init__(self):
        """Initialize the enhanced ArXiv search"""
        logger.info("Initializing EnhancedArxivSearch...")
        
        # Set up Google Search if available
        google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        google_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "f60d7c389de5240cd")  # Default from render.yaml
        
        self.has_google_search = bool(google_api_key) and bool(google_engine_id)
        
        if self.has_google_search:
            logger.info("Google Search API is available for enhanced results")
            logger.info(f"Using Google Search Engine ID: {google_engine_id}")
        else:
            logger.info("Google Search API is not available - will use ArXiv only")
    
    def search(self, query, max_results=5, include_abstracts=True, sort_by="relevance"):
        """
        Search for research papers on ArXiv
        
        Args:
            query (str): The search query
            max_results (int): Maximum number of results to return
            include_abstracts (bool): Whether to include abstracts in the results
            sort_by (str): How to sort the results (relevance, date)
            
        Returns:
            dict: Formatted search results
        """
        logger.info(f"Searching ArXiv for: {query}")
        
        # Query ArXiv API
        arxiv_results = self._query_arxiv(query, max_results)
        
        # Parse the results
        parsed_results = self._parse_arxiv_response(arxiv_results)
        
        # Enhance results with Google Search if available
        if self.has_google_search:
            logger.info("Enhancing results with Google Search")
            enhanced_results = self._enhance_with_google(parsed_results, query)
        else:
            enhanced_results = parsed_results
        
        # Format the results for display
        formatted_results = self._format_results(enhanced_results, include_abstracts)
        
        return formatted_results
    
    def _query_arxiv(self, query, max_results=5):
        """
        Query the ArXiv API
        
        Args:
            query (str): The search query
            max_results (int): Maximum number of results to return
            
        Returns:
            str: XML response from ArXiv
        """
        logger.info(f"Querying ArXiv API for: {query}")
        
        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                logger.info(f"ArXiv API returned {max_results} results")
                return response.text
            else:
                logger.error(f"ArXiv API error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error querying ArXiv: {str(e)}")
            return None
    
    def _parse_arxiv_response(self, xml_text):
        """
        Parse ArXiv API response XML
        
        Args:
            xml_text (str): XML response from ArXiv
            
        Returns:
            dict: Parsed information
        """
        if not xml_text:
            return {"total_results": 0, "entries": []}
        
        try:
            # Handle namespace in ArXiv XML
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
            }
            
            root = ET.fromstring(xml_text)
            
            # Parse total results
            total_results = root.find('.//opensearch:totalResults', ns)
            total_results = int(total_results.text) if total_results is not None else 0
            
            # Parse entries
            entries = []
            for entry in root.findall('.//atom:entry', ns):
                parsed_entry = {}
                
                # Get title
                title = entry.find('./atom:title', ns)
                if title is not None:
                    parsed_entry['title'] = title.text
                
                # Get authors
                authors = []
                for author in entry.findall('./atom:author/atom:name', ns):
                    if author.text:
                        authors.append(author.text)
                parsed_entry['authors'] = authors
                
                # Get summary
                summary = entry.find('./atom:summary', ns)
                if summary is not None:
                    parsed_entry['summary'] = summary.text
                
                # Get link (prefer PDF link if available)
                pdf_link = None
                for link in entry.findall('./atom:link', ns):
                    if link.get('title') == 'pdf':
                        pdf_link = link.get('href')
                        break
                
                # If no PDF link, use the main link
                if not pdf_link:
                    link = entry.find('./atom:id', ns)
                    if link is not None:
                        pdf_link = link.text
                
                parsed_entry['link'] = pdf_link
                
                # Get published date
                published = entry.find('./atom:published', ns)
                if published is not None:
                    parsed_entry['published'] = published.text
                
                # Get categories/tags
                categories = []
                for category in entry.findall('./atom:category', ns):
                    term = category.get('term')
                    if term:
                        categories.append(term)
                parsed_entry['categories'] = categories
                
                entries.append(parsed_entry)
            
            return {
                'total_results': total_results,
                'entries': entries
            }
        except Exception as e:
            logger.error(f"Error parsing ArXiv response: {str(e)}")
            return {"total_results": 0, "entries": []}
    
    def _enhance_with_google(self, arxiv_results, query):
        """
        Enhance ArXiv results with Google Search
        
        Args:
            arxiv_results (dict): Parsed ArXiv results
            query (str): Original search query
            
        Returns:
            dict: Enhanced results
        """
        if not self.has_google_search:
            return arxiv_results
        
        try:
            # Get API key and search engine ID from environment variables
            api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
            search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "f60d7c389de5240cd")  # Default from render.yaml
            
            # Construct the API URL with a focus on academic papers
            search_query = f"{query} research paper academic"
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={search_query}"
            
            logger.info(f"Making Google Search API request for: {search_query}")
            
            # Make the request
            response = requests.get(url)
            results = response.json()
            
            # If no Google results, return the original ArXiv results
            if "items" not in results:
                return arxiv_results
            
            # Process Google results to enhance ArXiv entries
            for arxiv_entry in arxiv_results.get("entries", []):
                arxiv_title = arxiv_entry.get("title", "").lower()
                
                # Try to find matching Google result for additional information
                for google_item in results.get("items", []):
                    google_title = google_item.get("title", "").lower()
                    
                    # If titles are similar, enhance with Google data
                    if self._similarity_score(arxiv_title, google_title) > 0.6:
                        arxiv_entry["citation_count"] = self._extract_citation_count(google_item.get("snippet", ""))
                        arxiv_entry["enhanced_link"] = google_item.get("link")
                        break
            
            return arxiv_results
        except Exception as e:
            logger.error(f"Error enhancing with Google: {str(e)}")
            return arxiv_results
    
    def _similarity_score(self, text1, text2):
        """
        Calculate a simple similarity score between two texts
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Simple word overlap similarity
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0
        
        intersection = words1.intersection(words2)
        return len(intersection) / max(len(words1), len(words2))
    
    def _extract_citation_count(self, snippet):
        """
        Extract citation count from Google snippet
        
        Args:
            snippet (str): Google snippet text
            
        Returns:
            int: Extracted citation count or None
        """
        # Try to find citation count in snippet
        match = re.search(r'cited by (\d+)', snippet.lower())
        if match:
            return int(match.group(1))
        return None
    
    def _format_results(self, results, include_abstracts=True):
        """
        Format results for display
        
        Args:
            results (dict): Parsed results
            include_abstracts (bool): Whether to include abstracts
            
        Returns:
            list: Formatted results for display
        """
        formatted_entries = []
        
        for entry in results.get("entries", []):
            # Format authors
            authors = entry.get("authors", [])
            if len(authors) > 3:
                formatted_authors = f"{authors[0]} et al."
            else:
                formatted_authors = ", ".join(authors)
            
            # Format published date
            published = entry.get("published", "")
            if published:
                try:
                    # Convert from ISO format to YYYY-MM-DD
                    published = published[:10]
                except:
                    pass
            
            # Format categories
            categories = entry.get("categories", [])
            formatted_categories = ", ".join(categories[:3])
            if len(categories) > 3:
                formatted_categories += "..."
            
            # Format summary/abstract
            summary = entry.get("summary", "")
            if summary and include_abstracts:
                # Truncate long abstracts
                if len(summary) > 300:
                    summary = summary[:297] + "..."
            else:
                summary = "No abstract available."
            
            # Create formatted entry
            formatted_entry = {
                "title": entry.get("title", "Untitled"),
                "authors": formatted_authors,
                "published": published,
                "categories": formatted_categories,
                "summary": summary,
                "link": entry.get("link", ""),
                "enhanced_link": entry.get("enhanced_link", ""),
                "citation_count": entry.get("citation_count")
            }
            
            formatted_entries.append(formatted_entry)
        
        return formatted_entries

# For testing
if __name__ == "__main__":
    searcher = EnhancedArxivSearch()
    results = searcher.search("quantum computing")
    print(json.dumps(results, indent=2))
