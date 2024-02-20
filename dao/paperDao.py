from entity.paperModel import Paper
from util import dbUtil
from PySide6.QtWidgets import QMessageBox


def addPaper(paper: Paper, popUp=False) -> bool:

    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()

        cursor.execute(
            f"insert into t_paper(folderPath, fileName, paperName, paperCatelogId, title, author, abstract, text, journal, issue, volume, page, date, url, doi, issn, isReferencedByCount) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (paper.folderPath, paper.fileName, paper.paperName, paper.paperCatelogId, paper.title, paper.author, paper.abstract, paper.text, paper.journal, paper.issue, paper.volume, paper.page, paper.date, paper.url, paper.doi, paper.issn, paper.isReferencedByCount))

        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to add paper - {paper.paperName} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def getPaperFromTypeFuzzyInfo(paperCatelogId: int, fuzzyInfo: str, popUp=False) -> list[Paper]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sqFuzzyInfo = "%" + fuzzyInfo + "%"
        cursor.execute(
            f"select * from t_paper where paperName like ? or title like ? or author like ? or abstract like ? or text like ? or journal like ? or date like ? or url like ? or doi like ? or issn like ? and paperCatelogId = ?", (sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, sqFuzzyInfo, paperCatelogId,))
        con.commit()
        paperList = cursor.fetchall()
        if not paperList:
            return []
        papers = []
        for _paper in paperList:
            paper = Paper(paperName=_paper[1], paperCatelogId=_paper[2], folderPath=_paper[3], fileName=_paper[4], title=_paper[5], author=_paper[6], abstract=_paper[7], text=_paper[8],
                          journal=_paper[9], issue=_paper[10], volume=_paper[11], page=_paper[12],  date=_paper[13], url=_paper[14],  doi=_paper[15],  issn=_paper[16], isReferencedByCount=_paper[17])
            paper.id_construct(_paper[0])
            papers.append(paper)
        return papers
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get paper from fuzzy information - {fuzzyInfo} (catelog id - {paperCatelogId}) - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)


def getPaperFromId(paperId: int, popUp=False) -> list[Paper]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_paper where id = ?", (paperId,))
        con.commit()
        paperList = cursor.fetchall()
        if not paperList:
            return []
        papers = []
        for _paper in paperList:
            paper = Paper(paperName=_paper[1], paperCatelogId=_paper[2], folderPath=_paper[3], fileName=_paper[4], title=_paper[5], author=_paper[6], abstract=_paper[7], text=_paper[8],
                          journal=_paper[9], issue=_paper[10], volume=_paper[11], page=_paper[12],  date=_paper[13], url=_paper[14],  doi=_paper[15],  issn=_paper[16], isReferencedByCount=_paper[17])
            paper.id_construct(_paper[0])
            papers.append(paper)
        return papers
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get paper from id - {paperId} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)


def getPaperFromPaperCatelogId(paperCatelogId: int, popUp=False) -> list[Paper]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_paper where paperCatelogId = ?", (paperCatelogId,))
        con.commit()

        paperList = cursor.fetchall()
        if not paperList:
            return []

        papers = []
        for _paper in papers:
            paper = Paper(paperName=_paper[1], paperCatelogId=_paper[2], folderPath=_paper[3], fileName=_paper[4], title=_paper[5], author=_paper[6], abstract=_paper[7], text=_paper[8],
                          journal=_paper[9], issue=_paper[10], volume=_paper[11], page=_paper[12],  date=_paper[13], url=_paper[14],  doi=_paper[15],  issn=_paper[16], isReferencedByCount=_paper[17])
            paper.id_construct(_paper[0])
            papers.append(paper)
        return papers
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get paper from type id - {paperCatelogId} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)


def modifyPaper(paper: Paper, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"update t_paper set folderPath = ?, fileName = ?, paperName = ?, paperCatelogId = ?, title = ?, author = ?, abstract = ?, text = ?, journal = ?, issue = ?, volume = ?, page = ?, date = ?, url = ?, doi = ?, issn = ?, isReferencedByCount = ? where id = ?", (paper.folderPath, paper.fileName, paper.paperName, paper.paperCatelogId, paper.title, paper.author, paper.abstract, paper.text, paper.journal, paper.issue, paper.volume, paper.page, paper.date, paper.url, paper.doi, paper.issn, paper.isReferencedByCount, paper.id, ))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to modity paper - {paper.paperName} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def delPaperFromId(paperId: int, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"delete from t_paper where id = ?", (paperId,))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to delete paper from id - {paperId} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)
