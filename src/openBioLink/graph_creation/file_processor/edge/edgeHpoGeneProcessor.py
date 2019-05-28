from ..fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.edge.inMetaEdgeHpoGene import InMetaEdgeHpoGene


class EdgeHpoGeneProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeHpoGene

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_HPO_GENE,
                         infileType=InfileType.IN_EDGE_HPO_GENE, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)