"""Executor module, implementing facilities for executing quantum programs using Classiq platform."""

import functools
from typing import Optional, Tuple, Union

import more_itertools
from typing_extensions import TypeAlias

from classiq.interface.backend.backend_preferences import BackendPreferencesTypes
from classiq.interface.chemistry.operator import PauliOperators
from classiq.interface.executor.estimation import OperatorsEstimation
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.execution_request import (
    EstimateOperatorsExecution,
    ExecutionRequest,
    QuantumCodeExecution,
)
from classiq.interface.executor.execution_result import (
    ResultsCollection,
    SavedResultValueType,
    TaggedEstimationResult,
    TaggedExecutionDetails,
)
from classiq.interface.executor.quantum_code import MultipleArguments, QuantumCode
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.executor.result import ExecutionDetails
from classiq.interface.generator.quantum_program import QuantumProgram

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import syncify_function
from classiq.execution.jobs import ExecutionJob
from classiq.synthesis import SerializedQuantumProgram

DEFAULT_RESULT_NAME = "result"

BatchExecutionResult: TypeAlias = Union[ExecutionDetails, BaseException]
ProgramAndResult: TypeAlias = Tuple[QuantumCode, BatchExecutionResult]
BackendPreferencesAndResult: TypeAlias = Tuple[
    BackendPreferencesTypes, int, BatchExecutionResult
]
_MAX_ARGUMENTS_SIZE = 1024


def _parse_serialized_qprog(
    quantum_program: SerializedQuantumProgram,
) -> QuantumProgram:
    return QuantumProgram.parse_raw(quantum_program)


async def execute_async(quantum_program: SerializedQuantumProgram) -> ExecutionJob:
    circuit = _parse_serialized_qprog(quantum_program)
    result = await ApiWrapper.call_execute_generated_circuit(circuit)
    return ExecutionJob(details=result)


execute = syncify_function(execute_async)


async def _execute_qnn_async_estimate(
    quantum_program: QuantumCode,
    execution_preferences: ExecutionPreferences,
    observables: PauliOperators,
) -> ResultsCollection:
    request = ExecutionRequest(
        execution_payload=EstimateOperatorsExecution(
            quantum_program=quantum_program,
            operators=observables,
        ),
        preferences=execution_preferences,
    )

    results = await ApiWrapper.call_execute_estimate(request)
    return [
        TaggedEstimationResult(
            name=DEFAULT_RESULT_NAME,
            value=result,
            value_type=SavedResultValueType.EstimationResult,
        )
        for result in results
    ]


async def _execute_qnn_async_program(
    quantum_program: QuantumCode,
    execution_preferences: ExecutionPreferences,
) -> ResultsCollection:
    request = ExecutionRequest(
        execution_payload=QuantumCodeExecution(**quantum_program.dict()),
        preferences=execution_preferences,
    )

    api_result = await ApiWrapper.call_execute_quantum_program(request)
    return [
        TaggedExecutionDetails(
            name=DEFAULT_RESULT_NAME,
            value=result,
            value_type=SavedResultValueType.ExecutionDetails,
        )
        for result in api_result.details
    ]


async def execute_qnn_async(
    quantum_program: SerializedQuantumProgram,
    arguments: MultipleArguments,
    observables: Optional[PauliOperators] = None,
) -> ResultsCollection:
    circuit = _parse_serialized_qprog(quantum_program)
    execution_preferences = circuit.model.execution_preferences

    legacy_quantum_program = circuit.to_program()

    if observables:
        execute_function = functools.partial(
            _execute_qnn_async_estimate,
            execution_preferences=execution_preferences,
            observables=observables,
        )
    else:
        execute_function = functools.partial(
            _execute_qnn_async_program,
            execution_preferences=execution_preferences,
        )

    result: ResultsCollection = []
    for chunk in more_itertools.chunked(arguments, _MAX_ARGUMENTS_SIZE):
        legacy_quantum_program.arguments = tuple(chunk)
        chunk_result = await execute_function(quantum_program=legacy_quantum_program)
        result.extend(chunk_result)
    return result


execute_qnn = syncify_function(execute_qnn_async)


def set_quantum_program_execution_preferences(
    quantum_program: SerializedQuantumProgram,
    preferences: ExecutionPreferences,
) -> SerializedQuantumProgram:
    circuit = _parse_serialized_qprog(quantum_program)
    circuit.model.execution_preferences = preferences
    return SerializedQuantumProgram(circuit.json())


def set_initial_values(
    quantum_program: SerializedQuantumProgram,
    **kwargs: int,
) -> SerializedQuantumProgram:
    circuit = _parse_serialized_qprog(quantum_program)
    circuit.initial_values = kwargs

    # Validate the initial values by calling `get_registers_initialization`
    circuit.get_registers_initialization(circuit.initial_values)

    return SerializedQuantumProgram(circuit.json())


__all__ = [
    "QuantumCode",
    "QuantumInstructionSet",
    "execute_qnn",
    "OperatorsEstimation",
    "set_quantum_program_execution_preferences",
    "set_initial_values",
]
