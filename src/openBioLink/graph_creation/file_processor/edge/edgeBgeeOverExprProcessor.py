from ..fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.edge.inMetaEdgeBgeeOverExpr import InMetaEdgeBgeeOverExpr


class EdgeBgeeOverExprProcessor(FileProcessor):
    IN_META_CLASS= InMetaEdgeBgeeOverExpr

    def __init__(self):
        self.use_cols =   self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_BGEE_DIFF,
                         infileType=InfileType.IN_EDGE_BGEE_OVEREXPR, mapping_sep= self.IN_META_CLASS.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.differential_expr == 'over-expression']
        return data