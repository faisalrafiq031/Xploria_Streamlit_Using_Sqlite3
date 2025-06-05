import streamlit as st
import sqlite3
import pandas as pd
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import os

# --- Page Configuration ---
st.set_page_config(page_title="AI Tools Directory", layout="wide")

st.markdown("""
<style>

/* Entire app background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #44104F, #782B84);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #00172B;
}

/* Top navigation bar */
header[data-testid="stHeader"] {
    background: linear-gradient(to right, #44104F, #782B84);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 5px;
}
::-webkit-scrollbar-thumb {
    background-color: #44104F;
    border-radius: 50px;
}
          

div[data-baseweb="input"] > div {
    background-color: #00172B;
    color: white;
}

div[data-baseweb="input"] > div > input {
    color: white;
}
div[data-baseweb="textarea"] > div > textarea {
    background-color: #00172B;
    color: white;
}     

div[data-baseweb="input"] > div {
            background-color: #00172B;
            color: white;
}
div[data-baseweb="input"] > div > input {
            color: white;
}
div[data-baseweb="textarea"] > div > textarea {
            background-color: #00172B;
    color: white;
        }

.stSelectbox > div > div {
            background-color: #00172B;
            color: white;
}
.stButton > button {
            background-color: #00172B;
            color: white;
}
.stButton > button:hover {
    background: linear-gradient(to left, #ff14fb, #782B84);
    color: white;
    border: 3px solid #44104F;
}              

          
</style>
""", unsafe_allow_html=True)

# --- SQLite3 Connection ---
DB_PATH = "data.db"

def get_connection():
    try:
        return sqlite3.connect(DB_PATH, check_same_thread=False)
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
        return None

conn = get_connection()


st.sidebar.markdown("<h1 style='background: linear-gradient(to right, #ff14fb, #ff69b4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>AI Tools Directory</h1>", unsafe_allow_html=True)


with st.sidebar:
    selected_option = option_menu(
        menu_title="Navigation Menu",
        options=["Home", "Database Tables", "SQL Query Editor", "Database Designer", "Analytics & Insights"],
        icons=["house-fill", "table", "terminal", "database", "bar-chart-line-fill"],
        menu_icon="grid-fill",
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#00172B"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",  # Reduced font size
                "text-align": "left",
                "margin": "4px 0",
                "--hover-color": "#2a2a2a",
                "white-space": "nowrap",  # Prevent text wrapping
                "overflow": "hidden",  # Hide overflowing text
                "text-overflow": "ellipsis",  # Show ellipsis for overflowing text
            },
            "nav-link-selected": {"background": "linear-gradient(to right, #ff69b4, #ff14fb)", "color": "white"},
        },
    )


st.sidebar.markdown("---")
st.sidebar.markdown("<h2>AI Tools Directory:</h2> Streamlined data management and analysis." \
"Your data, simplified. Powered by SQLite and Streamlit, empowering data-driven insights.",unsafe_allow_html=True )

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='position: relative; bottom: 0; padding-bottom: 10px;'>Copyright 2025 | Made By <a href='https://github.com/faisalrafiq031' style='background: linear-gradient(to right, #ff14fb, #ff69b4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Faisal Rafiq</a></div>", unsafe_allow_html=True)

# --- Page: Overview ---
if selected_option == "Home":
    st.markdown("<h1>AI Tools Directory Explorer</h1>", unsafe_allow_html=True)
    st.markdown("""
    Welcome to the **AI Tools Directory** - a streamlined interface built to manage and analyze data.

    ### Application Workflow:
    1. **Data Import**: Data is stored in a local SQLite database.
    2. **Exploration**: This Streamlit dashboard connects to the SQLite DB offering:
       - On-demand access to tables
       - SQL query execution
       - Database Designer
       - Dashboard analytics and insights
    """)

# --- Page: Database Tables ---
elif selected_option == "Database Tables":
    st.markdown("<h1>Database Table Viewer</h1>", unsafe_allow_html=True)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        if tables:
            table_name = st.selectbox("Select a table", tables)

            if st.button("Load Table Data"):
                try:
                    df = pd.read_sql_query(f"SELECT * FROM `{table_name}` LIMIT 100", conn)
                    st.dataframe(df, use_container_width=True)
                    st.caption(f"Showing top 100 rows from **{table_name}**")
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
        else:
            st.warning("No tables found in database.")
    else:
        st.warning("Unable to connect to SQLite database.")

# --- Page: SQL Query Editor ---
elif selected_option == "SQL Query Editor":
    st.markdown("<h1>SQL Query Editor</h1>", unsafe_allow_html=True)
    st.markdown("Write and run your custom SQL queries below:")

    sql_input = st_ace(
        placeholder="Write your SQL queries here...",
        language="sql",
        theme="dracula",
        font_size=16,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
        key="ace_editor",
        min_lines=10,
        height=200,
    )

    if sql_input and sql_input.strip():
        queries = [q.strip() for q in sql_input.split(";") if q.strip()]
        selected_query = st.selectbox("Select query to execute:", queries)

        if st.button("Execute Query"):
            if conn:
                try:
                    result_df = pd.read_sql_query(selected_query, conn)
                    st.dataframe(result_df, use_container_width=True)
                    st.success("Query executed successfully.")
                except Exception as e:
                    try:
                        cursor = conn.cursor()
                        cursor.execute(selected_query)
                        conn.commit()
                        st.success("Query executed (no result set).")
                    except Exception as inner_e:
                        st.error(f"Execution error: {inner_e}")
            else:
                st.warning("No database connection.")
    else:
        st.info("Enter SQL queries to execute.")

# --- Page: Database Designer ---
elif selected_option == "Database Designer":
    st.markdown("<h1>Database Designer</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Create Table", "Insert Data"])

    # Tab 1: Create Table
    with tabs[0]:
        st.subheader("Create Table")
        table_name = st.text_input("Table name:")
        columns_input = st.text_area("Columns (e.g., id INTEGER PRIMARY KEY, name TEXT)")
        if st.button("Create Table"):
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE TABLE {table_name} ({columns_input})")
                    conn.commit()
                    st.success(f"Table `{table_name}` created.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Tab 2: Insert Data
    with tabs[1]:
        st.subheader("Insert Data")
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [t[0] for t in cursor.fetchall()]
            selected_table = st.selectbox("Choose table:", tables)

            if selected_table:
                cursor.execute(f"PRAGMA table_info({selected_table})")
                columns = cursor.fetchall()
                values = []
                for col in columns:
                    val = st.text_input(f"{col[1]} ({col[2]})")
                    values.append(val)

                if st.button("Insert Record"):
                    try:
                        placeholders = ", ".join(["?"] * len(values))
                        col_names = ", ".join([col[1] for col in columns])
                        cursor.execute(f"INSERT INTO {selected_table} ({col_names}) VALUES ({placeholders})", values)
                        conn.commit()
                        st.success("Record inserted.")
                    except Exception as e:
                        st.error(f"Insertion failed: {e}")
        else:
            st.warning("Database connection not established.")

# Step 5: Dashboard & Analytics
elif selected_option == "Analytics & Insights":
    st.markdown("<h1>Analytics & Insights</h1>", unsafe_allow_html=True)

    if conn:
        cursor = conn.cursor()

        # Get all table names in sqlite3
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        row_counts = []

        # Get row count for each table
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                row_counts.append(count)
            except:
                row_counts.append(0)

        # Display table overview
        df_summary = pd.DataFrame({
            "Table": tables,
            "Rows": row_counts
        }).sort_values(by="Rows", ascending=False)

        st.markdown("<h3>Database Overview</h3>", unsafe_allow_html=True)
        st.dataframe(df_summary, use_container_width=True)

        col1, col2 = st.columns(2)

        # Chart 1: Row count per table
        with col1:
            st.markdown("**Row Count per Table**")
            st.bar_chart(df_summary.set_index("Table")["Rows"])

        # Chart 2: Rating-wise count (if table and column exist)
        with col2:
            st.markdown("**Tools by Rating (if available)**")
            try:
                # Adjust this table/column as per your DB structure
                rating_df = pd.read_sql("""
                    SELECT rating_stars, COUNT(*) as count
                    FROM CategoryAI
                    GROUP BY rating_stars
                """, conn)

                # Sort by rating if needed
                rating_df = rating_df.sort_values(by='rating_stars', ascending=False)
                st.bar_chart(rating_df.set_index('rating_stars')['count'])

            except Exception as e:
                st.info("Rating data not available. Check CategoryAI table structure.")
    else:
        st.warning("Database connection failed. Please check credentials.")

