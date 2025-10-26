# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import stdnum.ar
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Extend res.partner to add Argentinian localization fields to POS."""

    _inherit = "res.partner"

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Add Argentinian localization fields to POS partner data.

        This method extends the base POS partner fields loading to include
        AFIP responsibility type and identification type fields, making them
        available in the POS interface.

        Args:
            config_id: The POS configuration record.

        Returns:
            list: Extended list of field names to load in POS.
        """
        fields = super()._load_pos_data_fields(config_id)

        ar_fields = [
            "l10n_ar_afip_responsibility_type_id",
            "l10n_latam_identification_type_id",
        ]

        # Only add if not already present (avoid duplicates)
        for field in ar_fields:
            if field not in fields:
                fields.append(field)

        _logger.debug(
            "l10n_ar_pos_fields_partner: Loaded %d fields for res.partner in POS",
            len(fields),
        )

        return fields

    @api.constrains("vat", "l10n_latam_identification_type_id")
    def check_vat(self):
        """Validate Argentinian identification documents (CUIT, CUIL, DNI).

        This method extends the base VAT validation to handle Argentinian
        identification types. It validates documents specific to Argentina
        and delegates to the parent method for other cases.

        Note:
            This override was necessary to prevent type incoherence errors
            in POS when validating Argentinian documents.

        Returns:
            bool: True if validation passes.

        Raises:
            ValidationError: If the document format or content is invalid.
        """
        type_id = int(self.l10n_latam_identification_type_id.id)
        l10n_ar_partners = self.filtered(
            lambda self: self.env["l10n_latam.identification.type"]
            .browse(type_id)
            .l10n_ar_afip_code
        )
        l10n_ar_partners.l10n_ar_identification_validation()
        return super(ResPartner, self - l10n_ar_partners).check_vat()

    def _get_validation_module(self):
        """Get the appropriate validation module for the identification type.

        Returns the stdnum validation module based on the AFIP code of the
        identification type.

        Returns:
            module: stdnum.ar.cuit for CUIT (codes 80, 86),
                   stdnum.ar.dni for DNI (code 96),
                   None for other types.
        """
        self.ensure_one()
        type_id = int(self.l10n_latam_identification_type_id.id)
        l10n_latam_identification_type_id = self.env[
            "l10n_latam.identification.type"
        ].browse(type_id)
        if l10n_latam_identification_type_id.l10n_ar_afip_code in ["80", "86"]:
            return stdnum.ar.cuit
        elif l10n_latam_identification_type_id.l10n_ar_afip_code == "96":
            return stdnum.ar.dni

    def l10n_ar_identification_validation(self):
        """Validate Argentinian identification documents using stdnum library.

        Validates the VAT/identification number format and checksum according
        to Argentinian standards (CUIT, CUIL, or DNI).

        Raises:
            ValidationError: If the document has invalid checksum, length, or format.
        """
        type_id = int(self.l10n_latam_identification_type_id.id)
        l10n_latam_identification_type_id = self.env[
            "l10n_latam.identification.type"
        ].browse(type_id)
        for rec in self.filtered("vat"):
            try:
                module = rec._get_validation_module()
            except Exception as error:
                module = False
                _logger.warning(
                    "Argentinean document was not validated: %s", repr(error)
                )
            if not module:
                continue
            try:
                module.validate(rec.vat)

            except module.InvalidChecksum:
                raise ValidationError(
                    _(
                        'The validation digit is not valid for "%s"',
                        l10n_latam_identification_type_id.name,
                    )
                )
            except module.InvalidLength:
                raise ValidationError(
                    _('Invalid length for "%s"', l10n_latam_identification_type_id.name)
                )
            except module.InvalidFormat:
                raise ValidationError(
                    _(
                        'Only numbers allowed for "%s"',
                        l10n_latam_identification_type_id.name,
                    )
                )
            except Exception as error:
                raise ValidationError(repr(error))
