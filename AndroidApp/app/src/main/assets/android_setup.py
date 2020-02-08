import os, sys, time


class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)



if __name__ == '__main__':
    # We really don't want to do anything if this is being run as a file
    pass


# This will allow us access to the stderr & stdout
def setupEnvironment():
    import sys

    sys.stdout = Unbuffered(sys.stdout)
    sys.stderr = Unbuffered(sys.stderr)

    return 0
