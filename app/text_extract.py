import sys
import base64

from commons import log


def extract_multipart_text(source_file):
    content_start = "Content-Type: text/plain"
    encoding_base64 = "Content-Transfer-Encoding: base64"
    content_found = False
    encoding_found = False
    newline_found = False
    content = []
    with open(source_file, 'r') as f:
        for line in f:
            if encoding_found and content_found:
                l = line.strip()
                empty_line = not len(l)
                if newline_found and empty_line:
                    break

                if empty_line:
                    newline_found = True
                else:
                    content.append(l)

            if content_start in line:
                content_found = True
                encoding = extract_encoding(line)

            if encoding_base64 in line:
                encoding_found = True

    payload = "".join(content)
    return base64.b64decode(payload).decode(encoding) if content else ''


def extract_encoding(line):
    try:
        encoding = line.strip().split('=')[1].replace('"', '')
    except Exception:
        # use default encoding, exception swallowed on purpose
        encoding = 'utf-8'
    return encoding


if __name__ == '__main__':
    source_file = sys.argv[1]
    dest_file = source_file.replace('.eml', '.txt')
    content = extract_multipart_text(source_file)
    if content:
        with open(dest_file, 'w') as f:
            f.write(content)
        log.info("Text content saved to: %s" % dest_file)
    else:
        log.info("No text content found in: %s" % dest_file)

