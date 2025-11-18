import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="Disaster Relief Knapsack",
    layout="wide",
    page_icon="🚚"
)

# --- Title and Header ---
st.markdown(
    """
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #1F618D;
    }
    .main-title {
        color: #2E86C1;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        color: #1F618D;
        text-align: center;
        margin-top: 5px;
    }
    </style>
    <div style="text-align: center;">
        <h1 class="main-title">🚚 Relief Resource Optimization</h1>
        <h4 class="subtitle">Maximize utility within limited truck capacity using the Fractional Knapsack principle.</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- Sidebar: Input ---
st.sidebar.header("🚛 Setup & Constraints")

# 1. Capacity Input
truck_capacity = st.sidebar.number_input(
    "Truck Capacity (kg)", 
    min_value=1.0, 
    value=100.0, 
    step=10.0, 
    format="%.1f",
    help="The total weight capacity of the relief truck."
)

st.sidebar.markdown("---")
st.sidebar.header("📦 Item Data Input")

input_option = st.sidebar.radio("Choose input method:", ["Manual Input", "Upload CSV"])

df = pd.DataFrame()

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV (Columns: Item, Weight, Importance)", 
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()  # remove extra spaces
        
        required_cols = ['Item', 'Weight', 'Importance']
        if not all(col in df.columns for col in required_cols):
            st.sidebar.error("CSV must contain 'Item', 'Weight', and 'Importance' columns.")
            df = pd.DataFrame()
        else:
            # Ensure numeric columns
            df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
            df['Importance'] = pd.to_numeric(df['Importance'], errors='coerce')
            if df[['Weight','Importance']].isnull().any().any():
                st.sidebar.error("Weight and Importance must be numeric values.")
                df = pd.DataFrame()
            else:
                st.sidebar.success(f"CSV Loaded Successfully! (Rows: {len(df)})")
                
    except Exception as e:
        st.sidebar.error(f"Error reading CSV: {e}")
        df = pd.DataFrame()


else:
    # Manual Input
    num_items = st.sidebar.number_input("Number of Items to Define", min_value=1, value=4, step=1)
    
    items_data = []
    
    # Use st.columns for a cleaner manual input layout
    col_name, col_weight, col_util = st.sidebar.columns([2, 1, 1])
    
    with col_name: col_name.markdown("**Item Name**")
    with col_weight: col_weight.markdown("**Weight (kg)**")
    with col_util: col_util.markdown("**Utility**")

    for i in range(int(num_items)):
        col_name, col_weight, col_util = st.sidebar.columns([2, 1, 1])
        
        name = col_name.text_input(f"Name", value=f"Water {i+1}", label_visibility="collapsed", key=f"name_{i}")
        weight = col_weight.number_input(f"Weight (kg)", min_value=0.1, value=10.0, format="%.1f", label_visibility="collapsed", key=f"weight_{i}")
        utility = col_util.number_input(f"Utility", min_value=0.1, value=10.0, format="%.1f", label_visibility="collapsed", key=f"util_{i}")
        
        items_data.append({'Item': name, 'Weight': weight, 'Importance': utility})
    
    df = pd.DataFrame(items_data)

# --- Main Content: Display Input and Button ---

if not df.empty:
    st.subheader("Current Item Inventory")
    
    # Calculate the crucial ratio (Utility Density)
    df['Priority Ratio (Utility/kg)'] = df['Importance'] / df['Weight']
    
    # Display the input data in a cleaner format
    st.dataframe(
        df[['Item', 'Weight', 'Importance', 'Priority Ratio (Utility/kg)']].style.format({
            "Weight": "{:.1f}", 
            "Importance": "{:.1f}",
            "Priority Ratio (Utility/kg)": "{:.2f}"
        }), 
        use_container_width=True
    )
    
    # --- Centered Button using Columns ---
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        compute_button = st.button(" Compute Optimal Load Plan", type="primary", use_container_width=True)
else:
    st.warning("Please define items manually or upload a valid CSV to proceed.")
    compute_button = False

if compute_button and not df.empty:
    
    # --- Fractional Knapsack Computation ---
    
    # 1. Sort by Ratio (The greedy step of Fractional Knapsack)
    df_sorted = df.sort_values(by='Priority Ratio (Utility/kg)', ascending=False).reset_index(drop=True)
    
    loaded_items = []
    total_utility = 0.0
    total_weight_loaded = 0.0
    remaining_capacity = truck_capacity

    for index, row in df_sorted.iterrows():
        item = row['Item']
        weight = row['Weight']
        utility = row['Importance']
        
        if remaining_capacity <= 0:
            break
            
        if remaining_capacity >= weight:
            # Load the whole item
            loaded_weight = weight
            utility_obtained = utility
            total_weight_loaded += loaded_weight
            remaining_capacity -= weight
        else:
            # Load a fraction of the item
            fraction = remaining_capacity / weight
            loaded_weight = remaining_capacity
            utility_obtained = utility * fraction
            total_weight_loaded += loaded_weight
            remaining_capacity = 0 # Truck is now full

        loaded_items.append({
            'Item': item, 
            'Weight Loaded (kg)': loaded_weight, 
            'Utility Obtained (score)': utility_obtained,
            'Fraction Loaded (%)': (loaded_weight / weight) * 100
        })
        total_utility += utility_obtained

    load_df = pd.DataFrame(loaded_items)
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #2874A6;'> Optimized Truck Loading Results</h2>", unsafe_allow_html=True)
    
    # --- Metrics Summary ---
    utilization_percent = (total_weight_loaded / truck_capacity) * 100 if truck_capacity > 0 else 0
    
    col_u, col_w, col_cap = st.columns(3)
    
    col_u.metric(
        label="Total Utility Achieved (Score)", 
        value=f"{total_utility:,.2f} U", 
        delta="MAXIMUM Possible"
    )
    col_w.metric(
        label="Total Weight Loaded", 
        value=f"{total_weight_loaded:,.2f} kg",
        delta_color="off"
    )
    col_cap.metric(
        label="Truck Utilization", 
        value=f"{utilization_percent:,.1f} %",
        delta=f"Capacity: {truck_capacity:,.1f} kg",
        delta_color="off"
    )
    
    st.markdown("---")

    # --- Load Plan Table ---
    st.subheader(" Final Load Plan Details")
    
    st.dataframe(
        load_df.style.format({
            "Weight Loaded (kg)": "{:.2f}", 
            "Utility Obtained (score)": "{:.2f}",
            "Fraction Loaded (%)": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # --- Interactive Plot ---
    st.subheader(" Load Distribution Visualization")
    
    # Plotly Bar Chart: Weight Loaded
    fig = px.bar(
        load_df, 
        x='Item', 
        y='Weight Loaded (kg)', 
        color='Item',
        text='Weight Loaded (kg)',
        hover_data=['Utility Obtained (score)', 'Fraction Loaded (%)'],
        color_discrete_sequence=px.colors.qualitative.Dark24,
        title=f"Weight Loaded vs. Truck Capacity ({truck_capacity:.1f} kg)"
    )
    fig.add_hline(y=truck_capacity, line_dash="dot", annotation_text="Truck Capacity", annotation_position="top left")
    
    fig.update_traces(texttemplate='%{text:.1f} kg', textposition='outside')
    fig.update_layout(yaxis_title="Weight Loaded (kg)", xaxis_title="Item", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Expander for Algorithm Insight ---
    with st.expander(" Algorithm Insight: Priority Sorting Table"):
        st.write("The Fractional Knapsack algorithm selects items based on the **Priority Ratio (Utility/kg)**, loading them from highest to lowest ratio until the capacity is full.")
        st.dataframe(
            df_sorted[['Item', 'Weight', 'Importance', 'Priority Ratio (Utility/kg)']].style.format({
                "Weight": "{:.1f}", 
                "Importance": "{:.1f}",
                "Priority Ratio (Utility/kg)": "{:.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )


st.markdown("---")
st.markdown("""
<div style='text-align:center; 
            padding-top:20px; 
            color:#7F8C8D; 
            font-size:14px; 
            font-style:italic;'>
    Code available at <a href='https://github.com/RohankumarReddy' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
