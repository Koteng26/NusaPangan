"""
Helper utility for NusaPangan — handles data paths correctly
Works both locally and on Streamlit Cloud
"""
import os
import pandas as pd

def get_data_path(filename):
    """Get correct path to data file regardless of where app is run from."""
    # Try relative to this file first
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "data", filename)
    if os.path.exists(path):
        return path
    
    # Try from current working directory
    path2 = os.path.join("data", filename)
    if os.path.exists(path2):
        return path2
    
    # Try parent directory
    path3 = os.path.join(os.path.dirname(base), "data", filename)
    if os.path.exists(path3):
        return path3
    
    raise FileNotFoundError(f"Cannot find {filename} in any expected location")

def load_data(filename):
    """Load a CSV data file."""
    return pd.read_csv(get_data_path(filename))

# Common CSS for all pages
COMMON_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* White clean background */
    .stApp { background-color: #ffffff !important; }
    .main .block-container { background: #ffffff; }
    
    .np-header {
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .np-header h2 { margin: 0; font-size: 1.4rem; }
    .np-header p { margin: 0.3rem 0 0 0; opacity: 0.8; font-size: 0.9rem; }
    
    .np-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s;
    }
    .np-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
    
    .np-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .np-badge-green { background: #E8F5E9; color: #1B5E20; }
    .np-badge-red { background: #FFEBEE; color: #C62828; }
    .np-badge-orange { background: #FFF3E0; color: #E65100; }
    .np-badge-blue { background: #E3F2FD; color: #0D47A1; }
    
    .np-alert {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .np-alert-red { background: #FFEBEE; border-left: 4px solid #F44336; }
    .np-alert-orange { background: #FFF3E0; border-left: 4px solid #FF9800; }
    .np-alert-green { background: #E8F5E9; border-left: 4px solid #4CAF50; }
    
    .np-source {
        font-size: 0.75rem;
        color: #999;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] * { color: #333333 !important; }
    [data-testid="stSidebar"] img { border-radius: 8px; }
    
    /* Move sidebar user content ABOVE the page navigation */
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        order: -1;
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
    }
    [data-testid="stSidebarNav"] {
        order: 0;
    }
</style>
"""
