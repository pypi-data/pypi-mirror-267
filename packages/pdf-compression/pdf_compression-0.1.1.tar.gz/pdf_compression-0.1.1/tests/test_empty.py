import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_compression.compress_pdf import EmptyFileError, compress_pdf

# throws EmptyFileError
infile = 'tests/resources/empty.pdf'
outfile = 'out_empty.pdf'

try:
    compress_pdf(infile, outfile)
except EmptyFileError:
    print("File is empty")
