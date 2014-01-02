# Map-Reduce
# Web Intelligence and Big Data Homework 3
#
# Start this script:
# $ python wordcount.py
#
# Then in the separate shell start server:
# $ python mincemeat.py -p changeme localhost
#
# Both wordcount.py and mincemeat.py should be in the same directory.

import mincemeat
from operator import itemgetter
from optparse import OptionParser

def file_contents(filename):
    f = open(filename)
    try:
        return f.read()
    finally:
        f.close()


def mapfn(key, value):
    import re
    from stopwords import allStopWords

    lines = dict((l.strip().split(':::')[1:] for l in value.splitlines()))
    for authors, title in lines.iteritems():

        # Get rid of stopwords and non-alphanumeric symbols.
        title = [t for t in re.sub('\W+|\s+', ' ', title).lower().split(' ')
                 if (t not in allStopWords) and (len(t) > 1)]

        for w in title:
            # There can be more than 1 author.
            for a in authors.split('::'):
                yield (w, a), 1


def reducefn(key, value):
    return key, len(value)


def main(src_dir):
    import glob

    # Prepare data from files.
    src_dir = glob.glob(('%s/*' % src_dir).replace('//', '/'))
    filesource = dict((filename, file_contents(filename))
                      for filename in src_dir)

    # Map-reduce.
    s = mincemeat.Server()
    s.datasource = filesource
    s.mapfn = mapfn
    s.reducefn = reducefn
    results = s.run_server(password="changeme")

    # Processing results for better report.
    val = [(a[0], a[1], b) for a, b in results.values()]
    result = [(a, b, c) for a, b, c 
              in sorted(val, key=itemgetter(2, 0), reverse=True)]

    # Reposrt first 20 results
    for res in result[:20]:
        print '%-30s%-30s:%10d' % res


if __name__ == "__main__":
    cmdparser = OptionParser(usage="usage: python %prog /path/to/text/files/")
    opts, args = cmdparser.parse_args()

    try:
        main(args[0])
    except IndexError as ie:
        print 'You must specify a directory!'
        exit()
