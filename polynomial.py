class Polynomial:
    def __init__(self, grad, params):
        self.grad = grad
        self.params = params

    def draw(self):
        string = ""
        for i in range(0, self.grad + 1):
            if self.params[i] != 0:
                if self.grad - i == 0:
                    string += str(self.params[i])
                    if self.params[i] != self.params[-1]:
                        string += ' + '
                elif self.grad - i == 1:
                    string += str(self.params[i]) + 'x'
                    if self.params[i] != self.params[-1]:
                        string += ' + '
                else:
                    string += str(self.params[i]) + 'x^' + str(self.grad - i)
                    if self.params[i] != self.params[-1]:
                        string += ' + '
        return string

    def deriv(self):
        deriv = []
        deriv_str = ""
        for i in range(0, self.grad + 1):
            deriv.append(str(self.params[i] * (self.grad - i)) + 'x^' + str(self.grad - i - 1))
        for p in deriv:
            if p[0] != '0':
                if p[3] == '0':
                    deriv_str += p[0]
                    if p != deriv[-1]:
                        deriv_str += ' + '
                elif p[3] == '1':
                    deriv_str += p[0] + 'x'
                    if p != deriv[-1]:
                        deriv_str += ' + '
                else:
                    deriv_str += p
                    if p != deriv[-1]:
                        deriv_str += ' + '
        if deriv_str[-2] == '+':
            return deriv_str[:-2]
        else:
            return deriv_str
