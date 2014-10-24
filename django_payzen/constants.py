VADS_ACTION_MODE_CHOICES = (
    ('INTERACTIVE', 'INTERACTIVE'),
    ('SILENT', 'SILENT'),
)

VADS_CURRENCY_CHOICES = (
    ('036', 'Australian dollar'),
    ('124', 'Canadian dollar'),
    ('156', 'Chinese Yuan'),
    ('208', 'Danish Krone'),
    ('392', 'Japanese Yen'),
    ('578', 'Norwegian Krone'),
    ('752', 'Swedish Krona'),
    ('756', 'Swiss franc'),
    ('826', 'Pound sterling'),
    ('840', 'American dollar'),
    ('953', 'Franc Pacifique (CFP)'),
    ('978', 'Euro')
)

VADS_CTX_MODE_CHOICES = (
    ('TEST', 'TEST'),
    ('PRODUCTION', 'PRODUCTION')
)

VADS_RETURN_MODE_CHOICES = (
    ('AMEX', 'American Express'),
    ('AURORE-MULTI', 'AURORE (multi brand)'),
    ('BUYSTER', 'BUYSTER'),
    ('CB', 'CB'),
    ('COFINOGA', 'COFINOGA'),
    ('E-CARTEBLEUE', 'e blue card'),
    ('MASTERCARD', 'Eurocard / MasterCard'),
    ('JCB', 'JCB'),
    ('MAESTRO', 'Maestro'),
    ('ONEY', 'ONEY'),
    ('ONEY_SANDBOX', 'ONEY SANDBOX mode'),
    ('PAYPAL', 'PAYPAL'),
    ('PAYPAL_SB', 'PAYPAL SANDBOX mode'),
    ('PAYSAFECARD', 'PAYSAFECARD'),
    ('VISA', 'Visa'),
    ('VISA_ELECTRON', 'Visa Electron'),
    ('COF3XCB', '3x CB Cofinoga'),
    ('COF3XCB_SB', '3x CB Cofinoga SANDBOX'),
)

VADS_VALIDATION_MODE_CHOICES = (
    ('', 'Default shop configuration (using payzen admin)'),
    ('0', 'Automatic validation'),
    ('1', 'Manual validation')
)

VADS_TRANS_STATUS = (
    ('ABANDONED', 'ABANDONED'),
    ('AUTHORISED', 'AUTHORISED'),
    ('REFUSED', 'REFUSED'),
    ('AUTHORISED_TO_VALIDATE', 'AUTHORISED_TO_VALIDATE'),
    ('WAITING_AUTHORISATION', 'WAITING_AUTHORISATION'),
    ('EXPIRED', 'EXPIRED'),
    ('CANCELLED', 'CANCELLED'),
    ('WAITING_AUTHORISATION_TO_VALIDATE', 'WAITING_AUTHORISATION_TO_VALIDATE'),
    ('CAPTURED', 'CAPTURED'),
)

VADS_OPERATION_TYPE_CHOICES = (
    ('DEBIT', 'DEBIT'),
    ('CREDIT', 'CREDIT')
)

VADS_RESULT_CHOICES = (
    ('00', 'Payment successful'),
    ('02', 'Merchant should contact his bank'),
    ('05', 'Payment refused'),
    ('17', 'Payment cancelled by client'),
    ('30', 'Wrong request format'),
    ('96', 'Technical error during payment process')
)

VADS_AUTH_MODE_CHOICES = (
    ('FULL', 'FULL'),
    ('MARK', 'MARK')
)

VADS_THREEDS_ENROLLED = (
    ('Y', 'Y'),
    ('N', 'N'),
    ('U', 'U')
)

VADS_THREEDS_CAVVALGORITHM_CHOICES = (
    ('0', 'HMAC'),
    ('1', 'CVV'),
    ('2', 'CVV_ATN'),
    ('3', 'Mastercard SPA')
)

VADS_THREEDS_STATUS_CHOICES = (
    ('Y', 'U'),
    ('N', 'N'),
    ('U', 'U'),
    ('A', 'A')
)

VADS_URL_CHECK_SRC_CHOICES = (
    ('PAY', 'PAY'),
    ('BO', 'BO'),
    ('BATCH', 'BATCH'),
    ('BATCH_AUTO', 'BATCH_AUTO'),
    ('FILE', 'FILE'),
    ('REC', 'REC'),
    ('MERCH_BO', 'MERCH_BO')
)

VADS_PAYMENT_SRC_CHOICES = (
    ('EC', 'EC'),
    ('MOTO', 'MOTO'),
    ('CC', 'CC'),
    ('OTHER', 'OTHER')
)
