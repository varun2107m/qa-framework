from datetime import datetime
import re


def parse_sections(review: str) -> dict:
    sections = {}
    pattern = r"##\s+(.+?)\n(.*?)(?=\n##\s|\Z)"
    matches = re.findall(pattern, review, re.DOTALL)
    for title, content in matches:
        sections[title.strip()] = content.strip()
    return sections


def risk_badge(level: str) -> str:
    level = level.strip().split()[0].lower()
    colors = {
        "high":   ("##c0392b", "#fdf0ef", "#f5c6c2"),
        "medium": ("#d35400", "#fef5ec", "#f9d4b0"),
        "low":    ("#27ae60", "#eafaf1", "#a9dfbf"),
    }
    c = colors.get(level, ("#555", "#f4f4f4", "#ddd"))
    label = level.capitalize()
    return f'<span style="color:{c[0]};background:{c[1]};border:1px solid {c[2]};border-radius:6px;padding:3px 12px;font-size:13px;font-weight:600;">{label}</span>'


def section_html(title: str, icon: str, content: str) -> str:
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    items = "".join(
        f'<li style="padding:6px 0;border-bottom:1px solid #f0f0f0;line-height:1.6;">{l.lstrip("- ").lstrip("* ")}</li>'
        for l in lines
    )
    return f"""
    <div style="background:white;border-radius:12px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,0.08);margin-bottom:20px;">
      <h2 style="font-size:15px;font-weight:600;color:#1a1a2e;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #f0f0f0;">{icon} {title}</h2>
      <ul style="list-style:none;padding:0;margin:0;font-size:13px;color:#333;">{items}</ul>
    </div>"""


def generate_pr_report(pr_data: dict, review: str, pr_id: str) -> str:
    changed_files = pr_data.get("changed_files", [])
    title = pr_data.get("title", f"#{pr_id}")
    description = pr_data.get("description") or "No description provided."
    generated_at = datetime.now().strftime("%B %d, %Y at %H:%M")
    sections = parse_sections(review)

    # Risk badge
    risk_raw = sections.get("Overall Risk Level", "Unknown")
    risk_display = risk_badge(risk_raw)

    # Summary
    summary = sections.get("Summary", "No summary available.")

    # Files list
    files_html = "".join(
        f'<div style="display:flex;align-items:center;gap:10px;padding:9px 12px;border:1px solid #f0f0f0;border-radius:8px;margin-bottom:6px;font-size:12px;font-family:monospace;color:#333;">📄 {f}</div>'
        for f in changed_files
    )

    # Build all review sections
    section_blocks = ""

    section_map = [
        ("What Changed",        "🔀"),
        ("Diff Analysis",       "🔍"),
        ("Security",            "🔒"),
        ("Code Quality",        "✨"),
        ("Functional Risk",     "⚠️"),
        ("Regression Risk",     "🔁"),
        ("Performance",         "⚡"),
        ("Test Coverage Gaps",  "🧪"),
        ("Affected Modules",    "📦"),
        ("Suggested Test Scenarios", "📋"),
    ]

    for sec_title, icon in section_map:
        content = sections.get(sec_title, "")
        if content:
            section_blocks += section_html(sec_title, icon, content)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Review: {title}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f4f6f9; color: #1a1a2e; }}
    .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; padding: 32px 40px; }}
    .header h1 {{ font-size: 22px; font-weight: 600; margin-bottom: 6px; }}
    .header p {{ font-size: 13px; opacity: 0.7; }}
    .badge {{ background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.2); border-radius:20px; padding:3px 12px; font-size:12px; font-weight:500; margin-right:10px; }}
    .container {{ max-width: 1000px; margin: 32px auto; padding: 0 24px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 14px; margin-bottom: 24px; }}
    .stat {{ background: white; border-radius: 12px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid #0f3460; }}
    .stat .label {{ font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }}
    .stat .value {{ font-size: 20px; font-weight: 700; }}
    .summary-card {{ background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 20px; border-left: 4px solid #0f3460; }}
    .summary-card h2 {{ font-size:15px; font-weight:600; margin-bottom:10px; }}
    .summary-card p {{ font-size:14px; color:#444; line-height:1.7; }}
    .desc {{ font-size:13px; color:#555; background:#f8f9fc; border-radius:8px; padding:14px; margin-top:10px; line-height:1.6; }}
    .tabs {{ display:flex; gap:4px; margin-bottom:20px; background:#f4f6f9; padding:4px; border-radius:10px; width:fit-content; }}
    .tab {{ padding:8px 18px; border-radius:8px; font-size:13px; font-weight:500; cursor:pointer; color:#666; border:none; background:transparent; }}
    .tab.active {{ background:white; color:#1a1a2e; box-shadow:0 1px 3px rgba(0,0,0,0.1); }}
    #tab-files {{ display:none; }}
    .footer {{ text-align:center; padding:24px; font-size:12px; color:#999; }}
  </style>
</head>
<body>

<div class="header">
  <div style="margin-bottom:10px;">
    <span class="badge">#{pr_id}</span>
    <span style="font-size:12px;opacity:0.7;">Generated on {generated_at}</span>
  </div>
  <h1>{title}</h1>
  <p>{pr_data.get("description", "")[:120] if pr_data.get("description") else "AI Comprehensive Code Review"}</p>
</div>

<div class="container">

  <div class="grid">
    <div class="stat">
      <div class="label">Files Changed</div>
      <div class="value">{len(changed_files)}</div>
    </div>
    <div class="stat">
      <div class="label">Reference</div>
      <div class="value" style="font-size:16px;padding-top:4px;">#{pr_id}</div>
    </div>
    <div class="stat">
      <div class="label">Overall Risk</div>
      <div class="value" style="font-size:14px;padding-top:6px;">{risk_display}</div>
    </div>
    <div class="stat">
      <div class="label">Status</div>
      <div class="value" style="font-size:16px;padding-top:4px;">✅ Done</div>
    </div>
  </div>

  <div class="summary-card">
    <h2>📝 Summary</h2>
    <p>{summary}</p>
    <div class="desc"><strong>PR Description:</strong> {description}</div>
  </div>

  <div style="background:white;border-radius:12px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,0.08);margin-bottom:20px;">
    <h2 style="font-size:15px;font-weight:600;color:#1a1a2e;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #f0f0f0;">📂 Files & Review</h2>
    <div class="tabs">
      <button class="tab active" onclick="showTab('review', this)">Full Review</button>
      <button class="tab" onclick="showTab('files', this)">Changed Files ({len(changed_files)})</button>
    </div>
    <div id="tab-review">
      {section_blocks}
    </div>
    <div id="tab-files">
      {files_html}
    </div>
  </div>

</div>

<div class="footer">Generated by QA AI Orchestrator</div>

<script>
  function showTab(name, btn) {{
    document.getElementById('tab-review').style.display = name === 'review' ? 'block' : 'none';
    document.getElementById('tab-files').style.display = name === 'files' ? 'block' : 'none';
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
  }}
</script>
</body>
</html>"""

    return html

