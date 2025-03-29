import streamlit as st
import plotly.graph_objs as go
import numpy as np
import io
import pandas as pd

st.title("Create Compressor Curve")

st.markdown("""
    <style>
    .centered-input input {
        text-align: center;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# def convert_df_to_csv(df):
#     buffer = io.StringIO()
#     df.to_csv(buffer, index = False)
#     buffer.seek(0)
#     return buffer

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**X-max**")  # Label for Value 1
        X_max = st.number_input("X-max", min_value=1.0, step=1.0, format="%.2f", key = "X_max")
    with col2:
        st.markdown("**Y-max**")  # Label for Value 2
        Y_max = st.number_input("Y-max", min_value=1.0, step=1.0, format="%.2f",key = "Y_max")
    with col3:
        st.markdown("**Points no**")  # Label for Value 3
        points_no = st.number_input("Points no", min_value=1.0, step=1.0, format="%.0f", key = "Points no")

    # Second row with three columns
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("**Operating X**")  # Label for Value 4
        opr_x = st.number_input("Operating X", min_value=1.0, step=1.0, format="%.2f", key = "opr_x")
    with col5:
        st.markdown("**Operating Y**")  # Label for Value 5
        opr_y = st.number_input("Operating Y", min_value=1.0, step=1.0, format="%.2f", key = "opr_y")

def cal_n():
    return np.log(1 - opr_y / Y_max) / np.log(opr_x / X_max)

n = cal_n()

X_points = np.linspace(0, X_max, int(points_no))
Y_points = Y_max * (1 - (X_points / X_max)**n)

if int(points_no) == 1: 
    database_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    df = pd.DataFrame(database_array, columns=['Column 1', 'Column 2', 'Column 3'])
    csv_file = df.to_csv(index = False)
else:
    df = pd.DataFrame({"X Points": X_points, 
                "Y Points": Y_points})
    csv_file = df.to_csv(index = False)

st.download_button(
    label = "CSV", 
    data = csv_file,
    file_name = "compressor_curve.csv", 
    mime = "text/csv"
)

fig = go.Figure()
fig.add_trace(go.Scatter(x = X_points, y  = Y_points, mode ='lines+markers', name='Compressor Curves'))
fig.add_trace(go.Scatter(
    x = [opr_x],
    y = [opr_y], 
    mode = 'markers', 
    name = 'operating point',
    marker = dict(size = 15, color = 'red'),  
))
fig.update_layout(
    title=dict(text= "Compressor Curve", font=dict(color='white') ),
    xaxis_title="Capacity",
    yaxis_title="Head",
    template = 'plotly_dark', 
    paper_bgcolor='black', 
    plot_bgcolor='black', 
    legend=dict(font=dict(color='white')),
)

# Display the plot
st.plotly_chart(fig)
