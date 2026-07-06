import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Ensure Python can resolve system paths natively under Windows environments
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import run_agent_query

app = FastAPI(title="Pavan-Putra Invoice Generator Workspace")

class ChatQuery(BaseModel):
    message: str

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pavan-Putra Invoice Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }
        .invoice-paper { background-color: #ffffff; color: #1e293b; padding: 2rem; min-height: 11in; border-radius: 8px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }
        
        /* Persistent Scroll Constraints for Workspace Layout */
        .scrollable-panel { max-height: calc(100vh - 60px); overflow-y: auto; }
        
        @media print {
            body * { visibility: hidden; }
            #invoicePaperContainer, #invoicePaperContainer * { visibility: visible; }
            #invoicePaperContainer { position: absolute; left: 0; top: 0; width: 100%; margin: 0; padding: 0; box-shadow: none; }
            .invoice-paper { box-shadow: none; border: none; padding: 0; min-height: 100vh; }
            html, body { margin: 0; padding: 0; background: #fff; }
        }
    </style>
</head>
<body class="p-4 sm:p-6">

    <div class="max-w-[1600px] mx-auto">
        <div class="flex flex-col lg:flex-row gap-6">
            
            <div class="lg:w-1/2 flex flex-col gap-6 scrollable-panel">
                
                <div class="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl">
                    <h1 class="text-2xl font-bold text-sky-400 mb-2">🔱 Pavan-Putra Invoice Generator</h1>
                    <p class="text-xs text-gray-400 mb-6">Universal Proforma Processing Module • Built with Multi-Tool Architecture</p>
                    
                    <form id="invoiceForm" class="space-y-6">
                        <div class="p-4 bg-sky-950/40 rounded-lg border border-sky-800/50 flex flex-col gap-3">
                            <h3 class="text-sm font-semibold text-sky-300">Import Line Items from Sheet</h3>
                            <div class="flex items-center gap-3">
                                <label for="excel-file-upload" class="cursor-pointer bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold py-2 px-4 rounded transition-colors">
                                    Choose File (.xlsx, .xls, .csv)
                                </label>
                                <input type="file" id="excel-file-upload" accept=".xlsx, .xls, .csv" class="hidden">
                                <span id="file-name" class="text-xs text-gray-400 italic">No file mounted</span>
                            </div>
                        </div>

                        <div>
                            <h3 class="text-sm font-semibold text-gray-300 border-b border-gray-800 pb-2 mb-3">Merchant / Origin Details</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                                <div class="md:col-span-2"><label class="block text-gray-400 mb-1">Company Name</label><input type="text" id="yourName" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div class="md:col-span-2"><label class="block text-gray-400 mb-1">Street Address</label><input type="text" id="yourAddress" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">City</label><input type="text" id="yourCity" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Country</label><input type="text" id="yourCountry" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Phone Contact</label><input type="text" id="yourPhone" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Email Endpoint</label><input type="email" id="yourEmail" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                            </div>
                        </div>

                        <div>
                            <h3 class="text-sm font-semibold text-gray-300 border-b border-gray-800 pb-2 mb-3">Consignee / Client Details</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                                <div class="md:col-span-2"><label class="block text-gray-400 mb-1">Client Name</label><input type="text" id="clientName" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div class="md:col-span-2"><label class="block text-gray-400 mb-1">Delivery Address</label><input type="text" id="clientAddress" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">City</label><input type="text" id="clientCity" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Country</label><input type="text" id="clientCountry" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                            </div>
                        </div>

                        <div>
                            <h3 class="text-sm font-semibold text-gray-300 border-b border-gray-800 pb-2 mb-3">Logistics & Transaction Metadata</h3>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                                <div><label class="block text-gray-400 mb-1">Invoice String</label><input type="text" id="invoiceNumber" value="To be numbered" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Execution Date</label><input type="date" id="dateIssued" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Shipping Terms</label><input type="text" id="shippingTerms" value="FOB Port" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Freight Mode</label><input type="text" id="freightType" value="Sea Freight" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Exchange Conversion Factor</label><input type="number" id="exchangeRate" value="1.00" step="0.0001" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Target Disembarkation</label><input type="text" id="destination" class="w-full bg-gray-950 border border-gray-800 rounded p-2 text-white"></div>
                            </div>
                        </div>

                        <div>
                            <h3 class="text-sm font-semibold text-amber-400 border-b border-gray-800 pb-2 mb-3">Auxiliary Logistics Surcharges (Base Currency)</h3>
                            <div class="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
                                <div><label class="block text-gray-400 mb-1">Docs</label><input type="number" id="documentationCharge" value="0.00" step="0.01" class="w-full bg-gray-950 border border-gray-800 rounded p-1 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Packing</label><input type="number" id="packingCharge" value="0.00" step="0.01" class="w-full bg-gray-950 border border-gray-800 rounded p-1 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Transit</label><input type="number" id="transportationCharge" value="0.00" step="0.01" class="w-full bg-gray-950 border border-gray-800 rounded p-1 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Clearing</label><input type="number" id="clearingCharge" value="0.00" step="0.01" class="w-full bg-gray-950 border border-gray-800 rounded p-1 text-white"></div>
                                <div><label class="block text-gray-400 mb-1">Freight</label><input type="number" id="freightCharge" value="0.00" step="0.01" class="w-full bg-gray-950 border border-gray-800 rounded p-1 text-white"></div>
                            </div>
                        </div>

                        <div>
                            <h3 class="text-sm font-semibold text-gray-300 mb-2">Itemized Cargo Specifications</h3>
                            <div id="itemsContainer" class="space-y-2"></div>
                            <button type="button" id="addItemButton" class="w-full mt-2 bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 py-2 rounded transition-colors">+ Append Cargo Entry</button>
                        </div>
                    </form>
                </div>

                <div class="bg-gray-900 p-4 rounded-xl border border-gray-800 flex flex-col gap-3 shadow-xl">
                    <h3 class="text-xs font-bold uppercase tracking-wider text-sky-400">⚡ GlobalInvoice AI Copilot Loop</h3>
                    <div id="chat-pane" class="h-[200px] overflow-y-auto bg-gray-950 rounded-lg p-3 border border-gray-800 text-xs space-y-3">
                        <div class="text-slate-400"><b>System Loop Online.</b> Ready for financial context orchestration. Ask me to query conversion metrics or document variables.</div>
                    </div>
                    <div class="flex gap-2">
                        <input type="text" id="user-msg" placeholder="Ask AI copilot to compute currency arrays or audit numbers..." onkeypress="checkKey(event)" class="flex-1 bg-gray-950 border border-gray-800 rounded p-3 text-xs text-white focus:outline-none focus:border-sky-500">
                        <button onclick="sendQuery()" class="bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs px-6 rounded transition-colors">Query</button>
                    </div>
                </div>
            </div>

            <div class="lg:w-1/2 scrollable-panel">
                <div class="bg-gray-900 p-3 rounded-t-xl border-t border-x border-gray-800 flex justify-between items-center">
                    <span class="text-xs font-semibold text-gray-400">Print Canvas Preview Terminal</span>
                    <div class="flex gap-2">
                        <button id="printButton" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs py-1.5 px-4 rounded border border-slate-700 transition-colors">System Print</button>
                        <button id="copyButton" class="bg-sky-600 hover:bg-sky-500 text-white text-xs py-1.5 px-4 rounded transition-colors">Copy Plain Text</button>
                    </div>
                </div>
                
                <div id="invoicePaperContainer">
                    <div class="invoice-paper" id="invoicePreview">
                        </div>
                </div>
            </div>

        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const itemsContainer = document.getElementById('itemsContainer');
            const addItemButton = document.getElementById('addItemButton');
            const invoicePreview = document.getElementById('invoicePreview');
            const excelFileInput = document.getElementById('excel-file-upload');
            const fileNameDisplay = document.getElementById('file-name');

            document.getElementById('dateIssued').value = new Date().toISOString().split('T')[0];
            let rowIndexCounter = 0;

            function createCargoRow(desc='', qty=1, uom='Nos', price='', disc='', marg='') {
                const id = rowIndexCounter++;
                const div = document.createElement('div');
                div.className = "grid grid-cols-1 md:grid-cols-12 gap-2 bg-gray-950 p-2 rounded border border-gray-800 text-xs items-end";
                div.innerHTML = `
                    <div class="md:col-span-4"><label class="text-[10px] text-gray-500">Description</label><input type="text" name="itemDescription" value="${desc}" class="w-full bg-gray-900 border border-gray-800 rounded p-1 text-white"></div>
                    <div class="md:col-span-1"><label class="text-[10px] text-gray-500">Qty</label><input type="number" name="itemQuantity" value="${qty}" class="w-full bg-gray-900 border border-gray-800 rounded p-1 text-white text-center"></div>
                    <div class="md:col-span-1"><label class="text-[10px] text-gray-500">UOM</label><input type="text" name="itemUOM" value="${uom}" class="w-full bg-gray-900 border border-gray-800 rounded p-1 text-white text-center"></div>
                    <div class="md:col-span-2"><label class="text-[10px] text-gray-500">Base Rate</label><input type="number" name="itemUnitPrice" value="${price}" step="0.01" class="w-full bg-gray-900 border border-gray-800 rounded p-1 text-white text-right"></div>
                    <div class="md:col-span-1"><label class="text-[10px] text-gray-500">Disc%</label><input type="number" name="itemDiscount" value="${disc}" step="0.1" class="w-full bg-gray-900 border border-gray-800 rounded p-1 text-white text-center"></div>
                    <div class="md:col-span-1"><label class="text-[10px] text-gray-500">Marg%</label><input type="number" name="itemMargin" value="${marg}" step="0.1" class="w-full bg-gray-900 border border-gray-800 rounded p-1 text-white text-center"></div>
                    <button type="button" class="md:col-span-2 text-rose-500 hover:text-rose-400 pb-1 h-full font-bold text-center remove-row-btn">Delete</button>
                `;
                itemsContainer.appendChild(div);
                div.querySelector('.remove-row-btn').addEventListener('click', () => { div.remove(); calculateEngineTotals(); });
                div.querySelectorAll('input').forEach(i => i.addEventListener('input', calculateEngineTotals));
            }

            addItemButton.addEventListener('click', () => createCargoRow());

            excelFileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (!file) return;
                fileNameDisplay.textContent = file.name;

                const reader = new FileReader();
                reader.onload = (evt) => {
                    const data = new Uint8Array(evt.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const sheet = workbook.Sheets[workbook.SheetNames[0]];
                    const jsonRows = XLSX.utils.sheet_to_json(sheet, { header: 1 });

                    itemsContainer.innerHTML = '';
                    rowIndexCounter = 0;

                    let headerIndex = jsonRows.findIndex(r => r.includes('Sl. No.') || r.includes('Item'));
                    if(headerIndex === -1) headerIndex = 0;

                    const headers = jsonRows[headerIndex];
                    const contentRows = jsonRows.slice(headerIndex + 1);

                    contentRows.forEach(row => {
                        if(!row.length || row.every(c => !c)) return;
                        const obj = {};
                        headers.forEach((h, idx) => { obj[h] = row[idx]; });

                        const desc = obj['Item'] || obj['Description'] || '';
                        const qty = obj['Qty.'] || obj['Qty'] || 1;
                        const uom = obj['UOM'] || 'Nos';
                        const rate = obj['Unit rate'] || obj['Price'] || '';
                        
                        if(desc) createCargoRow(desc, qty, uom, rate, '', '');
                    });
                    calculateEngineTotals();
                };
                reader.readAsArrayBuffer(file);
            });

            function calculateEngineTotals() {
                const exchange = parseFloat(document.getElementById('exchangeRate').value) || 1.0;
                
                const docs = parseFloat(document.getElementById('documentationCharge').value) || 0;
                const pack = parseFloat(document.getElementById('packingCharge').value) || 0;
                const trans = parseFloat(document.getElementById('transportationCharge').value) || 0;
                const clear = parseFloat(document.getElementById('clearingCharge').value) || 0;
                const freight = parseFloat(document.getElementById('freightCharge').value) || 0;

                const packingAndTransitBase = docs + pack + trans;
                
                let subtotalConverted = 0;
                let tableRowsHtml = '';

                const descriptions = document.querySelectorAll('input[name="itemDescription"]');
                const quantities = document.querySelectorAll('input[name="itemQuantity"]');
                const uoms = document.querySelectorAll('input[name="itemUOM"]');
                const prices = document.querySelectorAll('input[name="itemUnitPrice"]');
                const discounts = document.querySelectorAll('input[name="itemDiscount"]');
                const margins = document.querySelectorAll('input[name="itemMargin"]');

                descriptions.forEach((d, i) => {
                    const desc = d.value;
                    const qty = parseInt(quantities[i].value) || 0;
                    const uom = uoms[i].value || 'Nos';
                    const baseRate = parseFloat(prices[i].value) || 0;
                    const disc = parseFloat(discounts[i].value) || 0;
                    const marg = parseFloat(margins[i].value) || 0;

                    if (desc) {
                        const discounted = baseRate * qty * (1 - (disc / 100));
                        const calculatedLineValueBase = discounted + (discounted * (marg / 100));
                        
                        const calculatedLineValueTarget = calculatedLineValueBase / exchange;
                        const finalUnitRateTarget = qty > 0 ? (calculatedLineValueTarget / qty) : 0;

                        subtotalConverted += calculatedLineValueTarget;

                        tableRowsHtml += `
                            <tr class="text-xs border-b border-gray-200">
                                <td class="p-2 text-left font-medium text-gray-800">${desc}</td>
                                <td class="p-2 text-center text-gray-600">${qty}</td>
                                <td class="p-2 text-center text-gray-600">${uom}</td>
                                <td class="p-2 text-right font-mono text-gray-700">${finalUnitRateTarget.toFixed(2)}</td>
                                <td class="p-2 text-right font-mono font-semibold text-gray-900">${calculatedLineValueTarget.toFixed(2)}</td>
                            </tr>
                        `;
                    }
                });

                const packTransitTarget = packingAndTransitBase / exchange;
                const clearTarget = clear / exchange;
                const freightTarget = freight / exchange;

                const trackingExWorksTotal = subtotalConverted + packTransitTarget;
                const trackingFobTotal = trackingExWorksTotal + clearTarget;
                const trackingCnfTotal = trackingFobTotal + freightTarget;

                invoicePreview.innerHTML = `
                    <div class="text-center mb-6">
                        <h2 class="text-2xl font-bold tracking-tight text-gray-900 uppercase">PROFORMA INVOICE</h2>
                        <div class="w-32 h-1 bg-sky-500 mx-auto mt-1"></div>
                    </div>

                    <div class="grid grid-cols-2 gap-6 text-xs mb-6 border-b border-gray-200 pb-6">
                        <div>
                            <h4 class="font-bold text-gray-400 uppercase tracking-wider mb-1">Exporter / Vendor:</h4>
                            <p class="font-bold text-gray-900 text-sm">${document.getElementById('yourName').value || '---'}</p>
                            <p class="text-gray-600">${document.getElementById('yourAddress').value || ''}</p>
                            <p class="text-gray-600">${document.getElementById('yourCity').value || ''} ${document.getElementById('yourCountry').value || ''}</p>
                            <p class="text-gray-500 mt-1">Contact: ${document.getElementById('yourPhone').value || '---'} | Email: ${document.getElementById('yourEmail').value || '---'}</p>
                        </div>
                        <div class="text-right">
                            <h4 class="font-bold text-gray-400 uppercase tracking-wider mb-1">Consigned To:</h4>
                            <p class="font-bold text-gray-900 text-sm">${document.getElementById('clientName').value || '---'}</p>
                            <p class="text-gray-600">${document.getElementById('clientAddress').value || ''}</p>
                            <p class="text-gray-600">${document.getElementById('clientCity').value || ''} ${document.getElementById('clientCountry').value || ''}</p>
                        </div>
                    </div>

                    <div class="grid grid-cols-3 gap-2 bg-gray-50 p-3 rounded text-[11px] text-gray-600 mb-6 border border-gray-200">
                        <div><strong>Invoice Ref:</strong> ${document.getElementById('invoiceNumber').value}</div>
                        <div><strong>Issuance Date:</strong> ${document.getElementById('dateIssued').value}</div>
                        <div><strong>Incoterms Vector:</strong> ${document.getElementById('shippingTerms').value}</div>
                        <div><strong>Logistics Layer:</strong> ${document.getElementById('freightType').value}</div>
                        <div><strong>Disembarkation Port:</strong> ${document.getElementById('destination').value}</div>
                        <div><strong>Index Multiplier:</strong> 1.00 Base = ${exchange.toFixed(4)} Converted</div>
                    </div>

                    <table class="w-full mb-6">
                        <thead>
                            <tr class="bg-gray-100 border-b border-gray-300 text-[11px] uppercase text-gray-600 font-semibold">
                                <th class="p-2 text-left">Description Specification</th>
                                <th class="p-2 text-center w-12">Qty</th>
                                <th class="p-2 text-center w-16">UOM</th>
                                <th class="p-2 text-right w-28">Unit Value</th>
                                <th class="p-2 text-right w-28">Gross Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tableRowsHtml || '<tr><td colspan="5" class="p-4 text-center text-gray-400 italic">No cargo definitions loaded.</td></tr>'}
                        </tbody>
                    </table>

                    <div class="grid grid-cols-12 gap-4 text-xs">
                        <div class="col-span-6">
                            <h5 class="font-bold text-gray-800 uppercase tracking-wider mb-1 border-b border-gray-200 pb-1">Declarations & Boilerplate</h5>
                            <ul class="space-y-1 text-[11px] text-gray-500 list-disc list-inside">
                                <li>All calculations are certified accurate as processed.</li>
                                <li>Settlement coordinates to be arranged post-approval.</li>
                                <li>Country of Origin: Global Commercial Network Ecosystem.</li>
                            </ul>
                        </div>
                        <div class="col-span-6 font-mono text-right text-gray-700 space-y-1.5">
                            <div class="flex justify-between border-b border-gray-100 pb-1"><span>Cargo Subtotal:</span><span class="font-bold text-gray-900">${subtotalConverted.toFixed(2)}</span></div>
                            <div class="flex justify-between border-b border-gray-100 pb-1"><span>Est. Packing/Transit Surcharge:</span><span>${packTransitTarget.toFixed(2)}</span></div>
                            <div class="flex justify-between border-b border-gray-200 pb-1 text-gray-900 font-semibold"><span>Ex-Works Consolidated Total:</span><span>${trackingExWorksTotal.toFixed(2)}</span></div>
                            <div class="flex justify-between border-b border-gray-100 pb-1"><span>Est. Customs Portal Clearing:</span><span>${clearTarget.toFixed(2)}</span></div>
                            <div class="flex justify-between border-b border-gray-200 pb-1 text-gray-900 font-semibold"><span>FOB Portal Total:</span><span>${trackingFobTotal.toFixed(2)}</span></div>
                            <div class="flex justify-between border-b border-gray-100 pb-1"><span>Est. Freight Transit Matrix:</span><span>${freightTarget.toFixed(2)}</span></div>
                            <div class="flex justify-between text-sm font-bold text-sky-700 border-t border-double border-gray-400 pt-1"><span>C&F Consolidated Balance:</span><span>${trackingCnfTotal.toFixed(2)}</span></div>
                        </div>
                    </div>
                `;
            }

            // Universal binding array to force synchronization on data entry changes
            const bindingSelectors = ['yourName','yourAddress','yourCity','yourCountry','yourPhone','yourEmail',
                                      'clientName','clientAddress','clientCity','clientCountry','invoiceNumber',
                                      'dateIssued','shippingTerms','freightType','exchangeRate','destination',
                                      'documentationCharge','packingCharge','transportationCharge','clearingCharge','freightCharge'];
            
            bindingSelectors.forEach(id => {
                document.getElementById(id).addEventListener('input', calculateEngineTotals);
            });

            document.getElementById('printButton').addEventListener('click', () => window.print());
            document.getElementById('copyButton').addEventListener('click', () => {
                const text = invoicePreview.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    alert('Plaintext canvas summary mirrored to local OS clipboards!');
                });
            });

            // Seed initial structural row context
            createCargoRow('', 1, 'Nos', '', '', '');
            calculateEngineTotals();
        });

        // ── Copilot Event Intercept Pipeline ──
        // ── Copilot Event Intercept Pipeline ──
// ── Copilot Event Intercept Pipeline ──
        async function sendQuery() {
            const box = document.getElementById('user-msg');
            const text = box.value.trim();
            if(!text) return;

            addBubble(text, 'user');
            box.value = '';

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await res.json();
                
                try {
                    // 🛠️ CRITICAL CLEANUP STEP: Strip out any markdown blocks (```json) or wrapping spaces
                    let cleanResponse = data.response.trim();
                    if (cleanResponse.startsWith("```")) {
                        cleanResponse = cleanResponse.replace(/^```json/i, "").replace(/^```/, "").replace(/```$/, "").trim();
                    }
                    
                    const invoiceData = JSON.parse(cleanResponse);
                    
                    // Map core fields into the DOM input elements automatically
                    if(invoiceData.clientName) document.getElementById('clientName').value = invoiceData.clientName;
                    if(invoiceData.clientAddress) document.getElementById('clientAddress').value = invoiceData.clientAddress;
                    if(invoiceData.clientCity) document.getElementById('clientCity').value = invoiceData.clientCity;
                    if(invoiceData.clientCountry) document.getElementById('clientCountry').value = invoiceData.clientCountry;
                    if(invoiceData.shippingTerms) document.getElementById('shippingTerms').value = invoiceData.shippingTerms;
                    if(invoiceData.destination) document.getElementById('destination').value = invoiceData.destination;
                    if(invoiceData.exchangeRate) document.getElementById('exchangeRate').value = invoiceData.exchangeRate;
                    
                    // Reset and populate item specification rows dynamically
                    if(invoiceData.items && invoiceData.items.length > 0) {
                        const itemsContainer = document.getElementById('itemsContainer');
                        itemsContainer.innerHTML = ''; // Clear default blank row
                        
                        invoiceData.items.forEach(item => {
                            createCargoRow(
                                item.description || '',
                                item.quantity || 1,
                                'Nos',
                                item.unitPrice || '',
                                item.discount || '0',
                                item.margin || '0'
                            );
                        });
                    }
                    
                    // Fire the mathematical orchestration layer to refresh totals on the fly
                    calculateEngineTotals();
                    addBubble("🔱 Canvas data fields successfully orchestrated!", 'agent');
                    
                } catch (parseError) {
                    // Fallback if the string couldn't be parsed as JSON, print the raw message to debug
                    console.error("JSON Parsing failed: ", parseError);
                    addBubble(data.response, 'agent');
                }
            } catch (networkError) {
                addBubble('⚠️ Exception linked to current runtime network thread.', 'agent');
            }
        }

        function addBubble(t, c) {
            const pane = document.getElementById('chat-pane');
            const d = document.createElement('div');
            d.className = `p-2 rounded text-xs ${c === 'user' ? 'bg-sky-950/40 border border-sky-800 text-sky-200 ml-4' : 'bg-slate-900 border border-slate-800 text-slate-300 mr-4'}`;
            d.innerHTML = t.replace(/\\n/g, '<br>');
            pane.appendChild(d);
            pane.scrollTop = pane.scrollHeight;
        }
        function checkKey(e) { if(e.key === 'Enter') sendQuery(); }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return HTML_TEMPLATE

@app.post("/chat")
async def chat(query: ChatQuery):
    response = run_agent_query(query.message)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
    