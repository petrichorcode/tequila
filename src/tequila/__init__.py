from tequila.utils import BitString, BitNumbering, BitStringLSB, initialize_bitstring, TequilaException
from tequila.circuit import gates, QCircuit
from tequila.hamiltonian import paulis
from tequila.objective import Objective, ExpectationValue, Variable, assign_variable
from tequila.optimizers import optimizer_scipy
from tequila.simulators import pick_backend
from tequila.wavefunction import QubitWaveFunction
from tequila.simulators import simulate_objective, simulate_wavefunction, sample_objective, sample_wavefunction
import tequila.quantumchemistry as chemistry

from typing import Dict, Union, Hashable
from numbers import Real as RealNumber


def simulate(objective: Objective,
             variables: Dict[Union[Variable, Hashable], RealNumber] = None,
             samples: int = None,
             backend: str = None,
             *args,
             **kwargs) -> Union[RealNumber, QubitWaveFunction]:
    """
    Simulate a tequila objective or circuit
    :param objective: tequila objective or circuit
    :param variables: The variables of the objective given as dictionary
    with keys as tequila Variables and values the corresponding real numbers
    :param samples: if None a full wavefunction simulation is performed, otherwise a fixed number of samples is simulated
    :param backend: specify the backend or give None for automatic assignment
    :return: simulated/sampled objective or simulated/sampled wavefunction
    """
    if variables is None and not (len(objective.extract_variables()) == 0):
        raise TequilaException("You called simulate for a parametrized type but forgot to pass down the variables: {}".format(objective.extract_variables()))
    elif variables is not None:
        # allow hashable types as keys without casting it to variables
        variables = {assign_variable(k): v for k, v in variables.items()}

    if isinstance(objective, Objective) or hasattr(objective, "args"):
        if samples is None:
            return simulate_objective(objective=objective, variables=variables, backend=backend)
        else:
            return sample_objective(objective=objective, variables=variables, samples=samples, backend=backend)
    elif isinstance(objective, QCircuit) or hasattr(objective, "gates"):
        if samples is None:
            return simulate_wavefunction(abstract_circuit=objective, variables=variables, backend=backend, *args, **kwargs)
        else:
            return sample_wavefunction(abstract_circuit=objective, variables=variables, samples=samples, backend=backend, *args, **kwargs)
    else:
        raise TequilaException(
            "Don't know how to simulate object of type: {type}, \n{object}".format(type=type(objective),
                                                                                   object=objective))


__version__ = "AndreasDorn"
