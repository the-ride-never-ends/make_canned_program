import asyncio
from typing import Any, Callable, Coroutine, Generator


from tqdm import asyncio as tqdmasyncio


from .create_tasks_list import create_tasks_list
from .create_tasks_list_with_outer_task_name import create_tasks_list_with_outer_task_name


class Limiter:
    """
    Create an instance-based custom rate-limiter based on a semaphore.
    Options for a custom stop condition and progress bar.
    """
    def __init__(self, 
                 semaphore: int, 
                 stop_condition: Any = "stop_condition", # Replace with your specific stop condition
                 progress_bar: bool=True
                ):
        """Initialize the Limiter with concurrency control settings.
        
        Args:
            semaphore (int): Maximum number of concurrent tasks allowed.
            stop_condition (Any, optional): Condition that triggers stopping of tasks.
                Defaults to "stop_condition".
            progress_bar (bool, optional): Whether to show progress bar during execution.
                Defaults to True.
        """
        self.semaphore = asyncio.Semaphore(semaphore)
        self.stop_condition = stop_condition
        self.progress_bar = progress_bar

    # Claude insisted that I include these for compatability/future use purposes.
    # It's probably a good idea. 
    async def __aenter__(self):
        """
        Initialize the Limiter using a context manager.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the limiter using a context manager.
        """
        pass

    @classmethod
    def start(cls):
        """
        Initialize the Limiter using a factory method.
        """
        instance = cls()
        return instance

    def stop():
        """
        Exit the limiter.
        """
        return


    async def run_task_with_limit(self, task: Coroutine) -> Any:
        """
        Set up rate-limit-conscious functions
        """
        async with self.semaphore:
            result = await task
            if result == self.stop_condition:  
                global stop_signal
                stop_signal = True
            return result 


    async def run_async_many(self, 
                             *args, 
                             inputs: Any=None, 
                             func: Callable=None,
                             enum: bool=True,
                             outer_task_name: str = "",
                             **kwargs
                            ) -> asyncio.Future | Generator:
        """Run multiple async tasks with concurrency limiting and optional progress tracking.
        
        Args:
            *args: Additional positional arguments for the task function.
            inputs (Any, optional): Input data for the tasks. Defaults to None.
            func (Callable, optional): The async function to run for each input.
                Defaults to None.
            enum (bool, optional): Whether to enumerate inputs. Defaults to True.
            outer_task_name (str, optional): Name prefix for tasks. Defaults to "".
            **kwargs: Additional keyword arguments for the task function.
            
        Returns:
            asyncio.Future | Generator: Future or generator of task results.
            
        Raises:
            ValueError: If inputs or func parameters are not provided.
        """
        if not inputs:
            raise ValueError("input_list was not input as a parameter")

        if not func:
            raise ValueError("func was not input as a parameter")

        # NOTE Adding an outer_task_name changes the tasks list from a list of Coroutines to a list of Tasks.
        # However, running it through the limiter appears to change them back into Coroutines, so maybe it's fine???
        if outer_task_name and self.progress_bar is False:
            tasks = create_tasks_list_with_outer_task_name(inputs, func, enum, *args, **kwargs)
        else:
            tasks = create_tasks_list(inputs, func, enum, *args, **kwargs)

        task_list = [
            self.run_task_with_limit(task) for task in tasks
        ]

        if self.progress_bar:
            for future in tqdmasyncio.tqdm.as_completed(task_list):
                await future
        else:
            return await asyncio.gather(*task_list)

