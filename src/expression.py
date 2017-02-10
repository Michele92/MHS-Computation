"""Contiene le classi per rappresentare l'espressione dei minimal hitting set"""

class AtomicElement:

    """
    Rappresenta un elemento atomico dell'espressione, dunque l'id di una colonna
    """

    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        return str(self.operand)

class Expression(object):

    """
    Rappresenta un'espressione generica.
    Puo' specializzarsi nelle classi SumExpression e ProductExpression a seconda dell'operatore coinvolto.
    Gli operandi possono essere a loro volta espressioni (istanze di Expression) o elementi atomici (istanze di
    AtomicElement)
    """

    def __init__(self, operands):
        if not operands:
            self.operands = []
        else:
            self.operands = operands

    def add_operands(self, operands):
        self.operands += operands

    def add_operand(self, operand):
        self.operands.append(operand)

    def count_operands(self):
        count = 0
        for operand in self.operands:
            if not isinstance(operand, AtomicElement):
                count += operand.count_operands()
            else:
                count += 1
        return count

    def is_empty(self):
        return len(self.operands) == 0

    def get_product_expression(self):
        for operand in self.operands:
            if isinstance(operand, ProductExpression):
                return operand
        return None

    def get_sum_expression(self):
        for operand in self.operands:
            if isinstance(operand, SumExpression):
                return operand
        return None

    def get_pending_operand(self):
        if self.is_empty():
            return self
        if isinstance(self, SumExpression):
            prod_expr = self.get_product_expression()
            if prod_expr:
                return prod_expr.get_pending_operand()
            return self
        sum_expr = self.get_sum_expression()
        if sum_expr:
            return sum_expr.get_pending_operand()
        return self

    def is_composed_by_all_atomic_elements(self):
        for operand in self.operands:
            if not isinstance(operand, AtomicElement):
                return False
        return True

    def remove_pending_operand(self):
        if isinstance(self, ProductExpression):
            if self.is_composed_by_all_atomic_elements():
                self.operands = []
                return
        for operand in self.operands:
            if isinstance(operand, SumExpression):
                operand.remove_pending_operand()
            elif isinstance(operand, ProductExpression):
                if operand.is_composed_by_all_atomic_elements():
                    self.operands.remove(operand)
                    return
                operand.remove_pending_operand()

    def substitute(self, substitutions_map):
        if not substitutions_map:
            return
        operands = []
        for operand in self.operands:
            if isinstance(operand, AtomicElement):
                new_operand = operand
                if str(operand) in substitutions_map:
                    new_operand = SumExpression([operand] + [AtomicElement(e) for e in substitutions_map[str(operand)]])
            else:
                operand.substitute(substitutions_map)
                new_operand = operand
            operands.append(new_operand)
        self.operands = operands

class SumExpression(Expression):

    """
    Rappresenta un'espressione i cui operandi sono legati dall'operatore '+'.
    Tale espressione e' adatta a rappresentare i singoletti e per unire i risultati trovati con il metodo per colonne
    """

    def __init__(self, operands=None):
        super(SumExpression, self).__init__(operands)
        self.operator = '+'

    def __str__(self):
        return self.operator.join([str(operand) for operand in self.operands])

class ProductExpression(Expression):

    """
    Rappresenta un'espressione i cui operandi sono legati dall'operatore '*'.
    Tale espressione e' adatta a rappresentare gli id degli elementi appartenenti a tutti i mhs del contesto attuale e
    per unire l'id della colonna scelta dal metodo per colonne con il relativo risultato
    """

    def __init__(self, operands=None):
        super(ProductExpression, self).__init__(operands)
        self.operator = '*'

    def __str__(self):
        operands = []
        for i, operand in enumerate(self.operands):
            if isinstance(operand, SumExpression) and operand.count_operands() > 1:
                operands.append('(' + str(operand) + ')')
            else:
                operands.append(str(operand))
        return self.operator.join(operands)
