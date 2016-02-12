import sys
import os

# Get current script's parent folder and append it to sys.path
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)))
