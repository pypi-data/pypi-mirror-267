#include "bap_polynom_mint_hp.h"
#include "bap_add_polynom_mint_hp.h"
#include "bap_mul_polynom_mint_hp.h"
#include "bap_creator_mint_hp.h"
#include "bap_itermon_mint_hp.h"
#include "bap_geobucket_mint_hp.h"
#include "bap_diff_polynom_mint_hp.h"

#define BAD_FLAG_mint_hp

/*
 * texinfo: bap_is_constant_polynom_mint_hp
 * Return @code{true} if the derivative of @var{A} w.r.t. @var{s} is zero, 
 * else @code{false}. If @var{s} is zero, then return @code{true} if 
 * the derivatives of @var{A} w.r.t. all independent variables are zero, 
 * else @code{false}.
 */

BAP_DLL bool
bap_is_constant_polynom_mint_hp (
    struct bap_polynom_mint_hp *A,
    struct bav_symbol *s,
    struct bav_tableof_parameter *P)
{
  struct bav_variable *w;
  struct bav_symbol *y;
  ba0_int_p i, j, k;
  bool is_constant;

  is_constant = true;
  if (s == BAV_NOT_A_SYMBOL)
    {
      for (i = 0; i < A->total_rank.size && is_constant; i++)
        {
          w = A->total_rank.rg[i].var;
          y = w->root;
          if (bav_symbol_type_variable (w) == bav_independent_symbol)
            is_constant = false;
          else if (P != (struct bav_tableof_parameter *) 0
              && bav_is_a_parameter (y, &k, P))
            is_constant = P->tab[k]->dep.size == 0;
          else
            is_constant = false;
        }
    }
  else
    {
      for (i = 0; is_constant && i < A->total_rank.size; i++)
        {
          w = A->total_rank.rg[i].var;
          y = w->root;
          if (bav_symbol_type_variable (w) == bav_independent_symbol)
            is_constant = y != s;
          else if (P != (struct bav_tableof_parameter *) 0
              && bav_is_a_parameter (y, &k, P))
            {
              for (j = 0; is_constant && j < P->tab[k]->dep.size; j++)
                is_constant = P->tab[k]->dep.tab[j] != s;
            }
          else
            is_constant = false;
        }
    }
  return is_constant;
}

/*
 * texinfo: bap_is_independent_polynom_mint_hp
 * Return @code{true} if @var{A} does not depend on dependent variables 
 * (i.e. does not depend on derivatives, unless they are parameters)
 * else return @code{false}.
 */

BAP_DLL bool
bap_is_independent_polynom_mint_hp (
    struct bap_polynom_mint_hp *A,
    struct bav_tableof_parameter *P)
{
  struct bav_variable *w;
  struct bav_symbol *y;
  bool is_independent;
  ba0_int_p i, k;

  if (bap_is_zero_polynom_mint_hp (A))
    is_independent = true;
  else
    {
      is_independent = true;
      for (i = 0; is_independent && i < A->total_rank.size; i++)
        {
          w = A->total_rank.rg[i].var;
          y = w->root;
          if (bav_symbol_type_variable (w) == bav_dependent_symbol)
            {
              if (P != (struct bav_tableof_parameter *) 0
                  && bav_is_a_parameter (y, &k, P))
                is_independent = P->tab[k]->dep.size == 0;
              else
                is_independent = false;
            }
        }
    }
  return is_independent;
}

static void diff_monome_mint_hp (
    struct bap_polynom_mint_hp *,
    struct bav_term *,
    struct bap_itermon_mint_hp *,
    struct bav_symbol *,
    struct bav_tableof_variable *);

/*
 * Assigns d/ds A to R.
 * Rewrites to zero every variable which lies in nulles.
 */

/*
 * texinfo: bap_diff_polynom_mint_hp
 * Assign to @var{R} the polynomial obtained by differentiating @var{A}
 * w.r.t. @var{s}. Rewrite to zero any monomial involving a derivative of
 * any element of @var{nulles}.
 */

BAP_DLL void
bap_diff_polynom_mint_hp (
    struct bap_polynom_mint_hp *R,
    struct bap_polynom_mint_hp *A,
    struct bav_symbol *s,
    struct bav_tableof_variable *nulles)
{
  struct bap_itermon_mint_hp iter;
  struct bap_geobucket_mint_hp geo;
  struct bap_polynom_mint_hp R1;
  struct bav_term rgtot;
  bool commuting_derivations;
  struct ba0_mark M;

  if (R->readonly)
    BA0_RAISE_EXCEPTION (BA0_ERRALG);

  ba0_push_another_stack ();
  ba0_record (&M);

  commuting_derivations = true;
/*
				bap_commuting_derivations_mint_hp ();
*/

  if (commuting_derivations)
    {
      bav_init_term (&rgtot);
      bav_set_term (&rgtot, &A->total_rank);
      bav_diff_term (&rgtot, &rgtot, s, nulles);
    }

  bap_init_geobucket_mint_hp (&geo);
  bap_init_polynom_mint_hp (&R1);
  bap_begin_itermon_mint_hp (&iter, A);
  while (!bap_outof_itermon_mint_hp (&iter))
    {
      if (commuting_derivations)
        diff_monome_mint_hp (&R1, &rgtot, &iter, s, nulles);
/*
	else
	    diff_monome_comrel_mint_hp (&R1, &iter, s, nulles);
*/
      bap_add_geobucket_mint_hp (&geo, &R1);
      bap_next_itermon_mint_hp (&iter);
    }
  ba0_pull_stack ();
  bap_set_polynom_geobucket_mint_hp (R, &geo);
  ba0_restore (&M);
}

/*
   It is assumed that the ordering is such that a derivative is lower than
   its proper derivatives. This is a property of ordering but some functions
   alter orderings for their own purposes.
*/

static void
diff_monome_mint_hp (
    struct bap_polynom_mint_hp *R,
    struct bav_term *rgtot,
    struct bap_itermon_mint_hp *iter,
    struct bav_symbol *s,
    struct bav_tableof_variable *nulles)
{
  struct bap_creator_mint_hp crea;
  struct bav_term T, U;
  bav_Inumber num_der;
  bav_Inumber num_v, num_w, num_k = 0;
  bav_Idegree d;
  struct bav_variable *v, *w;
  enum bav_typeof_symbol type_v;
  ba0_mint_hp_t c;
  ba0_int_p j, k, n, m;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  v = bav_R_symbol_to_variable (s);
  num_der = v->number.tab[bav_R_Iordering ()];

  bav_init_term (&T);
  bav_init_term (&U);
  ba0_mint_hp_init (c);

  bap_term_itermon_mint_hp (&T, iter);
  bav_realloc_term (&U, T.size + 1);
  ba0_pull_stack ();

  bap_begin_creator_mint_hp (&crea, R, rgtot, bap_approx_total_rank, T.size);
/*
   The monomial may be zero
*/
  for (j = 0; j < T.size; j++)
    {
      if (bav_is_derivative2 (T.rg[j].var, nulles))
        goto fin;
    }
/*
   It is non zero
*/
  for (j = 0; j < T.size; j++)
    {
      v = T.rg[j].var;
      type_v = bav_symbol_type_variable (v);
      num_v = v->number.tab[bav_R_Iordering ()];
      d = T.rg[j].deg;
/*
   v^d is the current rank of the term. Let's differentiate it.
*/
      if (type_v == bav_dependent_symbol)
        {
          w = bav_diff_variable (v, s);
/*
   w may be zero.
*/
          if (bav_is_derivative2 (w, nulles))
            continue;
/*
   It is non zero
*/
          num_w = w->number.tab[bav_R_Iordering ()];
/* 
   Look for the index k at which the derivative w of v must be inserted.
*/
          for (k = j - 1;; k--)
            {
              if (k < 0)
                break;
              num_k = T.rg[k].var->number.tab[bav_R_Iordering ()];
              if (num_w <= num_k)
                break;
            }
/*
   Building the differentiated term.
*/
          n = 0;
          m = 0;
          if (k < 0)
            {
              U.size = T.size + 1;
              U.rg[n].var = w;
              U.rg[n++].deg = 1;
            }
          else
            {
              while (m < k)
                U.rg[n++] = T.rg[m++];
              if (num_w == num_k)
                {
                  U.size = T.size;
                  U.rg[n].var = T.rg[m].var;
                  U.rg[n++].deg = T.rg[m++].deg + 1;
                }
              else
                {
                  U.size = T.size + 1;
                  U.rg[n++] = T.rg[m++];
                  U.rg[n].var = w;
                  U.rg[n++].deg = 1;
                }
            }
          while (m < j)
            U.rg[n++] = T.rg[m++];
          if (d > 1)
            {
              U.rg[n].var = T.rg[m].var;
              U.rg[n++].deg = T.rg[m++].deg - 1;
            }
          else
            {
              U.size--;
              m++;
            }
          while (m < T.size)
            U.rg[n++] = T.rg[m++];
          if (d > 1)
            {
              ba0_push_another_stack ();
              ba0_mint_hp_mul_ui (c, *bap_coeff_itermon_mint_hp (iter),
                  (unsigned long int) d);
              ba0_pull_stack ();
              bap_write_creator_mint_hp (&crea, &U, c);
            }
          else
            bap_write_creator_mint_hp (&crea, &U,
                *bap_coeff_itermon_mint_hp (iter));
        }
      else if (type_v == bav_independent_symbol)
        {
          if (v->root == s)
            {
/*
   Building the differentiated term.
*/
              n = 0;
              m = 0;
              while (m < j)
                U.rg[n++] = T.rg[m++];
              if (d > 1)
                {
                  U.size = T.size;
                  U.rg[n].var = T.rg[m].var;
                  U.rg[n++].deg = T.rg[m++].deg - 1;
                }
              else
                {
                  U.size = T.size - 1;
                  m++;
                }
              while (m < T.size)
                U.rg[n++] = T.rg[m++];
              if (d > 1)
                {
                  ba0_push_another_stack ();
                  ba0_mint_hp_mul_ui (c, *bap_coeff_itermon_mint_hp (iter),
                      (unsigned long int) d);
                  ba0_pull_stack ();
                  bap_write_creator_mint_hp (&crea, &U, c);
                }
              else
                bap_write_creator_mint_hp (&crea, &U,
                    *bap_coeff_itermon_mint_hp (iter));
            }
          else if (num_v < num_der)
            break;
        }
      else
        break;
    }
fin:
  ba0_restore (&M);
  bap_close_creator_mint_hp (&crea);
}

/*
 * A derivation operator is encoded by a term.
 * Variables should be independent.
 *
 * Differentiates A w.r.t. the derivation operator. Result in R.
 */

/*
 * texinfo: bap_diff2_polynom_mint_hp
 * Assign to @var{R} the polynomial obtained by differentiating @var{A}
 * w.r.t. @var{theta}. Rewrite to zero any monomial involving a derivative of
 * any element of @var{nulles}.
 * The term @var{theta} encodes a derivation operator (every variable
 * should correspond to a derivation). 
 */

BAP_DLL void
bap_diff2_polynom_mint_hp (
    struct bap_polynom_mint_hp *R,
    struct bap_polynom_mint_hp *A,
    struct bav_term *T,
    struct bav_tableof_variable *nulles)
{
  bav_Idegree d;
  ba0_int_p i;
  bool first;

  if (bav_is_one_term (T))
    {
      if (R != A)
        bap_set_polynom_mint_hp (R, A);
    }
  else
    {
      first = true;
      for (i = 0; i < T->size; i++)
        {
          for (d = 0; d < T->rg[i].deg; d++)
            {
              bap_diff_polynom_mint_hp (R, first ? A : R, T->rg[i].var->root,
                  nulles);
              first = false;
            }
        }
    }
}

/*
 * texinfo: bap_involved_derivations_polynom_mint_hp
 * Append to @var{T} the derivations involved in the derivatives @var{A}
 * depends on. The independent variables occuring in @var{A} are not
 * taken into account.
 */

BAP_DLL void
bap_involved_derivations_polynom_mint_hp (
    struct bav_tableof_variable *T,
    struct bap_polynom_mint_hp *P)
{
  struct bav_variable *v, *x;
  ba0_int_p i, j;

  for (i = 0; i < P->total_rank.size; i++)
    {
      v = P->total_rank.rg[i].var;
      if (bav_symbol_type_variable (v) == bav_dependent_symbol)
        {
          for (j = 0; j < bav_global.R.ders.size; j++)
            {
              if (v->order.tab[j] > 0)
                {
                  x = bav_R_derivation_index_to_derivation (j);
                  if (!ba0_member_table (x, (struct ba0_table *) T))
                    {
                      ba0_realloc_table ((struct ba0_table *) T,
                          bav_global.R.ders.size);
                      T->tab[T->size] = x;
                      T->size += 1;
                    }
                }
            }
        }
    }
}

/*
 * texinfo: bap_zero_derivatives_of_tableof_parameter_mint_hp
 * Append to @var{T} the equations which state that the derivatives of
 * the elements of @var{P} are zero. However, the function does not
 * generate any equation @math{p} such that @math{p} is the derivative 
 * of the leader of some existing element of @var{T}.
 */

BAP_DLL void
bap_zero_derivatives_of_tableof_parameter_mint_hp (
    struct bap_tableof_polynom_mint_hp *T,
    struct bav_tableof_parameter *P)
{
  struct bav_tableof_variable nulles;
  struct bav_variable *v, *w;
  struct ba0_mark M;
  ba0_int_p i, j;
  bool found;

  ba0_push_another_stack ();
  ba0_record (&M);
  ba0_init_table ((struct ba0_table *) &nulles);
  bav_zero_derivatives_of_tableof_parameter (&nulles, P);
  ba0_pull_stack ();
/*
 * Remove from nulles, any variable p which is the derivative of the
 * leader of some already existing element of T.
 */
  i = 0;
  while (i < nulles.size)
    {
      v = nulles.tab[i];
      found = false;
      for (j = 0; j < T->size && !found; j++)
        {
          w = bap_leader_polynom_mint_hp (T->tab[j]);
          found = bav_is_derivative (v, w);
        }
      if (found)
        ba0_delete_table ((struct ba0_table *) &nulles, i);
      else
        i += 1;
    }
/*
 * Append nulles to T.
 */
  ba0_realloc2_table ((struct ba0_table *) T, T->size + nulles.size,
      (ba0_new_function *) & bap_new_polynom_mint_hp);
  for (i = 0; i < nulles.size; i++)
    {
      bap_set_polynom_variable_mint_hp (T->tab[T->size], nulles.tab[i], 1);
      T->size += 1;
    }

  ba0_restore (&M);
}

#undef BAD_FLAG_mint_hp
