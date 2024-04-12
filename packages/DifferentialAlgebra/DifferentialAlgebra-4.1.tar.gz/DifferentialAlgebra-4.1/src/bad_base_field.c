#include "bad_base_field.h"
#include "bad_reduction.h"

/*
 * texinfo: bad_init_base_field
 * Initialize the base field @var{K} to the field of the rational
 * fractions in the independent variables. 
 */

BAD_DLL void
bad_init_base_field (
    struct bad_base_field *K)
{
  bool differential = bav_global.R.ders.size > 0;
  bad_init_regchain (&K->relations);
  bad_set_base_field_relations_properties (&K->relations, differential);
  K->varmax = BAV_NOT_A_VARIABLE;
  K->assume_reduced = false;
}

/*
 * texinfo: bad_new_base_field
 * Allocate a base field, initialize it and return it.
 */

BAD_DLL struct bad_base_field *
bad_new_base_field (
    void)
{
  struct bad_base_field *K;

  K = (struct bad_base_field *) ba0_alloc (sizeof (struct bad_base_field));
  bad_init_base_field (K);
  return K;
}

/*
 * texinfo: bad_set_base_field
 * Assign @var{L} to @var{K}.
 */

BAD_DLL void
bad_set_base_field (
    struct bad_base_field *K,
    struct bad_base_field *L)
{
  K->varmax = L->varmax;
  bad_set_regchain (&K->relations, &L->relations);
  K->assume_reduced = L->assume_reduced;
}

/*
 * texinfo: bad_base_field_generators
 * In the differential case, store in @var{G} all the dependent variables 
 * of order zero which are considered as lying in the base field i.e.
 * all the dependent variables which are lower than the @code{varmax} field
 * of @var{K} or which lie in the same block as @code{varmax}. 
 * In the non differential case, store in @var{G} all the dependent variables 
 * of any order which are considered as lying in the base field, i.e. all the
 * dependent variables which are lower than or equal to @code{varmax}.
 */

BAD_DLL void
bad_base_field_generators (
    struct bav_tableof_variable *G,
    struct bad_base_field *K)
{
  struct bav_variable *v;
  bav_Inumber blk, blk_v;
  ba0_int_p i;
  bool differential;

  ba0_reset_table ((struct ba0_table *) G);
  if (K->varmax == BAV_NOT_A_VARIABLE)
    return;
  blk = bav_R_symbol_block_number (K->varmax->root, (ba0_int_p *) 0);
  ba0_realloc_table ((struct ba0_table *) G, bav_global.R.vars.size);

  differential = bad_defines_a_differential_ideal_regchain (&K->relations);

  if (differential)
/*
 * The computation below is redundant w.r.t. bad_move_base_field_generator
 * since K->varmax is the highest variable of its block.
 */
    {
      for (i = 0; i < bav_global.R.deps.size; i++)
        {
          v = bav_global.R.vars.tab[bav_global.R.deps.tab[i]];
          blk_v = bav_R_symbol_block_number (v->root, (ba0_int_p *) 0);
/*
 * The higher the block number, the lower the block
 */
          if (blk_v >= blk)
            {
              G->tab[G->size] = v;
              G->size += 1;
            }
        }
    }
  else
    {
      for (i = 0; i < bav_global.R.vars.size; i++)
        {
          v = bav_global.R.vars.tab[i];
          if (bav_symbol_type_variable (v) == bav_dependent_symbol
              && (K->varmax == v || bav_gt_variable (K->varmax, v)))
            {
              G->tab[G->size] = v;
              G->size += 1;
            }
        }
    }
}

/*
 * texinfo: bad_move_base_field_generator
 * In the non differential case, let @var{w} be equal to @var{v}.
 * In the differential case, let @var{w} be the highest, order zero, dependent
 * variable belonging to the block of @var{v}.
 * Assign @var{w} to the @var{varmax} field of @var{K} if this variable is 
 * greater than @code{varmax}.
 */

BAD_DLL void
bad_move_base_field_generator (
    struct bad_base_field *K,
    struct bav_variable *v)
{
  struct bav_variable *w;
  bav_Inumber blk_v, blk_w;
  ba0_int_p i;
  bool differential;

  if (bav_symbol_type_variable (v) != bav_dependent_symbol)
    BA0_RAISE_EXCEPTION (BAD_ERRIND);
/*
 * In the differential case, v = the highest dependent variable of its block
 */
  differential = bad_defines_a_differential_ideal_regchain (&K->relations);
  if (differential)
    {
      v = bav_order_zero_variable (v);
      blk_v = bav_R_symbol_block_number (v->root, (ba0_int_p *) 0);
      for (i = 0; i < bav_global.R.deps.size; i++)
        {
          w = bav_global.R.vars.tab[bav_global.R.deps.tab[i]];
          blk_w = bav_R_symbol_block_number (w->root, (ba0_int_p *) 0);
          if (bav_gt_variable (w, v) && blk_v == blk_w)
            {
              v = w;
              blk_v = blk_w;
            }
        }
    }
  if (K->varmax == BAV_NOT_A_VARIABLE || bav_gt_variable (v, K->varmax))
    K->varmax = v;
}

static void
bad_move_base_field_relations_generators (
    struct bad_base_field *K,
    struct bad_regchain *A)
{
  struct bav_term *T;
  struct bav_variable *v;
  ba0_int_p i, j;

  for (i = 0; i < A->decision_system.size; i++)
    {
      T = &A->decision_system.tab[i]->total_rank;
      for (j = 0; j < T->size; j++)
        {
          v = T->rg[j].var;
          if (bav_symbol_type_variable (v) == bav_dependent_symbol)
            bad_move_base_field_generator (K, v);
        }
    }
}

/*
 * Assigns to K the base field defined by generators and relations.
 *
 * If P is nonzero then, the zero derivatives of the parameters of
 * P are appended to the relations.
 *
 * generators and P may be zero.
 */

static void
bad_set_base_field_generators_and_relations_with_all_parameters (
    struct bad_base_field *K,
    struct bav_tableof_variable *generators,
    struct bad_regchain *relations,
    struct bav_tableof_parameter *P,
    bool pretend)
{
  struct bap_tableof_polynom_mpz *eqns;
  struct ba0_tableof_string prop;
  struct ba0_mark M;
  ba0_int_p i;
/*
 * First move all necessary generators to K
 */
  if (generators)
    for (i = 0; i < generators->size; i++)
      bad_move_base_field_generator (K, generators->tab[i]);

  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * The properties are those of relations
 */
  ba0_init_table ((struct ba0_table *) &prop);
  bad_properties_attchain (&prop, &relations->attrib);
  eqns = &relations->decision_system;

  ba0_pull_stack ();

  bad_set_and_extend_regchain_tableof_polynom_mpz (&K->relations, eqns, P,
      &prop, true, pretend);
  bad_move_base_field_relations_generators (K, &K->relations);

  ba0_restore (&M);
}

/*
 * Assigns to K the base field defined by generators and relations.
 *
 * If P is nonzero then, the zero derivatives of the parameters of
 * P, which also occur in generators and relations are appended to 
 * the relations.
 *
 * generators and P may be zero.
 */

static void
bad_set_base_field_generators_and_relations_with_necessary_parameters (
    struct bad_base_field *K,
    struct bav_tableof_variable *generators,
    struct bad_regchain *relations,
    struct bav_tableof_parameter *P,
    bool pretend)
{
  struct bad_attchain attrib;
  struct bap_tableof_polynom_mpz *eqns;
  struct bav_tableof_variable gens;
  struct bav_tableof_parameter pars;
  struct ba0_tableof_string prop;
  struct ba0_mark M;
  ba0_int_p i, k;
  bool differential;
/*
 * First move all necessary generators to K
 */
  if (generators)
    for (i = 0; i < generators->size; i++)
      bad_move_base_field_generator (K, generators->tab[i]);

  if (relations)
    bad_move_base_field_relations_generators (K, relations);

  ba0_push_another_stack ();
  ba0_record (&M);

  ba0_init_table ((struct ba0_table *) &pars);

  differential = bad_defines_a_differential_ideal_regchain (&K->relations);

  if (differential && P != (struct bav_tableof_parameter *) 0)
    {
      ba0_init_table ((struct ba0_table *) &gens);
      bad_base_field_generators (&gens, K);
      ba0_realloc_table ((struct ba0_table *) &pars, gens.size);

      for (i = 0; i < gens.size; i++)
        {
          if (bav_is_a_parameter (gens.tab[i]->root, &k, P))
            {
              pars.tab[pars.size] = P->tab[k];
              pars.size += 1;
            }
        }
    }
/*
 * The properties are those of relations
 */
  ba0_init_table ((struct ba0_table *) &prop);
  bad_properties_attchain (&prop, &relations->attrib);
  eqns = &relations->decision_system;

  ba0_pull_stack ();

  bad_set_and_extend_regchain_tableof_polynom_mpz (&K->relations, eqns, &pars,
      &prop, true, pretend);

  ba0_restore (&M);
}

/*
 * texinfo: bad_set_base_field_generators_and_relations
 * Assign to @var{K} the base field defined by @var{generators}, @var{P} and
 * @var{relations}.
 * 
 * If @var{allpars} is true, then all the elements of @var{P} are moved 
 * to the base field. Otherwise, only the elements of @var{P} which occur
 * in @var{generators} and @var{relations} are moved to the base field.
 *
 * For each parameter which is moved to the base field,
 * some equations @math{p = 0}, stating that some derivatives of this
 * parameter are zero, are appended to @var{relations}.
 * To keep @var{relations} differentially triangular, no equation
 * @math{p = 0} such that @math{p} is the derivative of some other
 * element of @var{relations} is inserted in this chain.
 *
 * If @var{pretend} is @code{false} then some
 * checking is performed to ensure the consistency of the relations.
 *
 * The arguments @var{generators} and @var{P} may be zero.
 */

BAD_DLL void
bad_set_base_field_generators_and_relations (
    struct bad_base_field *K,
    struct bav_tableof_variable *generators,
    struct bad_regchain *relations,
    struct bav_tableof_parameter *P,
    bool allpars,
    bool pretend)
{
  if (allpars)
    bad_set_base_field_generators_and_relations_with_all_parameters (K,
        generators, relations, P, pretend);
  else
    bad_set_base_field_generators_and_relations_with_necessary_parameters (K,
        generators, relations, P, pretend);
}

/*
 * texinfo: bad_base_field_implicit_generators
 * Assign to @var{S} the generators of @var{K} 
 * (see @code{bad_base_field_generators}) which are present @var{generators}
 * and not present in @var{relations}.
 */

BAD_DLL void
bad_base_field_implicit_generators (
    struct bav_tableof_variable *S,
    struct bad_base_field *K,
    struct bav_tableof_variable *generators,
    struct bad_regchain *relations)
{
  struct bap_polynom_mpz *A;
  struct bav_tableof_variable gens, X;
  struct bav_variable *v;
  ba0_int_p i, j;
  struct ba0_mark M;
  bool differential;

  ba0_push_another_stack ();
  ba0_record (&M);
/*
 * gens = the actual generators of K
 */
  ba0_init_table ((struct ba0_table *) &gens);
  bad_base_field_generators (&gens, K);
/*
 * X = the generators actually present in generators and relations
 *
 * The only difference between the differential and the algebraic
 * case is that one must take the order-zero variable in the 
 * differential case.
 */
  ba0_init_table ((struct ba0_table *) &X);
  ba0_realloc_table ((struct ba0_table *) &X, bav_global.R.vars.size);

  differential = bad_defines_a_differential_ideal_regchain (&K->relations);

  if (generators)
    {
      for (i = 0; i < generators->size; i++)
        {
          v = generators->tab[i];
          if (bav_symbol_type_variable (v) == bav_dependent_symbol)
            {
              if (differential)
                v = bav_order_zero_variable (v);
              if (!ba0_member_table (v, (struct ba0_table *) &X))
                {
                  X.tab[X.size] = v;
                  X.size += 1;
                }
            }
        }
    }
  if (relations)
    {
      for (i = 0; i < relations->decision_system.size; i++)
        {
          A = relations->decision_system.tab[i];
          for (j = 0; j < A->total_rank.size; j++)
            {
              v = A->total_rank.rg[j].var;
              if (bav_symbol_type_variable (v) == bav_dependent_symbol)
                {
                  if (differential)
                    v = bav_order_zero_variable (v);
                  if (!ba0_member_table (v, (struct ba0_table *) &X))
                    {
                      X.tab[X.size] = v;
                      X.size += 1;
                    }
                }
            }
        }
    }
/*
 * S = gens \ X
 */
  i = 0;
  while (i < gens.size)
    {
      if (ba0_member_table (gens.tab[i], (struct ba0_table *) &X))
        ba0_delete_table ((struct ba0_table *) &gens, i);
      else
        i += 1;
    }

  ba0_push_another_stack ();
  ba0_set_table ((struct ba0_table *) S, (struct ba0_table *) &gens);
  ba0_restore (&M);
}

/*
 * texinfo: bad_is_a_compatible_base_field
 * Return @code{true} if the relations of @var{K} can be included in a
 * regular chain having properties @var{attrib}. 
 * See @code{bad_is_a_compatible_regchain}.
 */

BAD_DLL bool
bad_is_a_compatible_base_field (
    struct bad_base_field *K,
    struct bad_attchain *attrib)
{
  return bad_is_a_compatible_regchain (&K->relations, attrib);
}

/*
 * texinfo: bad_member_variable_base_field
 * Return @code{true} if @var{v} belongs to @var{K}, else @code{false}.
 */

BAD_DLL bool
bad_member_variable_base_field (
    struct bav_variable *v,
    struct bad_base_field *K)
{
  bool differential;

  if (bav_symbol_type_variable (v) == bav_independent_symbol)
    return true;
  else if (K->varmax == BAV_NOT_A_VARIABLE)
    return false;

  differential = bad_defines_a_differential_ideal_regchain (&K->relations);

  if (differential)
    v = bav_order_zero_variable (v);

  return v == K->varmax || bav_gt_variable (K->varmax, v);
}

/*
 * Return true if P, which is assumed to be reduced w.r.t. the relations,
 * lies in the base field. If P = 0 then false is returned.
 */

static bool
bad_member_reduced_nonzero_polynom_base_field (
    struct bap_polynom_mpz *P,
    struct bad_base_field *K)
{
  if (bap_is_numeric_polynom_mpz (P))
    return !bap_is_zero_polynom_mpz (P);
  else
    return bad_member_variable_base_field (bap_leader_polynom_mpz (P), K);
}

/*
 * texinfo: bad_member_nonzero_polynom_base_field
 * Return @code{true} if @var{P} is a nonzero element of @var{K}.
 * If the field @code{assume_reduced} of @var{K} is @code{true}, then the
 * polynomial @var{P} is supposed to be reduced w.r.t. the defining relations
 * of @var{K}, thereby speeding up the membership test.
 */

BAD_DLL bool
bad_member_nonzero_polynom_base_field (
    struct bap_polynom_mpz *P,
    struct bad_base_field *K)
{
  struct bap_product_mpz R;
  struct ba0_mark M;
  ba0_int_p i;
  bool b;
  bool differential;

  if (K->assume_reduced)
    return bad_member_reduced_nonzero_polynom_base_field (P, K);

  if (bap_is_independent_polynom_mpz (P, (struct bav_tableof_parameter *) 0))
    return !bap_is_zero_polynom_mpz (P);

  differential = bad_defines_a_differential_ideal_regchain (&K->relations);

  if (K->relations.decision_system.size == 0
      || !bad_is_a_reducible_polynom_by_regchain (P, &K->relations,
          differential ? bad_full_reduction : bad_algebraic_reduction,
          bad_all_derivatives_to_reduce, (struct bav_rank *) 0,
          (ba0_int_p *) 0))
    return bad_member_reduced_nonzero_polynom_base_field (P, K);

  ba0_record (&M);
  bap_init_product_mpz (&R);
  bad_reduce_polynom_by_regchain (&R, (struct bap_product_mpz *) 0, P,
      &K->relations,
      differential ? bad_full_reduction : bad_algebraic_reduction,
      bad_all_derivatives_to_reduce);
  b = !bap_is_zero_product_mpz (&R);
  for (i = 0; b && i < R.size; i++)
    b = bad_member_reduced_nonzero_polynom_base_field (&R.tab[i].factor, K);
  ba0_restore (&M);

  return b;
}

/*
 * texinfo: bad_member_polynom_base_field
 * Return @code{true} if @var{P} is an element (possibly zero) of @var{K}.
 */

BAD_DLL bool
bad_member_polynom_base_field (
    struct bap_polynom_mpz *P,
    struct bad_base_field *K)
{
  struct bap_product_mpz R;
  struct ba0_mark M;
  ba0_int_p i;
  bool b;
  bool differential;

  if (bap_is_independent_polynom_mpz (P, (struct bav_tableof_parameter *) 0))
    return true;

  if (bad_is_zero_regchain (&K->relations))
    return bad_member_reduced_nonzero_polynom_base_field (P, K);

  differential = bad_defines_a_differential_ideal_regchain (&K->relations);

  ba0_record (&M);
  bap_init_product_mpz (&R);
  bad_reduce_polynom_by_regchain (&R, (struct bap_product_mpz *) 0, P,
      &K->relations,
      differential ? bad_full_reduction : bad_algebraic_reduction,
      bad_all_derivatives_to_reduce);
  b = true;
  for (i = 0; b && i < R.size; i++)
    b = bad_member_reduced_nonzero_polynom_base_field (&R.tab[i].factor, K);
  ba0_restore (&M);

  return b;
}

/*
 * texinfo: bad_set_base_field_relations_properties
 * If @var{relations} is empty, set all
 * its properties (except the differential and the coherence ones
 * if @var{differential} is false).
 * If it is nonempty, set the prime 
 * ideal property then call @code{bad_set_automatic_properties_attchain}.
 * The parameter @var{relations} is supposed to provide the
 * @code{relations} field of a base field.
 */

BAD_DLL void
bad_set_base_field_relations_properties (
    struct bad_regchain * relations,
    bool differential)
{
  if (bad_is_zero_regchain (relations))
    {
      bad_set_property_regchain (relations, bad_prime_ideal_property);
      if (differential)
        {
          bad_set_property_regchain (relations, 
            bad_differential_ideal_property);
          bad_set_property_regchain (relations, bad_autoreduced_property);
          bad_set_property_regchain (relations, bad_primitive_property);
          bad_set_property_regchain (relations, bad_squarefree_property);
          bad_set_property_regchain (relations, bad_normalized_property);
          bad_set_property_regchain (relations, bad_coherence_property);
        }
      else
        {
          bad_clear_property_regchain (relations, 
            bad_differential_ideal_property);
          bad_set_property_regchain (relations, bad_autoreduced_property);
          bad_set_property_regchain (relations, bad_primitive_property);
          bad_set_property_regchain (relations, bad_squarefree_property);
          bad_set_property_regchain (relations, bad_normalized_property);
          bad_clear_property_regchain (relations, bad_coherence_property);
        }
    }
  else
    {
      bad_set_property_regchain (relations, bad_prime_ideal_property);
      bad_set_automatic_properties_attchain (&relations->attrib);
    }
}

/*
 * field ( [ differential = boolean, ] 
 *         [ generators = %t[%v], ] 
 *         [ relations = %regchain ] )
 */

/*
 * texinfo: bad_scanf_base_field
 * A parsing function for base fields.
 * It is called by @code{ba0_scanf/%base_field}.
 * The input string is expected to have the form:
 * @code{field ( [ differential = boolean ], [ generators = %t[%v] ], [ relations = %regchain ] )}.
 * The flag @code{differential} permits to force a base field
 * to be non differential.
 * Keywords @code{basefield} and @code{base_field} may be used
 * instead of @code{field}.
 * Exception @code{BAD_ERRBAS} may be raised.
 */

BAD_DLL void *
bad_scanf_base_field (
    void *AA)
{
  struct bad_base_field *K;
  bool differential_is_set, differential;
  struct bad_regchain relations;
  struct bav_tableof_variable generators;
  struct ba0_mark M;

  ba0_push_another_stack ();
  ba0_record (&M);

  if (ba0_type_token_analex () != ba0_string_token
      || (ba0_strcasecmp (ba0_value_token_analex (), "field") != 0
          && ba0_strcasecmp (ba0_value_token_analex (), "base_field") != 0
          && ba0_strcasecmp (ba0_value_token_analex (), "basefield") != 0))
    BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
  ba0_get_token_analex ();
  if (!ba0_sign_token_analex ("("))
    BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
  ba0_get_token_analex ();
/*
 * field ( 
 *              ^
 * differential_is_set = the differential flag is specified
 * differential        = the value of the differential flag (meaningful 
 *                       only if differential_is_set)
 */
  differential_is_set = false;
  if (ba0_type_token_analex () == ba0_string_token
      && ba0_strcasecmp (ba0_value_token_analex (), "differential") == 0)
    {
      differential_is_set = true;

      ba0_get_token_analex ();
      if (!ba0_sign_token_analex ("="))
        BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
      ba0_get_token_analex ();
      if (ba0_type_token_analex () != ba0_string_token)
        BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
      if (ba0_strcasecmp (ba0_value_token_analex (), "true") == 0)
        {
          if (bav_global.R.ders.size == 0)
            BA0_RAISE_EXCEPTION (BAD_ERRBFD);
          differential = true;
        }
      else if (ba0_strcasecmp (ba0_value_token_analex (), "false") == 0)
        differential = false;
      else
        BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
      ba0_get_token_analex ();
      if (ba0_sign_token_analex (","))
        {
          ba0_get_token_analex ();
          if (ba0_sign_token_analex (")"))
            BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
        }
    }
/*
 * generators = %t[%v] 
 */
  ba0_init_table ((struct ba0_table *) &generators);
  if (ba0_type_token_analex () == ba0_string_token
      && ba0_strcasecmp (ba0_value_token_analex (), "generators") == 0)
    {
      ba0_scanf ("generators = %t[%v]", &generators);
      ba0_get_token_analex ();
      if (ba0_sign_token_analex (","))
        {
          ba0_get_token_analex ();
          if (ba0_sign_token_analex (")"))
            BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
        }
    }

  bad_init_regchain (&relations);
  if (ba0_type_token_analex () == ba0_string_token
      && ba0_strcasecmp (ba0_value_token_analex (), "relations") == 0)
    {
      ba0_scanf ("relations = %pretend_regchain", &relations);
      ba0_get_token_analex ();
    }

  if (!ba0_sign_token_analex (")"))
    BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
/*
 * If a non empty regular chain is specified, 
 * - check consistency with (differential_is_set, differential)
 * - take its properties
 *
 * Otherwise, 
 * - use (differential_is_set, differential) if any
 * - set all properties to true
 */
  if (!bad_is_zero_regchain (&relations))
    {
      if (differential_is_set)
        if (differential != bad_has_property_regchain (&relations, 
            bad_differential_ideal_property))
          BA0_RAISE_PARSER_EXCEPTION (BAD_ERRBAS);
    }

  if (!differential_is_set)
    differential = bav_global.R.ders.size > 0;

  bad_set_base_field_relations_properties (&relations, differential);

  ba0_pull_stack ();
  if (AA == (void *) 0)
    K = bad_new_base_field ();
  else
    K = (struct bad_base_field *) AA;

  bad_set_base_field_generators_and_relations (K, &generators, &relations,
      &bav_global.parameters, false, false);

  ba0_restore (&M);
  return K;
}

/*
 * texinfo: bad_printf_base_field
 * A printing function for base fields.
 * It is called by @code{ba0_printf/%base_field}.
 */

BAD_DLL void
bad_printf_base_field (
    void *AA)
{
  struct bad_base_field *K = (struct bad_base_field *) AA;
  struct bav_tableof_variable generators;
  struct ba0_mark M;
  bool differential;

  ba0_record (&M);
  ba0_init_table ((struct ba0_table *) &generators);
  bad_base_field_generators (&generators, K);

  differential = bad_defines_a_differential_ideal_regchain (&K->relations);

  if (!bad_is_zero_regchain (&K->relations))
    ba0_printf
        ("field (differential = %s, generators = %t[%v], relations = %regchain)",
        differential ? "true" : "false", &generators, &K->relations);
  else
    ba0_printf ("field (differential = %s, generators = %t[%v])",
        differential ? "true" : "false", &generators);

  ba0_restore (&M);
}
