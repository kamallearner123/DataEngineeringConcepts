# from current directory go through all subdirectories and find all .html files
# To PDF file, add each subdirectory as new chapter and convert all html files and add them to the chapter
import os
import pdfkit
from pathlib import Path
from PyPDF2 import PdfMerger
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter

def convert_html_to_pdf(input_dir, output_pdf):
    print(f"Converting HTML files in {input_dir} to PDF...")

    # Create a list to store the paths of the HTML files
    html_files = []

    # Walk through the directory and find all HTML files
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    # Create a PDF merger object
    merger = PdfMerger()

    # Convert each HTML file to PDF and add it to the merger
    for html_file in html_files:
        pdf_file = html_file.replace('.html', '.pdf')
        pdfkit.from_file(html_file, pdf_file)
        merger.append(pdf_file)

    # Write out the merged PDF
    merger.write(output_pdf)
    merger.close()

if __name__ == "__main__":
    input_directory = os.getcwd()
    output_pdf_file = os.path.join(os.getcwd(), 'output.pdf')

    convert_html_to_pdf(input_directory, output_pdf_file)
    print(f"PDF generated successfully: {output_pdf_file}")
