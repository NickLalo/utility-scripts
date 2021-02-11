import threading
import time
import datetime


def threaded_function(thread_num, loop_count):
    global exit_script
    global reports
    seconds = 0
    for num in range(loop_count):
        seconds += 1
        reports[thread_num] = f"seconds {seconds} of {loop_count} complete"
        time.sleep(1)
    exit_script[thread_num] = True
    return


if __name__ == "__main__":
    exit_script = []  # place to hold bools to tell us when our threads are finished
    reports = []  # a place for threads to make reports on current progress
    loop_count = 10 # a dummy report to send to our loops
    
    for thread_num in range(5):
        # target is the function our thread is going to run
        # arg thread_num is used by the thread to mark when it is done running
        # arg loop_count is the dummy report
        a_thread = threading.Thread(target=threaded_function, args=(thread_num, loop_count))
        a_thread.daemon = True  # setting this to True means our threads will stop when the main thread even if they are not done
        exit_script.append(False)  # False bool to let us know not to end threading
        reports.append("")  # empty string for thread to update later
        a_thread.start()  # setup for thread is complete so we can start our thread
        time.sleep(0.2)  # probably not necessary
    
    seconds = 0
    while True:
        time.sleep(1)
        seconds += 1
        
        break_while_true = True  # setup for exiting the script
        for bool_val in exit_script:
            if not bool_val:  # if any of our threads are not done yet then keep going
                break_while_true = False

        print(f"time running threads: {datetime.timedelta(seconds=seconds)}")
        for index, report in enumerate(reports):
            print(f"thread {index} report: {report}")

        if break_while_true:
            break
        
    print("done.")