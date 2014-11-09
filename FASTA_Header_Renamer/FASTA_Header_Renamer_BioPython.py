'''FASTA Renamer BioPython uses BioPython to Process Files

Goes through each sequence and retrieves an accession number and header based
on the regular expression defined below.  It reorganizes it to remove all
spaces from the header line and format it to be in the
{accession number}_{name of virus} form.

If additional modifications are required for this use-case, it is unlikely this
script will be modified as it runs slower for large datasets.  Please see
FASTA_Renamer_Python module found in this same package.
'''

from Bio import SeqIO
from sys import stdout
import textwrap
import re

# Configuration
input_path = "data/BegomoSDTseqsmissing.fasta"
output_path = "data/BegomoSDTseqsmissing_OUTPUT.fasta"
virus_name_pattern = "^.+\|.+\|.+\|.+\|(.*[vV]irus).*"

input_handle = open(input_path, "rU")
output_handle = open(output_path, "w")
virus_name_prog = re.compile(virus_name_pattern)
virus_errors = []

print("\n=========================================")
print("FASTA Renamer BioPython")
print("=========================================")

virusCtr = 0
virusErr = 0
for record in SeqIO.parse(input_handle, "fasta"):
    # {...accession #2...}.1|
    virusAccession2 = record.id.split("|")[3].split(".")[0]
    virusDescription = record.description
    virusNameMatch = re.match(virus_name_prog, virusDescription)

    stdout.write("Number of Viruses Processed: {0}, Number of Errors: {1}\r"
        .format(virusCtr, virusErr))
    stdout.flush()
    if virusNameMatch:
         virusCtr = virusCtr + 1
         virusName = virusNameMatch.groups(1)[0].replace(" ", "_")
         # Wrapping causes the function to go into O(m^2) time since it is now
         # traversing each line, counting the characters up to 80.  This slows
         # down the running of this program.
         virusSeq = textwrap.fill(str(record.seq), 80)
         virusFormat = ">" + virusAccession2 + virusName + "\n" \
            + virusSeq + "\n"
         output_handle.write(virusFormat)
    else:
        virus_errors.append(virusDescription)
        virusErr = virusErr + 1 
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

print("Output written to: " + output_path)
print("\nGoodbye! The Momo loves you!")
