# flake8: noqa

from typing import Dict, List, Mapping, Optional, Type

from classiq.interface.chemistry.fermionic_operator import (
    FermionicOperator,
    SummedFermionicOperator,
)
from classiq.interface.chemistry.ground_state_problem import (
    CHEMISTRY_PROBLEMS_TYPE,
    HamiltonianProblem,
    MoleculeProblem,
)
from classiq.interface.chemistry.molecule import Atom
from classiq.interface.generator.expressions.enums.chemistry import (
    Element,
    FermionMapping,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    ClassicalType,
    Real,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_lambda_function import QuantumLambdaFunction

from classiq.applications.chemistry.ansatz_parameters import (
    AnsatzParameters,
    HEAParameters,
    HVAParameters,
    UCCParameters,
)
from classiq.applications.chemistry.chemistry_execution_parameters import (
    ChemistryExecutionParameters,
)
from classiq.exceptions import ClassiqError

_LADDER_OPERATOR_TYPE_INDICATOR_TO_QMOD_MAPPING: Dict[str, str] = {
    "+": "PLUS",
    "-": "MINUS",
}

_CHEMISTRY_PROBLEM_PREFIX_MAPPING: Dict[Type[CHEMISTRY_PROBLEMS_TYPE], str] = {
    MoleculeProblem: "molecule",
    HamiltonianProblem: "fock_hamiltonian",
}

_ANSATZ_PARAMETERS_FUNCTION_NAME_MAPPING: Dict[Type[AnsatzParameters], str] = {
    UCCParameters: "ucc",
    HVAParameters: "hva",
}

_EXECUTION_RESULT = "vqe_result"
_MOLECULE_PROBLEM_RESULT = "molecule_result"

_HAE_GATE_MAPPING: Dict[str, QuantumFunctionCall] = {
    "h": QuantumFunctionCall(
        function="H",
        inouts={"target": HandleBinding(name="q")},
    ),
    "x": QuantumFunctionCall(
        function="X",
        inouts={"target": HandleBinding(name="q")},
    ),
    "y": QuantumFunctionCall(
        function="Y",
        inouts={"target": HandleBinding(name="q")},
    ),
    "z": QuantumFunctionCall(
        function="Z",
        inouts={"target": HandleBinding(name="q")},
    ),
    "i": QuantumFunctionCall(
        function="I",
        inouts={"target": HandleBinding(name="q")},
    ),
    "s": QuantumFunctionCall(
        function="S",
        inouts={"target": HandleBinding(name="q")},
    ),
    "t": QuantumFunctionCall(
        function="T",
        inouts={"target": HandleBinding(name="q")},
    ),
    "sdg": QuantumFunctionCall(
        function="SDG",
        inouts={"target": HandleBinding(name="q")},
    ),
    "tdg": QuantumFunctionCall(
        function="TDG",
        inouts={"target": HandleBinding(name="q")},
    ),
    "p": QuantumFunctionCall(
        function="PHASE",
        inouts={"target": HandleBinding(name="q")},
    ),
    "rx": QuantumFunctionCall(
        function="RX",
        params={"theta": Expression(expr="angle")},
        inouts={"target": HandleBinding(name="q")},
    ),
    "ry": QuantumFunctionCall(
        function="RY",
        params={"theta": Expression(expr="angle")},
        inouts={"target": HandleBinding(name="q")},
    ),
    "rz": QuantumFunctionCall(
        function="RZ",
        params={"theta": Expression(expr="angle")},
        inouts={"target": HandleBinding(name="q")},
    ),
    "rxx": QuantumFunctionCall(
        function="RXX",
        params={"theta": Expression(expr="angle")},
        inouts={"target": HandleBinding(name="q")},
    ),
    "ryy": QuantumFunctionCall(
        function="RYY",
        params={"theta": Expression(expr="angle")},
        inouts={"target": HandleBinding(name="q")},
    ),
    "rzz": QuantumFunctionCall(
        function="RZZ",
        params={"theta": Expression(expr="angle")},
        inouts={"target": HandleBinding(name="q")},
    ),
    "ch": QuantumFunctionCall(
        function="CH",
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "cx": QuantumFunctionCall(
        function="CX",
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "cy": QuantumFunctionCall(
        function="CY",
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "cz": QuantumFunctionCall(
        function="CZ",
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "crx": QuantumFunctionCall(
        function="CRX",
        params={"theta": Expression(expr="angle")},
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "cry": QuantumFunctionCall(
        function="CRY",
        params={"theta": Expression(expr="angle")},
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "crz": QuantumFunctionCall(
        function="CRZ",
        params={"theta": Expression(expr="angle")},
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "cp": QuantumFunctionCall(
        function="CPHASE",
        params={"theta": Expression(expr="angle")},
        inouts={
            "target": HandleBinding(name="q1"),
            "control": HandleBinding(name="q2"),
        },
    ),
    "swap": QuantumFunctionCall(
        function="SWAP",
        inouts={"qbit0": HandleBinding(name="q1"), "qbit1": HandleBinding(name="q2")},
    ),
}


def _atoms_to_qmod_atoms(atoms: List[Atom]) -> str:
    # fmt: off
    atom_struct_literals = [
        "struct_literal(ChemistryAtom,"
            f"element={Element[atom.symbol]},"
            "position=struct_literal(Position,"
                f"x={atom.x},"
                f"y={atom.y},"
                f"z={atom.z}"
            ")"
        ")"
        for atom in atoms
    ]
    # fmt: on
    return ",".join(atom_struct_literals)


def molecule_problem_to_qmod(
    molecule_problem: MoleculeProblem,
) -> str:
    # fmt: off
    return (
        "struct_literal("
        "MoleculeProblem,"
        f"mapping={FermionMapping[molecule_problem.mapping.value.upper()]},"
        f"z2_symmetries={molecule_problem.z2_symmetries},"
        "molecule=struct_literal("
        "Molecule,"
        f"atoms=[{_atoms_to_qmod_atoms(molecule_problem.molecule.atoms)}],"
        f"spin={molecule_problem.molecule.spin},"
        f"charge={molecule_problem.molecule.charge}"
        "),"
        f"freeze_core={molecule_problem.freeze_core},"
        f"remove_orbitals={molecule_problem.remove_orbitals}"
        ")")
    # fmt: on


def _fermionic_operator_to_qmod_ladder_ops(
    fermionic_operator: FermionicOperator,
) -> str:
    return "\n\t\t\t\t\t".join(
        [
            f"struct_literal(LadderOp, op=LadderOperator.{_LADDER_OPERATOR_TYPE_INDICATOR_TO_QMOD_MAPPING[ladder_op[0]]}, index={ladder_op[1]}),"
            for ladder_op in fermionic_operator.op_list
        ]
    )[:-1]


def _summed_fermionic_operator_to_qmod_lader_terms(
    hamiltonian: SummedFermionicOperator,
) -> str:
    return "\t\t".join(
        [
            # fmt: off
            f"""
            struct_literal(LadderTerm,
                coefficient={fermionic_operator[1]},
                ops=[
                    {_fermionic_operator_to_qmod_ladder_ops(fermionic_operator[0])}
                ]
            ),"""
            for fermionic_operator in hamiltonian.op_list
            # fmt: on
        ]
    )[:-1]


def _hamiltonian_problem_to_qmod_fock_hamiltonian_problem(
    hamiltonian_problem: HamiltonianProblem,
) -> str:
    return (
        # fmt: off
        "struct_literal("
        "FockHamiltonianProblem,"
        f"mapping={FermionMapping[hamiltonian_problem.mapping.value.upper()]},"
        f"z2_symmetries={hamiltonian_problem.z2_symmetries},"
        f"terms=[{_summed_fermionic_operator_to_qmod_lader_terms(hamiltonian_problem.hamiltonian)}],"
        f"num_particles={hamiltonian_problem.num_particles}"
        ")"
        # fmt: on
    )


def _convert_library_problem_to_qmod_problem(problem: CHEMISTRY_PROBLEMS_TYPE) -> str:
    if isinstance(problem, MoleculeProblem):
        return molecule_problem_to_qmod(problem)
    elif isinstance(problem, HamiltonianProblem):
        return _hamiltonian_problem_to_qmod_fock_hamiltonian_problem(problem)
    else:
        raise ClassiqError(f"Invalid problem type: {problem}")


def _get_chemistry_function(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    chemistry_function_name: str,
    inouts: Mapping[IOName, HandleBinding],
    ansatz_parameters_expressions: Optional[Dict[str, Expression]] = None,
) -> QuantumFunctionCall:
    problem_prefix = _CHEMISTRY_PROBLEM_PREFIX_MAPPING[type(chemistry_problem)]
    return QuantumFunctionCall(
        function=f"{problem_prefix}_{chemistry_function_name}",
        params={
            f"{problem_prefix}_problem": Expression(
                expr=_convert_library_problem_to_qmod_problem(chemistry_problem)
            ),
            **(ansatz_parameters_expressions or dict()),
        },
        inouts=inouts,
    )


def _get_hartree_fock(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
) -> QuantumFunctionCall:
    return _get_chemistry_function(
        chemistry_problem,
        "hartree_fock",
        {"qbv": HandleBinding(name="qbv")},
    )


def _get_hea_function(hea_parameters: HEAParameters) -> QuantumFunctionCall:
    return QuantumFunctionCall(
        function="full_hea",
        params={
            "num_qubits": Expression(expr=f"{hea_parameters.num_qubits}"),
            "is_parametrized": Expression(
                expr=f"{[int(_is_parametric_gate(_HAE_GATE_MAPPING[gate])) for gate in hea_parameters.one_qubit_gates+hea_parameters.two_qubit_gates]}"
            ),
            "angle_params": Expression(expr="t"),
            "connectivity_map": Expression(
                expr=f"{[list(connectivity_pair) for connectivity_pair in hea_parameters.connectivity_map]}"
            ),
            "reps": Expression(expr=f"{hea_parameters.reps}"),
        },
        operands={
            "operands_1qubit": [
                QuantumLambdaFunction(body=[_HAE_GATE_MAPPING[gate]])
                for gate in hea_parameters.one_qubit_gates
            ],
            "operands_2qubit": [
                QuantumLambdaFunction(body=[_HAE_GATE_MAPPING[gate]])
                for gate in hea_parameters.two_qubit_gates
            ],
        },
        inouts={"x": HandleBinding(name="qbv")},
    )


def _get_ansatz(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    ansatz_parameters: AnsatzParameters,
) -> QuantumFunctionCall:
    if isinstance(ansatz_parameters, HEAParameters):
        return _get_hea_function(ansatz_parameters)
    return _get_chemistry_function(
        chemistry_problem,
        _ANSATZ_PARAMETERS_FUNCTION_NAME_MAPPING[type(ansatz_parameters)],
        {"qbv": HandleBinding(name="qbv")},
        {
            param_name: Expression(expr=str(param_value))
            for param_name, param_value in ansatz_parameters.__dict__.items()
        },
    )


def _get_chemistry_vqe_additional_params(
    execution_parameters: ChemistryExecutionParameters,
) -> str:
    return f"""maximize=False,
initial_point={execution_parameters.initial_point or list()},
optimizer=Optimizer.{execution_parameters.optimizer.value},
max_iteration={execution_parameters.max_iteration},
tolerance={execution_parameters.tolerance or 0},
step_size={execution_parameters.step_size or 0},
skip_compute_variance={execution_parameters.skip_compute_variance},
alpha_cvar=1.0,
"""


def _get_molecule_problem_execution_post_processing(
    molecule_problem: MoleculeProblem,
) -> str:
    return f"""
{_MOLECULE_PROBLEM_RESULT} = molecule_ground_state_solution_post_process({molecule_problem_to_qmod(molecule_problem)},{_EXECUTION_RESULT})
save({{{_MOLECULE_PROBLEM_RESULT!r}: {_MOLECULE_PROBLEM_RESULT}}})
"""


def _is_parametric_gate(call: QuantumFunctionCall) -> bool:
    return len(call.params) > 0


def _get_execution_result_post_processing_statements(
    problem: CHEMISTRY_PROBLEMS_TYPE,
) -> str:
    if isinstance(problem, MoleculeProblem):
        return _get_molecule_problem_execution_post_processing(problem)
    elif isinstance(problem, HamiltonianProblem):
        return ""
    else:
        raise ClassiqError(f"Invalid problem type: {problem}")


def _count_parametric_gates(gates: List[str]) -> int:
    return sum(_is_parametric_gate(_HAE_GATE_MAPPING[gate]) for gate in gates)


def _get_hea_port_size(hea_parameters: HEAParameters) -> int:
    return hea_parameters.reps * (
        hea_parameters.num_qubits
        * _count_parametric_gates(hea_parameters.one_qubit_gates)
        + len(hea_parameters.connectivity_map)
        * _count_parametric_gates(hea_parameters.two_qubit_gates)
    )


def _get_chemistry_quantum_main_params(
    ansatz_parameters: AnsatzParameters,
) -> Dict[str, ClassicalType]:
    if not isinstance(ansatz_parameters, HEAParameters):
        return dict()
    return {
        "t": ClassicalArray(
            element_type=Real(), size=_get_hea_port_size(ansatz_parameters)
        )
    }


def _get_problem_to_hamiltonian_name(chemistry_problem: CHEMISTRY_PROBLEMS_TYPE) -> str:
    problem_prefix = _CHEMISTRY_PROBLEM_PREFIX_MAPPING[type(chemistry_problem)]
    return f"{problem_prefix}_problem_to_hamiltonian"


def _get_chemistry_quantum_main(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    use_hartree_fock: bool,
    ansatz_parameters: AnsatzParameters,
) -> NativeFunctionDefinition:
    body = []
    body.append(
        QuantumFunctionCall(
            function="allocate",
            positional_args=[
                Expression(
                    expr=f"get_field(get_field({_get_problem_to_hamiltonian_name(chemistry_problem)}({_convert_library_problem_to_qmod_problem(chemistry_problem)})[0], 'pauli'), 'len')"
                ),
                HandleBinding(name="qbv"),
            ],
        ),
    )
    if use_hartree_fock:
        body.append(_get_hartree_fock(chemistry_problem))

    body.append(_get_ansatz(chemistry_problem, ansatz_parameters))

    return NativeFunctionDefinition(
        name="main",
        param_decls=_get_chemistry_quantum_main_params(ansatz_parameters),
        port_declarations=(
            {
                "qbv": PortDeclaration(
                    name="qbv", direction=PortDeclarationDirection.Output
                )
            }
        ),
        body=body,
    )


def _get_chemistry_classical_code(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    execution_parameters: ChemistryExecutionParameters,
) -> str:
    qmod_problem = _convert_library_problem_to_qmod_problem(chemistry_problem)
    return f"""
{_EXECUTION_RESULT} = vqe(
    hamiltonian={_get_problem_to_hamiltonian_name(chemistry_problem)}({qmod_problem}), {_get_chemistry_vqe_additional_params(execution_parameters)}
)
save({{{_EXECUTION_RESULT!r}: {_EXECUTION_RESULT}}})
""" + _get_execution_result_post_processing_statements(
        chemistry_problem
    )


def construct_chemistry_model(
    chemistry_problem: CHEMISTRY_PROBLEMS_TYPE,
    use_hartree_fock: bool,
    ansatz_parameters: AnsatzParameters,
    execution_parameters: ChemistryExecutionParameters,
) -> SerializedModel:
    model = Model(
        functions=[
            _get_chemistry_quantum_main(
                chemistry_problem, use_hartree_fock, ansatz_parameters
            ),
        ],
        classical_execution_code=_get_chemistry_classical_code(
            chemistry_problem, execution_parameters
        ),
    )
    return model.get_model()
