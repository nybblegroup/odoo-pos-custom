/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    /**
     * Override editPartner to add validation for Argentine tax requirements.
     *
     * Validates that registered taxpayers (Responsable Inscripto) have:
     * - A CUIT (VAT number)
     * - CUIT as their identification type
     */
    async editPartner(partner) {
        const result = await super.editPartner(...arguments);

        if (result && result.l10n_ar_afip_responsibility_type_id) {
            // Check if it's a registered taxpayer (Responsable Inscripto - ID 1)
            const isResponsableInscripto = result.l10n_ar_afip_responsibility_type_id.id === 1;

            if (isResponsableInscripto) {
                // Validate VAT is present
                if (!result.vat) {
                    this.notification.add(
                        _t("Warning: Registered taxpayers must have a CUIT (VAT number)"),
                        { type: "warning" }
                    );
                }

                // Validate identification type is CUIT (usually id 4)
                if (result.l10n_latam_identification_type_id) {
                    const identTypeId = result.l10n_latam_identification_type_id.id;
                    if (identTypeId && identTypeId !== 4) {
                        this.notification.add(
                            _t("Warning: Registered taxpayers should have CUIT as identification type"),
                            { type: "warning" }
                        );
                    }
                }
            }
        }

        return result;
    },
});
