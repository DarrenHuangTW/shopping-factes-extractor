# 🚀 Quick Start Guide

## Get Started in 3 Steps

### 1. Install Dependencies
```bash
uv sync
```

### 2. Run the Streamlit App
```bash
uv run streamlit run streamlit_app.py
```

### 3. Open Your Browser
Navigate to: `http://localhost:8501`

## First Time Setup

1. **Get SerpAPI Key**: Sign up at [serpapi.com](https://serpapi.com/) for a free API key
2. **Enter API Key**: Paste your key in the sidebar (it's password-protected)
3. **Test with Keywords**: Try these sample keywords:
   ```
   running shoes
   winter jackets
   coffee maker
   ```

## What You'll Get

- **Real-time Progress**: Watch as each keyword is processed
- **Consolidated Results**: Single CSV with all refine filters
- **Error Handling**: Continues even if some searches fail
- **Easy Download**: One-click CSV download

## Sample Output

Your CSV will look like this:
```csv
Keyword,Type,Title
running shoes,Brand,Nike
running shoes,Color,Black
winter jackets,Size,Large
coffee maker,Features,Programmable
```

## Need Help?

- Check [`README_STREAMLIT.md`](README_STREAMLIT.md) for detailed documentation
- Run `uv run test_app.py` to verify everything works
- Original CLI script still available as [`main.py`](main.py)

---
**Ready to extract shopping facets! 🔍✨**