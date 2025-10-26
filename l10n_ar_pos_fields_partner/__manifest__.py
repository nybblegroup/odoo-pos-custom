{
    "name": "POS Fields Partner",
    "version": "18.0.0.2",
    "author": "Ing. Gabriela Rivero",
    "license": "LGPL-3",
    "category": "Point Of Sale",
    "website": "www.galup.com.ar",
    "description": """
This module adds AFIP Responsibility, document type and document number fields to the POS customer view.

Features:
- Displays l10n_ar_afip_responsibility_type_id (AFIP Responsibility Type) in partner list
- Displays l10n_latam_identification_type_id (Identification Type) in partner list
- Displays VAT/ID Number in partner list
- Works in both desktop and mobile views
- Loads related models (identification types and responsibility types) in POS
- Validates that registered taxpayers have proper CUIT configuration
    """,
    "depends": ["point_of_sale", "l10n_ar", "l10n_latam_base"],
    "assets": {
        "point_of_sale._assets_pos": [
            "l10n_ar_pos_fields_partner/static/src/js/pos.js",
            "l10n_ar_pos_fields_partner/static/src/xml/pos.xml",
        ],
    },
    "installable": True,
}
