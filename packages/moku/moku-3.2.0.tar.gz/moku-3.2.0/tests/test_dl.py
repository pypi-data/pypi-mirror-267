import re


def parse_byte_range(byte_range, file_size):
    """
        bytes=1024-2048 : offset 1024, return next 2048 bytes
        bytes=-2048 : return last 2048 bytes
        bytes=2048- : return first 2048 bytes
    """
    pattern = re.match(r'bytes=(\d*)-(\d*)', byte_range)
    if pattern:
        start = int(pattern.group(1)) if pattern.group(1) else None
        end = int(pattern.group(2)) if pattern.group(2) else None

        if None not in [start, end]:
            if start < end <= file_size:
                return start, end
        elif start is not None and start <= file_size:
            return 0, start
        elif end is not None and end <= file_size:
            return file_size - end, file_size

    raise Exception("Range Not Satisfiable")


parse_byte_range("bytes=1-100", 1000)
