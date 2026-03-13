import PyPDF2
import sys
from pathlib import Path

def search_text_in_pdf(pdf_path, text_list):
    """
    Search for text strings in a PDF file and return the page numbers where they are found.
    
    Args:
        pdf_path (str): Path to the PDF file
        text_list (list): List of text strings to search for
    
    Returns:
        dict: Dictionary with text as key and page number (or "not found") as value
    """
    results = {}
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            
            print(f"Searching through {num_pages} pages...\n")
            
            for text in text_list:
                found = False
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if text in page_text:
                        results[text] = f"page {page_num + 1}"
                        found = True
                        break
                
                if not found:
                    results[text] = "not found"
        
        return results
    
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def display_results(results):
    """
    Display the search results in a formatted way.
    
    Args:
        results (dict): Dictionary containing search results
    """
    if results:
        print("Search Results:")
        print("-" * 40)
        for text, location in results.items():
            print(f"{text} - {location}")
        print("-" * 40)

def main():
    """Main function to run the PDF text searcher."""
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python pdf_text_searcher.py <pdf_file> <text_list_file>")
        print("\nExample:")
        print("  python pdf_text_searcher.py document.pdf search_terms.txt")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    text_file = sys.argv[2]
    
    # Read text list from file
    try:
        with open(text_file, 'r') as f:
            text_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Text file '{text_file}' not found.")
        sys.exit(1)
    
    if not text_list:
        print("Error: No text strings found in the text file.")
        sys.exit(1)
    
    print(f"PDF File: {pdf_path}")
    print(f"Search Terms: {len(text_list)} terms\n")
    
    # Search for text in PDF
    results = search_text_in_pdf(pdf_path, text_list)
    
    if results:
        display_results(results)

if __name__ == "__main__":
    main()