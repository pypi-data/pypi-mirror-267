import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_compression.compress_pdf import compress_pdf

# compress without outfile
infile = 'tests/resources/ex1.pdf'
compress_pdf(infile)
print("Compression rate:", 100- (os.path.getsize(infile[:-4]+"_compressed.pdf")/os.path.getsize(infile) * 100))
