# Helper Scripts for VEP 2

These are some simple Python Scripts that I have written in the process
of trying to bring the VEP project up to date.

These are for my personal use, but are made public for transparency.

## The tools...

1. `dircheck.py` - a tool for checking a directory against the metadata.
    also allows checking ZIP files. Good for seeing that a directory is
    complete and doesn't have extra files.
2. `ngram.py` - a simple tool for counting words and writing out CSVs of
    the top N. This is mainly written as an example of how easy it is
    to load a corpus of SimpleText files.
3. EEBO_BIB - convert from the EEBO bib I found on the web as XML to a
    more useful CSV file. While the source of this file is unofficial, it
    seems a lot more complete than anything else I've seen.

## GENERAL NOTES

The source Data files generally go into the "Data Directory".
Since I am not sure about licensing, I will not include them in the repo.

## Notes on Specific Tools

### EEBO_BIB

Getting information about EEBO is a bit of a pain.

The official version of the metadata from ProQuest 
https://www.proquest.com/go/tls-eebo
gives a corrupted xlsx file that Excel cannot repair.
*Update - they did fix it! But there it doesn't have TCP info*.

This GitHub Repo: https://github.com/lb42/eebo-bib has a good explanation.
It has tools that would be useful for format conversion.

Instead, I took the processed version (I did not run the scripts) since:

1. Getting the raw data seems intractable
2. It requires using XSLT tools, which always seemed tricky
3. I was lazy

So, I got the file from https://app.box.com/s/3p6ft7xebsrp6rd6jv0lzde19tx28en5
as suggested on the GitHub repo. I am using `tls-eebo-2021-plus.xml`.
It should be in the `Data` subdirectory.

It is a well formatted XML file. However, since I wanted to get it into a form
that MetaDataBuilder could process, I wrote a tool to convert it to CSV.

Some records have multiple TCP entries - I am not sure what is up with that.
The script (arbitrarily) takes the last one. It does report this.

This is handy for the **EEBO** files (not the other parts of TCP), since we 
can connect from TCP numbers back to Proquest (to get page images), and to 
get a sense of what newer EEBO files there might be.
