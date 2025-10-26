{
    "name": "POS einvoice AR",
    "version": "18.0.0.1",
    "author": "Eng. Gabriela Rivero",
    "license": "LGPL-3",
    "category": "Point Of Sale",
    "website": "www.galup.com.ar",
    "description": "This module optionally allows printing the invoice from the POS.",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_config.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "l10n_ar_pos_einvoice/static/src/js/pos.js",
            "l10n_ar_pos_einvoice/static/src/xml/afip_invoice_button.xml",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
