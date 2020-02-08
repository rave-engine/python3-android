
def main():
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    out_file = '{}/HelloWorld.txt'.format(dir_path)
    with open(out_file, 'a') as the_file:
        the_file.write('It works!\n')


if __name__ == '__main__':
    main()


