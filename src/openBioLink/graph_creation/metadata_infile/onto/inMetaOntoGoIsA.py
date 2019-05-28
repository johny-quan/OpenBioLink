from ....edgeType import EdgeType
from ...types.infileType import InfileType
from ...metadata_infile.infileMetadata import InfileMetadata
from ....nodeType import NodeType


class InMetaOntoGoIsA(InfileMetadata):

    CSV_NAME = "DB_ONTO_GO_IS_A_ontology.csv"
    USE_COLS = ['ID', 'IS_A']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    NODE1_TYPE = NodeType.GO
    NODE2_TYPE = NodeType.GO
    EDGE_TYPE = EdgeType.IS_A
    MAPPING_SEP = ';'
    INFILE_TYPE = InfileType.IN_ONTO_GO_IS_A


    def __init__(self):
        super().__init__(csv_name=self.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=self.INFILE_TYPE)
