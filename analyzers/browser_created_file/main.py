from typing import Any

from grapl_analyzerlib.analyzer import Analyzer, OneOrMany
from grapl_analyzerlib.entities import ProcessQuery, FileQuery, ProcessView
from grapl_analyzerlib.execution import ExecutionHit
from grapl_analyzerlib.querying import Not, Queryable


class BrowserCreatedFile(Analyzer):

    def get_queries(self) -> OneOrMany[ProcessQuery]:
        return (
            ProcessQuery()
            .with_process_name(eq="firefox.exe")
            .with_process_name(eq="chrome.exe")
            .with_created_files(
                FileQuery()
                .with_file_path(contains=[Not("AppData"), Not("tmp")])
            )
        )

    def on_response(self, response: ProcessView, output: Any):
        output.send(
            ExecutionHit(
                analyzer_name="Browser Created File",
                node_view=response,
                risk_score=5,
            )
        )
