from entity.promptModel import Prompt
from util import dbUtil
from PySide6.QtWidgets import QMessageBox


def addPrompt(prompt: Prompt, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()

        cursor.execute(
            f"insert into t_prompt('name', 'text', 'selected') values(?,?,?)", (prompt.name, prompt.text, prompt.selected))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to add prompt - {prompt.name} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def modifyPromptFromId(prompt: Prompt, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"update t_prompt set name = ?, text = ?, selected = ? where id = ? ", (prompt.name, prompt.text, prompt.selected, prompt.id))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to modify prompt from id - {prompt.id} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con)


def getPromptFromId(promptId: int, popUp=False) -> list[Prompt]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_prompt where id = ?", (promptId,))
        con.commit()
        promptList = cursor.fetchall()
        if not promptList:
            return []
        prompts = []
        for _prompt in promptList:
            prompt = Prompt(name=_prompt[1], text=_prompt[2], selected=_prompt[3])
            prompt.id_construct(_prompt[0])
            prompts.append(prompt)
        return prompts
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get prompt from id - {promptId} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)
        
def getAllPrompts(popUp=False) -> list[Prompt]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_prompt")
        con.commit()
        promptList = cursor.fetchall()
        if not promptList:
            return []
        prompts = []
        for _prompt in promptList:
            prompt = Prompt(name=_prompt[1], text=_prompt[2], selected=_prompt[3])
            prompt.id_construct(_prompt[0])
            prompts.append(prompt)
        return prompts
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get all prompt - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)

def getPromptFromSelected(selected: int, popUp=False) -> list[Prompt]:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"select * from t_prompt where selected = ?", (selected,))
        con.commit()
        promptList = cursor.fetchall()
        if not promptList:
            return []
        prompts = []
        for _prompt in promptList:
            prompt = Prompt(name=_prompt[1], text=_prompt[2], selected=_prompt[3])
            prompt.id_construct(_prompt[0])
            prompts.append(prompt)
        return prompts
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to get prompt from selected - {selected} - {e}")
        con.rollback()
        return []
    finally:
        dbUtil.closeCon(con)
    
def deletePromptFromId(promptId: int, popUp=False) -> bool:
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        cursor.execute(
            f"delete from t_prompt where id = ?", (promptId,))
        con.commit()
        return True
    except Exception as e:
        if popUp:
            QMessageBox.critical(
                None, "Error", f"Failed to delete prompt from id - {promptId} - {e}")
        con.rollback()
        return False
    finally:
        dbUtil.closeCon(con) 