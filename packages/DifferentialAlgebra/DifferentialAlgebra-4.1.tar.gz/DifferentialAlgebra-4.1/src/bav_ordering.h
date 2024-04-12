#ifndef BAV_ORDERING_H
#   define BAV_ORDERING_H 1

#   include "bav_common.h"
#   include "bav_symbol.h"
#   include "bav_block.h"
#   include "bav_variable.h"
#   include "bav_operator.h"

BEGIN_C_DECLS

/*
 * texinfo: bav_ordering
 * This data type is a subtype of @code{bav_differential_ring}
 * used to describe orderings. 
 * An @dfn{ordering} is defined by a ranking, a list of variables
 * @math{[v_0,\ldots,v_s]} and a subranking for differential operators.
 * The rules are the following.
 * 
 * @enumerate
 * @item   Every variable @math{v_i} present in the list is greater than
 *     any variable not present in the list.
 * @item   The order of the variables in the list is @math{v_0 > \cdots > v_s}.
 * @end enumerate
 * 
 * For variables not present in the list @math{[v_0,\ldots,v_s]}, rules
 * are the following.
 * 
 * @enumerate
 * @item   Every differential operator is greater than any derivative,
 *     any independent variable and any temporary variable.
 *     Among themselves, differential
 *     operators are compared w.r.t. their subranking.
 * @item   Every derivative is greater than any independent variable and
 *     any temporary variable.
 *     Among themselves, derivatives are compared w.r.t. the ranking.
 * @item   Any independent variable is greater than any
 *     temporary variable. Independent variables are compared
 *     w.r.t. the ordering @math{d_0 > \cdots > d_p}.
 * @item   Among themselves, temporary variables are ordered according
 *     to some unspecified ordering which may be session dependent.
 * @end enumerate
 *
 * In addition to these rules, some variables may be (temporarily)
 * set as maximal variables or minimal variables (this is useful
 * for enumerating coefficients of polynomials).
 * @enumerate
 * @item    Any variable listed in the @code{varmax} field
 *      is greater than any variable not listed in this field.
 *      Among variables listed in this field, the leftmost ones
 *      are considered as higher than the rightmost ones.
 * @item    Any variable listed in the @code{varmin} field
 *      is smaller than any variable not listed in this field.
 *      Among variables listed in this field, the leftmost ones
 *      are considered as higher than the rightmost ones.
 * @end enumerate
 * If a variable appears in both fields, it is considered as
 * occuring in @code{varmax} only.
 *
 * Here are some examples of orderings.
 * @verbatim
 * ordering (derivations = [t], blocks = [[u,v], grlexB[w]])
 * 
 * ordering (derivations = [t], blocks = [w,v,u])
 * 
 * ordering (derivations = [x,y], blocks = [degrevlexA[u]],
 *                                operator = [D], varmax = [u[x,x]])
 * @end verbatim
 */

struct bav_ordering
{
  struct bav_tableof_symbol ders;       // the table of derivations
  struct bav_tableof_block blocks;      // the table of blocks
  struct bav_block operator_block;      // the block for operators
// the variables set as maximal variables
  struct bav_tableof_variable varmax;
// the variables set as minimal variables
  struct bav_tableof_variable varmin;
};


struct bav_tableof_ordering
{
  ba0_int_p alloc;
  ba0_int_p size;
  struct bav_ordering **tab;
};


extern BAV_DLL void bav_set_settings_ordering (
    char *);

extern BAV_DLL void bav_get_settings_ordering (
    char **);

extern BAV_DLL void bav_init_ordering (
    struct bav_ordering *);

extern BAV_DLL void bav_reset_ordering (
    struct bav_ordering *);

extern BAV_DLL struct bav_ordering *bav_new_ordering (
    void);

extern BAV_DLL void bav_set_ordering (
    struct bav_ordering *,
    struct bav_ordering *);

extern BAV_DLL ba0_scanf_function bav_scanf_ordering;

extern BAV_DLL ba0_printf_function bav_printf_ordering;

END_C_DECLS
#endif /* !BAV_ORDERING_H */
