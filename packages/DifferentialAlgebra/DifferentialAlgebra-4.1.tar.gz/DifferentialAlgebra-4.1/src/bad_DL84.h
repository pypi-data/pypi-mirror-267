#if ! defined (BAD_DL84_H)
#   define BAD_DL84_H

#   include "bad_regchain.h"

BEGIN_C_DECLS

extern BAD_DLL void bad_positive_integer_roots_polynom_mod_regchain (
    struct ba0_tableof_mpz *,
    struct bap_polynom_mpz *,
    struct bav_variable *,
    struct bad_regchain *);

extern BAD_DLL void bad_parameters_of_polynom_mod_regchain (
    struct bav_tableof_variable *,
    struct baz_ratfrac *,
    struct bav_variable *,
    struct bad_regchain *);

extern BAD_DLL void bad_separant_valuation_mod_regchain_ratfrac (
    struct baz_ratfrac *,
    bav_Idegree *,
    struct baz_ratfrac *,
    struct bad_regchain *,
    struct baz_point_ratfrac *,
    struct bav_tableof_variable *);

extern BAD_DLL void bad_Hurwitz_coeffs_ratfrac (
    struct baz_tableof_ratfrac *,
    struct baz_ratfrac *,
    ba0_int_p,
    struct bav_symbol *,
    struct bav_tableof_variable *);

extern BAD_DLL void bad_DL_prolongation_prerequisites_mod_regchain (
    struct baz_ratfrac *,
    ba0_int_p *,
    ba0_int_p *,
    struct baz_ratfrac *,
    struct baz_ratfrac *,
    struct bav_symbol *,
    struct bav_variable *,
    struct bad_regchain *,
    struct baz_point_ratfrac *,
    struct bav_tableof_variable *);

extern BAD_DLL void bad_DL_prolongated_system_mod_regchain (
    struct baz_tableof_ratfrac *,
    struct bad_regchain *,
    struct baz_point_ratfrac *,
    struct bav_symbol *,
    struct bav_tableof_variable *);

END_C_DECLS
#endif /* !BAD_DL84_H */
