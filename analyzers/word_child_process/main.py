
from typing import Any

from grapl_analyzerlib.execution import ExecutionHit
from pydgraph import DgraphClient
from grapl_analyzerlib.entities import ProcessQuery, SubgraphView


def analyzer(client: DgraphClient, graph: SubgraphView, sender: Any):

    # commonly targeted applications
    # TODO: Adobe Reader

    ctas = ["winword.exe", "excel.exe"]

    for process in graph.process_iter():
        p = (
            ProcessQuery()
            .with_process_name(ends_with=ctas)
            .with_children(ProcessQuery())
            .query_first(client, contains_node_key=process.node_key)
        )

        if p:
            sender.send(
                ExecutionHit(
                    analyzer_name="Common Target Application With Child Process",
                    node_view=p,
                    risk_score=100,
                )
            )