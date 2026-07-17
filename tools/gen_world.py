#!/usr/bin/env python3
"""Generate the Bright Byte isometric scroll-world SVG."""
import math

C, S = 0.8660254, 0.5  # iso projection constants

def P(o, x, y, z=0.0):
    return (o[0] + (x - y) * C, o[1] + (x + y) * S - z)

def fmt(pts):
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)

def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def shade(h, f):
    r, g, b = hx(h)
    def s(v):
        v = v * f
        return max(0, min(255, int(v)))
    return f"#{s(r):02x}{s(g):02x}{s(b):02x}"

OUT = []
def add(s):
    OUT.append(s)

def poly(pts, fill, opacity=None, cls=None, stroke=None):
    o = f' opacity="{opacity}"' if opacity is not None else ""
    c = f' class="{cls}"' if cls else ""
    st = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    add(f'<polygon points="{fmt(pts)}" fill="{fill}"{o}{c}{st}/>')

def box(o, x, y, w, d, h, base, z0=0.0, top_f=1.28, left_f=1.0, right_f=0.68):
    """Iso box. Front-left face is the y+d plane, right face the x+w plane."""
    t = [P(o, x, y, z0+h), P(o, x+w, y, z0+h), P(o, x+w, y+d, z0+h), P(o, x, y+d, z0+h)]
    poly([t[3], t[2], P(o, x+w, y+d, z0), P(o, x, y+d, z0)], shade(base, left_f))   # front-left
    poly([t[1], P(o, x+w, y, z0), P(o, x+w, y+d, z0), t[2]], shade(base, right_f))  # right
    poly(t, shade(base, top_f))                                                     # top
    return t

def panel_front(o, x1, x2, d, z1, z2, fill, opacity=1.0, cls=None):
    """Rect on a front-left face (y = d plane)."""
    poly([P(o, x1, d, z2), P(o, x2, d, z2), P(o, x2, d, z1), P(o, x1, d, z1)], fill, opacity, cls)

def panel_right(o, w, y1, y2, z1, z2, fill, opacity=1.0, cls=None):
    poly([P(o, w, y1, z2), P(o, w, y2, z2), P(o, w, y2, z1), P(o, w, y1, z1)], fill, opacity, cls)

def cylinder(o, x, y, r, h, base, z0=0.0, top_f=1.3, side_f=0.85):
    cxp, cyp = P(o, x, y, z0)
    ct, cty = P(o, x, y, z0 + h)
    ry = r * S
    add(f'<path d="M {cxp-r*C:.1f} {cyp:.1f} A {r*C:.1f} {ry*C:.1f} 0 0 0 {cxp+r*C:.1f} {cyp:.1f} '
        f'L {ct+r*C:.1f} {cty:.1f} A {r*C:.1f} {ry*C:.1f} 0 0 1 {ct-r*C:.1f} {cty:.1f} Z" fill="{shade(base, side_f)}"/>')
    add(f'<ellipse cx="{ct:.1f}" cy="{cty:.1f}" rx="{r*C:.1f}" ry="{ry*C:.1f}" fill="{shade(base, top_f)}"/>')
    return ct, cty

def glow(o, x, y, z, r, gid, opacity=0.5, cls=None):
    gx, gy = P(o, x, y, z)
    c = f' class="{cls}"' if cls else ""
    add(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{r}" fill="url(#{gid})" opacity="{opacity}"{c}/>')

def tree(o, x, y, scale, leaf, trunk="#5C4B3A"):
    bx, by = P(o, x, y, 0)
    th = 10 * scale
    add(f'<rect x="{bx-2.5*scale:.1f}" y="{by-th:.1f}" width="{5*scale:.1f}" height="{th:.1f}" fill="{trunk}"/>')
    h = 46 * scale; r = 16 * scale
    add(f'<path d="M {bx-r:.1f} {by-th:.1f} Q {bx:.1f} {by-th-h*0.4:.1f} {bx:.1f} {by-th-h:.1f} '
        f'Q {bx:.1f} {by-th-h*0.4:.1f} {bx+r:.1f} {by-th:.1f} '
        f'A {r:.1f} {r*0.4:.1f} 0 0 1 {bx-r:.1f} {by-th:.1f} Z" fill="{leaf}"/>')
    add(f'<path d="M {bx-r:.1f} {by-th:.1f} Q {bx:.1f} {by-th-h*0.4:.1f} {bx:.1f} {by-th-h:.1f} L {bx:.1f} {by-th:.1f} Z" fill="{shade(leaf,1.25)}"/>')

# ---- palette ----
EARTH   = "#182138"
EARTH_D = "#111830"
FLOOR   = "#2A3554"
AMBER   = "#FFB627"
CYAN    = "#4CC9F0"
MINT    = "#3DDC97"
VIOLET  = "#9B8CFF"
WHITE   = "#E8ECF7"
SLATE   = "#3A4668"

def island_base(o, R, accent, gid):
    ox, oy = o
    t = R * 0.22            # rim thickness
    rx, ry = R, R * S
    # under-glow
    add(f'<ellipse cx="{ox}" cy="{oy + R*0.62:.1f}" rx="{R*1.15:.1f}" ry="{R*0.42:.1f}" fill="url(#{gid})" opacity="0.35"/>')
    # dirt cone
    tip_y = oy + R * 0.78
    add(f'<path d="M {ox-rx*0.94:.1f} {oy+t:.1f} C {ox-rx*0.5:.1f} {oy+R*0.62:.1f} {ox-rx*0.22:.1f} {tip_y:.1f} {ox:.1f} {tip_y:.1f} '
        f'C {ox+rx*0.22:.1f} {tip_y:.1f} {ox+rx*0.5:.1f} {oy+R*0.62:.1f} {ox+rx*0.94:.1f} {oy+t:.1f} Z" fill="{EARTH_D}"/>')
    # glowing crystals in dirt
    for dx, dy, s_ in ((-R*0.35, R*0.34, 9), (R*0.28, R*0.42, 7), (-R*0.05, R*0.55, 6)):
        add(f'<polygon points="{ox+dx:.1f},{oy+dy:.1f} {ox+dx+s_:.1f},{oy+dy+s_*1.6:.1f} {ox+dx:.1f},{oy+dy+s_*2.6:.1f} {ox+dx-s_:.1f},{oy+dy+s_*1.6:.1f}" fill="{accent}" opacity="0.55" class="pulse"/>')
    # rim band
    add(f'<path d="M {ox-rx:.1f} {oy:.1f} A {rx:.1f} {ry:.1f} 0 0 0 {ox+rx:.1f} {oy:.1f} '
        f'L {ox+rx:.1f} {oy+t:.1f} A {rx:.1f} {ry:.1f} 0 0 1 {ox-rx:.1f} {oy+t:.1f} Z" fill="{EARTH}"/>')
    # platform top
    add(f'<ellipse cx="{ox}" cy="{oy}" rx="{rx}" ry="{ry}" fill="{FLOOR}"/>')
    add(f'<ellipse cx="{ox}" cy="{oy}" rx="{rx*0.86:.1f}" ry="{ry*0.86:.1f}" fill="{shade(FLOOR,1.12)}"/>')
    # floating rocks below
    for dx, dy, rr in ((-R*1.12, R*0.75, 16), (R*1.05, R*0.9, 22), (R*0.55, R*1.05, 12)):
        add(f'<g class="bob"><ellipse cx="{ox+dx:.1f}" cy="{oy+dy:.1f}" rx="{rr}" ry="{rr*0.62:.1f}" fill="{EARTH}"/>'
            f'<ellipse cx="{ox+dx:.1f}" cy="{oy+dy-rr*0.28:.1f}" rx="{rr*0.8:.1f}" ry="{rr*0.4:.1f}" fill="{shade(EARTH,1.35)}"/></g>')

# ================= ISLAND 1 — DISCOVER (amber) =================
def discover(o):
    add(f'<g id="isl-discover">')
    island_base(o, 330, AMBER, "gAmber")
    # rug
    ox, oy = o
    add(f'<ellipse cx="{ox}" cy="{oy+8}" rx="150" ry="75" fill="{shade(FLOOR,1.28)}"/>')
    # whiteboard at back
    box(o, -60, -240, 150, 14, 108, SLATE)
    panel_front(o, -50, 80, -226, 34, 96, "#0E1526")
    # sketch lines on board
    for i, (x1, x2, z) in enumerate(((-40, 40, 84), (-40, 70, 68), (-40, 20, 52))):
        panel_front(o, x1, x2, -226, z, z+7, AMBER, 0.85 if i == 0 else 0.5)
    # round strategy table + hologram
    cylinder(o, 0, 0, 78, 34, "#4A5578")
    glow(o, 0, 0, 60, 95, "gAmber", 0.6, "pulse")
    for i, (bx, bh) in enumerate(((-30, 34), (-6, 56), (18, 44))):
        box(o, bx, -8, 16, 16, bh, AMBER, z0=36, top_f=1.45, left_f=1.0, right_f=0.75)
    t1 = P(o, 0, 0, 96)
    add(f'<ellipse cx="{t1[0]:.1f}" cy="{t1[1]:.1f}" rx="70" ry="24" fill="none" stroke="{AMBER}" stroke-width="2.5" stroke-dasharray="10 8" opacity="0.8" class="spin-dash"/>')
    # benches
    box(o, -150, 60, 90, 26, 24, "#6B5A8E")
    box(o, 70, 110, 90, 26, 24, "#6B5A8E")
    # telescope on tripod at front-right
    tx, ty = P(o, 190, 60, 0)
    add(f'<path d="M {tx} {ty} l -14 -46 m 14 46 l 15 -45 m -15 45 l 1 -50" stroke="{SLATE}" stroke-width="4" fill="none"/>')
    add(f'<g transform="rotate(-28 {tx} {ty-52})"><rect x="{tx-26}" y="{ty-60}" width="52" height="14" rx="7" fill="{shade(VIOLET,0.9)}"/><circle cx="{tx+26}" cy="{ty-53}" r="7" fill="{AMBER}" class="pulse"/></g>')
    # trees
    tree(o, -230, -60, 1.0, "#2E9E6B"); tree(o, -260, 20, 0.75, "#37B87E"); tree(o, 150, -170, 0.85, "#2E9E6B")
    # signal mast
    mx, my = P(o, -160, -160, 0)
    add(f'<line x1="{mx}" y1="{my}" x2="{mx}" y2="{my-92}" stroke="{SLATE}" stroke-width="5"/>')
    for rr in (10, 18, 26):
        add(f'<path d="M {mx-rr} {my-92} a {rr} {rr} 0 0 1 {rr*2} 0" fill="none" stroke="{AMBER}" stroke-width="2.5" opacity="{1.1-rr*0.03:.2f}" class="pulse"/>')
    add('</g>')

# ================= ISLAND 2 — DESIGN (violet) =================
def design(o):
    add(f'<g id="isl-design">')
    island_base(o, 330, VIOLET, "gViolet")
    ox, oy = o
    # big artboard
    box(o, -40, -250, 190, 16, 140, SLATE)
    panel_front(o, -28, 138, -234, 24, 128, "#0E1526")
    # wireframe on artboard
    panel_front(o, -16, 126, -234, 104, 118, VIOLET, 0.75)
    panel_front(o, -16, 52, -234, 58, 96, VIOLET, 0.4)
    panel_front(o, 62, 126, -234, 58, 96, VIOLET, 0.25)
    for z in (44, 34):
        panel_front(o, -16, 110, -234, z, z+5, WHITE, 0.35)
    glow(o, 55, -240, 80, 110, "gViolet", 0.5, "pulse")
    # two desks with monitors
    for dx, dy in ((-170, -40), (-40, 40)):
        box(o, dx, dy, 100, 46, 34, "#4A5578")
        box(o, dx+20, dy+6, 56, 8, 40, SLATE, z0=34)
        panel_front(o, dx+24, dx+72, dy+14, 44, 68, VIOLET, 0.9)
    # swatch tiles on floor
    for i, (sx, sy, col) in enumerate(((120, 20, AMBER), (160, 60, CYAN), (120, 100, MINT), (80, 60, VIOLET))):
        box(o, sx, sy, 30, 30, 8, col, top_f=1.1, left_f=0.8, right_f=0.55)
    # floating pen-tool crystal
    px, py = P(o, 150, -120, 120)
    add(f'<g class="bob"><polygon points="{px},{py-34} {px+20},{py} {px},{py+34} {px-20},{py}" fill="{VIOLET}"/>'
        f'<polygon points="{px},{py-34} {px+20},{py} {px},{py+8} Z" fill="{shade(VIOLET,1.3)}"/>'
        f'<circle cx="{px}" cy="{py}" r="52" fill="url(#gViolet)" opacity="0.55" class="pulse"/></g>')
    # lamp
    lx, ly = P(o, -230, 120, 0)
    add(f'<line x1="{lx}" y1="{ly}" x2="{lx}" y2="{ly-80}" stroke="{SLATE}" stroke-width="5"/>'
        f'<circle cx="{lx}" cy="{ly-88}" r="9" fill="{AMBER}" class="pulse"/><circle cx="{lx}" cy="{ly-88}" r="30" fill="url(#gAmber)" opacity="0.5"/>')
    tree(o, 230, -60, 0.8, "#37B87E")
    add('</g>')

# ================= ISLAND 3 — BUILD (cyan) =================
def build_isl(o):
    add(f'<g id="isl-build">')
    island_base(o, 360, CYAN, "gCyan")
    # server racks
    for i, (rx_, ry_) in enumerate(((-250, -120), (-190, -160), (-130, -200))):
        box(o, rx_, ry_, 52, 52, 150, "#39456B")
        for row in range(5):
            z = 24 + row * 26
            panel_front(o, rx_+8, rx_+44, ry_+52, z, z+9, "#0E1526")
            gx, gy = P(o, rx_+14, ry_+52, z+5)
            add(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="3.4" fill="{CYAN}" class="blink b{(i+row) % 3}"/>')
            gx2, gy2 = P(o, rx_+24, ry_+52, z+5)
            add(f'<circle cx="{gx2:.1f}" cy="{gy2:.1f}" r="3.4" fill="{MINT}" class="blink b{(i+row+1) % 3}"/>')
    # conveyor
    box(o, -60, 20, 300, 60, 26, "#4A5578")
    top = [P(o, -52, 26, 26), P(o, 232, 26, 26), P(o, 232, 74, 26), P(o, -52, 74, 26)]
    poly(top, "#222B47")
    for i in range(6):
        x = -40 + i * 46
        a, b = P(o, x, 26, 26), P(o, x, 74, 26)
        add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{shade("#222B47",1.6)}" stroke-width="2"/>')
    # glowing byte-cubes riding the belt
    for x, col in ((-20, CYAN), (80, AMBER), (180, MINT)):
        box(o, x, 34, 30, 30, 30, col, z0=26, top_f=1.35, left_f=0.95, right_f=0.65)
        glow(o, x+15, 49, 60, 46, "gCyan" if col == CYAN else ("gAmber" if col == AMBER else "gMint"), 0.45, "pulse")
    # gantry crane over the belt
    box(o, 40, -6, 18, 18, 110, SLATE)
    box(o, 40, 86, 18, 18, 110, SLATE)
    box(o, 36, -6, 26, 110, 14, "#39456B", z0=110)
    hookx, hooky = P(o, 49, 50, 108)
    add(f'<line x1="{hookx:.1f}" y1="{hooky:.1f}" x2="{hookx:.1f}" y2="{hooky+34:.1f}" stroke="{WHITE}" stroke-width="2" opacity="0.6"/>'
        f'<rect x="{hookx-9:.1f}" y="{hooky+34:.1f}" width="18" height="14" fill="{AMBER}" class="pulse"/>')
    # terminal station
    box(o, 130, -170, 120, 50, 36, "#4A5578")
    box(o, 138, -166, 104, 10, 62, SLATE, z0=36)
    panel_front(o, 144, 236, -156, 46, 92, "#0E1526")
    for j, (x1, x2, z) in enumerate(((150, 200, 82), (150, 224, 72), (150, 186, 62), (150, 214, 52))):
        panel_front(o, x1, x2, -156, z, z+5, CYAN if j % 2 == 0 else MINT, 0.8)
    glow(o, 190, -160, 70, 80, "gCyan", 0.5, "pulse")
    tree(o, 280, 40, 0.8, "#2E9E6B"); tree(o, -280, 60, 0.9, "#37B87E")
    add('</g>')

# ================= ISLAND 4 — LAUNCH (mint) =================
def launch(o):
    add(f'<g id="isl-launch">')
    island_base(o, 350, MINT, "gMint")
    ox, oy = o
    # pad
    cylinder(o, 40, 40, 120, 18, "#39456B")
    px_, py_ = P(o, 40, 40, 18)
    add(f'<ellipse cx="{px_:.1f}" cy="{py_:.1f}" rx="{86*C:.1f}" ry="{86*C*S:.1f}" fill="none" stroke="{MINT}" stroke-width="3" opacity="0.6" class="pulse"/>')
    # rocket
    rx_, ry_ = P(o, 40, 40, 18)
    bw, bh = 34, 120
    add(f'<g class="bob-slow">')
    add(f'<path d="M {rx_-bw:.1f} {ry_-8:.1f} L {rx_-bw:.1f} {ry_-8-bh:.1f} '
        f'Q {rx_:.1f} {ry_-30-bh:.1f} {rx_+bw:.1f} {ry_-8-bh:.1f} L {rx_+bw:.1f} {ry_-8:.1f} '
        f'A {bw} {bw*0.42:.1f} 0 0 1 {rx_-bw:.1f} {ry_-8:.1f} Z" fill="{WHITE}"/>')
    add(f'<path d="M {rx_:.1f} {ry_-8:.1f} L {rx_:.1f} {ry_-24-bh:.1f} Q {rx_+bw*0.9:.1f} {ry_-16-bh:.1f} {rx_+bw:.1f} {ry_-8-bh:.1f} L {rx_+bw:.1f} {ry_-8:.1f} A {bw} {bw*0.42:.1f} 0 0 1 {rx_:.1f} {ry_-8:.1f} Z" fill="{shade(WHITE,0.82)}"/>')
    add(f'<path d="M {rx_-bw:.1f} {ry_-8-bh:.1f} Q {rx_:.1f} {ry_-30-bh:.1f} {rx_+bw:.1f} {ry_-8-bh:.1f} '
        f'Q {rx_:.1f} {ry_-2-bh-58:.1f} {rx_-bw:.1f} {ry_-8-bh:.1f} Z" fill="{AMBER}"/>')
    add(f'<circle cx="{rx_:.1f}" cy="{ry_-52-bh*0.45:.1f}" r="13" fill="{CYAN}" stroke="{shade(WHITE,0.7)}" stroke-width="4"/>')
    add(f'<path d="M {rx_-bw:.1f} {ry_-40:.1f} L {rx_-bw-22:.1f} {ry_+6:.1f} L {rx_-bw:.1f} {ry_-4:.1f} Z" fill="{AMBER}"/>')
    add(f'<path d="M {rx_+bw:.1f} {ry_-40:.1f} L {rx_+bw+22:.1f} {ry_+6:.1f} L {rx_+bw:.1f} {ry_-4:.1f} Z" fill="{shade(AMBER,0.8)}"/>')
    add(f'<ellipse cx="{rx_:.1f}" cy="{ry_+2:.1f}" rx="18" ry="8" fill="{AMBER}" class="pulse"/>')
    add(f'<circle cx="{rx_:.1f}" cy="{ry_+6:.1f}" r="46" fill="url(#gAmber)" opacity="0.55" class="pulse"/>')
    add('</g>')
    # gantry tower
    box(o, -90, -60, 26, 26, 190, SLATE)
    for z in (60, 110, 160):
        a = P(o, -77, -47, z); b = (rx_ - 40, ry_ - z * 0.9)
        add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{SLATE}" stroke-width="4"/>')
    # mission control console
    box(o, -220, 90, 130, 56, 40, "#4A5578")
    box(o, -212, 96, 114, 12, 58, SLATE, z0=40)
    panel_front(o, -206, -110, 108, 48, 88, "#0E1526")
    for j, (x1, x2, z) in enumerate(((-198, -160, 76), (-198, -134, 64), (-198, -172, 52))):
        panel_front(o, x1, x2, 108, z, z+6, MINT, 0.85)
    glow(o, -155, 100, 66, 76, "gMint", 0.5, "pulse")
    # radar dish
    dx_, dy_ = P(o, 170, -150, 0)
    box(o, 155, -165, 30, 30, 26, "#39456B")
    add(f'<line x1="{dx_:.1f}" y1="{dy_-26:.1f}" x2="{dx_:.1f}" y2="{dy_-58:.1f}" stroke="{SLATE}" stroke-width="5"/>')
    add(f'<g transform="rotate(-32 {dx_:.1f} {dy_-64:.1f})"><ellipse cx="{dx_:.1f}" cy="{dy_-64:.1f}" rx="34" ry="13" fill="{shade(SLATE,1.35)}"/>'
        f'<line x1="{dx_:.1f}" y1="{dy_-64:.1f}" x2="{dx_:.1f}" y2="{dy_-84:.1f}" stroke="{MINT}" stroke-width="3"/>'
        f'<circle cx="{dx_:.1f}" cy="{dy_-86:.1f}" r="5" fill="{MINT}" class="pulse"/></g>')
    # flag
    fx, fy = P(o, 240, 60, 0)
    add(f'<line x1="{fx}" y1="{fy}" x2="{fx}" y2="{fy-70}" stroke="{SLATE}" stroke-width="4"/>'
        f'<path d="M {fx} {fy-70} L {fx+42} {fy-60} L {fx} {fy-50} Z" fill="{AMBER}"/>')
    tree(o, -270, -40, 0.85, "#37B87E")
    add('</g>')

# ================= COMPOSE =================
I1, I2, I3, I4 = (650, 520), (2080, 760), (1000, 1520), (2420, 1800)

add('<defs>')
for gid, col in (("gAmber", AMBER), ("gCyan", CYAN), ("gMint", MINT), ("gViolet", VIOLET)):
    add(f'<radialGradient id="{gid}"><stop offset="0%" stop-color="{col}" stop-opacity="0.85"/>'
        f'<stop offset="45%" stop-color="{col}" stop-opacity="0.28"/>'
        f'<stop offset="100%" stop-color="{col}" stop-opacity="0"/></radialGradient>')
add(f'<linearGradient id="gRoute" x1="0" y1="0" x2="1" y2="1">'
    f'<stop offset="0%" stop-color="{AMBER}"/><stop offset="38%" stop-color="{VIOLET}"/>'
    f'<stop offset="66%" stop-color="{CYAN}"/><stop offset="100%" stop-color="{MINT}"/></linearGradient>')
add('</defs>')

# flight route (behind islands)
route = (f'M {I1[0]+180} {I1[1]+60} C {I1[0]+700} {I1[1]-160}, {I2[0]-620} {I2[1]-360}, {I2[0]-60} {I2[1]-120} '
         f'S {I2[0]-160} {I2[1]+520}, {I3[0]+340} {I3[1]-220} '
         f'S {I3[0]+300} {I3[1]+420}, {I4[0]-220} {I4[1]-60}')
add(f'<path d="{route}" fill="none" stroke="url(#gRoute)" stroke-width="5" stroke-linecap="round" '
    f'stroke-dasharray="4 26" opacity="0.55" class="flow"/>')

# drifting mini-props between islands
for (mx, my, col) in ((1350, 480, VIOLET), (1560, 1140, CYAN), (1760, 1560, MINT), (520, 1080, CYAN), (2350, 1250, AMBER)):
    add(f'<g class="bob"><polygon points="{mx},{my-14} {mx+11},{my} {mx},{my+14} {mx-11},{my}" fill="{col}" opacity="0.75"/>'
        f'<ellipse cx="{mx}" cy="{my}" rx="24" ry="8" fill="none" stroke="{col}" stroke-width="1.6" opacity="0.4"/></g>')

discover(I1)
design(I2)
build_isl(I3)
launch(I4)

style = """<style>
  @media (prefers-reduced-motion: no-preference) {
    .bob { animation: swBob 7s ease-in-out infinite; }
    .bob-slow { animation: swBob 10s ease-in-out infinite; }
    .pulse { animation: swPulse 3.2s ease-in-out infinite; }
    .blink.b0 { animation: swBlink 2.1s steps(2) infinite; }
    .blink.b1 { animation: swBlink 2.7s steps(2) infinite 0.4s; }
    .blink.b2 { animation: swBlink 1.7s steps(2) infinite 0.9s; }
    .flow { animation: swFlow 2.6s linear infinite; }
    .spin-dash { animation: swFlow 4s linear infinite; }
  }
  @keyframes swBob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }
  @keyframes swPulse { 0%,100% { opacity: 0.9; } 50% { opacity: 0.45; } }
  @keyframes swBlink { 0%,100% { opacity: 1; } 50% { opacity: 0.15; } }
  @keyframes swFlow { to { stroke-dashoffset: -60; } }
</style>"""

svg = (f'<svg id="worldSvg" viewBox="0 0 3200 2400" width="3200" height="2400" '
       f'xmlns="http://www.w3.org/2000/svg" role="img" '
       f'aria-label="Isometric illustration of the Bright Byte delivery journey: four floating islands for discovery, design, engineering, and launch, connected by a glowing flight path.">'
       + style + "".join(OUT) + "</svg>")

with open("world.svg", "w") as f:
    f.write(svg)
print(f"world.svg written: {len(svg)/1024:.1f} KB")
