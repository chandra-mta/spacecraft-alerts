# Licensed under a 3-clause BSD style license - see LICENSE
"""
Internal module for handling intermediate files storing spacecraft data,
and logging the status of alerting
"""
import core
from numpy.ma import masked
from astropy.table import Table

def _read(file):
    #: Read in entire text content to minimize I/O operation time
    with open(file) as f:
        content = f.read()
    return content

def _coerce(x):
    if isinstance(x,list):
        return [_coerce(_) for _ in x]
    elif isinstance(x,str):
        #: String parsing.
        x = x.strip()
        if x == '':
            return masked
        #: If numeric, convert
        try:
            return int(x)
        except ValueError:
            try:
                return float(x)
            except ValueError:
                return x
    else:
        return x
    
def _parse(content):
    raw_lines = [line for line in content.split("\n")]
    #: Headers are written with an additional tab character at the end.
    header = raw_lines[0].strip().split('\t')
    #: Cannot strip the actual data lines in case the final column value is empty string, meaning masked value.
    data = _coerce([line.split('\t') for line in raw_lines[2:] if line != ''])
    return header, data

def _format(header, data):
    column_number = len(header)
    #: Drop non-matching rows and log
    rows = []
    for idx, entry in enumerate(data):
        if len(entry) != column_number:
            #: TODO Insert logging for handling ill-written telemetry files
            raise Exception(f"{header}, {entry}, {idx}")
        row = {}
        for i,j in zip(header,entry):
            row[i] = j
        rows.append(row)
    return Table(rows=rows)

def read_telemetry_file(file):
    """
    Read the acorn-formatted telemetry file into an astropy table
    """
    content = _read(file)
    header, data = _parse(content)
    table = _format(header, data)
    return table