#!/usr/bin/env python3
"""
Smart Document Analyzer and Splitter
Handles messy PDFs and detects chapters automatically
"""

import re
import os
from pathlib import Path
from collections import Counter

def analyze_document_structure(input_file):
    """
    Analyze a document to find chapter patterns and structure
    """
    
    # Read the file
    try:
        encodings = ['utf-8-sig', 'utf-8', 'cp1252', 'latin1']
        content = None
        
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"Successfully read file with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("Could not read file with any supported encoding")
            return None
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    print(f"Document size: {len(content):,} characters")
    print(f"Document size: {len(content.split()):,} words")
    
    # Look for various chapter patterns
    chapter_patterns = [
        r'Chapter\s+\d+',           # Chapter 1, Chapter 2, etc.
        r'CHAPTER\s+\d+',          # CHAPTER 1, CHAPTER 2, etc.
        r'Chapter\s+[IVX]+',       # Chapter I, Chapter II, etc.
        r'CHAPTER\s+[IVX]+',      # CHAPTER I, CHAPTER II, etc.
        r'Part\s+\d+',            # Part 1, Part 2, etc.
        r'PART\s+\d+',            # PART 1, PART 2, etc.
        r'Book\s+\d+',            # Book 1, Book 2, etc.
        r'BOOK\s+\d+',            # BOOK 1, BOOK 2, etc.
        r'Section\s+\d+',         # Section 1, Section 2, etc.
        r'SECTION\s+\d+',         # SECTION 1, SECTION 2, etc.
    ]
    
    print("\n" + "="*60)
    print("ANALYZING DOCUMENT STRUCTURE")
    print("="*60)
    
    all_matches = []
    for pattern in chapter_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"Found pattern '{pattern}': {len(matches)} matches")
            print(f"  Examples: {matches[:5]}")
            all_matches.extend(matches)
    
    if not all_matches:
        print("No clear chapter patterns found. Looking for other indicators...")
        
        # Look for page breaks or other indicators
        page_breaks = content.count('\f')  # Form feed characters
        double_newlines = content.count('\n\n\n')
        
        print(f"Page breaks (\\f): {page_breaks}")
        print(f"Triple newlines: {double_newlines}")
        
        # Look for common book patterns
        common_patterns = [
            r'\n\s*\d+\s*\n',      # Numbers on their own line
            r'\n\s*[A-Z][A-Z\s]+\n',  # All caps headers
            r'\n\s*[A-Z][a-z]+\s+[A-Z][a-z]+\n',  # Title case headers
        ]
        
        for pattern in common_patterns:
            matches = re.findall(pattern, content)
            if len(matches) > 5:  # Only if we find several
                print(f"Found potential headers with pattern '{pattern}': {len(matches)} matches")
                print(f"  Examples: {matches[:3]}")
    
    return content, all_matches

def smart_split_document(content, output_folder="smart_chapters"):
    """
    Intelligently split document into chapters
    """
    
    # Create output folder
    Path(output_folder).mkdir(exist_ok=True)
    
    print("\n" + "="*60)
    print("SMART SPLITTING OPTIONS")
    print("="*60)
    
    # Try different splitting strategies
    strategies = []
    
    # Strategy 1: Standard chapter patterns
    chapter_patterns = [
        r'(Chapter\s+\d+)',
        r'(CHAPTER\s+\d+)',
        r'(Chapter\s+[IVX]+)',
        r'(CHAPTER\s+[IVX]+)',
        r'(Part\s+\d+)',
        r'(PART\s+\d+)',
    ]
    
    for pattern in chapter_patterns:
        chapters = re.split(pattern, content)
        chapters = [ch for ch in chapters if ch.strip()]
        
        if len(chapters) > 2:  # More than just title and content
            strategies.append(("Chapter Pattern", pattern, chapters))
            print(f"Strategy: Chapter Pattern '{pattern}' - Found {len(chapters)//2} chapters")
    
    # Strategy 2: Page-based splitting (if document is very long)
    if len(content) > 100000:  # More than 100k characters
        # Split by approximate page length (assuming 2000 chars per page)
        page_size = 2000
        pages = [content[i:i+page_size] for i in range(0, len(content), page_size)]
        strategies.append(("Page-based", f"{page_size} chars", pages))
        print(f"Strategy: Page-based - Would create {len(pages)} files")
    
    # Strategy 3: Paragraph-based splitting (for very long documents)
    if len(content) > 200000:  # More than 200k characters
        paragraphs = content.split('\n\n')
        # Group paragraphs into chunks of ~10 paragraphs
        chunk_size = 10
        chunks = []
        for i in range(0, len(paragraphs), chunk_size):
            chunk = '\n\n'.join(paragraphs[i:i+chunk_size])
            chunks.append(chunk)
        strategies.append(("Paragraph-based", f"{chunk_size} paragraphs", chunks))
        print(f"Strategy: Paragraph-based - Would create {len(chunks)} files")
    
    # Choose the best strategy
    if not strategies:
        print("No suitable splitting strategy found!")
        return False
    
    # Prefer chapter-based splitting
    best_strategy = strategies[0]
    for strategy in strategies:
        if "Chapter" in strategy[0]:
            best_strategy = strategy
            break
    
    print(f"\nUsing strategy: {best_strategy[0]}")
    
    # Execute the splitting
    if best_strategy[0] == "Chapter Pattern":
        chapters = best_strategy[2]
        chapter_count = 0
        
        for i in range(0, len(chapters), 2):
            if i + 1 < len(chapters):
                chapter_title = chapters[i].strip()
                chapter_content = chapters[i + 1].strip()
                
                # Extract chapter number
                chapter_match = re.search(r'(\d+)', chapter_title)
                if chapter_match:
                    chapter_num = chapter_match.group(1)
                    chapter_count += 1
                    
                    filename = f"Chapter_{chapter_num.zfill(2)}.txt"
                    filepath = Path(output_folder) / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"{chapter_title}\n\n{chapter_content}")
                    
                    print(f"Created: {filename}")
    
    else:
        # Handle other strategies
        items = best_strategy[2]
        for i, item in enumerate(items, 1):
            filename = f"Part_{i:02d}.txt"
            filepath = Path(output_folder) / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(item.strip())
            
            print(f"Created: {filename}")
    
    print(f"\nSplit complete! Created files in '{output_folder}' folder.")
    return True

def main():
    """Main function"""
    
    print("Smart Document Analyzer and Splitter")
    print("="*50)
    
    # Look for the Julian Jaynes book
    input_file = "Caitlin WIP Doc Splits/The Origin of Consciousness in - Julian Jaynes.txt"
    
    if not Path(input_file).exists():
        print(f"File not found: {input_file}")
        print("Looking for other text files...")
        
        # Look for any text files in the current directory
        text_files = list(Path(".").glob("**/*.txt"))
        if text_files:
            print("Found text files:")
            for i, file in enumerate(text_files, 1):
                print(f"{i}. {file}")
            return
        else:
            print("No text files found.")
            return
    
    # Analyze the document
    result = analyze_document_structure(input_file)
    if not result:
        return
    
    content, matches = result
    
    # Auto-analyze and show preview
    print("\n" + "="*60)
    print("DOCUMENT PREVIEW")
    print("="*60)
    print("First 1000 characters:")
    print("-" * 40)
    try:
        print(content[:1000])
    except UnicodeEncodeError:
        print("(Content contains non-printable characters)")
    print("-" * 40)
    
    # Auto-split using best detected method
    print("\n" + "="*60)
    print("AUTO-SPLITTING DOCUMENT")
    print("="*60)
    smart_split_document(content)

if __name__ == "__main__":
    main()
