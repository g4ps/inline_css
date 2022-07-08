import os
import sys
import re

if (len(sys.argv) != 4):
    print("Usage:", sys.argv[0], " inp_file st_file out_file");
    exit(1);

inp_file=open(sys.argv[1], "r");
style_file=open(sys.argv[2], "r");
out_file=open(sys.argv[3], "w");
out_file.truncate(0);
# style_file=open(sys.argv[1], "r");

def style_as_object(inp_file):
    data = inp_file.readlines();
    ln=0
    ret = {}
    for line in data:
        ln += 1;
        line = re.sub('#.*', '', line);
        line = line.replace('\n', '');
        if (re.search(line, '^\s*$')):
            continue;
        name=re.sub('\s.*$', '', line);
        sub = re.sub('^[^\s]*\s', '', line);
        if (len(sub) == 0):
            print("Error: no substitution in line", ln)
            print(line)
            exit(1)
        ret[name] = sub
    return ret;

obj=style_as_object(style_file)

print(obj);

ln = 0;
while (True):
    ln += 1;
    line = inp_file.readline()
    line = line.replace('\n', '');
    if (not line):
        break;
    while (re.search("evg=['\"][^'\"]*[\'\"]", line)):
        p1 = '''.*evg=['"]([^'"]*)['"].*''';
        p2 = r"\1";
        attr_name = re.sub(p1, p2, line);
        attr_name = attr_name.strip();
        if (not attr_name in obj):
            print("ERROR: line", ln, ": Couldn't find attribute", attr_name, "in", sys.argv[2]);
            exit(1);
        line = re.sub('''evg=['"][^'"]*['"]''', "style='" + obj[attr_name] + "'", line);
    print(line);
    out_file.write(line + '\n');
    
