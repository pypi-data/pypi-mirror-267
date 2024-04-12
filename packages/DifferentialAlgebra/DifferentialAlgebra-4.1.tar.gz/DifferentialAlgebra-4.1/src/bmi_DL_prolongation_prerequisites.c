#include "bmi_exported.h"
#include "bmi_mesgerr.h"
#include "bmi_indices.h"
#include "bmi_DL_prolongation_prerequisites.h"

/*
 * EXPORTED
 * DLProlongationPrerequisites (list of ratfrac, derivation, variable, 
 *                             regchain | differential ring, 
 *                             point, normal_form)
 *
 * Return a list [[leader, n, k, r, c0, A(q)], ..., [leader, n, k, r, c0, A(q)]]
 * for each differential equation of regchain
 */

ALGEB
bmi_DL_prolongation_prerequisites (
    struct bmi_callback *callback)
{
  struct ba0_tableof_string result;
  struct bad_regchain C;
  struct baz_point_ratfrac point;
  struct baz_tableof_ratfrac Q;
  struct baz_ratfrac c0, lcoeff;
  struct bav_tableof_variable nulles;
  struct bav_variable *q;
  struct bav_symbol *x;
  ba0_int_p i, k, r;
  char *str_derivation, *str_variable, *str_ratfrac, *str_point, *stres;
  bool normal_form;
/*
 * Check the number of arguments and the location of the table
 */
  if (bmi_nops (callback) != 6)
    BA0_RAISE_EXCEPTION (BMI_ERRNOPS);
  if (!bmi_is_table_op (4, callback))
    BA0_RAISE_EXCEPTION (BMI_ERRDRNG);
/*
 * The table contains either a regular chain + differential ring
 * or a differential ring 
 *
 * Restore these data first (regular chain in C)
 *
 * If the table is a differential ring assign to C an empty regular chain
 */
  if (bmi_is_regchain_op (4, callback))
    bmi_set_ordering_and_regchain (&C, 4, callback, __FILE__, __LINE__);
  else
    {
      bmi_set_ordering (4, callback, __FILE__, __LINE__);
      bad_init_regchain (&C);
      ba0_sscanf2 ("regchain ([], [prime, autoreduced])", "%regchain", &C);
    }
/*
 * At this stage, we have a working differential ring
 * Get the derivation and convert it into BLAD symbol / variable
 */
  str_derivation = bmi_string_op (2, callback);
  if (str_derivation[0] == '\0')
    {
      if (bav_global.R.ders.size != 1)
        BA0_RAISE_EXCEPTION (BMI_ERRDER);
      x = bav_global.R.syms.tab[bav_global.R.ders.tab[0]];
    }
  else
    {
      ba0_sscanf2 (str_derivation, "%y", &x);
      if (x->type != bav_independent_symbol)
        BA0_RAISE_EXCEPTION (BMI_ERRDER);
    }
/*
 * Get the variable
 */
  str_variable = bmi_string_op (3, callback);
  ba0_sscanf2 (str_variable, "%v", &q);
/*
 * Get the ratfrac as a string and parse it also.
 *
 * If there is no ratfrac, apply the function to all the
 *  differential equations of the regular differential chain C
 * If it is nonempty, apply the function to it only.
 */
  ba0_init_table ((struct ba0_table *) &Q);
  ba0_realloc2_table ((struct ba0_table *) &Q, C.decision_system.size + 1,
      (ba0_new_function *) & baz_new_ratfrac);

  str_ratfrac = bmi_string_op (1, callback);
  if (str_ratfrac[0] == '\0')
    {
      for (i = 0; i < C.decision_system.size; i++)
        {
          if (!bap_is_constant_polynom_mpz (C.decision_system.tab[i], x,
                  &bav_global.parameters))
            {
              baz_set_ratfrac_polynom_mpz (Q.tab[Q.size],
                  C.decision_system.tab[i]);
              Q.size += 1;
            }
        }
    }
  else
    {
/*
 * The parser to be used is different for Maple and BALSA
 */
#if ! defined (BMI_BALSA)
      ba0_sscanf2 (str_ratfrac, "%simplify_expanded_Qz", Q.tab[0]);
#else
      ba0_sscanf2 (str_ratfrac, "%Qz", Q.tab[0]);
#endif
      Q.size = 1;
    }
/*
 * Get the point as a string and parse it also
 */
  str_point = bmi_string_op (5, callback);
  ba0_init_point ((struct ba0_point *) &point);
  ba0_sscanf2 (str_point, "%point{%Qz}", &point);
/*
 * normal_form
 */
  normal_form = bmi_bool_op (6, callback);
/*
 * Go
 */
  ba0_init_table ((struct ba0_table *) &result);
  ba0_realloc_table ((struct ba0_table *) &result, Q.size);

  ba0_init_table ((struct ba0_table *) &nulles);
  bav_zero_derivatives_of_tableof_parameter (&nulles, &bav_global.parameters);

  baz_init_ratfrac (&c0);
  baz_init_ratfrac (&lcoeff);

  for (i = 0; i < Q.size; i++)
    {
      struct bav_variable *u;
      ba0_int_p n;

      u = baz_leader_ratfrac (Q.tab[i]);
      n = bav_order_variable (u, x);

      bad_DL_prolongation_prerequisites_mod_regchain (&c0, &k, &r, &lcoeff,
          Q.tab[i], x, q, &C, &point, &nulles);
/*
 * k == -1 means that the separant valuation is +infinity
 */
      if (k != -1)
        {
          if (normal_form)
            {
              bad_normal_form_ratfrac_mod_regchain (&c0, &c0, &C,
                  (struct bap_polynom_mpz **) 0);
              bad_normal_form_ratfrac_mod_regchain (&lcoeff, &lcoeff, &C,
                  (struct bap_polynom_mpz **) 0);
            }
          result.tab[i] = ba0_new_printf ("[%v, %d, %d, %d, %Qz, %Qz]",
              u, n, k, r, &c0, &lcoeff);
        }
      else
        {
#if ! defined (BMI_BALSA)
          BA0_RAISE_EXCEPTION (BA0_ERRNYP);
#else
          result.tab[i] =
              ba0_new_printf ("[%v, %d, sympy.oo, sympy.oo, 0, 0]", u, n);
#endif
        }
      result.size = i + 1;
    }
  stres = ba0_new_printf ("%t[%s]", &result);
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
