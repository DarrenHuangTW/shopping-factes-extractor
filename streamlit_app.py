import streamlit as st
import pandas as pd
from datetime import datetime
import io
from search_utils import process_keywords_batch, validate_keywords, save_consolidated_csv


# Page configuration
st.set_page_config(
    page_title="Shopping Facets Extractor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🔍 Shopping Facets Extractor")
st.markdown("Extract Google Shopping refine filters for multiple keywords using SerpAPI")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# API Key input
api_key = st.sidebar.text_input(
    "SerpAPI Key *",
    type="password",
    help="Enter your SerpAPI key. Get one at https://serpapi.com/"
)

# Country selection
country_options = {
    "Australia": "au",
    "New Zealand": "nz",
    "United States": "us",
    "Singapore": "sg",
    "Philippines": "ph",
    "United Kingdom": "uk", 
    "Germany": "de"
}

selected_country = st.sidebar.selectbox(
    "Country (gl parameter)",
    options=list(country_options.keys()),
    index=0,
    help="Select the country for Google search localization"
)
gl_param = country_options[selected_country]

# Language selection
language_options = {
    "English": "en",
    "Spanish": "es",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw"
}

selected_language = st.sidebar.selectbox(
    "Language (hl parameter)",
    options=list(language_options.keys()),
    index=0,
    help="Select the language for Google search interface"
)
hl_param = language_options[selected_language]

# Main content area
st.header("📝 Keywords Input")

# Keywords input
keywords_text = st.text_area(
    "Enter keywords (one per line, max 30):",
    height=200,
    placeholder="low heels\nrunning shoes\nwinter jackets\n...",
    help="Enter each keyword on a separate line. Maximum 30 keywords allowed."
)

# Real-time keyword count
if keywords_text:
    keyword_lines = [line.strip() for line in keywords_text.strip().split('\n') if line.strip()]
    keyword_count = len(keyword_lines)
    
    if keyword_count > 30:
        st.error(f"⚠️ Too many keywords: {keyword_count}/30")
    elif keyword_count > 0:
        st.info(f"📊 Keywords count: {keyword_count}/30")

# Processing section
st.header("🚀 Processing")

# Validation and run button
can_run = bool(api_key and keywords_text)

if st.button("🔍 Run Extraction", disabled=not can_run, type="primary"):
    if not api_key:
        st.error("❌ Please provide your SerpAPI key in the sidebar.")
    elif not keywords_text:
        st.error("❌ Please enter at least one keyword.")
    else:
        # Validate keywords
        valid_keywords, validation_errors = validate_keywords(keywords_text, max_keywords=30)
        
        if validation_errors:
            for error in validation_errors:
                st.error(f"❌ {error}")
        else:
            # Initialize session state for results
            if 'processing_results' not in st.session_state:
                st.session_state.processing_results = None
            
            # Create progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Progress callback function
            def update_progress(current, total, current_keyword):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Processing keyword {current + 1}/{total}: '{current_keyword}'")
            
            # Process keywords
            with st.spinner("Starting extraction..."):
                try:
                    all_data, failed_keywords, search_metadata_list = process_keywords_batch(
                        valid_keywords,
                        api_key,
                        gl_param,
                        hl_param,
                        progress_callback=update_progress
                    )
                    
                    # Update progress to complete
                    progress_bar.progress(1.0)
                    status_text.text("✅ Processing complete!")
                    
                    # Store results in session state
                    st.session_state.processing_results = {
                        'data': all_data,
                        'failed_keywords': failed_keywords,
                        'search_metadata': search_metadata_list,
                        'total_keywords': len(valid_keywords),
                        'successful_keywords': len(valid_keywords) - len(failed_keywords),
                        'total_filters': len(all_data),
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                except Exception as e:
                    st.error(f"❌ An error occurred during processing: {str(e)}")
                    progress_bar.empty()
                    status_text.empty()

# Results section
if 'processing_results' in st.session_state and st.session_state.processing_results:
    results = st.session_state.processing_results
    
    st.header("📊 Results")
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Keywords", results['total_keywords'])
    
    with col2:
        st.metric("Successful", results['successful_keywords'])
    
    with col3:
        st.metric("Failed", len(results['failed_keywords']))
    
    with col4:
        st.metric("Total Filters", results['total_filters'])
    
    # Show failed keywords if any
    if results['failed_keywords']:
        st.warning("⚠️ Some keywords failed to process:")
        for keyword in results['failed_keywords']:
            st.write(f"• {keyword}")
    
    # Data preview
    if results['data']:
        st.subheader("📋 Data Preview")
        
        # Convert to DataFrame for display
        df = pd.DataFrame(results['data'], columns=['Keyword', 'Attribute', 'Value'])
        st.dataframe(df, use_container_width=True)
        
        # Search Metadata section
        if 'search_metadata' in results and results['search_metadata']:
            st.subheader("🔍 Search Metadata")
            
            # Create metadata DataFrame
            metadata_df = pd.DataFrame(results['search_metadata'])
            
            # Select and reorder columns to show the most important ones first
            important_columns = ['keyword', 'status', 'total_time_taken']
            optional_columns = ['raw_html_file', 'processed_at', 'google_url']
            excluded_columns = ['id', 'created_at', 'json_endpoint', 'pixel_position_endpoint']
            
            # Build column list with available columns
            display_columns = []
            for col in important_columns:
                if col in metadata_df.columns:
                    display_columns.append(col)
            
            for col in optional_columns:
                if col in metadata_df.columns:
                    display_columns.append(col)
            
            # Add any remaining columns (except excluded ones)
            for col in metadata_df.columns:
                if col not in display_columns and col not in excluded_columns:
                    display_columns.append(col)
            
            # Display metadata table
            if display_columns:
                st.dataframe(metadata_df[display_columns], use_container_width=True)
            
            # Show expandable raw HTML file links if available
            if 'raw_html_file' in metadata_df.columns:
                with st.expander("🔗 Raw HTML Files"):
                    for _, row in metadata_df.iterrows():
                        if pd.notna(row.get('raw_html_file')):
                            st.markdown(f"**{row.get('keyword', 'Unknown')}**: [{row['raw_html_file']}]({row['raw_html_file']})")
        
        # Download section
        st.subheader("💾 Download Results")
        
        # Generate CSV content
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"refine_filters_{timestamp}.csv"
        
        # Download button
        st.download_button(
            label="📥 Download CSV",
            data=csv_content,
            file_name=filename,
            mime="text/csv",
            type="primary"
        )
        
        st.success(f"✅ Ready to download {len(df)} filter results!")
    
    else:
        st.warning("⚠️ No refine filters found in the search results.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🤖 <strong>Made by Darren Huang & His AI Sidekick</strong></p>
        <p>Built with Streamlit • Powered by SerpAPI</p>
        <p>Found a bug? Have questions? Need someone to blame?
        <a href='https://www.linkedin.com/in/hunghsunhuang/' target='_blank' style='color: #0077B5; text-decoration: none;'>
        📧 Talk to me via LinkedIn DMs</a> 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)