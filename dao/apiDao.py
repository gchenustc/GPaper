from entity.apiModel import Api
from util import dbUtil
from PySide6.QtWidgets import QMessageBox


def addApi(api: Api, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()

        cursor.execute(
            f"insert into t_api('platform', 'key', 'host', 'selected') values(?,?,?,?)", (api.platform, api.key, api.host, api.selected))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to add api - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def modifyApiFromId(api: Api, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"update t_api set platform = ?, key = ?, host = ?, selected = ? where id = ? ", (api.platform, api.key, api.host, api.selected, api.id))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to modify api from id - {api.id} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def getApiFromId(ApiId: int, popUp=False) -> list[Api]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_api where id = ?", (ApiId,))
        con.commit()
        apiList = cursor.fetchall()
        if not apiList:
            return []
        apis = []
        for _api in apiList:
            api = Api(platform=_api[1], key=_api[2], host=_api[3], selected=_api[4])
            api.id_construct(_api[0])
            apis.append(api)
        return apis
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get api from id - {ApiId} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)

def getAllApis(popUp=False) -> list[Api]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_api")
        con.commit()
        apiList = cursor.fetchall()
        if not apiList:
            return []
        apis = []
        for _api in apiList:
            api = Api(platform=_api[1], key=_api[2], host=_api[3], selected=_api[4])
            api.id_construct(_api[0])
            apis.append(api)
        return apis
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get all apis - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)
        
def getApifromSelected(selected: int, popUp=False) -> list[Api]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_api where selected = ?", (selected,))
        con.commit()
        apiList = cursor.fetchall()
        if not apiList:
            return []
        apis = []
        for _api in apiList:
            api = Api(platform=_api[1], key=_api[2], host=_api[3], selected=_api[4])
            api.id_construct(_api[0])
            apis.append(api)
        return apis
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get api from selected - {selected} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)
