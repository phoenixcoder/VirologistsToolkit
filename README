# FASTA File Renamer

It takes a FASTA file with the format:

>gi|{...accession #1...}|gb|{...accession #2...}.1| {...Virus Name...} {...Other...}\cr
{...Sequence...}\cr

...and transforms it into:
>{...accession #2...}_{...Virus Name...}\cr
{...Sequence...}\cr

**Assumptions/Notes:**
 * {...Virus Name...} always ends with the word, "virus".
 * Uses underscore to replace all spaces in the header line.
