# Nybble AFIP Connection Check

## Overview

This module prevents Point of Sale (POS) freezing when AFIP (Administración Federal de Ingresos Públicos) web services are down or unreachable.

## Problem Statement

In Argentina, electronic invoices must be validated by AFIP through web services. When AFIP servers are down:

- **Without this module:** The POS hangs waiting for AFIP response (up to 60 seconds timeout)
- **With this module:** Pre-validates connectivity and immediately shows a user-friendly error message

## Features

- ✅ Pre-checks AFIP connectivity before issuing electronic invoices
- ✅ Shows actionable error message when AFIP is unreachable
- ✅ Suggests creating ticket without electronic invoice as fallback
- ✅ Prevents cashier frustration from long timeouts
- ✅ Proper logging for troubleshooting

## Technical Details

### How It Works

1. Intercepts `account.move._l10n_ar_do_afip_ws_request_cae()`
2. Calls `journal._l10n_ar_get_afip_last_invoice_number()` to test connectivity
3. If AFIP responds → Proceeds with normal CAE request
4. If AFIP is down → Raises `ValidationError` with user-friendly message

### Dependencies

- `point_of_sale`
- `l10n_ar_edi` (Odoo Enterprise)

## Installation

1. Copy module to `addons` directory
2. Update apps list
3. Install "Nybble AFIP Connection Check"

## Configuration

No configuration needed. Works automatically for all Argentine electronic invoices.

## Usage

The module works transparently in the background. When AFIP is down, users will see:

```
AFIP web services are currently unavailable.

Please create the ticket without electronic invoice by removing
the green invoice button located at the bottom right of the
payment menu.

Technical details:
[Exception details if available]
```

## Changelog

### Version 18.0.1.0.0 (2026-01-27)

- ✨ Initial migration from Odoo 13 to Odoo 18
- ♻️ Refactored code with English naming conventions
- 🌐 Added proper translation support with `_()`
- 📝 Improved logging and error messages
- 🐛 Better exception handling
- 🗑️ Removed debug `print()` statements

## Authors

**Nybble Group**

- Original author: Mauricio Ramirez
- Migration to v18: Nybble Development Team

## License

LGPL-3

## Support

For support, please contact Nybble Group at https://www.nybble.com.co
