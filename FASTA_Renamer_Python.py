'''FASTA Renamer Python uses vanilla Python2/3 to Process Files

Performs the same operations as the module, FASTA_Renamer_BioPython:

Goes through each sequence and retrieves an accession number and header based
on the regular expression defined below.  It reorganizes it to remove all
spaces from the header line and format it to be in the
{accession number}_{name of virus} form.

The difference is this operation avoids using the BioPython module and sticks to
Python's FileIO operations to identify the important components of the FASTA
file; this is done primarily through regular expressions rather than
BioPython's SeqIO data structures.

This version is generally faster since it performs operations line-by-line
rather reading in the entirety of a single sequence unit e.g. header,
description, and sequence text into a data structure before processing.  The
primary problem is text retrieved via BioPython's SeqRecord comes unformatted
requiring the main program to reformat it back to its original form.  More
specifically, the length of the line ends up exceeding the 120 character
recommended limit for FASTA format.  This makes the Big-O analysis a function
of the number of letters in each sequence rather than of the lines in the file.

This process runs in O(n) versus the BioPython version of O(m^2) where n is the
number of lines in the file and m is the total number of sequence characters
in the file with the assumption, m > n.
'''

from sys import stdout
import re

# Configuration
# TODO Query user for Input and Output paths
input_path = "data/BegomoSDTseqsmissing.fasta"
output_path = "data/BegomoSDTseqsmissing_OUTPUT.fasta"
name_pattern = "^>.+\|.+\|.+\|(.+)[.0-9]\|(.*[vV]irus).*"
alpha = "^[NATCG\-\n]+$"
replace_target = " "
replace_char = "_"

input_handle = open(input_path, "rU")
output_handle = open(output_path, "w")
name_prog = re.compile(name_pattern)
alpha_prog = re.compile(alpha)
virus_errors = []

print("\n=========================================")
print("FASTA Renamer BioPython")
print("=========================================")

ctr = 0
err = 0
valid = False
for line in input_handle:
    stdout.write("Number of Viruses Processed: {0}, Number of Errors: {1}\r"
        .format(ctr, err))
    stdout.flush()
    nameMatch = re.match(name_prog, line)
    seqMatch = re.match(alpha_prog, line)
    if seqMatch and valid:
        output_handle.write(line)
    elif nameMatch:
        ctr = ctr + 1
        valid = True
        groups = nameMatch.group(1, 2)
        virusAccession2 = groups[0].replace(replace_target, replace_char)
        virusName = groups[1].replace(replace_target, replace_char)
        output_handle.write(">" + virusAccession2 + virusName + "\n")
    elif not seqMatch:
        err = err + 1
        valid = False
        virus_errors.append(line.rstrip())

output_handle.close()
input_handle.close()

# Print Virus Sequences that had errors.
print("\n\n=========================================")
if virus_errors:
    print("Error extracting information for viruses:")
    for virusErr in virus_errors:
        print(virusErr)
else:
    print("\nAll sequences successfully processed!")
print("=========================================")

# Departure information
print("Output written to: " + output_path)
print("\nGoodbye! The Momo loves you!")
