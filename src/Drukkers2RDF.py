#!/usr/bin/env python

"""Drukkers2RDF.py: An RDF converter for the NL printers file."""

from rdflib import ConjunctiveGraph, Namespace, Literal, RDF, RDFS, BNode, URIRef

class Drukkers2RDF:
    """An RDF converter for the NL printers file."""
    
    namespaces = {
      'dcterms':Namespace('http://purl.org/dc/terms/'), 
      'skos':Namespace('http://www.w3.org/2004/02/skos/core#'), 
      'd2s':Namespace('http://www.data2semantics.org/core/'), 
      'qb':Namespace('http://purl.org/linked-data/cube#'), 
      'owl':Namespace('http://www.w3.org/2002/07/owl#')
    }

    printerID = -1

    def __init__(self, printersFile):
        """Constructor"""

        self.printersFile = open(printersFile, 'r')
        self.graph = ConjunctiveGraph()

        self.defaultNamespacePrefix = 'http://drukkers.data2semantics.org/resource/'
        scopeNamespace = self.defaultNamespacePrefix
        self.namespaces['scope'] = Namespace(scopeNamespace)
        self.graph.namespace_manager.bind('', self.namespaces['scope'])

        for namespace in self.namespaces:
            self.graph.namespace_manager.bind(namespace, self.namespaces[namespace])
        

    def parse(self):
        """Parse the printers file"""

        print "Parsing printers file..."

        for line in self.printersFile.readlines():
            if line.startswith("SET"):
                #Start new register
                self.printerID += 1
                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        RDF.type,
                        self.namespaces['d2s']['Printer']
                        ))

                #Parse SET, TTL, PPN and PAG
                firstLine = line.split(' ')
                #print firstLine
                printerSET = firstLine[1] + ' ' + firstLine[2]
                printerTTL = firstLine[4]
                printerPPN = line[line.find('PPN'):line.find('PAG')].split(' ')[1].strip()
                printerPAG = 1

                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printerSET'],
                        Literal(printerSET)
                        ))
                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printerTTL'],
                        Literal(printerTTL)
                        ))
                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printerPPN'],
                        Literal(printerPPN)
                        ))
                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printerPAG'],
                        Literal(printerPAG)
                        ))

            if line.startswith("Ingevoerd"):
                #Parse Ingevoerd, Gewijzigd and Status
                secondLine = line.split(' ')
                #print secondLine
                printerIngevoerd = secondLine[1]
                printerGewijzigd = secondLine[3] + ' ' + secondLine[4]
                printerStatus = secondLine[6].strip('\r\n')

                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printerIngevoerd'],
                        Literal(printerIngevoerd)
                        ))
                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printerGewijzigd'],
                        Literal(printerGewijzigd)
                        ))
                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printerStatus'],
                        Literal(printerStatus)
                        ))


            if line[0].isdigit():
                #Parse numerical fields

                self.graph.add((
                        self.namespaces['scope'][str(self.printerID)],
                        self.namespaces['d2s']['printers' + line[:3]],
                        Literal(line[4:].decode('latin1').strip(' \r\n'))
                        ))

        print "Parse done."

    def serialize(self, outputDataFile):
        """Write turtle RDF file to disk"""

        print "Serializing graph to {} ...".format(outputDataFile)
        fileWrite = open(outputDataFile, "w")
        turtle = self.graph.serialize(None, format='n3')
        fileWrite.writelines(turtle)
        fileWrite.close()
        print "Serialization done."

if __name__ == "__main__":
    drukkers2RDFInstance = Drukkers2RDF("../data/drukkers.txt")
    drukkers2RDFInstance.parse()
    drukkers2RDFInstance.serialize("../data/drukkers.ttl")



__author__ = "Albert Meronyo-Penyuela"
__copyright__ = "Copyright 2012, VU University Amsterdam"
__credits__ = ["Albert Meronyo-Penyuela"]
__license__ = "LGPL v3.0"
__version__ = "0.1"
__maintainer__ = "Albert Meronyo-Penyuela"
__email__ = "albert.merono@vu.nl"
__status__ = "Prototype"

