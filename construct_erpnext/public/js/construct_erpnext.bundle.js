// Construct ERPNext - Main bundle
// This file is loaded on every page.

window.construct_erpnext_report_badge = function(value) {
	if (value === undefined || value === null || value === "") {
		return value;
	}

	const label = __(String(value));
	const normalized = String(value).toLowerCase();
	const green = ["normal", "on track", "profitable", "paid", "fully invoiced", "available", "certified", "fully consumed"];
	const orange = ["watch", "partially invoiced", "partially certified", "partially paid", "reserved", "due", "near limit", "committed", "requested", "ordered", "received", "invoiced", "partially consumed", "partially measured"];
	const red = ["at risk", "overrun", "loss risk", "overdue", "outstanding high", "cash deficit", "red"];
	const gray = ["draft", "not started", "cancelled", "deferred", "closed", "archived", "invoice created", "open"];

	let color = "blue";
	if (green.includes(normalized)) color = "green";
	if (orange.includes(normalized)) color = "orange";
	if (red.includes(normalized)) color = "red";
	if (gray.includes(normalized)) color = "gray";

	return `<span class="indicator-pill ${color}">${label}</span>`;
};
