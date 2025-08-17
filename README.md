# Shopping Facets Extractor - Streamlit Web App

A user-friendly web interface for extracting Google Shopping refine filters using SerpAPI.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+** (check with `python --version`)
2. **SerpAPI Account** - Get your free API key at [serpapi.com](https://serpapi.com/)

### Installation

1. **Install dependencies:**
   ```bash
   # If using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open your browser** to `http://localhost:8501`

## 📋 How to Use

### Step 1: Configuration
- Enter your **SerpAPI key** in the sidebar (required)
- Select your preferred **country** (default: United States)
- Choose your **language** (default: English)

### Step 2: Enter Keywords
- Add keywords in the main text area (one per line)
- Maximum 30 keywords allowed
- Real-time keyword counter shows your progress

### Step 3: Run Extraction
- Click **"🔍 Run Extraction"** button
- Watch the progress bar as each keyword is processed
- View real-time status updates

### Step 4: Review Results
- Review the summary statistics
- Preview the extracted data
- Check search metadata (status, timing, raw HTML files)
- Download the consolidated CSV file

## 📊 Output Format

The generated CSV file contains three columns:

| Column | Description | Example |
|--------|-------------|---------|
| `Keyword` | Your search term | "running shoes" |
| `Type` | Filter category | "Brand", "Color", "Size" |
| `Title` | Filter option | "Nike", "Black", "Size 10" |

## 🔧 Features

### ✅ User Interface
- **Responsive design** with sidebar configuration
- **Real-time validation** and keyword counting
- **Progress tracking** with status updates
- **Error handling** with clear messages

### ✅ Processing
- **Batch processing** of multiple keywords
- **Error resilience** - continues even if some searches fail
- **Consolidated output** - single CSV with all results
- **Search metadata tracking** - status, timing, and raw HTML file links
- **Session persistence** - results remain until page refresh

### ✅ Configuration Options
- **API Key** - Your SerpAPI key (required)
- **Country (gl)** - 10 popular countries supported
- **Language (hl)** - 10 major languages supported

## 🛠️ Technical Details

### File Structure
```
├── streamlit_app.py      # Main Streamlit application
├── search_utils.py       # Core search functionality
├── main.py              # Original CLI script (still functional)
├── pyproject.toml       # Dependencies and project config
└── README_STREAMLIT.md  # This documentation
```

### Key Functions
- `validate_keywords()` - Input validation and cleaning
- `process_keywords_batch()` - Batch processing with progress tracking
- `extract_refine_filters()` - Parse SerpAPI response data
- `save_consolidated_csv()` - Generate downloadable CSV

## 🔍 Troubleshooting

### Common Issues

**"API Key required" error:**
- Make sure you've entered your SerpAPI key in the sidebar
- Verify your key is valid at [serpapi.com/dashboard](https://serpapi.com/dashboard)

**"Too many keywords" error:**
- Limit your input to 30 keywords maximum
- Remove empty lines from your keyword list

**Some keywords failed:**
- This is normal - some searches may not have refine filters
- Check the "Failed" section to see which keywords didn't work
- Failed keywords are often too generic or have no shopping results

**No results found:**
- Try more specific, shopping-related keywords
- Ensure your keywords would return shopping results on Google
- Consider changing the country/language settings

### Performance Tips
- **Smaller batches** process faster (10-15 keywords recommended)
- **Specific keywords** yield better results than generic terms
- **Shopping-related terms** work best (products, brands, categories)

## 🆚 CLI vs Web App

| Feature | CLI (`main.py`) | Web App (`streamlit_app.py`) |
|---------|-----------------|------------------------------|
| Interface | Command line | Web browser |
| Keywords | Single keyword | Up to 30 keywords |
| Progress | Text output | Visual progress bar |
| Output | Individual CSV files | Consolidated CSV |
| Configuration | Environment variables | Interactive UI |
| Error handling | Console messages | User-friendly alerts |

## 🔄 Extending the App

The application is designed to be easily extensible:

### Adding More SerpAPI Parameters
Edit `search_utils.py` and `streamlit_app.py` to add new parameters:

```python
# In search_utils.py - perform_search function
params = {
    "engine": "google",
    "q": query,
    "api_key": api_key,
    "gl": gl,
    "hl": hl,
    "safe": safe,  # Add new parameter
    # ... other parameters
}

# In streamlit_app.py - add UI controls
safe_search = st.sidebar.selectbox(
    "Safe Search",
    options=["off", "active"],
    help="Filter adult content"
)
```

### Adding Export Formats
Extend the download functionality to support JSON, Excel, etc.:

```python
# Add to streamlit_app.py
if st.button("📥 Download JSON"):
    json_data = df.to_json(orient='records')
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name=f"refine_filters_{timestamp}.json",
        mime="application/json"
    )
```

## 📞 Support

- **SerpAPI Documentation:** [serpapi.com/search-api](https://serpapi.com/search-api)
- **Streamlit Documentation:** [docs.streamlit.io](https://docs.streamlit.io)
- **Issues:** Check your API key and keyword format first

---

**Happy extracting! 🔍✨**