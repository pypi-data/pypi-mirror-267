from typing import Optional

from panel import Tabs
from panel.widgets import TooltipIcon

from atap_corpus_loader.controller import Controller
from atap_corpus_loader.view.gui import AbstractWidget, FileLoaderWidget, CorpusInfoWidget
from atap_corpus_loader.view.tooltips import TooltipManager


class ViewWrapperWidget(AbstractWidget):
    """
    A wrapper class that holds different loading method interfaces within a Tab
    """
    def __init__(self, controller: Controller, include_meta_loader: bool):
        super().__init__()
        self.controller: Controller = controller
        self.tooltip_manager: TooltipManager = TooltipManager()

        self.file_loader: FileLoaderWidget = FileLoaderWidget(self, controller, include_meta_loader)
        self.corpus_display: CorpusInfoWidget = CorpusInfoWidget(controller)

        self.panel = Tabs(("File Loader", self.file_loader),
                          ("Corpus Overview", self.corpus_display))
        self.corpus_info_idx: int = len(self.panel) - 1
        self.children = [self.file_loader, self.corpus_display]

    def update_display(self):
        pass

    def load_corpus_from_filepaths(self, filepath_ls: list[str], include_hidden: bool):
        if len(filepath_ls) == 0:
            return
        success = self.controller.load_corpus_from_filepaths(filepath_ls, include_hidden)
        self.update_displays()
        if success:
            self.controller.display_success("Corpus files loaded successfully")

    def load_meta_from_filepaths(self, filepath_ls: list[str], include_hidden: bool):
        if len(filepath_ls) == 0:
            return
        success = self.controller.load_meta_from_filepaths(filepath_ls, include_hidden)
        self.update_displays()
        if success:
            self.controller.display_success("Metadata files loaded successfully")

    def build_corpus(self, corpus_name: str) -> bool:
        success: bool = self.controller.build_corpus(corpus_name)
        if success:
            self.update_displays()

            self.panel.active = self.corpus_info_idx
            corpus_name: str = self.controller.get_latest_corpus().name
            self.controller.display_success(f"Corpus {corpus_name} built successfully")

        return success

    def get_tooltip(self, tooltip_name: str) -> Optional[TooltipIcon]:
        return self.tooltip_manager.get_tooltip(tooltip_name)
