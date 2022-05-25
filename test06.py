import os
import json


class Alarm(object):
    def __init__(self, sn):
        self.sn = sn


if __name__ == '__main__':
    a = 'a,b,c'
    print(list(a.split(',')))
    b = 'hello world'
    print(list(b))
    c = list(b)
    print(''.join(c))
    print('====1')
    s = {str(i): i for i in range(7)}
    print(s)
    print(set(s))
    print(s.keys())
    f = list(s.keys())
    print(f[1])
    print(s.values())
    e = list(s.values())
    print(e[1])
    print(s.items())
    d = dict(s.items())
    print(d["0"])

    colors = ["Goldenrod", "Purple", "Salmon", "Turquoise", "Cyan"]

    normalized_colors = map(lambda s: s.casefold(), colors)
    normalized_colors = filter(lambda t: 'S' in t, normalized_colors)
    print(list(normalized_colors))
    g = lambda x: x + 1
    print(g(1))

    alarm = Alarm('123123132')
    print(alarm.sn)
