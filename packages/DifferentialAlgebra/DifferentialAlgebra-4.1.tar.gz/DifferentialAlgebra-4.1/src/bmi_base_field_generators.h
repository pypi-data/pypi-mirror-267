#ifndef BMI_BASE_FIELD_GENERATORS_H
#   define BMI_BASE_FIELD_GENERATORS_H 1

#   include <blad.h>
#   include "bmi_callback.h"

BEGIN_C_DECLS

extern ALGEB bmi_base_field_generators (
    struct bmi_callback *);

extern void bmi_forbid_base_field_implicit_generators (
    struct bad_base_field *,
    struct bav_tableof_variable *,
    struct bad_regchain *);

extern void bmi_scanf_generators (
    struct bav_tableof_variable *,
    char *);

END_C_DECLS
#endif /*! BMI_BASE_FIELD_GENERATORS_H */
