"""
Some simple progress bars for the CLI.
"""
# Errors
from errors import invalidProgressError

class barBase:
    """
    The base class for all progress bars (does not include display functionality)
    
    Args:
        message:
            type: ```str```\n
            default: ```""```\n
            The message displayed to the user\n
        maxValue:
            type: ```float```\n
            default: ```100```\n
            The maximum progress of the bar\n
        clearAtEnd:
            type: ```bool```\n
            default: ```False```\n
            Determins wether the progress bar will be cleared upon completion\n
        steps:
            type: ```int```\n
            default: ```100```\n
            The amount of steps that will be displayed (The more steps the smoother the bar goes up)
    """
    def __init__(self, message:str = "", maxValue:float = 100, clearAtEnd:bool = False, steps:int = 100) -> None:
        """
        The base class for all progress bars (does not include display functionality)

        Args:
            message:
                type: ```str```\n
                default: ```""```\n
                The message displayed to the user\n
            maxValue:
                type: ```float```\n
                default: ```100```\n
                The maximum progress of the bar\n
            clearAtEnd:
                type: ```bool```\n
                default: ```False```\n
                Determins wether the progress bar will be cleared upon completion\n
            steps:
                type: ```int```\n
                default: ```100```\n
                The amount of steps that will be displayed (The more steps the smoother the bar goes up)
        """
        self.message:str = message
        self.maxValue:float = maxValue
        self.clearAtEnd:bool = clearAtEnd
        self.steps:int = steps
        
        self.value:float = 0
        
    def setValue(self, amount:float) -> None:
        """
        Sets the progress of the progress bar
        """
        if type(amount) == int or type(amount) == float:
            if amount <= self.maxValue and amount >= 0:
                self.value = amount
            else:
                raise invalidProgressError("The value cannot outside of possible bounds")
        else:
            raise invalidProgressError("The value can only be numbers")
        
    def addToValue(self, amount:float) -> None:
        """
        Adds to the progress of the progress bar
        """
        if type(amount) == int or type(amount) == float:
            if self.value + amount <= self.maxValue and self.value + amount >= 0:
                self.value += amount
            else:
                raise invalidProgressError("The value cannot outside of possible bounds")
        else:
            raise invalidProgressError("The value can only be numbers")
        
    def removeFromValue(self, amount:float) -> None:
        """
        Removes from the progress of the progress bar
        """
        if type(amount) == int or type(amount) == float:
            if self.value - amount <= self.maxValue and self.value - amount >= 0:
                self.value -= amount
            else:
                raise invalidProgressError("The value cannot outside of possible bounds")
        else:
            raise invalidProgressError("The value can only be numbers")
    
    @property
    def progress(self) -> float:
        """
        The progress of the bar returned as a number below 0
        """
        return float(self.value / self.maxValue)
    
    @property
    def stepsFinished(self) -> int:
        """
        The amount of steps completed
        """
        return int(self.steps * self.progress)
    
    @property
    def percent(self) -> float:
        """
        The progress of the bar returned as a percentage
        """
        return float(round(self.progress * 100, 2))
    
    
class progressBar(barBase):
    """
    A basic progress bar

    Args:
        message:
            type: ```str```\n
            default: ```""```\n
            The message displayed to the user\n
        maxValue:
            type: ```float```\n
            default: ```100```\n
            The maximum progress of the bar\n
        clearAtEnd:
            type: ```bool```\n
            default: ```False```\n
            Determins wether the progress bar will be cleared upon completion\n
        steps:
            type: ```int```\n
            default: ```100```\n
            The amount of steps that will be displayed (The more steps the smoother the bar goes up)\n
        caps:
            type: ```list[str]```\n
            default: ```["[", "]"]```\n
            The caps of the progress bar
        empty:
            type: ```str```\n
            default: ```"-"```\n
            The empty parts of the progress bar
        full:
            type: ```str```\n
            default: ```"#"```\n
            The full parts of the progress bar
    """
    def __init__(self, message: str = "", maxValue: float = 100, clearAtEnd: bool = False, steps: int = 100, caps:list[str] = ["[", "]"], empty:str = "-", full:str = "#") -> None:
        """
        A basic progress bar

        Args:
            message:
                type: ```str```\n
                default: ```""```\n
                The message displayed to the user\n
            maxValue:
                type: ```float```\n
                default: ```100```\n
                The maximum progress of the bar\n
            clearAtEnd:
                type: ```bool```\n
                default: ```False```\n
                Determins wether the progress bar will be cleared upon completion\n
            steps:
                type: ```int```\n
                default: ```100```\n
                The amount of steps that will be displayed (The more steps the smoother the bar goes up)\n
            caps:
                type: ```list[str]```\n
                default: ```["[", "]"]```\n
                The caps of the progress bar
            empty:
                type: ```str```\n
                default: ```"-"```\n
                The empty parts of the progress bar
            full:
                type: ```str```\n
                default: ```"#"```\n
                The full parts of the progress bar
        """
        super().__init__(message, maxValue, clearAtEnd, steps)
        
        self.caps:list[str] = caps
        self.empty:str = empty
        self.full:str = full
    
    @property    
    def bar(self) -> str:
        """
        Returns the progress bar that can be displayed as a string
        """
        return f"{self.message} {self.caps[0]}{self.full*self.stepsFinished}{self.empty*(self.steps-self.stepsFinished)}{self.caps[1]} {self.percent}%"
    
    def displayBar(self) -> None:
        """
        Renders the progress bar to the terminal using ```print()```
        """
        print(f"\r{self.bar}", end="")
        
    def endBar(self):
        if self.clearAtEnd:
            print(f"\r{" "*len(self.bar)}", end="\r")
        else:
            print()
        