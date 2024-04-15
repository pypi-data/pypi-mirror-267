import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_compression.compress_pdf import PdfFileNotFoundError, compress_pdf

# throws FileNotFoundError
infile = 'does_not_exist.pdf'
outfile = 'out_not_exist.pdf'
try:
    compress_pdf(infile, outfile)
except PdfFileNotFoundError:
    print("File name given does not exist")
