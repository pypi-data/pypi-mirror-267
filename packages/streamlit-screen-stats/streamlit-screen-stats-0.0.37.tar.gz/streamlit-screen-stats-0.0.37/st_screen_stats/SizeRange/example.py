import streamlit as st
# from __init__ import WindowScreenRange
from st_screen_stats import WindowScreenRange

st.set_page_config(layout="wide")

test_class = WindowScreenRange()
st.write(test_class.WidthUpperRangeTop(1400))
# st.write(test_class.WidthUpperLimitTop(1400))
# st.write(test_class.WidthLowerRange(700))
