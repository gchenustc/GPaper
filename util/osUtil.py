import json
import os
import shutil
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import requests
import io
import re
import string
from PySide6.QtWidgets import QMessageBox

def pdf2Text(pdf_path: str) -> str:
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            # 创建资源管理器和PDF解释器对象
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()  # 设置分析参数，如是否合并字符等
            output_string = io.StringIO()
            device = TextConverter(rsrcmgr, output_string, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            with file as fp:
                for page_num, page in enumerate(PDFPage.get_pages(fp)):
                    interpreter.process_page(page)

                    # 获取转换后的文本并将其从缓冲区读出
                    text = output_string.getvalue()
                    text += text

                # 清空输出缓冲区
                output_string.seek(0)
                output_string.truncate(0)

            # 关闭设备
            device.close()

        return text

    except Exception as e:
        QMessageBox.critical(None, "Error", "Failed to convert PDF to text")
        return ""


def movePdfToDestFolder(pdf_path: str, dest_folder: str, popUp=False) -> str:

    file_name = os.path.basename(pdf_path)
    
    # test if the destination folder is a file with the same name
    if os.path.exists(dest_folder) and not os.path.isdir(dest_folder):
        try:
            os.remove(dest_folder)
        except Exception as e:
            if popUp:
                QMessageBox.critical(None, "Error", f"Failed to remove the file with the same name with the destination folder - {dest_folder}")
            return ""
    
    # create the destination folder if it does not exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # detect if there is a file with the same name
    while os.path.exists(os.path.join(dest_folder, file_name)):
        file_name = file_name.split(".")[0] + "_copy." + file_name.split(".")[1]
    
    try:
        shutil.copy(pdf_path, os.path.join(dest_folder, file_name))

    except Exception as e:
        if popUp:
            QMessageBox.critical(None, "Error", f"Failed to copy the {pdf_path} to the destination folder - {dest_folder} - {e}")
        return ""

    return file_name


def extractDoi(text: str) -> str:
    # DOI的一般格式是10开头的数字和.分割的路径，后面可能跟着 / 或 # 及其他内容
    doi_pattern = r"10\.\d{4,9}\/[-._;()/:A-Za-z0-9]+"

    # 使用正则表达式查找DOI
    match = re.search(doi_pattern, text)

    if match:
        return match.group(0)  # 返回找到的DOI
    else:
        return ""  # 未找到DOI

def remove_punctuation_from_end(text):
    if text and text[-1] in string.punctuation:
        return text[:-1]
    else:
        return text

def isValidWord(string):
    string = remove_punctuation_from_end(string)
    if string.isalpha() and len(string) > 1:
        return True
    else:
        return False


def splitStr(string, word_limit):
    result_list = []  # 最终的分割结果列表
    paragraphs = re.split(r'\n{1,}', string)  # 分割成段落

    result = ""
    word_count = 0

    for idx, paragraph in enumerate(paragraphs):
        words = paragraph.split()  # 按空格分割单词
        paragraph_word_count = len(words)

        # 判断累计的单词数目
        if word_count + paragraph_word_count <= word_limit:
            result += paragraph + "\n\n"
            word_count += paragraph_word_count
        else:
            if result:
                result_list.append(result)

            result = paragraph + "\n\n"
            word_count = paragraph_word_count

    if result:
        result_list.append(result)

    return result_list


def filterText(text: str, filter_level: int) -> str:
    # filter_level 最大为4
    if filter_level:
        # 尝试将pra-\nctise(practise)这样的文本连接成一行
        text = re.sub(r'\-\n', '', text)
        filter_level -= 1

    if filter_level:
        # 将单独的换行符替换为空格
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
        filter_level -= 1

    if filter_level:
        # 将连续的换行符替换为单个换行符
        text = re.sub(r"\n\n+", "\n", text)
        filter_level -= 1

    if filter_level:
        # 根据一行的单词数和字符数判断保留与否
        lines = text.split('\n')  # 将字符串按换行符分割成列表
        filtered_lines = []
        for line in lines:
            chars_list = line.strip().split()
            words_in_line = len(chars_list)  # 使用正则表达式计算单词数
            chars_in_line = len("".join(chars_list))
            if chars_in_line == 0:
                continue
            vaild_words_ratio = sum(
                [1 for i in chars_list if isValidWord(i)]) / words_in_line
            ###### 判断标准: ####
            if chars_in_line > 10 and words_in_line > 3 and vaild_words_ratio > 0.4:
                filtered_lines.append(line)
        text = '\n'.join(filtered_lines)  # 使用换行符重新组合筛选后的行
        filter_level -= 1

    return text.strip()


def getArticalInfoByDoi(doi: str, popUp=False) -> dict:
    # Crossref API基础URL
    base_url = "https://api.crossref.org/works/"

    # DOI号
    doi_value = doi.replace(" ", "")  # 清除DOI中的空格

    # 构造请求URL
    url = f"{base_url}{doi_value}"

    # 发送GET请求
    response = requests.get(url)

    # 检查响应状态码是否为200，表示成功
    if response.status_code == 200:
        # 解析JSON响应内容
        data = response.json()

        # 提取文章信息
        try:
            article_info = data['message']
            url = article_info.get('URL', 'Unknown')
            title = article_info.get('title', ['Unknown'])[0]  # 取第一条标题记录
            abstract = article_info.get('abstract', ['Unknown'])
            author = [author['given'] + ' ' + author['family']
                       for author in article_info.get('author', [])]
            journal = article_info.get(
                'container-title', ['Unknown'])[0]  # 取第一条期刊名称记录
            issue = article_info.get('issue', 'Unknown')
            volume = article_info.get('volume', 'Unknown')
            published_date_list = article_info.get(
                'published-print', {}).get('date-parts', [['Unknown', 'Unknown', 'Unknown']])[0]
            date = "-".join([str(i) for i in published_date_list])
            year = published_date_list[0]
            month = published_date_list[1] if len(
                published_date_list) > 1 else ""
            day = published_date_list[2] if len(
                published_date_list) > 2 else ""
            issn = article_info.get('ISSN', ['Unknown'])[0]
            doi = article_info.get('DOI', ['Unknown'])
            page = article_info.get('page', 'Unknown')
            isReferencedByCount = article_info.get(
                'is-referenced-by-count', 'Unknown')
            reference = article_info.get('reference', 'Unknown')

            all_info_dict = {"url": url, "title": title, "abstract": abstract, "author": author, "journal": journal, "issue": issue, "volume": volume, "date": date,
                             "year": year, "month": month, "day": day, "issn": issn, "doi": doi, "page": page, "isReferencedByCount": isReferencedByCount, "reference": reference}

            return all_info_dict

        except Exception as e:
            if popUp:
                QMessageBox.critical(None, "Error", f"Failed to extract article information from the DOI - {doi} - {e}")
            return {}

    else:
        QMessageBox.critical(None, "Error", "Failed to get article information from the DOI (response status code is not 200)")
        return None
########################

def splitStr(string, word_limit):
    result_list = []  # 最终的分割结果列表
    paragraphs = re.split(r'\n{1,}', string)  # 分割成段落

    result = ""
    word_count = 0

    for idx, paragraph in enumerate(paragraphs):
        words = paragraph.split()  # 按空格分割单词
        paragraph_word_count = len(words)

        # 判断累计的单词数目
        if word_count + paragraph_word_count <= word_limit:
            result += paragraph + "\n\n"
            word_count += paragraph_word_count
        else:
            if result:
                result_list.append(result)

            result = paragraph + "\n\n"
            word_count = paragraph_word_count

    if result:
        result_list.append(result)

    return result_list