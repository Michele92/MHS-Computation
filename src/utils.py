"""Contiene i metodi di utilita' e l'algoritmo principale"""
import functools

import multiprocessing.pool

from expression import *
from matrix import *

def timeout(max_timeout):
    def timeout_decorator(item):
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator

def keep_valid_solutions(singletons, everywhere_ids, matrix, grey_matrix):
    stop = False
    for k in range(len(singletons)):
        s = singletons[k]
        e = everywhere_ids[k]
        i = 0
        while i < len(s):
            if deepcopy(grey_matrix).check_for_hit_grey_rows(s[i]):
                s.pop(i)
            else:
                i += 1
        i = 0
        while i < len(e):
            if grey_matrix.check_for_hit_grey_rows(e[i]):
                everywhere_ids[k] = []
                singletons = singletons[:k+1]
                everywhere_ids = everywhere_ids[:k+1]
                stop = True
                return singletons, everywhere_ids, stop
            grey_matrix.set_grey_rows(e[i])
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

def normalize(singletons, everywhere_ids):
    i = 1
    while i < len(singletons):
        if not singletons[i]:
            everywhere_ids[i-1] += everywhere_ids[i]
            singletons.pop(i)
            everywhere_ids.pop(i)
        else:
            i += 1
    return singletons, everywhere_ids

def generate_expr(singletons, everywhere_ids, matrix, grey_matrix):
    singletons, everywhere_ids, stop = keep_valid_solutions(singletons, everywhere_ids, matrix, grey_matrix)
    singletons, everywhere_ids = normalize(singletons, everywhere_ids)
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

@timeout(600)
def compute_mhs(matrix):
    expr, substitutions_map = mhs_rec(deepcopy(matrix))
    expr.substitute(substitutions_map)
    return expr

def mhs_rec(matrix, grey_matrix=None, removed_cols=None, removed_rows=None, enable_map=False, enable_partition=True):
    if not grey_matrix:
        grey_matrix = deepcopy(matrix)
    if removed_cols:
        col_id = matrix.get_cols()[removed_cols[0]].get_id()
        matrix.submatrix(removed_rows=removed_rows, removed_cols=removed_cols)
        grey_matrix.set_grey_rows(col_id)
    singletons, everywhere_ids, substitutions_map = matrix.preprocessing(enable_map)
    expr, stop = generate_expr(singletons, everywhere_ids, matrix, grey_matrix)
    if matrix.is_empty() or stop:
        if expr and stop:
            expr.remove_pending_operand()
        return expr, substitutions_map
    submatrices = [matrix]
    partitionable = False
    if enable_partition:
        submatrices = matrix.partition()
        if submatrices:
            partitionable = True
            substitutions_map = {}
        else:
            substitutions_map = matrix.remove_equals_cols()
            submatrices = [matrix]
    prod_expr = ProductExpression()
    sum_expr = SumExpression()
    for submatrix in submatrices:
        if partitionable:
            result, partition_map = mhs_rec(matrix=deepcopy(submatrix), enable_map=True, enable_partition=False)
            substitutions_map.update(partition_map)
            if result and not result.is_empty():
                prod_expr.add_operand(result)
        else:
            while not submatrix.is_empty() and not submatrix.check_for_rows_without_1():
                col_index = submatrix.find_next_col()
                col_id = submatrix.get_cols()[col_index].get_id()
                _grey_matrix = deepcopy(grey_matrix)
                if _grey_matrix.check_for_hit_grey_rows(col_id):
                    submatrix.submatrix(removed_cols=[col_index])
                    continue
                hit_rows = submatrix.hit_rows(col_index)
                super_cols = submatrix.get_super_cols(col_index)
                result, _ = mhs_rec(matrix=deepcopy(submatrix), grey_matrix=_grey_matrix, removed_cols=[col_index] + super_cols, removed_rows=hit_rows, enable_partition=False)
                submatrix.submatrix(removed_cols=[col_index])
                if result and not result.is_empty():
                    sum_expr.add_operand(ProductExpression([AtomicElement(col_id), result]))
    result = sum_expr
    if enable_partition and partitionable:
        result = prod_expr
    if not expr or expr.is_empty():
        return result, substitutions_map
    if not result.is_empty():
        pending_operand = expr.get_pending_operand()
        pending_operand.add_operand(result)
    else:
        expr.remove_pending_operand()
    return expr, substitutions_map
