import configparser
import json
import os
import sqlite3
from sqlite3 import Error


class CoverageContextReport:
    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def get_rows(conn, sql):
        conn.row_factory = CoverageContextReport.dict_factory
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_template_content(filename='coverage_html_context.js'):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)) as handle:
            return handle.read()

    @staticmethod
    def main():

        coverage_database = r".coverage"
        coverage_config_file = r".coveragerc"
        coverage_html_directory = 'htmlcov'
        coverage_html_context_file = 'coverage_html_context.js'

        coverage_html_context_file_path = os.path.join(coverage_html_directory, coverage_html_context_file)
        if os.path.isfile(coverage_config_file):
            config = configparser.ConfigParser()
            config.read(coverage_config_file)
            if config.has_option('html', 'directory'):
                coverage_html_context_file_path = os.path.join(config.get('html', 'directory'),
                                                               coverage_html_context_file)
        conn = CoverageContextReport.create_connection(coverage_database)
        with conn:
            contexts = CoverageContextReport.get_rows(conn, "SELECT * FROM context")
            files = CoverageContextReport.get_rows(conn, "SELECT * FROM file")
            arcs = CoverageContextReport.get_rows(conn, "SELECT * FROM arc")

        contexts_by_lineno = []
        for arc in arcs:
            file_id_filter = next(filter(lambda x: x['id'] == arc['file_id'], contexts_by_lineno), None)
            if file_id_filter is None:
                contexts_by_lineno.append({'id': arc['file_id'], 'context': []})
                file_id_filter = contexts_by_lineno[-1]
            context_id_filter = next(filter(lambda x: x['id'] == arc['context_id'], file_id_filter['context']), None)
            if context_id_filter is None:
                file_id_filter['context'].append({'id': arc['context_id'], 'arcs': []})
                context_id_filter = file_id_filter['context'][-1]
            if arc['fromno'] not in context_id_filter['arcs']:
                context_id_filter['arcs'].append(arc['fromno'])
            if arc['tono'] not in context_id_filter['arcs']:
                context_id_filter['arcs'].append(arc['tono'])

        template = CoverageContextReport.get_template_content()
        template = template.replace('@@contexts@@', json.dumps(contexts))
        template = template.replace('@@files@@', json.dumps(files))
        template = template.replace('@@arcs@@', json.dumps(contexts_by_lineno))

        with open(coverage_html_context_file_path.replace(coverage_html_context_file, "coverage_html.js"), '+a') as f:
            f.write(template)
        f.close()


if __name__ == '__main__':
    CoverageContextReport.main()
