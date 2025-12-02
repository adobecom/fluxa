# Fluxa Quick Start Guide

Get started with Fluxa in 5 minutes! 🚀

## Step 1: Install

```bash
cd Fluxa
bash setup.sh
```

Or manually:
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Step 2: Configure API Key

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

Or add to `.env` file:
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

## Step 3: Run Your First Conversion

### From YouTube Tutorial:
```bash
fluxa https://www.youtube.com/watch?v=VIDEO_ID -o my-actions.json
```

### From Web Article:
```bash
fluxa https://example.com/photoshop-tutorial -o my-actions.json
```

## Step 4: Check the Output

```bash
cat my-actions.json
```

You should see Photoshop API JSON actions! 🎉

## Common Use Cases

### Preview Cost Before Running
```bash
fluxa URL --estimate-cost
```

### Verbose Output
```bash
fluxa URL -v -o output.json
```

### Without Metadata Wrapper
```bash
fluxa URL --no-metadata -o clean.json
```

## Tips

1. **YouTube videos must have captions** - Check that the video has subtitles enabled
2. **Web tutorials work best with clear steps** - Numbered lists and bullet points
3. **Use `--estimate-cost`** to check API costs before processing
4. **Start with short tutorials** to test and understand the output format
5. **API Context** - Generated actions exclude file operations (`open`/`save`) since they're designed for API use where documents are already loaded

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/](examples/) for sample outputs
- See [CONTRIBUTING.md](CONTRIBUTING.md) to extend functionality

## Troubleshooting

**"OpenAI API key not found"**
→ Export the key: `export OPENAI_API_KEY='your-key'`

**"No transcript found"**
→ Use a video with captions or try a web article instead

**"Invalid JSON"**
→ The AI couldn't parse the tutorial. Try a clearer, step-by-step tutorial

## Support

Open an issue or check the main README for more help!


