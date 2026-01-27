"""Account move extension for AFIP connection pre-check."""

import logging

from odoo import _, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    """Extend account.move to pre-validate AFIP connectivity before invoicing."""

    _inherit = "account.move"

    def _l10n_ar_do_afip_ws_request_cae(self, client, auth, transport):
        """
        Override to pre-check AFIP connectivity before requesting CAE.

        This prevents POS freezing when AFIP webservices are down by validating
        connectivity first and showing a user-friendly error message.

        Parameters
        ----------
        client : zeep.Client
            SOAP client for AFIP webservice
        auth : dict
            Authentication credentials
        transport : zeep.transports.Transport
            Transport layer for SOAP requests

        Returns
        -------
        dict
            AFIP response with CAE and validation data

        Raises
        ------
        ValidationError
            If AFIP webservice is unreachable or down

        """
        check_result = self._check_afip_connectivity()

        if check_result is True:
            _logger.info("AFIP connectivity verified successfully")
            return super()._l10n_ar_do_afip_ws_request_cae(client, auth, transport)

        # AFIP is down or unreachable
        error_message = self._build_afip_error_message(check_result)
        _logger.error("AFIP connectivity check failed: %s", error_message)
        raise ValidationError(error_message)

    def _check_afip_connectivity(self):
        """
        Pre-validate AFIP connectivity by querying last invoice number.

        Returns
        -------
        bool or Exception
            True if AFIP is reachable, Exception object if connectivity fails

        """
        # Only check for invoices that use AFIP webservices
        afip_moves = self.filtered(lambda x: x.journal_id.l10n_ar_afip_ws)

        if not afip_moves:
            return True

        move = afip_moves[0]
        journal = move.journal_id

        try:
            last_number = journal._l10n_ar_get_afip_last_invoice_number(
                move.l10n_latam_document_type_id
            )

            if last_number is not False:
                _logger.info(
                    "AFIP connection OK - Last invoice number: %s (Journal: %s, "
                    "Document Type: %s)",
                    last_number,
                    journal.name,
                    move.l10n_latam_document_type_id.name,
                )
                return True

            _logger.warning(
                "AFIP returned no last invoice number (Journal: %s, Document Type: %s)",
                journal.name,
                move.l10n_latam_document_type_id.name,
            )
            return False

        except Exception as error:
            _logger.error(
                "AFIP connectivity check failed with exception: %s (Journal: %s)",
                str(error),
                journal.name,
                exc_info=True,
            )
            return error

    def _build_afip_error_message(self, check_result):
        """
        Build user-friendly error message when AFIP is unreachable.

        Parameters
        ----------
        check_result : bool, Exception, or None
            Result from connectivity check

        Returns
        -------
        str
            Translated error message for the user

        """
        base_message = _(
            "AFIP web services are currently unavailable.\n\n"
            "Please create the ticket without electronic invoice by removing "
            "the green invoice button located at the bottom right of the "
            "payment menu."
        )

        if isinstance(check_result, Exception):
            error_name = getattr(check_result, "name", None) or str(check_result)
            if error_name and error_name.strip():
                base_message += _("\n\nTechnical details:\n%s") % error_name

        return base_message
