/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AccountReportLine } from "@account_reports/components/account_report/line/line";
console.log("logger details:::::>>>")

patch(AccountReportLine.prototype, {
    _renderCell(col, index) {
        const el = this._super(col, index);

        try {
            if (
                this.props.line.code === "CURRENT_RATIO" &&
                col &&
                col.no_format !== undefined
            ) {
                if (!el.dataset || !el.dataset.ratioPatched) {
                    el.textContent = `${col.no_format} : 1`; // use raw value, not re-read text
                    el.dataset.ratioPatched = "true";
                }
            }
        } catch (e) {
            console.warn("Ratio patch error", e);
        }

        return el;
    },
});