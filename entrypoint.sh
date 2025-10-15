#!/bin/sh
set -e

# Check the RUN_MODE environment variable.
if [ "$RUN_MODE" = "notebook" ]; then
  echo "--- Running application from Jupyter Notebook (non-interactive) ---"
  exec jupyter nbconvert --to python --execute app.ipynb
elif [ "$RUN_MODE" = "jupyter" ]; then
  echo "--- Starting Jupyter Notebook server ---"
  exec jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
else
  echo "--- Running application from Python script ---"
  exec python ./app.py
fi