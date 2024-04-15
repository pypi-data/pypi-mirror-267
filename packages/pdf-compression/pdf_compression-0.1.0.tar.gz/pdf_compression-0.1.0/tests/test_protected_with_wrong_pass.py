import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_compression.compress_pdf import WrongPasswordError, compress_pdf


# wrong password throws WrongPasswordError
infile = 'tests/resources/ex2_protected.pdf'
outfile = 'out2.pdf'
try:
    compress_pdf(infile, outfile, '1234567')
except WrongPasswordError:
    print("Password is wrong")
print("Compression rate:", 100- (os.path.getsize(outfile)/os.path.getsize(infile) * 100))
