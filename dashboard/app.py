# ai-code-reviewer/dashboard/app.py
import streamlit as st
import json
import pandas as pd
import os

REPORT_PATH = "code_reviewer_report.json"

def load_report(path):
    """Loads the JSON report and returns the metadata and issues."""
    if not os.path.exists(path):
        st.error(f"Error: Report file not found at {path}. Please run the CLI analysis first.")
        return None, []
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
            return report_data.get('metadata', {}), report_data.get('issues', [])
    except json.JSONDecodeError:
        st.error(f"Error: Invalid JSON format in {path}.")
        return None, []
    except Exception as e:
        st.error(f"An error occurred while loading the report: {e}")
        return None, []

def create_issue_dataframe(issues):
    """Converts the list of issues into a DataFrame for display."""
    if not issues:
        return pd.DataFrame()

    data = []
    for issue in issues:
        data.append({
            "Line": issue.get('line', 'N/A'),
            "Type": issue.get('type', 'N/A'),
            "Detected Value": issue.get('value', 'N/A'),
            "Message": issue.get('message', ''),
            "AI Suggestion": issue.get('suggestion', 'N/A'),
            "Fix Status": issue.get('autofix_status', 'N/A'),
            "Fix Description": issue.get('autofix_description', 'N/A'),
        })
    
    df = pd.DataFrame(data)
    
    return df

st.set_page_config(
    page_title="AI Code Review Dashboard", 
    page_icon="🤖", 
    layout="wide"
)

# --- Main Dashboard Logic ---
st.title("🤖 AI Code Reviewer Dashboard")

metadata, issues = load_report(REPORT_PATH)

if issues:
    st.subheader(f"Results for: `{metadata.get('file', 'N/A')}`")
    st.metric(label="Total Issues Found", value=metadata.get('total_issues', 0))
    st.markdown("---")
    
    df = create_issue_dataframe(issues)
    
    st.dataframe(
        df[['Line', 'Type', 'Detected Value', 'Message', 'Fix Status']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Line": st.column_config.NumberColumn("Line #", help="Line number in the file"),
            "Detected Value": st.column_config.TextColumn("Value", help="The detected numerical value"),
        }
    )
    

    st.subheader("Detailed Review & Solutions")
    
    # Display details using expanders
    for index, row in df.iterrows():
        with st.expander(f"Code Smell L{row['Line']}: {row['Type']} ({row['Detected Value']})"):
            st.markdown(f"**Issue:** {row['Message']}")
            
            # --- AI Suggestion ---
            st.markdown("##### 🧠 AI Suggestion")
            st.info(row['AI Suggestion'])
            
            # --- Auto-Fix Status ---
            if row['Fix Status'] == 'Prepared':
                st.markdown("##### 🔧 Auto-Fix Patch")
                st.success(f"**Status:** Fix Prepared. This change can be applied automatically.")
                st.code(row['Fix Description'], language='markdown')
            else:
                st.markdown("##### ❌ Auto-Fix Status")
                st.warning(f"**Status:** {row['Fix Status']}. Manual refactoring is required.")

else:
    st.info("No issues found in the latest report, or the report file is missing/empty.")

# Add instructions for running the dashboard
st.sidebar.title("App Instructions")
st.sidebar.markdown(
    """
    1.  Run the CLI tool to generate the report:  
        `python -m cli.main sample_project/example.py`
    2.  Start this dashboard:  
        `streamlit run dashboard/app.py`
    """
)