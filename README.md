# Virologist's Toolkit
Contains helpful tools for very specific use scenarios. Many
of the scripts are develop-on-demand with multiple attempts to abstract-away
commonalities e.g. input/output file formats, to make the scripts as flexible
as possible.  However, no guarantees can be made about what cases they address
except for the user to examine the process of the scripts and determine for
themselves whether it is applicable.

## FASTA File Renamer

It takes a FASTA file with the format:

>{ ANY CHARS }|{ ANY CHARS }|{...accession #2...}.{ Single 0-9 }|
{...Virus Name... virus/Virus} {...Other...}\cr
{...Sequence...}\cr

...and transforms it into:
>{...accession #2...}_{...Virus Name...}\cr
{...Sequence...}\cr

**Assumptions/Notes:**
 * {...Virus Name...} always ends with the word, "virus".
 * Uses underscore to replace all spaces in the header line.
