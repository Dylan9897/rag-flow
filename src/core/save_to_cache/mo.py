# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 17:19
import pymysql
from pymysql.converters import escape_string

class MatrixOne:
    def __init__(self):
        self.db = pymysql.connect(
            host='',
            port=6001,
            user='root',
            password="111",
            db='competition'
        )
        self.cursor = self.db.cursor()

    def _create_database_document(self):
        instruction = """CREATE TABLE chunk_table(
id int(11) AUTO_INCREMENT PRIMARY KEY,
file VARCHAR NOT NULL,
file_name VARCHAR NOT NULL,
chunks LONGTEXT NOT NULL,
category VARCHAR NOT NULL,
title VARCHAR NOT NULL,
address VARCHAR NOT NULL,
indexs VARCHAR NOT NULL,
chunks_embedding vecf32(1024),
sub_chunks_embedding vecf32(1024),
title_embedding vecf32(1024),
file_name_embedding vecf32(1024)
);"""
        self.cursor.execute(instruction)
        self.db.commit()

    def _create_database_split_document(self):
        instruction = """CREATE TABLE sub_chunk_table(
        id int(11) AUTO_INCREMENT PRIMARY KEY,
        file VARCHAR NOT NULL,
        file_name VARCHAR NOT NULL,
        chunks LONGTEXT NOT NULL,
        sub_chunks LONGTEXT NOT NULL,
        category VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        address VARCHAR NOT NULL,
        indexs VARCHAR NOT NULL,
        sub_indexs VARCHAR NOT NULL,
        chunks_embedding vecf32(1024),
        sub_chunks_embedding vecf32(1024),
        title_embedding vecf32(1024),
        file_name_embedding vecf32(1024)
        );"""
        self.cursor.execute(instruction)
        self.db.commit()

    def _insert_to_table(self, table, columns, values):
        column = ",".join(columns)
        value = ','.join(["'" + str(escape_string(str(unit))) + "'" for unit in values])
        sql_instruction = "INSERT INTO {table} ({column}) VALUES ({data})".format(table=table, column=column,
                                                                                  data=value)
        self.cursor.execute(sql_instruction)
        self.db.commit()

    def _insert_to_table_abstract(self, columns, values,table):
        column = ",".join(columns)
        value = ','.join(["'" + str(escape_string(str(unit))) + "'" for unit in values])
        sql_instruction = "INSERT INTO {table} ({column}) VALUES ({data})".format(table=table, column=column,
                                                                                  data=value)
        self.cursor.execute(sql_instruction)
        self.db.commit()

    def search_to_table(self, embed, column_name="chunks_embedding", method="l1_norm", table_name="handx"):
        assert method in ["l1_norm", "l2_norm", "cosine_similarity"]
        instruction = "SELECT file,file_name,chuncks,category,title FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 10;".format(
            table_name=table_name, method=method, column_name=column_name, embed=embed
        )

        self.cursor.execute(instruction)
        result = self.cursor.fetchall()
        result = [list(item) for item in result]

        return result

if __name__ == '__main__':
    func = MatrixOne()
    func._create_database_document()
    func._create_database_split_document()
