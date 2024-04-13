"""
Implements a basic spinner for the CLI
"""

import multiprocessing
import time

# Error imports
from errors import spinnerActiveError

class spinnerBase:
    """
    The base for all spinners (does not implement functionality)
    
    Args:
        name:
            type: ```str```\n
            default: ```"CLI spinnerBase"```\n
            The name used by ```multiprocessing``` to identify the spinner\n
        message:
            type: ```str```\n
            default: ```""```\n
            The message displayed to the user when the spinner is running\n
        speed:
            type: ```float```\n
            default: ```0.1```\n
            The speed of the spinner\n
        clearAtEnd:
            type: ```bool```\n
            default: ```False```\n
            Determins wether the spinner will be cleared at the end of spinning\n
    """
    def __init__(self, name:str = "CLI spinnerBase", message:str = "", speed:float = 0.1, clearAtEnd:bool = False) -> None:
        self.message:str = message
        self.speed:float = speed
        self.name:str = name
        self.clearAtEnd = clearAtEnd
        
        self.n = 0

class spinner(spinnerBase):
    """
    Creates a simple spinner with a message for a CLI.\n
    Started with ```start()```\n
    Ended with ```stop()```\n
    
    Args:
        name:
            type: ```str```\n
            default: ```"CLI Spinner"```\n
            The name used by ```multiprocessing``` to identify the spinner\n
        message:
            type: ```str```\n
            default: ```""```\n
            The message displayed to the user when the spinner is running\n
        speed:
            type: ```float```\n
            default: ```0.1```\n
            The speed of the spinner\n
        chars:
            type: ```list[str]```\n
            default: ```["|", "/", "─", "\\"]```\n
            The charaters looped through when the spinner is spinning\n
        clearAtEnd:
            type: ```bool```\n
            default: ```False```\n
            Determins wether the spinner will be cleared at the end of spinning\n
    """
    def __init__(self, name:str = "CLI Spinner", message:str = "", speed:float = 0.1, chars:list[str] = ["|", "/", "─", "\\"], clearAtEnd:bool = False) -> None:
        """
        Creates a simple spinner with a message for a CLI.\n
        Started with ```start()```\n
        Ended with ```stop()```\n

        Args:
            name:
                type: ```str```\n
                default: ```"CLI Spinner"```\n
                The name used by ```multiprocessing``` to identify the spinner\n
            message:
                type: ```str```\n
                default: ```""```\n
                The message displayed to the user when the spinner is running\n
            speed:
                type: ```float```\n
                default: ```0.1```\n
                The speed of the spinner\n
            chars:
                type: ```list[str]```\n
                default: ```["|", "/", "─", "\\"]```\n
                The charaters looped through when the spinner is spinning\n
            clearAtEnd:
                type: ```bool```\n
                default: ```False```\n
                Determins wether the spinner will be cleared at the end of spinning\n
        """
        super().__init__(name, message, speed, clearAtEnd)
        self.chars:list[str] = chars
        
        
        self.spinning = multiprocessing.Process(
            name = self.name,
            args = (),
            target = self.spin
        )
        
    def spin(self) -> None:
        """
        Renders the spinner based off the list of characters provided upon initialisation.
        
        Args:
            None
        """
        
        self.n = 0
        while True:
            print(f"\r{self.message} {self.chars[self.n]}", end="")
            
            self.n += 1
            
            if self.n >= len(self.chars):
                self.n = 0
            
            time.sleep(self.speed)
            
    def start(self):
        """
        Starts the spinner
        
        Args:
            None
        """
        if not self.spinning.is_alive():
            self.spinning.start()
        else:
            raise spinnerActiveError('This Spinner Is Already Active!')
        
    def stop(self):
        """
        Stops the spinner 
        
        Args:
            None
        """
        if self.spinning.is_alive():
            self.spinning.terminate()
            if self.clearAtEnd:
                print(f"\r{" "*(len(self.message) + len(self.chars[self.n]))} ", end="\r")
            else:
                print("")
        else:
            raise spinnerActiveError('This Spinner Is Not Active!')
        
class spinnerBar(spinnerBase):
    """
    Creates a spinner bar for the CLI.
    
    Args:
        name:
            type: ```str```\n
            default: ```"CLI Spinner-Bar"```\n
            The name used by ```multiprocessing``` to identify the spinner\n
        message:
            type: ```str```\n
            default: ```""```\n
            The message displayed to the user when the spinner is running\n
        speed:
            type: ```float```\n
            default: ```0.1```\n
            The speed of the spinner\n
        clearAtEnd:
            type: ```bool```\n
            default: ```False```
            Determins wether the spinner will be cleared at the end of spinning\n
        barCaps:
            type: ```list[str]```\n
            default: ```["[","]"]```\n
            The caps of the bar\n
        barEmpty:
            type: ```str```\n
            default: ```"-"```\n
            Displays at empty parts of the bar
        barFilled:
            type: ```str```\n
            default: ```"#"```\n
            Displays at filled parts of the bar\n
        barLen:
            type: ```int```\n
            default: ```5```\n
            The length of the bar\n
        filledLen:
            type: ```int```\n
            default: ```3```\n
            The length of filled parts of the bar
    """
    def __init__(self, name:str = "CLI Spinner-Bar", message:str = "", speed:float = 0.1, clearAtEnd:bool = False, barCaps:list[str] = ["[","]"], barEmpty:str = "-", barFilled:str = "#", barLen:int = 5, filledLen:int = 3) -> None:
        """
        Creates a spinner bar for the CLI.

        Args:
            name:
                type: ```str```\n
                default: ```"CLI Spinner-Bar"```\n
                The name used by ```multiprocessing``` to identify the spinner\n
            message:
                type: ```str```\n
                default: ```""```\n
                The message displayed to the user when the spinner is running\n
            speed:
                type: ```float```\n
                default: ```0.1```\n
                The speed of the spinner\n
            clearAtEnd:
                type: ```bool```\n
                default: ```False```
                Determins wether the spinner will be cleared at the end of spinning\n
            barCaps:
                type: ```list[str]```\n
                default: ```["[","]"]```\n
                The caps of the bar\n
            barEmpty:
                type: ```str```\n
                default: ```"-"```\n
                Displays at empty parts of the bar
            barFilled:
                type: ```str```\n
                default: ```"#"```\n
                Displays at filled parts of the bar\n
            barLen:
                type: ```int```\n
                default: ```5```\n
                The length of the bar\n
            filledLen:
                type: ```int```\n
                default: ```3```\n
                The length of filled parts of the bar
        """
        super().__init__(name, message, speed, clearAtEnd)
        
        self.barCaps = barCaps
        self.barEmpty = barEmpty
        self.barFilled = barFilled
        self.barLen = barLen
        self.filledLen = filledLen
        
        self.spinning = multiprocessing.Process(
            name = self.name,
            args = (),
            target = self.spin
        )
        
    def spin(self) -> None:
        """
        Renders the spinner based off the list of characters provided upon initialisation.
        
        Args:
            None
        """
        
        self.n = 0
        while True:
            barStr = ""
            bar = [self.barEmpty for i in range(self.barLen)]
            for i in range(self.filledLen):
                bar[self.n-i] = self.barFilled
            
            for part in bar:
                barStr += part
            print(f"\r{self.message} {self.barCaps[0]}{barStr}{self.barCaps[1]}", end="")
            
            self.n += 1
            if self.n >= self.barLen:
                self.n = 0
            time.sleep(self.speed)
            
    def start(self):
        """
        Starts the spinner
        
        Args:
            None
        """
        if not self.spinning.is_alive():
            self.spinning.start()
        else:
            raise spinnerActiveError('This Spinner Is Already Active!')
        
    def stop(self):
        """
        Stops the spinner
        
        Args:
            None
        """
        if self.spinning.is_alive():
            self.spinning.terminate()
            if self.clearAtEnd:
                print(f"\r{" "*(len(self.message) + self.barLen)}   ", end="\r")
            else:
                print("")
        else:
            raise spinnerActiveError('This Spinner Is Not Active!')