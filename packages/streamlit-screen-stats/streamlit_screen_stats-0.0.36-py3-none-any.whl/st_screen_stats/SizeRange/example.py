import streamlit as st
from __init__ import WindowScreenRange

st.set_page_config(layout="wide")

test_class = WindowScreenRange()
st.write(test_class.WidthUpperRangeTop(1300))
# st.write(test_class.WidthLowerRange(700))
