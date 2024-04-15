import sys
import os

from pdf_compression.compress_pdf import compress_pdf, NotPdfError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# throws NotPdfError
infile = 'tests/resources/image.jpeg'
outfile = 'out_nonpdf.pdf'
try:
    compress_pdf(infile, outfile)
except NotPdfError:
    print("File is not a PDF")
