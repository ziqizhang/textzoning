# import parser object from tike
import tika
from tika import parser
import sys

if __name__ == "__main__":
    #tika runs on java. it must init jvm first
    #also you need to make sure you install java 8+ and it is configured on your computer
    tika.initVM()

    # opening pdf file
    f1="/home/zz/Work/vamstar/textzoning/input/test_docs/Pliego de Cláusulas Administrativas Particulares-2020 02104 PCAP.pdf"
    # this one needs ocr:
    f2="/home/zz/Work/vamstar/textzoning/input/test_docs/дансон.pdf"
    #infile=sys.argv[1]
    infile=f2
    parsed_pdf = parser.from_file(infile)

    # saving content of pdf
    # you can also bring text only, by parsed_pdf['text']
    # parsed_pdf['content'] returns string
    data = parsed_pdf['content']

    # Printing of content
    print(data)

    # <class 'str'>
    print(type(data))