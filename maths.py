from polynomial import Polynomial


def get_deriv(args):
    if args[-1] == '|':
        args = args[:-1]
    args = args.split('|')
    type = args[0]
    params = []
    for param in args[1:]:
        params.append(int(param))
    if type == 'polynomial':
        p = Polynomial(len(params)-1, params)
        return p.deriv()