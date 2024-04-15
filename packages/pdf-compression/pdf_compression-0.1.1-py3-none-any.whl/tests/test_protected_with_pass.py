import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_compression.compress_pdf import compress_pdf


# compress protected pdf
infile = 'tests/resources/ex2_protected.pdf'
outfile = 'out2.pdf'
compress_pdf(infile, outfile, '123456')
print("Compression rate:", 100- (os.path.getsize(outfile)/os.path.getsize(infile) * 100))
