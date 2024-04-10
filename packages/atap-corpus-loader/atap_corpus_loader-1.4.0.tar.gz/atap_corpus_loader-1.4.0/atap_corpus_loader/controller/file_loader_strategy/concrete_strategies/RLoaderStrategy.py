from pandas import DataFrame, concat
from pyreadr import list_objects, read_r
from pyreadr.librdata import PyreadrError, LibrdataError

from atap_corpus_loader.controller.data_objects import CorpusHeader, DataType
from atap_corpus_loader.controller.file_loader_strategy.FileLoadError import FileLoadError
from atap_corpus_loader.controller.file_loader_strategy.FileLoaderStrategy import FileLoaderStrategy


class RLoaderStrategy(FileLoaderStrategy):
    def get_inferred_headers(self) -> list[CorpusHeader]:
        real_path: str = self.file_ref.resolve_real_file_path()

        try:
            file_objects: list[dict] = list_objects(real_path)
        except (PyreadrError, LibrdataError) as e:
            raise FileLoadError(f"Error loading R file: {str(e)}")

        if len(file_objects) == 0:
            return []

        columns = file_objects[0].get('columns')
        for file_object in file_objects[1:]:
            if file_object.get('columns') != columns:
                raise FileLoadError(f"Incompatible headers within loaded R objects")

        if len(columns) == 0:
            raise FileLoadError(f"No tabular data found. Ensure the file contains tabular data (rows and columns)")

        headers: list[CorpusHeader] = []
        dtype: DataType = DataType.TEXT
        for col_name in columns:
            headers.append(CorpusHeader(col_name, dtype))

        return headers

    def get_dataframe(self, headers: list[CorpusHeader]) -> DataFrame:
        real_path: str = self.file_ref.resolve_real_file_path()

        try:
            object_df_dict: dict = read_r(real_path)
        except (PyreadrError, LibrdataError) as e:
            raise FileLoadError(f"Error loading R file: {str(e)}")

        df_list = object_df_dict.values()
        concat_df: DataFrame = concat(df_list, ignore_index=True)
        excluded_headers: list[str] = [header.name for header in headers if not header.include]
        df = concat_df.drop(excluded_headers, axis='columns')
        dtypes_applied_df: DataFrame = FileLoaderStrategy._apply_selected_dtypes(df, headers)

        return dtypes_applied_df
