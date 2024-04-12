const {
  SvelteComponent: Dn,
  assign: zn,
  create_slot: Pn,
  detach: Bn,
  element: In,
  get_all_dirty_from_scope: Un,
  get_slot_changes: Rn,
  get_spread_update: Zn,
  init: Hn,
  insert: Qn,
  safe_not_equal: Kn,
  set_dynamic_element_data: Nt,
  set_style: ee,
  toggle_class: ce,
  transition_in: fn,
  transition_out: an,
  update_slot_base: Yn
} = window.__gradio__svelte__internal;
function Gn(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), r = Pn(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], c = {};
  for (let s = 0; s < o.length; s += 1)
    c = zn(c, o[s]);
  return {
    c() {
      e = In(
        /*tag*/
        l[14]
      ), r && r.c(), Nt(
        /*tag*/
        l[14]
      )(e, c), ce(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), ce(
        e,
        "padded",
        /*padding*/
        l[6]
      ), ce(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), ce(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), ce(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), ee(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), ee(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), ee(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), ee(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), ee(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), ee(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), ee(e, "border-width", "var(--block-border-width)");
    },
    m(s, f) {
      Qn(s, e, f), r && r.m(e, null), n = !0;
    },
    p(s, f) {
      r && r.p && (!n || f & /*$$scope*/
      131072) && Yn(
        r,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? Rn(
          i,
          /*$$scope*/
          s[17],
          f,
          null
        ) : Un(
          /*$$scope*/
          s[17]
        ),
        null
      ), Nt(
        /*tag*/
        s[14]
      )(e, c = Zn(o, [
        (!n || f & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || f & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || f & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), ce(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), ce(
        e,
        "padded",
        /*padding*/
        s[6]
      ), ce(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), ce(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), ce(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), f & /*height*/
      1 && ee(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), f & /*width*/
      2 && ee(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), f & /*variant*/
      16 && ee(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), f & /*allow_overflow*/
      2048 && ee(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), f & /*scale*/
      4096 && ee(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), f & /*min_width*/
      8192 && ee(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (fn(r, s), n = !0);
    },
    o(s) {
      an(r, s), n = !1;
    },
    d(s) {
      s && Bn(e), r && r.d(s);
    }
  };
}
function Wn(l) {
  let e, t = (
    /*tag*/
    l[14] && Gn(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (fn(t, n), e = !0);
    },
    o(n) {
      an(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Jn(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: r = void 0 } = e, { width: o = void 0 } = e, { elem_id: c = "" } = e, { elem_classes: s = [] } = e, { variant: f = "solid" } = e, { border_mode: a = "base" } = e, { padding: _ = !0 } = e, { type: b = "normal" } = e, { test_id: p = void 0 } = e, { explicit_call: k = !1 } = e, { container: F = !0 } = e, { visible: D = !0 } = e, { allow_overflow: B = !0 } = e, { scale: z = null } = e, { min_width: h = 0 } = e, v = b === "fieldset" ? "fieldset" : "div";
  const m = (d) => {
    if (d !== void 0) {
      if (typeof d == "number")
        return d + "px";
      if (typeof d == "string")
        return d;
    }
  };
  return l.$$set = (d) => {
    "height" in d && t(0, r = d.height), "width" in d && t(1, o = d.width), "elem_id" in d && t(2, c = d.elem_id), "elem_classes" in d && t(3, s = d.elem_classes), "variant" in d && t(4, f = d.variant), "border_mode" in d && t(5, a = d.border_mode), "padding" in d && t(6, _ = d.padding), "type" in d && t(16, b = d.type), "test_id" in d && t(7, p = d.test_id), "explicit_call" in d && t(8, k = d.explicit_call), "container" in d && t(9, F = d.container), "visible" in d && t(10, D = d.visible), "allow_overflow" in d && t(11, B = d.allow_overflow), "scale" in d && t(12, z = d.scale), "min_width" in d && t(13, h = d.min_width), "$$scope" in d && t(17, i = d.$$scope);
  }, [
    r,
    o,
    c,
    s,
    f,
    a,
    _,
    p,
    k,
    F,
    D,
    B,
    z,
    h,
    v,
    m,
    b,
    i,
    n
  ];
}
class On extends Dn {
  constructor(e) {
    super(), Hn(this, e, Jn, Wn, Kn, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const Xn = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Et = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Xn.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: Et[e][t],
      secondary: Et[e][n]
    }
  }),
  {}
);
function Me(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Oe() {
}
function $n(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const cn = typeof window < "u";
let Lt = cn ? () => window.performance.now() : () => Date.now(), un = cn ? (l) => requestAnimationFrame(l) : Oe;
const De = /* @__PURE__ */ new Set();
function _n(l) {
  De.forEach((e) => {
    e.c(l) || (De.delete(e), e.f());
  }), De.size !== 0 && un(_n);
}
function xn(l) {
  let e;
  return De.size === 0 && un(_n), {
    promise: new Promise((t) => {
      De.add(e = { c: l, f: t });
    }),
    abort() {
      De.delete(e);
    }
  };
}
const Te = [];
function ei(l, e = Oe) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if ($n(l, c) && (l = c, t)) {
      const s = !Te.length;
      for (const f of n)
        f[1](), Te.push(f, l);
      if (s) {
        for (let f = 0; f < Te.length; f += 2)
          Te[f][0](Te[f + 1]);
        Te.length = 0;
      }
    }
  }
  function r(c) {
    i(c(l));
  }
  function o(c, s = Oe) {
    const f = [c, s];
    return n.add(f), n.size === 1 && (t = e(i, r) || Oe), c(l), () => {
      n.delete(f), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: r, subscribe: o };
}
function At(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function pt(l, e, t, n) {
  if (typeof t == "number" || At(t)) {
    const i = n - t, r = (t - e) / (l.dt || 1 / 60), o = l.opts.stiffness * i, c = l.opts.damping * r, s = (o - c) * l.inv_mass, f = (r + s) * l.dt;
    return Math.abs(f) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, At(t) ? new Date(t.getTime() + f) : t + f);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, r) => pt(l, e[r], t[r], n[r])
      );
    if (typeof t == "object") {
      const i = {};
      for (const r in t)
        i[r] = pt(l, e[r], t[r], n[r]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Tt(l, e = {}) {
  const t = ei(l), { stiffness: n = 0.15, damping: i = 0.8, precision: r = 0.01 } = e;
  let o, c, s, f = l, a = l, _ = 1, b = 0, p = !1;
  function k(D, B = {}) {
    a = D;
    const z = s = {};
    return l == null || B.hard || F.stiffness >= 1 && F.damping >= 1 ? (p = !0, o = Lt(), f = D, t.set(l = a), Promise.resolve()) : (B.soft && (b = 1 / ((B.soft === !0 ? 0.5 : +B.soft) * 60), _ = 0), c || (o = Lt(), p = !1, c = xn((h) => {
      if (p)
        return p = !1, c = null, !1;
      _ = Math.min(_ + b, 1);
      const v = {
        inv_mass: _,
        opts: F,
        settled: !0,
        dt: (h - o) * 60 / 1e3
      }, m = pt(v, f, l, a);
      return o = h, f = l, t.set(l = m), v.settled && (c = null), !v.settled;
    })), new Promise((h) => {
      c.promise.then(() => {
        z === s && h();
      });
    }));
  }
  const F = {
    set: k,
    update: (D, B) => k(D(a, l), B),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: r
  };
  return F;
}
const {
  SvelteComponent: ti,
  append: re,
  attr: P,
  component_subscribe: Ft,
  detach: li,
  element: ni,
  init: ii,
  insert: si,
  noop: jt,
  safe_not_equal: oi,
  set_style: Ge,
  svg_element: fe,
  toggle_class: Mt
} = window.__gradio__svelte__internal, { onMount: ri } = window.__gradio__svelte__internal;
function fi(l) {
  let e, t, n, i, r, o, c, s, f, a, _, b;
  return {
    c() {
      e = ni("div"), t = fe("svg"), n = fe("g"), i = fe("path"), r = fe("path"), o = fe("path"), c = fe("path"), s = fe("g"), f = fe("path"), a = fe("path"), _ = fe("path"), b = fe("path"), P(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), P(i, "fill", "#FF7C00"), P(i, "fill-opacity", "0.4"), P(i, "class", "svelte-43sxxs"), P(r, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), P(r, "fill", "#FF7C00"), P(r, "class", "svelte-43sxxs"), P(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), P(o, "fill", "#FF7C00"), P(o, "fill-opacity", "0.4"), P(o, "class", "svelte-43sxxs"), P(c, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), P(c, "fill", "#FF7C00"), P(c, "class", "svelte-43sxxs"), Ge(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), P(f, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), P(f, "fill", "#FF7C00"), P(f, "fill-opacity", "0.4"), P(f, "class", "svelte-43sxxs"), P(a, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), P(a, "fill", "#FF7C00"), P(a, "class", "svelte-43sxxs"), P(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), P(_, "fill", "#FF7C00"), P(_, "fill-opacity", "0.4"), P(_, "class", "svelte-43sxxs"), P(b, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), P(b, "fill", "#FF7C00"), P(b, "class", "svelte-43sxxs"), Ge(s, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), P(t, "viewBox", "-1200 -1200 3000 3000"), P(t, "fill", "none"), P(t, "xmlns", "http://www.w3.org/2000/svg"), P(t, "class", "svelte-43sxxs"), P(e, "class", "svelte-43sxxs"), Mt(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(p, k) {
      si(p, e, k), re(e, t), re(t, n), re(n, i), re(n, r), re(n, o), re(n, c), re(t, s), re(s, f), re(s, a), re(s, _), re(s, b);
    },
    p(p, [k]) {
      k & /*$top*/
      2 && Ge(n, "transform", "translate(" + /*$top*/
      p[1][0] + "px, " + /*$top*/
      p[1][1] + "px)"), k & /*$bottom*/
      4 && Ge(s, "transform", "translate(" + /*$bottom*/
      p[2][0] + "px, " + /*$bottom*/
      p[2][1] + "px)"), k & /*margin*/
      1 && Mt(
        e,
        "margin",
        /*margin*/
        p[0]
      );
    },
    i: jt,
    o: jt,
    d(p) {
      p && li(e);
    }
  };
}
function ai(l, e, t) {
  let n, i, { margin: r = !0 } = e;
  const o = Tt([0, 0]);
  Ft(l, o, (b) => t(1, n = b));
  const c = Tt([0, 0]);
  Ft(l, c, (b) => t(2, i = b));
  let s;
  async function f() {
    await Promise.all([o.set([125, 140]), c.set([-125, -140])]), await Promise.all([o.set([-125, 140]), c.set([125, -140])]), await Promise.all([o.set([-125, 0]), c.set([125, -0])]), await Promise.all([o.set([125, 0]), c.set([-125, 0])]);
  }
  async function a() {
    await f(), s || a();
  }
  async function _() {
    await Promise.all([o.set([125, 0]), c.set([-125, 0])]), a();
  }
  return ri(() => (_(), () => s = !0)), l.$$set = (b) => {
    "margin" in b && t(0, r = b.margin);
  }, [r, n, i, o, c];
}
class ci extends ti {
  constructor(e) {
    super(), ii(this, e, ai, fi, oi, { margin: 0 });
  }
}
const {
  SvelteComponent: ui,
  append: Ne,
  attr: ue,
  binding_callbacks: Vt,
  check_outros: dn,
  create_component: _i,
  create_slot: di,
  destroy_component: mi,
  destroy_each: mn,
  detach: L,
  element: pe,
  empty: Be,
  ensure_array_like: tt,
  get_all_dirty_from_scope: hi,
  get_slot_changes: gi,
  group_outros: hn,
  init: bi,
  insert: A,
  mount_component: pi,
  noop: wt,
  safe_not_equal: wi,
  set_data: oe,
  set_style: ye,
  space: _e,
  text: G,
  toggle_class: se,
  transition_in: ze,
  transition_out: Pe,
  update_slot_base: ki
} = window.__gradio__svelte__internal, { tick: yi } = window.__gradio__svelte__internal, { onDestroy: vi } = window.__gradio__svelte__internal, Ci = (l) => ({}), Dt = (l) => ({});
function zt(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n[40] = t, n;
}
function Pt(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n;
}
function Si(l) {
  let e, t = (
    /*i18n*/
    l[1]("common.error") + ""
  ), n, i, r;
  const o = (
    /*#slots*/
    l[29].error
  ), c = di(
    o,
    l,
    /*$$scope*/
    l[28],
    Dt
  );
  return {
    c() {
      e = pe("span"), n = G(t), i = _e(), c && c.c(), ue(e, "class", "error svelte-1yserjw");
    },
    m(s, f) {
      A(s, e, f), Ne(e, n), A(s, i, f), c && c.m(s, f), r = !0;
    },
    p(s, f) {
      (!r || f[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      s[1]("common.error") + "") && oe(n, t), c && c.p && (!r || f[0] & /*$$scope*/
      268435456) && ki(
        c,
        o,
        s,
        /*$$scope*/
        s[28],
        r ? gi(
          o,
          /*$$scope*/
          s[28],
          f,
          Ci
        ) : hi(
          /*$$scope*/
          s[28]
        ),
        Dt
      );
    },
    i(s) {
      r || (ze(c, s), r = !0);
    },
    o(s) {
      Pe(c, s), r = !1;
    },
    d(s) {
      s && (L(e), L(i)), c && c.d(s);
    }
  };
}
function qi(l) {
  let e, t, n, i, r, o, c, s, f, a = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Bt(l)
  );
  function _(h, v) {
    if (
      /*progress*/
      h[7]
    )
      return Li;
    if (
      /*queue_position*/
      h[2] !== null && /*queue_size*/
      h[3] !== void 0 && /*queue_position*/
      h[2] >= 0
    )
      return Ei;
    if (
      /*queue_position*/
      h[2] === 0
    )
      return Ni;
  }
  let b = _(l), p = b && b(l), k = (
    /*timer*/
    l[5] && Rt(l)
  );
  const F = [ji, Fi], D = [];
  function B(h, v) {
    return (
      /*last_progress_level*/
      h[15] != null ? 0 : (
        /*show_progress*/
        h[6] === "full" ? 1 : -1
      )
    );
  }
  ~(r = B(l)) && (o = D[r] = F[r](l));
  let z = !/*timer*/
  l[5] && Wt(l);
  return {
    c() {
      a && a.c(), e = _e(), t = pe("div"), p && p.c(), n = _e(), k && k.c(), i = _e(), o && o.c(), c = _e(), z && z.c(), s = Be(), ue(t, "class", "progress-text svelte-1yserjw"), se(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), se(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(h, v) {
      a && a.m(h, v), A(h, e, v), A(h, t, v), p && p.m(t, null), Ne(t, n), k && k.m(t, null), A(h, i, v), ~r && D[r].m(h, v), A(h, c, v), z && z.m(h, v), A(h, s, v), f = !0;
    },
    p(h, v) {
      /*variant*/
      h[8] === "default" && /*show_eta_bar*/
      h[18] && /*show_progress*/
      h[6] === "full" ? a ? a.p(h, v) : (a = Bt(h), a.c(), a.m(e.parentNode, e)) : a && (a.d(1), a = null), b === (b = _(h)) && p ? p.p(h, v) : (p && p.d(1), p = b && b(h), p && (p.c(), p.m(t, n))), /*timer*/
      h[5] ? k ? k.p(h, v) : (k = Rt(h), k.c(), k.m(t, null)) : k && (k.d(1), k = null), (!f || v[0] & /*variant*/
      256) && se(
        t,
        "meta-text-center",
        /*variant*/
        h[8] === "center"
      ), (!f || v[0] & /*variant*/
      256) && se(
        t,
        "meta-text",
        /*variant*/
        h[8] === "default"
      );
      let m = r;
      r = B(h), r === m ? ~r && D[r].p(h, v) : (o && (hn(), Pe(D[m], 1, 1, () => {
        D[m] = null;
      }), dn()), ~r ? (o = D[r], o ? o.p(h, v) : (o = D[r] = F[r](h), o.c()), ze(o, 1), o.m(c.parentNode, c)) : o = null), /*timer*/
      h[5] ? z && (z.d(1), z = null) : z ? z.p(h, v) : (z = Wt(h), z.c(), z.m(s.parentNode, s));
    },
    i(h) {
      f || (ze(o), f = !0);
    },
    o(h) {
      Pe(o), f = !1;
    },
    d(h) {
      h && (L(e), L(t), L(i), L(c), L(s)), a && a.d(h), p && p.d(), k && k.d(), ~r && D[r].d(h), z && z.d(h);
    }
  };
}
function Bt(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = pe("div"), ue(e, "class", "eta-bar svelte-1yserjw"), ye(e, "transform", t);
    },
    m(n, i) {
      A(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && ye(e, "transform", t);
    },
    d(n) {
      n && L(e);
    }
  };
}
function Ni(l) {
  let e;
  return {
    c() {
      e = G("processing |");
    },
    m(t, n) {
      A(t, e, n);
    },
    p: wt,
    d(t) {
      t && L(e);
    }
  };
}
function Ei(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, r, o;
  return {
    c() {
      e = G("queue: "), n = G(t), i = G("/"), r = G(
        /*queue_size*/
        l[3]
      ), o = G(" |");
    },
    m(c, s) {
      A(c, e, s), A(c, n, s), A(c, i, s), A(c, r, s), A(c, o, s);
    },
    p(c, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      c[2] + 1 + "") && oe(n, t), s[0] & /*queue_size*/
      8 && oe(
        r,
        /*queue_size*/
        c[3]
      );
    },
    d(c) {
      c && (L(e), L(n), L(i), L(r), L(o));
    }
  };
}
function Li(l) {
  let e, t = tt(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Ut(Pt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Be();
    },
    m(i, r) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, r);
      A(i, e, r);
    },
    p(i, r) {
      if (r[0] & /*progress*/
      128) {
        t = tt(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const c = Pt(i, t, o);
          n[o] ? n[o].p(c, r) : (n[o] = Ut(c), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && L(e), mn(n, i);
    }
  };
}
function It(l) {
  let e, t = (
    /*p*/
    l[38].unit + ""
  ), n, i, r = " ", o;
  function c(a, _) {
    return (
      /*p*/
      a[38].length != null ? Ti : Ai
    );
  }
  let s = c(l), f = s(l);
  return {
    c() {
      f.c(), e = _e(), n = G(t), i = G(" | "), o = G(r);
    },
    m(a, _) {
      f.m(a, _), A(a, e, _), A(a, n, _), A(a, i, _), A(a, o, _);
    },
    p(a, _) {
      s === (s = c(a)) && f ? f.p(a, _) : (f.d(1), f = s(a), f && (f.c(), f.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      a[38].unit + "") && oe(n, t);
    },
    d(a) {
      a && (L(e), L(n), L(i), L(o)), f.d(a);
    }
  };
}
function Ai(l) {
  let e = Me(
    /*p*/
    l[38].index || 0
  ) + "", t;
  return {
    c() {
      t = G(e);
    },
    m(n, i) {
      A(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Me(
        /*p*/
        n[38].index || 0
      ) + "") && oe(t, e);
    },
    d(n) {
      n && L(t);
    }
  };
}
function Ti(l) {
  let e = Me(
    /*p*/
    l[38].index || 0
  ) + "", t, n, i = Me(
    /*p*/
    l[38].length
  ) + "", r;
  return {
    c() {
      t = G(e), n = G("/"), r = G(i);
    },
    m(o, c) {
      A(o, t, c), A(o, n, c), A(o, r, c);
    },
    p(o, c) {
      c[0] & /*progress*/
      128 && e !== (e = Me(
        /*p*/
        o[38].index || 0
      ) + "") && oe(t, e), c[0] & /*progress*/
      128 && i !== (i = Me(
        /*p*/
        o[38].length
      ) + "") && oe(r, i);
    },
    d(o) {
      o && (L(t), L(n), L(r));
    }
  };
}
function Ut(l) {
  let e, t = (
    /*p*/
    l[38].index != null && It(l)
  );
  return {
    c() {
      t && t.c(), e = Be();
    },
    m(n, i) {
      t && t.m(n, i), A(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[38].index != null ? t ? t.p(n, i) : (t = It(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && L(e), t && t.d(n);
    }
  };
}
function Rt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = G(
        /*formatted_timer*/
        l[20]
      ), n = G(t), i = G("s");
    },
    m(r, o) {
      A(r, e, o), A(r, n, o), A(r, i, o);
    },
    p(r, o) {
      o[0] & /*formatted_timer*/
      1048576 && oe(
        e,
        /*formatted_timer*/
        r[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      r[0] ? `/${/*formatted_eta*/
      r[19]}` : "") && oe(n, t);
    },
    d(r) {
      r && (L(e), L(n), L(i));
    }
  };
}
function Fi(l) {
  let e, t;
  return e = new ci({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      _i(e.$$.fragment);
    },
    m(n, i) {
      pi(e, n, i), t = !0;
    },
    p(n, i) {
      const r = {};
      i[0] & /*variant*/
      256 && (r.margin = /*variant*/
      n[8] === "default"), e.$set(r);
    },
    i(n) {
      t || (ze(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Pe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      mi(e, n);
    }
  };
}
function ji(l) {
  let e, t, n, i, r, o = `${/*last_progress_level*/
  l[15] * 100}%`, c = (
    /*progress*/
    l[7] != null && Zt(l)
  );
  return {
    c() {
      e = pe("div"), t = pe("div"), c && c.c(), n = _e(), i = pe("div"), r = pe("div"), ue(t, "class", "progress-level-inner svelte-1yserjw"), ue(r, "class", "progress-bar svelte-1yserjw"), ye(r, "width", o), ue(i, "class", "progress-bar-wrap svelte-1yserjw"), ue(e, "class", "progress-level svelte-1yserjw");
    },
    m(s, f) {
      A(s, e, f), Ne(e, t), c && c.m(t, null), Ne(e, n), Ne(e, i), Ne(i, r), l[30](r);
    },
    p(s, f) {
      /*progress*/
      s[7] != null ? c ? c.p(s, f) : (c = Zt(s), c.c(), c.m(t, null)) : c && (c.d(1), c = null), f[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      s[15] * 100}%`) && ye(r, "width", o);
    },
    i: wt,
    o: wt,
    d(s) {
      s && L(e), c && c.d(), l[30](null);
    }
  };
}
function Zt(l) {
  let e, t = tt(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Gt(zt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Be();
    },
    m(i, r) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, r);
      A(i, e, r);
    },
    p(i, r) {
      if (r[0] & /*progress_level, progress*/
      16512) {
        t = tt(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const c = zt(i, t, o);
          n[o] ? n[o].p(c, r) : (n[o] = Gt(c), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && L(e), mn(n, i);
    }
  };
}
function Ht(l) {
  let e, t, n, i, r = (
    /*i*/
    l[40] !== 0 && Mi()
  ), o = (
    /*p*/
    l[38].desc != null && Qt(l)
  ), c = (
    /*p*/
    l[38].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null && Kt()
  ), s = (
    /*progress_level*/
    l[14] != null && Yt(l)
  );
  return {
    c() {
      r && r.c(), e = _e(), o && o.c(), t = _e(), c && c.c(), n = _e(), s && s.c(), i = Be();
    },
    m(f, a) {
      r && r.m(f, a), A(f, e, a), o && o.m(f, a), A(f, t, a), c && c.m(f, a), A(f, n, a), s && s.m(f, a), A(f, i, a);
    },
    p(f, a) {
      /*p*/
      f[38].desc != null ? o ? o.p(f, a) : (o = Qt(f), o.c(), o.m(t.parentNode, t)) : o && (o.d(1), o = null), /*p*/
      f[38].desc != null && /*progress_level*/
      f[14] && /*progress_level*/
      f[14][
        /*i*/
        f[40]
      ] != null ? c || (c = Kt(), c.c(), c.m(n.parentNode, n)) : c && (c.d(1), c = null), /*progress_level*/
      f[14] != null ? s ? s.p(f, a) : (s = Yt(f), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(f) {
      f && (L(e), L(t), L(n), L(i)), r && r.d(f), o && o.d(f), c && c.d(f), s && s.d(f);
    }
  };
}
function Mi(l) {
  let e;
  return {
    c() {
      e = G(" /");
    },
    m(t, n) {
      A(t, e, n);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Qt(l) {
  let e = (
    /*p*/
    l[38].desc + ""
  ), t;
  return {
    c() {
      t = G(e);
    },
    m(n, i) {
      A(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[38].desc + "") && oe(t, e);
    },
    d(n) {
      n && L(t);
    }
  };
}
function Kt(l) {
  let e;
  return {
    c() {
      e = G("-");
    },
    m(t, n) {
      A(t, e, n);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Yt(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[40]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = G(e), n = G("%");
    },
    m(i, r) {
      A(i, t, r), A(i, n, r);
    },
    p(i, r) {
      r[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && oe(t, e);
    },
    d(i) {
      i && (L(t), L(n));
    }
  };
}
function Gt(l) {
  let e, t = (
    /*p*/
    (l[38].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null) && Ht(l)
  );
  return {
    c() {
      t && t.c(), e = Be();
    },
    m(n, i) {
      t && t.m(n, i), A(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[38].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[40]
      ] != null ? t ? t.p(n, i) : (t = Ht(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && L(e), t && t.d(n);
    }
  };
}
function Wt(l) {
  let e, t;
  return {
    c() {
      e = pe("p"), t = G(
        /*loading_text*/
        l[9]
      ), ue(e, "class", "loading svelte-1yserjw");
    },
    m(n, i) {
      A(n, e, i), Ne(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && oe(
        t,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && L(e);
    }
  };
}
function Vi(l) {
  let e, t, n, i, r;
  const o = [qi, Si], c = [];
  function s(f, a) {
    return (
      /*status*/
      f[4] === "pending" ? 0 : (
        /*status*/
        f[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(l)) && (n = c[t] = o[t](l)), {
    c() {
      e = pe("div"), n && n.c(), ue(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1yserjw"), se(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), se(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), se(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), se(
        e,
        "border",
        /*border*/
        l[12]
      ), ye(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), ye(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(f, a) {
      A(f, e, a), ~t && c[t].m(e, null), l[31](e), r = !0;
    },
    p(f, a) {
      let _ = t;
      t = s(f), t === _ ? ~t && c[t].p(f, a) : (n && (hn(), Pe(c[_], 1, 1, () => {
        c[_] = null;
      }), dn()), ~t ? (n = c[t], n ? n.p(f, a) : (n = c[t] = o[t](f), n.c()), ze(n, 1), n.m(e, null)) : n = null), (!r || a[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      f[8] + " " + /*show_progress*/
      f[6] + " svelte-1yserjw")) && ue(e, "class", i), (!r || a[0] & /*variant, show_progress, status, show_progress*/
      336) && se(e, "hide", !/*status*/
      f[4] || /*status*/
      f[4] === "complete" || /*show_progress*/
      f[6] === "hidden"), (!r || a[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && se(
        e,
        "translucent",
        /*variant*/
        f[8] === "center" && /*status*/
        (f[4] === "pending" || /*status*/
        f[4] === "error") || /*translucent*/
        f[11] || /*show_progress*/
        f[6] === "minimal"
      ), (!r || a[0] & /*variant, show_progress, status*/
      336) && se(
        e,
        "generating",
        /*status*/
        f[4] === "generating"
      ), (!r || a[0] & /*variant, show_progress, border*/
      4416) && se(
        e,
        "border",
        /*border*/
        f[12]
      ), a[0] & /*absolute*/
      1024 && ye(
        e,
        "position",
        /*absolute*/
        f[10] ? "absolute" : "static"
      ), a[0] & /*absolute*/
      1024 && ye(
        e,
        "padding",
        /*absolute*/
        f[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(f) {
      r || (ze(n), r = !0);
    },
    o(f) {
      Pe(n), r = !1;
    },
    d(f) {
      f && L(e), ~t && c[t].d(), l[31](null);
    }
  };
}
let We = [], gt = !1;
async function Di(l, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (We.push(l), !gt)
      gt = !0;
    else
      return;
    await yi(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let n = 0; n < We.length; n++) {
        const r = We[n].getBoundingClientRect();
        (n === 0 || r.top + window.scrollY <= t[0]) && (t[0] = r.top + window.scrollY, t[1] = n);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), gt = !1, We = [];
    });
  }
}
function zi(l, e, t) {
  let n, { $$slots: i = {}, $$scope: r } = e, { i18n: o } = e, { eta: c = null } = e, { queue_position: s } = e, { queue_size: f } = e, { status: a } = e, { scroll_to_output: _ = !1 } = e, { timer: b = !0 } = e, { show_progress: p = "full" } = e, { message: k = null } = e, { progress: F = null } = e, { variant: D = "default" } = e, { loading_text: B = "Loading..." } = e, { absolute: z = !0 } = e, { translucent: h = !1 } = e, { border: v = !1 } = e, { autoscroll: m } = e, d, y = !1, S = 0, j = 0, I = null, T = null, H = 0, Z = null, E, N = null, V = !0;
  const rt = () => {
    t(0, c = t(26, I = t(19, Ae = null))), t(24, S = performance.now()), t(25, j = 0), y = !0, Ie();
  };
  function Ie() {
    requestAnimationFrame(() => {
      t(25, j = (performance.now() - S) / 1e3), y && Ie();
    });
  }
  function Ue() {
    t(25, j = 0), t(0, c = t(26, I = t(19, Ae = null))), y && (y = !1);
  }
  vi(() => {
    y && Ue();
  });
  let Ae = null;
  function ft(C) {
    Vt[C ? "unshift" : "push"](() => {
      N = C, t(16, N), t(7, F), t(14, Z), t(15, E);
    });
  }
  function Ye(C) {
    Vt[C ? "unshift" : "push"](() => {
      d = C, t(13, d);
    });
  }
  return l.$$set = (C) => {
    "i18n" in C && t(1, o = C.i18n), "eta" in C && t(0, c = C.eta), "queue_position" in C && t(2, s = C.queue_position), "queue_size" in C && t(3, f = C.queue_size), "status" in C && t(4, a = C.status), "scroll_to_output" in C && t(21, _ = C.scroll_to_output), "timer" in C && t(5, b = C.timer), "show_progress" in C && t(6, p = C.show_progress), "message" in C && t(22, k = C.message), "progress" in C && t(7, F = C.progress), "variant" in C && t(8, D = C.variant), "loading_text" in C && t(9, B = C.loading_text), "absolute" in C && t(10, z = C.absolute), "translucent" in C && t(11, h = C.translucent), "border" in C && t(12, v = C.border), "autoscroll" in C && t(23, m = C.autoscroll), "$$scope" in C && t(28, r = C.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (c === null && t(0, c = I), c != null && I !== c && (t(27, T = (performance.now() - S) / 1e3 + c), t(19, Ae = T.toFixed(1)), t(26, I = c))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && t(17, H = T === null || T <= 0 || !j ? null : Math.min(j / T, 1)), l.$$.dirty[0] & /*progress*/
    128 && F != null && t(18, V = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (F != null ? t(14, Z = F.map((C) => {
      if (C.index != null && C.length != null)
        return C.index / C.length;
      if (C.progress != null)
        return C.progress;
    })) : t(14, Z = null), Z ? (t(15, E = Z[Z.length - 1]), N && (E === 0 ? t(16, N.style.transition = "0", N) : t(16, N.style.transition = "150ms", N))) : t(15, E = void 0)), l.$$.dirty[0] & /*status*/
    16 && (a === "pending" ? rt() : Ue()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && d && _ && (a === "pending" || a === "complete") && Di(d, m), l.$$.dirty[0] & /*status, message*/
    4194320, l.$$.dirty[0] & /*timer_diff*/
    33554432 && t(20, n = j.toFixed(1));
  }, [
    c,
    o,
    s,
    f,
    a,
    b,
    p,
    F,
    D,
    B,
    z,
    h,
    v,
    d,
    Z,
    E,
    N,
    H,
    V,
    Ae,
    n,
    _,
    k,
    m,
    S,
    j,
    I,
    T,
    r,
    i,
    ft,
    Ye
  ];
}
class Pi extends ui {
  constructor(e) {
    super(), bi(
      this,
      e,
      zi,
      Vi,
      wi,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Bi,
  append: Ii,
  attr: te,
  detach: Ui,
  init: Ri,
  insert: Zi,
  noop: Jt,
  safe_not_equal: Hi,
  svg_element: Ot
} = window.__gradio__svelte__internal;
function Qi(l) {
  let e, t;
  return {
    c() {
      e = Ot("svg"), t = Ot("path"), te(t, "d", "M30 28.59L22.45 21A11 11 0 1 0 21 22.45L28.59 30zM5 14a9 9 0 1 1 9 9a9 9 0 0 1-9-9z"), te(t, "fill", "currentColor"), te(
        e,
        "class",
        /*classNames*/
        l[0]
      ), te(e, "xmlns", "http://www.w3.org/2000/svg"), te(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), te(e, "aria-hidden", "true"), te(e, "focusable", "false"), te(e, "role", "img"), te(e, "width", "1em"), te(e, "height", "1em"), te(e, "preserveAspectRatio", "xMidYMid meet"), te(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      Zi(n, e, i), Ii(e, t);
    },
    p(n, [i]) {
      i & /*classNames*/
      1 && te(
        e,
        "class",
        /*classNames*/
        n[0]
      );
    },
    i: Jt,
    o: Jt,
    d(n) {
      n && Ui(e);
    }
  };
}
function Ki(l, e, t) {
  let { classNames: n = "" } = e;
  return l.$$set = (i) => {
    "classNames" in i && t(0, n = i.classNames);
  }, [n];
}
class Yi extends Bi {
  constructor(e) {
    super(), Ri(this, e, Ki, Qi, Hi, { classNames: 0 });
  }
}
const {
  SvelteComponent: Gi,
  attr: Fe,
  detach: Wi,
  element: Ji,
  init: Oi,
  insert: Xi,
  noop: Xt,
  safe_not_equal: $i,
  src_url_equal: $t
} = window.__gradio__svelte__internal;
function xi(l) {
  let e, t, n;
  return {
    c() {
      e = Ji("img"), Fe(e, "alt", ""), Fe(e, "class", t = /*SIZE_CLASS*/
      l[3][
        /*size*/
        l[2]
      ] + " " + /*author*/
      (l[0].type === "user" ? "rounded-full" : "rounded") + " " + /*classNames*/
      l[1] + " flex-none"), $t(e.src, n = /*author*/
      l[0].avatarUrl) || Fe(e, "src", n), Fe(e, "crossorigin", "anonymous");
    },
    m(i, r) {
      Xi(i, e, r);
    },
    p(i, [r]) {
      r & /*size, author, classNames*/
      7 && t !== (t = /*SIZE_CLASS*/
      i[3][
        /*size*/
        i[2]
      ] + " " + /*author*/
      (i[0].type === "user" ? "rounded-full" : "rounded") + " " + /*classNames*/
      i[1] + " flex-none") && Fe(e, "class", t), r & /*author*/
      1 && !$t(e.src, n = /*author*/
      i[0].avatarUrl) && Fe(e, "src", n);
    },
    i: Xt,
    o: Xt,
    d(i) {
      i && Wi(e);
    }
  };
}
function es(l, e, t) {
  let { author: n } = e, { classNames: i = "" } = e, { size: r = "md" } = e;
  const o = {
    xs: "w-2.5 h-2.5",
    sm: "w-3 h-3",
    md: "w-3.5 h-3.5",
    lg: "w-5 h-5",
    xl: "w-9 h-9",
    xxl: "w-24 h-24"
  };
  return l.$$set = (c) => {
    "author" in c && t(0, n = c.author), "classNames" in c && t(1, i = c.classNames), "size" in c && t(2, r = c.size);
  }, [n, i, r, o];
}
class ts extends Gi {
  constructor(e) {
    super(), Oi(this, e, es, xi, $i, { author: 0, classNames: 1, size: 2 });
  }
}
const {
  SvelteComponent: ls,
  append: ns,
  attr: le,
  detach: is,
  init: ss,
  insert: os,
  noop: xt,
  safe_not_equal: rs,
  svg_element: el
} = window.__gradio__svelte__internal;
function fs(l) {
  let e, t;
  return {
    c() {
      e = el("svg"), t = el("path"), le(t, "d", "M18 6l-1.4 1.4l7.5 7.6H3v2h21.1l-7.5 7.6L18 26l10-10z"), le(t, "fill", "currentColor"), le(
        e,
        "class",
        /*classNames*/
        l[0]
      ), le(e, "xmlns", "http://www.w3.org/2000/svg"), le(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), le(e, "aria-hidden", "true"), le(e, "focusable", "false"), le(e, "role", "img"), le(e, "width", "1em"), le(e, "height", "1em"), le(e, "preserveAspectRatio", "xMidYMid meet"), le(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      os(n, e, i), ns(e, t);
    },
    p(n, [i]) {
      i & /*classNames*/
      1 && le(
        e,
        "class",
        /*classNames*/
        n[0]
      );
    },
    i: xt,
    o: xt,
    d(n) {
      n && is(e);
    }
  };
}
function as(l, e, t) {
  let { classNames: n = "" } = e;
  return l.$$set = (i) => {
    "classNames" in i && t(0, n = i.classNames);
  }, [n];
}
class gn extends ls {
  constructor(e) {
    super(), ss(this, e, as, fs, rs, { classNames: 0 });
  }
}
const {
  SvelteComponent: cs,
  append: Se,
  attr: ae,
  check_outros: tl,
  create_component: yt,
  destroy_component: vt,
  detach: He,
  element: Ke,
  group_outros: ll,
  init: us,
  insert: Qe,
  listen: _s,
  mount_component: Ct,
  noop: kt,
  prevent_default: ds,
  safe_not_equal: ms,
  set_data: bn,
  space: Xe,
  stop_propagation: hs,
  text: St,
  transition_in: ke,
  transition_out: Ee
} = window.__gradio__svelte__internal;
function gs(l) {
  let e, t, n;
  return {
    c() {
      e = Ke("span"), t = St("new"), ae(e, "class", n = "mr-1.5 rounded px-1 text-xs leading-tight " + /*isSelected*/
      (l[1] ? "bg-white/10 text-white" : "bg-blue-500/10 text-blue-700 dark:text-blue-200"));
    },
    m(i, r) {
      Qe(i, e, r), Se(e, t);
    },
    p(i, r) {
      r & /*isSelected*/
      2 && n !== (n = "mr-1.5 rounded px-1 text-xs leading-tight " + /*isSelected*/
      (i[1] ? "bg-white/10 text-white" : "bg-blue-500/10 text-blue-700 dark:text-blue-200")) && ae(e, "class", n);
    },
    i: kt,
    o: kt,
    d(i) {
      i && He(e);
    }
  };
}
function bs(l) {
  let e, t;
  return e = new ts({
    props: {
      author: {
        avatarUrl: (
          /*entry*/
          l[0].imgUrl
        ),
        type: (
          /*entry*/
          l[0].type === "user" ? "user" : "org"
        )
      },
      classNames: "mr-1.5"
    }
  }), {
    c() {
      yt(e.$$.fragment);
    },
    m(n, i) {
      Ct(e, n, i), t = !0;
    },
    p(n, i) {
      const r = {};
      i & /*entry*/
      1 && (r.author = {
        avatarUrl: (
          /*entry*/
          n[0].imgUrl
        ),
        type: (
          /*entry*/
          n[0].type === "user" ? "user" : "org"
        )
      }), e.$set(r);
    },
    i(n) {
      t || (ke(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      vt(e, n);
    }
  };
}
function ps(l) {
  let e, t;
  return e = new gn({
    props: { classNames: "flex-none mr-1 h-3 w-3" }
  }), {
    c() {
      yt(e.$$.fragment);
    },
    m(n, i) {
      Ct(e, n, i), t = !0;
    },
    p: kt,
    i(n) {
      t || (ke(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      vt(e, n);
    }
  };
}
function nl(l) {
  let e, t, n, i = (
    /*entry*/
    l[0].description + ""
  ), r, o;
  return {
    c() {
      e = Ke("span"), e.textContent = "·", t = Xe(), n = Ke("span"), r = St(i), ae(e, "class", "pl-0.5 pr-1.5 text-gray-300"), ae(n, "class", o = "mr-2 truncate " + /*isSelected*/
      (l[1] ? "text-white" : "text-gray-400"));
    },
    m(c, s) {
      Qe(c, e, s), Qe(c, t, s), Qe(c, n, s), Se(n, r);
    },
    p(c, s) {
      s & /*entry*/
      1 && i !== (i = /*entry*/
      c[0].description + "") && bn(r, i), s & /*isSelected*/
      2 && o !== (o = "mr-2 truncate " + /*isSelected*/
      (c[1] ? "text-white" : "text-gray-400")) && ae(n, "class", o);
    },
    d(c) {
      c && (He(e), He(t), He(n));
    }
  };
}
function il(l) {
  let e, t;
  return e = new gn({
    props: {
      classNames: "flex-none ml-auto h-3.5 w-3.5 "
    }
  }), {
    c() {
      yt(e.$$.fragment);
    },
    m(n, i) {
      Ct(e, n, i), t = !0;
    },
    i(n) {
      t || (ke(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ee(e.$$.fragment, n), t = !1;
    },
    d(n) {
      vt(e, n);
    }
  };
}
function ws(l) {
  let e, t, n, i, r, o, c, s = (
    /*entry*/
    l[0].label + ""
  ), f, a, _, b, p, k, F, D, B;
  const z = [ps, bs, gs], h = [];
  function v(y, S) {
    return S & /*entry*/
    1 && (t = null), S & /*entry*/
    1 && (n = null), t == null && (t = !!["all-datasets", "all-models", "all-spaces"].includes(
      /*entry*/
      y[0].type
    )), t ? 0 : (n == null && (n = !!(["org", "user"].includes(
      /*entry*/
      y[0].type
    ) && /*entry*/
    y[0].imgUrl)), n ? 1 : (
      /*entry*/
      y[0].type === "full-text-search" ? 2 : -1
    ));
  }
  ~(i = v(l, -1)) && (r = h[i] = z[i](l));
  let m = (
    /*entry*/
    l[0].description && nl(l)
  ), d = (
    /*entry*/
    l[0].type === "full-text-search" && il()
  );
  return {
    c() {
      e = Ke("a"), r && r.c(), o = Xe(), c = Ke("span"), f = St(s), _ = Xe(), m && m.c(), b = Xe(), d && d.c(), ae(c, "class", a = "flex-shrink-0 truncate " + /*entry*/
      (l[0].type === "model" && !/*isSelected*/
      l[1] ? "rounded bg-gradient-to-b from-gray-50 to-gray-100 px-1 dark:from-gray-925 dark:to-gray-950" : "px-1")), ae(e, "class", p = "flex h-8 cursor-pointer items-center px-2 " + (["dataset", "model", "no-results", "space"].includes(
        /*entry*/
        l[0].type
      ) ? "font-mono text-xs" : "") + " " + (["all-datasets", "all-models", "all-spaces"].includes(
        /*entry*/
        l[0].type
      ) && !/*isSelected*/
      l[1] ? "text-gray-400" : "") + " " + /*isSelected*/
      (l[1] ? "bg-blue-500 text-white dark:bg-blue-700" : "hover:bg-gray-50 dark:hover:bg-gray-900")), ae(e, "href", k = /*entry*/
      l[0].href);
    },
    m(y, S) {
      Qe(y, e, S), ~i && h[i].m(e, null), Se(e, o), Se(e, c), Se(c, f), Se(e, _), m && m.m(e, null), Se(e, b), d && d.m(e, null), F = !0, D || (B = _s(e, "click", hs(ds(
        /*click_handler*/
        l[3]
      ))), D = !0);
    },
    p(y, [S]) {
      let j = i;
      i = v(y, S), i === j ? ~i && h[i].p(y, S) : (r && (ll(), Ee(h[j], 1, 1, () => {
        h[j] = null;
      }), tl()), ~i ? (r = h[i], r ? r.p(y, S) : (r = h[i] = z[i](y), r.c()), ke(r, 1), r.m(e, o)) : r = null), (!F || S & /*entry*/
      1) && s !== (s = /*entry*/
      y[0].label + "") && bn(f, s), (!F || S & /*entry, isSelected*/
      3 && a !== (a = "flex-shrink-0 truncate " + /*entry*/
      (y[0].type === "model" && !/*isSelected*/
      y[1] ? "rounded bg-gradient-to-b from-gray-50 to-gray-100 px-1 dark:from-gray-925 dark:to-gray-950" : "px-1"))) && ae(c, "class", a), /*entry*/
      y[0].description ? m ? m.p(y, S) : (m = nl(y), m.c(), m.m(e, b)) : m && (m.d(1), m = null), /*entry*/
      y[0].type === "full-text-search" ? d ? S & /*entry*/
      1 && ke(d, 1) : (d = il(), d.c(), ke(d, 1), d.m(e, null)) : d && (ll(), Ee(d, 1, 1, () => {
        d = null;
      }), tl()), (!F || S & /*entry, isSelected*/
      3 && p !== (p = "flex h-8 cursor-pointer items-center px-2 " + (["dataset", "model", "no-results", "space"].includes(
        /*entry*/
        y[0].type
      ) ? "font-mono text-xs" : "") + " " + (["all-datasets", "all-models", "all-spaces"].includes(
        /*entry*/
        y[0].type
      ) && !/*isSelected*/
      y[1] ? "text-gray-400" : "") + " " + /*isSelected*/
      (y[1] ? "bg-blue-500 text-white dark:bg-blue-700" : "hover:bg-gray-50 dark:hover:bg-gray-900"))) && ae(e, "class", p), (!F || S & /*entry*/
      1 && k !== (k = /*entry*/
      y[0].href)) && ae(e, "href", k);
    },
    i(y) {
      F || (ke(r), ke(d), F = !0);
    },
    o(y) {
      Ee(r), Ee(d), F = !1;
    },
    d(y) {
      y && He(e), ~i && h[i].d(), m && m.d(), d && d.d(), D = !1, B();
    }
  };
}
function ks(l, e, t) {
  let { entry: n } = e, { isSelected: i } = e, { onClick: r } = e;
  const o = () => r(n);
  return l.$$set = (c) => {
    "entry" in c && t(0, n = c.entry), "isSelected" in c && t(1, i = c.isSelected), "onClick" in c && t(2, r = c.onClick);
  }, [n, i, r, o];
}
class we extends cs {
  constructor(e) {
    super(), us(this, e, ks, ws, ms, { entry: 0, isSelected: 1, onClick: 2 });
  }
}
function ys(l) {
  let e, t = l[0], n = 1;
  for (; n < l.length; ) {
    const i = l[n], r = l[n + 1];
    if (n += 2, (i === "optionalAccess" || i === "optionalCall") && t == null)
      return;
    i === "access" || i === "optionalAccess" ? (e = t, t = r(t)) : (i === "call" || i === "optionalCall") && (t = r((...o) => t.call(e, ...o)), e = void 0);
  }
  return t;
}
function vs(l) {
  const e = new URLSearchParams();
  for (const [n, i] of Object.entries(l))
    if (i !== void 0)
      if (Array.isArray(i))
        for (const r of i)
          e.append(n, String(r));
      else
        e.set(n, String(i));
  const t = e.toString();
  return t ? `?${t}` : "";
}
async function sl(l, e) {
  try {
    return ys([l, "access", (t) => t.headers, "access", (t) => t.get, "call", (t) => t("content-type"), "optionalAccess", (t) => t.includes, "call", (t) => t("json")]) ? await l.json() : e === "blob" ? await l.blob() : await l.text();
  } catch {
    return;
  }
}
async function Cs(l, e, t = {}) {
  try {
    const n = {
      ...t.headers,
      ...t.responseType === "json" ? { Accept: "application/json" } : t.responseType === "text" ? { Accept: "text/plain" } : {}
    }, i = await fetch(e, {
      body: t.data instanceof File ? t.data : t.data ? JSON.stringify(t.data) : void 0,
      headers: n,
      method: l,
      ...t.signal ? { signal: t.signal } : {},
      ...t.credentials ? { credentials: t.credentials } : {}
    }), r = i.clone();
    if (!i.ok) {
      let s = `${i.status} ${i.statusText}`;
      const f = await sl(i);
      return typeof f == "object" && f && ("message" in f && typeof f.message == "string" ? s = f.message : "error" in f && typeof f.error == "string" && (s = f.error)), {
        aborted: !1,
        error: s,
        isError: !0,
        payload: f,
        rawResponse: r,
        statusCode: i.status
      };
    }
    const o = await sl(i, t.responseType), c = i.headers.get("Link") ? qs(i.headers.get("Link")) : void 0;
    return o !== void 0 ? {
      isError: !1,
      payload: o,
      rawResponse: r,
      statusCode: i.status,
      links: c
    } : {
      aborted: !1,
      error: t.responseType === "json" ? "Error parsing JSON" : "Error parsing server response",
      isError: !0,
      payload: o,
      rawResponse: r,
      statusCode: i.status,
      links: c
    };
  } catch (n) {
    return {
      aborted: n instanceof DOMException && n.name === "AbortError",
      error: (n instanceof TypeError || n instanceof DOMException) && n.message ? n.message : "Failed to fetch",
      isError: !0,
      payload: void 0,
      rawResponse: void 0,
      statusCode: 0
    };
  }
}
function Ss(l, e = {}) {
  return Cs("GET", l, { ...e });
}
function qs(l) {
  const e = /<(https?:[/][/][^>]+)>;\s+rel="([^"]+)"/g;
  return Object.fromEntries([...l.matchAll(e)].map(([t, n, i]) => [i, n]));
}
function Ns(l, e) {
  let t, n;
  return function(...i) {
    const r = Date.now();
    t && r < t + e ? (clearTimeout(n), n = setTimeout(function() {
      t = r, l(...i);
    }, e)) : (t = r, l(...i));
  };
}
const {
  SvelteComponent: Es,
  append: W,
  attr: Y,
  binding_callbacks: ie,
  check_outros: O,
  create_component: de,
  destroy_component: me,
  destroy_each: ve,
  detach: U,
  element: J,
  empty: Le,
  ensure_array_like: $,
  group_outros: X,
  init: Ls,
  insert: R,
  listen: Je,
  mount_component: he,
  run_all: As,
  safe_not_equal: Ts,
  set_input_value: ol,
  space: Q,
  transition_in: w,
  transition_out: q
} = window.__gradio__svelte__internal, { createEventDispatcher: Fs, onMount: js, tick: Ms } = window.__gradio__svelte__internal;
function rl(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[54] = e, n[55] = t, n;
}
function fl(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[56] = e, n[57] = t, n;
}
function al(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[58] = e, n[59] = t, n;
}
function cl(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[60] = e, n[61] = t, n;
}
function ul(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[62] = e, n[63] = t, n;
}
function _l(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[64] = e, n[65] = t, n;
}
function dl(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[66] = e, n[67] = t, n;
}
function ml(l, e, t) {
  const n = l.slice();
  return n[53] = e[t], n[68] = e, n[69] = t, n;
}
function hl(l) {
  let e, t;
  return e = new Yi({
    props: {
      classNames: "absolute left-2.5 text-gray-400 top-1/2 transform -translate-y-1/2"
    }
  }), {
    c() {
      de(e.$$.fragment);
    },
    m(n, i) {
      he(e, n, i), t = !0;
    },
    i(n) {
      t || (w(e.$$.fragment, n), t = !0);
    },
    o(n) {
      q(e.$$.fragment, n), t = !1;
    },
    d(n) {
      me(e, n);
    }
  };
}
function gl(l) {
  let e, t, n, i = (
    /*entries*/
    l[15].some(Wl)
  ), r, o = (
    /*entries*/
    l[15].some(Gl)
  ), c, s = (
    /*entries*/
    l[15].some(Yl)
  ), f, a = (
    /*entries*/
    l[15].some(Kl)
  ), _, b = (
    /*entries*/
    l[15].some(Ql)
  ), p, k = (
    /*entries*/
    l[15].some(Hl)
  ), F, D = (
    /*entries*/
    l[15].some(Zl)
  ), B, z, h = (
    /*entries*/
    l[15].some(Rl)
  ), v, m, d = !/*numResults*/
  l[16] && bl(), y = i && pl(l), S = o && yl(l), j = s && Sl(l), I = a && El(l), T = b && Tl(l), H = k && Ml(l), Z = D && zl(l), E = h && Il(l);
  return {
    c() {
      e = J("div"), t = J("ul"), d && d.c(), n = Q(), y && y.c(), r = Q(), S && S.c(), c = Q(), j && j.c(), f = Q(), I && I.c(), _ = Q(), T && T.c(), p = Q(), H && H.c(), F = Q(), Z && Z.c(), z = Q(), E && E.c(), Y(t, "class", B = "mt-1 max-h-[calc(100vh-100px)] w-full divide-y divide-gray-100 overflow-hidden overflow-y-auto rounded-lg border border-gray-100 bg-white text-sm shadow-lg dark:divide-gray-900 " + /*bodyClassNames*/
      l[2]), Y(e, "class", v = /*position*/
      l[10] + " z-40 w-full md:min-w-[24rem]");
    },
    m(N, V) {
      R(N, e, V), W(e, t), d && d.m(t, null), W(t, n), y && y.m(t, null), W(t, r), S && S.m(t, null), W(t, c), j && j.m(t, null), W(t, f), I && I.m(t, null), W(t, _), T && T.m(t, null), W(t, p), H && H.m(t, null), W(t, F), Z && Z.m(t, null), l[40](t), W(e, z), E && E.m(e, null), l[42](e), m = !0;
    },
    p(N, V) {
      /*numResults*/
      N[16] ? d && (X(), q(d, 1, 1, () => {
        d = null;
      }), O()) : d ? V[0] & /*numResults*/
      65536 && w(d, 1) : (d = bl(), d.c(), w(d, 1), d.m(t, n)), V[0] & /*entries*/
      32768 && (i = /*entries*/
      N[15].some(Wl)), i ? y ? (y.p(N, V), V[0] & /*entries*/
      32768 && w(y, 1)) : (y = pl(N), y.c(), w(y, 1), y.m(t, r)) : y && (X(), q(y, 1, 1, () => {
        y = null;
      }), O()), V[0] & /*entries*/
      32768 && (o = /*entries*/
      N[15].some(Gl)), o ? S ? (S.p(N, V), V[0] & /*entries*/
      32768 && w(S, 1)) : (S = yl(N), S.c(), w(S, 1), S.m(t, c)) : S && (X(), q(S, 1, 1, () => {
        S = null;
      }), O()), V[0] & /*entries*/
      32768 && (s = /*entries*/
      N[15].some(Yl)), s ? j ? (j.p(N, V), V[0] & /*entries*/
      32768 && w(j, 1)) : (j = Sl(N), j.c(), w(j, 1), j.m(t, f)) : j && (X(), q(j, 1, 1, () => {
        j = null;
      }), O()), V[0] & /*entries*/
      32768 && (a = /*entries*/
      N[15].some(Kl)), a ? I ? (I.p(N, V), V[0] & /*entries*/
      32768 && w(I, 1)) : (I = El(N), I.c(), w(I, 1), I.m(t, _)) : I && (X(), q(I, 1, 1, () => {
        I = null;
      }), O()), V[0] & /*entries*/
      32768 && (b = /*entries*/
      N[15].some(Ql)), b ? T ? (T.p(N, V), V[0] & /*entries*/
      32768 && w(T, 1)) : (T = Tl(N), T.c(), w(T, 1), T.m(t, p)) : T && (X(), q(T, 1, 1, () => {
        T = null;
      }), O()), V[0] & /*entries*/
      32768 && (k = /*entries*/
      N[15].some(Hl)), k ? H ? (H.p(N, V), V[0] & /*entries*/
      32768 && w(H, 1)) : (H = Ml(N), H.c(), w(H, 1), H.m(t, F)) : H && (X(), q(H, 1, 1, () => {
        H = null;
      }), O()), V[0] & /*entries*/
      32768 && (D = /*entries*/
      N[15].some(Zl)), D ? Z ? (Z.p(N, V), V[0] & /*entries*/
      32768 && w(Z, 1)) : (Z = zl(N), Z.c(), w(Z, 1), Z.m(t, null)) : Z && (X(), q(Z, 1, 1, () => {
        Z = null;
      }), O()), (!m || V[0] & /*bodyClassNames*/
      4 && B !== (B = "mt-1 max-h-[calc(100vh-100px)] w-full divide-y divide-gray-100 overflow-hidden overflow-y-auto rounded-lg border border-gray-100 bg-white text-sm shadow-lg dark:divide-gray-900 " + /*bodyClassNames*/
      N[2])) && Y(t, "class", B), V[0] & /*entries*/
      32768 && (h = /*entries*/
      N[15].some(Rl)), h ? E ? (E.p(N, V), V[0] & /*entries*/
      32768 && w(E, 1)) : (E = Il(N), E.c(), w(E, 1), E.m(e, null)) : E && (X(), q(E, 1, 1, () => {
        E = null;
      }), O()), (!m || V[0] & /*position*/
      1024 && v !== (v = /*position*/
      N[10] + " z-40 w-full md:min-w-[24rem]")) && Y(e, "class", v);
    },
    i(N) {
      m || (w(d), w(y), w(S), w(j), w(I), w(T), w(H), w(Z), w(E), m = !0);
    },
    o(N) {
      q(d), q(y), q(S), q(j), q(I), q(T), q(H), q(Z), q(E), m = !1;
    },
    d(N) {
      N && U(e), d && d.d(), y && y.d(), S && S.d(), j && j.d(), I && I.d(), T && T.d(), H && H.d(), Z && Z.d(), l[40](null), E && E.d(), l[42](null);
    }
  };
}
function bl(l) {
  let e, t;
  return e = new we({
    props: {
      entry: {
        id: "no-result",
        label: "No results found :(",
        type: "no-results"
      },
      isSelected: !1,
      onClick: zs
    }
  }), {
    c() {
      de(e.$$.fragment);
    },
    m(n, i) {
      he(e, n, i), t = !0;
    },
    i(n) {
      t || (w(e.$$.fragment, n), t = !0);
    },
    o(n) {
      q(e.$$.fragment, n), t = !1;
    },
    d(n) {
      me(e, n);
    }
  };
}
function pl(l) {
  let e, t, n, i = (
    /*showSearchType*/
    l[11] && wl()
  ), r = $(
    /*entries*/
    l[15].filter(Jl)
  ), o = [];
  for (let s = 0; s < r.length; s += 1)
    o[s] = kl(ml(l, r, s));
  const c = (s) => q(o[s], 1, 1, () => {
    o[s] = null;
  });
  return {
    c() {
      i && i.c(), e = Q();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      t = Le();
    },
    m(s, f) {
      i && i.m(s, f), R(s, e, f);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(s, f);
      R(s, t, f), n = !0;
    },
    p(s, f) {
      if (/*showSearchType*/
      s[11] ? i || (i = wl(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), f[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        r = $(
          /*entries*/
          s[15].filter(Jl)
        );
        let a;
        for (a = 0; a < r.length; a += 1) {
          const _ = ml(s, r, a);
          o[a] ? (o[a].p(_, f), w(o[a], 1)) : (o[a] = kl(_), o[a].c(), w(o[a], 1), o[a].m(t.parentNode, t));
        }
        for (X(), a = r.length; a < o.length; a += 1)
          c(a);
        O();
      }
    },
    i(s) {
      if (!n) {
        for (let f = 0; f < r.length; f += 1)
          w(o[f]);
        n = !0;
      }
    },
    o(s) {
      o = o.filter(Boolean);
      for (let f = 0; f < o.length; f += 1)
        q(o[f]);
      n = !1;
    },
    d(s) {
      s && (U(e), U(t)), i && i.d(s), ve(o, s);
    }
  };
}
function wl(l) {
  let e;
  return {
    c() {
      e = J("li"), e.textContent = "Models", Y(e, "class", "flex h-7 items-center bg-gradient-to-r from-blue-50 to-white px-2 font-semibold text-blue-800 dark:from-blue-900 dark:to-gray-950 dark:text-gray-300");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && U(e);
    }
  };
}
function kl(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding*/
    l[33](e, i)
  ), c = () => (
    /*li_binding*/
    l[33](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function yl(l) {
  let e, t, n, i = (
    /*showSearchType*/
    l[11] && vl()
  ), r = $(
    /*entries*/
    l[15].filter(Ol)
  ), o = [];
  for (let s = 0; s < r.length; s += 1)
    o[s] = Cl(dl(l, r, s));
  const c = (s) => q(o[s], 1, 1, () => {
    o[s] = null;
  });
  return {
    c() {
      i && i.c(), e = Q();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      t = Le();
    },
    m(s, f) {
      i && i.m(s, f), R(s, e, f);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(s, f);
      R(s, t, f), n = !0;
    },
    p(s, f) {
      if (/*showSearchType*/
      s[11] ? i || (i = vl(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), f[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        r = $(
          /*entries*/
          s[15].filter(Ol)
        );
        let a;
        for (a = 0; a < r.length; a += 1) {
          const _ = dl(s, r, a);
          o[a] ? (o[a].p(_, f), w(o[a], 1)) : (o[a] = Cl(_), o[a].c(), w(o[a], 1), o[a].m(t.parentNode, t));
        }
        for (X(), a = r.length; a < o.length; a += 1)
          c(a);
        O();
      }
    },
    i(s) {
      if (!n) {
        for (let f = 0; f < r.length; f += 1)
          w(o[f]);
        n = !0;
      }
    },
    o(s) {
      o = o.filter(Boolean);
      for (let f = 0; f < o.length; f += 1)
        q(o[f]);
      n = !1;
    },
    d(s) {
      s && (U(e), U(t)), i && i.d(s), ve(o, s);
    }
  };
}
function vl(l) {
  let e;
  return {
    c() {
      e = J("li"), e.textContent = "Datasets", Y(e, "class", "flex h-7 items-center bg-gradient-to-r from-red-50 to-white px-2 font-semibold text-red-800 dark:from-red-900 dark:to-gray-950 dark:text-gray-300");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && U(e);
    }
  };
}
function Cl(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding_1*/
    l[34](e, i)
  ), c = () => (
    /*li_binding_1*/
    l[34](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function Sl(l) {
  let e, t, n, i = (
    /*showSearchType*/
    l[11] && ql()
  ), r = $(
    /*entries*/
    l[15].filter(Xl)
  ), o = [];
  for (let s = 0; s < r.length; s += 1)
    o[s] = Nl(_l(l, r, s));
  const c = (s) => q(o[s], 1, 1, () => {
    o[s] = null;
  });
  return {
    c() {
      i && i.c(), e = Q();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      t = Le();
    },
    m(s, f) {
      i && i.m(s, f), R(s, e, f);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(s, f);
      R(s, t, f), n = !0;
    },
    p(s, f) {
      if (/*showSearchType*/
      s[11] ? i || (i = ql(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), f[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        r = $(
          /*entries*/
          s[15].filter(Xl)
        );
        let a;
        for (a = 0; a < r.length; a += 1) {
          const _ = _l(s, r, a);
          o[a] ? (o[a].p(_, f), w(o[a], 1)) : (o[a] = Nl(_), o[a].c(), w(o[a], 1), o[a].m(t.parentNode, t));
        }
        for (X(), a = r.length; a < o.length; a += 1)
          c(a);
        O();
      }
    },
    i(s) {
      if (!n) {
        for (let f = 0; f < r.length; f += 1)
          w(o[f]);
        n = !0;
      }
    },
    o(s) {
      o = o.filter(Boolean);
      for (let f = 0; f < o.length; f += 1)
        q(o[f]);
      n = !1;
    },
    d(s) {
      s && (U(e), U(t)), i && i.d(s), ve(o, s);
    }
  };
}
function ql(l) {
  let e;
  return {
    c() {
      e = J("li"), e.textContent = "Spaces", Y(e, "class", "flex h-7 items-center bg-gradient-to-r from-orange-50 to-white px-2 font-semibold text-orange-800 dark:from-orange-900 dark:to-gray-950 dark:text-gray-300");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && U(e);
    }
  };
}
function Nl(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding_2*/
    l[35](e, i)
  ), c = () => (
    /*li_binding_2*/
    l[35](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function El(l) {
  let e, t, n, i = (
    /*showSearchType*/
    l[11] && Ll()
  ), r = $(
    /*entries*/
    l[15].filter($l)
  ), o = [];
  for (let s = 0; s < r.length; s += 1)
    o[s] = Al(ul(l, r, s));
  const c = (s) => q(o[s], 1, 1, () => {
    o[s] = null;
  });
  return {
    c() {
      i && i.c(), e = Q();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      t = Le();
    },
    m(s, f) {
      i && i.m(s, f), R(s, e, f);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(s, f);
      R(s, t, f), n = !0;
    },
    p(s, f) {
      if (/*showSearchType*/
      s[11] ? i || (i = Ll(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), f[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        r = $(
          /*entries*/
          s[15].filter($l)
        );
        let a;
        for (a = 0; a < r.length; a += 1) {
          const _ = ul(s, r, a);
          o[a] ? (o[a].p(_, f), w(o[a], 1)) : (o[a] = Al(_), o[a].c(), w(o[a], 1), o[a].m(t.parentNode, t));
        }
        for (X(), a = r.length; a < o.length; a += 1)
          c(a);
        O();
      }
    },
    i(s) {
      if (!n) {
        for (let f = 0; f < r.length; f += 1)
          w(o[f]);
        n = !0;
      }
    },
    o(s) {
      o = o.filter(Boolean);
      for (let f = 0; f < o.length; f += 1)
        q(o[f]);
      n = !1;
    },
    d(s) {
      s && (U(e), U(t)), i && i.d(s), ve(o, s);
    }
  };
}
function Ll(l) {
  let e;
  return {
    c() {
      e = J("li"), e.textContent = "Organizations", Y(e, "class", "flex h-7 items-center bg-gradient-to-r from-purple-50 to-white px-2 font-semibold text-indigo-800 dark:from-indigo-900 dark:to-gray-950 dark:text-gray-300");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && U(e);
    }
  };
}
function Al(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding_3*/
    l[36](e, i)
  ), c = () => (
    /*li_binding_3*/
    l[36](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function Tl(l) {
  let e, t, n, i = (
    /*showSearchType*/
    l[11] && Fl()
  ), r = $(
    /*entries*/
    l[15].filter(xl)
  ), o = [];
  for (let s = 0; s < r.length; s += 1)
    o[s] = jl(cl(l, r, s));
  const c = (s) => q(o[s], 1, 1, () => {
    o[s] = null;
  });
  return {
    c() {
      i && i.c(), e = Q();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      t = Le();
    },
    m(s, f) {
      i && i.m(s, f), R(s, e, f);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(s, f);
      R(s, t, f), n = !0;
    },
    p(s, f) {
      if (/*showSearchType*/
      s[11] ? i || (i = Fl(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), f[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        r = $(
          /*entries*/
          s[15].filter(xl)
        );
        let a;
        for (a = 0; a < r.length; a += 1) {
          const _ = cl(s, r, a);
          o[a] ? (o[a].p(_, f), w(o[a], 1)) : (o[a] = jl(_), o[a].c(), w(o[a], 1), o[a].m(t.parentNode, t));
        }
        for (X(), a = r.length; a < o.length; a += 1)
          c(a);
        O();
      }
    },
    i(s) {
      if (!n) {
        for (let f = 0; f < r.length; f += 1)
          w(o[f]);
        n = !0;
      }
    },
    o(s) {
      o = o.filter(Boolean);
      for (let f = 0; f < o.length; f += 1)
        q(o[f]);
      n = !1;
    },
    d(s) {
      s && (U(e), U(t)), i && i.d(s), ve(o, s);
    }
  };
}
function Fl(l) {
  let e;
  return {
    c() {
      e = J("li"), e.textContent = "Users", Y(e, "class", "flex h-7 items-center bg-gradient-to-r from-teal-50 to-white px-2 font-semibold text-teal-800 dark:from-teal-900 dark:to-gray-950 dark:text-gray-300");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && U(e);
    }
  };
}
function jl(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding_4*/
    l[37](e, i)
  ), c = () => (
    /*li_binding_4*/
    l[37](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function Ml(l) {
  let e, t, n, i = (
    /*showSearchType*/
    l[11] && Vl()
  ), r = $(
    /*entries*/
    l[15].filter(en)
  ), o = [];
  for (let s = 0; s < r.length; s += 1)
    o[s] = Dl(al(l, r, s));
  const c = (s) => q(o[s], 1, 1, () => {
    o[s] = null;
  });
  return {
    c() {
      i && i.c(), e = Q();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      t = Le();
    },
    m(s, f) {
      i && i.m(s, f), R(s, e, f);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(s, f);
      R(s, t, f), n = !0;
    },
    p(s, f) {
      if (/*showSearchType*/
      s[11] ? i || (i = Vl(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), f[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        r = $(
          /*entries*/
          s[15].filter(en)
        );
        let a;
        for (a = 0; a < r.length; a += 1) {
          const _ = al(s, r, a);
          o[a] ? (o[a].p(_, f), w(o[a], 1)) : (o[a] = Dl(_), o[a].c(), w(o[a], 1), o[a].m(t.parentNode, t));
        }
        for (X(), a = r.length; a < o.length; a += 1)
          c(a);
        O();
      }
    },
    i(s) {
      if (!n) {
        for (let f = 0; f < r.length; f += 1)
          w(o[f]);
        n = !0;
      }
    },
    o(s) {
      o = o.filter(Boolean);
      for (let f = 0; f < o.length; f += 1)
        q(o[f]);
      n = !1;
    },
    d(s) {
      s && (U(e), U(t)), i && i.d(s), ve(o, s);
    }
  };
}
function Vl(l) {
  let e;
  return {
    c() {
      e = J("li"), e.textContent = "Papers", Y(e, "class", "flex h-7 items-center bg-gradient-to-r from-gray-50 to-white px-2 font-semibold text-gray-800 dark:from-gray-900 dark:to-gray-950 dark:text-gray-300");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && U(e);
    }
  };
}
function Dl(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding_5*/
    l[38](e, i)
  ), c = () => (
    /*li_binding_5*/
    l[38](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function zl(l) {
  let e, t, n, i = (
    /*showSearchType*/
    l[11] && Pl()
  ), r = $(
    /*entries*/
    l[15].filter(tn)
  ), o = [];
  for (let s = 0; s < r.length; s += 1)
    o[s] = Bl(fl(l, r, s));
  const c = (s) => q(o[s], 1, 1, () => {
    o[s] = null;
  });
  return {
    c() {
      i && i.c(), e = Q();
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      t = Le();
    },
    m(s, f) {
      i && i.m(s, f), R(s, e, f);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(s, f);
      R(s, t, f), n = !0;
    },
    p(s, f) {
      if (/*showSearchType*/
      s[11] ? i || (i = Pl(), i.c(), i.m(e.parentNode, e)) : i && (i.d(1), i = null), f[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        r = $(
          /*entries*/
          s[15].filter(tn)
        );
        let a;
        for (a = 0; a < r.length; a += 1) {
          const _ = fl(s, r, a);
          o[a] ? (o[a].p(_, f), w(o[a], 1)) : (o[a] = Bl(_), o[a].c(), w(o[a], 1), o[a].m(t.parentNode, t));
        }
        for (X(), a = r.length; a < o.length; a += 1)
          c(a);
        O();
      }
    },
    i(s) {
      if (!n) {
        for (let f = 0; f < r.length; f += 1)
          w(o[f]);
        n = !0;
      }
    },
    o(s) {
      o = o.filter(Boolean);
      for (let f = 0; f < o.length; f += 1)
        q(o[f]);
      n = !1;
    },
    d(s) {
      s && (U(e), U(t)), i && i.d(s), ve(o, s);
    }
  };
}
function Pl(l) {
  let e;
  return {
    c() {
      e = J("li"), e.textContent = "Collections", Y(e, "class", "flex h-7 items-center bg-gradient-to-r from-gray-50 to-white px-2 font-semibold text-gray-800 dark:from-gray-900 dark:to-gray-950 dark:text-gray-300");
    },
    m(t, n) {
      R(t, e, n);
    },
    d(t) {
      t && U(e);
    }
  };
}
function Bl(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding_6*/
    l[39](e, i)
  ), c = () => (
    /*li_binding_6*/
    l[39](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function Il(l) {
  let e, t, n = $(
    /*entries*/
    l[15].filter(ln)
  ), i = [];
  for (let o = 0; o < n.length; o += 1)
    i[o] = Ul(rl(l, n, o));
  const r = (o) => q(i[o], 1, 1, () => {
    i[o] = null;
  });
  return {
    c() {
      e = J("ul");
      for (let o = 0; o < i.length; o += 1)
        i[o].c();
      Y(e, "class", "mt-1 max-h-[calc(100vh-100px)] w-full divide-y divide-gray-100 overflow-hidden overflow-y-auto rounded-lg border border-gray-100 bg-white text-sm shadow-lg");
    },
    m(o, c) {
      R(o, e, c);
      for (let s = 0; s < i.length; s += 1)
        i[s] && i[s].m(e, null);
      t = !0;
    },
    p(o, c) {
      if (c[0] & /*resultElements, entries, isSelected, selectedEntryIdx, handleClickEntry*/
      36995072) {
        n = $(
          /*entries*/
          o[15].filter(ln)
        );
        let s;
        for (s = 0; s < n.length; s += 1) {
          const f = rl(o, n, s);
          i[s] ? (i[s].p(f, c), w(i[s], 1)) : (i[s] = Ul(f), i[s].c(), w(i[s], 1), i[s].m(e, null));
        }
        for (X(), s = n.length; s < i.length; s += 1)
          r(s);
        O();
      }
    },
    i(o) {
      if (!t) {
        for (let c = 0; c < n.length; c += 1)
          w(i[c]);
        t = !0;
      }
    },
    o(o) {
      i = i.filter(Boolean);
      for (let c = 0; c < i.length; c += 1)
        q(i[c]);
      t = !1;
    },
    d(o) {
      o && U(e), ve(i, o);
    }
  };
}
function Ul(l) {
  let e, t, n, i = (
    /*entry*/
    l[53]
  ), r;
  t = new we({
    props: {
      entry: (
        /*entry*/
        l[53]
      ),
      isSelected: (
        /*isSelected*/
        l[25](
          /*selectedEntryIdx*/
          l[18],
          /*entry*/
          l[53]
        )
      ),
      onClick: (
        /*handleClickEntry*/
        l[21]
      )
    }
  });
  const o = () => (
    /*li_binding_7*/
    l[41](e, i)
  ), c = () => (
    /*li_binding_7*/
    l[41](null, i)
  );
  return {
    c() {
      e = J("li"), de(t.$$.fragment), n = Q();
    },
    m(s, f) {
      R(s, e, f), he(t, e, null), W(e, n), o(), r = !0;
    },
    p(s, f) {
      l = s;
      const a = {};
      f[0] & /*entries*/
      32768 && (a.entry = /*entry*/
      l[53]), f[0] & /*selectedEntryIdx, entries*/
      294912 && (a.isSelected = /*isSelected*/
      l[25](
        /*selectedEntryIdx*/
        l[18],
        /*entry*/
        l[53]
      )), t.$set(a), i !== /*entry*/
      l[53] && (c(), i = /*entry*/
      l[53], o());
    },
    i(s) {
      r || (w(t.$$.fragment, s), r = !0);
    },
    o(s) {
      q(t.$$.fragment, s), r = !1;
    },
    d(s) {
      s && U(e), me(t), c();
    }
  };
}
function Vs(l) {
  let e, t, n, i, r, o, c, s, f, a = (
    /*showIcon*/
    l[5] && hl()
  ), _ = (
    /*isOpen*/
    l[12] && gl(l)
  );
  return {
    c() {
      e = J("div"), t = J("input"), i = Q(), a && a.c(), r = Q(), _ && _.c(), t.disabled = /*disabled*/
      l[9], Y(t, "autocomplete", "off"), Y(t, "class", n = "w-full dark:bg-gray-950 " + /*showIcon*/
      (l[5] ? "pl-8" : "") + " " + /*header*/
      (l[4] ? "form-input-alt h-9 pr-3 focus:shadow-xl" : "form-input") + " " + /*inputClassNames*/
      l[3]), Y(
        t,
        "name",
        /*inputName*/
        l[6]
      ), Y(
        t,
        "placeholder",
        /*placeholder*/
        l[7]
      ), t.required = /*required*/
      l[8], Y(t, "spellcheck", "false"), Y(t, "type", "text"), Y(e, "class", o = "relative " + /*classNames*/
      l[1]);
    },
    m(b, p) {
      R(b, e, p), W(e, t), ol(
        t,
        /*inputValue*/
        l[0]
      ), l[32](t), W(e, i), a && a.m(e, null), W(e, r), _ && _.m(e, null), l[43](e), c = !0, s || (f = [
        Je(
          t,
          "input",
          /*input_input_handler*/
          l[31]
        ),
        Je(
          t,
          "focus",
          /*handleFocus*/
          l[22]
        ),
        Je(
          t,
          "input",
          /*handleInput*/
          l[24]
        ),
        Je(
          t,
          "keydown",
          /*handleKeyDown*/
          l[23]
        )
      ], s = !0);
    },
    p(b, p) {
      (!c || p[0] & /*disabled*/
      512) && (t.disabled = /*disabled*/
      b[9]), (!c || p[0] & /*showIcon, header, inputClassNames*/
      56 && n !== (n = "w-full dark:bg-gray-950 " + /*showIcon*/
      (b[5] ? "pl-8" : "") + " " + /*header*/
      (b[4] ? "form-input-alt h-9 pr-3 focus:shadow-xl" : "form-input") + " " + /*inputClassNames*/
      b[3])) && Y(t, "class", n), (!c || p[0] & /*inputName*/
      64) && Y(
        t,
        "name",
        /*inputName*/
        b[6]
      ), (!c || p[0] & /*placeholder*/
      128) && Y(
        t,
        "placeholder",
        /*placeholder*/
        b[7]
      ), (!c || p[0] & /*required*/
      256) && (t.required = /*required*/
      b[8]), p[0] & /*inputValue*/
      1 && t.value !== /*inputValue*/
      b[0] && ol(
        t,
        /*inputValue*/
        b[0]
      ), /*showIcon*/
      b[5] ? a ? p[0] & /*showIcon*/
      32 && w(a, 1) : (a = hl(), a.c(), w(a, 1), a.m(e, r)) : a && (X(), q(a, 1, 1, () => {
        a = null;
      }), O()), /*isOpen*/
      b[12] ? _ ? (_.p(b, p), p[0] & /*isOpen*/
      4096 && w(_, 1)) : (_ = gl(b), _.c(), w(_, 1), _.m(e, null)) : _ && (X(), q(_, 1, 1, () => {
        _ = null;
      }), O()), (!c || p[0] & /*classNames*/
      2 && o !== (o = "relative " + /*classNames*/
      b[1])) && Y(e, "class", o);
    },
    i(b) {
      c || (w(a), w(_), c = !0);
    },
    o(b) {
      q(a), q(_), c = !1;
    },
    d(b) {
      b && U(e), l[32](null), a && a.d(), _ && _.d(), l[43](null), s = !1, As(f);
    }
  };
}
const Ds = 300;
function ge(l, e) {
  return l ?? e();
}
function ne(l) {
  let e, t = l[0], n = 1;
  for (; n < l.length; ) {
    const i = l[n], r = l[n + 1];
    if (n += 2, (i === "optionalAccess" || i === "optionalCall") && t == null)
      return;
    i === "access" || i === "optionalAccess" ? (e = t, t = r(t)) : (i === "call" || i === "optionalCall") && (t = r((...o) => t.call(e, ...o)), e = void 0);
  }
  return t;
}
function be(l) {
  return `${l.type}__${l.id}`;
}
const Rl = (l) => l.type === "full-text-search", Zl = (l) => l.type === "collection", Hl = (l) => l.type === "paper", Ql = (l) => l.type === "user", Kl = (l) => l.type === "org", Yl = (l) => l.type === "space", Gl = (l) => l.type === "dataset", Wl = (l) => l.type === "model", zs = () => {
}, Jl = (l) => ["model", "all-models"].includes(l.type), Ol = (l) => ["dataset", "all-datasets"].includes(l.type), Xl = (l) => ["space", "all-spaces"].includes(l.type), $l = (l) => l.type === "org", xl = (l) => l.type === "user", en = (l) => l.type === "paper", tn = (l) => l.type === "collection", ln = (l) => l.type === "full-text-search";
function Ps(l, e, t) {
  let { classNames: i = "" } = e, { bodyClassNames: r = "" } = e, { inputClassNames: o = "" } = e, { header: c = !1 } = e, { showIcon: s = !1 } = e, { inputName: f = "" } = e, { placeholder: a = "" } = e, { required: _ = !1 } = e, { inputValue: b = "" } = e, { disabled: p = !1 } = e, { searchParams: k = {} } = e, { url: F = "https://huggingface.co/api/quicksearch" } = e, { initialFocus: D = !1 } = e, { position: B = "absolute" } = e, { showSearchType: z = !0 } = e, { resetLastQueryOnCommit: h = !1 } = e, v = [], m = !1, d = null, y = 0, S, j, I, T = -1, H, Z = new AbortController();
  const E = {}, N = Fs();
  js(() => (document.addEventListener("click", V), D && I.focus(), () => {
    document.removeEventListener("click", V);
  }));
  function V(u) {
    if (!m)
      return;
    const M = u.target;
    M !== H && !ne([
      H,
      "optionalAccess",
      (K) => K.contains,
      "call",
      (K) => K(M)
    ]) && t(12, m = !1);
  }
  function rt(u) {
    t(18, T = v.findIndex((M) => M.id === u.id && M.type === u.type)), Ie();
  }
  function Ie() {
    if (v[T]) {
      const u = v[T];
      t(0, b = u.id), N("selected", u), h && (d = null), t(12, m = !1);
    }
  }
  function Ue(u) {
    u === 1 ? t(18, T = T + 1 > v.length - 1 ? 0 : T + 1) : t(18, T = T - 1 < 0 ? v.length - 1 : T - 1);
    const M = v[T];
    if (!M)
      return;
    const K = E[be(M)];
    if (K.offsetTop < S.scrollTop) {
      const Re = ne([
        S,
        "access",
        (Ce) => Ce.firstElementChild,
        "optionalAccess",
        (Ce) => Ce.clientHeight
      ]) || 0;
      S.scrollTo({ top: K.offsetTop - Re });
    } else
      K.offsetTop + K.offsetHeight > S.scrollTop + S.offsetHeight && S.scrollTo({ top: K.offsetTop });
  }
  async function Ae() {
    d === null && await Ye(), t(12, m = !0);
  }
  function ft(u) {
    u.key === "Escape" && m ? (u.preventDefault(), u.stopPropagation(), t(12, m = !1)) : u.key === "Enter" && m ? (u.preventDefault(), Ie()) : u.altKey && u.key === "ArrowUp" && m ? (u.preventDefault(), t(12, m = !1)) : u.altKey && u.key === "ArrowDown" && !m ? (u.preventDefault(), t(12, m = !0)) : u.key === "ArrowUp" && m ? (u.preventDefault(), Ue(-1)) : u.key === "ArrowDown" && m ? (u.preventDefault(), Ue(1)) : (u.metaKey || u.ctrlKey) && u.code === "KeyK" && (u.preventDefault(), t(12, m = !1));
  }
  async function Ye() {
    const u = b.trim();
    if (u !== d) {
      const M = await wn(u);
      if (M.isError) {
        M.aborted || console.error(`QuickSearch Error: ${M.error}`);
        return;
      }
      const K = kn(M.payload);
      t(15, v = [...K]), t(16, y = K.length), d = u, t(18, T = v.length ? 0 : -1);
    }
  }
  const C = Ns(
    async () => {
      t(12, m = !0), await Ms(), await Ye();
    },
    Ds
  );
  function pn(u, M) {
    return ne([v, "access", (K) => K[u], "optionalAccess", (K) => K.id]) === M.id && ne([
      v,
      "access",
      (K) => K[u],
      "optionalAccess",
      (K) => K.type
    ]) === M.type;
  }
  async function wn(u = "") {
    Z.abort(), Z = new AbortController();
    const { lang: M, library: K, limit: Re, orgsFilter: Ce, pipelines: at, reposFilter: ct, searchType: ut, exclude: _t, namespace: dt } = k, mt = ne([
      at,
      "optionalAccess",
      (g) => g.filter,
      "call",
      (g) => g((Vn) => ne([Vn, "optionalAccess", (ht) => ht.trim, "call", (ht) => ht()])),
      "access",
      (g) => g.join,
      "call",
      (g) => g(",")
    ]);
    return await Ss(
      F + vs({
        q: u,
        lang: M,
        library: K,
        limit: Re,
        orgsFilter: Ce,
        pipelines: mt,
        reposFilter: ct,
        type: ut,
        exclude: _t,
        namespace: dt
      }),
      { signal: Z.signal }
    );
  }
  function kn(u) {
    const M = ge(ne([u, "optionalAccess", (g) => g.datasets, "access", (g) => g.length]), () => 0) + ge(ne([u, "optionalAccess", (g) => g.models, "access", (g) => g.length]), () => 0) + ge(ne([u, "optionalAccess", (g) => g.orgs, "access", (g) => g.length]), () => 0) + ge(ne([u, "optionalAccess", (g) => g.spaces, "access", (g) => g.length]), () => 0) + ge(ne([u, "optionalAccess", (g) => g.users, "access", (g) => g.length]), () => 0) + ge(ne([u, "optionalAccess", (g) => g.papers, "access", (g) => g.length]), () => 0) + ge(
      ne([
        u,
        "optionalAccess",
        (g) => g.collections,
        "access",
        (g) => g.length
      ]),
      () => 0
    );
    if (!u || !M)
      return [];
    const K = u.models.map((g) => ({
      href: k.withLinks ? `/${g.id}` : void 0,
      id: g.id,
      _id: g._id,
      label: g.id,
      type: "model"
    })), Re = k.withLinks && u.modelsCount && u.q ? [] : [], Ce = u.datasets.map((g) => ({
      href: k.withLinks ? `/datasets/${g.id}` : void 0,
      id: g.id,
      _id: g._id,
      label: g.id,
      type: "dataset"
    })), at = k.withLinks && u.datasetsCount && u.q ? [] : [], ct = u.spaces.map((g) => ({
      href: k.withLinks ? `/spaces/${g.id}` : void 0,
      id: g.id,
      _id: g._id,
      label: g.id,
      type: "space"
    })), ut = k.withLinks && u.spacesCount && u.q ? [] : [], _t = u.orgs.map((g) => ({
      href: k.withLinks ? `/${g.name}` : void 0,
      id: g.name,
      _id: g._id,
      imgUrl: g.avatarUrl,
      label: g.fullname,
      type: "org"
    })), dt = u.users.map((g) => ({
      href: k.withLinks ? `/${g.user}` : void 0,
      id: g.user,
      _id: g._id,
      imgUrl: g.avatarUrl,
      label: g.user,
      type: "user",
      description: g.fullname
    })), mt = u.papers.map((g) => ({
      _id: g._id,
      id: g._id,
      href: k.withLinks ? `/paper/${g._id}` : void 0,
      label: g._id,
      description: g.id,
      type: "paper"
    })), qt = u.collections.map((g) => ({
      _id: g._id,
      id: g._id,
      href: k.withLinks ? `/collections/${g._id}` : void 0,
      label: g.title,
      description: g.description,
      type: "collection"
    }));
    return [
      ...K,
      ...Re,
      ...Ce,
      ...at,
      ...ct,
      ...ut,
      ..._t,
      ...dt,
      ...ge(mt, () => []),
      ...ge(qt, () => [])
    ];
  }
  function yn() {
    b = this.value, t(0, b);
  }
  function vn(u) {
    ie[u ? "unshift" : "push"](() => {
      I = u, t(14, I);
    });
  }
  function Cn(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function Sn(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function qn(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function Nn(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function En(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function Ln(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function An(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function Tn(u) {
    ie[u ? "unshift" : "push"](() => {
      S = u, t(17, S);
    });
  }
  function Fn(u, M) {
    ie[u ? "unshift" : "push"](() => {
      E[be(M)] = u, t(20, E);
    });
  }
  function jn(u) {
    ie[u ? "unshift" : "push"](() => {
      j = u, t(13, j), t(10, B), t(14, I);
    });
  }
  function Mn(u) {
    ie[u ? "unshift" : "push"](() => {
      H = u, t(19, H);
    });
  }
  return l.$$set = (u) => {
    "classNames" in u && t(1, i = u.classNames), "bodyClassNames" in u && t(2, r = u.bodyClassNames), "inputClassNames" in u && t(3, o = u.inputClassNames), "header" in u && t(4, c = u.header), "showIcon" in u && t(5, s = u.showIcon), "inputName" in u && t(6, f = u.inputName), "placeholder" in u && t(7, a = u.placeholder), "required" in u && t(8, _ = u.required), "inputValue" in u && t(0, b = u.inputValue), "disabled" in u && t(9, p = u.disabled), "searchParams" in u && t(27, k = u.searchParams), "url" in u && t(28, F = u.url), "initialFocus" in u && t(29, D = u.initialFocus), "position" in u && t(10, B = u.position), "showSearchType" in u && t(11, z = u.showSearchType), "resetLastQueryOnCommit" in u && t(30, h = u.resetLastQueryOnCommit);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*position, resultsContainerWrapperElement, inputElement*/
    25600 && B === "fixed" && j && t(13, j.style.width = `${I.clientWidth}px`, j), l.$$.dirty[0] & /*isOpen*/
    4096 && (m || N("close"));
  }, [
    b,
    i,
    r,
    o,
    c,
    s,
    f,
    a,
    _,
    p,
    B,
    z,
    m,
    j,
    I,
    v,
    y,
    S,
    T,
    H,
    E,
    rt,
    Ae,
    ft,
    C,
    pn,
    !0,
    k,
    F,
    D,
    h,
    yn,
    vn,
    Cn,
    Sn,
    qn,
    Nn,
    En,
    Ln,
    An,
    Tn,
    Fn,
    jn,
    Mn
  ];
}
class Bs extends Es {
  constructor(e) {
    super(), Ls(
      this,
      e,
      Ps,
      Vs,
      Ts,
      {
        hydrate: 26,
        classNames: 1,
        bodyClassNames: 2,
        inputClassNames: 3,
        header: 4,
        showIcon: 5,
        inputName: 6,
        placeholder: 7,
        required: 8,
        inputValue: 0,
        disabled: 9,
        searchParams: 27,
        url: 28,
        initialFocus: 29,
        position: 10,
        showSearchType: 11,
        resetLastQueryOnCommit: 30
      },
      null,
      [-1, -1, -1]
    );
  }
  get hydrate() {
    return this.$$.ctx[26];
  }
}
const {
  SvelteComponent: Is,
  attr: Us,
  create_slot: Rs,
  detach: Zs,
  element: Hs,
  get_all_dirty_from_scope: Qs,
  get_slot_changes: Ks,
  init: Ys,
  insert: Gs,
  safe_not_equal: Ws,
  transition_in: Js,
  transition_out: Os,
  update_slot_base: Xs
} = window.__gradio__svelte__internal;
function $s(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = Rs(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = Hs("div"), i && i.c(), Us(e, "class", "svelte-bv8rca");
    },
    m(r, o) {
      Gs(r, e, o), i && i.m(e, null), t = !0;
    },
    p(r, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      1) && Xs(
        i,
        n,
        r,
        /*$$scope*/
        r[0],
        t ? Ks(
          n,
          /*$$scope*/
          r[0],
          o,
          null
        ) : Qs(
          /*$$scope*/
          r[0]
        ),
        null
      );
    },
    i(r) {
      t || (Js(i, r), t = !0);
    },
    o(r) {
      Os(i, r), t = !1;
    },
    d(r) {
      r && Zs(e), i && i.d(r);
    }
  };
}
function xs(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (r) => {
    "$$scope" in r && t(0, i = r.$$scope);
  }, [i, n];
}
class eo extends Is {
  constructor(e) {
    super(), Ys(this, e, xs, $s, Ws, {});
  }
}
const {
  SvelteComponent: to,
  attr: bt,
  check_outros: lo,
  create_component: no,
  create_slot: io,
  destroy_component: so,
  detach: $e,
  element: oo,
  empty: ro,
  get_all_dirty_from_scope: fo,
  get_slot_changes: ao,
  group_outros: co,
  init: uo,
  insert: xe,
  mount_component: _o,
  null_to_empty: nn,
  safe_not_equal: mo,
  set_data: ho,
  space: go,
  text: bo,
  toggle_class: je,
  transition_in: Ze,
  transition_out: et,
  update_slot_base: po
} = window.__gradio__svelte__internal;
function sn(l) {
  let e, t;
  return e = new eo({
    props: {
      $$slots: { default: [wo] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      no(e.$$.fragment);
    },
    m(n, i) {
      _o(e, n, i), t = !0;
    },
    p(n, i) {
      const r = {};
      i & /*$$scope, info*/
      18 && (r.$$scope = { dirty: i, ctx: n }), e.$set(r);
    },
    i(n) {
      t || (Ze(e.$$.fragment, n), t = !0);
    },
    o(n) {
      et(e.$$.fragment, n), t = !1;
    },
    d(n) {
      so(e, n);
    }
  };
}
function wo(l) {
  let e;
  return {
    c() {
      e = bo(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      xe(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && ho(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && $e(e);
    }
  };
}
function ko(l) {
  let e, t, n, i, r;
  const o = (
    /*#slots*/
    l[3].default
  ), c = io(
    o,
    l,
    /*$$scope*/
    l[4],
    null
  );
  let s = (
    /*info*/
    l[1] && sn(l)
  );
  return {
    c() {
      e = oo("span"), c && c.c(), n = go(), s && s.c(), i = ro(), bt(e, "data-testid", "block-info"), bt(e, "class", t = nn(
        /*classNames*/
        l[2]
      ) + " svelte-10jur7g"), je(e, "sr-only", !/*show_label*/
      l[0]), je(e, "hide", !/*show_label*/
      l[0]), je(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(f, a) {
      xe(f, e, a), c && c.m(e, null), xe(f, n, a), s && s.m(f, a), xe(f, i, a), r = !0;
    },
    p(f, [a]) {
      c && c.p && (!r || a & /*$$scope*/
      16) && po(
        c,
        o,
        f,
        /*$$scope*/
        f[4],
        r ? ao(
          o,
          /*$$scope*/
          f[4],
          a,
          null
        ) : fo(
          /*$$scope*/
          f[4]
        ),
        null
      ), (!r || a & /*classNames*/
      4 && t !== (t = nn(
        /*classNames*/
        f[2]
      ) + " svelte-10jur7g")) && bt(e, "class", t), (!r || a & /*classNames, show_label*/
      5) && je(e, "sr-only", !/*show_label*/
      f[0]), (!r || a & /*classNames, show_label*/
      5) && je(e, "hide", !/*show_label*/
      f[0]), (!r || a & /*classNames, info*/
      6) && je(
        e,
        "has-info",
        /*info*/
        f[1] != null
      ), /*info*/
      f[1] ? s ? (s.p(f, a), a & /*info*/
      2 && Ze(s, 1)) : (s = sn(f), s.c(), Ze(s, 1), s.m(i.parentNode, i)) : s && (co(), et(s, 1, 1, () => {
        s = null;
      }), lo());
    },
    i(f) {
      r || (Ze(c, f), Ze(s), r = !0);
    },
    o(f) {
      et(c, f), et(s), r = !1;
    },
    d(f) {
      f && ($e(e), $e(n), $e(i)), c && c.d(f), s && s.d(f);
    }
  };
}
function yo(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: r = !0 } = e, { info: o = void 0 } = e, { classNames: c = "" } = e;
  return l.$$set = (s) => {
    "show_label" in s && t(0, r = s.show_label), "info" in s && t(1, o = s.info), "classNames" in s && t(2, c = s.classNames), "$$scope" in s && t(4, i = s.$$scope);
  }, [r, o, c, n, i];
}
class vo extends to {
  constructor(e) {
    super(), uo(this, e, yo, ko, mo, { show_label: 0, info: 1, classNames: 2 });
  }
}
const {
  SvelteComponent: Co,
  add_flush_callback: So,
  assign: qo,
  attr: No,
  bind: Eo,
  binding_callbacks: Lo,
  check_outros: Ao,
  create_component: lt,
  destroy_component: nt,
  detach: it,
  element: To,
  flush: x,
  get_spread_object: Fo,
  get_spread_update: jo,
  group_outros: Mo,
  init: Vo,
  insert: st,
  mount_component: ot,
  safe_not_equal: Do,
  set_data: zo,
  space: on,
  text: Po,
  transition_in: qe,
  transition_out: Ve
} = window.__gradio__svelte__internal;
function rn(l) {
  let e, t;
  const n = [
    { autoscroll: (
      /*gradio*/
      l[1].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[1].i18n
    ) },
    /*loading_status*/
    l[10]
  ];
  let i = {};
  for (let r = 0; r < n.length; r += 1)
    i = qo(i, n[r]);
  return e = new Pi({ props: i }), {
    c() {
      lt(e.$$.fragment);
    },
    m(r, o) {
      ot(e, r, o), t = !0;
    },
    p(r, o) {
      const c = o & /*gradio, loading_status*/
      1026 ? jo(n, [
        o & /*gradio*/
        2 && { autoscroll: (
          /*gradio*/
          r[1].autoscroll
        ) },
        o & /*gradio*/
        2 && { i18n: (
          /*gradio*/
          r[1].i18n
        ) },
        o & /*loading_status*/
        1024 && Fo(
          /*loading_status*/
          r[10]
        )
      ]) : {};
      e.$set(c);
    },
    i(r) {
      t || (qe(e.$$.fragment, r), t = !0);
    },
    o(r) {
      Ve(e.$$.fragment, r), t = !1;
    },
    d(r) {
      nt(e, r);
    }
  };
}
function Bo(l) {
  let e;
  return {
    c() {
      e = Po(
        /*label*/
        l[2]
      );
    },
    m(t, n) {
      st(t, e, n);
    },
    p(t, n) {
      n & /*label*/
      4 && zo(
        e,
        /*label*/
        t[2]
      );
    },
    d(t) {
      t && it(e);
    }
  };
}
function Io(l) {
  let e, t, n, i, r, o, c = (
    /*loading_status*/
    l[10] && rn(l)
  );
  t = new vo({
    props: {
      classNames: "z-0",
      show_label: (
        /*show_label*/
        l[7]
      ),
      info: void 0,
      $$slots: { default: [Bo] },
      $$scope: { ctx: l }
    }
  });
  function s(a) {
    l[15](a);
  }
  let f = {
    classNames: "flex-1 lg:max-w-sm mr-2 sm:mr-4 md:mr-3 xl:mr-6",
    header: !0,
    showIcon: !0,
    disabled: !/*interactive*/
    l[11],
    placeholder: (
      /*placeholder*/
      l[6]
    ),
    searchParams: {
      withLinks: !0,
      searchType: (
        /*search_type*/
        l[12]
      )
    }
  };
  return (
    /*value*/
    l[0] !== void 0 && (f.inputValue = /*value*/
    l[0]), i = new Bs({ props: f }), Lo.push(() => Eo(i, "inputValue", s)), i.$on(
      "selected",
      /*selected_handler*/
      l[16]
    ), {
      c() {
        c && c.c(), e = on(), lt(t.$$.fragment), n = on(), lt(i.$$.fragment);
      },
      m(a, _) {
        c && c.m(a, _), st(a, e, _), ot(t, a, _), st(a, n, _), ot(i, a, _), o = !0;
      },
      p(a, _) {
        /*loading_status*/
        a[10] ? c ? (c.p(a, _), _ & /*loading_status*/
        1024 && qe(c, 1)) : (c = rn(a), c.c(), qe(c, 1), c.m(e.parentNode, e)) : c && (Mo(), Ve(c, 1, 1, () => {
          c = null;
        }), Ao());
        const b = {};
        _ & /*show_label*/
        128 && (b.show_label = /*show_label*/
        a[7]), _ & /*$$scope, label*/
        524292 && (b.$$scope = { dirty: _, ctx: a }), t.$set(b);
        const p = {};
        _ & /*interactive*/
        2048 && (p.disabled = !/*interactive*/
        a[11]), _ & /*placeholder*/
        64 && (p.placeholder = /*placeholder*/
        a[6]), _ & /*search_type*/
        4096 && (p.searchParams = {
          withLinks: !0,
          searchType: (
            /*search_type*/
            a[12]
          )
        }), !r && _ & /*value*/
        1 && (r = !0, p.inputValue = /*value*/
        a[0], So(() => r = !1)), i.$set(p);
      },
      i(a) {
        o || (qe(c), qe(t.$$.fragment, a), qe(i.$$.fragment, a), o = !0);
      },
      o(a) {
        Ve(c), Ve(t.$$.fragment, a), Ve(i.$$.fragment, a), o = !1;
      },
      d(a) {
        a && (it(e), it(n)), c && c.d(a), nt(t, a), nt(i, a);
      }
    }
  );
}
function Uo(l) {
  let e, t, n;
  return t = new On({
    props: {
      visible: (
        /*visible*/
        l[5]
      ),
      elem_id: (
        /*elem_id*/
        l[3]
      ),
      elem_classes: (
        /*elem_classes*/
        l[4]
      ),
      scale: (
        /*scale*/
        l[8]
      ),
      min_width: (
        /*min_width*/
        l[9]
      ),
      allow_overflow: !0,
      padding: !0,
      $$slots: { default: [Io] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      e = To("div"), lt(t.$$.fragment), No(e, "class", "custom-component");
    },
    m(i, r) {
      st(i, e, r), ot(t, e, null), n = !0;
    },
    p(i, [r]) {
      const o = {};
      r & /*visible*/
      32 && (o.visible = /*visible*/
      i[5]), r & /*elem_id*/
      8 && (o.elem_id = /*elem_id*/
      i[3]), r & /*elem_classes*/
      16 && (o.elem_classes = /*elem_classes*/
      i[4]), r & /*scale*/
      256 && (o.scale = /*scale*/
      i[8]), r & /*min_width*/
      512 && (o.min_width = /*min_width*/
      i[9]), r & /*$$scope, interactive, placeholder, search_type, value, sumbit_on_select, gradio, show_label, label, loading_status*/
      539847 && (o.$$scope = { dirty: r, ctx: i }), t.$set(o);
    },
    i(i) {
      n || (qe(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Ve(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && it(e), nt(t);
    }
  };
}
function Ro(l, e, t) {
  let { gradio: n } = e, { label: i = "Textbox" } = e, { elem_id: r = "" } = e, { elem_classes: o = [] } = e, { visible: c = !0 } = e, { value: s = "" } = e, { placeholder: f = "Search models, datasets, users..." } = e, { show_label: a } = e, { scale: _ = null } = e, { min_width: b = void 0 } = e, { loading_status: p = void 0 } = e, { value_is_output: k = !1 } = e, { interactive: F } = e, { search_type: D = ["model", "dataset", "space", "org", "user"] } = e, { sumbit_on_select: B = !0 } = e;
  function z() {
    n.dispatch("change"), k || n.dispatch("input");
  }
  function h(m) {
    s = m, t(0, s);
  }
  const v = () => {
    B && n.dispatch("submit");
  };
  return l.$$set = (m) => {
    "gradio" in m && t(1, n = m.gradio), "label" in m && t(2, i = m.label), "elem_id" in m && t(3, r = m.elem_id), "elem_classes" in m && t(4, o = m.elem_classes), "visible" in m && t(5, c = m.visible), "value" in m && t(0, s = m.value), "placeholder" in m && t(6, f = m.placeholder), "show_label" in m && t(7, a = m.show_label), "scale" in m && t(8, _ = m.scale), "min_width" in m && t(9, b = m.min_width), "loading_status" in m && t(10, p = m.loading_status), "value_is_output" in m && t(14, k = m.value_is_output), "interactive" in m && t(11, F = m.interactive), "search_type" in m && t(12, D = m.search_type), "sumbit_on_select" in m && t(13, B = m.sumbit_on_select);
  }, l.$$.update = () => {
    l.$$.dirty & /*value*/
    1 && s === null && t(0, s = ""), l.$$.dirty & /*value*/
    1 && z();
  }, [
    s,
    n,
    i,
    r,
    o,
    c,
    f,
    a,
    _,
    b,
    p,
    F,
    D,
    B,
    k,
    h,
    v
  ];
}
class Zo extends Co {
  constructor(e) {
    super(), Vo(this, e, Ro, Uo, Do, {
      gradio: 1,
      label: 2,
      elem_id: 3,
      elem_classes: 4,
      visible: 5,
      value: 0,
      placeholder: 6,
      show_label: 7,
      scale: 8,
      min_width: 9,
      loading_status: 10,
      value_is_output: 14,
      interactive: 11,
      search_type: 12,
      sumbit_on_select: 13
    });
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), x();
  }
  get label() {
    return this.$$.ctx[2];
  }
  set label(e) {
    this.$$set({ label: e }), x();
  }
  get elem_id() {
    return this.$$.ctx[3];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), x();
  }
  get elem_classes() {
    return this.$$.ctx[4];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), x();
  }
  get visible() {
    return this.$$.ctx[5];
  }
  set visible(e) {
    this.$$set({ visible: e }), x();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), x();
  }
  get placeholder() {
    return this.$$.ctx[6];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), x();
  }
  get show_label() {
    return this.$$.ctx[7];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), x();
  }
  get scale() {
    return this.$$.ctx[8];
  }
  set scale(e) {
    this.$$set({ scale: e }), x();
  }
  get min_width() {
    return this.$$.ctx[9];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), x();
  }
  get loading_status() {
    return this.$$.ctx[10];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), x();
  }
  get value_is_output() {
    return this.$$.ctx[14];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), x();
  }
  get interactive() {
    return this.$$.ctx[11];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), x();
  }
  get search_type() {
    return this.$$.ctx[12];
  }
  set search_type(e) {
    this.$$set({ search_type: e }), x();
  }
  get sumbit_on_select() {
    return this.$$.ctx[13];
  }
  set sumbit_on_select(e) {
    this.$$set({ sumbit_on_select: e }), x();
  }
}
export {
  Zo as default
};
