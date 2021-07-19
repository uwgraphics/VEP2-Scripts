# Helper Scripts fr VEP 2

These are some simple Python Scripts that I have written in the process
of trying to bring the VEP project up to date.

These are for my personal use, but are made public for transparency.

## GENERAL NOTES

The source Data files generally go into the "Data Directory".
Since I am not sure about licensing, I will not include them in the repo,
but the README should say where I got them from, and this file should
explain why.

## EEBO_BIB

Getting information about EEBO is a bit of a pain.

The official version of the metadata from ProQuest 
https://www.proquest.com/go/tls-eebo
gives a corrupted xlsx file that Excel cannot repair.

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

