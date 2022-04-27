from pathlib import Path

from facturx import *
import pathlib
import os
from os.path import isfile, join

import PyPDF4

current_directory = str(pathlib.Path(__file__).parent.resolve())
rep = current_directory + '/anciens_fichiers_pdf/'

def extract_xml(reader):
    """
    Retrieves the file attachments of the PDF as a dictionary of file names
    and the file data as a bytestring.
    :return: dictionary of filenames and bytestrings
    """

    handler = open('/home/agardille/Correction_XMLs/FCLI009060_N° 64603.pdf', 'rb')
    reader = PyPDF4.PdfFileReader(handler)

    catalog = reader.trailer["/Root"]
    fileNames = catalog['/Names']['/EmbeddedFiles']['/Names']
    attachments = {}
    for f in fileNames:
        if isinstance(f, str):
            name = f
            dataIndex = fileNames.index(f) + 1
            fDict = fileNames[dataIndex].getObject()
            fData = fDict['/EF']['/F'].getData()
            attachments[name] = fData

    for fName, fData in attachments.items():
        with open('exctracted.xml', 'wb') as outfile:
            outfile.write(fData)


def extractXML_old(pdf_filename, out_xml_filename='exctracted.xml', disable_xsd_check=True):

    if not isfile(pdf_filename):
        raise Exception('Argument %s is not a filename', pdf_filename)

    pdf_file = open(pdf_filename, 'rb')
    check_xsd = True
    if disable_xsd_check:
        check_xsd = False
    # The important line of code is below !
    
    (xml_filename, xml_string) = get_xml_from_pdf(pdf_file, check_xsd=check_xsd)
    #(xml_filename, xml_string) = get_facturx_xml_from_pdf(pdf_file, check_xsd=check_xsd)
    
    
    if xml_filename and xml_string:
        if isfile(out_xml_filename):
            print('File %s already exists. Overwriting it!', out_xml_filename)
        xml_file = open(out_xml_filename, 'wb')
        xml_file.write(xml_string)
        xml_file.close()
        print('File %s generated', out_xml_filename)
    else:
        raise Exception('File %s has not been created', out_xml_filename)

def checkXML(xml_file):


    if not isfile(xml_file):
        raise Exception('%s is not a filename', xml_file)
    xml_file = open(xml_file, 'rb')
    # The important line of code is below !

    xml_check_xsd(xml_file, flavor='autodetect', level='autodetect')

def createPDF(pdf_filename, xml_filename, output_pdf_filename, overwrite=True, disable_xsd_check=False, additional_attachment_filenames=[]):

    for filename in [pdf_filename, xml_filename] + additional_attachment_filenames:
        if not isfile(filename):
            raise Exception('Argument %s is not a filename', filename)

    xml_file = open(xml_filename, 'rb')
    check_xsd = True
    if disable_xsd_check:
        check_xsd = False
    pdf_metadata = None

    if isfile(output_pdf_filename):
        if overwrite:
            print('File %s already exists. Overwriting it.',
                output_pdf_filename)
        else:
            print('File %s already exists. Exit.', output_pdf_filename)

    # The important line of code is below !
    generate_from_file(
        pdf_filename, xml_file, check_xsd=check_xsd,
        pdf_metadata=pdf_metadata, output_pdf_file=output_pdf_filename)


def correctXML(xml_filename):
    with open(xml_filename, 'r') as bdata:
        data = bdata.read()
        
        data = data.replace('\n', '').replace('\r', '').replace('\t', '')
        

        parts = data.split('ram:ID schemeID=')
        l = len(parts)
        [id_prec, num_prec] = ["", ""]
        reste_prec = []
        
        for i in range(1, l-1):
            [id, num] = parts[i].split('>')[:2]
            reste = parts[i].split('>')[2:]
    
            if id == id_prec:
                L = [id_prec, num_prec[:9]+num_prec[14:]]
                L.extend(reste)
                parts[i] = ">".join(L)

            [id_prec, num_prec] = [id, num]
            reste_prec = reste
        
        
        newData = 'ram:ID schemeID='.join(parts)
        

        path_xml = current_directory + '/corrected.xml'
        
        f = open(path_xml,"w",encoding="utf-8")
        f.write(newData)
        f.close()
        

try:
    fichiers = [f for f in os.listdir(rep) if isfile(join(rep, f))]
except:
    os.mkdir(rep)
    fichiers = [f for f in os.listdir(rep) if isfile(join(rep, f))]

if not os.path.isdir(current_directory + '/nouveaux_fichiers_pdf/'):
    os.mkdir(current_directory + '/nouveaux_fichiers_pdf/')



print('fichiers: ', fichiers)
for fichier in fichiers:
    print(fichier)
    if fichier[-3:] != "pdf":
        continue
    path = current_directory + '/anciens_fichiers_pdf/' + fichier
    extract_xml(path)
    #extractXML(path)
    checkXML('exctracted.xml')
    correctXML('exctracted.xml')
    path_new_pdf = current_directory + '/nouveaux_fichiers_pdf/' + fichier 

    createPDF(path, 'corrected.xml', path_new_pdf)

    os.remove("exctracted.xml") 
    os.remove("corrected.xml") 



