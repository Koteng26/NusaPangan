"""
Helper utility for NusaPangan
"""
import os
import pandas as pd

def get_data_path(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "data", filename)
    if os.path.exists(path):
        return path
    path2 = os.path.join("data", filename)
    if os.path.exists(path2):
        return path2
    path3 = os.path.join(os.path.dirname(base), "data", filename)
    if os.path.exists(path3):
        return path3
    raise FileNotFoundError(f"Cannot find {filename}")

def load_data(filename):
    return pd.read_csv(get_data_path(filename))

COMMON_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Warm light green gradient background */
    .stApp { background: linear-gradient(180deg, #f0fdf4 0%, #ecfccb 50%, #f0fdf4 100%) !important; }
    
    .np-header {
        padding: 1.5rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .np-header h2 { margin: 0; font-size: 1.4rem; }
    .np-header p { margin: 0.3rem 0 0 0; opacity: 0.85; font-size: 0.9rem; }
    
    .np-card {
        background: white;
        border: 1px solid #c8e6c9;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 2px 12px rgba(27,94,32,0.06);
        transition: all 0.25s;
    }
    .np-card:hover { 
        box-shadow: 0 6px 24px rgba(27,94,32,0.14);
        transform: translateY(-2px);
    }
    
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
        padding: 1rem 1.2rem;
        border-radius: 14px;
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
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebar"] * { color: #1B5E20 !important; }
    
    /* Logo + tagline above nav */
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        order: -1;
        padding-top: 0.5rem;
        padding-bottom: 0;
    }
    
    /* Team info below nav */
    [data-testid="stSidebarNav"]::after {
        content: "🌾 NusaPangan · Tim We Are Solution\a PIDI DIGDAYA × HACKATHON 2026";
        display: block;
        text-align: center;
        font-size: 0.68rem;
        color: #999 !important;
        padding: 16px 12px 8px;
        line-height: 1.6;
        white-space: pre-line;
        margin-top: 12px;
    }
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
    }
    [data-testid="stSidebarNav"] {
        order: 0;
        margin-top: -1rem;
    }
    
    /* Nav active */
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: #E8F5E9 !important;
        border-radius: 10px;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #c8e6c9;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 2px 8px rgba(27,94,32,0.06);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #c8e6c9;
    }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #c8e6c9;
        border-radius: 14px;
        overflow: hidden;
    }
    
    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        border-radius: 10px !important;
    }
</style>
"""
