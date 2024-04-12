#include "bmi_exported.h"
#include "bmi_mesgerr.h"
#include "bmi_indices.h"
#include "bmi_positive_integer_roots.h"

/*
 * EXPORTED
 * Positive_integer_roots (ratfrac, variable, differential ring)
 *
 * Return a list of positive integers
 */

ALGEB
bmi_positive_integer_roots (
    struct bmi_callback *callback)
{
  struct baz_ratfrac Q;
  struct bav_variable *q;
  struct ba0_tableof_mpz roots;
  char *variable, *ratfrac, *stres;
/*
 * There must be three arguments. 
 * The last one must be a table
 */
  if (bmi_nops (callback) != 3)
    BA0_RAISE_EXCEPTION (BMI_ERRNOPS);
  if (!bmi_is_dring_op (3, callback))
    BA0_RAISE_EXCEPTION (BMI_ERRDRNG);
/*
 * The table contains a differential ring
 * Restore these data first
 */
  bmi_set_ordering (3, callback, __FILE__, __LINE__);
/*
 * At this stage, we have a working differential ring
 *
 * Get the variable as a string and use BLAD parsers to convert it
 * into a BLAD variable
 */
  variable = bmi_string_op (2, callback);
  ba0_sscanf2 (variable, "%v", &q);
/*
 * Get the ratfrac as a string and parse it also.
 * The parser to be used is not exactly the same if we are called from
 * Maple or from BALSA
 */
  ratfrac = bmi_string_op (1, callback);
  baz_init_ratfrac (&Q);
#if ! defined (BMI_BALSA)
  ba0_sscanf2 (ratfrac, "%simplify_expanded_Qz", &Q);
#else
  ba0_sscanf2 (ratfrac, "%Qz", &Q);
#endif
/*
 * Go
 */
  ba0_init_table ((struct ba0_table *) &roots);
  baz_positive_integer_roots_polynom_mpz (&roots, &Q.numer, q);
/*
 * Convert the result as a string (stres)
 */
  stres = ba0_new_printf ("%t[%z]", &roots);
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
