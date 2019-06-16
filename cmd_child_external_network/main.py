
from typing import Any

from pydgraph import DgraphClient

from grapl_analyzerlib.execution import ExecutionHit
from grapl_analyzerlib.entities import ProcessQuery, SubgraphView, ExternalIpQuery


def analyzer(client: DgraphClient, graph: SubgraphView, sender: Any):

    for process in graph.process_iter():

        cmd = ProcessQuery().with_process_name(eq="cmd.exe")

        cmd_child = ProcessQuery().with_parent(cmd)

        cmd_child.with_created_connection(ExternalIpQuery())

        p = cmd_child.query_first(client, contains_node_key=process.node_key)

        if p:
            sender.send(
                ExecutionHit(
                    analyzer_name="Browser Created File",
                    node_view=p,
                    risk_score=5,
                )
            )
