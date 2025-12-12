# CropR 🖼️

Professional headshot batch processor with automatic face detection. Convert full-body or casual photos into polished profile pictures suitable for LinkedIn, GitHub, and other professional platforms.

## Features

- 🤖 **AI-Powered Cropping** - Uses Gemini Vision AI to intelligently detect shoulders and optimize crop
- 🎯 **Smart Shoulder Detection** - Ensures both shoulders are visible in final crop
- 📐 **Multiple Aspect Ratios** - Portrait (600×850), Rounded (600×850), or Circle (600×600)
- 🚀 **Batch Processing** - Process multiple images with preview approval
- ✅ **Preview & Approve** - Review each crop before downloading
- 🔄 **Fallback Mode** - Mathematical center crop when AI is unavailable
- 🌐 **100% Client-Side** - No uploads, all processing in browser
- 💻 **No Backend Required** - Pure HTML/CSS/JS application

## Setup

### Web Interface (Recommended)

1. **Get a Gemini API Key** (Optional but recommended for best results)
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a free API key
   - Click the Settings button in CropR
   - Paste your API key and save

2. **Open `index.html` in your browser**
   - No installation required!
   - Works completely offline (without AI features)
   - AI features require internet connection

### Python CLI (Optional)

For command-line batch processing:

**Prerequisites:**
- Python 3.8 or higher
- pip (Python package manager)

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

This will install:
- `opencv-python` - Face detection
- `Pillow` - Image processing
- `numpy` - Array operations

## Usage

### Web Interface

1. Open `index.html` in your browser
2. (Optional) Configure Gemini API key in Settings for AI-powered cropping
3. Select crop style: Portrait, Rounded, or Circle
4. Choose your images
5. Click "Process images"
6. Preview each crop and approve/reject
7. Approved images download automatically

### Command Line

#### Basic Usage

```bash
# Process a directory with default settings (portrait, 600px)
python crop_headshot.py --input ./photos --output ./headshots

# Process a single image
python crop_headshot.py --input photo.jpg --output headshot.webp
```

#### Advanced Options

```bash
# Square crop at 800px with 90% quality
python crop_headshot.py -i ./photos -o ./output --aspect square --size 800 --quality 90

# Portrait crop with custom size
python crop_headshot.py -i ./photos -o ./headshots -s 1200 -q 95
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--input` | `-i` | Input file or directory (required) | - |
| `--output` | `-o` | Output file or directory (required) | - |
| `--size` | `-s` | Output size in pixels | 600 |
| `--quality` | `-q` | WebP quality (1-100) | 85 |
| `--aspect` | `-a` | Aspect ratio: `portrait`, `square`, or `circle` | portrait |

### Aspect Ratios

#### Portrait (600×850)
- Professional headshot with shoulders
- Suitable for LinkedIn, resumes
- Includes appropriate headroom above face
- Best for: Professional profiles

#### Square (600×600)
- Versatile square crop
- Perfect for most social media
- Tighter crop, face-focused
- Best for: GitHub, Twitter, avatars

#### Circle (600×600)
- Square crop (circular masking can be applied in post)
- Same dimensions as square
- Best for: Profile pictures requiring circular crops

## How It Works

### AI-Powered Processing (Web Interface)

**With Gemini API Key:**
1. Image is analyzed by Gemini Vision AI
2. AI detects person's head and shoulder positions
3. Optimal crop box calculated to include both shoulders
4. Image cropped and resized to target dimensions
5. Preview shown for approval
6. Approved images download automatically

**Without API Key (Fallback Mode):**
1. Mathematical center crop algorithm
2. Preserves aspect ratio
3. Biased toward showing shoulders in portrait mode

### Python CLI Processing

1. Loads image and converts to grayscale
2. Uses OpenCV's Haar Cascade classifier to detect faces
3. Selects the largest face (assumed to be primary subject)
4. Calculates intelligent crop with proper headroom and shoulder space

### Processing Pipeline

**Web Interface:**
```
Input Image → AI Analysis → Boundary Detection → Crop → Resize → Preview → Approve → Download
```

**Python CLI:**
```
Input Image → Face Detection → Calculate Crop → Resize → Save as WebP
```

## Examples

### Batch Processing

```bash
# Process all photos in a folder
python crop_headshot.py \
  --input ~/Pictures/team-photos \
  --output ~/Pictures/headshots \
  --aspect portrait \
  --size 600 \
  --quality 90
```

### Single File Processing

```bash
# Convert a single photo
python crop_headshot.py -i my-photo.jpg -o my-headshot.webp
```

### High Quality Output

```bash
# Maximum quality, larger size
python crop_headshot.py \
  -i ./originals \
  -o ./high-res \
  --size 1200 \
  --quality 98
```

## Output

Processed images are saved with the suffix `_headshot.webp`:

```
Input:  photo.jpg
Output: photo_headshot.webp
```

## Troubleshooting

### No faces detected
- Ensure faces are clearly visible and front-facing
- Try with better-lit photos
- The script will fall back to center crop

### Poor crop quality
- Increase `--quality` parameter (higher = better)
- Use larger `--size` for source material
- Ensure input photos are high resolution

### Installation issues
```bash
# If OpenCV fails to install, try:
pip install opencv-python-headless

# On macOS with M1/M2, you might need:
arch -arm64 pip install opencv-python
```

## Technical Details

- **Face Detection**: Haar Cascade Classifier (OpenCV)
- **Image Processing**: PIL/Pillow
- **Output Format**: WebP (better compression than JPEG/PNG)
- **Resize Algorithm**: Lanczos (high quality)
- **Supported Input**: JPG, PNG, BMP, TIFF, WebP

## File Structure

```
cropR/
├── index.html           # Web interface
├── crop_headshot.py     # Main Python script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── assets/             # SVG icons and graphics
```

## License

MIT License - Free to use for personal and commercial projects.

## Contributing

Contributions welcome! Some ideas:
- Support for additional output formats
- Video frame extraction
- Batch renaming options
- GUI application
- Cloud storage integration

---

**Made with ❤️ for better profile pictures**
