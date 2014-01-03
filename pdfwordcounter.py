# Start this script:
# $ python pdfwordcounter.py /path/to/pdf/files/
#
# Then in the separate shell start server:
# $ python mincemeat.py -p changeme localhost

import mincemeat

def file_content(filename):
    import PyPDF2 as pypdf

    content = ""
    pdf = pypdf.PdfFileReader(file(filename, "rb"))
    for i in range(0, pdf.getNumPages()):
        content += pdf.getPage(i).extractText().strip()

    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content


def mapfn(key, value):
    import re
    import stopwords

    # Get rid of stopwords, non-alphanumeric symbols,
    # numbers and lines too long to be words.
    words = [t for t in re.sub('\W+|\s+', ' ', value).lower().split(' ')
             if (t not in stopwords.allStopWords) and (not t.isdigit())
             and (len(t) > 1) and (len(t) < 30)]

    for word in words:
        yield (key, word), 1


def reducefn(key, value):
    return key, len(value)


def main(src_dir):
    import glob
    import operator

    # Prepare data from files.
    src_dir = glob.glob(('%s/*' % src_dir).replace('//', '/'))
    filesource = dict(
        (filename, file_content(filename).encode("ascii", "xmlcharrefreplace"))
        for filename in src_dir)

    # Map-reduce.
    s = mincemeat.Server()
    s.datasource = filesource
    s.mapfn = mapfn
    s.reducefn = reducefn
    results = s.run_server(password="changeme")

    # Processing results for better report.
    val = [(a[0].rsplit('/', 1)[-1], a[1], b) for a, b in results.values()]
    result = [(a, b, c) for a, b, c
              in sorted(val, key=operator.itemgetter(2, 0), reverse=True)]

    # Report first 100 results
    for res in result[:100]:
        print '%-50s%-30s:%10d' % res


if __name__ == "__main__":
    import optparse

    cmdparser = optparse.OptionParser(
        usage="usage: python %prog /path/to/pdf/files/")
    opts, args = cmdparser.parse_args()

    try:
        main(args[0])
    except IndexError as ie:
        print 'You must specify a directory!'
        exit()
