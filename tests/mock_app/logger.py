import sys
from filelock import FileLock


def execution_count(filename: str) -> int:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except OSError:
        lines = []
    start = sum(1 for l in lines if 'start' in l)
    stop = sum(1 for l in lines if 'stop' in l)
    return start - stop


def write_log(text: str) -> None:
    filename = 'log.txt'
    lock_filename = 'log.txt.lock'
    lock = FileLock(lock_filename, timeout=10)
    with lock:
        with open(filename, 'a+', encoding='utf-8') as f:
            f.write(text)
            f.write('\n')
        n = execution_count(filename)
        with open(filename, 'a+', encoding='utf-8') as f:
            f.write(f'[logger] {n} running tasks\n')


if __name__ == '__main__':
    write_log(sys.argv[1])
