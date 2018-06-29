# -*- coding: utf-8 -*-
import dbClass
import translatorClass
import funcs
import json
import re
import sys

def _main(tableName, translateNum):
    StartID = {'rentals': {'ID': 0}, 'residential': {'ID': 0}}
    try:
        with open('StartID.json', 'r') as f:
            StartID = json.load(f)
        f.close()
    except IOError:
        pass

    db = dbClass.db()
    db.execute("SELECT TOP {2} ID, heading, description, chineseheading, chinesedescription "
               "FROM dbo.{0} WHERE ID >{1} ORDER BY ID ASC;".format(tableName, StartID[tableName]['ID'], translateNum))
    result = db.cursor.fetchall()
    trans = translatorClass.translator(4, ['NNP', 'NNPS'], ['VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'VBD'])
    for row in result:
        ID = row[0]
        print(ID)
        EngHeading = row[1]
        EngDescription = row[2]
        ChinHeading = row[3]
        ChinDescription = row[4]
        if not funcs.check_contain_chinese(ChinHeading) and not funcs.check_contain_chinese(ChinDescription):
            try:
                TransHeading = trans.translate(EngHeading)
                TransDescription = ''
                for line in EngDescription.split('\n'):
                    translation = trans.translate(line)
                    if re.match('Translate Failed', translation):
                        TransDescription += line + '\n'
                    else:
                        TransDescription += translation + '\n'
                query = "UPDATE dbo.{3} SET archived = 1, chineseheading = N\'{0}\', chinesedescription =N\'{1}\' WHERE ID ={2}" \
                    .format(funcs.format_correct(TransHeading), funcs.format_correct(TransDescription), ID, tableName)
                try:
                    db.execute(funcs.mssql_query(query))
                except:
                    print("Insert SQL Failed")
                db.commit()
            except:
                pass
    StartID[tableName]['ID'] = ID
    db.close()

    try:
        with open('StartID.json', 'w') as f:
            json.dump(StartID, f)
        f.close()
    except IOError:
        pass

def _main2(tableName, translateNum):
    StartID = {'rentals': {'ID': 0}, 'residential': {'ID': 0}}
    try:
        with open('StartID.json', 'r') as f:
            StartID = json.load(f)
        f.close()
    except IOError:
        pass

    db = dbClass.db()
    db.execute("SELECT TOP {2} ID, heading, description, chineseheading, chinesedescription "
               "FROM dbo.{0} WHERE ID >{1} ORDER BY ID ASC;".format(tableName, StartID[tableName]['ID'], translateNum))
    result = db.cursor.fetchall()
    trans = translatorClass.translator(4, ['NNP', 'NNPS'], ['VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'VBD'])
    for row in result:
        ID = row[0]
        print(ID)
        EngHeading = row[1]
        EngDescription = row[2]
        ChinHeading = row[3]
        ChinDescription = row[4]
        if not funcs.check_contain_chinese(ChinHeading) and not funcs.check_contain_chinese(ChinDescription):
            try:
                TransHeading = trans.translate(EngHeading)
                TransDescription = ''
                for line in EngDescription.split('\n'):
                    translation = trans.translate(line)
                    if re.match('Translate Failed', translation):
                        TransDescription += line + '\n'
                    else:
                        TransDescription += translation + '\n'
                query = "UPDATE dbo.{3} SET archived = 1, chineseheading = N\'{0}\', chinesedescription =N\'{1}\' WHERE ID ={2}" \
                    .format(funcs.format_correct(TransHeading), funcs.format_correct(TransDescription), ID, tableName)
                try:
                    db.execute(funcs.mssql_query(query))
                except:
                    print("Insert SQL Failed")
                db.commit()
            except:
                pass
    StartID[tableName]['ID'] = ID
    db.close()

    try:
        with open('StartID.json', 'w') as f:
            json.dump(StartID, f)
        f.close()
    except IOError:
        pass

if __name__ == '__main__':
    tableName = sys.argv[1]
    postNum = sys.argv[2]

    _main(tableName, postNum)







