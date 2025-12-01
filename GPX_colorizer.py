#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25, 2025

https://github.com/firatsoylu/Comaps_Colorizer

"""
import xml.etree.ElementTree as ET
import glob
import os
from typing import Dict, List, Optional
import tkinter as tk
from tkinter import filedialog 

# --- Configuration ---
COLOR_MAP: Dict[str, str] = {
    # Key: Keyword to search for (case-insensitive, partial word)
    # Value: ARGB Hex Code (OsmAnd/KML format)
    'camp': '#FF804633',        # Brown
    'water': '#FF249CF2',       # Blue
    'creek': '#FF249CF2',       # Blue
    'stream': '#FF249CF2',      # Blue
    'pond': '#FF249CF2',        # Blue
    'pool': '#FF249CF2',        # Blue
    'lake': '#FF249CF2',        # Blue
    'fall': '#FF249CF2',        # Blue
    'trailhead': '#FF737373',   # Gray
    'parking': '#FF737373',     # Gray
    'viewpoint': '#FF3C8C3C',   # Green
    'peak': '#FF3C8C3C',        # Green
    'ranger': '#FFFFC800',      # Yellow
    'office': '#FFFFC800',      # Yellow
    'restroom': '#FFFFC800',    # Yellow
    # Note: Orange (#FFFF9600) and Purple (#FF9B24B2) color codes can also be used for
    # more categories
}

# --- XML Namespace Setup ---
# The default GPX namespace
ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')
# The custom namespace for the color extension
GPX_NS = {'gpx': 'http://www.topografix.com/GPX/1/1'}
XSI_GPX_COLOR_NS = 'http://www.topografix.com/GPX/1/1' # For the xsi:gpx tag

# --- Helper Functions ---

def select_file_from_dialog(directory: str = '.') -> Optional[str]:
    """
    Opens a standard graphical file selection dialog box.
    """
    # Initialize tkinter root window (must be done before calling dialog)
    # We withdraw it so the root window doesn't pop up unnecessarily.
    root = tk.Tk()
    root.withdraw() 
    
    # Calculate the starting directory (parent of script location)
    initial_dir = os.path.abspath(os.path.join(directory, '..'))
    
    print("Opening file selection dialog...")
    
    # Open the file selection dialog
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="Select GPX File to Process",
        filetypes=(("GPX files", "*.gpx"), ("All files", "*.*"))
    )
    
    # Destroy the root window after use
    root.destroy()

    if file_path:
        return file_path
    else:
        return None

def get_waypoint_color(name: str) -> Optional[str]:
    """Determines the color code based on keywords in the waypoint name."""
    name_lower = name.lower()
    for keyword, color_code in COLOR_MAP.items():
        # Check if the keyword is a substring of the waypoint name
        if keyword in name_lower:
            return color_code
    return None

def process_gpx_file(file_path: str):
    """Parses the GPX file, colors waypoints, and saves the changes to a new file."""
    print(f"\nProcessing file: {file_path}")
    
    try:
        # Load the file
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return

    waypoints_processed = 0
    
    # Iterate through all waypoints (<wpt>) in the GPX file
    for wpt in root.findall('gpx:wpt', GPX_NS):
        # ... (rest of the logic remains the same for coloring) ...
        name_element = wpt.find('gpx:name', GPX_NS)
        
        if name_element is None or name_element.text is None:
            name = "[Unnamed Waypoint]"
            color_code = None
        else:
            name = name_element.text
            color_code = get_waypoint_color(name)
        
        # If a color is found, add the required extension block
        if color_code:
            
            # 1. Create <extensions> tag
            extensions = wpt.find('gpx:extensions', GPX_NS)
            if extensions is None:
                extensions = ET.SubElement(wpt, 'extensions')
            
            # 2. Create <xsi:gpx> tag inside <extensions>
            xsi_gpx = ET.Element(f'{{{XSI_GPX_COLOR_NS}}}gpx')
    
            extensions.append(xsi_gpx)
            
            # 3. Create <color> tag inside <xsi:gpx>
            color = ET.SubElement(xsi_gpx, 'color')
            color.text = color_code
            
            print(f" -> Found keyword, colored '{name}' with {color_code} (Success)")
            waypoints_processed += 1
        # else:
            # print(f" -> No color keyword found for '{name}'")


    if waypoints_processed > 0:
        # --- NEW FILE NAMING LOGIC ---
        base, ext = os.path.splitext(file_path)
        output_path = base + "_color" + ext
        # -----------------------------
        
        # Write the modified tree to the NEW file path
        # No need for backup or renaming steps since we are writing to a new file
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"\nSuccessfully added color to {waypoints_processed} waypoints.")
        print(f"New colored file saved as: {output_path}")
    else:
        # Write the tree to the output path even if no waypoints were colored
        # to ensure a copy with the original content.
        base, ext = os.path.splitext(file_path)
        output_path = base + "_color" + ext
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"No waypoints were modified based on the keyword list.")
        print(f"Original file copied to: {output_path}")


if __name__ == "__main__":
    # Get the directory where the script is run
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
    
    # Select the file using the new GUI dialog
    selected_file = select_file_from_dialog(script_dir)
    
    if selected_file:
        process_gpx_file(selected_file)
    else:
        print("Script cancelled or file not selected.")