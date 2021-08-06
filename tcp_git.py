# List the repositories in the TCP's git organization (actually, the Oxford TEI5 files)
#
# this project was aborted:
# because each text is in a separate repository, just listing them requires fetching a list
# of 60000+ repos.
# since you can only get 100 per "page" this would take hundreds of pages - which you cannot
# fetch from GH because of throttling issues
# even if you could find all of the directories, you couldn't fetch them all

import github as G
import toml

# in order to get decent API rate limits with github, you need to be logged in
# so, I log in as me
# but... I don't want to put my key into this repo
# put your github token string into a keys file

keys = toml.load()

gh = G.Github()
org = g.get_organization("textcreationpartnership")

# warning... this is a paged list - naively turning it into a paged list takes FOREVER!
# and it isn't even "legal" (it requires
repos = org.get_repos()