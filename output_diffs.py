# 
# output_diffs.py
# 

import sys

def create_diffs(container_file, item_file):
    content = []
    with open(container_file, 'r') as f1:
        content = f1.readlines()
    output = []
    with open(item_file, 'r') as f2:
        for line in f2:
            if (line not in content) and (line not in output):
                output.append(line)
    return output

def create_output_file(diffs, output_file):
    with open(output_file, 'w') as f:
        f.writelines(diffs)

# TODO features: 
# prompts if no arguments
# uniqueness preference
# printing preference
# file existance handling
# optimize data operations (hashtable?)
# documentation
# merging
# name proposal (SimpDiff)
# work across file formats (.xls)
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Wrong number of arguments."
        sys.exit()
    print "Running..."
    container_file = sys.argv[1]
    item_file = sys.argv[2]
    output_file = sys.argv[3]
    diffs = create_diffs(container_file, item_file)
    print "Diffs calculated."
    create_output_file(diffs, output_file)
    print "Done."