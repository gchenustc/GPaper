from entity.modelModel import Model
from util import dbUtil
from PySide6.QtWidgets import QMessageBox


def addModel(model: Model, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()

        cursor.execute(
            f"insert into t_model('name', 'apiId', 'selected') values(?,?,?)", (model.name, model.apiId, model.selected))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to add model - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def modifyModelFromId(model: Model, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"update t_model set name = ?, apiId = ?, selected = ? where id = ? ", (model.name, model.apiId, model.selected, model.id))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to modify model from id - {model.id} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def getModelFromId(modelId: int, popUp=False) -> list[Model]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_model where id = ?", (modelId,))
        con.commit()
        modelList = cursor.fetchall()
        if not modelList:
            return []
        models = []
        for _model in modelList:
            model = Model(name=_model[1],
                          apiId=_model[2], selected=_model[3])
            model.id_construct(_model[0])
            models.append(model)
        return models
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get model from id - {modelId} - {e}")
        return []
    finally:
        dbUtil.closeCon(con)


def getModelFromSelected(selected: int, popUp=False) -> list[Model]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_model where selected = ?", (selected,))
        con.commit()
        modelList = cursor.fetchall()
        if not modelList:
            return []
        models = []
        for _model in modelList:
            model = Model(name=_model[1],
                          apiId=_model[2], selected=_model[3])
            model.id_construct(_model[0])
            models.append(model)
        return models
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get model from selected - {selected} - {e}")
        return []
    finally:
        dbUtil.closeCon(con)


def getAllModels(popUp=False) -> list[Model]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_model")
        con.commit()
        modelList = cursor.fetchall()
        if not modelList:
            return []
        models = []
        for _model in modelList:
            model = Model(name=_model[1],
                          apiId=_model[2], selected=_model[3])
            model.id_construct(_model[0])
            models.append(model)
        return models
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get all models - {e}")
        return []
    finally:
        dbUtil.closeCon(con)


def getModelFromApiId(apiId: int, popUp=False) -> list[Model]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_model where apiId = ?", (apiId,))
        con.commit()
        modelList = cursor.fetchall()
        if not modelList:
            return []
        models = []
        for _model in modelList:
            model = Model(name=_model[1],
                          apiId=_model[2], selected=_model[3])
            model.id_construct(_model[0])
            models.append(model)
        return models
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get model from platform id - {apiId} - {e}")
        return []
    finally:
        dbUtil.closeCon(con)
        
def getModelFromApiIdAndSelected(apiId: int, selected: int, popUp=False) -> list[Model]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_model where apiId = ? and selected = ?", (apiId, selected))
        con.commit()
        modelList = cursor.fetchall()
        if not modelList:
            return []
        models = []
        for _model in modelList:
            model = Model(name=_model[1],
                          apiId=_model[2], selected=_model[3])
            model.id_construct(_model[0])
            models.append(model)
        return models
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get model from platform id and selected - {apiId} - {selected} - {e}")
        return []
    finally:
        dbUtil.closeCon(con)
