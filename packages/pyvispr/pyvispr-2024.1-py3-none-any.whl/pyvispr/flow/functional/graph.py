# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2017)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import typing as h

from pyvispr.flow.functional.node_linked import node_t


@dtcl.dataclass(repr=False, eq=False)
class graph_t(list[node_t]):
    """
    Cannot be sloted because of QThread issue with weak reference (see visual.graph).
    """

    next_node_uid: int = 1

    def AddNode(self, node: node_t, /) -> None:
        """"""
        node.SetUniqueName(self.next_node_uid)
        self.next_node_uid += 1
        self.append(node)

    def AddLink(
        self, source: node_t, output_name: str, target: node_t, input_name: str, /
    ) -> None:
        """"""
        source.AddLink(output_name, target, input_name)
        self.InvalidateNodesInCascadeFromNode(target)

    def RemoveNode(self, node: node_t, /) -> None:
        """"""
        self.InvalidateNodesInCascadeFromNode(node)

        node.RemoveLink(None, None, None)
        for predecessor in self._PredecessorsOfNode(node):
            for output_name in predecessor.outputs:
                predecessor.RemoveLink(output_name, node, None)

        self.remove(node)
        if self.__len__() == 0:
            self.next_node_uid = 1

    def RemoveLink(
        self,
        source: node_t,
        output_name: str | None,
        target: node_t,
        input_name: str | None,
        /,
    ) -> None:
        """
        Removes one or several links assuming that the link(s) exist(s).
        """
        self.InvalidateNodesInCascadeFromNode(target)

        if output_name is None:
            output_names = source.outputs  # Will be iterated, so equivalent to .keys().
        else:
            output_names = (output_name,)
        for output_name in output_names:
            source.RemoveLink(output_name, target, input_name)

    def _PredecessorsOfNode(
        self, target: node_t, /, *, input_name: str | None = None
    ) -> tuple[node_t, ...]:
        """"""
        output = set()

        for node in self:
            if input_name is None:
                if target in node.links:
                    output.add(node)
            elif (target, input_name) in node.links:
                return (node,)

        if input_name is None:
            return tuple(output)

        return ()

    def InvalidateNodesInCascadeFromNode(
        self, origin_node: node_t, /, *, barrier_node: node_t = None
    ) -> None:
        """
        Reasons for invalidating from origin_node:
            - origin_node is about to be deleted
            - some input links have been added or deleted
            - some inputs have been modified
        """
        nodes_to_be_invalidated = [origin_node]
        invalidated_nodes = []  # Useful only in presence of cycles.

        while len(nodes_to_be_invalidated) > 0:
            successors = []
            node_idc = map(lambda _elm: self.index(_elm), nodes_to_be_invalidated)

            for node_idx, node in zip(node_idc, nodes_to_be_invalidated):
                if (barrier_node is not None) and (node is barrier_node):
                    continue

                node.InvalidateOutputValues()
                for links in node.links.values():
                    for node_tgt, input_name in links:
                        node_tgt.InvalidateInputValue(name=input_name)
                        if not (
                            (node_tgt in successors) or (node_tgt in invalidated_nodes)
                        ):
                            successors.append(node_tgt)
                invalidated_nodes.append(node)

            nodes_to_be_invalidated = successors

    def InvalidateAllNodes(self) -> None:
        """"""
        for node in self:
            if not node.needs_running:
                self.InvalidateNodesInCascadeFromNode(node)

            if all(_nde.needs_running for _nde in self):
                break

    def Run(self, /, *, script_accessor: h.TextIO = None) -> set[node_t]:
        """"""
        nodes_to_be_run = set(filter(lambda _elm: _elm.needs_running, self))
        should_save_as_script = script_accessor is not None

        while (n_to_be_run := nodes_to_be_run.__len__()) > 0:
            runnable_nodes = tuple(filter(lambda _elm: _elm.can_run, nodes_to_be_run))
            if runnable_nodes.__len__() == 0:
                break

            for node in runnable_nodes:
                output_names = node.description.output_names
                n_outputs = output_names.__len__()

                if should_save_as_script and (n_outputs > 0):
                    if n_outputs > 1:
                        for idx in range(n_outputs - 1):
                            script_accessor.write(
                                node.UniqueOutputName(output_names[idx]) + ", "
                            )
                    script_accessor.write(
                        node.UniqueOutputName(output_names[-1]) + " = "
                    )

                node.Run(script_accessor=script_accessor)
                node.SendOutputsToSuccessors()

            nodes_to_be_run.difference_update(runnable_nodes)

        if (n_to_be_run > 0) and should_save_as_script:
            script_accessor.write(
                'print("Workflow saving was incomplete due to some nodes not being runnable.")'
            )

        return nodes_to_be_run
