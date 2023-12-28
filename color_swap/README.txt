Tool to make it easy to do palette swaps for images.  Load an image from a
file (PNG); make changes, and save back to a file.

--------

GUI DESIGN:
  IMAGES
    - Top left: original
        - Zoomable with scroll wheel
    - Top middle: edited
        - Zoomable with scroll wheel (independent of left)
    - Top right: bitmask, showing pixels used by current color

  COLORS
    - Rows along the bottom, sorted from most abundant (top) to least
    - Left side: original colors
    - Middle: new colors
    - Right: color picker or wheel

