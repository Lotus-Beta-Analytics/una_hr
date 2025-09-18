/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ReportRenderer } from "@account_reports/components/report/report_renderer";

patch(ReportRenderer.prototype, "ratio_analysis_report_ratio_patch", {
    /**
     * Extend cell rendering to append " : 1" for the Current Ratio line.
     */
    _renderLine(line) {
        const el = this._super(line);

        try {
            // Match by line code (make sure your XML line has code="CURRENT_RATIO")
            if (line.code === "CURRENT_RATIO") {
                const numberCells = el.querySelectorAll("td.number");
                numberCells.forEach((cell) => {
                    if (!cell.dataset.ratioPatched) {
                        cell.textContent = `${cell.textContent} : 1`;
                        cell.dataset.ratioPatched = "true";
                    }
                });
            }
        } catch (e) {
            console.warn("Ratio patch error", e);
        }

        return el;
    },
});
