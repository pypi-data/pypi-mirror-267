#include "bad_splitting_control.h"

/*
 * texinfo: bad_init_splitting_control
 * Initialize @var{C}. The field @code{first_leaf_only} is set
 * to @code{false}. The fields @code{dimlb} and @code{apply_dimlb_one_eq}
 * are set to @code{bad_algebraic_dimension_lower_bound} and @code{true}.
 */

BAD_DLL void
bad_init_splitting_control (
    struct bad_splitting_control *S)
{
  memset (S, 0, sizeof (struct bad_splitting_control));
  S->first_leaf_only = false;
  S->dimlb = bad_algebraic_dimension_lower_bound;
  S->apply_dimlb_one_eq = true;
}

/*
 * texinfo: bad_new_splitting_control
 * Allocate a new @code{struct bad_splitting_control *}, initialize it and return it.
 */

BAD_DLL struct bad_splitting_control *
bad_new_splitting_control (
    void)
{
  struct bad_splitting_control *S;

  S = (struct bad_splitting_control *) ba0_alloc (sizeof (struct
          bad_splitting_control));
  bad_init_splitting_control (S);
  return S;
}

/*
 * texinfo: bad_set_splitting_control
 * Assign @var{T} to @var{S}.
 */

BAD_DLL void
bad_set_splitting_control (
    struct bad_splitting_control *S,
    struct bad_splitting_control *T)
{
  if (S != T)
    *S = *T;
}

/*
 * texinfo: bad_set_first_leaf_only_splitting_control
 * Assign @var{b} to the field @code{first_leaf_only} of @var{C}.
 */

BAD_DLL void
bad_set_first_leaf_only_splitting_control (
    struct bad_splitting_control *S,
    bool b)
{
  S->first_leaf_only = b;
}

/*
 * texinfo: bad_set_dimension_lower_bound_splitting_control
 * Assign @var{lb} and @var{one_eq} to the fields
 * @code{dimlb} and @code{apply_dimlb_one_eq} of @var{C}.
 */

BAD_DLL void
bad_set_dimension_lower_bound_splitting_control (
    struct bad_splitting_control *S,
    enum bad_typeof_dimension_lower_bound lb,
    bool one_eq)
{
  S->dimlb = lb;
  S->apply_dimlb_one_eq = one_eq;
}

/*
 * texinfo: bad_apply_dimension_lower_bound_splitting_control
 * Return @code{true} if differential elimination methods
 * must discard any output regular differential chain involving
 * more than the number of input equations.
 * The input equations are provided by @var{A} and @var{eqns}.
 * Their number if returned in @var{numberof_input_equations}.
 * The decision depends on @var{S}, the number of input equations,
 * and the number of derivations involved in our problem and
 * whether the elimination process is differential or not
 * (information in @var{differential}).
 */

BAD_DLL bool
bad_apply_dimension_lower_bound_splitting_control (
    struct bad_splitting_control *S,
    struct bad_regchain *A,
    struct bap_listof_polynom_mpz *eqns,
    bool differential,
    ba0_int_p *numberof_input_equations)
{
  struct bap_listof_polynom_mpz *L;
  struct bav_tableof_variable T;
  struct ba0_mark M;
  ba0_int_p i, nbders, length;
  bool b = false;
/*
 * bad_no_dimension_lower_bound overrides apply_dimlb_one_eq
 */
  if (S->dimlb == bad_no_dimension_lower_bound)
    return false;
/*
 * numberof_input_equations = the number of input equations
 */
  length = A->decision_system.size + ba0_length_list ((struct ba0_list *) eqns);
  *numberof_input_equations = length;
/*
 * The case of a single equation
 */
  if (length == 1 && S->apply_dimlb_one_eq)
    return true;
/*
 * nbders = the number of derivations actually involved in our problem
 */
  ba0_record (&M);
  ba0_init_table ((struct ba0_table *) &T);
  for (i = 0; i < A->decision_system.size; i++)
    bap_involved_derivations_polynom_mpz (&T, A->decision_system.tab [i]);
  for (L = eqns; L != (struct bap_listof_polynom_mpz *) 0; L = L->next)
    bap_involved_derivations_polynom_mpz (&T, L->value);
  nbders = T.size;
  ba0_restore (&M);

  switch (S->dimlb)
    {
    case bad_no_dimension_lower_bound:
      b = false;
      break;
    case bad_algebraic_dimension_lower_bound:
/*
 * One may perform a non-differential decomposition over a
 * differential system.
 */
      if (!differential)
        b = true;
      else if (nbders == 0)
        b = true;
      else
        b = false;
      break;
    case bad_ode_dimension_lower_bound:
      if (nbders <= 1)
        b = true;
      else
        b = false;
      break;
    case bad_pde_dimension_lower_bound:
      b = true;
      break;
    }
  return b;
}
