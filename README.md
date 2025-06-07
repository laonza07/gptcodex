# gptcodex

This repository contains a simple color verification utility for comparing two pattern images.

## Usage

1. Prepare two images in the ASCII `P3` PPM format with the same width and height.
2. Run the verifier:

```bash
python3 color_verification.py reference.ppm comparison.ppm --threshold 5.0
```

The script computes the mean color distance between the images. If the value is below the threshold, the patterns are considered a match.
