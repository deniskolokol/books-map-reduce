Books and authors map-reduce
================

Map-Reduce over books, authors and publishers. Coursera, Web Intelligence and Big Data, HW3

Prerequisites:

mincemeat https://github.com/michaelfairley/mincemeatpy

PyPDF2 https://github.com/mstamy2/PyPDF2 (for PDF word counter only)

Start this script:

      $ python wordcount.py

For PDF:

      $ python pdfwordcounter.py /path/to/the/folder/with/pdf/files/

Then in the separate shell start server:

     $ python mincemeat.py -p changeme localhost


WARNING!

Both wordcount.py (or pdfwordcounter.py) and mincemeat.py should be in the same directory.

It takes around 2 minutes on average i5 to perform full cycle for wordcount.py!

pdfwordcounter.py may take more time, depending on the amount of information on the PDFs.