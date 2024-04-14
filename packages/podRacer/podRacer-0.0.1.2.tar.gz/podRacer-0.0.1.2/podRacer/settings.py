## IMPORTS
if 'Imports':

    if 'Standard Python Library':
        import inspect                      # returns data on code execution, useful for debugging
        import os                           # local file operations, mainly os.path.join
        import platform                     # returns operating system information

## HANDLES APP SETTINGS
class Settings():

    ## INITIALIZE SETTINGS
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)

            ## DEFAULT VALUES
            cls._instance.error_logging = 'standard'
        return cls._instance

    ## CLEARS THE TERMINAL
    def clear_terminal(self):
        """Clears the terminal screen."""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        print()

    ## SET - ERROR LOGGING
    def set_error_logging(self, level):
        '''
        Default Value: 'standard'

        Options: ['standard', 'detailed']
        '''
        self.error_logging = level

    ## GET - ERROR LOGGING
    def get_error_logging(self):
        return self.error_logging

    ## RETURNS ERROR MESSAGES
    def error(self, exception=None, reason=None, caught_input=None, valid_input=None, message=None, output=True):

        ## INITIALIZE ERROR MESSAGE
        error_message = []

        ## GET CALLER FRAME
        caller_frame = inspect.currentframe().f_back

        ## GET NAMES OF CLASS AND FUNCTION
        class_name = caller_frame.f_locals.get('self', None).__class__.__name__
        function_name = caller_frame.f_code.co_name

        ## STANDARD ERROR MESSAGE
        error_message.append(f"\nThe function '{function_name}()' from the '{class_name}' class, threw an error!")
        if exception:
                error_message.append(f"Error: {exception}")

        ## DETAILED ERROR MESSAGE
        if self.error_logging == 'detailed':
            if reason:
                error_message.append(f"Reason: {reason}")
            if caught_input:
                error_message.append(f"Your Input: {caught_input}")
            if valid_input:
                error_message.append(f"Valid Inputs: {valid_input}")
            if message:
                error_message.append(f"\n{message}")

        ## JOIN ERROR MESSAGE
        error_message = "\n".join(error_message)

        ## PRINTS TO TERMINAL
        if output:
            print(error_message)

        ## RETURN ERROR MESSAGE
        return error_message

    ## PRINTS TO TERMINAL
    def print(self, message, *args, **kwargs):
        print(message)
        for arg in args:
            print(arg)
        for key, value in kwargs.items():
            print(f"{key}: {value}")
