import re

from logger.logger import Logger
logger = Logger(logger_name=__name__,log_level=20)


def next_step(message: str, step: int=None, stop: bool=False):
    """Display a step message and optionally prompt for user confirmation.
    
    Displays the given message with logging and optionally prompts the user
    to continue execution. If the message contains a step number pattern,
    it extracts and uses that for prompting.
    
    Args:
        message (str): The step message to display and log.
        step (int, optional): Explicit step number. Defaults to None.
        stop (bool, optional): Whether to prompt user for confirmation. 
            Defaults to False.
            
    Raises:
        KeyboardInterrupt: If user chooses not to continue when prompted.
    """

    step_pattern = re.compile(r'^Step \d+', flags=re.IGNORECASE)
    match = re.match(step_pattern, message)
    asterisks = '*' * len(message)

    if stop:
        if match:
            step = int(re.search(r'\d+', match.group()).group())
        if match or step:
            current_step = step - 1
            result = input(f"{asterisks}\n{message}\n{asterisks}\nContinue to Step {step}? y/n: ")
            if result != "y":
                raise KeyboardInterrupt(f"scrape_the_law program stopped at Step {current_step}.")
            else:
                logger.info(message, f=True)
                return
        else:
            result = input(f"Continue next step? y/n: ")
            if result != "y":
                raise KeyboardInterrupt(f"scrape_the_law program stopped at step.")
            else:
                logger.info(message, f=True)
                return
    else:
        logger.info(message, f=True)
        return
