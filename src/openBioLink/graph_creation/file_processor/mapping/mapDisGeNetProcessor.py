from ...metadata_infile.mapping.inMetaMapDisGeNet import InMetaMapDisGeNet

from ...types.readerType import ReaderType
from ...file_processor.fileProcessor import FileProcessor
from ...types.infileType import InfileType


class MapDisGeNetProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapDisGeNet

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_MAP_DISGENET,
                         infileType=InfileType.IN_MAP_DISGENET, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_preprocessing(self, data):
        # making ids unique in DisGeNet mapping file for DO and OMIM (metadata_db_file:id)
        data.loc[data['voc'] == 'DO', 'code'] = 'DOID:' + data[data['voc'] == 'DO']['code']
        data = data[data['voc'] == 'DO']

        return data


