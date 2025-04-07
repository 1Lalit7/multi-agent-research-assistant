import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit.web.bootstrap
streamlit.web.bootstrap.run("src/app.py", "", [], [])