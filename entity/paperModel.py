class Paper:

    id = -1
    paperName = ""
    paperCatelogId = -1
    folderPath = ""
    fileName = ""
    title = ""
    author = ""
    abstract = ""
    text = ""
    journal = ""
    issue = ""
    volume = ""
    page = ""
    date = ""
    url = ""
    doi = ""
    issn = ""
    isReferencedByCount = ""

    def __init__(self, paperName=paperName, paperCatelogId=paperCatelogId, folderPath=folderPath, fileName=fileName, title=title, author=author, abstract=abstract, text=text, journal=journal, issue=issue, volume=volume, page=page, date=date, url=url, doi=doi, issn=issn, isReferencedByCount=isReferencedByCount):
        self.paperName = paperName
        self.paperCatelogId = paperCatelogId
        self.folderPath = folderPath
        self.fileName = fileName
        self.title = title
        self.author = author
        self.abstract = abstract
        self.text = text
        self.journal = journal
        self.issue = issue
        self.volume = volume
        self.page = page
        self.date = date
        self.url = url
        self.doi = doi
        self.issn = issn
        self.isReferencedByCount = isReferencedByCount

    def id_construct(self, id=id):
        self.id = id
