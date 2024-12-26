import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Objects.Dashboard import Dashboard
from Objects.Plot import Plot
import streamlit as st
from streamlit import session_state as state
from streamlit_elements import elements, sync, event,lazy
from types import SimpleNamespace
import json

def main():
    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            radar=Plot(board, 12,  7, w=5, h=7, minW=2, minH=4),
        )
        print(w)
        state.w = w

    else:
        w = state.w
    
    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.radar()


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()