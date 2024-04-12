#if ! defined (BAZ_EVAL_POLYSPEC_MPZ_H)
#   define BAZ_EVAL_POLYSPEC_MPZ_H 1

#   include "baz_common.h"
#   include "baz_point_ratfrac.h"

BEGIN_C_DECLS

extern BAZ_DLL void baz_eval_to_interval_at_point_interval_mpq_polynom_mpz (
    struct ba0_interval_mpq *,
    struct bap_polynom_mpz *,
    struct bav_point_interval_mpq *);

extern BAZ_DLL void baz_eval_to_ratfrac_at_point_ratfrac_polynom_mpz (
    struct baz_ratfrac *,
    struct bap_polynom_mpz *,
    struct baz_point_ratfrac *);

extern BAZ_DLL void baz_evaluate_to_ratfrac_at_point_ratfrac_polynom_mpz (
    struct baz_ratfrac *,
    struct bap_polynom_mpz *,
    struct baz_point_ratfrac *,
    struct bav_tableof_variable *);

extern BAZ_DLL void baz_twice_evaluate_to_ratfrac_at_point_ratfrac_polynom_mpz (
    struct baz_ratfrac *,
    struct bap_polynom_mpz *,
    struct baz_point_ratfrac *,
    struct baz_point_ratfrac *,
    struct bav_tableof_variable *);

END_C_DECLS
#endif /* !BAZ_EVAL_POLYSPEC_MPZ_H */
