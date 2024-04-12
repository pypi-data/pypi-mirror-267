#include "baz_eval_polyspec_mpz.h"
#include "baz_eval_ratfrac.h"

/*
 * texinfo: baz_eval_to_interval_at_point_interval_mpq_polynom_mpz
 * Evaluate @var{A} at @var{point}.
 * Result in @var{res}.
 * All the variables of @var{A} must be assigned a value a value.
 * The evaluation is not differential.
 */

BAZ_DLL void
baz_eval_to_interval_at_point_interval_mpq_polynom_mpz (
    struct ba0_interval_mpq *res,
    struct bap_polynom_mpz *A,
    struct bav_point_interval_mpq *point)
{
  struct bap_itermon_mpz iter;
  struct bav_term T;
  struct ba0_interval_mpq X, S;
  struct ba0_mark M;
  ba0_mpq_t q;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_interval_mpq (&S);
  ba0_init_interval_mpq (&X);
  bav_init_term (&T);
  ba0_mpq_init (q);
  ba0_set_interval_mpq_si (&S, 0);
  bap_begin_itermon_mpz (&iter, A);
  while (!bap_outof_itermon_mpz (&iter))
    {
      bap_term_itermon_mpz (&T, &iter);
      bav_term_at_point_interval_mpq (&X, &T, point);
      ba0_mpz_set (ba0_mpq_numref (q), *bap_coeff_itermon_mpz (&iter));
      ba0_mul_interval_mpq_mpq (&X, &X, q);
      ba0_add_interval_mpq (&S, &S, &X);
      bap_next_itermon_mpz (&iter);
    }

  ba0_pull_stack ();
  ba0_set_interval_mpq (res, &S);
  ba0_restore (&M);
}

/*
 * texinfo: baz_eval_to_ratfrac_at_ratfrac_polynom_mpz
 * Assign to @var{R} the rational fraction obtained by evaluating
 * @var{A} at @var{point}. 
 * The substitution is parallel: values are not substituted into values.
 * The evaluation is not differential.
 */

BAZ_DLL void
baz_eval_to_ratfrac_at_point_ratfrac_polynom_mpz (
    struct baz_ratfrac *R,
    struct bap_polynom_mpz *A,
    struct baz_point_ratfrac *point)
{
  struct baz_point_ratfrac pnt;
  struct baz_ratfrac result, val_term, tmp;
  struct bap_polynom_mpz B, coeff;
  struct bap_itercoeff_mpz iter;
  struct bav_term term, prev_term, ratio;
  struct bav_variable *v;
  bav_Iordering r;
  struct ba0_mark M;
  ba0_int_p i;

  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * pnt = the values useful for evaluating A
 */
  ba0_init_point ((struct ba0_point *) &pnt);
  ba0_set_point ((struct ba0_point *) &pnt, (struct ba0_point *) point);
  i = pnt.size - 1;
  while (i > 0)
    {
      if (!bap_depend_polynom_mpz (A, pnt.tab[i]->var))
        ba0_delete_point ((struct ba0_point *) &pnt, (struct ba0_point *) &pnt,
            i);
      i -= 1;
    }
/*
 * To avoid pointless computations
 */
  if (pnt.size == 0)
    {
      ba0_pull_stack ();
      ba0_restore (&M);

      baz_set_ratfrac_polynom_mpz (R, A);
      return;
    }
/*
 * Create an ordering r such that the evaluated variables are
 * greater than any other one
 */
  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);
  for (i = 0; i < pnt.size; i++)
    {
      v = pnt.tab[i]->var;
      bav_R_set_maximal_variable (v);
    }
/*
 * Sort the values of pnt w.r.t. r
 */
  for (i = 0; i < pnt.size; i++)
    {
      struct baz_ratfrac *Q = pnt.tab[i]->value;
      pnt.tab[i]->value = baz_new_readonly_ratfrac ();
      baz_sort_ratfrac (pnt.tab[i]->value, Q);
    }

  baz_init_ratfrac (&result);
  baz_init_ratfrac (&tmp);
/*
 * term = 1
 * val_term = term evaluated at point
 */
  bav_init_term (&term);
  baz_init_ratfrac (&val_term);
  baz_set_ratfrac_one (&val_term);
/*
 * prev_term = the previous value of term
 */
  bav_init_term (&prev_term);
  bav_init_term (&ratio);

  bap_init_readonly_polynom_mpz (&B);
  bap_init_readonly_polynom_mpz (&coeff);
  bap_sort_polynom_mpz (&B, A);
/*
 * v = the lowest variable of terms
 */
  v = pnt.tab[0]->var;
  bap_end_itercoeff_mpz (&iter, &B, v);
/*
 * Start with the lowest term to save computations when possible
 * If pnt involves a single value, this is equivalent to Horner scheme
 */
  while (!bap_outof_itercoeff_mpz (&iter))
    {
      BA0_SWAP (struct bav_term,
          term,
          prev_term);
      bap_term_itercoeff_mpz (&term, &iter);
      bap_coeff_itercoeff_mpz (&coeff, &iter);

      if (!bav_is_factor_term (&term, &prev_term, &ratio))
        {
          bav_set_term (&ratio, &term);
          baz_set_ratfrac_one (&val_term);
        }
      while (!bav_is_one_term (&ratio))
        {
          struct baz_value_ratfrac *value;
          v = ratio.rg[0].var;
          value =
              (struct baz_value_ratfrac *) ba0_bsearch_point (v,
              (struct ba0_point *) &pnt, (ba0_int_p *) 0);
          if ((struct ba0_value *) value == BA0_NOT_A_VALUE)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);
          baz_mul_ratfrac (&val_term, &val_term, value->value);
          bav_exquo_term_variable (&ratio, &ratio, v, 1);
        }
      baz_mul_ratfrac_polynom_mpz (&tmp, &val_term, &coeff);
      baz_add_ratfrac (&result, &result, &tmp);
      bap_prev_itercoeff_mpz (&iter);
    }
  bap_close_itercoeff_mpz (&iter);

  ba0_pull_stack ();
  baz_set_ratfrac (R, &result);
  ba0_restore (&M);
  bav_R_pull_ordering ();
  bav_R_free_ordering (r);
  baz_physort_ratfrac (R);
}

/*
 * texinfo: baz_evaluate_to_ratfrac_at_point_ratfrac_polynom_mpz
 * Assign to @var{R} the rational fraction obtained by evaluating @var{A}
 * at @var{point}. 
 * The substitution is parallel: values are not substituted into values.
 * The evaluation is differential: the evaluation point used for 
 * evaluating @var{A} is obtained by prolongating @var{point} 
 * (see @code{baz_prolongate_point_ratfrac}) but
 * the parameter @var{point} is left unchanged.
 * The table @var{nulles} contains derivatives which should be rewritten
 * to zero while differentiating rational fractions.
 */

BAZ_DLL void
baz_evaluate_to_ratfrac_at_point_ratfrac_polynom_mpz (
    struct baz_ratfrac *R,
    struct bap_polynom_mpz *A,
    struct baz_point_ratfrac *point,
    struct bav_tableof_variable *nulles)
{
  struct baz_point_ratfrac pnt;
  struct bav_variable *v;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_point ((struct ba0_point *) &pnt);
  ba0_set_point ((struct ba0_point *) &pnt, (struct ba0_point *) point);
  baz_prolongate_point_ratfrac_term (&pnt, &pnt, &A->total_rank, nulles);
  ba0_pull_stack ();
  baz_eval_to_ratfrac_at_point_ratfrac_polynom_mpz (R, A, &pnt);
  ba0_restore (&M);
}

/*
 * texinfo: baz_twice_evaluate_to_ratfrac_at_point_ratfrac_polynom_mpz
 * Assign to @var{R} the rational fraction obtained by evaluating @var{A}
 * at a point as explained below.
 * The evaluation point used for evaluating @var{A} is obtained by 
 * prolongating @var{point0} (by means of differentiations), then
 * evaluating the right hand sides at @var{point1} (without any
 * prolongation).
 * The substitution is parallel: values are not substituted into values.
 * The table @var{nulles} contains derivatives which should be rewritten
 * to zero while differentiating rational fractions.
 * This function is useful for evaluating a differential polynomial in @math{y}
 * at a series @math{\bar{y}}$ in an independent variable @math{x}, then
 * evaluate the result at @math{x=0}.
 */

BAZ_DLL void
baz_twice_evaluate_to_ratfrac_at_point_ratfrac_polynom_mpz (
    struct baz_ratfrac *R,
    struct bap_polynom_mpz *A,
    struct baz_point_ratfrac *point0,
    struct baz_point_ratfrac *point1,
    struct bav_tableof_variable *nulles)
{
  struct baz_point_ratfrac pnt;
  struct bav_variable *v;
  struct ba0_mark M;
  ba0_int_p i;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_point ((struct ba0_point *) &pnt);
  ba0_set_point ((struct ba0_point *) &pnt, (struct ba0_point *) point0);
  baz_prolongate_point_ratfrac_term (&pnt, &pnt, &A->total_rank, nulles);
  for (i = 0; i < pnt.size; i++)
    {
      struct baz_ratfrac *Q = pnt.tab[i]->value;
      pnt.tab[i]->value = baz_new_ratfrac ();
      baz_eval_to_ratfrac_at_point_ratfrac_ratfrac (pnt.tab[i]->value, Q,
          point1);
    }
  ba0_pull_stack ();
  baz_eval_to_ratfrac_at_point_ratfrac_polynom_mpz (R, A, &pnt);
  ba0_restore (&M);
}
