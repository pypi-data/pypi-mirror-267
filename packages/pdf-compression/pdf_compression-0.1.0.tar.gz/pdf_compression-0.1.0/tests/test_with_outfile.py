import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_compression.compress_pdf import compress_pdf

# compress with outfile
infile = 'tests/resources/ex1.pdf'
outfile = 'out1.pdf'
compress_pdf(infile, outfile)
print("Compression rate:", 100- (os.path.getsize(outfile)/os.path.getsize(infile) * 100))