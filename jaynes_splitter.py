#!/usr/bin/env python3
"""
Julian Jaynes Book Splitter
Splits "The Origin of Consciousness in the Breakdown of the Bicameral Mind"
using the actual section titles from the Table of Contents
"""

import re
from pathlib import Path
import sys

def split_jaynes_book(input_file: Path, output_folder: str = "jaynes_chapters") -> bool:
    """
    Splits Julian Jaynes book using the actual section titles
    """
    
    # Create output folder
    Path(output_folder).mkdir(exist_ok=True)
    
    # Read the book file
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
            return False
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    print(f"Document size: {len(content):,} characters")
    print(f"Document size: {len(content.split()):,} words")
    
    # Define the actual section titles in order (from Table of Contents)
    section_titles = [
        "Preface",
        "Introduction", 
        "The Consciousness of Consciousness",
        "Consciousness",
        "The Mind of Iliad", 
        "The Bicameral Mind",
        "The Double Brain",
        "The Origin of Civilization",
        "Gods, Graves, and Idols",
        "Literate Bicameral Theocracies", 
        "The Causes of Consciousness",
        "A Change of Mind in Mesopotamia",
        "The Intellectual Consciousness of Greece",
        "The Moral Consciousness of the Khabiru",
        "The Quest for Authorization",
        "Of Prophets and Possession",
        "Of Poetry and Music",
        "Hypnosis",
        "Schizophrenia", 
        "The Auguries of Science",
        "Afterword"
    ]
    
    print(f"\nLooking for {len(section_titles)} sections...")
    
    # Find all section markers
    found_sections = []
    for title in section_titles:
        # Look for the title as a standalone line
        pattern = f"^{re.escape(title)}$"
        matches = list(re.finditer(pattern, content, re.MULTILINE))
        if matches:
            found_sections.append((title, matches[0].start()))
            print(f"Found: {title}")
        else:
            print(f"NOT FOUND: {title}")
    
    print(f"\nFound {len(found_sections)} sections out of {len(section_titles)} expected")
    
    if len(found_sections) < 5:
        print("Not enough sections found. This might not be the right splitting method.")
        return False
    
    # Sort by position in document
    found_sections.sort(key=lambda x: x[1])
    
    # Create chapter files
    chapter_count = 0
    
    for i, (title, start_pos) in enumerate(found_sections):
        # Determine end position (start of next section or end of document)
        if i + 1 < len(found_sections):
            end_pos = found_sections[i + 1][1]
        else:
            end_pos = len(content)
        
        # Extract section content
        section_content = content[start_pos:end_pos].strip()
        
        # Create filename
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f"{output_folder}/{chapter_count + 1:02d}_{safe_title}.txt"
        
        # Write section to file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(section_content)
            print(f"Created: {Path(filename).name}")
            chapter_count += 1
        except Exception as e:
            print(f"Error writing section file {filename}: {e}")
            return False
    
    print(f"\nSplit complete! Created {chapter_count} section files in '{output_folder}' folder.")
    return True

def main():
    """Main function"""
    
    print("Julian Jaynes Book Splitter")
    print("="*50)
    
    input_file = Path("Caitlin WIP Doc Splits/The Origin of Consciousness in - Julian Jaynes.txt")
    
    if not input_file.exists():
        print(f"File not found: {input_file}")
        return False
    
    print(f"Splitting '{input_file.name}' into sections...")
    print("="*50)
    
    success = split_jaynes_book(input_file)
    
    if success:
        print("\nSuccess! Book successfully split into sections!")
        print("You can now copy the section files to the 'text_input' folder")
        print("and run the batch converter to create audio files.")
    else:
        print("\nError splitting the book.")
    
    return success

if __name__ == "__main__":
    main()
