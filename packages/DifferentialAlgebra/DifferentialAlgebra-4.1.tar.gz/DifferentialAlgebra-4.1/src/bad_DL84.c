#include "bad_DL84.h"
#include "bad_reduction.h"
#include "bad_regularize.h"

/*
 * texinfo: bad_positive_integer_roots_polynom_mod_regchain
 * Assign to @var{T} the positive integer roots of @var{P},
 * viewed as a univariate polynomial in @var{v}, with coefficients
 * taken modulo the ideal defined by @var{A}.
 * If @var{v} is @code{BAV_NOT_A_VARIABLE}, it is supposed to
 * be the leader of @var{P}.
 * The roots are sorted by increasing value.
 */

BAD_DLL void
bad_positive_integer_roots_polynom_mod_regchain (
    struct ba0_tableof_mpz *T,
    struct bap_polynom_mpz *P,
    struct bav_variable *v,
    struct bad_regchain *A)
{
  struct baz_tableof_ratfrac U;
  struct bav_point_int_p point;
  struct bap_tableof_polynom_mpq V;
  struct bap_polynom_mpq Q;
  struct bav_variable *u;
  bav_Iordering r;
  ba0_int_p d, i, j;
  struct ba0_mark M0, M1;

  ba0_reset_table ((struct ba0_table *) T);

  if (v == BAV_NOT_A_VARIABLE)
    v = bap_leader_polynom_mpz (P);

  d = bap_degree_polynom_mpz (P, v);

  if (d < 1)
    return;

  ba0_push_another_stack ();
  ba0_record (&M0);

  {
    struct bap_polynom_mpz C;
/*
 * U the table of the normal forms of the coefficients of P
 */
    bap_init_polynom_mpz (&C);
    ba0_init_table ((struct ba0_table *) &U);
    ba0_realloc2_table ((struct ba0_table *) &U, d + 1,
        (ba0_new_function *) & baz_new_ratfrac);
    for (i = 0; i <= d; i++)
      {
        bap_coeff_polynom_mpz (&C, P, v, i);
        bad_normal_form_polynom_mod_regchain (U.tab[i], &C, A,
            (struct bap_polynom_mpz **) 0);
      }
  }
/*
 * Update the degree d
 */
  while (d > 0 && baz_is_zero_ratfrac (U.tab[d]))
    d -= 1;
  U.size = d + 1;
  if (d == 0)
    {
      ba0_pull_stack ();
      ba0_restore (&M0);
      return;
    }
/*
 * vars the table of the variables occuring in the denominators
 */
  ba0_record (&M1);

  {
    struct bav_tableof_variable vars;

    bav_R_mark_variables (false);
    for (i = 0; i <= d; i++)
      bap_mark_indets_polynom_mpz (&U.tab[i]->denom);
    ba0_init_table ((struct ba0_table *) &vars);
    bav_R_marked_variables (&vars, true);
/*
 * point the evaluation point in order to get rid of denominators
 */
    ba0_init_point ((struct ba0_point *) &point);
    ba0_realloc2_table ((struct ba0_table *) &point, vars.size,
        (ba0_new_function *) & ba0_new_value);
    for (i = 0; i < vars.size; i++)
      {
        point.tab[i]->var = vars.tab[i];
        point.tab[i]->value = 0;
      }
    point.size = vars.size;
    ba0_sort_point ((struct ba0_point *) &point, (struct ba0_point *) &point);
  }

  if (point.size > 0)
    {
      struct bap_tableof_polynom_mpz nonzero;
      struct bap_product_mpz prod;
/*
 * nonzero the table of the polynomials which must not vanish:
 * - the denominators
 * - the numerator of the leading coefficient
 */
      ba0_init_table ((struct ba0_table *) &nonzero);
      ba0_realloc_table ((struct ba0_table *) &nonzero, d + 2);
      for (i = 0; i <= d; i++)
        nonzero.tab[i] = &U.tab[i]->denom;
      nonzero.tab[d + 1] = &U.tab[d]->numer;
      nonzero.size = d + 2;
/*
 * Computation of the evaluation point
 */
      bap_init_product_mpz (&prod);
      baz_yet_another_point_int_p_mpz (&point, &nonzero, &prod,
          BAV_NOT_A_VARIABLE);
    }
/*
 * V the table of the polynomials obtained by evaluation of the normal forms
 */
  ba0_init_table ((struct ba0_table *) &V);
  ba0_realloc2_table ((struct ba0_table *) &V, d + 1,
      (ba0_new_function *) & bap_new_polynom_mpq);
  for (i = 0; i <= d; i++)
    baz_eval_to_polynom_at_point_int_p_ratfrac (V.tab[i], U.tab[i], &point);
  V.size = d + 1;
/*
 * The variable v becomes the lowest variable
 */
  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);
  bav_R_set_minimal_variable (v);

  {
    struct bap_geobucket_mpq geo;
/*
 * Q the polynomial obtained by forming the sum of the V[i] * v**i
 */
    bap_init_geobucket_mpq (&geo);
    bap_init_polynom_mpq (&Q);
    for (i = 0; i <= d; i++)
      {
        bap_sort_polynom_mpq (V.tab[i], V.tab[i]);
        bap_mul_polynom_variable_mpq (&Q, V.tab[i], v, i);
        bap_add_geobucket_mpq (&geo, &Q);
      }
    bap_set_polynom_geobucket_mpq (&Q, &geo);
  }

/*
 * W the table of the coefficients of Q (coefficients being polynomials in v)
 * Q the gcd of the elements of W
 */
  u = bav_R_smallest_greater_variable (v);
  if (u != BAV_NOT_A_VARIABLE)
    {
// if (u == BAV_NOT_A_VARIABLE) there is nothing to do
      struct bap_tableof_polynom_mpz W;
      struct bap_polynom_mpq C;
      struct bap_itercoeff_mpq iter;
      struct bap_polynom_mpz gcd;
      struct bap_product_mpz gcd_prod;

      ba0_init_table ((struct ba0_table *) &W);
      bap_init_readonly_polynom_mpq (&C);
      bap_begin_itercoeff_mpq (&iter, &Q, u);
      while (!bap_outof_itercoeff_mpq (&iter))
        {
          if (W.size == W.alloc)
            {
              ba0_realloc2_table ((struct ba0_table *) &W, 2 * W.alloc + 1,
                  (ba0_new_function *) & bap_new_polynom_mpz);
            }
          bap_coeff_itercoeff_mpq (&C, &iter);
          bap_numer_polynom_mpq (W.tab[W.size], (ba0__mpz_struct *) 0, &C);
          W.size += 1;
          bap_next_itercoeff_mpq (&iter);
        }
      bap_close_itercoeff_mpq (&iter);
      bap_init_product_mpz (&gcd_prod);
      baz_gcd_tableof_polynom_mpz (&gcd_prod, &W, false);
      bap_init_polynom_mpz (&gcd);
      bap_expand_product_mpz (&gcd, &gcd_prod);
      bap_set_polynom_numer_denom_mpq (&Q, &gcd, (ba0__mpz_struct *) 0);
    }
/*
 * Compute the positive integer roots of Q
 */
  ba0_pull_stack ();
  if (bap_is_numeric_polynom_mpq (&Q))
    ba0_reset_table ((struct ba0_table *) T);
  else
    baz_positive_integer_roots_polynom_mpq (T, &Q);
  ba0_push_another_stack ();
/*
 * Remove the temporary ranking
 */
  bav_R_pull_ordering ();
  bav_R_free_ordering (r);
  ba0_restore (&M1);
/*
 * Remove the roots of Q which are not roots of P
 */
  {
    struct baz_ratfrac result;

    i = T->size - 1;
    baz_init_ratfrac (&result);
    while (i >= 0)
      {
// Horner scheme
        baz_set_ratfrac (&result, U.tab[d]);
        for (j = d - 1; j >= 0; j--)
          {
            baz_mul_ratfrac_numeric (&result, &result, T->tab[i]);
            baz_add_ratfrac (&result, &result, U.tab[j]);
          }
// The ba0_delete_table function does not allocate memory
        if (!baz_is_zero_ratfrac (&result))
          ba0_delete_table ((struct ba0_table *) T, i);
        i -= 1;
      }
  }

  ba0_pull_stack ();
  ba0_restore (&M0);
}

/*
 * texinfo: bad_parameters_of_polynom_mod_regchain
 * The rational fraction @var{P} is viewed as a polynomial in @var{q}
 * with coefficients taken modulo the regular chain @var{A}.
 * Assign to @var{X} the set of non leaders of @var{A}
 * the coefficients of @var{P} depend on, modulo @var{A}.
 * Exception @code{BA0_ERRALG} is raised if the denominator of @var{P}
 * depend on @var{q}.
 */

BAD_DLL void
bad_parameters_of_polynom_mod_regchain (
    struct bav_tableof_variable *X,
    struct baz_ratfrac *P,
    struct bav_variable *q,
    struct bad_regchain *A)
{
  struct baz_ratfrac Q, tmp1, tmp2, lcoeff;
  struct bap_itercoeff_mpz iter;
  struct bap_polynom_mpz coeff;
  struct bav_tableof_variable Y;
  bav_Iordering r;
  struct ba0_mark M;

  if (bap_degree_polynom_mpz (&P->denom, q) > 0)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  if (bap_degree_polynom_mpz (&P->numer, q) < 1)
    ba0_reset_table ((struct ba0_table *) X);
  else
    {
      ba0_push_another_stack ();
      ba0_record (&M);

      r = bav_R_copy_ordering (bav_R_Iordering ());
      bav_R_push_ordering (r);
      bav_R_set_maximal_variable (q);

      ba0_init_table ((struct ba0_table *) &Y);

      baz_init_readonly_ratfrac (&Q);
      baz_sort_ratfrac (&Q, P);
      baz_init_ratfrac (&tmp1);
      baz_init_ratfrac (&tmp2);
      baz_init_ratfrac (&lcoeff);
      bap_init_readonly_polynom_mpz (&coeff);

      bap_begin_itercoeff_mpz (&iter, &Q.numer, q);
      bap_coeff_itercoeff_mpz (&coeff, &iter);
      baz_set_ratfrac_fraction (&lcoeff, &coeff, &Q.denom);
      bap_next_itercoeff_mpz (&iter);
/*
 * Let P = Q = a_n * q**n + ... + a_1 * q + q_0
 * The idea consists in computing
 *
 *  NF(a_{n-1}/a_n), ..., NF(a_1/a_n), NF(a_0/a_n)
 *
 * and extract the variables which occur in these normal forms
 * but are not leaders of any element of te regular chain A
 * (the regular chain is supposed to be non-differential).
 */
      while (!bap_outof_itercoeff_mpz (&iter))
        {
          ba0_int_p i;

          bap_coeff_itercoeff_mpz (&coeff, &iter);
          baz_set_ratfrac_fraction (&tmp1, &coeff, &Q.denom);
          baz_div_ratfrac (&tmp2, &tmp1, &lcoeff);
          bad_normal_form_ratfrac_mod_regchain (&tmp1, &tmp2, A,
              (struct bap_polynom_mpz **) 0);
          ba0_realloc_table ((struct ba0_table *) &Y,
              Y.size + tmp1.numer.total_rank.size + tmp1.denom.total_rank.size);
          for (i = 0; i < tmp1.numer.total_rank.size; i++)
            {
              struct bav_variable *v = tmp1.numer.total_rank.rg[i].var;
              if (!bad_is_leader_of_regchain (v, A, (ba0_int_p *) 0))
                {
                  Y.tab[Y.size] = v;
                  Y.size++;
                }
            }
/*
 * Denominators of normal forms mod A do not depend on any leader of A
 */
          for (i = 0; i < tmp1.denom.total_rank.size; i++)
            {
              struct bav_variable *v = tmp1.denom.total_rank.rg[i].var;
              Y.tab[Y.size] = v;
              Y.size++;
            }
          bap_next_itercoeff_mpz (&iter);
        }

      ba0_sort_table ((struct ba0_table *) &Y, (struct ba0_table *) &Y);
      ba0_unique_table ((struct ba0_table *) &Y, (struct ba0_table *) &Y);

      bav_R_pull_ordering ();
      bav_R_free_ordering (r);

      ba0_pull_stack ();
      ba0_set_table ((struct ba0_table *) X, (struct ba0_table *) &Y);
      ba0_restore (&M);
    }
}

/*
BAD_DLL bav_Idegree
bad_separant_valuation_mod_regchain_polynom_mpz (
    struct bap_polynom_mpz *P,
    struct bad_regchain *A,
    struct baz_point_ratfrac *point,
    struct bav_tableof_variable *nulles)
{
  struct baz_ratfrac Q;
  struct ba0_mark M;
  bav_Idegree deg;

  ba0_push_another_stack ();
  ba0_record (&M);

  baz_init_ratfrac (&Q);
  baz_set_ratfrac_polynom_mpz (&Q, P);
  ba0_pull_stack ();
  deg = bad_separant_valuation_mod_regchain_ratfrac (&Q, A, point, nulles);
  ba0_restore (&M);
  return deg;
}
 */

/*
 * texinfo: bad_separant_valuation_mod_regchain_ratfrac
 * Assign to @var{c0} and @var{k} the rational fraction @math{c_0} and
 * the valuation @var{k} defined as follows [DL84, Lemma 2.3, (1), page 216].
 *
 * @displaymath
 * {S_P (x,\bar{y}, \bar{y}', \ldots)} =
 *  {c_0\,x^k + c_1\,x^{k+1} + \cdots {} \quad (c_0 \neq 0) \ @var{mod}\ A}
 * @end displaymath
 *
 * where @math{S_P} denotes the separant of @var{P}.
 * The initial value encoding series @math{\bar{y}, \bar{z}, \ldots}
 * are provided by @var{point}. These series may depend on variables
 * constrained by the algebraic relations provided by the regular
 * chain @var{A}.
 *
 * If @var{point} contains values for independent variables such as
 * @math{x:0}, they are not taken into account.
 * The table @var{nulles} contains derivatives which should be rewritten
 * to zero during the differentiation process of the differential 
 * evaluation at @var{point}.
 *
 * If the valuation is infinite then @var{k} is set to @math{-1}
 * and @var{c0} is left unchanged.
 *
 * Exception @code{BA0_ERRIVZ} is raised if the denominator of
 * the separant is zero modulo @var{A}.
 * Exception @code{BA0_ERRNYP} is raised if the denominator of
 * the separant evaluates to an expression depending on independent variables.
 */

BAD_DLL void
bad_separant_valuation_mod_regchain_ratfrac (
    struct baz_ratfrac *c0,
    bav_Idegree *k,
    struct baz_ratfrac *P,
    struct bad_regchain *A,
    struct baz_point_ratfrac *point,
    struct bav_tableof_variable *nulles)
{
  struct baz_point_ratfrac pnt;
  struct baz_ratfrac S, val_S;
  struct bap_polynom_mpz coeff2;
  struct bav_variable *w;
  bav_Idegree kk;
  bav_Iordering r;
  ba0_int_p i;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  baz_init_ratfrac (&S);
  baz_separant_ratfrac (&S, P);
/*
 * In the separant, independent variables must not be evaluated
 */
  ba0_init_point ((struct ba0_point *) &pnt);
  bav_delete_independent_values_point ((struct ba0_point *) &pnt,
      (struct ba0_point *) point);
/*
 * val_S = the separant evaluated at pnt
 */
  baz_init_ratfrac (&val_S);
  baz_evaluate_to_ratfrac_at_point_ratfrac_ratfrac (&val_S, &S, &pnt, nulles);
/*
 * The denominator of val_S 
 * - must be nonzero (BA0_ERRIVZ)
 * - must not depend on any independent variable (BA0_ERRNYP)
 */
  if (bad_is_a_reduced_to_zero_polynom_by_regchain (&val_S.denom, A,
          bad_algebraic_reduction))
    BA0_RAISE_EXCEPTION (BA0_ERRIVZ);

  for (i = 0; i < val_S.denom.total_rank.size; i++)
    {
      struct bav_variable *v = val_S.denom.total_rank.rg[i].var;
      if (bav_symbol_type_variable (v) == bav_independent_symbol)
        BA0_RAISE_EXCEPTION (BA0_ERRNYP);
    }
/*
 * Create a new ordering and set the independent variables as maximal variables
 */
  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);

  bap_init_polynom_mpz (&coeff2);

  w = BAV_NOT_A_VARIABLE;
  for (i = 0; i < val_S.numer.total_rank.size; i++)
    {
      struct bav_variable *v = val_S.numer.total_rank.rg[i].var;
      if (bav_symbol_type_variable (v) == bav_independent_symbol)
        {
          if (w == BAV_NOT_A_VARIABLE)
            w = v;
          bav_R_set_maximal_variable (v);
        }
    }
/*
 * w = the first (= lowest) independent variable set as maximal variable
 */
  if (w != BAV_NOT_A_VARIABLE)
    {
      struct bap_itercoeff_mpz iter;
      struct bap_polynom_mpz numer, denom, coeff;
      bool found;

      bap_init_readonly_polynom_mpz (&numer);
      bap_init_readonly_polynom_mpz (&denom);
      bap_init_readonly_polynom_mpz (&coeff);
      bap_sort_polynom_mpz (&numer, &val_S.numer);
      bap_sort_polynom_mpz (&denom, &val_S.denom);

      bap_end_itercoeff_mpz (&iter, &numer, w);
      found = false;
/*
 * Look for the lowest coefficient which is nonzero mod A
 */
      while (!bap_outof_itercoeff_mpz (&iter) && !found)
        {
          bap_coeff_itercoeff_mpz (&coeff, &iter);
          bap_set_polynom_mpz (&coeff2, &coeff);
/*
 * A rational fraction is zero iff its numerator is zero
 */
          bav_R_pull_ordering ();
          bap_physort_polynom_mpz (&coeff2);
          if (!bad_is_a_reduced_to_zero_polynom_by_regchain (&coeff2, A,
                  bad_algebraic_reduction))
            found = true;
          bav_R_push_ordering (r);

          if (!found)
            bap_prev_itercoeff_mpz (&iter);
        }
      if (!found)
        kk = -1;
      else
        {
          struct bav_term term;

          bav_init_term (&term);
          bap_term_itercoeff_mpz (&term, &iter);
          kk = bav_total_degree_term (&term);
        }
    }

  bav_R_pull_ordering ();
  bav_R_free_ordering (r);
/*
 * the ordering of coeff2 is the right one
 */
  ba0_pull_stack ();

  if (w != BAV_NOT_A_VARIABLE)
    {
/*
 * val_S depends on independent variables
 * Then either all coefficients are zero (kk == -1) 
 *          or there is one nonzero coefficient (kk >= 0)
 */
      if (kk != -1 && c0 != BAZ_NOT_A_RATFRAC)
        baz_set_ratfrac_fraction (c0, &coeff2, &val_S.denom);
    }
  else if (!baz_is_zero_ratfrac (&val_S))
    {
/*
 * val_S = c0
 */
      kk = 0;
      if (c0 != BAZ_NOT_A_RATFRAC)
        baz_set_ratfrac (c0, &val_S);
    }
  else
/*
 * val_S = 0
 */
    kk = -1;

  *k = kk;

  ba0_restore (&M);
}

/*
 * texinfo: bad_Hurwitz_coeffs_ratfrac
 * Assign to @var{fn} the table @math{[f_n, f_{n+1}, \ldots, f_{n+k}]}
 * of the Hurwitz coefficients defined by
 * 
 * @displaymath 
 * P^{(2\,k+2)} =
 *  y^{(n+2\,k+2)}\,f_n +
 *  y^{(n+2\,k+1)}\,f_{n+1} + \cdots +
 *  y^{(n+k+2)}\,f_{n+k} + f_{n+k+1}
 * @end displaymath
 *
 * where the leader of @var{P} is @math{y^{(n)}},
 * the @math{f_i} are polynomials in @math{y} of order at most @math{i}
 * and @math{f_n} is the separant of @var{P}. 
 * Differentiations are performed w.r.t. @var{x}.
 * The array @var{nulles} contains derivatives which should be rewritten
 * to zero during differentiation.
 *
 * The formula is due to Hurwitz (1889).
 * It is used in [DL84, Lemma 2.2, page 215] with @var{k} computed
 * from @code{bad_separant_valuation_mod_regchain}.
 */

BAD_DLL void
bad_Hurwitz_coeffs_ratfrac (
    struct baz_tableof_ratfrac *fn,
    struct baz_ratfrac *P,
    ba0_int_p k,
    struct bav_symbol *x,
    struct bav_tableof_variable *nulles)
{
  struct baz_ratfrac P_2k_2;
  struct bap_polynom_mpz coeff;
  struct bav_term theta;
  struct bav_variable *u, *v, *w;
  struct ba0_mark M;
  ba0_int_p i;

  ba0_realloc2_table ((struct ba0_table *) fn, k + 1,
      (ba0_new_function *) & baz_new_ratfrac);

  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * P_2k_2 = P^{(2k + 2)}
 */
  baz_init_ratfrac (&P_2k_2);
  baz_diff_ratfrac (&P_2k_2, P, x, nulles);
  for (i = 1; i < 2 * k + 2; i++)
    baz_diff_ratfrac (&P_2k_2, &P_2k_2, x, nulles);
// u = y^{(n)}
  u = baz_leader_ratfrac (P);
  v = bav_R_symbol_to_variable (x);
// w = y^{(n + k + 2)}
  bav_init_term (&theta);
  bav_set_term_variable (&theta, v, k + 2);
  w = bav_diff2_variable (u, &theta);

  bap_init_polynom_mpz (&coeff);
  for (i = 0; i <= k; i++)
    {
// w = y^{(n + 2k + 2 - i)}
      bav_set_term_variable (&theta, v, 2 * k + 2 - i);
      w = bav_diff2_variable (u, &theta);
// coeff = coeff (numer (P_2k_2), w)
      bav_set_term_variable (&theta, w, 1);
      bap_coeff_polynom_mpz (&coeff, &P_2k_2.numer, w, 1);
// fn[i] = coeff / denom (P_2k_2) or zero if coeff = 0 mod A
      ba0_pull_stack ();
      baz_set_ratfrac_fraction (fn->tab[i], &coeff, &P_2k_2.denom);
      fn->size = i + 1;
      ba0_push_another_stack ();
    }
  ba0_pull_stack ();
  ba0_restore (&M);
}

/*
 * texinfo: bad_DL_prolongation_prerequisites_mod_regchain
 * Assign to @var{c0}, @var{k}, @var{r} and @var{lcoeff} the rational
 * fraction @math{c_0}, the nonnegative integers
 * @var{k} and @var{r} and the following polynomial
 * defined in [DL84, Lemma 2.3, page 216]
 *
 * @displaymath
 * @var{lcoeff} = 
 * \left[f_{n+r} + q\,f'_{n+r-1} + \cdots +
 *      {q \choose r} \, f_n^{(r)}\right] (0, \bar{y}(0), \bar{y}'(0), \ldots)
 * @end displaymath
 *
 * The arguments @var{c0} and @var{k} are computed by calling
 * @code{bad_separant_valuation_mod_regchain_ratfrac} (see this
 * function).
 *
 * The rational fraction @var{P} contains the ODE under study.
 * The symbol @var{x} contains the derivation.
 * The variable @var{q} contains the indeterminate @math{q} of the formula.
 * The initial value encoding series @math{\bar{y}, \bar{z}, \ldots}
 * are provided by @var{point}. These series may depend on variables
 * constrained by the algebraic relations provided by the regular
 * chain @var{A}. The expansion point @math{x:\alpha} must be
 * provided by @var{point} also (note that @math{alpha} may be
 * different from zero).
 *
 * If the valuation of the separant is infinite then @var{k}
 * is assigned @math{-1} and the other arguments are left unchanged.
 *
 * The table @var{nulles} contains derivatives which should be rewritten
 * to zero during the differentiation process.
 *
 * Exception @code{BAP_ERRIND} is raised if the numerator of @var{P} 
 * does not depend on any dependent variable.
 * Exception @code{BAD_ERRIPT} is raised if @var{point} does not
 * contain any value of the form @math{x:\alpha}.
 */

BAD_DLL void
bad_DL_prolongation_prerequisites_mod_regchain (
    struct baz_ratfrac *c0,
    ba0_int_p *k,
    ba0_int_p *r,
    struct baz_ratfrac *lcoeff,
    struct baz_ratfrac *P,
    struct bav_symbol *x,
    struct bav_variable *q,
    struct bad_regchain *A,
    struct baz_point_ratfrac *point,
    struct bav_tableof_variable *nulles)
{
  struct baz_point_ratfrac x_equal_alpha;
  struct baz_tableof_ratfrac fn, der_fn, T;
  struct baz_ratfrac tmp;
  struct bap_tableof_polynom_mpq binomial;
  struct bap_polynom_mpq bin_fact;
  struct bav_variable *var_x;
  struct ba0_mark M;
  ba0_int_p kk, j;
  bool found;
/*
 * P should depend on a dependent variable
 * The denominator, if any, should not depend on dependent variables
 */
  if (bap_is_independent_polynom_mpz (&P->numer, &bav_global.parameters))
    BA0_RAISE_EXCEPTION (BAP_ERRIND);
/*
  else if (!bap_is_independent_polynom_mpz (&P->denom, &bav_global.parameters))
    BA0_RAISE_EXCEPTION (BA0_ERRNYP);
 */
  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * x_equal_alpha = { x:alpha }
 */
  var_x = bav_R_symbol_to_variable (x);
  ba0_init_point ((struct ba0_point *) &x_equal_alpha);
  ba0_realloc_table ((struct ba0_table *) &x_equal_alpha, 1);
  x_equal_alpha.tab[0] =
      (struct baz_value_ratfrac *) ba0_bsearch_point (var_x,
      (struct ba0_point *) point, (ba0_int_p *) 0);
  x_equal_alpha.size = 1;
/*
 * point must contain x:alpha
 */
  if ((struct ba0_value *) x_equal_alpha.tab[1] == BA0_NOT_A_VALUE)
    BA0_RAISE_EXCEPTION (BAD_ERRIPT);
/*
 * kk = the valuation of the separant of P (denoted k in [DL84, Lemma 2.3]
 */
  ba0_pull_stack ();
  bad_separant_valuation_mod_regchain_ratfrac (c0, &kk, P, A, point, nulles);
  ba0_push_another_stack ();

  *k = kk;

  if (kk >= 0)
    {
/*
 * fn = [f_n, f_{n+1}, f_{n+2}, ..., f_{n+k}]
 */
      ba0_init_table ((struct ba0_table *) &fn);
      bad_Hurwitz_coeffs_ratfrac (&fn, P, kk, x, nulles);
/*
 * successive values of der_fn are
 * [f_n]    (initial value)
 * [f_{n+1}, f_n']
 * [f_{n+2}, f_{n+1}', f_n'']
 *      ...
 */
      ba0_init_table ((struct ba0_table *) &der_fn);
      ba0_realloc2_table ((struct ba0_table *) &der_fn, kk + 1,
          (ba0_new_function *) & baz_new_ratfrac);
      der_fn.tab[0] = fn.tab[0];
      der_fn.size = 1;
/*
 * T = der_fn evaluated at point
 *     each T[i] being simplified to 0 if T[i] is reduced to 0 by A
 */
      ba0_init_table ((struct ba0_table *) &T);
      ba0_realloc2_table ((struct ba0_table *) &T, kk + 1,
          (ba0_new_function *) & baz_new_ratfrac);
      baz_twice_evaluate_to_ratfrac_at_point_ratfrac_ratfrac (T.tab[0],
          der_fn.tab[0], point, &x_equal_alpha, nulles);
      T.size = 1;
/*
 * successive values of binomial are
 * [1]
 * [1, q]
 * [1, q, q(q-1)/2]
 *      ...
 */
      bap_init_polynom_mpq (&bin_fact);
      ba0_init_table ((struct ba0_table *) &binomial);
      ba0_realloc2_table ((struct ba0_table *) &binomial, kk + 1,
          (ba0_new_function *) & bap_new_polynom_mpq);
      bap_set_polynom_one_mpq (binomial.tab[0]);
      binomial.size = 1;
/*
 * We stop at the first index r (= T.size - 1) such that some T[i] is nonzero
 */
      found =
          !bad_is_a_reduced_to_zero_polynom_by_regchain (&T.tab[T.size -
              1]->numer, A, bad_algebraic_reduction);
      while (!found)
        {
          for (j = der_fn.size; j > 0; j--)
            baz_diff_ratfrac (der_fn.tab[j], der_fn.tab[j - 1], x, nulles);
          der_fn.tab[0] = fn.tab[der_fn.size];
          der_fn.size += 1;

          for (j = 0; j <= T.size; j++)
            {
              baz_twice_evaluate_to_ratfrac_at_point_ratfrac_ratfrac (T.tab[j],
                  der_fn.tab[j], point, &x_equal_alpha, nulles);
              if (!bad_is_a_reduced_to_zero_polynom_by_regchain (&T.
                      tab[j]->numer, A, bad_algebraic_reduction))
                found = true;
              else
                baz_set_ratfrac_zero (T.tab[j]);
            }
          T.size += 1;

          if (T.size == kk + 1 && !found)
            BA0_RAISE_EXCEPTION (BA0_ERRALG);

          ba0_scanf_printf ("%Aq", "(%v - %d)/%d", &bin_fact, q,
              binomial.size - 1, binomial.size);
          bap_mul_polynom_mpq (binomial.tab[binomial.size],
              binomial.tab[binomial.size - 1], &bin_fact);
          binomial.size += 1;
        }
/*
 * R = sum_{j = 0}^r T[j] * binomial[j]
 *
 * The result is stored in T[0] to save a rational fraction
 */
      baz_init_ratfrac (&tmp);
      for (j = 1; j < T.size; j++)
        {
          baz_mul_ratfrac_polynom_mpq (&tmp, T.tab[j], binomial.tab[j]);
          baz_add_ratfrac (T.tab[0], T.tab[0], &tmp);
        }

      *r = T.size - 1;

      ba0_pull_stack ();
      baz_set_ratfrac (lcoeff, T.tab[0]);
    }
  ba0_restore (&M);
}

/*
 * texinfo: bad_DL_a_priori_prolongation_bounds_mod_regchain
 * Assign to @var{bounds} values of the form @math{y = d} where
 * the @var{y} are the differential indeterminates of the leaders of the 
 * elements of @var{A}. For each @var{y}, the degree @var{d} provides a 
 * minimal bound on the number of prolongations of the corresponding 
 * elements of @var{A} for computing the prolongation system.
 * These bounds are a priori bounds because they may be increased
 * by @code{bad_DL_a_priori_prolongation_bounds_mod_regchain}.
 * They are uniquely determined by considering the coefficients
 * of the initial value encoding series provided by @var{point}:
 * numeric coefficients, coefficients which depend on variables
 * which occur in some other coefficient in @var{point} or in
 * some algebraic relation in @var{A}.

BAD_DLL void
bad_DL_a_priori_prolongation_bounds_mod_regchain (
    struct bav_point_int_p *bounds,
    struct bav_symbol *x,
    struct bad_regchain *A,
    struct baz_point_ratfrac *point)
{
  struct baz_ratfrac R, Q;
  struct bap_itercoeff_mpz iter;
  struct bap_polynom_mpz coeff;
  struct bav_tableof_int_p counter;
  struct bav_term term;
  struct bav_tableof_variable V;
  struct bav_variable *var_x;
  bav_Iordering r;
  ba0_int_p i, j, n;
  struct ba0_mark M;
 *
 * bounds = a point with values y = degree (one per element of A) where
 * y      = the differential indeterminate of the leader of the element of A
 * degree = the prolongation bound
 * 
  ba0_reset_point ((struct ba0_point *) bounds);
  ba0_realloc2_table ((struct ba0_table *) bounds, A->decision_system.size,
      (ba0_new_function *) & ba0_new_value);
  for (i = 0; i < A->decision_system.size; i++)
    {
      struct bav_variable *u;
      u = bap_leader_polynom_mpz (A->decision_system.tab[i]);
      y = bav_order_zero_variable (u);
      bounds->tab[i]->var = y;
      bounds->tab[i]->value = 0;
    }
  bounds->size = A->decision_system.size;

  ba0_push_another_stack ();
  ba0_record (&M);

 *
 * V = all variables occuring in the right hand sides of point
 * 
  bav_R_mark_variables (false);
  for (i = 0; i < point->size; i++)
    {
      struct baz_ratfrac *Q = point->value->value;
      baz_mark_indets_ratfrac (Q);
    }
  ba0_init_table ((struct ba0_table *) &V);
  bav_R_marked_variables (&V, true);
 *
 * counter = is a point with values (var = number of occurences)
 *
 * The left hand sides of the values are the variables of V 
 * i.e. all variables in the right hand sides of point - except x
 *
 * The right hand sides are initialized to zero.
 * 
  ba0_init_point ((struct ba0_point *) &counter);
  ba0_realloc2_table ((struct ba0_table *) &counter, V.size,
      (ba0_new_function *) & ba0_new_value);
  for (i = 0; i < V.size; i++)
    {
      counter.tab[i]->var = V.tab[i];
      counter.tab[i]->value = 0;
    }
  counter.size = V.size;
  ba0_sort_point ((struct ba0_point *) &counter);
  var_x = bav_R_symbol_to_variable (x);
  if (ba0_bsearch_point (var_x, &counter, &i) != (struct ba0_value *) 0)
    ba0_delete_point ((struct ba0_point *) &counter, i);
 *
 * All variables in counter values which occur also in the regular chain have
 * their right hand sides set to one.
 * 
  for (i = 0; i < A->decision_system.size; i++)
    {
      struct bap_polynom_mpz *P = A->decision_system.tab[i];

      for (j = 0; j < P->total_rank.size; j++)
        {
          struct bav_variable *v = P->total_rank.rg[j].var;
          struct bav_value_int_p *val;

          val = (struct bav_value_int_p *) ba0_bsearch_point
              ((struct ba0_point *) &counter, v, (ba0_int_p *) 0);
          if (val)
            val->value = 1;
        }
    }
 *
 * Run again over all the right hand sides of point, coefficient
 * per coefficient (this is important) and increase the right hand
 * sides each time a variable occurs
 *
 * Eventually, all variables occuring in a value of point and
 * a) in another coefficient of the same value
 * b) in another value of point
 * c) in the regular chain
 * will have their counter >= 2
 *
 * All other variables will have their counter = 1
 * 
  r = bav_R_copy_ordering (bav_R_Iordering ());
  bav_R_push_ordering (r);
  bav_R_set_maximal_variable (var_x);

  baz_init_ratfrac (&R);
  baz_init_readonly_ratfrac (&Q);
  bap_init_readonly_polynom_mpz (&coeff);
  for (i = 0; i < point->size; i++)
    {
      baz_sort_ratfrac (&Q, point->value->value);
      bap_end_itercoeff_mpz (&iter, &Q->numer, var_x);
      while (!bap_outof_itercoeff_mpz (&iter))
        {
          bool zero;

          bap_coeff_itercoeff_mpz (&coeff, &iter);
 *
 * It is important to carefully rebuild the coefficients because
 * common factors - hence variables - may disappear
 * 
          baz_set_ratfrac_fraction (&R, &coeff, &Q->denom);

          bav_R_pull_ordering ();
          baz_physort_ratfrac (&R);
          zero = bad_is_a_reduced_to_zero_polynom_by_regchain (&R.numer, A,
              bad_algebraic_reduction);
          bav_R_push_ordering (r);

          if (!zero)
            {
              for (j = 0; j < R.numer.total_rank.size; j++)
                {
                  struct bav_variable *v = R.numer.total_rank.rg[j].var;
                  struct bav_value_int_p *val;
                  val = (struct bav_value_int_p *) ba0_bsearch_point
                      ((struct ba0_point *) &counter, v, (ba0_int_p *) 0);
                  val->value += 1;
                }
              for (j = 0; j < R.denom.total_rank.size; j++)
                {
                  struct bav_variable *v = R.denom.total_rank.rg[j].var;
                  struct bav_value_int_p *val;
                  val = (struct bav_value_int_p *) ba0_bsearch_point
                      ((struct ba0_point *) &counter, v, (ba0_int_p *) 0);
                  val->value += 1;
                }
            }
          bap_prev_itercoeff_mpz (&iter);
        }
      bap_close_itercoeff_mpz (&iter);
    }
 *
 * At this stage, we can determine if a prolongation bound must be
 * greater than of equal to d where coeff * x**d denotes some coefficient
 * of some right hand side of point. It is so if
 *
 * a) coeff is numeric 
 * b) coeff depends on a variable v such that the value of v in counter is >= 2
 *
 * Run again over all right hand sides of points, coefficient per coefficient
 * 
  bav_init_term (&term);

  for (i = 0; i < point->size; i++)
    {
      struct bav_variable *y = point->value->var;
      struct bav_value_int_p *val_bound;

      baz_sort_ratfrac (&Q, point->value->value);

      val_bound = (struct bav_value_int_p *) ba0_bsearch_point
          ((struct ba0_point *) bounds, y, (ba0_int_p *) 0);

      if (val_bound != (struct bav_value_int_p *) 0)
        {
          bap_end_itercoeff_mpz (&iter, &Q->numer, var_x);
          while (!bap_outof_itercoeff_mpz (&iter))
            {
              bav_Idegree d;

              bap_coeff_itercoeff_mpz (&coeff, &iter);
              bap_term_itercoeff_mpz (&term, &iter);
// !! Beware to numeric = 0 coefficient - not handled here
              d = bav_total_degree_term (&term);
 *
 * It is important to carefully rebuild the coefficients because
 * common factors - hence variables - may disappear
 * 
              baz_set_ratfrac_fraction (&R, &coeff, &Q->denom);

              if (baz_is_numeric_ratfrac (&R))
                val_bound->value = d;
              else
                {
                  bool zero;

                  bav_R_pull_ordering ();
                  baz_physort_ratfrac (&R);
                  zero = bad_is_a_reduced_to_zero_polynom_by_regchain (&R.numer,
                      A, bad_algebraic_reduction);
                  bav_R_push_ordering (r);

                  if (!zero)
                    {
                      for (j = 0; j < R.numer.total_rank.size; j++)
                        {
                          struct bav_variable *v = R.numer.total_rank.rg[j].var;
                          struct bav_value_int_p *val;
                          val = (struct bav_value_int_p *) ba0_bsearch_point
                              ((struct ba0_point *) &counter, v,
                              (ba0_int_p *) 0);
                          if (val->value >= 2)
                            val_bound->value = d;
                        }
                      for (j = 0; j < R.denom.total_rank.size; j++)
                        {
                          struct bav_variable *v = R.denom.total_rank.rg[j].var;
                          struct bav_value_int_p *val;
                          val = (struct bav_value_int_p *) ba0_bsearch_point
                              ((struct ba0_point *) &counter, v,
                              (ba0_int_p *) 0);
                          if (val->value >= 2)
                            val_bound->value = d;
                        }
                    }
                }
              bap_prev_itercoeff_mpz (&iter);
            }
          bap_close_itercoeff_mpz (&iter);
        }
    }

  bav_R_pull_ordering ();
  bav_R_free_ordering (r);

  ba0_pull_stack ();
  ba0_restore (&M);
}
 */

/*
 * texinfo: bad_DL_prolongated_system_mod_regchain
 * Assign to @var{T} the prolongated system obtained from the elements
 * of the regular chain @var{A} and the initial value encoding series
 * stored in @var{point}. Derivations are with respect to @var{x}.
 * The table @var{nulles} contains variables which should be rewritten
 * to zero during the differentiation processes.
 * The returned table @var{T} is sorted by increasing rank.
 *
 * For each element @var{P} of @var{A}, the nonnegative integers @var{k},
 * @var{r} and the polynomial @var{lcoeff} are computed using
 * @code{bad_DL_prolongation_prerequisites}. Then @var{gamma}
 * is computed as the smallest integer greater than all positive
 * integer roots of @var{lcoeff}. Then @var{beta} is defined
 * as @math{2\,k + 2 + @var{gamma} + r} [DL84, Lemma 2.3, (3)].
 * The first @var{beta} derivatives of @var{P}, evaluated at @var{point}
 * modulo @var{A}, are stored in @var{T}.
 *
 * Exception @code{BAD_ERRSFV} is raised if the separant valuation
 * of some element of @var{A} is infinite (@math{k = -1}).
 */

BAD_DLL void
bad_DL_prolongated_system_mod_regchain (
    struct baz_tableof_ratfrac *T,
    struct bad_regchain *A,
    struct baz_point_ratfrac *point,
    struct bav_symbol *x,
    struct bav_tableof_variable *nulles)
{
  struct baz_point_ratfrac x_equal_alpha;
  struct baz_ratfrac P, lcoeff;
  struct bap_polynom_mpz poly;
  struct bav_variable *var_x, *q;
  bav_Idegree k, r, beta, gamma;
  struct ba0_tableof_mpz roots;
  ba0_int_p i, j;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

/*
 * x_equal_alpha = { x:alpha }
 */
  var_x = bav_R_symbol_to_variable (x);
  ba0_init_point ((struct ba0_point *) &x_equal_alpha);
  ba0_realloc_table ((struct ba0_table *) &x_equal_alpha, 1);
  x_equal_alpha.tab[0] =
      (struct baz_value_ratfrac *) ba0_bsearch_point (var_x,
      (struct ba0_point *) point, (ba0_int_p *) 0);
  x_equal_alpha.size = 1;
/*
 * for bad_positive_integer_roots_mod_regchain
 */
  q = bav_R_new_temporary_variable ();

  ba0_init_table ((struct ba0_table *) &roots);
  baz_init_ratfrac (&P);
  baz_init_ratfrac (&lcoeff);
  bap_init_polynom_mpz (&poly);

  for (i = 0; i < A->decision_system.size; i++)
    {
      if (!bap_is_independent_polynom_mpz (A->decision_system.tab[i],
              &bav_global.parameters))
        {
          baz_set_ratfrac_polynom_mpz (&P, A->decision_system.tab[i]);
          bad_DL_prolongation_prerequisites_mod_regchain (BAZ_NOT_A_RATFRAC, &k,
              &r, &lcoeff, &P, x, q, A, point, nulles);
/*
 * The prolongation is meaningful for a finite valuation k of the separant
 * If it is not, the formal power series in point are likely to be too short
 */
          if (k == -1)
            BA0_RAISE_EXCEPTION (BAD_ERRSFV);
/*
 * gamma is bigger than the maximum of the positive integer roots of lcoeff
 */
          bad_positive_integer_roots_polynom_mod_regchain (&roots,
              &lcoeff.numer, q, A);
          if (roots.size == 0)
            gamma = 0;
          else
            gamma = 1 + ba0_mpz_get_si (roots.tab[roots.size - 1]);
/*
 * beta is the prolongation bound (series truncated mod x**beta)
 */
          beta = 2 * k + 2 + gamma + r;

          ba0_pull_stack ();
          if (T->size + beta > T->alloc)
            {
/*
 * Estimated overall size to avoid too many realloc
 */
              ba0_int_p size;
              size = T->size + (A->decision_system.size - i) * beta;
              ba0_realloc2_table ((struct ba0_table *) T, size,
                  (ba0_new_function *) & baz_new_ratfrac);
            }
/*
 * First rational fraction in T
 */
          baz_twice_evaluate_to_ratfrac_at_point_ratfrac_ratfrac (T->
              tab[T->size], &P, point, &x_equal_alpha, nulles);
          if (!baz_is_zero_ratfrac (T->tab[T->size]))
            T->size += 1;
          ba0_push_another_stack ();
/*
 * Next rational fractions
 */
          for (j = 1; j < beta; j++)
            {
              if (j == 1)
                bap_diff_polynom_mpz (&poly, A->decision_system.tab[i], x,
                    nulles);
              else
                bap_diff_polynom_mpz (&poly, &poly, x, nulles);
              baz_set_ratfrac_polynom_mpz (&P, &poly);

              ba0_pull_stack ();
              baz_twice_evaluate_to_ratfrac_at_point_ratfrac_ratfrac (T->
                  tab[T->size], &P, point, &x_equal_alpha, nulles);
              if (!baz_is_zero_ratfrac (T->tab[T->size]))
                T->size += 1;
              ba0_push_another_stack ();
            }
        }
    }
/*
 * That's all
 */
  bav_R_free_temporary_variable (q);
  ba0_pull_stack ();
/*
 * Sort the resulting table by increasing rank
 */
  qsort (T->tab, T->size, sizeof (struct baz_ratfrac *),
      &baz_compare_rank_ratfrac);
  ba0_restore (&M);
}
