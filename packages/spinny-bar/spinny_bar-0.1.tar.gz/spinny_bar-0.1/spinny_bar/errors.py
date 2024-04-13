"""
The errors used by spinny-bar
"""

class spinnerActiveError(Exception):
    """
    The error for spinner activity
    """
    def __init__(self, value) -> None:
        self.value = value
    
        
class invalidProgressError(Exception):
    """
    The error used when an invalid progrss is put in
    """
    def __init__(self, value) -> None:
        self.value = value