# CropR 🖼️

Professional headshot batch processor with automatic face detection. Convert full-body or casual photos into polished profile pictures suitable for LinkedIn, GitHub, and other professional platforms.

## Features

- 🤖 **AI-Powered Face Detection** - Uses face-api.js TinyFaceDetector for intelligent cropping
- 🎯 **Smart Cover-Style Cropping** - Automatically centers on detected faces
- 📐 **Professional Portrait Output** - 700×850 optimized dimensions
- 🚀 **Batch Processing** - Process multiple images with preview approval
- ✅ **Preview & Approve** - Review each crop before downloading
- 🔄 **Fallback Mode** - Center crop when face detection unavailable
- 🌐 **100% Client-Side** - No uploads, all processing in browser
- 💻 **No Backend Required** - Pure HTML/CSS/JS application
- 🆓 **Completely Free** - No API keys needed, all libraries from CDN

## Quick Start

### Web Interface (Recommended)

Simply open `index.html` in your browser - that's it!

- No installation required
- No API keys needed
- Works offline (face detection requires internet for first load)
- All processing happens locally in your browser

### Python CLI (Optional)

For command-line batch processing:

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Basic Usage:**
```bash
# Process a directory
python crop_headshot.py --input ./photos --output ./headshots

# Process a single image
python crop_headshot.py --input photo.jpg --output headshot.webp
```

## Usage

### Web Interface

1. Open `index.html` in your browser
2. Click "Select files to upload"
3. Choose your images
4. Click "Process images"
5. Preview each crop and approve/reject
6. Approved images download automatically as JPEG files

### Command Line

#### Advanced Options

```bash
# Square crop at 800px with 90% quality
python crop_headshot.py -i ./photos -o ./output --aspect square --size 800 --quality 90

# Portrait crop with custom size
python crop_headshot.py -i ./photos -o ./headshots -s 1200 -q 95
```

#### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--input` | `-i` | Input file or directory (required) | - |
| `--output` | `-o` | Output file or directory (required) | - |
| `--size` | `-s` | Output size in pixels | 600 |
| `--quality` | `-q` | WebP quality (1-100) | 85 |
| `--aspect` | `-a` | Aspect ratio: `portrait`, `square`, or `circle` | portrait |

## How It Works

### Web Interface Processing

**With Face Detection (Automatic):**
1. face-api.js TinyFaceDetector analyzes image
2. Detects face position and calculates optimal crop
3. Cover-style crop centers on face (like Photoshop)
4. Resizes to 700×850 professional portrait
5. Shows preview for approval
6. Downloads as JPEG on approval

**Fallback (No Face Detected):**
1. Uses mathematical center crop (90% width)
2. Maintains 700×850 aspect ratio
3. Positions crop at top of image

### Python CLI Processing

1. Loads image and converts to grayscale
2. Uses OpenCV's Haar Cascade classifier to detect faces
3. Selects the largest face (primary subject)
4. Calculates intelligent crop with headroom and shoulder space
5. Saves as WebP format

### Processing Pipeline

**Web Interface:**
```
Input Image → Face Detection → Cover Crop → Resize → Preview → Approve → Download
```

**Python CLI:**
```
Input Image → Face Detection → Calculate Crop → Resize → Save as WebP
```

## Output

### Web Interface
- Format: JPEG (90% quality)
- Dimensions: 700×850 pixels
- Naming: `{filename}_portrait.jpg`

### Python CLI
- Format: WebP
- Dimensions: Configurable (default 600×850)
- Naming: `{filename}_headshot.webp`

## Technical Details

### Web Interface
- **Face Detection**: face-api.js TinyFaceDetector (TensorFlow.js)
- **Processing**: HTML5 Canvas API
- **Libraries**: Loaded from CDN (no installation)
- **Privacy**: 100% client-side, no data leaves your browser

### Python CLI
- **Face Detection**: OpenCV Haar Cascade Classifier
- **Image Processing**: PIL/Pillow
- **Output Format**: WebP (better compression than JPEG/PNG)
- **Resize Algorithm**: Lanczos (high quality)
- **Supported Input**: JPG, PNG, BMP, TIFF, WebP

## Troubleshooting

### Web Interface

**Face detection not working:**
- Ensure you have internet connection (first load only)
- Check browser console for errors
- Try a different photo with clear frontal face

**Poor crop results:**
- Use high-resolution source images
- Ensure faces are front-facing and well-lit
- Subject should be clearly visible

### Python CLI

**No faces detected:**
- Ensure faces are clearly visible and front-facing
- Try with better-lit photos
- Script will fall back to center crop

**Installation issues:**
```bash
# If OpenCV fails to install, try:
pip install opencv-python-headless

# On macOS with M1/M2:
arch -arm64 pip install opencv-python
```

## File Structure

```
cropR/
├── index.html           # Web interface (main app)
├── crop_headshot.py     # Python CLI tool
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── assets/             # Logo and graphics
    └── logos.png
```

## Browser Compatibility

- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Older browsers may not support face-api.js

## License

MIT License - Free to use for personal and commercial projects.

## Contributing

Contributions welcome! Some ideas:
- Additional crop aspect ratios
- Batch download as ZIP
- Adjustable crop positioning
- Custom output dimensions
- Background removal integration

---

**Made with ❤️ for better profile pictures**

**Version 1.1**
