# 🏕️ GPX Waypoint Colorizer for CoMaps / Organic Maps

This Python script provides a simple solution for hikers who use **CoMaps or Organic Maps and need custom, color-coded waypoint markers in their imported GPX files.

When managing complex navigation data like campsites, water sources, and trailheads, generic red pins make map planning difficult. This tool automatically injects the necessary proprietary color data into your existing GPX file based on keywords found in the waypoint name.

## 📌 The Problem: Generic Waypoints

In CoMaps (and other mapping apps that lack advanced GPX styling support), manually imported waypoints often appear as the same generic pin or bubble, regardless of whether they represent a water source, a scenic view, or a parking lot.

To check what a waypoint is, the user must click on it, losing efficiency during route planning.

## ✨ The Solution: Custom Styling Injection

CoMaps supports KML/GPX color codes when they are nested in a specific, non-standard extension format upon import. The script automates this process by:

1.  Reading the waypoint's `<name>` (e.g., "Main Campsite").
2.  Matching the name against a keyword list (e.g., `camp`).
3.  Injecting the proprietary color tag into the waypoint's XML structure:

```xml
<wpt lat="..." lon="...">
  <name>Campsite</name>
  <extensions>
    <xsi:gpx><color>#FF804633</color></xsi:gpx>
  </extensions>
</wpt>
```

This immediately assigns a custom color to the pin when the file is imported into the app.

The images below show the default waypoint view in Comaps vs. the color coded version.

![Comaps colorcoded](images/comaps_color_coded.webp)

## Default Keyword-to-Color Mapping

The following rules are used by the script to assign color codes. You can customize the `COLOR_MAP` dictionary inside the `gpx_colorizer.py` file to suit your preferences.

| Category | Keywords (Case-Insensitive) | Hex Code (ARGB) | Visual Reference |
| :--- | :--- | :--- | :--- |
| **Blue** | `water`, `creek`, `stream`, `fall`, `pool`, `pond`, `lake` | `#FF249CF2` | Water/Falls |
| **Gray** | `trailhead`, `parking` | `#FF737373` | Trailhead/Infrastructure |
| **Brown** | `camp` | `#FF804633` | Campsites/Primitive Site |
| **Green** | `viewpoint`, `peak` | `#FF3C8C3C` | Scenic Area/Attraction |
| **Yellow** | `ranger`, `office`, `restroom` | `#FFFFC800` | Administrative/Facilities |

## 🚀 How to Use the Script

### Prerequisites

You need a standard Python installation (`3.x`) on your desktop environment. The script uses the built-in `xml.etree.ElementTree`, `glob`, and `tkinter` libraries.

### Running the Tool

1.  **Save the Script:** Save the `gpx_colorizer.py` file (provided previously) to a convenient location (e.g., a "Scripts" folder).

2.  **Execute:** Run the script from your terminal:

    ```bash
    python gpx_colorizer.py
    ```

3.  **Select File:** A standard graphical file dialog will pop up, allowing you to easily browse and select your GPX file (e.g., `MyRoutes.gpx`).

4.  **Output:** The script will process the file and save a new version named: `MyRoutes_color.gpx`.

### Safety and Disclaimer

> **WARNING:** Use this script with caution. This tool modifies the XML structure of GPX files using proprietary tags recognized by applications like OsmAnd/CoMaps.
>
>   * **The original GPX file is NOT modified.** A new file ending in `_color.gpx` is always created.
>   * Always verify the output file in your mapping application before relying on it.

## 📤 Final Step: Import to CoMaps / OsmAnd

Once the script has finished:

1.  Take the new file (`yourfile_color.gpx`).
2.  Import this file into **CoMaps or OsmAnd**.
3.  The waypoints whose names contained a keyword (e.g., 'camp', 'pool') will now display with their assigned custom color.
