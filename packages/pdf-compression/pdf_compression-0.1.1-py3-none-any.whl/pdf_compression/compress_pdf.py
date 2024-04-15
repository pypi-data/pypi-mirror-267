import io
import fitz
import os
from PIL import Image

class NotPdfError(Exception):
    pass

class PdfFileNotFoundError(Exception):
    pass

class EmptyFileError(Exception):
    pass

class FileNeedsPasswordError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

def compress_pdf(infile, outfile=None, password=None):

    if not os.path.isfile(infile):
        raise PdfFileNotFoundError("File name given does not exist")
    
    if os.path.getsize(infile) == 0:
        raise EmptyFileError("File given is empty")

    pdf_file = fitz.open(infile)
    
    if not pdf_file.is_pdf:
        raise NotPdfError("File given is not a PDF")

    if pdf_file.is_encrypted:
        if not password:
            raise FileNeedsPasswordError("Provide a password")
        if pdf_file.authenticate(password) == 0:
            raise WrongPasswordError("Password is wrong")

    # iterate over pdf pages
    for page in pdf_file:
        image_list = page.get_images()

        for img in image_list:
            xref, smask = img[0], img[1]

            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            # check transparency
            if smask == 0:
                ext = "jpeg"
            else:
                ext = "png"
                # image without transparency
                pix1 = fitz.Pixmap(image_bytes)
                # transparency mask
                mask = fitz.Pixmap(pdf_file.extract_image(smask)["image"])
                # add transparency to image
                image_bytes = fitz.Pixmap(pix1, mask).tobytes()
            
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            # compress and save it to memory
            compressed_image = io.BytesIO()
            image.save(
                compressed_image,
                format=ext,
                optimize=True,
                quality=25
                )

            # replace image
            page.replace_image(xref, stream=compressed_image)
        
    if infile == outfile or outfile == None or outfile == '':

        if infile.endswith(".pdf"):
            outfile = infile[:-4] + "_compressed.pdf"
        else:
            outfile = infile + "_compressed.pdf"

        pdf_file.save(
            outfile,
            garbage=4,
            clean=True,
            deflate_images=True,
            deflate_fonts=True,
            deflate=True
            )
        return

    pdf_file.save(
        outfile,
        garbage=4,
        clean=True,
        deflate_images=True,
        deflate_fonts=True,
        deflate=True
        )
    # print(100- (os.path.getsize(outfile)/os.path.getsize(infile) * 100))


def compress_image(infile, outfile=None):
    if not os.path.isfile(infile):
        raise FileNotFoundError("File name given does not exist")
    
    image = Image.open(infile)
    if has_transparency(image):
        ext = "png"
    else:
        ext = "jpeg"
    image.save(
        outfile,
        format=ext,
        optimize=True,
        quality=25
        )

def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    
    if img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False
