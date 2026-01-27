{
    "name": "Nybble AFIP Connection Check",
    "summary": "Pre-validate AFIP connection before issuing electronic invoices",
    "version": "18.0.1.0.0",
    "description": """
AFIP Connection Pre-Check
==========================

This module prevents POS freezing when AFIP web services are down.

Features:
---------
* Pre-validates AFIP connectivity before issuing electronic invoices
* Shows user-friendly error message when AFIP is unreachable
* Suggests creating ticket without electronic invoice as fallback
* Prevents long timeouts and improves cashier experience

Technical:
----------
* Extends account.move._l10n_ar_do_afip_ws_request_cae()
* Tests connectivity using _l10n_ar_get_afip_last_invoice_number()
* Raises ValidationError with actionable message if AFIP is down
    """,
    "author": "Nybble Group",
    "company": "Nybble Group",
    "website": "https://www.nybble.com.co",
    "category": "Accounting/Localizations",
    "depends": ["point_of_sale", "l10n_ar_edi"],
    "license": "LGPL-3",
    "data": [],
    "installable": True,
    "auto_install": False,
    "application": False,
}
