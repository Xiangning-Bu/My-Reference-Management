import json
from urllib.request import urlopen
import sqlite3

conn = sqlite3.connect("MyRefs.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE COVID19 (
                pmid_int integer,
                title text,
                pubdate text,
                journal text,
                authors text,
                abstract text,
                elocationid text
                )"""
)

## search Pubmed with provided keyword and extract PMID lists
# keyword = input("Enter key word:")
# print(keyword)

with urlopen(
    f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=covid19&retmode=json"
) as response:
    source = response.read()

data = json.loads(source)
# print(json.dumps(data, indent=2))

# insert information for each paper
id_list = []
for id in data["esearchresult"]["idlist"]:
    id_list.append(id)
print(id_list)
id_lists = ",".join(id_list)
# print(id_list)
## search with PMID
with urlopen(
    f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={id_lists}&retmode=json"
) as response2:
    source2 = response2.read()

    data2 = json.loads(source2)

    with open("pmid20", "w") as f:
        json.dump(data2, f)


for id in id_list:
    #  extact all parameters for each columns, convert to apropriate datatype
    pmid = id
    title = data2["result"][id]["title"]
    # print(title)
    pubdate = data2["result"][id]["pubdate"]
    journal = data2["result"][id]["source"]

    author_list = data2["result"][id]["authors"]
    authors = []
    for author in author_list:
        authors.append(author["name"])
    authors = ",".join(authors)

    abstract = data2["result"][id]["attributes"]
    abstract = " ".join(abstract)

    elocationid = data2["result"][id]["elocationid"]

    pmid_int = int(id)
    # print(type(pmid_int))
    # print(type(title))
    # print(type(pubdate))
    # print(type(journal))
    # print(type(authors))
    # print(type(abstract))
    # print(type(elocationid))

    c.execute(
        "INSERT INTO COVID19 VALUES(?,?,?,?,?,?,?) ",
        (pmid_int, title, pubdate, journal, authors, abstract, elocationid),
    )


conn.commit()
conn.close()