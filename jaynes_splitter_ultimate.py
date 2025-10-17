#!/usr/bin/env python3
"""
Julian Jaynes Book Splitter - ULTIMATE FINAL VERSION
Splits "The Origin of Consciousness in the Breakdown of the Bicameral Mind"
using the ACTUAL content sections, not Table of Contents titles
"""

import re
from pathlib import Path
import sys

def split_jaynes_book_ultimate(input_file: Path, output_folder: str = "jaynes_chapters_ultimate") -> bool:
    """
    Splits Julian Jaynes book using the actual content sections
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
    
    # Define the EXACT order from Table of Contents
    toc_order = [
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
    
    print(f"\nLooking for ACTUAL content sections ({len(toc_order)} sections)...")
    
    # Split content into lines for easier processing
    lines = content.split('\n')
    
    # Find the actual section markers in the content (skip TOC, find real content)
    section_positions = {}
    
    # Skip the first 100 lines (TOC area) and look for actual content
    for i, line in enumerate(lines[100:], 100):
        line_stripped = line.strip()
        if line_stripped in toc_order:
            # Check if this is a standalone line (not part of a paragraph)
            is_standalone = True
            if i > 0 and lines[i-1].strip():  # Previous line not empty
                is_standalone = False
            if i < len(lines)-1 and lines[i+1].strip():  # Next line not empty
                is_standalone = False
            
            if is_standalone:
                # Only keep the first occurrence of each section
                if line_stripped not in section_positions:
                    section_positions[line_stripped] = i
                    print(f"Found content section: '{line_stripped}' at line {i}")
    
    print(f"\nFound {len(section_positions)} actual content sections")
    
    # Create chapter files in TOC order
    chapter_count = 0
    
    for section_title in toc_order:
        if section_title not in section_positions:
            print(f"WARNING: '{section_title}' not found in content!")
            continue
        
        start_line = section_positions[section_title]
        
        # Find the next section to determine end position
        next_start_line = len(lines)  # Default to end of document
        
        for next_title in toc_order:
            if next_title in section_positions and section_positions[next_title] > start_line:
                next_start_line = section_positions[next_title]
                break
        
        # Extract section content
        section_lines = lines[start_line:next_start_line]
        section_content = '\n'.join(section_lines).strip()
        
        # Skip if content is too short (just the title)
        if len(section_content.split()) < 50:
            print(f"Skipping '{section_title}' - too short ({len(section_content.split())} words)")
            continue
        
        # Create filename
        safe_title = re.sub(r'[^\w\s-]', '', section_title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f"{output_folder}/{chapter_count + 1:02d}_{safe_title}.txt"
        
        # Write section to file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(section_content)
            
            word_count = len(section_content.split())
            print(f"Created: {Path(filename).name} ({word_count:,} words)")
            chapter_count += 1
        except Exception as e:
            print(f"Error writing section file {filename}: {e}")
            return False
    
    print(f"\nSplit complete! Created {chapter_count} section files in '{output_folder}' folder.")
    print("Files are now in the CORRECT Table of Contents order!")
    return True

def main():
    """Main function"""
    
    print("Julian Jaynes Book Splitter - ULTIMATE FINAL")
    print("="*50)
    
    input_file = Path("Caitlin WIP Doc Splits/The Origin of Consciousness in - Julian Jaynes.txt")
    
    if not input_file.exists():
        print(f"File not found: {input_file}")
        return False
    
    print(f"Splitting '{input_file.name}' into sections...")
    print("Using ACTUAL content sections, not TOC titles...")
    print("="*50)
    
    success = split_jaynes_book_ultimate(input_file)
    
    if success:
        print("\nSuccess! Book successfully split into sections!")
        print("Files are now in the CORRECT order!")
        print("You can now copy the section files to the 'text_input' folder")
        print("and run the batch converter to create audio files.")
    else:
        print("\nError splitting the book.")
    
    return success

if __name__ == "__main__":
    main()
