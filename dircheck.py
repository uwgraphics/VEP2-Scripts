# check what files are in a directory (even if it is a ZIP)
# if you have a directory full of XML or CSV or TXT, it's hard to even count how many
# there are, never mind to see if you have "all" of them (and which set of "all" do
# you have)

# handle zips
import zipfile
# use glob to get file list
import glob
# pandas for dealing with metadata
import pandas
# need for getting names
import os
#provide a CLI
import argparse

# defaults are on my disk - mainly for testing
test_dir = "C:\\DigHum\\TCP\\CleanExtractedStandardized"
play_dir = "C:\\DigHum\\Plays\\emd1554_charCleanExtractedSt"

# the metada file to check
tcp_meta = "https://raw.githubusercontent.com/uwgraphics/VEP-corpora/master/tcp_ascii_standardized.csv"
drama_meta = "https://raw.githubusercontent.com/uwgraphics/VEP-corpora/master/vep_early_modern_drama_all_known_texts_master.csv"
eebo_meta = "https://raw.githubusercontent.com/uwgraphics/VEP-corpora/master/VEP2/tls-eebo-2021-plus.csv"

# get the list of files
def getPaths(dir, ext):
    if (ext[0]=="."):
        ext = ext[1:]
    return glob.glob(dir + "/**/*[.]" + ext, recursive=True)

c_tn = []
c_fn = []

# get a list of files, the meta data, and then match...
def check(*, dir=play_dir, ext=".txt", meta=drama_meta, downcase=False, suffix=False,
          rows_to_show=5, writefile=False):
    global c_tn,c_fn

    # get full paths
    paths = []
    if dir[-4:]==".zip":
        with zipfile.ZipFile(dir,"r") as zf:
            all_paths = zf.namelist()
            # filter to get the right extension
            paths = list(filter(lambda f: f[-(len(ext)+1):] == "."+ext, all_paths))
            print("Total {} files in ZIP. {} are '*.{}'".format(len(all_paths),len(paths),ext))
    else:
        paths = getPaths(dir,ext)

    # get file list
    files = [os.path.splitext(os.path.basename(p))[0] for p in paths]

    # fetch metadata
    print("Fetching meta data")
    meta = pandas.read_csv(meta,dtype=str).fillna(False)

    # create a list of the file names...
    # the drama metadata has this - the TCP metadata, maybe not...
    textnames = []
    if "text_name" in meta.columns:
        textnames = [os.path.splitext(t)[0] if t else False for t in meta["text_name"]]
    elif "TCP" in meta.columns:
        textnames = [ (t+("" if t[0]=="K" else ".headed")) if t else "" for t in meta["TCP"]]

    if downcase:
        textnames = [t.lower() if t else False for t in textnames]
        files = [f.lower() if f else False for f in files]

    # build the sets - after we have adjusted the names
    textname_set = set([t for t in textnames if t])
    file_set = set(files)

    print("There are {} files in the directory, and {} in the metadata".format(len(files),len(meta)))

    # create two lists, files in metadata, files not in metadata
    in_meta = []
    not_in_meta = []
    for f in files:
        if f.replace(suffix,"") in textname_set:
            in_meta.append(f)
        else:
            not_in_meta.append(f)
    print("Files: {} files in metadata, {} files not in metadata".format(len(in_meta),len(not_in_meta)))

    # create two lists, rows in files, rows not in files
    # note: we keep the row number! (so we can report back)
    rows_none = []
    rows_with = []
    rows_without = []
    for i,t in enumerate(textnames):
        if t:
            if t+suffix in file_set:
                rows_with.append(i)
            else:
                rows_without.append(i)
        else: # there is no text
            rows_none.append(i)
    print("Metadata: {} rows with files, {} rows with missing files, {} rows without files".format(len(rows_with),len(rows_without),len(rows_none)))

    # diagnose missing rows
    if rows_without:
        for ri in rows_without[:rows_to_show]:
            print("   Row {}: '{}'".format(ri,textnames[ri]))

    if writefile:
        print("Writing Report",writefile)
        with open(writefile,"w") as fo:
            fo.write("Files without rows ({} of {})\n".format(len(not_in_meta),len(files)))
            for fi in not_in_meta:
                fo.write("   {}\n".format(fi))
            fo.write("-------------------------------------------------------\n")
            fo.write("Rows without files ({} of {}):\n".format(len(rows_without),len(textnames)))
            for ri in rows_without:
                fo.write("   Row {}: '{}'\n".format(ri, textnames[ri]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check that a directory has a full set of files")
    parser.add_argument("directory",type=str,help="Path to the directory with files (it does recurse)")
    parser.add_argument("repo", type=str, help="Repository (either D or T)")
    parser.add_argument("-e","--ext",type=str,default="txt",help="file extension to look for (no .)")
    parser.add_argument("-d","--downcase",help="Convert names (both sides) to lower case",action="store_true")
    parser.add_argument("-s","--suffix",type=str,help="Suffix to add to base names (use = for leading dash)",default="")
    parser.add_argument("-r","--rows_to_show",type=int,help="Number of missing rows to show",default=5)
    parser.add_argument("-w","--writefile",type=str,default=False,help="write report file")
    args = parser.parse_args()
    repo = None
    if not(args.repo) or args.repo[0]=="T" or args.repo[0]=="t":
        repo = tcp_meta
        print("using TCP repository")
    elif args.repo[0]=="E" or args.repo[0]=="e":
        repo = eebo_meta
    elif args.repo[0]=="D" or args.repo[0]=="d":
        repo = drama_meta
        print("using Drama repository")
    check(dir=args.directory,ext=args.ext,meta=repo,downcase=args.downcase,
          suffix=args.suffix,rows_to_show=args.rows_to_show,writefile=args.writefile)

