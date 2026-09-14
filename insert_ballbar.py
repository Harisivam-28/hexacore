import re

svc_06_block = '''                    <div class="svc-card-expandable" id="svc-06">
                        <div class="svc-img-wrap" style="height:200px;overflow:hidden;background:#F8FAFC;display:flex;align-items:center;justify-content:center;padding:12px;">
                            <img src="images/services/machine_health_diagnose.png" alt="Machine Health Diagnose (Ballbar Test)" style="max-width:92%;max-height:92%;object-fit:contain;">
                        </div>
                        <div class="svc-card-top" onclick="toggleIndividualService(this)">
                            <div class="svc-card-header-row">
                                <span style="font-size:11px;font-weight:700;color:var(--orange);text-transform:uppercase;">Click to Expand ▼</span>
                            </div>
                            <h4>Machine Health Diagnose (Ballbar Test)</h4>
                            <p>Evaluates overall CNC performance by analyzing circular interpolation errors.</p>
                            <div class="svc-expand-trigger">
                                <span>View Full Details, Machines &amp; Standards</span>
                                <span class="chevron">▼</span>
                            </div>
                        </div>
                        <div class="svc-drawer-body">
                            <div class="svc-drawer-content">

                                <!-- 1. Service Details -->
                                <div class="svc-drawer-block">
                                    <div class="svc-drawer-block-title"><span>01</span> 📋 Service Details &amp; Specifications</div>
                                    <p style="font-size:13px;color:var(--steel);margin:0;line-height:1.55;">Quick, highly effective circularity test using a telescoping magnetic ballbar. Analyzes circular contouring accuracy, backlash, reversal spikes, lateral play, and servo mismatch in under 15 minutes.</p>
                                </div>

                                <!-- 2. Types of Calibrated Machines -->
                                <div class="svc-drawer-block">
                                    <div class="svc-drawer-block-title"><span>02</span> ⚙️ Types of Calibrated Machines</div>
                                    <div class="svc-machine-tag-grid">
                                        <span class="svc-machine-tag">CNC Turning Centers (Lathes)</span><span class="svc-machine-tag">Vertical Machining Centers (VMC)</span><span class="svc-machine-tag">Horizontal Machining Centers (HMC)</span><span class="svc-machine-tag">2-Axis CNC Machines</span>
                                    </div>
                                </div>

                                <!-- 3. Applicable Standards to Refer -->
                                <div class="svc-drawer-block">
                                    <div class="svc-drawer-block-title"><span>03</span> 📜 Applicable Standards to Refer</div>
                                    <div class="svc-std-list">
                                        <div class="svc-std-item"><strong>ISO 230-4</strong> – Circular tests for NC machine tools using ballbar systems.</div><div class="svc-std-item"><strong>BSI BS 3800</strong> – Methods for testing accuracy of machine tools.</div>
                                    </div>
                                </div>

                                <!-- 4. Importance of Technical Reports -->
                                <div class="svc-drawer-block" style="background:#FFF7ED;border-color:#FED7AA;">
                                    <div class="svc-drawer-block-title" style="color:#C2410C;"><span style="background:#C2410C;">04</span> 📊 Importance of Clear Technical Reports</div>
                                    <p style="font-size:13px;color:#9A3412;margin:0;line-height:1.55;">Generates polar plot diagnostic charts detailing exact backlash (µm), servo mismatch (ms), and squareness error, enabling targeted mechanical repairs before major machine breakdown.</p>
                                </div>

                            </div>
                        </div>
                    </div>'''

for filename in ['index.html', 'frontend.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target the end of Division 1 (CNC Machine Tool Calibration) section right before </section>
    target = '''                </div>
            </div>
        </section>


        <section class="responsive-section" style="background:#fff;padding:64px 44px;border-bottom:1px solid #e2e8f0;">'''

    replacement = svc_06_block + '''
                </div>
            </div>
        </section>


        <section class="responsive-section" style="background:#fff;padding:64px 44px;border-bottom:1px solid #e2e8f0;">'''

    if target in content and 'id="svc-06"' not in content:
        content = content.replace(target, replacement)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Successfully inserted svc-06 into {filename}')
