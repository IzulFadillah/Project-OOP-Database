import html
import os
import webbrowser
import customtkinter as ctk

from demo_program import PasienUmum, PasienBPJS, PasienAsuransi


def buat_nota_html(pasien):
    subtotal = pasien.get_biaya_tindakan() + pasien.get_biaya_obat()
    total_bayar = pasien.hitung_tagihan()
    potongan = subtotal - total_bayar
    id_pasien = html.escape(str(pasien.get_id_pasien()))
    nama_pasien = html.escape(str(pasien.get_nama()))

    if isinstance(pasien, PasienUmum):
        tipe_str = "Pasien Umum"
        ket_str = "Membayar 100% biaya tindakan & obat"
        diskon_str = "Rp 0"
    elif isinstance(pasien, PasienBPJS):
        tipe_str = "Pasien BPJS"
        ket_str = "Biaya obat dikover penuh oleh BPJS"
        diskon_str = f"Rp {pasien.get_biaya_obat():,.0f}"
    elif isinstance(pasien, PasienAsuransi):
        tipe_str = "Pasien Asuransi"
        ket_str = "Diskon Klaim Polis Asuransi"
        diskon_str = f"Rp {potongan:,.0f}"

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nota Pembayaran | Klinik Kelompok 7</title>
    <style>
        :root {{
            --ink: #17323b;
            --muted: #6f858b;
            --teal: #087f82;
            --mint: #69cfb1;
            --line: #e4eceb;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            min-height: 100vh;
            margin: 0;
            padding: 48px 20px;
            display: grid;
            place-items: center;
            color: var(--ink);
            background:
                radial-gradient(ellipse at 12% 12%, rgba(80, 190, 166, .16), transparent 34%),
                radial-gradient(ellipse at 88% 82%, rgba(242, 123, 98, .13), transparent 30%),
                #f3f7f7;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        }}
        .card {{
            position: relative;
            isolation: isolate;
            width: min(100%, 470px);
            overflow: hidden;
            padding: 34px;
            border: 1px solid rgba(255, 255, 255, .8);
            border-radius: 24px;
            background: rgba(255, 255, 255, .8);
            box-shadow: 0 24px 70px rgba(28, 73, 78, .13), 0 3px 12px rgba(28, 73, 78, .05);
            backdrop-filter: blur(18px);
        }}
        .card::before {{
            position: absolute;
            z-index: -1;
            top: -92px;
            right: -78px;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: rgba(105, 207, 177, .18);
            content: "";
            filter: blur(2px);
        }}
        .clinic-heading {{ display: flex; align-items: center; gap: 14px; margin-bottom: 28px; }}
        .clinic-mark {{
            flex: 0 0 52px;
            width: 52px;
            height: 52px;
            display: grid;
            place-items: center;
            border: 1px solid rgba(8, 127, 130, .12);
            border-radius: 17px;
            background: rgba(105, 207, 177, .2);
            color: var(--teal);
        }}
        .clinic-mark svg {{ width: 28px; height: 28px; }}
        .clinic-name {{ margin: 0; font-size: 19px; font-weight: 750; letter-spacing: -.5px; }}
        .clinic-address {{ margin: 5px 0 0; color: var(--muted); font-size: 12px; }}
        .receipt-title {{
            margin: 0;
            padding: 17px 18px;
            border: 1px solid rgba(8, 127, 130, .1);
            border-radius: 16px;
            background: linear-gradient(110deg, rgba(105, 207, 177, .2), rgba(255, 255, 255, .58) 78%);
        }}
        .receipt-title span {{ display: block; color: var(--teal); font-size: 10px; font-weight: 800; letter-spacing: 1.8px; }}
        .receipt-title strong {{ display: block; margin-top: 5px; font-size: 17px; letter-spacing: -.25px; }}
        .section-label {{
            margin: 25px 0 9px;
            color: var(--muted);
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.45px;
            text-transform: uppercase;
        }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        td {{ padding: 9px 0; vertical-align: top; }}
        td:first-child {{ color: var(--muted); }}
        td.right {{ padding-left: 12px; color: var(--ink); text-align: right; }}
        tr + tr td {{ border-top: 1px solid rgba(228, 236, 235, .75); }}
        .subtotal td {{ padding-top: 13px; color: var(--ink); font-weight: 700; }}
        .discount {{ color: #d45e4b !important; }}
        .total-box {{
            margin-top: 19px;
            padding: 17px 19px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            border: 1px solid rgba(8, 127, 130, .12);
            border-radius: 16px;
            background: rgba(8, 127, 130, .08);
        }}
        .total-box span {{ color: var(--teal); font-size: 14px; font-weight: 800; letter-spacing: 1.2px; }}
        .total-box strong {{ color: var(--teal); font-size: 19px; white-space: nowrap; }}
        .thank-you {{ margin: 22px 0 0; color: var(--muted); font-size: 12px; line-height: 1.6; text-align: center; }}
        .actions {{ display: flex; gap: 10px; margin-top: 22px; }}
        .actions button {{
            flex: 1;
            min-height: 46px;
            padding: 11px 14px;
            border: 1px solid transparent;
            border-radius: 13px;
            cursor: pointer;
            font: inherit;
            font-size: 13px;
            font-weight: 700;
        }}
        .print-button {{ background: var(--teal); box-shadow: 0 7px 16px rgba(8, 127, 130, .2); color: white; }}
        .download-button {{ border-color: rgba(8, 127, 130, .18) !important; background: rgba(255, 255, 255, .65); color: var(--teal); }}
        .download-status {{ min-height: 18px; margin: 9px 0 0; color: var(--muted); font-size: 11px; text-align: center; }}
        @media (max-width: 520px) {{
            body {{ padding: 24px 14px; }}
            .card {{ padding: 26px 22px; border-radius: 21px; }}
        }}
        @media print {{
            @page {{ margin: 12mm; }}
            body {{ min-height: auto; padding: 0; display: block; background: white; print-color-adjust: exact; -webkit-print-color-adjust: exact; }}
            .card {{ width: 100%; max-width: 470px; margin: 0 auto; border: 1px solid var(--line); box-shadow: none; backdrop-filter: none; }}
            .actions, .download-status {{ display: none; }}
        }}
    </style>
</head>
<body>
    <main class="card" id="receipt">
        <header class="clinic-heading">
            <div class="clinic-mark" aria-hidden="true">
                <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 5v7a6 6 0 0 0 12 0V5M8 5H6v3m14-3h2v3M14 18v1a7 7 0 0 0 14 0v-3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="26" cy="14" r="2" fill="currentColor"/>
                </svg>
            </div>
            <div>
                <h1 class="clinic-name">Klinik Kelompok 7</h1>
                <p class="clinic-address">Jl. Sipelem, Kampus UBSI Tegal</p>
            </div>
        </header>
        <h2 class="receipt-title">
            <span>BUKTI PEMBAYARAN</span>
            <strong>Terima kasih atas kepercayaan Anda</strong>
        </h2>
        <h3 class="section-label">Informasi pasien</h3>
        <table class="patient-table">
            <tbody>
                <tr><td>ID Pasien</td><td class="right">{id_pasien}</td></tr>
                <tr><td>Nama Pasien</td><td class="right">{nama_pasien}</td></tr>
                <tr><td>Kategori</td><td class="right">{html.escape(tipe_str)}</td></tr>
            </tbody>
        </table>
        <h3 class="section-label">Rincian pembayaran</h3>
        <table class="payment-table">
            <tbody>
                <tr><td>Biaya Tindakan Medis</td><td class="right">Rp {pasien.get_biaya_tindakan():,.0f}</td></tr>
                <tr><td>Biaya Obat-obatan</td><td class="right">Rp {pasien.get_biaya_obat():,.0f}</td></tr>
                <tr class="subtotal"><td>Subtotal</td><td class="right">Rp {subtotal:,.0f}</td></tr>
                <tr><td>{html.escape(ket_str)}</td><td class="right discount">- {diskon_str}</td></tr>
            </tbody>
        </table>
        <div class="total-box">
            <span>TOTAL BAYAR</span>
            <strong>Rp {total_bayar:,.0f}</strong>
        </div>
        <p class="thank-you">Semoga lekas sehat. Terima kasih telah berobat di Klinik Kelompok 7.</p>
        <div class="actions" aria-label="Aksi struk">
            <button class="print-button" type="button" onclick="window.print()">Cetak / Simpan PDF</button>
            <button class="download-button" type="button" onclick="downloadReceipt()">Unduh JPG</button>
        </div>
        <p class="download-status" role="status" aria-live="polite"></p>
    </main>
    <script>
        async function downloadReceipt() {{
            const status = document.querySelector(".download-status");
            let imageUrl;
            try {{
                const text = selector => document.querySelector(selector).textContent.trim();
                const patientRows = [...document.querySelectorAll(".patient-table tr")];
                const paymentRows = [...document.querySelectorAll(".payment-table tr")];
                const data = {{
                    clinic: text(".clinic-name"),
                    address: text(".clinic-address"),
                    title: text(".receipt-title span"),
                    subtitle: text(".receipt-title strong"),
                    patientHeading: "INFORMASI PASIEN",
                    patient: patientRows.map(row => [...row.cells].map(cell => cell.textContent.trim())),
                    paymentHeading: "RINCIAN PEMBAYARAN",
                    payment: paymentRows.map(row => [...row.cells].map(cell => cell.textContent.trim())),
                    totalLabel: text(".total-box span"),
                    total: text(".total-box strong"),
                    thankYou: text(".thank-you")
                }};
                const escapeXml = value => String(value).replace(/[&<>"']/g, char => ({{
                    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;"
                }})[char]);
                const line = (value, x, y, options = {{}}) =>
                    `<text x="${{x}}" y="${{y}}" fill="${{options.color || "#17323b"}}" font-family="Segoe UI, Arial, sans-serif" font-size="${{options.size || 13}}" font-weight="${{options.weight || 400}}" text-anchor="${{options.anchor || "start"}}" letter-spacing="${{options.spacing || 0}}">${{escapeXml(value)}}</text>`;
                const parts = [
                    '<svg xmlns="http://www.w3.org/2000/svg" width="940" height="1320" viewBox="0 0 470 660">',
                    '<defs><radialGradient id="glow"><stop stop-color="#69cfb1" stop-opacity=".24"/><stop offset="1" stop-color="#69cfb1" stop-opacity="0"/></radialGradient></defs>',
                    '<rect width="470" height="660" rx="24" fill="#ffffff"/>',
                    '<ellipse cx="420" cy="24" rx="130" ry="118" fill="url(#glow)"/>',
                    '<rect x="34" y="34" width="52" height="52" rx="17" fill="#e1f5ee" stroke="#d4ebe4"/>',
                    '<g transform="translate(46 46)" fill="none" stroke="#087f82" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 5v7a6 6 0 0 0 12 0V5M8 5H6v3m14-3h2v3M14 18v1a7 7 0 0 0 14 0v-3"/><circle cx="26" cy="14" r="2" fill="#087f82" stroke="none"/></g>',
                    line(data.clinic, 100, 57, {{ size: 19, weight: 750 }}),
                    line(data.address, 100, 77, {{ size: 12, color: "#6f858b" }}),
                    '<rect x="34" y="108" width="402" height="66" rx="16" fill="#eaf8f3" stroke="#e1efeb"/>',
                    line(data.title, 52, 134, {{ size: 10, weight: 800, color: "#087f82", spacing: 1.8 }}),
                    line(data.subtitle, 52, 158, {{ size: 16, weight: 700 }}),
                    line(data.patientHeading, 34, 207, {{ size: 10, weight: 800, color: "#6f858b", spacing: 1.4 }})
                ];
                let y = 235;
                for (const [label, value] of data.patient) {{
                    parts.push(line(label, 34, y, {{ color: "#6f858b" }}));
                    parts.push(line(value, 436, y, {{ anchor: "end" }}));
                    y += 34;
                }}
                y += 8;
                parts.push(line(data.paymentHeading, 34, y, {{ size: 10, weight: 800, color: "#6f858b", spacing: 1.4 }}));
                y += 28;
                for (const [index, [label, value]] of data.payment.entries()) {{
                    const isSubtotal = index === 2;
                    const isDiscount = index === 3;
                    parts.push(line(label, 34, y, {{ color: isSubtotal ? "#17323b" : "#6f858b", weight: isSubtotal ? 700 : 400, size: 12 }}));
                    parts.push(line(value, 436, y, {{ anchor: "end", color: isDiscount ? "#d45e4b" : "#17323b", weight: isSubtotal ? 700 : 400, size: 12 }}));
                    y += isSubtotal ? 38 : 32;
                }}
                y += 2;
                parts.push(`<rect x="34" y="${{y}}" width="402" height="58" rx="16" fill="#eaf5f3" stroke="#dcebe8"/>`);
                parts.push(line(data.totalLabel, 52, y + 35, {{ size: 14, weight: 800, color: "#087f82", spacing: 1.2 }}));
                parts.push(line(data.total, 418, y + 36, {{ size: 19, weight: 750, color: "#087f82", anchor: "end" }}));
                y += 91;
                parts.push(line(data.thankYou, 235, y, {{ size: 11, color: "#6f858b", anchor: "middle" }}));
                parts[0] = `<svg xmlns="http://www.w3.org/2000/svg" width="940" height="${{(y + 28) * 2}}" viewBox="0 0 470 ${{y + 28}}">`;
                parts.push("</svg>");

                const svgBlob = new Blob(parts, {{ type: "image/svg+xml;charset=utf-8" }});
                imageUrl = URL.createObjectURL(svgBlob);
                const image = new Image();
                image.src = imageUrl;
                await image.decode();

                const canvas = document.createElement("canvas");
                canvas.width = image.naturalWidth;
                canvas.height = image.naturalHeight;
                const context = canvas.getContext("2d");
                if (!context) throw new Error("Tidak dapat membuat gambar struk.");
                context.fillStyle = "#ffffff";
                context.fillRect(0, 0, canvas.width, canvas.height);
                context.drawImage(image, 0, 0);

                const jpg = await new Promise((resolve, reject) => {{
                    canvas.toBlob(file => file ? resolve(file) : reject(new Error("Gambar struk gagal dibuat.")), "image/jpeg", .95);
                }});
                const patientId = document.querySelector(".patient-table tr td.right").textContent.trim().replace(/[^a-zA-Z0-9_-]/g, "_");
                const link = document.createElement("a");
                link.href = URL.createObjectURL(jpg);
                link.download = `struk-klinik-${{patientId}}.jpg`;
                document.body.appendChild(link);
                link.click();
                link.remove();
                status.textContent = "Struk berhasil diunduh sebagai gambar JPG.";
                window.setTimeout(() => URL.revokeObjectURL(link.href), 1000);
            }} catch (error) {{
                console.error("Gagal mengunduh struk sebagai JPG.", error);
                status.textContent = "Gagal membuat gambar struk. Silakan coba tombol cetak.";
            }} finally {{
                if (imageUrl) URL.revokeObjectURL(imageUrl);
            }}
        }}
    </script>
</body>
</html>
"""
        
    filename = "nota_pembayaran.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    webbrowser.open("file://" + os.path.realpath(filename))


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppKlinik(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Tagihan Klinik (GUI Mode)")
        self.geometry("520x680")
        self.resizable(False, False)

        self.lbl_title = ctk.CTkLabel(self, text="Sistem Kasir & Tagihan Klinik", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.pack(pady=(20, 10))

        self.frame = ctk.CTkFrame(self, corner_radius=10)
        self.frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.entry_id = self._buat_input("ID Pasien:", "Contoh: P-001")
        self.entry_nama = self._buat_input("Nama Pasien:", "Masukkan nama pasien")
        self.entry_tindakan = self._buat_input("Biaya Tindakan Medis (Rp):", "0")
        self.entry_obat = self._buat_input("Biaya Obat-obatan (Rp):", "0")

        self.lbl_jenis = ctk.CTkLabel(self.frame, text="Jenis Kepesertaan Pasien:", font=ctk.CTkFont(weight="bold"))
        self.lbl_jenis.pack(anchor="w", padx=20, pady=(5, 2))
        
        self.combo_jenis = ctk.CTkOptionMenu(
            self.frame, 
            values=["Pasien Umum", "Pasien BPJS", "Pasien Asuransi"],
            command=self._on_jenis_change
        )
        self.combo_jenis.pack(padx=20, pady=(0, 10), fill="x")

        # Container khusus untuk input tambahan (BPJS / Asuransi)
        self.frame_extra = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.lbl_extra = ctk.CTkLabel(self.frame_extra, text="", font=ctk.CTkFont(weight="bold"))
        self.entry_extra = ctk.CTkEntry(self.frame_extra)

        # Container Tombol Aksi (Hitung & Reset)
        self.frame_btn = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.frame_btn.pack(padx=20, pady=(15, 10), fill="x")

        self.btn_hitung = ctk.CTkButton(
            self.frame_btn, 
            text="Hitung & Buka Nota", 
            command=self.proses_transaksi, 
            fg_color="#27ae60", 
            hover_color="#219150"
        )
        self.btn_hitung.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_reset = ctk.CTkButton(
            self.frame_btn, 
            text="Reset Form", 
            command=self.reset_form, 
            fg_color="#e74c3c", 
            hover_color="#c0392b"
        )
        self.btn_reset.pack(side="right", expand=True, fill="x", padx=(5, 0))

        self.lbl_hasil = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2ecc71")
        self.lbl_hasil.pack(pady=10)

        # Inisialisasi tampilan awal
        self._on_jenis_change("Pasien Umum")

    def _buat_input(self, label_text, placeholder):
        lbl = ctk.CTkLabel(self.frame, text=label_text, font=ctk.CTkFont(weight="bold"))
        lbl.pack(anchor="w", padx=20, pady=(5, 2))
        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder)
        entry.pack(padx=20, pady=(0, 5), fill="x")
        return entry

    def _on_jenis_change(self, choice):
        self.lbl_extra.pack_forget()
        self.entry_extra.pack_forget()
        self.entry_extra.delete(0, "end")

        if choice == "Pasien BPJS":
            self.frame_extra.pack(before=self.frame_btn, padx=20, pady=5, fill="x")
            self.lbl_extra.configure(text="Nomor Kartu BPJS:")
            self.entry_extra.configure(placeholder_text="Contoh: 000123456789")
            self.lbl_extra.pack(anchor="w", pady=(5, 2))
            self.entry_extra.pack(fill="x")
        elif choice == "Pasien Asuransi":
            self.frame_extra.pack(before=self.frame_btn, padx=20, pady=5, fill="x")
            self.lbl_extra.configure(text="No. Polis & Diskon (%):")
            self.entry_extra.configure(placeholder_text="Format: NO_POLIS,PERSEN (Misal: POL-999,25)")
            self.lbl_extra.pack(anchor="w", pady=(5, 2))
            self.entry_extra.pack(fill="x")
        else:
            # Sembunyikan frame ekstra secara total untuk Pasien Umum agar tidak mengganggu tata letak
            self.frame_extra.pack_forget()

    def reset_form(self):
        # Mengosongkan seluruh kotak input
        self.entry_id.delete(0, "end")
        self.entry_nama.delete(0, "end")
        self.entry_tindakan.delete(0, "end")
        self.entry_obat.delete(0, "end")
        self.entry_extra.delete(0, "end")

        # Mengembalikan pilihan ke Pasien Umum
        self.combo_jenis.set("Pasien Umum")
        self._on_jenis_change("Pasien Umum")

        # Mengosongkan status teks
        self.lbl_hasil.configure(text="")

        # Mengarahkan fokus kursor ke input pertama
        self.entry_id.focus()

    def proses_transaksi(self):
        try:
            id_p = self.entry_id.get().strip() or "P-001"
            nama = self.entry_nama.get().strip() or "Pasien Anonim"
            tindakan = float(self.entry_tindakan.get().strip() or 0)
            obat = float(self.entry_obat.get().strip() or 0)
            jenis = self.combo_jenis.get()

            obj_pasien = None

            if jenis == "Pasien Umum":
                obj_pasien = PasienUmum(id_p, nama, tindakan, obat)

            elif jenis == "Pasien BPJS":
                no_bpjs = self.entry_extra.get().strip() or "BPJS-DEFAULT"
                obj_pasien = PasienBPJS(id_p, nama, tindakan, obat, no_bpjs)

            elif jenis == "Pasien Asuransi":
                raw_extra = self.entry_extra.get().strip()
                if "," in raw_extra:
                    no_polis, pct = raw_extra.split(",", 1)
                    pct = float(pct.strip())
                else:
                    no_polis = raw_extra or "POL-DEFAULT"
                    pct = 15.0
                obj_pasien = PasienAsuransi(id_p, nama, tindakan, obat, no_polis, pct)

            total = obj_pasien.hitung_tagihan()
            self.lbl_hasil.configure(
                text=f"Total Tagihan: Rp {total:,.0f}\nNota terbuka di browser (bisa dicetak atau diunduh JPG).",
                text_color="#2ecc71"
            )

            buat_nota_html(obj_pasien)

        except ValueError:
            self.lbl_hasil.configure(text="Error: Input angka tidak valid!", text_color="#e74c3c")


if __name__ == "__main__":
    app = AppKlinik()
    app.mainloop()