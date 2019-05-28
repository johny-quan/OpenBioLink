from ..fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.edge.inMetaEdgeDrugCentralContraInd import InMetaEdgeDrugCentralContraInd



class EdgeDrugCentralIndProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeDrugCentralContraInd

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_DRUGCENTRAL_IND,
                         infileType=InfileType.IN_EDGE_DRUGCENTRAL_CONTRA_IND, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.relationship_name == 'contraindication']
        return data