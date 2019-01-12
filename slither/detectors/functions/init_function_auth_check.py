"""
Module detecting initialize function

A initialization function is an unprotected function that does not check the caller(msg.sender)
"""
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
class InitFunctionAuth(AbstractDetector):
    """
    Unprotected function detector
    """
    ARGUMENT = 'init-auth'
    HELP = 'Functions allowing call initialize function without check the caller'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH
    #do not have wiki now
    WIKI = 'https://github.com/trailofbits/slither/wiki'

    def detect(self):
        """ Detect the unprotected initialize funtion
        """
        results = []
        for contract in self.contracts:
            # Check if a function has 'initialize' in its lower case name and not check the caller(msg.sender)
            for f in contract.functions:
                if 'initialize' in f.name.lower() and not f.is_protected():
                    # Info to be printed
                    info = 'Initialize function without checking the caller found in {}.{} ({})\n'
                    info = info.format(contract.name, f.name, f.source_mapping_str)
                    # Print the info
                    self.log(info)
                    # Add the result in result
                    json = self.generate_json_result(info)
                    self.add_function_to_json(f, json)
                    results.append(json)


        return results