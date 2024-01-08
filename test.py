import threading

class Test:

    def __init__(self):
        # Create a thread
        my_thread = threading.Timer(5,self._my_function,[1,2])

        # Start the thread
        my_thread.start()

        # # Wait for the thread to finish before continuing
        # my_thread.join()

            # Now the program continues after the thread has completed its work
        print("Program continues after thread is done.")

    def _my_function(self, hi, bye):
        print(hi + bye)

def main():
    Test()

if __name__ == "__main__":
    main()