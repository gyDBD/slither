"""
Module detecting initialize function

A initialization function is an unprotected function that does not check the caller(msg.sender)
"""
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
class FunctionAuth(AbstractDetector):
    """
    Unprotected function detector
    """
    ARGUMENT = 'function-auth'
    HELP = 'Functions set sensitive state variables without check the authentication'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH
    #do not have wiki now
    WIKI = 'https://github.com/trailofbits/slither/wiki'

    @staticmethod
    def detect_func_visibile(func, contract):
        """ Detect if the function is visible
        1. public or external, which means that it can be invoked directly from outside;
        2. private or internal but are invoked / reachable from some public or external functions (entrance).

        Returns:
            (bool): True if the function is visible
        """
        # functions_reachable = contract.all_functions_called()
        if func.visibility in ["public", "external"]:
            return True
        # elif func.visibility in ["private", "internal"] and func in functions_reachable:
        #     return True
        return False

    @staticmethod
    def detect_set_sensitive_func(func, clas):
        """ Detect if the function includes setting sensitive state variables
        which are the ones that are either checked by some requirement statements or appear in some modifier definitions

        Returns:
            (bool): True if the function is a function is setting sensitive state variables.
        TODO: need to check requirement statements not just conditional
        """

        # state_variables_written = [v.name for v in func.all_state_variables_written()]
        # #require_state_variables_read = [v.name for v in func.is_reading_in_require()]
        # conditional_vars = func.all_conditional_solidity_variables_read(include_loop=False)
        # args_vars = func.all_solidity_variables_used_as_args()
        state_variables_written = [v.name for v in func.all_state_variables_written()]
        conditional_state_variables_read = [v.name for v in func.all_conditional_state_variables_read()]
        intersection = list(set(state_variables_written)&set(conditional_state_variables_read))
        if intersection:
            assignment = func.get_assginment()
            assignments = assignment.split("\n")
            for assign in assignments:
                split_result = assign.split("=")
                right = split_result[len(split_result) - 1].replace(" ","").replace("\t","")
                clas.log(right)
                left = split_result[0].replace(" ","").replace("\t","")
                clas.log(left)
                if left in intersection and right in ["msg.sender", "tx.origin"]:
                    return True

        return False


    def detect(self):
        """ Detect the unprotected setting sensitive state variables function
        """
        results = []
        for contract in self.contracts:
            # Check if a function set sensitive state variables and not check the auth
            for f in contract.functions:
                if f.is_constructor or not self.detect_func_visibile(f, contract) :
                    continue
                if f.is_implemented and self.detect_set_sensitive_func(f, self):
                    self.log("fsdfasdfasdf")
                    # Info to be printed
                    info = 'Setting sensitive state variables function without checking the auth found in {}.{} ({})\n'
                    info = info.format(contract.name, f.name, f.source_mapping_str)
                    # Print the info
                    self.log(info)
                    # Add the result in result
                    json = self.generate_json_result(info)
                    self.add_function_to_json(f, json)
                    results.append(json)

        return results