from entity.paperCatelogModel import PaperCatelog
from util import dbUtil
from PySide6.QtWidgets import QMessageBox


def addPaperCatelog(paperCatelog: PaperCatelog, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()

        # exclude the same paper type name
        cursor.execute(
            f"select * from t_papercatelog where catelogName = ?", (paperCatelog.catelogName,))
        if cursor.fetchall():
            if popUp:
                QMessageBox.critical(
                    None, "Error", f"The paper type - {paperCatelog.catelogName} already exists")
            return False

        cursor.execute(
            f"insert into t_papercatelog('catelogName', 'catelogDesc', 'sortedId') values(?,?,?)", (paperCatelog.catelogName, paperCatelog.catelogDesc, paperCatelog.sortedId))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to add paper type - {paperCatelog.catelogName} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def getPaperCatelogFromName(catelogName: str, popUp=False) -> list:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_papercatelog where catelogName = ?", (catelogName,))
        con.commit()
        return cursor.fetchall()
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get paper type - {catelogName} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)


def getPaperCatelogFromFuzzyName(fuzzyCatelogName: str = "", popUp=False) -> list:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_papercatelog where catelogName like ?", ("%" + fuzzyCatelogName + "%",))
        con.commit()
        return cursor.fetchall()
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get paper type from fuzzy name - {fuzzyCatelogName} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)


def modityPaperCatelogFromId(paperCatelog: PaperCatelog, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"update t_papercatelog set catelogName = ?, catelogDesc = ?, sortedId = ? where id = ? ", (paperCatelog.catelogName, paperCatelog.catelogDesc, paperCatelog.sortedId, paperCatelog.id))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to modify paper type - {paperCatelog.catelogName} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def modityPaperCatelogFromSortedId(paperCatelog: PaperCatelog, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"update t_papercatelog set catelogName = ?, catelogDesc = ? where sortedId = ? ", (paperCatelog.catelogName, paperCatelog.catelogDesc, paperCatelog.sortedId))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to modify paper type - {paperCatelog.catelogName} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def delPaperCatelogFromSortedId(id: int, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"delete from t_papercatelog where sortedId = ?", (id,))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to delete paper type from id - {id} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)
