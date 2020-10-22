import sys, os
''' Image generation required modules ''' 
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
''' PDF generation required modules '''
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import io
''' Import config file '''
from config import *
''' Import required functions. '''
from functions import get_random_string
''' Time Initialistaion '''
startTime = datetime.now()
print('Generation started at {}'.format(startTime))

''' Generate ID '''
ID = get_random_string(20)

''' Handling input variables '''
student_name = sys.argv[1].replace("_"," ") # Student name, input with '_'
course_name = sys.argv[2].replace("_"," ") # Course name, input with '_'
issue_date = sys.argv[3].replace("_"," ") # Issue date, Format: Month DD, YYYY

''' Open Certification file + convert it for later manipulation. '''
certification = Image.open('template.jpg')

''' Load fonts for later usage '''
DATE_FONT = ImageFont.truetype(LUCIDA_GRANDE_LOCATION, DATE_SIZE)
ID_FONT = ImageFont.truetype(LUCIDA_GRANDE_LOCATION, ID_SIZE)
STUDENT_NAME_FONT = ImageFont.truetype(DANCING_SCRIPT_LOCATION, STUDENT_NAME_SIZE)
COURSE_NAME_FONT = ImageFont.truetype(FUTURA_LOCATION, COURSE_NAME_SIZE)
pdfmetrics.registerFont(TTFont('DancingScript', DANCING_SCRIPT_LOCATION))
pdfmetrics.registerFont(TTFont('Futura', FUTURA_LOCATION))
pdfmetrics.registerFont(TTFont('LucidaGrande', LUCIDA_GRANDE_LOCATION))

''' Image generation '''
''' Draw texts on Certification '''
draw = ImageDraw.Draw(certification)
''' Student name '''
draw.text(STUDENT_NAME_LOCATION, student_name, font=STUDENT_NAME_FONT, fill=STUDENT_NAME_COLOR[0])
''' Course name '''
draw.text(COURSE_NAME_LOCATION, course_name, font=COURSE_NAME_FONT, fill=COURSE_NAME_COLOR[0])
''' Issue Date '''
draw.text(DATE_LOCATION, issue_date, font=DATE_FONT, fill=DATE_ID_COLOR[0])
''' ID '''
draw.text(ID_LOCATION, ID, font=ID_FONT, fill=DATE_ID_COLOR[0])
''' Finally save the image as JPEG '''
certification.save('Generated/' + ID + '.jpg', "JPEG", quality=100)
''' Image generation finished execution '''
print("Image Generation completed for id '{}', took {}".format(ID,datetime.now() - startTime))
startTime = datetime.now()


''' PDF generation '''
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)

''' Student name '''
can.setFillColor(HexColor(STUDENT_NAME_COLOR[1]))
can.setFont('DancingScript', 100)
can.drawString(180, 680, student_name)
''' Course name '''
can.setFillColor(HexColor(COURSE_NAME_COLOR[1]))
can.setFont('Futura', 72)
can.drawString(185, 465, course_name)
''' Issue Date '''
can.setFillColor(HexColor(DATE_ID_COLOR[1]))
can.setFont('LucidaGrande', 26)
can.drawString(430, 176, issue_date)
''' ID '''
can.setFont('LucidaGrande', 22)
can.drawString(342, 140, ID)
''' Finally save the certificate as PDF '''
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("template.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("Generated/"+ID+".pdf", "wb")
output.write(outputStream)
outputStream.close()
''' Image generation finished execution '''
print("PDF Generation completed for id '{}', took {}".format(ID,datetime.now() - startTime))