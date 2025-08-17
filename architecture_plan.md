# Streamlit Shopping Facets Extractor - Architecture Plan

## Application Flow

```mermaid
flowchart TD
    A[User opens Streamlit App] --> B[Configuration Section]
    B --> C{API Key provided?}
    C -->|No| D[Show error message]
    C -->|Yes| E[Keywords Input Section]
    E --> F{Keywords valid?}
    F -->|No| G[Show validation errors]
    F -->|Yes| H[User clicks Run button]
    H --> I[Initialize progress bar]
    I --> J[Start processing keywords]
    J --> K[For each keyword]
    K --> L[Call SerpAPI]
    L --> M{API call successful?}
    M -->|No| N[Log error, continue to next]
    M -->|Yes| O[Extract refine filters]
    O --> P[Add to consolidated results]
    P --> Q[Update progress bar]
    Q --> R{More keywords?}
    R -->|Yes| K
    R -->|No| S[Generate consolidated CSV]
    S --> T[Display download button]
    T --> U[User downloads CSV file]
```

## Application Structure

### Main Components

1. **Configuration Panel**
   - API key input (required)
   - Country selector (gl parameter, default: "us")
   - Language selector (hl parameter, default: "en")

2. **Keywords Input Section**
   - Text area for entering keywords (one per line)
   - Validation: maximum 30 keywords
   - Real-time keyword count display

3. **Processing Section**
   - Run button to start extraction
   - Progress bar showing current keyword being processed
   - Status messages for user feedback

4. **Results Section**
   - Download button for consolidated CSV
   - Summary statistics (total filters found, successful/failed searches)

### Technical Architecture

- **streamlit_app.py**: Main application file
- **search_utils.py**: Extracted search functions from main.py
- **Consolidated CSV Output**: Format with columns: `Keyword`, `Type`, `Title`

### Key Features

- **Error Resilience**: Continue processing even if some API calls fail
- **Progress Tracking**: Real-time updates during batch processing
- **Extensible Design**: Easy to add more SerpAPI parameters later
- **User-Friendly**: Clear validation messages and error handling

## Expected User Experience

1. User enters SerpAPI key
2. Optionally adjusts country and language settings
3. Enters keywords (one per line, max 30)
4. Clicks "Run Extraction"
5. Watches progress as each keyword is processed
6. Downloads consolidated CSV when complete

## Implementation Priority

The todo list follows a logical implementation order:
1. Setup and dependencies
2. Core UI components
3. Backend functionality
4. Integration and testing
5. Documentation