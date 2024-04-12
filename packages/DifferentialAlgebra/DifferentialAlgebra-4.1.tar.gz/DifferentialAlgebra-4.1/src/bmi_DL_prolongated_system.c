#include "bmi_exported.h"
#include "bmi_mesgerr.h"
#include "bmi_indices.h"
#include "bmi_DL_prolongated_system.h"

/*
 * EXPORTED
 * DLProlongatedSystem (derivation, regchain, point, normal_form)
 *
 * Return [S, X, N] where
 * - S is a list of polynomials sorted by increasing rank
 * - X is the list of variables S depends on by decreasing order
 * - N is the set of the non-leaders occuring in the normal forms of S
 */

ALGEB
bmi_DL_prolongated_system (
    struct bmi_callback *callback)
{
  struct bad_regchain C;
  struct baz_point_ratfrac point;
  struct baz_tableof_ratfrac T, *U;
  struct bav_tableof_variable nulles, X, *Y, N;
  struct bav_symbol *x;
  ba0_int_p i;
  bool normal_form;
  char *str_derivation, *str_point, *stres;
/*
 * There must be four arguments. The second one must be a regchain
 */
  if (bmi_nops (callback) != 4)
    BA0_RAISE_EXCEPTION (BMI_ERRNOPS);
  if (!bmi_is_regchain_op (2, callback))
    BA0_RAISE_EXCEPTION (BMI_ERRREGC);
/*
 * Restore the regular chain first
 */
  bmi_set_ordering_and_regchain (&C, 2, callback, __FILE__, __LINE__);
/*
 * At this stage we have a working differential ring and a regchain
 *
 * Get the derivation
 */
  str_derivation = bmi_string_op (1, callback);
  ba0_sscanf2 (str_derivation, "%y", &x);
  if (x->type != bav_independent_symbol)
    BA0_RAISE_EXCEPTION (BMI_ERRDER);
/*
 * Get the point
 */
  str_point = bmi_string_op (3, callback);
  ba0_init_point ((struct ba0_point *) &point);
  ba0_sscanf2 (str_point, "%point{%Qz}", &point);
/*
 * normal_form
 */
  normal_form = bmi_bool_op (4, callback);
/*
 * Go
 */
  ba0_init_table ((struct ba0_table *) &nulles);
  bav_zero_derivatives_of_tableof_parameter (&nulles, &bav_global.parameters);
  ba0_init_table ((struct ba0_table *) &T);
  bad_DL_prolongated_system_mod_regchain (&T, &C, &point, x, &nulles);
/*
 * Normal forms are stored in U
 * if normal_form is true than T = U
 */
  if (normal_form)
    U = &T;
  else
    {
      U = (struct baz_tableof_ratfrac *) ba0_new_table ();
      ba0_realloc2_table ((struct ba0_table *) U, T.size,
          (ba0_new_function *) & baz_new_ratfrac);
      U->size = T.size;
    }
  for (i = 0; i < T.size; i++)
    bad_normal_form_ratfrac_mod_regchain (U->tab[i], T.tab[i], &C,
        (struct bap_polynom_mpz **) 0);
/*
 * X = the indets of T
 */
  ba0_init_table ((struct ba0_table *) &X);
  bav_R_mark_variables (false);
  for (i = 0; i < T.size; i++)
    baz_mark_indets_ratfrac (T.tab[i]);
  bav_R_marked_variables (&X, true);
  bav_sort_tableof_variable (&X, ba0_ascending_mode);
/*
 * N = the non leaders the normal forms in U depend on
 */
  if (normal_form)
    Y = &X;
  else
    {
      Y = (struct bav_tableof_variable *) ba0_new_table ();
      bav_R_mark_variables (false);
      for (i = 0; i < U->size; i++)
        baz_mark_indets_ratfrac (U->tab[i]);
      bav_R_marked_variables (Y, true);
      bav_sort_tableof_variable (Y, ba0_ascending_mode);
    }

  ba0_init_table ((struct ba0_table *) &N);
  ba0_realloc_table ((struct ba0_table *) &N, Y->size);
  for (i = 0; i < Y->size; i++)
    if (!bad_is_leader_of_regchain (Y->tab[i], &C, (ba0_int_p *) 0))
      {
        N.tab[N.size] = Y->tab[i];
        N.size += 1;
      }
/*
 * stres = the result as a string
 */
  stres = ba0_new_printf ("[%t[%Qz], %t[%v], %t[%v]]", &T, &X, &N);
/*
 * Convert stres into a result (res)
 */
  {
    ALGEB res;
    bmi_push_maple_gmp_allocators ();
#if ! defined (BMI_BALSA)
/*
 * res is the Maple object obtained by evaluating the string
 * with Maple interpreter
 */
    res = EvalMapleStatement (callback->kv, stres);
#else
/*
 * res is a BALSA object of type string wrapping stres
 * It will also be evaluated but at the Cython level
 */
    res = bmi_balsa_new_string (stres);
#endif
    bmi_pull_maple_gmp_allocators ();
    return res;
  }
}
