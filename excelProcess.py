from openpyxl import load_workbook
from openpyxl.styles import Alignment
from lingmoAPI import lingmoAPI
from funcs import str_join, regx_replace_keywords, build_dict_from_xlsx
import os


def translator_xlsx(dest_file, english_keywords_replacement_dict = None):

    lw = load_workbook(filename=dest_file)
    ws = lw.active

    api = lingmoAPI()

    index = 5
    total_count = 0
    while index <= ws.max_row:
        value = ws[str_join('B', index)].value
        if value:
            if english_keywords_replacement_dict:
                value = regx_replace_keywords(value, english_keywords_replacement_dict)
            translation = api.en_to_ch(value)
            ws[str_join('E', index)] = translation
            ws[str_join('F', index)] = value
            ws[str_join('F', index)].alignment = Alignment(wrapText=True)
            ws[str_join('E', index)].alignment = Alignment(wrapText=True)
            total_count += 1
        index += 1

    print(total_count)

    lw.save(dest_file)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
keywords_dict = build_dict_from_xlsx(os.path.join(ROOT_DIR, 'tmp\SampleEnglishKeyword2.xlsx'))
translator_xlsx(os.path.join(ROOT_DIR,'tmp', '5.27.xlsx'), english_keywords_replacement_dict=keywords_dict)






