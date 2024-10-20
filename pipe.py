import sys

tmp_list = []
for line in sys.stdin:
    tmp_list.append(line.strip().lower())
sys.stdout.write("\n".join(tmp_list))
