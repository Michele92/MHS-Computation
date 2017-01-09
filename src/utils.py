"""Contiene i metodi di utilita' e l'algoritmo principale"""

from copy import deepcopy

from expression import *
from matrix import *

def keep_valid_solutions(singletons, everywhere_ids, matrix, original_matrix):
    stop = False
    for k in range(len(singletons)):
        s = singletons[k]
        e = everywhere_ids[k]
        i = 0
        while i < len(s):
            if deepcopy(original_matrix).check_for_hit_grey_rows(s[i]):
                s.pop(i)
            else:
                i += 1
        i = 0
        while i < len(e):
            if original_matrix.check_for_hit_grey_rows(e[i]):
                everywhere_ids[k] = []
                singletons = singletons[:k+1]
                everywhere_ids = everywhere_ids[:k+1]
                stop = True
                return singletons, everywhere_ids, stop
            original_matrix.set_grey_rows(e[i])
            i += 1
    for k in range(len(everywhere_ids)):
        no_other_singletons = bool(singletons[k+1:]) and not any(singletons[k+1:])
        no_other_everywhere_ids = bool(everywhere_ids[k+1:]) and not any(everywhere_ids[k+1:])
        if matrix.is_empty() and no_other_singletons and no_other_everywhere_ids:
            everywhere_ids[k] = []
            singletons = singletons[:k+1]
            everywhere_ids = everywhere_ids[:k+1]
            stop = True
            return singletons, everywhere_ids, stop
    return singletons, everywhere_ids, stop


def build_elements(elements):
    return [[AtomicElement(col_id) for col_id in element] for element in elements]

def generate_expression(singletons, everywhere_ids, matrix, original_matrix):
    singletons, everywhere_ids, stop = keep_valid_solutions(singletons, everywhere_ids, matrix, original_matrix)
    singletons = build_elements(singletons)
    everywhere_ids = build_elements(everywhere_ids)
    expr = None
    for i in range(len(singletons) - 1, -1, -1):
        prod_expr = ProductExpression()
        if expr:
            prod_expr.add_operand(expr)
        if everywhere_ids[i]:
            prod_expr.add_operands(everywhere_ids[i])
        if singletons[i]:
            expr = SumExpression(singletons[i])
            if not prod_expr.is_empty():
                expr.add_operand(prod_expr)
        elif not prod_expr.is_empty():
            expr = prod_expr
    return expr, stop

def compute_mhs(matrix, original_matrix=None, removed_cols=None, removed_rows=None):
    if not original_matrix:
        original_matrix = deepcopy(matrix)
    if removed_cols:
        matrix.submatrix(removed_rows=removed_rows)
        matrix.submatrix(removed_cols=removed_cols)
        original_matrix.set_grey_rows(removed_cols[0])
    singletons, everywhere_ids = matrix.preprocessing()
    expr, stop = generate_expression(singletons, everywhere_ids, matrix, original_matrix)
    if matrix.is_empty() or stop:
        if expr and stop:
            expr.remove_pending_operand()
        return expr
    sum_expr = SumExpression()
    complementary_cols = OrderedDict()
    while not matrix.is_empty() and not matrix.check_for_rows_without_1():
        # col_id = matrix.get_cols()[0].get_id()
        col_id = matrix.find_next_col(complementary_cols)
        _original_matrix = deepcopy(original_matrix)
        if _original_matrix.check_for_hit_grey_rows(col_id):
            matrix.submatrix(removed_cols=[col_id])
            continue
        hit_rows = matrix.hit_rows(col_id)
        super_cols = matrix.get_super_cols(col_id)
        result = compute_mhs(deepcopy(matrix), _original_matrix, [col_id] + super_cols, hit_rows)
        matrix.submatrix(removed_cols=[col_id])
        if result and not result.is_empty():
            sum_expr.add_operand(ProductExpression([AtomicElement(col_id), result]))
    if not expr or expr.is_empty():
        return sum_expr
    if not sum_expr.is_empty():
        pending_operand = expr.get_pending_operand()
        pending_operand.add_operand(sum_expr)
    else:
        expr.remove_pending_operand()
    return expr


