#!/usr/bin/env python3
"""Generate Bytes 360 interior pages with shared header/footer chrome."""
import os

ROOT = "/Users/yb/Desktop/Bytes 360"
EMAIL = "brightbyte.myb@gmail.com"  # TODO: swap for company address

MARK = '''<svg width="{s}" height="{s}" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect x="1" y="9" width="6" height="6" rx="2" fill="#4a5578"/><rect x="9" y="9" width="6" height="6" rx="2" fill="#4a5578"/><rect x="17" y="9" width="6" height="6" rx="2" fill="#4a5578"/><rect x="25" y="9" width="6" height="6" rx="2" fill="#ffb627"/><rect x="1" y="17" width="6" height="6" rx="2" fill="#4a5578"/><rect x="9" y="17" width="6" height="6" rx="2" fill="#98a2bd"/><rect x="17" y="17" width="6" height="6" rx="2" fill="#4a5578"/><rect x="25" y="17" width="6" height="6" rx="2" fill="#4a5578"/></svg>'''

NAV_ITEMS = [
    ("index.html", "Home"), ("services.html", "Services"), ("process.html", "Process"),
    ("about.html", "About"), ("careers.html", "Careers"), ("contact.html", "Contact"),
]

def header(current):
    cur = ' aria-current="page"'
    links = "\n        ".join(
        f'<a href="{href}"{cur if href == current else ""}>{label}</a>'
        for href, label in NAV_ITEMS
    )
    return f'''  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="index.html" aria-label="Bytes 360 home">
        {MARK.format(s=30)}
        Bytes&nbsp;<span class="byte">360</span>
      </a>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false" aria-controls="siteNav">
        <span></span><span></span><span></span>
      </button>
      <nav class="site-nav" id="siteNav" aria-label="Main">
        {links}
        <a href="contact.html" class="btn btn-sm nav-cta">Start a project</a>
      </nav>
    </div>
  </header>'''

FOOTER = f'''  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="brand" href="index.html">
            {MARK.format(s=26)}
            Bytes&nbsp;<span class="byte">360</span>
          </a>
          <p class="footer-tagline">A software development studio that takes products from first question to stable orbit.</p>
        </div>
        <div>
          <h4>Studio</h4>
          <ul>
            <li><a href="services.html">Services</a></li>
            <li><a href="process.html">Process</a></li>
            <li><a href="about.html">About</a></li>
          </ul>
        </div>
        <div>
          <h4>Join us</h4>
          <ul>
            <li><a href="careers.html">Careers</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul>
            <!-- TODO: replace with your company address once set up -->
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><span class="muted" style="font-size:.94rem">Remote-first · Worldwide</span></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span data-year>2026</span> Bytes 360. All rights reserved.</span>
        <span>Made with care — and shipped on a Friday.</span>
      </div>
    </div>
  </footer>'''

def page(filename, title, description, current, main):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#070b16">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="css/style.css">
  <script>document.documentElement.classList.add("js");</script>
</head>
<body>
{header(current)}

  <main id="main">
{main}
  </main>

{FOOTER}

  <script src="js/main.js" defer></script>
</body>
</html>
'''

def hero(eyebrow, h1, lede):
    return f'''    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow reveal">{eyebrow}</p>
        <h1 class="reveal" style="--d:.05s">{h1}</h1>
        <p class="lede reveal" style="--d:.1s">{lede}</p>
      </div>
    </section>'''

def cta(h, p, label="Start the conversation"):
    return f'''    <section class="section">
      <div class="wrap">
        <div class="cta-band reveal">
          <p class="eyebrow" style="justify-content:center">Ready when you are</p>
          <h2>{h}</h2>
          <p>{p}</p>
          <a class="btn" href="contact.html">{label} <span class="arrow" aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>'''

# ============================== SERVICES ==============================
def detail(anchor, name, body, items):
    lis = "\n            ".join(f"<li>{i}</li>" for i in items)
    return f'''        <div class="detail-row reveal" id="{anchor}">
          <div>
            <h3>{name}</h3>
            {body}
          </div>
          <div class="deliverables">
            <h4>What this includes</h4>
            <ul>
            {lis}
            </ul>
          </div>
        </div>'''

services_main = hero(
    "Services",
    "Everything it takes to ship.",
    "Strategy, design, engineering, and operations under one roof — so nothing gets lost between handoffs. Every service below is delivered by the same senior team, on the same weekly demo rhythm."
) + f'''

    <section class="section-tight">
      <div class="wrap">
{detail("custom", "Custom software",
        "<p>The spreadsheet that became a process. The legacy system nobody dares to touch. The workflow your off-the-shelf tools almost cover. We build software shaped around how your company actually operates — and modernise what's already there without stopping the business to do it.</p><p>Every custom build starts with a workflow audit, because the most expensive software is the kind that solves the wrong problem.</p>",
        ["Workflow &amp; systems audit", "Internal tools, dashboards &amp; portals",
         "Third-party integrations — CRM, ERP, payments", "Legacy system modernisation",
         "Role-based access &amp; audit trails", "Documentation &amp; training handover"])}
{detail("web", "Web applications",
        "<p>From a marketing site that loads instantly to a SaaS platform with thousands of concurrent users — we build for the web with performance and accessibility budgets agreed up front, not discovered in production.</p><p>Search engines, screen readers, and slow connections are treated as first-class users on every build.</p>",
        ["SaaS products &amp; customer portals", "Progressive web apps",
         "Real-time &amp; collaborative features", "WCAG 2.1 AA accessibility reviews",
         "Performance budgets &amp; Core Web Vitals", "Analytics &amp; experimentation setup"])}
{detail("mobile", "Mobile apps",
        "<p>Native Swift and Kotlin when the product demands it; React Native or Flutter when one codebase serves you better. We recommend the platform strategy that fits your product and team — not the one we happen to prefer.</p><p>Store submission, release trains, and crash monitoring are part of the engagement, because an app isn't done when it compiles.</p>",
        ["Native iOS (Swift) &amp; Android (Kotlin)", "Cross-platform with React Native or Flutter",
         "Offline-first data sync", "Push notifications &amp; deep linking",
         "App Store &amp; Play Store submission", "Crash reporting &amp; phased releases"])}
{detail("cloud", "Cloud &amp; DevOps",
        "<p>Releases should be boring. We design cloud architecture, migrate workloads, and build CI/CD pipelines that let your team deploy on a Friday afternoon without holding their breath.</p><p>Everything is infrastructure-as-code in your own cloud accounts — reviewable, repeatable, and yours.</p>",
        ["Cloud architecture &amp; migration plans", "Infrastructure as code with Terraform",
         "Kubernetes &amp; container platforms", "CI/CD pipelines with review gates",
         "Observability — metrics, logs, tracing", "Cost reviews &amp; right-sizing"])}
{detail("ai", "Data &amp; AI",
        "<p>We build AI features the same way we build everything else: measured. Retrieval pipelines, agents, and copilots ship with evaluation suites and guardrails, so you know how they behave before your users do.</p><p>Underneath, we put your data in order — pipelines, warehouses, and dashboards your whole team can trust.</p>",
        ["Data pipelines &amp; warehouses", "Product analytics &amp; dashboards",
         "LLM features — RAG, agents, copilots", "Evaluation suites &amp; guardrails",
         "Cost &amp; latency optimisation", "Privacy-aware data handling"])}
{detail("qa", "QA &amp; support",
        "<p>Shipped software needs looking after. We write the test automation that keeps regressions out, run security and dependency reviews on a schedule, and offer SLA-backed maintenance for products we built — and ones we didn't.</p>",
        ["Test automation, unit through end-to-end", "Manual &amp; exploratory QA",
         "Security &amp; dependency reviews", "SLA-backed maintenance plans",
         "Incident response &amp; postmortems", "Quarterly product health reports"])}
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Common questions</p>
          <h2>Asked before, answered honestly.</h2>
        </div>
        <div class="faq" style="max-width:780px">
          <details class="reveal">
            <summary>How do projects usually start?</summary>
            <p>Almost always with a discovery sprint: one to two weeks where we interrogate the idea, prototype the riskiest piece, and produce a scoped plan with a real estimate. It's fixed-price, and the outputs are yours even if you build elsewhere.</p>
          </details>
          <details class="reveal">
            <summary>What does a project cost?</summary>
            <p>It depends on scope, team size, and duration — which is why we don't quote from a contact form. After discovery you get a fixed quote for fixed-scope work, or a transparent monthly rate for a dedicated team. We'll share honest ranges on the first call.</p>
          </details>
          <details class="reveal">
            <summary>How long does a first version take?</summary>
            <p>Most MVPs we build ship in eight to fourteen weeks. You'll see working software in a staging environment from the first week, so there's never a long silent stretch before a big reveal.</p>
          </details>
          <details class="reveal">
            <summary>Who owns the code and the infrastructure?</summary>
            <p>You do — completely. Repositories, cloud accounts, designs, and documentation live in your organisation's accounts from day one. If we part ways, you lose nothing.</p>
          </details>
          <details class="reveal">
            <summary>Can you work with our existing codebase or team?</summary>
            <p>Yes. We start with a short audit to understand what's there, then either take ownership of a workstream or embed senior engineers directly into your team's rituals and review process.</p>
          </details>
          <details class="reveal">
            <summary>What happens after launch?</summary>
            <p>Your choice: a clean, documented handover to your team, or an ongoing plan — support SLAs, monitoring, and a continuing product roadmap. Most clients start with three months of post-launch support and decide from there.</p>
          </details>
        </div>
      </div>
    </section>

''' + cta("Not sure which service fits?",
          "Describe the problem instead — we'll tell you the smallest engagement that solves it.")

# ============================== PROCESS ==============================
def pstep(num, name, time, body, artifacts):
    lis = "\n              ".join(f"<li>{a}</li>" for a in artifacts)
    return f'''        <div class="detail-row reveal">
          <div>
            <span class="num" style="font-family:var(--mono);font-size:.8rem;color:var(--amber);letter-spacing:.14em">STAGE {num} · {time}</span>
            <h3 style="margin-top:10px">{name}</h3>
            {body}
          </div>
          <div class="deliverables">
            <h4>You get</h4>
            <ul>
              {lis}
            </ul>
          </div>
        </div>'''

process_main = hero(
    "Process",
    "How an idea reaches orbit.",
    "The same journey as the flight on our homepage — discover, design, build, launch — plus the part that matters most: what happens after. No mystery, no black box, no big reveal at the end."
) + f'''

    <section class="section-tight">
      <div class="wrap">
{pstep("01", "Discover", "1–2 weeks",
       "<p>We start by understanding the problem better than the brief describes it. That means talking to the people who'll use the product, auditing any existing systems, and prototyping the single riskiest assumption before committing to a plan.</p><p>Discovery is fixed-price and stands on its own — everything it produces is useful whether or not we build together.</p>",
       ["A scoped, prioritised feature map", "A prototype of the riskiest piece",
        "Architecture recommendation", "A real estimate with named risks"])}
{pstep("02", "Design", "2–3 weeks",
       "<p>Design and architecture happen side by side. While the designer turns flows into a clickable prototype, the lead engineer designs the system underneath it — so nothing gets approved that can't be built well.</p><p>You review the prototype on your own devices, with your own data scenarios, before a sprint is planned.</p>",
       ["Clickable prototype of core flows", "UI system — components, tokens, states",
        "System architecture &amp; data model", "A sprint-by-sprint build plan"])}
{pstep("03", "Build", "weekly cycles",
       "<p>Build runs in one-week cycles, each ending with a Friday demo of working software in a staging environment you can open anytime. Progress is visible in your project board and your inbox — never just claimed in a meeting.</p><p>Every line of code is reviewed, tested in CI, and merged behind feature flags, so the main branch is always releasable.</p>",
       ["A demo every Friday, no exceptions", "Staging environment from week one",
        "Weekly written progress notes", "A main branch that's always shippable"])}
{pstep("04", "Launch", "when it's ready",
       "<p>Launch is a checklist, not a leap of faith: load tests run, monitoring wired, rollback rehearsed, and a go-live plan agreed with your team. We ship gradually where the product allows it and watch the dashboards with you.</p>",
       ["Pre-launch checklist &amp; load tests", "Monitoring, alerting &amp; dashboards",
        "A rehearsed rollback plan", "Go-live support in the room"])}
{pstep("05", "Evolve", "ongoing",
       "<p>The first release is the beginning, not the end. We review what real usage teaches, keep dependencies current and security patched, and plan the next quarter of product work with you — or hand over cleanly to your in-house team.</p>",
       ["Usage review &amp; next-quarter roadmap", "SLA-backed support option",
        "Security &amp; dependency updates", "A full, documented handover — if you want it"])}
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Working together</p>
          <h2>What collaboration actually looks like.</h2>
        </div>
        <div class="grid grid-4">
          <article class="card reveal">
            <h3>One point of contact</h3>
            <p>A project lead who knows every detail — not an account manager relaying messages.</p>
          </article>
          <article class="card reveal" style="--d:.06s">
            <h3>Your tools or ours</h3>
            <p>We work in your Slack, Linear, and GitHub — or set ours up for you. Either way, you see everything.</p>
          </article>
          <article class="card reveal" style="--d:.12s">
            <h3>Async by default</h3>
            <p>Written updates over status meetings. Your calendar stays yours; the record stays searchable.</p>
          </article>
          <article class="card reveal" style="--d:.18s">
            <h3>Bad news travels fast</h3>
            <p>If a risk appears, you hear it that day — with options, not excuses.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tight">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">The quality bar</p>
          <h2>Non-negotiables on every build.</h2>
        </div>
        <div class="grid grid-3">
          <div class="step reveal"><h3>Reviewed code</h3><p>Nothing merges without a second senior pair of eyes. Ever.</p></div>
          <div class="step reveal" style="--d:.06s"><h3>Tested in CI</h3><p>Unit, integration, and end-to-end tests run on every pull request.</p></div>
          <div class="step reveal" style="--d:.12s"><h3>Secure by default</h3><p>Least-privilege access, secret scanning, and dependency audits in the pipeline.</p></div>
          <div class="step reveal"><h3>Observable</h3><p>Metrics, logs, and traces wired before launch — not after the first incident.</p></div>
          <div class="step reveal" style="--d:.06s"><h3>Documented</h3><p>Architecture decisions and runbooks written as we go, not reconstructed later.</p></div>
          <div class="step reveal" style="--d:.12s"><h3>Accessible</h3><p>WCAG 2.1 AA is the floor for everything with a user interface.</p></div>
        </div>
      </div>
    </section>

''' + cta("Want to see this process on your product?",
          "Tell us where you are — an idea, a prototype, or a system under strain — and we'll map the route.")

# ============================== ABOUT ==============================
about_main = hero(
    "About",
    "The studio behind the bytes.",
    "Bytes 360 exists because too much software gets built twice: once wrong, then again properly. We were founded by engineers to do the second version first."
) + f'''

    <section class="section-tight">
      <div class="wrap">
        <div class="grid grid-2" style="align-items:start;gap:48px">
          <div class="reveal">
            <h2>Why we exist</h2>
            <p>Every engineer here has lived the other side of this industry: the agency that staffed juniors after selling seniors, the project that went dark for two months and returned unrecognisable, the codebase held hostage by its own builders.</p>
            <p>Bytes 360 is the studio we wished we could have hired. Small senior teams. Working software every week. Code, infrastructure, and documentation that live in the client's accounts from the first commit — so trust is structural, not contractual.</p>
          </div>
          <div class="reveal" style="--d:.08s">
            <h2>How we're built</h2>
            <p>We deliberately stay small and take on few projects at a time. Work is organised in pods — two to four engineers, a designer, and a lead — that own one product end to end. No pool of interchangeable resources, no context-switching between five clients a day.</p>
            <p>We're remote-first and async by default, which keeps our hiring bar about talent rather than geography, and keeps our writing habit strong. The documentation you receive is the same documentation we run on.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Values</p>
          <h2>Four words we hire and fire by.</h2>
        </div>
        <div class="grid grid-4">
          <article class="card reveal">
            <h3>Clarity</h3>
            <p>Plain language in proposals, estimates, and code review. If we can't explain it simply, we don't understand it yet.</p>
          </article>
          <article class="card reveal" style="--d:.06s">
            <h3>Craft</h3>
            <p>The parts nobody sees — tests, naming, error states — are built like the parts everybody sees.</p>
          </article>
          <article class="card reveal" style="--d:.12s">
            <h3>Ownership</h3>
            <p>We act like it's our product and our pager. Problems get raised by the person who found them, the day they're found.</p>
          </article>
          <article class="card reveal" style="--d:.18s">
            <h3>Momentum</h3>
            <p>Something real ships every week. Small steps, relentlessly — that's how orbits are reached.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tight">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Drawing the line</p>
          <h2>What we won't do.</h2>
        </div>
        <div class="grid grid-2">
          <div class="step reveal"><h3>Sell you a team we won't send</h3><p>The engineers in the proposal are the engineers in the repository. Bait-and-switch staffing is the industry habit we exist to break.</p></div>
          <div class="step reveal" style="--d:.06s"><h3>Build before we understand</h3><p>If the why isn't clear, we'll say so and start with discovery — even when a bigger contract was on the table.</p></div>
          <div class="step reveal"><h3>Lock you in</h3><p>No proprietary frameworks, no hostage repositories, no exit penalties. Leaving us should be easy; we'd rather you stay because it's working.</p></div>
          <div class="step reveal" style="--d:.06s"><h3>Go quiet</h3><p>You will never wonder what's happening with your money. A silent week is a broken promise here.</p></div>
        </div>
      </div>
    </section>

''' + cta("Sound like a team you'd work with?",
          "We'd love to hear what you're building — or, if you'd rather join us than hire us, check the open roles.",
          "Get in touch")

# ============================== CAREERS ==============================
def role(title, chips, blurb, resp, req):
    ch = "".join(f'<span class="chip">{c}</span>' for c in chips)
    rl = "\n                ".join(f"<li>{r}</li>" for r in resp)
    ql = "\n                ".join(f"<li>{r}</li>" for r in req)
    subject = title.replace(" ", "%20")
    return f'''          <article class="role reveal">
            <div>
              <h3>{title}</h3>
              <div class="meta">{ch}</div>
              <p>{blurb}</p>
              <details>
                <summary>What you'll do &amp; what we look for</summary>
                <ul>
                {rl}
                </ul>
                <ul>
                {ql}
                </ul>
              </details>
            </div>
            <a class="btn btn-sm" href="mailto:{EMAIL}?subject=Application%3A%20{subject}">Apply <span class="arrow" aria-hidden="true">→</span></a>
          </article>'''

careers_main = hero(
    "Careers",
    "Do the best work of your career, calmly.",
    "Small senior teams, a weekly shipping rhythm, and no theatre: no daily standup marathons, no growth-at-all-costs whiplash. Just interesting problems, good colleagues, and time to solve things properly."
) + f'''

    <section class="section-tight">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Life at Bytes 360</p>
          <h2>How we treat the people who build.</h2>
        </div>
        <div class="grid grid-4">
          <article class="card reveal"><h3>Remote-first</h3><p>Work from anywhere. We hire for talent and overlap hours, not postcodes.</p></article>
          <article class="card reveal" style="--d:.06s"><h3>Deep-work culture</h3><p>Async by default, meetings by exception. Your calendar is for building.</p></article>
          <article class="card reveal" style="--d:.12s"><h3>Learning budget</h3><p>Annual budget for books, courses, and conferences — plus time to actually use it.</p></article>
          <article class="card reveal" style="--d:.18s"><h3>Proper equipment</h3><p>The laptop, screen, and chair you'd choose yourself, refreshed on a sane cycle.</p></article>
          <article class="card reveal"><h3>Sustainable pace</h3><p>We plan at 80% capacity because life happens. Crunch is a planning failure, not a badge.</p></article>
          <article class="card reveal" style="--d:.06s"><h3>Real ownership</h3><p>Pods own products end to end — you talk to clients, make calls, and see the impact.</p></article>
          <article class="card reveal" style="--d:.12s"><h3>Transparent pay</h3><p>Salary bands shared in the job ad's first call, reviewed every year. No negotiation games.</p></article>
          <article class="card reveal" style="--d:.18s"><h3>Time off that's real</h3><p>Generous leave and a culture where taking it is expected, not tolerated.</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Open roles</p>
          <h2>Come build with us.</h2>
        </div>
        <div style="max-width:880px">
{role("Senior Full-Stack Engineer",
      ["Remote", "Full-time", "TypeScript · React · Node"],
      "Own features end to end on client products — from data model to pixel — inside a pod that ships every Friday.",
      ["Design, build, and review product features across the stack",
       "Lead technical conversations with clients and demo your work",
       "Raise the bar on testing, observability, and documentation"],
      ["5+ years building production web applications",
       "Fluent TypeScript; strong SQL and API design instincts",
       "Clear written communication — we work async"])}
{role("Senior Mobile Engineer",
      ["Remote", "Full-time", "Swift · Kotlin · React Native"],
      "Ship native and cross-platform apps that people rate five stars — and keep them healthy through every OS release.",
      ["Build and release iOS/Android apps through phased rollouts",
       "Advise clients on platform strategy — native vs cross-platform",
       "Own crash rates, performance, and release automation"],
      ["5+ years shipping mobile apps to the stores",
       "Depth in at least one native platform plus a cross-platform framework",
       "Experience owning releases, not just features"])}
{role("Platform / DevOps Engineer",
      ["Remote", "Full-time", "AWS · Kubernetes · Terraform"],
      "Make releases boring for every pod: infrastructure as code, pipelines with guardrails, and observability that catches issues before clients do.",
      ["Design and run cloud infrastructure across client accounts",
       "Build CI/CD pipelines, review gates, and rollback paths",
       "Wire monitoring and lead incident response practice"],
      ["4+ years in platform, SRE, or DevOps roles",
       "Strong Terraform and Kubernetes; security-first habits",
       "Calm under incident conditions — and honest in postmortems"])}
{role("Product Designer",
      ["Remote", "Full-time", "UX · UI · Prototyping"],
      "Turn fuzzy briefs into clickable prototypes clients can react to — then into design systems engineers love building from.",
      ["Run discovery interviews and translate them into flows",
       "Build prototypes and production-ready UI systems",
       "Work shoulder to shoulder with engineers through build"],
      ["4+ years designing shipped digital products",
       "A portfolio showing systems thinking, not just screens",
       "Comfort presenting to clients and defending decisions with evidence"])}
        </div>
        <p class="muted reveal" style="margin-top:22px">Nothing that fits? We keep a short bench of people we want to work with — <a href="mailto:{EMAIL}?subject=Open%20application">introduce yourself</a> anyway.</p>
      </div>
    </section>

    <section class="section section-tight">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Hiring process</p>
          <h2>Four steps, two weeks, zero hazing.</h2>
        </div>
        <div class="grid grid-4">
          <div class="step reveal"><span class="num">STEP 01</span><h3>Intro call</h3><p>Thirty minutes, mutual. You interview us as much as we interview you.</p></div>
          <div class="step reveal" style="--d:.06s"><span class="num">STEP 02</span><h3>Technical conversation</h3><p>A deep talk about real work you've shipped. No whiteboard puzzles, no trick questions.</p></div>
          <div class="step reveal" style="--d:.12s"><span class="num">STEP 03</span><h3>Paid working session</h3><p>A few hours pairing on a realistic problem — paid, and yours to keep in your portfolio.</p></div>
          <div class="step reveal" style="--d:.18s"><span class="num">STEP 04</span><h3>Offer</h3><p>A clear written offer with the salary band you already knew from step one.</p></div>
        </div>
      </div>
    </section>
'''

# ============================== CONTACT ==============================
contact_main = hero(
    "Contact",
    "Let's build something bright.",
    "Tell us about your product in a few sentences. A senior engineer — not a salesperson — reads every message and replies within two business days."
) + f'''

    <section class="section-tight">
      <div class="wrap">
        <div class="grid" style="grid-template-columns:1.5fr 1fr;gap:48px;align-items:start">
          <form id="contactForm" class="reveal" data-to="{EMAIL}" novalidate>
            <div class="form-grid">
              <div class="field">
                <label for="cName">Name <span class="req">*</span></label>
                <input id="cName" name="name" type="text" autocomplete="name" required>
              </div>
              <div class="field">
                <label for="cEmail">Work email <span class="req">*</span></label>
                <input id="cEmail" name="email" type="email" autocomplete="email" required>
              </div>
              <div class="field">
                <label for="cCompany">Company</label>
                <input id="cCompany" name="company" type="text" autocomplete="organization">
              </div>
              <div class="field">
                <label for="cType">What do you need?</label>
                <select id="cType" name="type">
                  <option>New product build</option>
                  <option>Existing product — new features</option>
                  <option>Rescue / modernise a system</option>
                  <option>Cloud &amp; DevOps help</option>
                  <option>Data &amp; AI feature</option>
                  <option>Team extension</option>
                  <option>Something else</option>
                </select>
              </div>
              <div class="field full">
                <label for="cBudget">Budget range</label>
                <select id="cBudget" name="budget">
                  <option>Still figuring it out</option>
                  <option>Under $25k</option>
                  <option>$25k – $75k</option>
                  <option>$75k – $200k</option>
                  <option>$200k+</option>
                </select>
              </div>
              <div class="field full">
                <label for="cMessage">Project details <span class="req">*</span></label>
                <textarea id="cMessage" name="message" required placeholder="What are you building, who is it for, and where are you today — idea, prototype, or live product?"></textarea>
              </div>
              <div class="full">
                <button class="btn" type="submit">Send message <span class="arrow" aria-hidden="true">→</span></button>
                <p class="form-note" id="formStatus" style="margin-top:14px">Submitting opens a pre-filled email in your mail app — nothing is stored on this site.</p>
              </div>
            </div>
          </form>

          <aside>
            <div class="card reveal" style="--d:.06s;margin-bottom:18px">
              <h3>Prefer email?</h3>
              <p>Write to us directly — same inbox, same people.</p>
              <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
            </div>
            <div class="card reveal" style="--d:.12s">
              <h3>What happens next</h3>
              <ol style="margin:0;padding-left:1.2em;color:var(--muted);font-size:.96rem;line-height:1.9">
                <li>A senior engineer replies within two business days.</li>
                <li>A 30-minute call to understand the problem — free, no deck.</li>
                <li>A written recommendation: the smallest engagement that moves you forward.</li>
              </ol>
              <p style="margin-top:14px;font-size:.9rem;color:var(--faint)">Working under wraps? Happy to sign an NDA before the call.</p>
            </div>
          </aside>
        </div>
      </div>
    </section>
'''

# ============================== 404 ==============================
notfound_main = '''    <section class="page-hero" style="min-height:62vh;display:flex;align-items:center">
      <div class="wrap" style="text-align:center">
        <p class="eyebrow" style="justify-content:center">Error 404</p>
        <h1>This byte drifted out of orbit.</h1>
        <p class="lede" style="margin-inline:auto">The page you're looking for doesn't exist — it may have been moved, renamed, or launched into deep space.</p>
        <p style="margin-top:28px">
          <a class="btn" href="index.html">Back to mission control</a>
          <a class="btn btn-ghost" href="contact.html" style="margin-left:10px">Report a broken link</a>
        </p>
      </div>
    </section>
'''

PAGES = [
    ("services.html", "Services — Bytes 360", "Custom software, web and mobile apps, cloud & DevOps, data & AI, QA & support — delivered by senior engineers with weekly demos.", services_main),
    ("process.html", "Process — Bytes 360", "How Bytes 360 takes software from discovery to launch: fixed-price discovery, weekly build cycles, monitored launches, and honest collaboration.", process_main),
    ("about.html", "About — Bytes 360", "Bytes 360 is a senior software development studio built on clarity, craft, ownership, and momentum — small pods, no lock-in, no silence.", about_main),
    ("careers.html", "Careers — Bytes 360", "Join a remote-first senior software studio: deep-work culture, sustainable pace, transparent pay, and a hiring process without hazing.", careers_main),
    ("contact.html", "Contact — Bytes 360", "Tell us what you're building. A senior engineer replies within two business days with honest first thoughts.", contact_main),
    ("404.html", "Page not found — Bytes 360", "This page drifted out of orbit. Head back to Bytes 360 mission control.", notfound_main),
]

for fname, title, desc, main in PAGES:
    path = os.path.join(ROOT, fname)
    with open(path, "w") as f:
        f.write(page(fname, title, desc, fname, main))
    print("wrote", fname)
