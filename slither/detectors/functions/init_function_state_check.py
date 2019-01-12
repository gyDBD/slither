"""
Module detecting initialize function

A initialization function is an unprotected function that does not
exist a state variable that is properly set during initialization and the variable is checked before the entrance.
"""
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
class InitFunctionState(AbstractDetector):
    """
    Unprotected function detector
    """
    ARGUMENT = 'init-state'
    HELP = 'Functions allowing initialize function without ' \
           'a state variable that is properly set during initialization and the variable is checked before the entrance.'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH
    # do not have wiki now
    WIKI = 'https://github.com/trailofbits/slither/wiki'


    @staticmethod
    def detect_init_func(func):
        """ Detect if the function is unprotected initialize funtion

        Returns:
            (bool): True if the function is an initalize function does not
            exist a state variable that is properly set during initialization and the variable is checked before the entrance.
        """

        state_variables_written = [v.name for v in func.all_state_variables_written()]
        conditional_state_variables_read = [v.name for v in func.all_conditional_state_variables_read()]
        if list(set(state_variables_written)&set(conditional_state_variables_read)):
            return False

        return True

    def detect(self):
        """ Detect the unprotected initialize funtion
        """
        results = []
        for contract in self.contracts:
            # Check if a function has 'initialize' in its lower case name and not check the exist a state variable that is properly set during initialization and the variable is checked before the entrance.

            for f in contract.functions:
                if 'initialize' in f.name.lower() and self.detect_init_func(f):
                    # Info to be printed
                    info = 'Initialize function without checking state variables found in {}.{} ({})\n'
                    info = info.format(contract.name, f.name, f.source_mapping_str)
                    # Print the info
                    self.log(info)
                    # Add the result in result
                    json = self.generate_json_result(info)
                    self.add_function_to_json(f, json)
                    results.append(json)


        return results