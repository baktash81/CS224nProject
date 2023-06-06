#!/bin/bash

# Display initial message
echo "Generating graphs and tables."

# Run Python code
python3 general_reports.py
python3 common_noncommon.py
python3 10_noncommon.py
python3 RNF.py
python3 TF-IDF.py
python3 histogram.py

echo "Build new pdf using latex"

# Change directory to ./latex
cd ./latex

# Run pdflatex on mydocument.tex
pdflatex Phase1-Report.tex

# Display final message
echo "Now you can open pdf file in latex directory :) ."
