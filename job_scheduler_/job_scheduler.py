import subprocess
import time


def read_config(fn = 'config.dat'):
    '''
    Reads the config file, removes comments marked by '#' and replaces multiple whitespaces by single ones.
    '''
    lines = []
    with open(fn) as f:
        for line in f:
            # substring the line to stop before the first occurrence of '#'
            line = line[:line.find('#')]
            # remove whitespaces from the beginning and the end of the line
            line = line.strip()
            # remove all double / multiple spaces by single spaces
            len_old = 0
            while (len(line) != len_old):
                len_old = len(line)
                line = line.replace('  ', ' ')
            # append if remaining line is one or more characters
            if (len(line) > 0):
                lines.append(line)
        return lines

def get_current_datetime():
    return subprocess.check_output('date +"%Y %m %e %H %M"', shell=True).decode().replace('\n','').split(' ')

def get_datetime_from_line(line):
    line = line.split(' ')
    return [s for s in line[:5]]

def get_command_from_line(line):
    line = line.split(' ')
    return ' '.join([str(s) for s in line[5:]])

def is_equal(dt, dt_):
    return (dt[0] == dt_[0]) and (dt[1] == dt_[1]) and (dt[2] == dt_[2]) and (dt[3] == dt_[3]) and (dt[4] == dt_[4])

def check_run_condition(dtc, dt, dt_old):
    # do not run twice at the same date and time
    if (is_equal(dt, dt_old)):
        return False
    # replace all '*' with the corresponding value of the current datetime
    for i in range(0, 5):
        if (dtc[i] == '*'):
            dtc[i] = dt[i]
    if (is_equal(dtc, dt)):
        return True
    return False


dt_ = get_current_datetime()
ds = 60

while True:
    time.sleep(ds)
    dt = get_current_datetime()
    # print(dt)
    lines = read_config()
    for line in lines:
        dtc = get_datetime_from_line(line)
        if check_run_condition(dtc, dt, dt_):
            command = get_command_from_line(line)
            #print(f'Running command {command}')
            output = subprocess.check_output(command, shell=True).decode().replace('\n', '')
            #print(f'Output is: {output}')

    dt_ = dt