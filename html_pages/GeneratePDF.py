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

    toc = []

    # Walk through the directory and find all HTML files
    for root, dirs, files in os.walk(input_dir):
        Chapter = root.split("/")[-1]
        toc.append(Chapter)
        # Check if the directory is not empty
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                toc.append(file)
                # open same html file and add File name as header
                with open(file, 'r') as f:
                    content = f.read()
                # Add the file name as a header in the HTML content
                content = f"<h1>{file}</h1>" + content
                # Write the modified content back to the HTML file
                with open(file, 'w') as f:
                    f.write(content)


    html_files.sort()
    # Create a PDF merger object
    merger = PdfMerger()

    # Create a temporary HTML file for the table of contents
    toc_html = "<html><body><h1>Table of Contents</h1><ul>"
    for item in toc:
        toc_html += f"<li><a href='{item}.html'>{item}</a></li>"

    toc_html += "</ul></body></html>"

    toc_file = os.path.join(input_dir, 'toc.html')
    with open(toc_file, 'w') as f:
        f.write(toc_html)

    # Convert the table of contents HTML file to PDF and add it to the merger
    toc_pdf = toc_file.replace('.html', '.pdf')
    pdfkit.from_file(toc_file, toc_pdf)
    merger.append(toc_pdf)
    # remove the temporary TOC PDF file
    os.remove(toc_pdf)

    # Convert each HTML file to PDF and add it to the merger
    for html_file in html_files:
        pdf_file = html_file.replace('.html', '.pdf')
        pdfkit.from_file(html_file, pdf_file)
        merger.append(pdf_file)
        # remove the temporary PDF file
        os.remove(pdf_file)

    # Write out the merged PDF
    merger.write(output_pdf)
    merger.close()

if __name__ == "__main__":
    input_directory = os.getcwd()
    output_pdf_file = os.path.join(os.getcwd(), 'output.pdf')

    convert_html_to_pdf(input_directory, output_pdf_file)
    print(f"PDF generated successfully: {output_pdf_file}")
