# check what files are in a directory
# if you have a directory full of XML or CSV or TXT, it's hard to even count how many
# there are, never mind to see if you have "all" of them (and which set of "all" do
# you have)

# use glob to get file list
import glob
# pandas for dealing with metadata
import pandas
# need for getting names
import os

# defaults are on my disk - mainly for testing
test_dir = "C:\\DigHum\\TCP\\CleanExtractedStandardized"
play_dir = "C:\\DigHum\\Plays\\emd1554_charCleanExtractedSt"

# the metada file to check
tcp_meta = "https://raw.githubusercontent.com/uwgraphics/VEP-corpora/master/tcp_ascii_standardized.csv"
drama_meta = "https://raw.githubusercontent.com/uwgraphics/VEP-corpora/master/vep_early_modern_drama_all_known_texts_master.csv"

# get the list of files
def getPaths(dir, ext):
    if (ext[0]=="."):
        ext = ext[1:]
    return glob.glob(dir + "/**/*[.]" + ext, recursive=True)

c_tn = []
c_fn = []

# get a list of files, the meta data, and then match...
def check(*, dir=play_dir, ext=".txt", meta=drama_meta):
    global c_tn,c_fn

    # get file list
    paths = getPaths(dir,ext)
    files = [os.path.splitext(os.path.basename(p))[0] for p in paths]
    file_set = set(files)

    # fetch metadata
    print("Fetching meta data")
    meta = pandas.read_csv(meta).fillna(False)

    # create a list of the file names...
    # the drama metadata has this - the TCP metadata, maybe not...
    textnames = []
    if "text_name" in meta.columns:
        textnames = [os.path.splitext(t)[0] if t else False for t in meta["text_name"]]
    elif "TCP" in meta.columns:
        textnames = [ t+("" if t[0]=="K" else ".headed") for t in meta["TCP"]]

    # either way, build the set
    textname_set = set([t for t in textnames if t])

    print("There are {} files in the directory, and {} in the metadata".format(len(files),len(meta)))

    # create two lists, files in metadata, files not in metadata
    in_meta = []
    not_in_meta = []
    for f in files:
        if f in textname_set:
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
            if t in file_set:
                rows_with.append(i)
            else:
                rows_without.append(i)
        else: # there is no text
            rows_none.append(i)
    print("Metadata: {} rows with files, {} rows with missing files, {} rows without files".format(len(rows_with),len(rows_without),len(rows_none)))

    # diagnose missing rows
    if rows_without:
        for ri in rows_without[:5]:
            print("   Row {}: '{}'".format(ri,textnames[ri]))