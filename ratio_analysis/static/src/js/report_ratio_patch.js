/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ReportLineRenderer } from "@account_reports/components/report/report_line_renderer";

patch(ReportLineRenderer.prototype, "ratio_analysis_report_ratio_patch", {
    _renderCell({ column, line }) {
        const el = this._super({ column, line });

        try {
            if (line.code === "CURRENT_RATIO" && column.expression_label === "balance") {
                const text = el.textContent?.trim();
                if (text && !text.includes(": 1")) {
                    el.textContent = `${text} : 1`;
                }
            }
        } catch (e) {
            console.warn("Ratio patch error", e);
        }

        return el;
    },
});
