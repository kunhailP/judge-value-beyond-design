"""Machine-specific locations. Data (pools, judge outputs; not redistributed) live under $JV_DATA (default: <repo>/data)."""
import os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.environ.get("JV_DATA", os.path.join(REPO, "data"))
