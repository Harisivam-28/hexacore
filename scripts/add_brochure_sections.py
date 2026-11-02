#!/usr/bin/env python3
"""
Adds Hexacore Corporate Brochure sections:
1. Home page (index.html, frontend.html) bottom (before </main>)
2. Contact page (contact.html) top (right after <main>)
3. Interactive high-res 6-page brochure modal viewer & thumbnail strips
4. Direct PDF download links (/hexacore-brochure.pdf)
"""

import sys

BROCHURE_CSS = """
        /* ── Corporate Brochure Section & Modal ── */
        .brochure-section {
            padding: clamp(52px, 6vw, 84px) clamp(20px, 4vw, 44px);
            background: linear-gradient(135deg, #071527 0%, #0B1F3A 55%, #132a4e 100%);
            color: #ffffff;
            position: relative;
            overflow: hidden;
        }
        .brochure-section.border-top {
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .brochure-section.border-bottom {
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .brochure-grid {
            display: grid;
            grid-template-columns: 1.18fr 0.82fr;
            gap: clamp(28px, 4vw, 56px);
            align-items: center;
            max-width: 1240px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }
        .contact-brochure-grid {
            display: grid;
            grid-template-columns: 1.25fr 0.75fr;
            gap: clamp(24px, 3.5vw, 48px);
            align-items: center;
            max-width: 1240px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }
        .brochure-badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(244,123,32,0.15);
            border: 1px solid rgba(244,123,32,0.35);
            border-radius: 20px;
            padding: 6px 16px;
            margin-bottom: 16px;
        }
        .brochure-badge-pill .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--orange);
            box-shadow: 0 0 8px rgba(244,123,32,0.6);
        }
        .brochure-badge-pill .txt {
            font-size: 11px;
            font-weight: 800;
            color: var(--orange);
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .brochure-heading {
            font-family: 'Inter', sans-serif;
            font-size: clamp(24px, 3vw, 36px);
            font-weight: 900;
            color: #ffffff;
            line-height: 1.2;
            margin: 0 0 14px;
        }
        .brochure-desc {
            color: #AAB6C9;
            font-size: 15px;
            line-height: 1.65;
            margin-bottom: 24px;
            max-width: 650px;
        }
        .brochure-specs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 12px 18px;
            margin-bottom: 28px;
        }
        .brochure-spec-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }
        .brochure-spec-item svg {
            flex-shrink: 0;
            margin-top: 2px;
            color: var(--orange);
        }
        .brochure-spec-item span {
            font-size: 13px;
            color: #E2E8F0;
            line-height: 1.45;
        }
        .brochure-spec-item strong {
            color: #ffffff;
            font-weight: 700;
        }
        .brochure-actions {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 14px;
            margin-bottom: 14px;
        }
        .brochure-meta-note {
            font-size: 12px;
            color: #8292A6;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .brochure-meta-note span.sep {
            opacity: 0.4;
        }

        /* Card Mockup */
        .brochure-card-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
        }
        .brochure-mockup {
            position: relative;
            max-width: 330px;
            width: 100%;
            cursor: pointer;
        }
        .brochure-mockup-glow {
            position: absolute;
            inset: -6px;
            background: radial-gradient(circle, rgba(244,123,32,0.28) 0%, rgba(244,123,32,0) 70%);
            filter: blur(20px);
            border-radius: 14px;
            z-index: 0;
            transition: opacity 0.3s ease;
        }
        .brochure-mockup:hover .brochure-mockup-glow {
            opacity: 1;
        }
        .brochure-mockup-inner {
            position: relative;
            z-index: 1;
            border-radius: 12px;
            overflow: hidden;
            background: #071527;
            box-shadow: 0 20px 45px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,255,255,0.12);
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease;
        }
        .brochure-mockup:hover .brochure-mockup-inner {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 28px 60px rgba(0,0,0,0.7), 0 0 0 2px var(--orange);
        }
        .brochure-mockup-inner img {
            width: 100%;
            height: auto;
            display: block;
            aspect-ratio: 595/794;
            object-fit: cover;
        }
        .brochure-page-badge {
            position: absolute;
            top: 12px;
            right: 12px;
            background: rgba(7,21,39,0.85);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            color: #fff;
            padding: 4px 12px;
            border-radius: 16px;
            border: 1px solid rgba(244,123,32,0.5);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .brochure-page-badge .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--orange);
        }
        .brochure-hover-cta {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(7,21,39,0.95) 0%, rgba(7,21,39,0.4) 65%, rgba(7,21,39,0) 100%);
            padding: 36px 14px 14px;
            text-align: center;
        }
        .brochure-hover-cta span {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11.5px;
            font-weight: 800;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            background: var(--orange);
            padding: 6px 16px;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(244,123,32,0.4);
        }
        .brochure-thumbs-row {
            display: flex;
            gap: 8px;
            margin-top: 16px;
            max-width: 360px;
            width: 100%;
            justify-content: center;
        }
        .brochure-thumb-btn {
            border: 2px solid rgba(255,255,255,0.18);
            border-radius: 6px;
            padding: 0;
            background: #0B1F3A;
            cursor: pointer;
            overflow: hidden;
            transition: all 0.2s ease;
            width: 48px;
            height: 64px;
            flex-shrink: 0;
        }
        .brochure-thumb-btn:hover, .brochure-thumb-btn.active {
            border-color: var(--orange);
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(244,123,32,0.4);
        }
        .brochure-thumb-btn img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        /* Modal styles */
        .brochure-modal-backdrop {
            position: fixed;
            inset: 0;
            background: rgba(5, 14, 26, 0.94);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 99999;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
            opacity: 0;
            transition: opacity 0.25s ease;
        }
        .brochure-modal-backdrop.open {
            opacity: 1;
        }
        .brochure-modal-content {
            background: #0B1F3A;
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 14px;
            width: 100%;
            max-width: 980px;
            max-height: 94vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 30px 70px rgba(0, 0, 0, 0.75);
            animation: brochureModalZoom 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes brochureModalZoom {
            from { transform: scale(0.94); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .brochure-modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 22px;
            background: #071527;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            gap: 16px;
        }
        .brochure-modal-title-wrap {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .brochure-modal-badge {
            background: rgba(244,123,32,0.18);
            color: var(--orange);
            border: 1px solid rgba(244,123,32,0.4);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .brochure-modal-title {
            color: #fff;
            font-weight: 700;
            font-size: 14px;
        }
        .brochure-modal-counter {
            background: rgba(255,255,255,0.08);
            color: #94A3B8;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11.5px;
            font-weight: 600;
        }
        .brochure-modal-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .brochure-modal-dl-btn {
            padding: 9px 18px !important;
            font-size: 12px !important;
            border-radius: 4px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .brochure-modal-close {
            background: rgba(255,255,255,0.08);
            border: none;
            color: #fff;
            width: 36px;
            height: 36px;
            border-radius: 6px;
            font-size: 24px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
            transition: background 0.15s ease, transform 0.15s ease;
        }
        .brochure-modal-close:hover {
            background: #E53E3E;
            transform: scale(1.05);
        }
        .brochure-modal-stage {
            position: relative;
            flex: 1;
            min-height: 320px;
            max-height: 64vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #040c17;
            padding: 16px 64px;
        }
        .brochure-img-container {
            height: 100%;
            max-height: 60vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .brochure-img-container img {
            max-height: 58vh;
            max-width: 100%;
            width: auto;
            object-fit: contain;
            border-radius: 6px;
            box-shadow: 0 12px 36px rgba(0,0,0,0.65);
            transition: opacity 0.18s ease;
        }
        .brochure-nav-btn {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(11, 31, 58, 0.85);
            border: 1px solid rgba(255,255,255,0.18);
            color: #fff;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            font-size: 18px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            z-index: 2;
        }
        .brochure-nav-btn:hover {
            background: var(--orange);
            border-color: var(--orange);
            transform: translateY(-50%) scale(1.08);
        }
        .brochure-nav-btn.prev { left: 14px; }
        .brochure-nav-btn.next { right: 14px; }
        .brochure-modal-footer {
            background: #071527;
            padding: 12px 18px;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .brochure-modal-strip {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            overflow-x: auto;
            padding: 2px 4px;
        }
        .brochure-modal-strip .brochure-thumb-btn {
            width: 46px;
            height: 62px;
        }

        @media (max-width: 860px) {
            .brochure-grid, .contact-brochure-grid {
                grid-template-columns: 1fr !important;
                gap: 32px !important;
                text-align: left;
            }
            .brochure-card-wrapper {
                margin-top: 8px;
            }
            .brochure-mockup {
                max-width: 280px;
            }
            .brochure-modal-stage {
                padding: 12px 12px;
                max-height: 52vh;
            }
            .brochure-img-container img {
                max-height: 48vh;
            }
            .brochure-nav-btn {
                width: 36px;
                height: 36px;
                font-size: 14px;
            }
            .brochure-nav-btn.prev { left: 6px; }
            .brochure-nav-btn.next { right: 6px; }
            .brochure-modal-header {
                padding: 10px 14px;
            }
            .brochure-modal-title {
                font-size: 12.5px;
            }
            .brochure-modal-strip .brochure-thumb-btn {
                width: 36px;
                height: 48px;
            }
        }
"""

HOME_BROCHURE_SECTION = """
        <!-- 8. CORPORATE BROCHURE DOWNLOAD SECTION -->
        <section id="corporate-brochure" class="responsive-section brochure-section border-top">
            <!-- decorative subtle background radial accents -->
            <div style="position: absolute; top: -120px; right: -120px; width: 450px; height: 450px; border-radius: 50%; background: radial-gradient(circle, rgba(244,123,32,0.14) 0%, rgba(244,123,32,0) 70%); pointer-events: none;"></div>
            <div style="position: absolute; bottom: -100px; left: -100px; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(11,31,58,0.7) 0%, rgba(0,0,0,0) 70%); pointer-events: none;"></div>

            <div class="brochure-grid">
                <!-- Left: Content, highlights, and download buttons -->
                <div>
                    <div class="brochure-badge-pill">
                        <span class="dot"></span>
                        <span class="txt">Official Corporate Publication</span>
                    </div>

                    <h2 class="brochure-heading">
                        Download Hexacore Precision Corporate Brochure
                    </h2>

                    <p class="brochure-desc">
                        Explore our complete precision calibration capabilities, ISO compliance standards, CMM analysis, probing integrations, and pan-India service infrastructure in one comprehensive technical brochure.
                    </p>

                    <div class="brochure-specs-grid">
                        <div class="brochure-spec-item">
                            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <span><strong>Laser &amp; Rotary:</strong> Linear up to 40m, ballbar &amp; indexing tests</span>
                        </div>
                        <div class="brochure-spec-item">
                            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <span><strong>Geometric Accuracy:</strong> Spindle runout, straightness &amp; PMCs</span>
                        </div>
                        <div class="brochure-spec-item">
                            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <span><strong>Metrology &amp; Probing:</strong> 1D/2D gauges, VMM, CMM &amp; retrofit</span>
                        </div>
                        <div class="brochure-spec-item">
                            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <span><strong>Standards &amp; Traceability:</strong> ISO 230-2 / 230-4, VDI &amp; JIS</span>
                        </div>
                    </div>

                    <div class="brochure-actions">
                        <a href="/hexacore-brochure.pdf" download="Hexacore-Precision-Brochure.pdf" class="btn btn-orange" style="display:inline-flex; align-items:center; gap:10px; padding:15px 28px; box-shadow:0 8px 24px rgba(244,123,32,0.35);">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            <span>Download Brochure (PDF)</span>
                        </a>
                        <button type="button" onclick="openBrochureViewer(0)" class="btn btn-outline" style="display:inline-flex; align-items:center; gap:10px; padding:15px 24px;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                            <span>Preview Online (6 Pages)</span>
                        </button>
                        <a href="/hexacore-brochure.pdf" target="_blank" rel="noopener noreferrer" style="color:#94A3B8; font-size:12.5px; text-decoration:none; display:inline-flex; align-items:center; gap:4px; margin-left:4px;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#94A3B8'">
                            Open PDF in new tab ↗
                        </a>
                    </div>

                    <div class="brochure-meta-note">
                        <span>Official Edition</span>
                        <span class="sep">•</span>
                        <span>High-Resolution PDF (8.3 MB)</span>
                        <span class="sep">•</span>
                        <span>6 Full Color Pages</span>
                    </div>
                </div>

                <!-- Right: Brochure Showcase Mockup with Thumbnails -->
                <div class="brochure-card-wrapper">
                    <div class="brochure-mockup" onclick="openBrochureViewer(0)" title="Click to view full brochure">
                        <div class="brochure-mockup-glow"></div>
                        <div class="brochure-mockup-inner">
                            <img src="images/brochure/page-1.webp" alt="Hexacore Precision Technologies Corporate Brochure">
                            <div class="brochure-page-badge">
                                <span class="dot"></span>
                                <span>6 PAGES</span>
                            </div>
                            <div class="brochure-hover-cta">
                                <span>Click to View Pages</span>
                            </div>
                        </div>
                    </div>

                    <!-- Mini Page thumbs strip -->
                    <div class="brochure-thumbs-row">
                        <button type="button" class="brochure-thumb-btn active" onclick="openBrochureViewer(0)" title="Page 1: Cover"><img src="images/brochure/page-1-thumb.webp" alt="P1"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(1)" title="Page 2: About Us &amp; Foundation"><img src="images/brochure/page-2-thumb.webp" alt="P2"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(2)" title="Page 3: Calibrations &amp; CNC Types"><img src="images/brochure/page-3-thumb.webp" alt="P3"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(3)" title="Page 4: Probing &amp; Geometric Inspection"><img src="images/brochure/page-4-thumb.webp" alt="P4"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(4)" title="Page 5: Metrology Instruments &amp; Standards"><img src="images/brochure/page-5-thumb.webp" alt="P5"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(5)" title="Page 6: Reddot &amp; GMS Alliances"><img src="images/brochure/page-6-thumb.webp" alt="P6"></button>
                    </div>
                </div>
            </div>
        </section>
"""

CONTACT_BROCHURE_SECTION = """
        <!-- TOP BROCHURE DOWNLOAD & PREVIEW BANNER -->
        <section id="corporate-brochure" class="responsive-section brochure-section border-bottom" style="padding-top: clamp(40px, 5vw, 64px); padding-bottom: clamp(40px, 5vw, 64px);">
            <!-- decorative radial glow -->
            <div style="position: absolute; top: -100px; right: 10%; width: 380px; height: 380px; border-radius: 50%; background: radial-gradient(circle, rgba(244,123,32,0.15) 0%, rgba(244,123,32,0) 70%); pointer-events: none;"></div>

            <div class="contact-brochure-grid">
                <div>
                    <div class="brochure-badge-pill">
                        <span class="dot"></span>
                        <span class="txt">Official Capabilities Publication</span>
                    </div>

                    <h1 class="brochure-heading" style="font-size: clamp(24px, 3.2vw, 36px);">
                        Download Hexacore Precision Corporate Brochure
                    </h1>

                    <p class="brochure-desc" style="max-width: 720px;">
                        Need complete technical specifications, CNC calibration parameters, CMM inspection protocols, or corporate credentials for procurement approval? Download our official 6-page brochure or preview each page online.
                    </p>

                    <div class="brochure-actions">
                        <a href="/hexacore-brochure.pdf" download="Hexacore-Precision-Brochure.pdf" class="btn btn-orange" style="display:inline-flex; align-items:center; gap:10px; padding:14px 26px; font-weight:700; box-shadow:0 6px 20px rgba(244,123,32,0.35);">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            <span>Download Brochure (PDF)</span>
                        </a>
                        <button type="button" onclick="openBrochureViewer(0)" class="btn btn-outline" style="display:inline-flex; align-items:center; gap:10px; padding:14px 22px;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                            <span>Preview Online (6 Pages)</span>
                        </button>
                        <a href="/hexacore-brochure.pdf" target="_blank" rel="noopener noreferrer" style="color:#94A3B8; font-size:12.5px; text-decoration:none; display:inline-flex; align-items:center; gap:4px; margin-left:4px;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#94A3B8'">
                            Open PDF in new tab ↗
                        </a>
                    </div>

                    <div class="brochure-meta-note">
                        <span>6 Full Color Pages</span>
                        <span class="sep">•</span>
                        <span>High-Resolution PDF (8.3 MB)</span>
                        <span class="sep">•</span>
                        <span>ISO 230-2 &amp; VDI Standards Traceable</span>
                    </div>
                </div>

                <!-- Right: Brochure Showcase Mockup with Thumbnails -->
                <div class="brochure-card-wrapper">
                    <div class="brochure-mockup" style="max-width: 270px;" onclick="openBrochureViewer(0)" title="Click to view full brochure">
                        <div class="brochure-mockup-glow"></div>
                        <div class="brochure-mockup-inner">
                            <img src="images/brochure/page-1.webp" alt="Hexacore Precision Technologies Corporate Brochure">
                            <div class="brochure-page-badge">
                                <span class="dot"></span>
                                <span>6 PAGES</span>
                            </div>
                            <div class="brochure-hover-cta">
                                <span>Click to Preview</span>
                            </div>
                        </div>
                    </div>

                    <!-- Mini Page thumbs strip -->
                    <div class="brochure-thumbs-row" style="max-width: 290px;">
                        <button type="button" class="brochure-thumb-btn active" onclick="openBrochureViewer(0)" title="Page 1: Cover"><img src="images/brochure/page-1-thumb.webp" alt="P1"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(1)" title="Page 2: About Us &amp; Foundation"><img src="images/brochure/page-2-thumb.webp" alt="P2"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(2)" title="Page 3: Calibrations &amp; CNC Types"><img src="images/brochure/page-3-thumb.webp" alt="P3"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(3)" title="Page 4: Probing &amp; Geometric Inspection"><img src="images/brochure/page-4-thumb.webp" alt="P4"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(4)" title="Page 5: Metrology Instruments &amp; Standards"><img src="images/brochure/page-5-thumb.webp" alt="P5"></button>
                        <button type="button" class="brochure-thumb-btn" onclick="openBrochureViewer(5)" title="Page 6: Reddot &amp; GMS Alliances"><img src="images/brochure/page-6-thumb.webp" alt="P6"></button>
                    </div>
                </div>
            </div>
        </section>
"""

BROCHURE_MODAL_HTML_AND_JS = """
<!-- BROCHURE LIGHTBOX / VIEWER MODAL -->
<div id="brochureViewerModal" class="brochure-modal-backdrop" role="dialog" aria-modal="true" aria-label="Hexacore Corporate Brochure Viewer">
    <div class="brochure-modal-content">
        <!-- Top bar -->
        <div class="brochure-modal-header">
            <div class="brochure-modal-title-wrap">
                <span class="brochure-modal-badge">Official Brochure</span>
                <span class="brochure-modal-title">Hexacore Precision Technologies</span>
                <span id="brochurePageCounter" class="brochure-modal-counter">Page 1 of 6</span>
            </div>
            <div class="brochure-modal-actions">
                <a href="/hexacore-brochure.pdf" download="Hexacore-Precision-Brochure.pdf" class="btn btn-orange brochure-modal-dl-btn">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                    <span>Download PDF</span>
                </a>
                <button type="button" class="brochure-modal-close" onclick="closeBrochureViewer()" aria-label="Close Brochure Viewer">
                    &times;
                </button>
            </div>
        </div>

        <!-- Center viewport with nav arrows and high-res page image -->
        <div class="brochure-modal-stage">
            <button type="button" class="brochure-nav-btn prev" onclick="changeBrochurePage(-1)" aria-label="Previous Page">
                &#10094;
            </button>
            <div class="brochure-img-container">
                <img id="brochureActiveImg" src="images/brochure/page-1.webp" alt="Hexacore Brochure Page 1" />
            </div>
            <button type="button" class="brochure-nav-btn next" onclick="changeBrochurePage(1)" aria-label="Next Page">
                &#10095;
            </button>
        </div>

        <!-- Bottom Page Selector Tabs -->
        <div class="brochure-modal-footer">
            <div class="brochure-modal-strip" id="brochureModalStrip">
                <button type="button" class="brochure-thumb-btn active" onclick="setBrochurePage(0)" title="Page 1: Cover"><img src="images/brochure/page-1-thumb.webp" alt="P1"></button>
                <button type="button" class="brochure-thumb-btn" onclick="setBrochurePage(1)" title="Page 2: About Us &amp; Foundation"><img src="images/brochure/page-2-thumb.webp" alt="P2"></button>
                <button type="button" class="brochure-thumb-btn" onclick="setBrochurePage(2)" title="Page 3: Calibrations &amp; CNC Types"><img src="images/brochure/page-3-thumb.webp" alt="P3"></button>
                <button type="button" class="brochure-thumb-btn" onclick="setBrochurePage(3)" title="Page 4: Probing &amp; Geometric Inspection"><img src="images/brochure/page-4-thumb.webp" alt="P4"></button>
                <button type="button" class="brochure-thumb-btn" onclick="setBrochurePage(4)" title="Page 5: Metrology Instruments &amp; Standards"><img src="images/brochure/page-5-thumb.webp" alt="P5"></button>
                <button type="button" class="brochure-thumb-btn" onclick="setBrochurePage(5)" title="Page 6: Reddot &amp; GMS Alliances"><img src="images/brochure/page-6-thumb.webp" alt="P6"></button>
            </div>
        </div>
    </div>
</div>

<script>
    // ── Hexacore Brochure Interactive Modal Controller ────────────────
    const brochurePages = [
        { title: "Page 1 — Cover & Calibration Capabilities", src: "images/brochure/page-1.webp" },
        { title: "Page 2 — About Us & Our Foundation", src: "images/brochure/page-2.webp" },
        { title: "Page 3 — Machine Analyses & Types We Calibrate", src: "images/brochure/page-3.webp" },
        { title: "Page 4 — Probing Solutions & Geometric Inspection", src: "images/brochure/page-4.webp" },
        { title: "Page 5 — Height Gauges, VMM, CMM & Standards", src: "images/brochure/page-5.webp" },
        { title: "Page 6 — Portable Arm, Reddot & GMS Alliances", src: "images/brochure/page-6.webp" }
    ];
    let currentBrochurePageIndex = 0;

    function openBrochureViewer(pageIndex = 0) {
        currentBrochurePageIndex = Math.max(0, Math.min(pageIndex, brochurePages.length - 1));
        const modal = document.getElementById('brochureViewerModal');
        if (!modal) return;
        renderBrochureModalPage();
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('open'), 10);
        document.body.style.overflow = 'hidden';
    }

    function closeBrochureViewer() {
        const modal = document.getElementById('brochureViewerModal');
        if (!modal) return;
        modal.classList.remove('open');
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }, 250);
    }

    function changeBrochurePage(delta) {
        let next = currentBrochurePageIndex + delta;
        if (next < 0) next = brochurePages.length - 1;
        if (next >= brochurePages.length) next = 0;
        currentBrochurePageIndex = next;
        renderBrochureModalPage();
    }

    function setBrochurePage(index) {
        currentBrochurePageIndex = index;
        renderBrochureModalPage();
    }

    function renderBrochureModalPage() {
        const page = brochurePages[currentBrochurePageIndex];
        const img = document.getElementById('brochureActiveImg');
        const counter = document.getElementById('brochurePageCounter');
        if (img) {
            img.style.opacity = '0.5';
            img.src = page.src;
            img.alt = page.title;
            img.onload = () => { img.style.opacity = '1'; };
        }
        if (counter) {
            counter.textContent = `Page ${currentBrochurePageIndex + 1} of ${brochurePages.length}`;
        }
        // Update active thumbnail in strip
        document.querySelectorAll('#brochureModalStrip .brochure-thumb-btn').forEach((btn, idx) => {
            if (idx === currentBrochurePageIndex) {
                btn.classList.add('active');
                btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // Close on backdrop click
    document.addEventListener('DOMContentLoaded', function() {
        const modal = document.getElementById('brochureViewerModal');
        if (modal) {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    closeBrochureViewer();
                }
            });
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        const modal = document.getElementById('brochureViewerModal');
        if (!modal || !modal.classList.contains('open')) return;
        if (e.key === 'Escape') closeBrochureViewer();
        if (e.key === 'ArrowLeft') changeBrochurePage(-1);
        if (e.key === 'ArrowRight') changeBrochurePage(1);
    });

    // Touch swipe support on modal stage
    (function() {
        window.addEventListener('DOMContentLoaded', function() {
            const stage = document.querySelector('.brochure-modal-stage');
            if (!stage) return;
            let touchStartX = 0;
            stage.addEventListener('touchstart', function(e) {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });
            stage.addEventListener('touchend', function(e) {
                let touchEndX = e.changedTouches[0].screenX;
                if (touchStartX - touchEndX > 50) {
                    changeBrochurePage(1);
                } else if (touchEndX - touchStartX > 50) {
                    changeBrochurePage(-1);
                }
            }, { passive: true });
        });
    })();
</script>
"""

def update_file(filepath, is_home=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert CSS
    if '.brochure-section' not in content:
        # Insert before </head>
        head_target = '</head>'
        if head_target in content:
            content = content.replace(head_target, f'<style>{BROCHURE_CSS}</style>\n{head_target}', 1)
            print(f"[{filepath}] CSS inserted successfully")
        else:
            print(f"[{filepath}] ERROR: </head> not found")

    # 2. Insert Brochure Section
    if is_home:
        if 'id="corporate-brochure"' not in content:
            # Home page bottom: right before </main>
            main_end = '</main>'
            if main_end in content:
                content = content.replace(main_end, f'{HOME_BROCHURE_SECTION}\n{main_end}', 1)
                print(f"[{filepath}] Home brochure section inserted before </main>")
            else:
                print(f"[{filepath}] ERROR: </main> not found")
    else:
        if 'id="corporate-brochure"' not in content:
            # Contact page top: right after <main>
            main_start = '<main>'
            if main_start in content:
                content = content.replace(main_start, f'<main>\n{CONTACT_BROCHURE_SECTION}', 1)
                print(f"[{filepath}] Contact top brochure section inserted after <main>")
            else:
                print(f"[{filepath}] ERROR: <main> not found")

    # 3. Insert Modal + JS
    if 'id="brochureViewerModal"' not in content:
        body_end = '</body>'
        if body_end in content:
            content = content.replace(body_end, f'{BROCHURE_MODAL_HTML_AND_JS}\n{body_end}', 1)
            print(f"[{filepath}] Brochure viewer modal inserted before </body>")
        else:
            print(f"[{filepath}] ERROR: </body> not found")

    # 4. Update Quick Links in footerHTML to include Download Brochure
    quick_links_target = '<li><a href="/contact">Contact</a></li>'
    brochure_link = '<li><a href="/contact">Contact</a></li>\n      <li><a href="/hexacore-brochure.pdf" download="Hexacore-Precision-Brochure.pdf">Download Brochure</a></li>'
    if 'Download Brochure</a></li>' not in content and quick_links_target in content:
        content = content.replace(quick_links_target, brochure_link)
        print(f"[{filepath}] Footer Quick Links updated with Download Brochure link")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Starting brochure insertion...")
update_file('index.html', is_home=True)
update_file('frontend.html', is_home=True)
update_file('contact.html', is_home=False)
print("Finished brochure insertion.")

