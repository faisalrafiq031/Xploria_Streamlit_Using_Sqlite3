import streamlit as st
import sqlite3
import pandas as pd
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import os
import altair as alt

# --- Page Configuration ---
st.set_page_config(page_title="AI Tools Directory", layout="wide")

st.markdown("""
<style>

/* Entire app background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #002B36, #14655B, #64998d);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0E1117;
            border-radius: none;
}

/* Top navigation bar */
header[data-testid="stHeader"] {
    background: linear-gradient(to right, #002B36, #14655B, #64998d);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 5px;
}
::-webkit-scrollbar-thumb {
    background-color: #002B36;
    border-radius: 50px;
}
          

div[data-baseweb="input"] > div {
    background-color: #0E1117;
    color: white;
}

div[data-baseweb="input"] > div > input {
    color: white;
}
div[data-baseweb="textarea"] > div > textarea {
    background-color: #0E1117;
    color: white;
}     

div[data-baseweb="input"] > div {
            background-color: #0E1117;
            color: white;
}
div[data-baseweb="input"] > div > input {
            color: white;
}
div[data-baseweb="textarea"] > div > textarea {
            background-color: #0E1117;
    color: white;
        }

.stSelectbox > div > div {
            background-color: #0E1117;
            color: white;
}
.stButton > button {
            background-color: #0E1117;
            color: white;
}
.stButton > button:hover {
    background: linear-gradient(to right, #002B36, #14655B, #64998d);
    color: white;
    border: 3px solid #0E1117;
}      
/* Active (when clicked) */
[data-testid="stBaseButton-secondary"]:active,
[data-testid="stBaseButton-secondary"]:focus {
    color: white !important;
    border: 2px solid #0E1117 !important;
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


st.logo("./Logo/logo.png", size="large", link=None)


with st.sidebar:
    selected_option = option_menu(
        menu_title="Navigation Menu",
        options=["Home", "Database Tables", "SQL Query Editor", "Database Designer", "Analytics & Insights"],
        icons=["house-fill", "table", "terminal", "database", "bar-chart-line-fill"],
        menu_icon="grid-fill",
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#0E1117", "border-radius": "1px", },
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",  # Reduced font size 101917
                "text-align": "left",
                "margin": "4px 0",
                "--hover-color": "#14655B",
                "white-space": "nowrap",  # Prevent text wrapping
                "overflow": "hidden",  # Hide overflowing text
                "text-overflow": "ellipsis",  # Show ellipsis for overflowing text
            },
            "nav-link-selected": {"background": "linear-gradient(to right, #002B36, #14655B, #64998d);", "color": "white"},
        },
    )


st.sidebar.markdown("---")
st.sidebar.markdown("<h2>AI Tools Directory:</h2> Streamlined data management and analysis." \
" Your data, simplified. Powered by SQLite and Streamlit, empowering data-driven insights.",unsafe_allow_html=True )

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='position: relative; bottom: 0; padding-bottom: 10px;'>Copyright 2025 | Made By <a href='https://github.com/faisalrafiq031' style='background: linear-gradient(to right, #A7FFEB); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Faisal Rafiq</a></div>", unsafe_allow_html=True)

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

                    # Convert DataFrame to styled HTML table
                    styled_table = df.to_html(index=False, classes='custom-table')

                    # CSS styling with scrollable container
                    st.markdown("""
                        <style>
                        .custom-table {
                            width: 100%;
                            border-collapse: collapse;
                            background: linear-gradient(to right, #002B36, #14655B, #64998d);
                            color: white;
                            border: 2px solid #002B36;
                            border-radius: 2px;
                            font-family: Arial, sans-serif;
                        }

                        .custom-table th, .custom-table td {
                            padding: 12px;
                            text-align: left;
                            border-bottom: 2px solid #002B36;
                        }

                        .custom-table th {
                            background-color: rgba(14, 17, 23, 0.9);
                        }

                        .scroll-table {
                            max-height: 500px;
                            overflow-y: auto;
                            overflow-x: auto;
                            border-right: 2px solid #002B36;
                            border-radius: 4px;
                            margin-top: 5px;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    # Wrap table in scrollable div
                    scrollable_table = f"""
                    <div class="scroll-table">
                        {styled_table}
                    </div>
                    """
                    st.markdown(scrollable_table, unsafe_allow_html=True)
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
        theme="dark",
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

    # Inject custom CSS for the styled table
    st.markdown("""
        <style>
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            background: linear-gradient(to right, #002B36, #14655B, #64998d);
            color: white;
            border: 2px solid #002B36;
            border-radius: 8px;
            font-family: Arial, sans-serif;
        }

        .custom-table th, .custom-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #002B36;
        }

        .custom-table th {
            background-color: rgba(14, 17, 23, 0.9);
        }

        .scroll-table {
            max-height: 500px;
            overflow-y: auto;
            overflow-x: auto;
            border-right: 2px solid #002B36;
            border-radius: 4px;
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    if sql_input and sql_input.strip():
        queries = [q.strip() for q in sql_input.split(";") if q.strip()]
        selected_query = st.selectbox("Select query to execute:", queries)

        if st.button("Execute Query"):
            if conn:
                try:
                    result_df = pd.read_sql_query(selected_query, conn)

                    # Convert result to styled HTML table
                    styled_table = result_df.to_html(index=False, classes='custom-table')

                    # Wrap in scrollable div and render
                    scrollable_table = f"""
                        <div class="scroll-table">
                            {styled_table}
                        </div>
                    """
                    st.markdown(scrollable_table, unsafe_allow_html=True)
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
        st.markdown("""
    <div style="
        background-color: rgba(14, 17, 23, 0.9);
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
        font-size: 16px;
    ">
        Enter SQL queries to execute.
    </div>
""", unsafe_allow_html=True)


# --- Page: Database Designer ---
elif selected_option == "Database Designer":
    st.markdown("<h1>Database Designer</h1>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Change tab underline (slider) */
    [data-baseweb="tab-highlight"] {
        background-color: rgba(14, 17, 23, 0.9); !important;
    }
    
    /* Change tab underline (slider) */
    [data-baseweb="tab-highlight"]:hover {
        background-color: #14655B !important;
    }

    /* Optional: style tab text and hover */
    .stTabs [data-baseweb="tab"] {
        color: white;
        font-weight: bold; 
        font-size: 16px;
        transition: background 0.3s;
        border-radius: 6px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: white;
    }

    .stTabs [aria-selected="true"] {
        color: rgba(14, 17, 23, 0.9);
    }
    </style>
""", unsafe_allow_html=True)

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
        # st.dataframe(df_summary, use_container_width=True)
        styled_table = df_summary.to_html(index=False, classes='custom-table')
        # Inject CSS + Render styled HTML table
        st.markdown("""
            <style>
            .custom-table {
                width: 100%;
                border-collapse: collapse;
                background: linear-gradient(to right, #14655B, #64998d);
                color: white;
                border: 2px solid #002B36;
                border-radius: 0px;
                overflow: hidden;
            }

            .custom-table th, .custom-table td {
                padding: 12px;
                text-align: left;
                border: 2px solid #002B36;
            }

            .custom-table th {
                background-color: rgba(14, 17, 23, 0.9);
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(styled_table, unsafe_allow_html=True)
        col1, col2 = st.columns(2)

    # Chart 1: Row count per table with custom styling
    with col1:
        st.markdown("**Row Count per Table**")
        chart1 = alt.Chart(df_summary).mark_bar(
            color="#14655B",
            stroke="#14655B",
            strokeWidth=2
        ).encode(
            x=alt.X('Table:N', sort='-y', title='Table'),
            y=alt.Y('Rows:Q', title='Row Count'),
            tooltip=['Table', 'Rows']
        ).properties(
            height=400,
            width=400,
            background='linear-gradient(to right, #002B36, #14655B, #64998d)'
        )
        st.altair_chart(chart1, use_container_width=True)

    # Chart 2: Tools by Rating with custom styling
    with col2:
        st.markdown("**Tools by Rating (if available)**")
        try:
            rating_df = pd.read_sql("""
                SELECT rating_stars, COUNT(*) as count
                FROM CategoryAI
                GROUP BY rating_stars
            """, conn)

            rating_df = rating_df.sort_values(by='rating_stars', ascending=False)

            chart2 = alt.Chart(rating_df).mark_bar(
                color="#14655B",
                stroke="#14655B",
                strokeWidth=2
            ).encode(
                x=alt.X('rating_stars:N', title='Rating'),
                y=alt.Y('count:Q', title='Count'),
                tooltip=['rating_stars', 'count']
            ).properties(
                height=400,
                width=400,
                background='linear-gradient(to right, #002B36, #14655B, #64998d)'
            )
            st.altair_chart(chart2, use_container_width=True)

        except Exception as e:
            st.info("Rating data not available. Check CategoryAI table structure.")

