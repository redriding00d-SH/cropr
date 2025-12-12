# CropR

Professional headshot batch processor with AI-powered face detection.

![CropR Interface](assets/screenshot.png)

## Features

- 🤖 **AI Face Detection** - Automatic face-centered cropping
- 📐 **700×850 Portrait** - Optimized for professional profiles
- 🚀 **Batch Processing** - Preview and approve each crop
- 🆓 **100% Free** - No API keys, runs in browser
- 🔒 **Private** - All processing happens locally

## Quick Start

Open `index.html` in your browser - that's it!

1. Select images
2. Click "Process images"
3. Preview & approve/reject
4. Download results

## Python CLI (Optional)

```bash
pip install -r requirements.txt
python crop_headshot.py --input ./photos --output ./headshots
```

## Technical Details

- **Face Detection**: face-api.js TinyFaceDetector
- **Output**: 700×850 WebP (90% quality)
- **Privacy**: Client-side processing, no uploads

## License

MIT - Free for personal and commercial use

---

**Version 1.1**
