#!/usr/bin/env python3
# -*- encoding:utf8 -*-
"""
    Parser Module
    =============
    This module is charged to manipulate CSV Files, to import them,
    or to write them on file.
"""
import csv
from sys import maxsize

csv.field_size_limit(maxsize)

__all__ = ['Exporter','Importer']

class Importer:
    """
        Importeur de CSV.
        Attend un path vers le csv à importer, + quelques params optionnels
        (par defaut compatible avec les sorties Dataloader), et offre un
        attribut, data, contenant la sortie : une list de dictionnaires.
    """
    def __init__(self, filename, encoding='utf-8', async=True):
        self.filename = filename

        # detect dialect
        with open(filename) as infile:
            self.dialect = csv.Sniffer().sniff(infile.read(2048))
        print('DETECTING CSV DIALECT ::\n delimiter :: "{delimiter}", quotechar :: "{quotechar}"'.format(
            delimiter=self.dialect.delimiter,
            quotechar=self.dialect.quotechar))

        self.encoding = encoding
        self.header = None
        if not async:
            self.data, self.header = self.hydrate()

    def hydrate(self):
        """
            Parse le csv
        """
        with open(self.filename, 'r', encoding=self.encoding) as f:
            reader = csv.DictReader(f, dialect=self.dialect)
            data = []
            for row in reader:
                data.append(row)
        return data, reader.fieldnames

    def get_row_async(self):
        with open(self.filename, 'r', encoding=self.encoding) as f:
            reader = csv.DictReader(f, dialect=self.dialect)
            if self.header is None:
                self.header = reader.fieldnames

            for row in reader:
                yield row

    def get_header(self):
        """
            Retourne une liste ordonée des colonnes du CSV
        """
        return self.header

    def get_dialect(self):
        """
            Retourne le dialect detetecté pour le csv lu.
        """
        return self.dialect


class Exporter:
    """
        Permet d'ecrire un csv simplement.
        Attend en param le path vers le fichier de sortie (écrase l'existant !)
        et le header du csv.
        Dispose de methodes pour ecrire le csv ligne par ligne, ou directement une liste de ligne.
    """
    def __init__(self, filename, header, delimiter=',', quotechar='"', encoding='utf-8'):
        self.filename = filename
        self.header = header
        self.quotechar = quotechar
        self.delimiter = delimiter
        self.encoding = encoding
        with open(self.filename, 'wt', encoding='utf-8') as fwrite:
            writer = csv.DictWriter(fwrite, self.header,
                                    delimiter=self.delimiter,
                                    quotechar=self.quotechar,
                                    quoting=csv.QUOTE_ALL,
                                    lineterminator='\n')
            writer.writeheader()

    def write_row(self, row):
        """
            Ecrire une ligne depuis un dictionnaire.
            Leve une exception si une clef n'est pas contenu dans le header.
        """
        with open(self.filename, 'at', encoding='utf-8') as fwrite:
            writer = csv.DictWriter(fwrite,
                                    self.header,
                                    delimiter=self.delimiter,
                                    quotechar=self.quotechar,
                                    quoting=csv.QUOTE_ALL)
            writer.writerow(row)

    def write_rows(self, rows):
        """
            Ecrire une liste de ligne depuis une liste de dictionnaire.
            Leve une exception si une clef n'est pas contenu dans le header.
        """
        with open(self.filename, 'at', encoding='utf-8') as fwrite:
            writer = csv.DictWriter(fwrite,
                                    self.header,
                                    delimiter=self.delimiter,
                                    quotechar=self.quotechar,
                                    quoting=csv.QUOTE_ALL)
            writer.writerows(rows)
