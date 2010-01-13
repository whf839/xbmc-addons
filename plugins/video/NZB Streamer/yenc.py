import string
import sre
from zlib import crc32

decode_table = string.join(map(lambda x: chr((x-42) & 255), range(256)), "")
decode_escape_table = string.join(map(lambda x: chr((x-106) & 255), range(256)), "")

##
# Decode a YENC-encoded message into a list of string fragments.
# Returns None if no YENC body was found.

# =ybegin part=1 line=128 size=500000 name=mybinary.dat
# =ypart begin=1 end=100000
# .... data
# =yend size=100000 part=1 pcrc32=abcdef12

def yenc_decode(encoded_lines):

    # check for start tag
    first_line = 0
    for line in encoded_lines:
        if line[:7] == "=ybegin":
            break;
        first_line += 1

    if first_line == len(encoded_lines):
        raise Exception("ybegin line not found")

    file_size = None

    # =ybegin part=2 total=66 line=128 size=50000000
    ybegin_match = sre.search("size=(\d+)", encoded_lines[first_line][7:])
    if ybegin_match == None:
        raise Exception("ybegin line is malformed")
    else:
        file_size = int(ybegin_match.group(1))

    decoded_buffer = ""
    part_number = None
    part_begin = None
    part_end = None
    part_size = None
    for line in encoded_lines[first_line+1:]:

        if line[:6] == "=ypart":
            ypart_match = sre.search("begin=(\d+) end=(\d+)", line[6:])
            if ypart_match == None:
                raise Exception("ypart line is malformed")
            else:
                part_begin = int(ypart_match.group(1))
                part_end = int(ypart_match.group(2))
            continue

        elif line[:5] == "=yend":
            yend_match = sre.search("size=(\d+) part=(\d+) pcrc32=([0-9a-zA-Z]{8})", line[5:])
            if yend_match == None:
                raise Exception("yend line is malformed")
            else:
                part_size = int(yend_match.group(1))
                part_number = int(yend_match.group(2))
                pcrc32 = int(yend_match.group(3), 16)
                if (crc32(decoded_buffer) & 0xffffffff) != pcrc32:
                    raise Exception("CRC32 checksum failed", crc32(decoded_buffer) & 0xffffffff, pcrc32)
            break

        i = 0
        end = len(line)
        while i < end:
            byte = line[i]

            # end of line
            if byte in "\r\n":
                break;

            # escape byte
            if byte == '=':
                i += 1
                decoded_buffer += decode_escape_table[ord(line[i])]

            # normal byte
            else:
                decoded_buffer += decode_table[ord(byte)]

            i += 1

    if part_size != None and part_size != len(decoded_buffer):
        print "Warning: yend size attribute does not equal buffer length"

    return decoded_buffer, part_number, part_begin, part_end, file_size


# unit test an NFO file

encoded_nfo= ['=ybegin part=1 line=128 size=3554 name=Fringe S01E07 X264 720p 2Audio (2009-12-06).nfo',
              '=ypart begin=1 end=3554',
              'q\x8f\x98\x8f\x9c\x8b\x9674m\x99\x97\x9a\x96\x8f\x9e\x8fJ\x98\x8b\x97\x8fJJJJJJJJJJJJJJJJJJJJdJp\x9c\x93\x98\x91\x8fJ}Z[oZaJ\x82\\`^Ja\\Z\x9aJ\\k\x9f\x8e\x93\x99JR\\ZZcW[\\WZ`SX\x97\x95\xa074p\x99\x9c\x97\x8b\x9eJJJJJJJJJJJJJJJJJJJJJJJJJJJdJ',
              'w\x8b\x9e\x9c\x99\x9d\x95\x8b74p\x93\x96\x8fJ\x9d\x93\xa4\x8fJJJJJJJJJJJJJJJJJJJJJJJJdJ[XZcJq\x93l74n\x9f\x9c\x8b\x9e\x93\x99\x98JJJJJJJJJJJJJJJJJJJJJJJJJdJ^a\x97\x98J\\\x9d74y\xa0\x8f\x9c\x8b\x96\x96J\x8c\x93\x9eJ\x9c\x8b\x9e\x8fJJJJJJJJJJJJJ',
              'JJJJdJ]J][]Ju\x8c\x9a\x9d74w\x99\xa0\x93\x8fJ\x98\x8b\x97\x8fJJJJJJJJJJJJJJJJJJJJJJJdJ\x92\x9e\x9e\x9adYY\x92\x95\x8f\x98\x91\x9d\x8f\x9c\x93\x8f\x9dX\x8c\x96\x99\x91\x8c\x9f\x9dX\x8d\x99\x97Y74o\x98\x8d\x99\x8e\x8f\x8eJ\x8e\x8b\x9e\x8fJJJJJJJJJJJJJJJJJJJJJdJ\x7f~mJ\\ZZ',
              'cW[\\WZaJZ^d\\^d^]74\x81\x9c\x93\x9e\x93\x98\x91J\x8b\x9a\x9a\x96\x93\x8d\x8b\x9e\x93\x99\x98JJJJJJJJJJJJJJdJ\x97\x95\xa0\x97\x8f\x9c\x91\x8fJ\xa0\\XbXZJRQ~\x92\x8fJ~\x9c\x8f\x8fQSJ\x8c\x9f\x93\x96\x9eJ\x99\x98Jw\x8b\xa3JJcJ\\ZZcJ[bdZ\\dZ`74\x81\x9c\x93\x9e\x93\x98\x91J\x96\x93\x8c\x9c\x8b\x9c\xa3',
              'JJJJJJJJJJJJJJJJJJdJ\x96\x93\x8c\x8f\x8c\x97\x96J\xa0ZXaXaJUJ\x96\x93\x8c\x97\x8b\x9e\x9c\x99\x9d\x95\x8bJ\xa0ZXbX[7474\x80\x93\x8e\x8f\x9974snJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJdJ[74p\x99\x9c\x97\x8b\x9eJJJJJJJJJJJJJJJJJJ',
              'JJJJJJJJJdJk\x80m74p\x99\x9c\x97\x8b\x9eYs\x98\x90\x99JJJJJJJJJJJJJJJJJJJJJJdJk\x8e\xa0\x8b\x98\x8d\x8f\x8eJ\x80\x93\x8e\x8f\x99Jm\x99\x8e\x8f\x8d74p\x99\x9c\x97\x8b\x9eJ\x9a\x9c\x99\x90\x93\x96\x8fJJJJJJJJJJJJJJJJJJJdJr\x93\x91\x92jv^XZ74p\x99\x9c\x97\x8b\x9eJ\x9d\x8f',
              '\x9e\x9e\x93\x98\x91\x9dVJmklkmJJJJJJJJJJJdJ\x83\x8f\x9d74p\x99\x9c\x97\x8b\x9eJ\x9d\x8f\x9e\x9e\x93\x98\x91\x9dVJ|\x8fp\x9c\x8b\x97\x8f\x9dJJJJJJJJdJ]J\x90\x9c\x8b\x97\x8f\x9d74w\x9f\xa2\x93\x98\x91J\x97\x99\x8e\x8fJJJJJJJJJJJJJJJJJJJJJJdJm\x99\x98\x9e\x8b\x93\x98\x8f\x9cJ\x9a\x9c\x99\x90\x93\x96\x8f',
              'g\x7f\x98\x95\x98\x99\xa1\x98j^XZ74m\x99\x8e\x8f\x8dJsnJJJJJJJJJJJJJJJJJJJJJJJJJdJ\x80\x89wzoq^Ys}yYk\x80m74n\x9f\x9c\x8b\x9e\x93\x99\x98JJJJJJJJJJJJJJJJJJJJJJJJJdJ^a\x97\x98J\\\x9d74l\x93\x9eJ\x9c\x8b\x9e\x8fJJJJJJJJJJ',
              'JJJJJJJJJJJJJJJdJ\\J`a[Ju\x8c\x9a\x9d74x\x99\x97\x93\x98\x8b\x96J\x8c\x93\x9eJ\x9c\x8b\x9e\x8fJJJJJJJJJJJJJJJJJdJ\\Ja]ZJu\x8c\x9a\x9d74\x81\x93\x8e\x9e\x92JJJJJJJJJJJJJJJJJJJJJJJJJJJJdJ[J\\bZJ\x9a\x93\xa2\x8f\x96\x9d74r\x8f\x93',
              '\x91\x92\x9eJJJJJJJJJJJJJJJJJJJJJJJJJJJdJa\\ZJ\x9a\x93\xa2\x8f\x96\x9d74n\x93\x9d\x9a\x96\x8b\xa3J\x8b\x9d\x9a\x8f\x8d\x9eJ\x9c\x8b\x9e\x93\x99JJJJJJJJJJJJJdJ[`dc74p\x9c\x8b\x97\x8fJ\x9c\x8b\x9e\x8fJJJJJJJJJJJJJJJJJJJJJJJdJ\\_XZZZJ\x90',
              '\x9a\x9d74|\x8f\x9d\x99\x96\x9f\x9e\x93\x99\x98JJJJJJJJJJJJJJJJJJJJJJJdJ\\^J\x8c\x93\x9e\x9d74m\x99\x96\x99\x9c\x93\x97\x8f\x9e\x9c\xa3JJJJJJJJJJJJJJJJJJJJJJdJ^d\\dZ74}\x8d\x8b\x98J\x9e\xa3\x9a\x8fJJJJJJJJJJJJJJJJJJJJJJJJdJz\x9c\x99',
              '\x91\x9c\x8f\x9d\x9d\x93\xa0\x8f74l\x93\x9e\x9dYRz\x93\xa2\x8f\x96Tp\x9c\x8b\x97\x8fSJJJJJJJJJJJJJJJdJZX[[`74}\x9e\x9c\x8f\x8b\x97J\x9d\x93\xa4\x8fJJJJJJJJJJJJJJJJJJJJJJdJbccJw\x93lJRb[OS74~\x93\x9e\x96\x8fJJJJJJJJJJJJJJJJJJJJJ',
              'JJJJJJJdJ~\x80lJrnJt\x8b\x8e\x8fJRr\x99\x98\x91Ju\x99\x98\x91SJ\xda\xd4\xdcw\xe5l\xe5k\xcf\xa274\x81\x9c\x93\x9e\x93\x98\x91J\x96\x93\x8c\x9c\x8b\x9c\xa3JJJJJJJJJJJJJJJJJJdJ\xa2\\`^J\x8d\x99\x9c\x8fJ``J\x9c[Zc\\J`Z\x90^\x8d\x8eb7474k\x9f\x8e\x93\x99JM[74snJJJJJJ',
              'JJJJJJJJJJJJJJJJJJJJJJJJJdJ\\74p\x99\x9c\x97\x8b\x9eJJJJJJJJJJJJJJJJJJJJJJJJJJJdJkmW]74p\x99\x9c\x97\x8b\x9eYs\x98\x90\x99JJJJJJJJJJJJJJJJJJJJJJdJk\x9f\x8e\x93\x99Jm\x99\x8e\x93\x98\x91J]74m\x99\x8e\x8f\x8dJ',
              'snJJJJJJJJJJJJJJJJJJJJJJJJJdJk\x89km]74n\x9f\x9c\x8b\x9e\x93\x99\x98JJJJJJJJJJJJJJJJJJJJJJJJJdJ^a\x97\x98J\\\x9d74l\x93\x9eJ\x9c\x8b\x9e\x8fJ\x97\x99\x8e\x8fJJJJJJJJJJJJJJJJJJJJdJm\x99\x98\x9d\x9e\x8b\x98\x9e74l\x93\x9e',
              'J\x9c\x8b\x9e\x8fJJJJJJJJJJJJJJJJJJJJJJJJJdJ]b^Ju\x8c\x9a\x9d74m\x92\x8b\x98\x98\x8f\x96R\x9dSJJJJJJJJJJJJJJJJJJJJJJJdJ`J\x8d\x92\x8b\x98\x98\x8f\x96\x9d74m\x92\x8b\x98\x98\x8f\x96J\x9a\x99\x9d\x93\x9e\x93\x99\x98\x9dJJJJJJJJJJJJJJJJdJp\x9c\x99\x98',
              '\x9edJvJmJ|VJ}\x9f\x9c\x9c\x99\x9f\x98\x8edJvJ|VJvpo74}\x8b\x97\x9a\x96\x93\x98\x91J\x9c\x8b\x9e\x8fJJJJJJJJJJJJJJJJJJJJdJ^bXZJur\xa474}\x9e\x9c\x8f\x8b\x97J\x9d\x93\xa4\x8fJJJJJJJJJJJJJJJJJJJJJJdJ[\\cJw\x93lJR[\\OS74~\x93\x9e',
              '\x96\x8fJJJJJJJJJJJJJJJJJJJJJJJJJJJJdJo\x98\x91\x96\x93\x9d\x92J_X[Jn\x99\x96\x8c\xa3Jn\x93\x91\x93\x9e\x8b\x9674v\x8b\x98\x91\x9f\x8b\x91\x8fJJJJJJJJJJJJJJJJJJJJJJJJJdJo\x98\x91\x96\x93\x9d\x927474k\x9f\x8e\x93\x99JM\\74snJJJJJJJJJJJ',
              'JJJJJJJJJJJJJJJJJJJJdJ]74p\x99\x9c\x97\x8b\x9eJJJJJJJJJJJJJJJJJJJJJJJJJJJdJkmW]74p\x99\x9c\x97\x8b\x9eYs\x98\x90\x99JJJJJJJJJJJJJJJJJJJJJJdJk\x9f\x8e\x93\x99Jm\x99\x8e\x93\x98\x91J]74m\x99\x8e\x8f\x8dJsnJJJ',
              'JJJJJJJJJJJJJJJJJJJJJJdJk\x89km]74n\x9f\x9c\x8b\x9e\x93\x99\x98JJJJJJJJJJJJJJJJJJJJJJJJJdJ^a\x97\x98J\\\x9d74l\x93\x9eJ\x9c\x8b\x9e\x8fJ\x97\x99\x8e\x8fJJJJJJJJJJJJJJJJJJJJdJm\x99\x98\x9d\x9e\x8b\x98\x9e74l\x93\x9eJ\x9c\x8b\x9e\x8f',
              'JJJJJJJJJJJJJJJJJJJJJJJJJdJ[c\\Ju\x8c\x9a\x9d74m\x92\x8b\x98\x98\x8f\x96R\x9dSJJJJJJJJJJJJJJJJJJJJJJJdJ\\J\x8d\x92\x8b\x98\x98\x8f\x96\x9d74m\x92\x8b\x98\x98\x8f\x96J\x9a\x99\x9d\x93\x9e\x93\x99\x98\x9dJJJJJJJJJJJJJJJJdJvJ|74}\x8b\x97\x9a',
              '\x96\x93\x98\x91J\x9c\x8b\x9e\x8fJJJJJJJJJJJJJJJJJJJJdJ^bXZJur\xa474}\x9e\x9c\x8f\x8b\x97J\x9d\x93\xa4\x8fJJJJJJJJJJJJJJJJJJJJJJdJ`^X`Jw\x93lJR`OS74~\x93\x9e\x96\x8fJJJJJJJJJJJJJJJJJJJJJJJJJJJJdJm\x8b',
              '\x98\x9e\x99\x98\x8f\x9d\x8fJ\\XZJn\x99\x96\x8c\xa3Jn\x93\x91\x93\x9e\x8b\x9674v\x8b\x98\x91\x9f\x8b\x91\x8fJJJJJJJJJJJJJJJJJJJJJJJJJdJm\x92\x93\x98\x8f\x9d\x8f7474~\x8f\xa2\x9eJM[74snJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJdJ^74p\x99\x9c\x97\x8b\x9eJJ',
              'JJJJJJJJJJJJJJJJJJJJJJJJJdJ\x80\x99\x8c}\x9f\x8c74m\x99\x8e\x8f\x8dJsnJJJJJJJJJJJJJJJJJJJJJJJJJdJ}\x89\x80yl}\x7fl74m\x99\x8e\x8f\x8dJsnYs\x98\x90\x99JJJJJJJJJJJJJJJJJJJJdJ~\x92\x8fJ\x9d\x8b\x97\x8fJ\x9d\x9f\x8c\x9e',
              '\x93\x9e\x96\x8fJ\x90\x99\x9c\x97\x8b\x9eJ\x9f\x9d\x8f\x8eJ\x99\x98Jn\x80n\x9d74~\x93\x9e\x96\x8fJJJJJJJJJJJJJJJJJJJJJJJJJJJJdJm\x92\x93\x98\x8f\x9d\x8fJ~\x9c\x8b\x8e\x93\x9e\x93\x99\x98\x8b\x96J}\x9f\x8cz\x93\x8d\x9e\x9f\x9c\x8fJ\xeb\x8d\xef\x13\xce\xce\xce\x0f\xd0\x9c\xe3\x1f74v\x8b\x98\x91\x9f\x8b\x91\x8fJJJJJJJJJJJJJJ',
              'JJJJJJJJJJJdJm\x92\x93\x98\x8f\x9d\x8f7474~\x8f\xa2\x9eJM\\74snJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJdJ_74p\x99\x9c\x97\x8b\x9eJJJJJJJJJJJJJJJJJJJJJJJJJJJdJ\x80\x99\x8c}\x9f\x8c74m\x99\x8e\x8f\x8dJsnJJJJJJ',
              'JJJJJJJJJJJJJJJJJJJdJ}\x89\x80yl}\x7fl74m\x99\x8e\x8f\x8dJsnYs\x98\x90\x99JJJJJJJJJJJJJJJJJJJJdJ~\x92\x8fJ\x9d\x8b\x97\x8fJ\x9d\x9f\x8c\x9e\x93\x9e\x96\x8fJ\x90\x99\x9c\x97\x8b\x9eJ\x9f\x9d\x8f\x8eJ\x99\x98Jn\x80n\x9d74~\x93\x9e\x96\x8fJJJJJJJJJJJJJJJJJJ',
              'JJJJJJJJJJdJm\x92\x93\x98\x8f\x9d\x8fJ}\x93\x97\x9a\x96\x93\x90\x93\x8f\x8eJ}\x9f\x8cz\x93\x8d\x9e\x9f\x9c\x8fJ\xec\xdc\xef\x13\xce\xce\xce\x0f\xd0\x9c\xe3\x1f74v\x8b\x98\x91\x9f\x8b\x91\x8fJJJJJJJJJJJJJJJJJJJJJJJJJdJm\x92\x93\x98\x8f\x9d\x8f',
              '=yend size=3554 part=1 pcrc32=13fca903']
result = yenc_decode(encoded_nfo)
assert(result != None)
decoded_buffer, part_number, part_begin, part_end, file_size = result
assert(part_number == 1)
assert(part_begin == 1)
assert(part_end == 3554)
assert(file_size == 3554)

# add a newline before =ybegin to test first_line logic
encoded_nfo.insert(0, "")
result = yenc_decode(encoded_nfo)
assert(result != None)
decoded_buffer, part_number, part_begin, part_end, file_size = result
assert(part_number == 1)
assert(part_begin == 1)
assert(part_end == 3554)
assert(file_size == 3554)