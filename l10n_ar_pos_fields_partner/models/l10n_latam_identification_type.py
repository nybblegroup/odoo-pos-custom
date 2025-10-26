# -*- coding: utf-8 -*-
"""Extend l10n_latam.identification.type to load in POS."""

from odoo import api, models


class L10nLatamIdentificationType(models.Model):
    """Extend identification type model to be available in POS."""

    _name = "l10n_latam.identification.type"
    _inherit = ["l10n_latam.identification.type", "pos.load.mixin"]

    @api.model
    def _load_pos_data_domain(self, data):
        """Load all identification types for POS.

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
