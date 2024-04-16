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

import importlib as mprt
import inspect as spct
import types as t

from pyvispr.constant.catalog import (
    ACTUAL_SOURCE,
    FUNCTION_NAME,
    INPUT_II_NAMES,
    NODE_NAME,
    OUTPUT_NAMES,
)
from pyvispr.extension.function import function_t
from pyvispr.extension.string_ import SplitAndStriped


def N_A_F_A(
    description: str, default_name: str, /
) -> tuple[str, str | None, str, str | None, str | None]:
    """"""
    description = dict(SplitAndStriped(_lne, ":") for _lne in description.splitlines())

    return (
        description.get(NODE_NAME, default_name),
        description.get(ACTUAL_SOURCE),
        description.get(FUNCTION_NAME, default_name),
        description.get(INPUT_II_NAMES),
        description.get(OUTPUT_NAMES),
    )


def AllFunctions(
    module_name: str, /, *, recursively: bool = False
) -> tuple[function_t | None, ...]:
    """"""
    module = mprt.import_module(module_name)
    if recursively:
        output = []
        modules = []
        _AllFunctionsRecursively(f"{module_name}.", module, modules, output)
    else:
        output = _AllFunctions(module)
        if output.__len__() == 0:
            modules = []
            _AllFunctionsRecursively(f"{module_name}.", module, modules, output)

    return tuple(output)


def _AllFunctions(module: t.ModuleType, /) -> list[function_t | None]:
    """"""
    output = []

    for name in dir(module):
        if name[0] == "_":
            continue

        element = getattr(module, name)
        if (is_function := spct.isfunction(element)) or hasattr(element, "__call__"):
            if is_function:
                function = element
            else:
                function = element.__call__
            output.append(function_t.NewFromInstance(function, name, module))

    return output


def _AllFunctionsRecursively(
    prefix: str,
    module: t.ModuleType,
    modules: list[t.ModuleType],
    output: list[function_t | None],
    /,
) -> None:
    """"""
    modules.append(module)

    OnlyModulesOrFunctions = lambda _arg: spct.ismodule(_arg) or spct.isfunction(_arg)
    for name, element in spct.getmembers(module, OnlyModulesOrFunctions):
        # Explicitly defined: spct.getmodule(function) == module
        if name[0] == "_":
            continue

        if spct.ismodule(element):
            if element not in modules:
                _AllFunctionsRecursively(prefix, element, modules, output)
        elif module.__name__.startswith(prefix):
            output.append(function_t.NewFromInstance(element, name, module))
