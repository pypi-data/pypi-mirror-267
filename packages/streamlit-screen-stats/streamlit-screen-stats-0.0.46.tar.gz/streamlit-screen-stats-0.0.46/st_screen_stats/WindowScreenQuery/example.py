from __init__ import WindowQuerySize
import streamlit as st

st.set_page_config(layout="wide")

screenSizeInit = WindowQuerySize()
# result = screenSizeInit.mediaQueryT("(max-width: 700px)")

width_threshold = "max"
value_ = 700

result = f'"({width_threshold}-width: {value_}px)"'

st.write(result)

width_threshold = "min"
value_2 = 900
range_result = f'"({width_threshold}-width: {value_}px) and ({width_threshold}-width: {value_2}px)"'

st.write(range_result)

def single_width_query(measurement="max", threshold=700):

    result = f"({measurement}-width: {threshold}px)"

    return result

st.write(single_width_query())


def range_width_query(min_threshold=500, max_threshold=1000):

    result = f'"(min-width: {min_threshold}px) and (max-width: {max_threshold}px)"'

    return result

st.write(range_width_query())



