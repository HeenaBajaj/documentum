from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_watermark(content,watermark,x):
    c = canvas.Canvas(watermark, pagesize = (612, 792))   
    # c.translate(10, 10) # Move the coordinate origin (the lower left of the coordinate system is (0,0)))                                                                                                                             
    c.setFont('Helvetica',60)#Set the font to Song, size 22
    c.setFillColorRGB(0.5,0.5,0.5)#gray                                                                                                                         
    c.rotate(45)# rotates 45 degrees, the coordinate system is rotated
    a = (x.getLowerLeft_x() + x.getLowerRight_x())/2
    b = (x.getLowerLeft_y()+x.getLowerRight_y())/2
    c.drawString(a,b, content)
    c.save()#Close and save the pdf file

def apply_watermark(watermarktxt,input_pdf):
    
    filename = os.path.basename(input_pdf)  #original File name
    # os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_pdf =os.path.expanduser("~/Desktop")+ '/'+ filename
    from shutil import copyfile
    copyfile(input_pdf, output_pdf)

    # watermark_pdf = r'C:\Users\A118090\OneDrive - AXAXL\Desktop\hello_django\PyQT\Izoe\CADocumentum\watermark.pdf'

    with open(os.path.join(BASE_DIR, "watermark.pdf"), 'w') as fp:
        print("Created watermark")

    watermark_pdf = BASE_DIR + "\\"+ "watermark.pdf"
    
    # create_watermark("DOCUMENTUM",watermark_pdf)
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open(input_pdf,"rb"))

    page_count = input_file.getNumPages()
    output_pdf = open(output_pdf, "wb")

    create_watermark(watermarktxt,watermark_pdf,input_file.getPage(0).mediaBox)

    watermark = PdfFileReader(open(watermark_pdf, "rb"))

    for page_number in range(page_count):
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        output_file.addPage(input_page)
        output_file.write(output_pdf)
