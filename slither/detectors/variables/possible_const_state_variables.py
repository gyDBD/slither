"""
Module detecting state variables that could be declared as constant
"""

from collections import defaultdict
from slither.core.solidity_types.elementary_type import ElementaryType
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import OperationWithLValue
from slither.core.variables.state_variable import StateVariable
from slither.core.expressions.literal import Literal


class ConstCandidateStateVars(AbstractDetector):
    """
    State variables that could be declared as constant detector.
    Not all types for constants are implemented in Solidity as of 0.4.25.
    The only supported types are value types and strings (ElementaryType).
    Reference: https://solidity.readthedocs.io/en/latest/contracts.html#constant-state-variables
    """

    ARGUMENT = 'constable-states'
    HELP = 'State variables that could be declared constant'
    IMPACT = DetectorClassification.INFORMATIONAL
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = 'https://github.com/trailofbits/slither/wiki/Vulnerabilities-Description#state-variables-that-could-be-declared-constant'

    def lvalues_of_operations_with_lvalue(self):
        """
        Obtains all state variables on the left-hand side of any operations in functions or modifiers.
        :return: Returns a set of state variables which are on the left-hand side of any operations in functions or
        modifiers.
        """
        # Define our results set.
        results = set()

        # Loop for each function node explicitly defined in each contract, and look at all IR to find operations with
        # left hand values that we can extract from, and the left hand side to our set if it is a state variable.
        for contract in self.contracts:
            for function in contract.functions_and_modifiers_not_inherited:
                for node in function.nodes:
                    for ir in node.irs:
                        if isinstance(ir, OperationWithLValue) and isinstance(ir.lvalue, StateVariable):
                            results.add(ir.lvalue)
        return results

    @staticmethod
    def non_const_state_variables(contract):
        """
        Obtains all non-constant state variables explicitly defined in a given contract which are assigned a literal to.
        :param contract: The contract to obtain state variables from
        :return: Returns a list of state variables which are non-constant, accessible from this contract.
        """
        return [variable for variable in contract.state_variables
                if variable.contract == contract and not variable.is_constant and type(variable.expression) == Literal]

    def detect(self):
        """ Detect state variables that could be const
        """
        results = []
        all_info = ''

        # Obtain all state variables that are assigned to in a function/modifier.
        all_assigned = self.lvalues_of_operations_with_lvalue()

        # Loop through each contract and find state variables which were not assigned to.
        for contract in self.contracts:

            # Obtain all non-constant state variables
            candidate_variables = self.non_const_state_variables(contract)

            # Filter the candidates to those that are not assigned to, and are value-types.
            candidate_variables = [candidate for candidate in candidate_variables
                                   if candidate not in all_assigned
                                   and isinstance(candidate.type, ElementaryType)]

            # If we have any candidates remaining, we output them as recommendations to be made constant.
            if candidate_variables:
                info = ''
                for candidate in candidate_variables:
                    info += "{}.{} should be constant ({})\n".format(candidate.contract.name,
                                                                     candidate.name,
                                                                     candidate.source_mapping_str)
                all_info += info
                json = self.generate_json_result(info)
                self.add_variables_to_json(candidate_variables, json)
                results.append(json)

        if all_info != '':
            self.log(all_info)
        return results
