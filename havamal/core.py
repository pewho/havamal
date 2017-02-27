from ulv.parser import Exporter
from ldif import LDIFParser

from os.path import exists
import configparser

class LDIF2CSVParser(LDIFParser):
    def __init__(self, infile_path, csv_exporter, mapper):
        self.exporter = csv_exporter
        self.mapper = mapper
        super().__init__(infile_path)

    def handle(self, dn, entry):
        exported_dic = {}
        for key, value in entry.items():
            if self.is_col_exported(key):
                exported_dic[self.mapper.csv_colnames_mapping[key.lower().strip()]] = self.format_value(value)
        self.exporter.write_row(exported_dic)

    def format_value(self, value):
        return ", ".join([val.decode('utf-8') for val in value])

    def is_col_exported(self, colname):
        return colname.upper().strip() in self.mapper.uniformized_ldif_cols


class ColsMapper():
    def __init__(self, mapper_file):
        self.csv_colnames_mapping = self.import_mapping(mapper_file)
        self.uniformized_ldif_cols = self.uniformize_colnames()

    def import_mapping(self, mapper_file):
        if not exists(mapper_file):
            raise OSError("Mapper file not found !")
        mapper = configparser.ConfigParser()
        mapper.read(mapper_file)

        mapper_dic = {}
        for key in mapper["MAP"]:
            mapper_dic[key] = mapper["MAP"][key]

        return mapper_dic

    def uniformize_colnames(self):
        return [k.upper().strip() for k in self.csv_colnames_mapping.keys()]


class LDIFDefaultMappingTool(LDIFParser):
    def __init__(self, infile_path, mapper_path):
        self.mapper_path = mapper_path
        self.mapper = configparser.ConfigParser()
        self.mapper['MAP'] = {}
        self.first_line_handled = False
        super().__init__(infile_path)

    def handle(self, dn, entry):
        if self.first_line_handled:
            pass
        else:
            for key in entry.keys():
                self.mapper['MAP'][key] = key
            self.first_line_handled = True

    def write_conf(self):
        with open(self.mapper_path, 'w') as out:
            self.mapper.write(out)


def format(infile_path, outfile_path, mapper_file):
    with open(infile_path) as in_f:
        mapper = ColsMapper(mapper_file)
        exporter = Exporter(outfile_path, mapper.csv_colnames_mapping.values())
        parser = LDIF2CSVParser(in_f, exporter, mapper)

        parser.parse()

def default_mapping(infile, mapper_output):
    with open(infile) as in_f:
        parser = LDIFDefaultMappingTool(in_f, mapper_output)
        parser.parse()
        parser.write_conf()
