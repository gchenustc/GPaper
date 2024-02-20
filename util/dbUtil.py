import sqlite3

def getCon():
    """
    获取数据连接
    :return: 数据库连接
    """
    
    con = sqlite3.connect(
        "db_data.db",
        # detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    return con

def closeCon(con):
    """
    关闭数据库连接
    :param con: 数据库连接
    :return: None
    """
    con.close()


if __name__ == "__main__":
    con = None
    try:
        con = getCon()
        cursor = con.cursor()
        cursor.execute("select * from t_papertype")
        con.commit()
    except Exception as e:
        print(e)
    finally:
        closeCon(con)