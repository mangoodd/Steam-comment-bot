from PyQt5 import QtCore


class CloseProgress(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return self.message


class Worker(QtCore.QRunnable):
    status = None

    def __init__(self, fn, *args):
        """
        :param fn: function to run
        :param args: args
        """
        super().__init__()
        self.fn = fn
        self.args = args[0]

    def run(self):
        try:
            if isinstance(self.args, list):
                Worker.status = self.fn(*self.args)
            else:
                Worker.status = self.fn(self.args)
        except CloseProgress:
            # print(f'DropProcess {self.fn} --------- {self.args}')
            pass
        except (BaseException,):
            Worker.status = 'Error in Worker process!!!'
            # print(f'Error in Worker process!!! in {self.fn} --------- {self.args}')
