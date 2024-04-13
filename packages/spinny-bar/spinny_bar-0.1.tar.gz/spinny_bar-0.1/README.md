# spinny-bar
Loading bars, progress bars and loading wheels for the console.

## How to use
This example uses the time modual to simulate processing
```python
import spinny_bar
import multiprocessing
import time

if __name__ == "__main__":
    multiprocessing.freeze_support()
    spinner = spinny_bar.spinner(message="A functional Spinner")
    spinner.start()
    time.sleep(2)
    spinner.stop()
