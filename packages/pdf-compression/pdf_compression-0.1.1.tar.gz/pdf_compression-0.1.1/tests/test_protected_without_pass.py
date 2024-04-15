import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_compression.compress_pdf import FileNeedsPasswordError, compress_pdf


# throws FileNeedsPasswordError
infile = 'tests/resources/ex2_protected.pdf'
outfile = 'out2.pdf'
try:
    compress_pdf(infile, outfile)
except FileNeedsPasswordError:
    print("File needs a password")
print("Compression rate:", 100- (os.path.getsize(outfile)/os.path.getsize(infile) * 100))
