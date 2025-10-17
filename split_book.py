#!/usr/bin/env python3
"""
Document Splitter for "The Researcher"
Splits a book into individual chapters based on "Chapter X" markers
"""

import re
import os
from pathlib import Path

def split_book_by_chapters(input_file, output_folder="book_chapters"):
    """
    Split a book into individual chapter files
    
    Args:
        input_file (str): Path to the full book file
        output_folder (str): Folder to save chapter files
    """
    
    # Create output folder
    Path(output_folder).mkdir(exist_ok=True)
    
    # Read the book file with proper encoding handling
    try:
        # Try different encodings
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
            return False
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Split by chapter markers (Chapter 1, Chapter 2, etc.)
    # This regex looks for "Chapter" followed by a number
    chapter_pattern = r'(Chapter \d+)'
    
    # Debug: Show first 500 characters to see format
    print("First 500 characters of file:")
    try:
        print(content[:500])
    except UnicodeEncodeError:
        print("(Content contains non-printable characters)")
    print("\n" + "="*50)
    
    # Find all chapter markers
    chapter_matches = re.findall(chapter_pattern, content)
    print(f"Found chapter markers: {chapter_matches}")
    
    # Split the content into chapters
    chapters = re.split(chapter_pattern, content)
    
    # Remove empty strings and organize into chapter pairs
    chapters = [ch for ch in chapters if ch.strip()]
    print(f"Split into {len(chapters)} parts")
    
    chapter_count = 0
    
    # Process chapters (title + content pairs)
    for i in range(0, len(chapters), 2):
        if i + 1 < len(chapters):
            chapter_title = chapters[i].strip()
            chapter_content = chapters[i + 1].strip()
            
            # Extract chapter number
            chapter_match = re.search(r'Chapter (\d+)', chapter_title)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                chapter_count += 1
                
                # Create filename
                filename = f"Chapter_{chapter_num.zfill(2)}.txt"
                filepath = Path(output_folder) / filename
                
                # Write chapter file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"{chapter_title}\n\n{chapter_content}")
                
                print(f"Created: {filename}")
    
    print(f"\nSplit complete! Created {chapter_count} chapter files in '{output_folder}' folder.")
    return True

def main():
    """Main function"""
    
    # Look for the book file
    book_file = "Andrew WIP Doc Splits/The Researcher Full.txt"
    
    if not Path(book_file).exists():
        print(f"Book file not found: {book_file}")
        print("Please make sure the file exists and try again.")
        return
    
    print("Splitting 'The Researcher Full.txt' into chapters...")
    print("=" * 50)
    
    success = split_book_by_chapters(book_file)
    
    if success:
        print("\nSuccess! Book successfully split into chapters!")
        print("You can now copy the chapter files to the 'text_input' folder")
        print("and run the batch converter to create audio files.")
    else:
        print("\nError splitting the book.")

if __name__ == "__main__":
    main()
