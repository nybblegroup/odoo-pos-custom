# -*- coding: utf-8 -*-
"""Extend l10n_ar.afip.responsibility.type to load in POS."""

from odoo import api, models


class L10nArAfipResponsibilityType(models.Model):
    """Extend AFIP responsibility type model to be available in POS."""

    _name = "l10n_ar.afip.responsibility.type"
    _inherit = ["l10n_ar.afip.responsibility.type", "pos.load.mixin"]

    @api.model
    def _load_pos_data_domain(self, data):
        """Load all AFIP responsibility types for POS.

        Returns:
            list: Domain to filter records. Empty list means load all.
        """
        return []

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Define fields to load in POS.

        Args:
            config_id: The POS configuration record ID.

        Returns:
            list: List of field names to load.
        """
        return ["id", "name"]
