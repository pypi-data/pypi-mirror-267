from typing import TYPE_CHECKING, Optional

import pydantic
from sympy import Equality
from sympy.core.numbers import Integer

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.qmod_qscalar_proxy import (
    QmodQNumProxy,
    QmodSizedProxy,
)
from classiq.interface.model.quantum_expressions.control_state import (
    min_bit_length,
    to_twos_complement,
)
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumExpressionOperation,
)

from classiq.exceptions import ClassiqValueError

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock

CONTROL_INOUT_NAME = "ctrl"
CONTROL_CTRL_ARG_ERROR_MESSAGE_FORMAT = (
    "control condition must be of the form '<quantum-variable> == "
    "<classical-integer-expression>', but condition's {}-hand side was {!r}"
)


class Control(QuantumExpressionOperation):
    body: "StatementBlock"
    _ctrl: Optional[QmodSizedProxy] = pydantic.PrivateAttr(
        default=None,
    )
    _ctrl_val: Optional[int] = pydantic.PrivateAttr(
        default=None,
    )

    @property
    def condition(self) -> Expression:
        return self.expression

    @property
    def ctrl(self) -> QmodSizedProxy:
        assert self._ctrl is not None
        return self._ctrl

    @property
    def ctrl_val(self) -> int:
        assert self._ctrl_val is not None
        return self._ctrl_val

    def resolve_condition(self) -> None:
        condition = self.condition.value.value
        if isinstance(condition, QmodSizedProxy):
            self._resolve_port_condition(condition)
        elif isinstance(condition, Equality):
            self._resolve_num_condition(condition)
        else:
            raise ClassiqValueError(
                f"control condition must be a qubit, an array of qubits, or a quantum "
                f"numeric equality, was {str(condition)!r}"
            )

    def _resolve_port_condition(self, condition: QmodSizedProxy) -> None:
        self._ctrl = condition

    def _resolve_num_condition(self, condition: Equality) -> None:
        ctrl, ctrl_val = condition.args
        if isinstance(ctrl, Integer) and isinstance(ctrl_val, QmodQNumProxy):
            ctrl, ctrl_val = ctrl_val, ctrl
        if not isinstance(ctrl, QmodQNumProxy):
            raise ClassiqValueError(
                CONTROL_CTRL_ARG_ERROR_MESSAGE_FORMAT.format("left", str(ctrl))
            )
        if not isinstance(ctrl_val, Integer):
            raise ClassiqValueError(
                CONTROL_CTRL_ARG_ERROR_MESSAGE_FORMAT.format("right", str(ctrl_val))
            )
        self._ctrl, self._ctrl_val = ctrl, int(ctrl_val)

    @property
    def has_ctrl_state(self) -> bool:
        assert self._ctrl is not None
        return self._ctrl_val is not None

    @property
    def ctrl_state(self) -> str:
        ctrl = self.ctrl
        assert isinstance(ctrl, QmodQNumProxy)
        is_signed = ctrl.is_signed
        fraction_places = ctrl.fraction_digits
        ctrl_size = len(ctrl)
        if not is_signed and self.ctrl_val < 0:
            raise ClassiqValueError(
                f"Variable {str(ctrl)!r} is not signed but control value "
                f"{self.ctrl_val} is negative"
            )
        required_qubits = min_bit_length(self.ctrl_val, is_signed)
        if ctrl_size < required_qubits:
            raise ClassiqValueError(
                f"Variable {str(ctrl)!r} has {ctrl_size} qubits but control value "
                f"{str(self.ctrl_val)!r} requires at least {required_qubits} qubits"
            )
        if fraction_places != 0:
            raise ClassiqValueError(
                f"Comparison (`==`) on a non-integer quantum variable {str(ctrl)!r} is "
                f"not supported at the moment"
            )
        return to_twos_complement(self.ctrl_val, ctrl_size, is_signed)
