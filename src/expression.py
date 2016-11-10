class Expression(object):

    """
    Rappresenta un'espressione generica.
    Puo' specializzarsi nelle classi SumExpression e ProdExpression a seconda dell'operatore coinvolto.
    Gli operandi possono essere a loro volta espressioni (istanze di Expression) o elementi atomici (istanze di
    AtomicElem).
    """

    def __init__(self, operands):

        """
        Inizializza l'espressione con la lista degli operandi.
        """
        if not operands:
            self.operands = []
        else:
            self.operands = operands

    def add_operands(self, operands):

        """
        Concatena gli elementi di due espressioni.
        """

        self.operands += operands

    def add_operand(self, operand):

        """
        Aggiunge un operando all'espressione.
        """

        self.operands.append(operand)

    def count_operands(self, count=0):
        for operand in self.operands:
            if not isinstance(operand, AtomicElem):
                count = operand.count_operands(count)
            else:
                count += 1
        return count

    def is_empty(self):

        """
        Controlla se l'espressione e' vuota, ovvero non contiene operandi.
        """

        return len(self.operands) == 0

    def get_prod_expression(self):
        for operand in self.operands:
            if isinstance(operand, ProdExpression):
                return operand
        return None

    def get_sum_expression(self):
        for operand in self.operands:
            if isinstance(operand, SumExpression):
                return operand
        return None

    def get_incomplete_operand(self):
        if self.is_empty():
            return self
        if isinstance(self, SumExpression):
            prod_expr = self.get_prod_expression()
            if prod_expr:
                return prod_expr.get_incomplete_operand()
            else:
                return self
        else:
            sum_expr = self.get_sum_expression()
            if sum_expr:
                return sum_expr.get_incomplete_operand()
            else:
                return self

class ProdExpression(Expression):

    """
    Rappresenta un'espressione i cui operandi sono legati dall'operatore '*'.
    Tale espressione e' adatta a rappresentare gli id degli elementi appartenenti a tutti i mhs del contesto attuale e
    per unire l'espressione temporanea con il risultato della ricorsione.
    """

    def __init__(self, operands=None):
        super(ProdExpression, self).__init__(operands)
        # Expression.__init__(self, operands)

    def __str__(self):

        """
        Crea e restituisce una rappresentazione dell'espressione in forma testuale.
        """

        # return '(' + '*'.join([str(op) for op in self.operands]) + ')'
        result = []
        for i, operand in enumerate(self.operands):
            if isinstance(operand, SumExpression) and operand.count_operands() > 1:
                result.append('(' + str(operand) + ')')
            else:
                result.append(str(operand))
        return '*'.join(result)

class SumExpression(Expression):

    """
    Rappresenta un'espressione i cui operandi sono legati dall'operatore '+'.
    Tale espressione e' adatta a rappresentare i singoletti, le sostituzioni in caso di colonne duplicate e per unire i
    risultati trovati con l'eliminazione di una colonna per volta.
    """

    def __init__(self, operands=None):
        super(SumExpression, self).__init__(operands)
        # Expression.__init__(self, operands)

    def __str__(self):

        """
        Crea e restituisce una rappresentazione dell'espressione in forma testuale.
        """

        # return '(' + '+'.join([str(op) for op in self.operands]) + ')'
        return '+'.join([str(op) for op in self.operands])

class AtomicElem:

    """
    Rappresenta un elemento atomico dell'espressione, quindi l'id di un singoletto o di un elemento che appartiene a
    a tutti i mhs del contesto corrente.
    """

    def __init__(self, operand):

        """
        Inizializza l'elemento atomico attribuendo il corrispondente id.
        """

        self.operand = operand

    def __str__(self):

        """
        Restituisce l'id dell'elemento atomico.
        """

        return self.operand