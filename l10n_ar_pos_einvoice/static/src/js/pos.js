/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {
    // Enable automatic invoice download if configured
    shouldDownloadInvoice() {
        const config = this.pos && this.pos.config ? this.pos.config : undefined;
        if (config && config.print_pdf_invoice) {
            return true;
        }
        return super.shouldDownloadInvoice ? super.shouldDownloadInvoice() : false;
    },

    // Method to handle AFIP button click
    clickAfipInvoice() {
        const order = this.currentOrder;

        if (!order) {
            this.notification.add(
                _t("No active order"),
                { type: "warning" }
            );
            return;
        }

        if (!order.is_to_invoice()) {
            this.notification.add(
                _t("This order is not marked for invoicing"),
                { type: "warning" }
            );
            return;
        }

        // If the order already has an associated invoice, try to download it
        if (order.account_move) {
            const url = `/web/content/account.move/${order.account_move}/invoice_pdf`;
            window.open(url, '_blank');
            this.notification.add(
                _t("Downloading AFIP Invoice"),
                { type: "success" }
            );
        } else {
            this.notification.add(
                _t("The AFIP invoice will be generated upon payment validation"),
                { type: "info" }
            );
        }
    },
});
