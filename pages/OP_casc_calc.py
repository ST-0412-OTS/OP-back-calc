import streamlit as st
import plotly.graph_objs as go

st.title("Reverse Calculation of Controller OP from Valve Current OP")

# Larger description (heading level 4)
st.markdown("#### User need to create the control action curve by using two points and provide the controller current position that is not 0% to 100%. It only works for two lines curve.")

# Add custom CSS to center-align the text input and increase font size
st.markdown("""
    <style>
    .centered-input input {
        text-align: center;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def ys_from_points(x1, y1, x2, y2):
    try:
        m = (y2 - y1) / (x2 - x1)
    except:
        m = 0
    b = y1 - m * x1
    x_min = 0
    x_max  = 100
    y_min = min(max(m*x_min + b, 0), 100)
    y_max = min(max(m*x_max + b, 0), 100)
    return y_min, y_max, m, b

with st.container():
# First row with two columns

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center;'><b>A lines</b></p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center;'><b>B lines</b></p>", unsafe_allow_html=True)

    col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([0.4, 1, 0.4, 1, 0.4, 1, 0.4, 1]) 
    with col3:
        st.markdown("<p style='text-align: center;'>x1_A</p>", unsafe_allow_html=True)
    with col4:
        x1_A = st.number_input(label="", value=0.0, format="%.2f", key="x1_A")
    with col5:
        st.markdown("<p style='text-align: center;'>y1_A</p>", unsafe_allow_html=True)
    with col6:
        y1_A = st.number_input(label="", value=0.0, format="%.2f", key="y1_A")
    with col7:
        st.markdown("<p style='text-align: center;'>x1_B</p>", unsafe_allow_html=True)
    with col8:     
        x1_B = st.number_input(label="", value=0.0, format="%.2f", key="x1_B")
    with col9:
        st.markdown("<p style='text-align: center;'>y1_B</p>", unsafe_allow_html=True)
    with col10:
        y1_B = st.number_input(label="", value=0.0, format="%.2f", key="y1_B")

with st.container():
    col11, col12, col13, col14, col15, col16, col17, col18 = st.columns([0.4, 1, 0.4, 1, 0.4, 1, 0.4, 1]) 
    with col11:
        st.markdown("<p style='text-align: center;'>x2_A</p>", unsafe_allow_html=True)

    with col12:
        x2_A = st.number_input(label="", value=0.0, format="%.2f", key="x2_A")

    with col13:
        st.markdown("<p style='text-align: center;'>y2_A</p>", unsafe_allow_html=True)

    with col14:
        y2_A = st.number_input(label="", value=0.0, format="%.2f", key="y2_A")

    with col15:
        st.markdown("<p style='text-align: center;'>x2_B</p>", unsafe_allow_html=True)

    with col16:     
        x2_B = st.number_input(label="", value=0.0, format="%.2f", key="x2_B")

    with col17:
        st.markdown("<p style='text-align: center;'>y2_B</p>", unsafe_allow_html=True)

    with col18:
        y2_B = st.number_input(label="", value=0.0, format="%.2f", key="y2_B")

y_min_A, y_max_A, m_A, b_A = ys_from_points(x1_A, y1_A, x2_A, y2_A)
y_min_B, y_max_B, m_B, b_B = ys_from_points(x1_B, y1_B, x2_B, y2_B)

# Add dropdowns
with st.container():
    col19, col20, col21 = st.columns(3)
    with col19:
        control_action = st.selectbox("Control Action", ["Direct", "Reverse"], key="control_action")
    with col20:
        y_characteristic_line = st.selectbox("Y Characteristics Line", ["A Line", "B Line"], key="y_characteristic_line")
    with col21:
        col22, col23 = st.columns(2)
        with col22:
            st.markdown("<p style='text-align: center;'>y_char</p>", unsafe_allow_html=True)
        with col23:
            y_char = st.number_input(label="", value=0.0, format="%.2f", key="y_char")
                                             
# Create the plot
fig = go.Figure()

if control_action == "Direct":
    y_char_calc = y_char
else:
    y_char_calc = 100 - y_char

try:
    if y_characteristic_line == "A Line":
        x_guess = (y_char_calc - b_A) / m_A
    else:
        x_guess = (y_char_calc - b_B) / m_B
except:
    x_guess = 0

# Display the calculated value in a centered text input with a larger font
st.text_input("Calculated Controller OP Value", value=f"{x_guess:.3f}", key="centered-input", disabled=True)

# Add lines
fig.add_trace(go.Scatter(
    x=[0.0, x1_A, x2_A, 100.0], 
    y=[y_min_A, y1_A, y2_A, y_max_A], 
    mode='lines+markers', 
    name='A Line', 
    line=dict(color='red'), 
    marker=dict(size=10)
))
fig.add_trace(go.Scatter(
    x=[0.0, x1_B, x2_B, 100.0], 
    y=[y_min_B, y1_B, y2_B, y_max_B], 
    mode='lines+markers', 
    name='B Line', 
    line=dict(color='blue'), 
    marker=dict(size=10)
))

# Add the single dot with a larger x mark
fig.add_trace(go.Scatter(
    x=[x_guess], 
    y=[min(max(m_A*x_guess + b_A, 0), 100)], 
    mode='markers', 
    name = "A Valve",
    marker=dict(size=15, symbol='x', color='red')
))

fig.add_trace(go.Scatter(
    x=[x_guess], 
    y=[min(max(m_B*x_guess + b_B, 0), 100)], 
    mode='markers', 
    name = "B Valve",
    marker=dict(size=15, symbol='x', color='blue')
))

# Set plot limits, layout, and labels
fig.update_layout(
    xaxis=dict(range=[-5, 105], title='Controller Output', minor = dict(showgrid = False)), 
    yaxis=dict(
        range=[-5, 105], 
        title='Valve OP Received',
        minor=dict(
            showgrid=False  # Hide minor grid lines on the x-axis
        )
    ),
    legend=dict(font=dict(color='white')),
    template='plotly_dark',
    paper_bgcolor='black',  # Set the background color of the paper to black
    plot_bgcolor='black'    # Set the background color of the plot to black
)

# Display the plot in Streamlit
st.plotly_chart(fig)