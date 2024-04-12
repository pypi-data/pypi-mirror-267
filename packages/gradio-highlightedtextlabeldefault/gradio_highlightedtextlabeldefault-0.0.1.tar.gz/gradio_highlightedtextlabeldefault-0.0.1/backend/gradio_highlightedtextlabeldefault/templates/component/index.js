const Ll = [
  "red",
  "green",
  "blue",
  "yellow",
  "purple",
  "teal",
  "orange",
  "cyan",
  "lime",
  "pink"
], Sn = [
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
], El = {
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
}, Nl = Sn.reduce(
  (t, { color: e, primary: l, secondary: n }) => ({
    ...t,
    [e]: {
      primary: El[e][l],
      secondary: El[e][n]
    }
  }),
  {}
), At = (t) => Ll[t % Ll.length];
function jl(t, e, l) {
  if (!l) {
    var n = document.createElement("canvas");
    l = n.getContext("2d");
  }
  l.fillStyle = t, l.fillRect(0, 0, 1, 1);
  const [o, s, i] = l.getImageData(0, 0, 1, 1).data;
  return l.clearRect(0, 0, 1, 1), `rgba(${o}, ${s}, ${i}, ${255 / e})`;
}
function Bt(t, e, l, n) {
  for (const o in t) {
    const s = t[o].trim();
    s in Nl ? e[o] = Nl[s] : e[o] = {
      primary: l ? jl(t[o], 1, n) : t[o],
      secondary: l ? jl(t[o], 0.5, n) : t[o]
    };
  }
}
function Ht(t, e) {
  let l = [], n = null, o = null;
  for (const s of t)
    e === "empty" && s.class_or_confidence === null || e === "equal" && o === s.class_or_confidence ? n = n ? n + s.token : s.token : (n !== null && l.push({
      token: n,
      class_or_confidence: o
    }), n = s.token, o = s.class_or_confidence);
  return n !== null && l.push({
    token: n,
    class_or_confidence: o
  }), l;
}
const {
  SvelteComponent: qn,
  append: ue,
  attr: H,
  destroy_each: fl,
  detach: Z,
  element: Q,
  empty: Ot,
  ensure_array_like: we,
  init: Ln,
  insert: P,
  listen: Ze,
  noop: Vl,
  run_all: En,
  safe_not_equal: Nn,
  set_data: vl,
  set_style: ll,
  space: Ae,
  text: Pe,
  toggle_class: he
} = window.__gradio__svelte__internal, { createEventDispatcher: jn } = window.__gradio__svelte__internal;
function Ml(t, e, l) {
  const n = t.slice();
  n[17] = e[l];
  const o = typeof /*v*/
  n[17].class_or_confidence == "string" ? parseInt(
    /*v*/
    n[17].class_or_confidence
  ) : (
    /*v*/
    n[17].class_or_confidence
  );
  return n[26] = o, n;
}
function Fl(t, e, l) {
  const n = t.slice();
  return n[17] = e[l], n[19] = l, n;
}
function Tl(t, e, l) {
  const n = t.slice();
  return n[20] = e[l], n[22] = l, n;
}
function Il(t, e, l) {
  const n = t.slice();
  return n[23] = e[l][0], n[24] = e[l][1], n[19] = l, n;
}
function Vn(t) {
  let e, l, n = (
    /*show_legend*/
    t[1] && zl()
  ), o = we(
    /*value*/
    t[0]
  ), s = [];
  for (let i = 0; i < o.length; i += 1)
    s[i] = Al(Ml(t, o, i));
  return {
    c() {
      n && n.c(), e = Ae(), l = Q("div");
      for (let i = 0; i < s.length; i += 1)
        s[i].c();
      H(l, "class", "textfield svelte-1woixh4"), H(l, "data-testid", "highlighted-text:textfield");
    },
    m(i, a) {
      n && n.m(i, a), P(i, e, a), P(i, l, a);
      for (let f = 0; f < s.length; f += 1)
        s[f] && s[f].m(l, null);
    },
    p(i, a) {
      if (/*show_legend*/
      i[1] ? n || (n = zl(), n.c(), n.m(e.parentNode, e)) : n && (n.d(1), n = null), a & /*value, parseInt*/
      1) {
        o = we(
          /*value*/
          i[0]
        );
        let f;
        for (f = 0; f < o.length; f += 1) {
          const r = Ml(i, o, f);
          s[f] ? s[f].p(r, a) : (s[f] = Al(r), s[f].c(), s[f].m(l, null));
        }
        for (; f < s.length; f += 1)
          s[f].d(1);
        s.length = o.length;
      }
    },
    d(i) {
      i && (Z(e), Z(l)), n && n.d(i), fl(s, i);
    }
  };
}
function Mn(t) {
  let e, l, n = (
    /*show_legend*/
    t[1] && Bl(t)
  ), o = we(
    /*value*/
    t[0]
  ), s = [];
  for (let i = 0; i < o.length; i += 1)
    s[i] = Dl(Fl(t, o, i));
  return {
    c() {
      n && n.c(), e = Ae(), l = Q("div");
      for (let i = 0; i < s.length; i += 1)
        s[i].c();
      H(l, "class", "textfield svelte-1woixh4");
    },
    m(i, a) {
      n && n.m(i, a), P(i, e, a), P(i, l, a);
      for (let f = 0; f < s.length; f += 1)
        s[f] && s[f].m(l, null);
    },
    p(i, a) {
      if (/*show_legend*/
      i[1] ? n ? n.p(i, a) : (n = Bl(i), n.c(), n.m(e.parentNode, e)) : n && (n.d(1), n = null), a & /*splitTextByNewline, value, active, selectable, _color_map, dispatch, show_legend*/
      111) {
        o = we(
          /*value*/
          i[0]
        );
        let f;
        for (f = 0; f < o.length; f += 1) {
          const r = Fl(i, o, f);
          s[f] ? s[f].p(r, a) : (s[f] = Dl(r), s[f].c(), s[f].m(l, null));
        }
        for (; f < s.length; f += 1)
          s[f].d(1);
        s.length = o.length;
      }
    },
    d(i) {
      i && (Z(e), Z(l)), n && n.d(i), fl(s, i);
    }
  };
}
function zl(t) {
  let e;
  return {
    c() {
      e = Q("div"), e.innerHTML = "<span>-1</span> <span>0</span> <span>+1</span>", H(e, "class", "color-legend svelte-1woixh4"), H(e, "data-testid", "highlighted-text:color-legend");
    },
    m(l, n) {
      P(l, e, n);
    },
    d(l) {
      l && Z(e);
    }
  };
}
function Al(t) {
  let e, l, n = (
    /*v*/
    t[17].token + ""
  ), o, s, i;
  return {
    c() {
      e = Q("span"), l = Q("span"), o = Pe(n), s = Ae(), H(l, "class", "text svelte-1woixh4"), H(e, "class", "textspan score-text svelte-1woixh4"), H(e, "style", i = "background-color: rgba(" + /*score*/
      (t[26] && /*score*/
      t[26] < 0 ? "128, 90, 213," + -/*score*/
      t[26] : "239, 68, 60," + /*score*/
      t[26]) + ")");
    },
    m(a, f) {
      P(a, e, f), ue(e, l), ue(l, o), ue(e, s);
    },
    p(a, f) {
      f & /*value*/
      1 && n !== (n = /*v*/
      a[17].token + "") && vl(o, n), f & /*value*/
      1 && i !== (i = "background-color: rgba(" + /*score*/
      (a[26] && /*score*/
      a[26] < 0 ? "128, 90, 213," + -/*score*/
      a[26] : "239, 68, 60," + /*score*/
      a[26]) + ")") && H(e, "style", i);
    },
    d(a) {
      a && Z(e);
    }
  };
}
function Bl(t) {
  let e, l = we(Object.entries(
    /*_color_map*/
    t[5]
  )), n = [];
  for (let o = 0; o < l.length; o += 1)
    n[o] = Hl(Il(t, l, o));
  return {
    c() {
      e = Q("div");
      for (let o = 0; o < n.length; o += 1)
        n[o].c();
      H(e, "class", "category-legend svelte-1woixh4"), H(e, "data-testid", "highlighted-text:category-legend");
    },
    m(o, s) {
      P(o, e, s);
      for (let i = 0; i < n.length; i += 1)
        n[i] && n[i].m(e, null);
    },
    p(o, s) {
      if (s & /*Object, _color_map, handle_mouseover, handle_mouseout*/
      416) {
        l = we(Object.entries(
          /*_color_map*/
          o[5]
        ));
        let i;
        for (i = 0; i < l.length; i += 1) {
          const a = Il(o, l, i);
          n[i] ? n[i].p(a, s) : (n[i] = Hl(a), n[i].c(), n[i].m(e, null));
        }
        for (; i < n.length; i += 1)
          n[i].d(1);
        n.length = l.length;
      }
    },
    d(o) {
      o && Z(e), fl(n, o);
    }
  };
}
function Hl(t) {
  let e, l = (
    /*category*/
    t[23] + ""
  ), n, o, s, i;
  function a() {
    return (
      /*mouseover_handler*/
      t[10](
        /*category*/
        t[23]
      )
    );
  }
  function f() {
    return (
      /*focus_handler*/
      t[11](
        /*category*/
        t[23]
      )
    );
  }
  return {
    c() {
      e = Q("div"), n = Pe(l), o = Ae(), H(e, "class", "category-label svelte-1woixh4"), H(e, "style", "background-color:" + /*color*/
      t[24].secondary);
    },
    m(r, _) {
      P(r, e, _), ue(e, n), ue(e, o), s || (i = [
        Ze(e, "mouseover", a),
        Ze(e, "focus", f),
        Ze(
          e,
          "mouseout",
          /*mouseout_handler*/
          t[12]
        ),
        Ze(
          e,
          "blur",
          /*blur_handler*/
          t[13]
        )
      ], s = !0);
    },
    p(r, _) {
      t = r;
    },
    d(r) {
      r && Z(e), s = !1, En(i);
    }
  };
}
function Ol(t) {
  let e, l, n = (
    /*line*/
    t[20] + ""
  ), o, s, i, a, f = !/*show_legend*/
  t[1] && /*v*/
  t[17].class_or_confidence !== null && Zl(t);
  function r() {
    return (
      /*click_handler*/
      t[14](
        /*i*/
        t[19],
        /*v*/
        t[17]
      )
    );
  }
  return {
    c() {
      e = Q("span"), l = Q("span"), o = Pe(n), s = Ae(), f && f.c(), H(l, "class", "text svelte-1woixh4"), he(
        l,
        "no-label",
        /*v*/
        t[17].class_or_confidence === null || !/*_color_map*/
        t[5][
          /*v*/
          t[17].class_or_confidence
        ]
      ), H(e, "class", "textspan svelte-1woixh4"), he(
        e,
        "no-cat",
        /*v*/
        t[17].class_or_confidence === null || /*active*/
        t[3] && /*active*/
        t[3] !== /*v*/
        t[17].class_or_confidence
      ), he(
        e,
        "hl",
        /*v*/
        t[17].class_or_confidence !== null
      ), he(
        e,
        "selectable",
        /*selectable*/
        t[2]
      ), ll(
        e,
        "background-color",
        /*v*/
        t[17].class_or_confidence === null || /*active*/
        t[3] && /*active*/
        t[3] !== /*v*/
        t[17].class_or_confidence ? "" : (
          /*_color_map*/
          t[5][
            /*v*/
            t[17].class_or_confidence
          ].secondary
        )
      );
    },
    m(_, d) {
      P(_, e, d), ue(e, l), ue(l, o), ue(e, s), f && f.m(e, null), i || (a = Ze(e, "click", r), i = !0);
    },
    p(_, d) {
      t = _, d & /*value*/
      1 && n !== (n = /*line*/
      t[20] + "") && vl(o, n), d & /*value, _color_map*/
      33 && he(
        l,
        "no-label",
        /*v*/
        t[17].class_or_confidence === null || !/*_color_map*/
        t[5][
          /*v*/
          t[17].class_or_confidence
        ]
      ), !/*show_legend*/
      t[1] && /*v*/
      t[17].class_or_confidence !== null ? f ? f.p(t, d) : (f = Zl(t), f.c(), f.m(e, null)) : f && (f.d(1), f = null), d & /*value, active*/
      9 && he(
        e,
        "no-cat",
        /*v*/
        t[17].class_or_confidence === null || /*active*/
        t[3] && /*active*/
        t[3] !== /*v*/
        t[17].class_or_confidence
      ), d & /*value*/
      1 && he(
        e,
        "hl",
        /*v*/
        t[17].class_or_confidence !== null
      ), d & /*selectable*/
      4 && he(
        e,
        "selectable",
        /*selectable*/
        t[2]
      ), d & /*value, active*/
      9 && ll(
        e,
        "background-color",
        /*v*/
        t[17].class_or_confidence === null || /*active*/
        t[3] && /*active*/
        t[3] !== /*v*/
        t[17].class_or_confidence ? "" : (
          /*_color_map*/
          t[5][
            /*v*/
            t[17].class_or_confidence
          ].secondary
        )
      );
    },
    d(_) {
      _ && Z(e), f && f.d(), i = !1, a();
    }
  };
}
function Zl(t) {
  let e, l, n = (
    /*v*/
    t[17].class_or_confidence + ""
  ), o;
  return {
    c() {
      e = Pe(` 
								`), l = Q("span"), o = Pe(n), H(l, "class", "label svelte-1woixh4"), ll(
        l,
        "background-color",
        /*v*/
        t[17].class_or_confidence === null || /*active*/
        t[3] && /*active*/
        t[3] !== /*v*/
        t[17].class_or_confidence ? "" : (
          /*_color_map*/
          t[5][
            /*v*/
            t[17].class_or_confidence
          ].primary
        )
      );
    },
    m(s, i) {
      P(s, e, i), P(s, l, i), ue(l, o);
    },
    p(s, i) {
      i & /*value*/
      1 && n !== (n = /*v*/
      s[17].class_or_confidence + "") && vl(o, n), i & /*value, active*/
      9 && ll(
        l,
        "background-color",
        /*v*/
        s[17].class_or_confidence === null || /*active*/
        s[3] && /*active*/
        s[3] !== /*v*/
        s[17].class_or_confidence ? "" : (
          /*_color_map*/
          s[5][
            /*v*/
            s[17].class_or_confidence
          ].primary
        )
      );
    },
    d(s) {
      s && (Z(e), Z(l));
    }
  };
}
function Pl(t) {
  let e;
  return {
    c() {
      e = Q("br");
    },
    m(l, n) {
      P(l, e, n);
    },
    d(l) {
      l && Z(e);
    }
  };
}
function Rl(t) {
  let e = (
    /*line*/
    t[20].trim() !== ""
  ), l, n = (
    /*j*/
    t[22] < tl(
      /*v*/
      t[17].token
    ).length - 1
  ), o, s = e && Ol(t), i = n && Pl();
  return {
    c() {
      s && s.c(), l = Ae(), i && i.c(), o = Ot();
    },
    m(a, f) {
      s && s.m(a, f), P(a, l, f), i && i.m(a, f), P(a, o, f);
    },
    p(a, f) {
      f & /*value*/
      1 && (e = /*line*/
      a[20].trim() !== ""), e ? s ? s.p(a, f) : (s = Ol(a), s.c(), s.m(l.parentNode, l)) : s && (s.d(1), s = null), f & /*value*/
      1 && (n = /*j*/
      a[22] < tl(
        /*v*/
        a[17].token
      ).length - 1), n ? i || (i = Pl(), i.c(), i.m(o.parentNode, o)) : i && (i.d(1), i = null);
    },
    d(a) {
      a && (Z(l), Z(o)), s && s.d(a), i && i.d(a);
    }
  };
}
function Dl(t) {
  let e, l = we(tl(
    /*v*/
    t[17].token
  )), n = [];
  for (let o = 0; o < l.length; o += 1)
    n[o] = Rl(Tl(t, l, o));
  return {
    c() {
      for (let o = 0; o < n.length; o += 1)
        n[o].c();
      e = Ot();
    },
    m(o, s) {
      for (let i = 0; i < n.length; i += 1)
        n[i] && n[i].m(o, s);
      P(o, e, s);
    },
    p(o, s) {
      if (s & /*splitTextByNewline, value, active, selectable, _color_map, dispatch, show_legend*/
      111) {
        l = we(tl(
          /*v*/
          o[17].token
        ));
        let i;
        for (i = 0; i < l.length; i += 1) {
          const a = Tl(o, l, i);
          n[i] ? n[i].p(a, s) : (n[i] = Rl(a), n[i].c(), n[i].m(e.parentNode, e));
        }
        for (; i < n.length; i += 1)
          n[i].d(1);
        n.length = l.length;
      }
    },
    d(o) {
      o && Z(e), fl(n, o);
    }
  };
}
function Fn(t) {
  let e;
  function l(s, i) {
    return (
      /*mode*/
      s[4] === "categories" ? Mn : Vn
    );
  }
  let n = l(t), o = n(t);
  return {
    c() {
      e = Q("div"), o.c(), H(e, "class", "container svelte-1woixh4");
    },
    m(s, i) {
      P(s, e, i), o.m(e, null);
    },
    p(s, [i]) {
      n === (n = l(s)) && o ? o.p(s, i) : (o.d(1), o = n(s), o && (o.c(), o.m(e, null)));
    },
    i: Vl,
    o: Vl,
    d(s) {
      s && Z(e), o.d();
    }
  };
}
function tl(t) {
  return t.split(`
`);
}
function Tn(t, e, l) {
  const n = typeof document < "u";
  let { value: o = [] } = e, { show_legend: s = !1 } = e, { color_map: i = {} } = e, { selectable: a = !1 } = e, f, r = {}, _ = "";
  const d = jn();
  let p;
  function b(g) {
    l(3, _ = g);
  }
  function c() {
    l(3, _ = "");
  }
  const h = (g) => b(g), v = (g) => b(g), L = () => c(), y = () => c(), u = (g, N) => {
    d("select", {
      index: g,
      value: [N.token, N.class_or_confidence]
    });
  };
  return t.$$set = (g) => {
    "value" in g && l(0, o = g.value), "show_legend" in g && l(1, s = g.show_legend), "color_map" in g && l(9, i = g.color_map), "selectable" in g && l(2, a = g.selectable);
  }, t.$$.update = () => {
    if (t.$$.dirty & /*color_map, value*/
    513) {
      if (i || l(9, i = {}), o.length > 0) {
        for (let g of o)
          if (g.class_or_confidence !== null)
            if (typeof g.class_or_confidence == "string") {
              if (l(4, p = "categories"), !(g.class_or_confidence in i)) {
                let N = At(Object.keys(i).length);
                l(9, i[g.class_or_confidence] = N, i);
              }
            } else
              l(4, p = "scores");
      }
      Bt(i, r, n, f);
    }
  }, [
    o,
    s,
    a,
    _,
    p,
    r,
    d,
    b,
    c,
    i,
    h,
    v,
    L,
    y,
    u
  ];
}
class In extends qn {
  constructor(e) {
    super(), Ln(this, e, Tn, Fn, Nn, {
      value: 0,
      show_legend: 1,
      color_map: 9,
      selectable: 2
    });
  }
}
const {
  SvelteComponent: zn,
  attr: oe,
  detach: yl,
  element: Zt,
  empty: An,
  init: Bn,
  insert: Cl,
  listen: Ce,
  noop: Yl,
  run_all: Pt,
  safe_not_equal: Hn,
  set_style: Me
} = window.__gradio__svelte__internal;
function On(t) {
  let e, l, n, o;
  return {
    c() {
      e = Zt("input"), oe(e, "class", "label-input svelte-df6jzs"), e.autofocus = !0, oe(e, "type", "number"), oe(e, "step", "0.1"), oe(e, "style", l = "background-color: rgba(" + (typeof /*category*/
      t[1] == "number" && /*category*/
      t[1] < 0 ? "128, 90, 213," + -/*category*/
      t[1] : "239, 68, 60," + /*category*/
      t[1]) + ")"), e.value = /*category*/
      t[1], Me(e, "width", "7ch");
    },
    m(s, i) {
      Cl(s, e, i), e.focus(), n || (o = [
        Ce(
          e,
          "input",
          /*handleInput*/
          t[8]
        ),
        Ce(
          e,
          "blur",
          /*blur_handler_1*/
          t[14]
        ),
        Ce(
          e,
          "keydown",
          /*keydown_handler_1*/
          t[15]
        )
      ], n = !0);
    },
    p(s, i) {
      i & /*category*/
      2 && l !== (l = "background-color: rgba(" + (typeof /*category*/
      s[1] == "number" && /*category*/
      s[1] < 0 ? "128, 90, 213," + -/*category*/
      s[1] : "239, 68, 60," + /*category*/
      s[1]) + ")") && oe(e, "style", l), i & /*category*/
      2 && e.value !== /*category*/
      s[1] && (e.value = /*category*/
      s[1]);
      const a = i & /*category*/
      2;
      (i & /*category*/
      2 || a) && Me(e, "width", "7ch");
    },
    d(s) {
      s && yl(e), n = !1, Pt(o);
    }
  };
}
function Zn(t) {
  let e, l, n, o;
  return {
    c() {
      var s;
      e = Zt("input"), oe(e, "class", "label-input svelte-df6jzs"), e.autofocus = !0, oe(e, "id", l = `label-input-${/*indexOfLabel*/
      t[3]}`), oe(e, "type", "text"), oe(e, "placeholder", "label"), e.value = /*category*/
      t[1], Me(
        e,
        "background-color",
        /*category*/
        t[1] === null || /*active*/
        t[2] && /*active*/
        t[2] !== /*category*/
        t[1] ? "" : (
          /*_color_map*/
          t[6][
            /*category*/
            t[1]
          ].primary
        )
      ), Me(
        e,
        "width",
        /*_input_value*/
        t[7] ? (
          /*_input_value*/
          ((s = t[7].toString()) == null ? void 0 : s.length) + 4 + "ch"
        ) : "8ch"
      );
    },
    m(s, i) {
      Cl(s, e, i), e.focus(), n || (o = [
        Ce(
          e,
          "input",
          /*handleInput*/
          t[8]
        ),
        Ce(
          e,
          "blur",
          /*blur_handler*/
          t[12]
        ),
        Ce(
          e,
          "keydown",
          /*keydown_handler*/
          t[13]
        ),
        Ce(e, "focus", Rn)
      ], n = !0);
    },
    p(s, i) {
      var a;
      i & /*indexOfLabel*/
      8 && l !== (l = `label-input-${/*indexOfLabel*/
      s[3]}`) && oe(e, "id", l), i & /*category*/
      2 && e.value !== /*category*/
      s[1] && (e.value = /*category*/
      s[1]), i & /*category, active, _color_map*/
      70 && Me(
        e,
        "background-color",
        /*category*/
        s[1] === null || /*active*/
        s[2] && /*active*/
        s[2] !== /*category*/
        s[1] ? "" : (
          /*_color_map*/
          s[6][
            /*category*/
            s[1]
          ].primary
        )
      ), i & /*_input_value*/
      128 && Me(
        e,
        "width",
        /*_input_value*/
        s[7] ? (
          /*_input_value*/
          ((a = s[7].toString()) == null ? void 0 : a.length) + 4 + "ch"
        ) : "8ch"
      );
    },
    d(s) {
      s && yl(e), n = !1, Pt(o);
    }
  };
}
function Pn(t) {
  let e;
  function l(s, i) {
    return (
      /*isScoresMode*/
      s[5] ? On : Zn
    );
  }
  let n = l(t), o = n(t);
  return {
    c() {
      o.c(), e = An();
    },
    m(s, i) {
      o.m(s, i), Cl(s, e, i);
    },
    p(s, [i]) {
      n === (n = l(s)) && o ? o.p(s, i) : (o.d(1), o = n(s), o && (o.c(), o.m(e.parentNode, e)));
    },
    i: Yl,
    o: Yl,
    d(s) {
      s && yl(e), o.d(s);
    }
  };
}
function Rn(t) {
  let e = t.target;
  e && e.placeholder && (e.placeholder = "");
}
function Dn(t, e, l) {
  let { value: n } = e, { category: o } = e, { active: s } = e, { labelToEdit: i } = e, { indexOfLabel: a } = e, { text: f } = e, { handleValueChange: r } = e, { isScoresMode: _ = !1 } = e, { _color_map: d } = e, p = o;
  function b(u) {
    let g = u.target;
    g && l(7, p = g.value);
  }
  function c(u, g, N) {
    let k = u.target;
    l(10, n = [
      ...n.slice(0, g),
      {
        token: N,
        class_or_confidence: k.value === "" ? null : _ ? Number(k.value) : k.value
      },
      ...n.slice(g + 1)
    ]), r();
  }
  const h = (u) => c(u, a, f), v = (u) => {
    u.key === "Enter" && (c(u, a, f), l(0, i = -1));
  }, L = (u) => c(u, a, f), y = (u) => {
    u.key === "Enter" && (c(u, a, f), l(0, i = -1));
  };
  return t.$$set = (u) => {
    "value" in u && l(10, n = u.value), "category" in u && l(1, o = u.category), "active" in u && l(2, s = u.active), "labelToEdit" in u && l(0, i = u.labelToEdit), "indexOfLabel" in u && l(3, a = u.indexOfLabel), "text" in u && l(4, f = u.text), "handleValueChange" in u && l(11, r = u.handleValueChange), "isScoresMode" in u && l(5, _ = u.isScoresMode), "_color_map" in u && l(6, d = u._color_map);
  }, [
    i,
    o,
    s,
    a,
    f,
    _,
    d,
    p,
    b,
    c,
    n,
    r,
    h,
    v,
    L,
    y
  ];
}
class Rt extends zn {
  constructor(e) {
    super(), Bn(this, e, Dn, Pn, Hn, {
      value: 10,
      category: 1,
      active: 2,
      labelToEdit: 0,
      indexOfLabel: 3,
      text: 4,
      handleValueChange: 11,
      isScoresMode: 5,
      _color_map: 6
    });
  }
}
const {
  SvelteComponent: Yn,
  add_flush_callback: Dt,
  append: D,
  attr: E,
  bind: Yt,
  binding_callbacks: Ut,
  check_outros: Ee,
  create_component: Xt,
  destroy_component: Gt,
  destroy_each: al,
  detach: A,
  element: O,
  empty: Sl,
  ensure_array_like: ve,
  group_outros: Ne,
  init: Un,
  insert: B,
  listen: T,
  mount_component: Kt,
  run_all: Be,
  safe_not_equal: Xn,
  set_data: rl,
  set_style: nl,
  space: ae,
  text: Ye,
  toggle_class: K,
  transition_in: z,
  transition_out: R
} = window.__gradio__svelte__internal, { createEventDispatcher: Gn, onMount: Kn } = window.__gradio__svelte__internal;
function Ul(t, e, l) {
  const n = t.slice();
  n[46] = e[l].token, n[47] = e[l].class_or_confidence, n[49] = l;
  const o = typeof /*class_or_confidence*/
  n[47] == "string" ? parseInt(
    /*class_or_confidence*/
    n[47]
  ) : (
    /*class_or_confidence*/
    n[47]
  );
  return n[55] = o, n;
}
function Xl(t, e, l) {
  const n = t.slice();
  return n[46] = e[l].token, n[47] = e[l].class_or_confidence, n[49] = l, n;
}
function Gl(t, e, l) {
  const n = t.slice();
  return n[50] = e[l], n[52] = l, n;
}
function Kl(t, e, l) {
  const n = t.slice();
  return n[47] = e[l][0], n[53] = e[l][1], n[49] = l, n;
}
function Jn(t) {
  let e, l, n, o = (
    /*show_legend*/
    t[1] && Jl()
  ), s = ve(
    /*value*/
    t[0]
  ), i = [];
  for (let f = 0; f < s.length; f += 1)
    i[f] = $l(Ul(t, s, f));
  const a = (f) => R(i[f], 1, 1, () => {
    i[f] = null;
  });
  return {
    c() {
      o && o.c(), e = ae(), l = O("div");
      for (let f = 0; f < i.length; f += 1)
        i[f].c();
      E(l, "class", "textfield svelte-u7mykt"), E(l, "data-testid", "highlighted-text:textfield");
    },
    m(f, r) {
      o && o.m(f, r), B(f, e, r), B(f, l, r);
      for (let _ = 0; _ < i.length; _ += 1)
        i[_] && i[_].m(l, null);
      n = !0;
    },
    p(f, r) {
      if (/*show_legend*/
      f[1] ? o || (o = Jl(), o.c(), o.m(e.parentNode, e)) : o && (o.d(1), o = null), r[0] & /*removeHighlightedText, value, activeElementIndex, active, labelToEdit, _color_map, handleValueChange*/
      889) {
        s = ve(
          /*value*/
          f[0]
        );
        let _;
        for (_ = 0; _ < s.length; _ += 1) {
          const d = Ul(f, s, _);
          i[_] ? (i[_].p(d, r), z(i[_], 1)) : (i[_] = $l(d), i[_].c(), z(i[_], 1), i[_].m(l, null));
        }
        for (Ne(), _ = s.length; _ < i.length; _ += 1)
          a(_);
        Ee();
      }
    },
    i(f) {
      if (!n) {
        for (let r = 0; r < s.length; r += 1)
          z(i[r]);
        n = !0;
      }
    },
    o(f) {
      i = i.filter(Boolean);
      for (let r = 0; r < i.length; r += 1)
        R(i[r]);
      n = !1;
    },
    d(f) {
      f && (A(e), A(l)), o && o.d(f), al(i, f);
    }
  };
}
function Qn(t) {
  let e, l, n, o = (
    /*show_legend*/
    t[1] && xl(t)
  ), s = ve(
    /*value*/
    t[0]
  ), i = [];
  for (let f = 0; f < s.length; f += 1)
    i[f] = at(Xl(t, s, f));
  const a = (f) => R(i[f], 1, 1, () => {
    i[f] = null;
  });
  return {
    c() {
      o && o.c(), e = ae(), l = O("div");
      for (let f = 0; f < i.length; f += 1)
        i[f].c();
      E(l, "class", "textfield svelte-u7mykt");
    },
    m(f, r) {
      o && o.m(f, r), B(f, e, r), B(f, l, r);
      for (let _ = 0; _ < i.length; _ += 1)
        i[_] && i[_].m(l, null);
      n = !0;
    },
    p(f, r) {
      if (/*show_legend*/
      f[1] ? o ? o.p(f, r) : (o = xl(f), o.c(), o.m(e.parentNode, e)) : o && (o.d(1), o = null), r[0] & /*value, removeHighlightedText, active, selectable, _color_map, handleSelect, labelToEdit, handleKeydownSelection, activeElementIndex, handleValueChange, show_legend*/
      13183) {
        s = ve(
          /*value*/
          f[0]
        );
        let _;
        for (_ = 0; _ < s.length; _ += 1) {
          const d = Xl(f, s, _);
          i[_] ? (i[_].p(d, r), z(i[_], 1)) : (i[_] = at(d), i[_].c(), z(i[_], 1), i[_].m(l, null));
        }
        for (Ne(), _ = s.length; _ < i.length; _ += 1)
          a(_);
        Ee();
      }
    },
    i(f) {
      if (!n) {
        for (let r = 0; r < s.length; r += 1)
          z(i[r]);
        n = !0;
      }
    },
    o(f) {
      i = i.filter(Boolean);
      for (let r = 0; r < i.length; r += 1)
        R(i[r]);
      n = !1;
    },
    d(f) {
      f && (A(e), A(l)), o && o.d(f), al(i, f);
    }
  };
}
function Jl(t) {
  let e;
  return {
    c() {
      e = O("div"), e.innerHTML = "<span>-1</span> <span>0</span> <span>+1</span>", E(e, "class", "color-legend svelte-u7mykt"), E(e, "data-testid", "highlighted-text:color-legend");
    },
    m(l, n) {
      B(l, e, n);
    },
    d(l) {
      l && A(e);
    }
  };
}
function Ql(t) {
  let e, l, n;
  function o(i) {
    t[33](i);
  }
  let s = {
    labelToEdit: (
      /*labelToEdit*/
      t[6]
    ),
    _color_map: (
      /*_color_map*/
      t[3]
    ),
    category: (
      /*class_or_confidence*/
      t[47]
    ),
    active: (
      /*active*/
      t[5]
    ),
    indexOfLabel: (
      /*i*/
      t[49]
    ),
    text: (
      /*token*/
      t[46]
    ),
    handleValueChange: (
      /*handleValueChange*/
      t[9]
    ),
    isScoresMode: !0
  };
  return (
    /*value*/
    t[0] !== void 0 && (s.value = /*value*/
    t[0]), e = new Rt({ props: s }), Ut.push(() => Yt(e, "value", o)), {
      c() {
        Xt(e.$$.fragment);
      },
      m(i, a) {
        Kt(e, i, a), n = !0;
      },
      p(i, a) {
        const f = {};
        a[0] & /*labelToEdit*/
        64 && (f.labelToEdit = /*labelToEdit*/
        i[6]), a[0] & /*_color_map*/
        8 && (f._color_map = /*_color_map*/
        i[3]), a[0] & /*value*/
        1 && (f.category = /*class_or_confidence*/
        i[47]), a[0] & /*active*/
        32 && (f.active = /*active*/
        i[5]), a[0] & /*value*/
        1 && (f.text = /*token*/
        i[46]), !l && a[0] & /*value*/
        1 && (l = !0, f.value = /*value*/
        i[0], Dt(() => l = !1)), e.$set(f);
      },
      i(i) {
        n || (z(e.$$.fragment, i), n = !0);
      },
      o(i) {
        R(e.$$.fragment, i), n = !1;
      },
      d(i) {
        Gt(e, i);
      }
    }
  );
}
function Wl(t) {
  let e, l, n;
  function o() {
    return (
      /*click_handler_5*/
      t[38](
        /*i*/
        t[49]
      )
    );
  }
  function s(...i) {
    return (
      /*keydown_handler_5*/
      t[39](
        /*i*/
        t[49],
        ...i
      )
    );
  }
  return {
    c() {
      e = O("span"), e.textContent = "×", E(e, "class", "label-clear-button svelte-u7mykt"), E(e, "role", "button"), E(e, "aria-roledescription", "Remove label from text"), E(e, "tabindex", "0");
    },
    m(i, a) {
      B(i, e, a), l || (n = [
        T(e, "click", o),
        T(e, "keydown", s)
      ], l = !0);
    },
    p(i, a) {
      t = i;
    },
    d(i) {
      i && A(e), l = !1, Be(n);
    }
  };
}
function $l(t) {
  let e, l, n, o = (
    /*token*/
    t[46] + ""
  ), s, i, a, f, r, _, d, p, b = (
    /*class_or_confidence*/
    t[47] && /*labelToEdit*/
    t[6] === /*i*/
    t[49] && Ql(t)
  );
  function c() {
    return (
      /*mouseover_handler_3*/
      t[34](
        /*i*/
        t[49]
      )
    );
  }
  function h() {
    return (
      /*focus_handler_3*/
      t[35](
        /*i*/
        t[49]
      )
    );
  }
  function v() {
    return (
      /*click_handler_4*/
      t[36](
        /*i*/
        t[49]
      )
    );
  }
  function L(...u) {
    return (
      /*keydown_handler_4*/
      t[37](
        /*i*/
        t[49],
        ...u
      )
    );
  }
  let y = (
    /*class_or_confidence*/
    t[47] && /*activeElementIndex*/
    t[4] === /*i*/
    t[49] && Wl(t)
  );
  return {
    c() {
      e = O("span"), l = O("span"), n = O("span"), s = Ye(o), i = ae(), b && b.c(), f = ae(), y && y.c(), r = ae(), E(n, "class", "text svelte-u7mykt"), E(l, "class", "textspan score-text svelte-u7mykt"), E(l, "role", "button"), E(l, "tabindex", "0"), E(l, "style", a = "background-color: rgba(" + /*score*/
      (t[55] && /*score*/
      t[55] < 0 ? "128, 90, 213," + -/*score*/
      t[55] : "239, 68, 60," + /*score*/
      t[55]) + ")"), K(
        l,
        "no-cat",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47]
      ), K(
        l,
        "hl",
        /*class_or_confidence*/
        t[47] !== null
      ), E(e, "class", "score-text-container svelte-u7mykt");
    },
    m(u, g) {
      B(u, e, g), D(e, l), D(l, n), D(n, s), D(l, i), b && b.m(l, null), D(e, f), y && y.m(e, null), D(e, r), _ = !0, d || (p = [
        T(l, "mouseover", c),
        T(l, "focus", h),
        T(l, "click", v),
        T(l, "keydown", L)
      ], d = !0);
    },
    p(u, g) {
      t = u, (!_ || g[0] & /*value*/
      1) && o !== (o = /*token*/
      t[46] + "") && rl(s, o), /*class_or_confidence*/
      t[47] && /*labelToEdit*/
      t[6] === /*i*/
      t[49] ? b ? (b.p(t, g), g[0] & /*value, labelToEdit*/
      65 && z(b, 1)) : (b = Ql(t), b.c(), z(b, 1), b.m(l, null)) : b && (Ne(), R(b, 1, 1, () => {
        b = null;
      }), Ee()), (!_ || g[0] & /*value*/
      1 && a !== (a = "background-color: rgba(" + /*score*/
      (t[55] && /*score*/
      t[55] < 0 ? "128, 90, 213," + -/*score*/
      t[55] : "239, 68, 60," + /*score*/
      t[55]) + ")")) && E(l, "style", a), (!_ || g[0] & /*value, active*/
      33) && K(
        l,
        "no-cat",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47]
      ), (!_ || g[0] & /*value*/
      1) && K(
        l,
        "hl",
        /*class_or_confidence*/
        t[47] !== null
      ), /*class_or_confidence*/
      t[47] && /*activeElementIndex*/
      t[4] === /*i*/
      t[49] ? y ? y.p(t, g) : (y = Wl(t), y.c(), y.m(e, r)) : y && (y.d(1), y = null);
    },
    i(u) {
      _ || (z(b), _ = !0);
    },
    o(u) {
      R(b), _ = !1;
    },
    d(u) {
      u && A(e), b && b.d(), y && y.d(), d = !1, Be(p);
    }
  };
}
function xl(t) {
  let e, l = (
    /*_color_map*/
    t[3] && et(t)
  );
  return {
    c() {
      e = O("div"), l && l.c(), E(e, "class", "class_or_confidence-legend svelte-u7mykt"), E(e, "data-testid", "highlighted-text:class_or_confidence-legend");
    },
    m(n, o) {
      B(n, e, o), l && l.m(e, null);
    },
    p(n, o) {
      /*_color_map*/
      n[3] ? l ? l.p(n, o) : (l = et(n), l.c(), l.m(e, null)) : l && (l.d(1), l = null);
    },
    d(n) {
      n && A(e), l && l.d();
    }
  };
}
function et(t) {
  let e, l = ve(Object.entries(
    /*_color_map*/
    t[3]
  )), n = [];
  for (let o = 0; o < l.length; o += 1)
    n[o] = lt(Kl(t, l, o));
  return {
    c() {
      for (let o = 0; o < n.length; o += 1)
        n[o].c();
      e = Sl();
    },
    m(o, s) {
      for (let i = 0; i < n.length; i += 1)
        n[i] && n[i].m(o, s);
      B(o, e, s);
    },
    p(o, s) {
      if (s[0] & /*_color_map, handle_mouseover, handle_mouseout*/
      3080) {
        l = ve(Object.entries(
          /*_color_map*/
          o[3]
        ));
        let i;
        for (i = 0; i < l.length; i += 1) {
          const a = Kl(o, l, i);
          n[i] ? n[i].p(a, s) : (n[i] = lt(a), n[i].c(), n[i].m(e.parentNode, e));
        }
        for (; i < n.length; i += 1)
          n[i].d(1);
        n.length = l.length;
      }
    },
    d(o) {
      o && A(e), al(n, o);
    }
  };
}
function lt(t) {
  let e, l = (
    /*class_or_confidence*/
    t[47] + ""
  ), n, o, s, i, a;
  function f() {
    return (
      /*mouseover_handler*/
      t[16](
        /*class_or_confidence*/
        t[47]
      )
    );
  }
  function r() {
    return (
      /*focus_handler*/
      t[17](
        /*class_or_confidence*/
        t[47]
      )
    );
  }
  return {
    c() {
      e = O("div"), n = Ye(l), o = ae(), E(e, "role", "button"), E(e, "aria-roledescription", "Categories of highlighted text. Hover to see text with this class_or_confidence highlighted."), E(e, "tabindex", "0"), E(e, "class", "class_or_confidence-label svelte-u7mykt"), E(e, "style", s = "background-color:" + /*color*/
      t[53].secondary);
    },
    m(_, d) {
      B(_, e, d), D(e, n), D(e, o), i || (a = [
        T(e, "mouseover", f),
        T(e, "focus", r),
        T(
          e,
          "mouseout",
          /*mouseout_handler*/
          t[18]
        ),
        T(
          e,
          "blur",
          /*blur_handler*/
          t[19]
        )
      ], i = !0);
    },
    p(_, d) {
      t = _, d[0] & /*_color_map*/
      8 && l !== (l = /*class_or_confidence*/
      t[47] + "") && rl(n, l), d[0] & /*_color_map*/
      8 && s !== (s = "background-color:" + /*color*/
      t[53].secondary) && E(e, "style", s);
    },
    d(_) {
      _ && A(e), i = !1, Be(a);
    }
  };
}
function tt(t) {
  let e, l, n, o = (
    /*line*/
    t[50] + ""
  ), s, i, a, f, r, _, d;
  function p() {
    return (
      /*focus_handler_1*/
      t[21](
        /*i*/
        t[49]
      )
    );
  }
  function b() {
    return (
      /*mouseover_handler_1*/
      t[22](
        /*i*/
        t[49]
      )
    );
  }
  function c() {
    return (
      /*click_handler*/
      t[23](
        /*i*/
        t[49]
      )
    );
  }
  let h = !/*show_legend*/
  t[1] && /*class_or_confidence*/
  t[47] !== null && /*labelToEdit*/
  t[6] !== /*i*/
  t[49] && nt(t), v = (
    /*labelToEdit*/
    t[6] === /*i*/
    t[49] && /*class_or_confidence*/
    t[47] !== null && it(t)
  );
  function L() {
    return (
      /*click_handler_2*/
      t[27](
        /*class_or_confidence*/
        t[47],
        /*i*/
        t[49],
        /*token*/
        t[46]
      )
    );
  }
  function y(...k) {
    return (
      /*keydown_handler_2*/
      t[28](
        /*class_or_confidence*/
        t[47],
        /*i*/
        t[49],
        /*token*/
        t[46],
        ...k
      )
    );
  }
  function u() {
    return (
      /*focus_handler_2*/
      t[29](
        /*i*/
        t[49]
      )
    );
  }
  function g() {
    return (
      /*mouseover_handler_2*/
      t[30](
        /*i*/
        t[49]
      )
    );
  }
  let N = (
    /*class_or_confidence*/
    t[47] !== null && ot(t)
  );
  return {
    c() {
      e = O("span"), l = O("span"), n = O("span"), s = Ye(o), i = ae(), h && h.c(), a = ae(), v && v.c(), f = ae(), N && N.c(), E(n, "class", "text svelte-u7mykt"), E(n, "role", "button"), E(n, "tabindex", "0"), K(
        n,
        "no-label",
        /*class_or_confidence*/
        t[47] === null
      ), E(l, "role", "button"), E(l, "tabindex", "0"), E(l, "class", "textspan svelte-u7mykt"), K(
        l,
        "no-cat",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47]
      ), K(
        l,
        "hl",
        /*class_or_confidence*/
        t[47] !== null
      ), K(
        l,
        "selectable",
        /*selectable*/
        t[2]
      ), nl(
        l,
        "background-color",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47] ? "" : (
          /*class_or_confidence*/
          t[47] && /*_color_map*/
          t[3][
            /*class_or_confidence*/
            t[47]
          ] ? (
            /*_color_map*/
            t[3][
              /*class_or_confidence*/
              t[47]
            ].secondary
          ) : ""
        )
      ), E(e, "class", "text-class_or_confidence-container svelte-u7mykt");
    },
    m(k, w) {
      B(k, e, w), D(e, l), D(l, n), D(n, s), D(l, i), h && h.m(l, null), D(l, a), v && v.m(l, null), D(e, f), N && N.m(e, null), r = !0, _ || (d = [
        T(
          n,
          "keydown",
          /*keydown_handler*/
          t[20]
        ),
        T(n, "focus", p),
        T(n, "mouseover", b),
        T(n, "click", c),
        T(l, "click", L),
        T(l, "keydown", y),
        T(l, "focus", u),
        T(l, "mouseover", g)
      ], _ = !0);
    },
    p(k, w) {
      t = k, (!r || w[0] & /*value*/
      1) && o !== (o = /*line*/
      t[50] + "") && rl(s, o), (!r || w[0] & /*value*/
      1) && K(
        n,
        "no-label",
        /*class_or_confidence*/
        t[47] === null
      ), !/*show_legend*/
      t[1] && /*class_or_confidence*/
      t[47] !== null && /*labelToEdit*/
      t[6] !== /*i*/
      t[49] ? h ? h.p(t, w) : (h = nt(t), h.c(), h.m(l, a)) : h && (h.d(1), h = null), /*labelToEdit*/
      t[6] === /*i*/
      t[49] && /*class_or_confidence*/
      t[47] !== null ? v ? (v.p(t, w), w[0] & /*labelToEdit, value*/
      65 && z(v, 1)) : (v = it(t), v.c(), z(v, 1), v.m(l, null)) : v && (Ne(), R(v, 1, 1, () => {
        v = null;
      }), Ee()), (!r || w[0] & /*value, active*/
      33) && K(
        l,
        "no-cat",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47]
      ), (!r || w[0] & /*value*/
      1) && K(
        l,
        "hl",
        /*class_or_confidence*/
        t[47] !== null
      ), (!r || w[0] & /*selectable*/
      4) && K(
        l,
        "selectable",
        /*selectable*/
        t[2]
      ), w[0] & /*value, active, _color_map*/
      41 && nl(
        l,
        "background-color",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47] ? "" : (
          /*class_or_confidence*/
          t[47] && /*_color_map*/
          t[3][
            /*class_or_confidence*/
            t[47]
          ] ? (
            /*_color_map*/
            t[3][
              /*class_or_confidence*/
              t[47]
            ].secondary
          ) : ""
        )
      ), /*class_or_confidence*/
      t[47] !== null ? N ? N.p(t, w) : (N = ot(t), N.c(), N.m(e, null)) : N && (N.d(1), N = null);
    },
    i(k) {
      r || (z(v), r = !0);
    },
    o(k) {
      R(v), r = !1;
    },
    d(k) {
      k && A(e), h && h.d(), v && v.d(), N && N.d(), _ = !1, Be(d);
    }
  };
}
function nt(t) {
  let e, l = (
    /*class_or_confidence*/
    t[47] + ""
  ), n, o, s;
  function i() {
    return (
      /*click_handler_1*/
      t[24](
        /*i*/
        t[49]
      )
    );
  }
  function a() {
    return (
      /*keydown_handler_1*/
      t[25](
        /*i*/
        t[49]
      )
    );
  }
  return {
    c() {
      e = O("span"), n = Ye(l), E(e, "id", `label-tag-${/*i*/
      t[49]}`), E(e, "class", "label svelte-u7mykt"), E(e, "role", "button"), E(e, "tabindex", "0"), nl(
        e,
        "background-color",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47] ? "" : (
          /*_color_map*/
          t[3][
            /*class_or_confidence*/
            t[47]
          ].primary
        )
      );
    },
    m(f, r) {
      B(f, e, r), D(e, n), o || (s = [
        T(e, "click", i),
        T(e, "keydown", a)
      ], o = !0);
    },
    p(f, r) {
      t = f, r[0] & /*value*/
      1 && l !== (l = /*class_or_confidence*/
      t[47] + "") && rl(n, l), r[0] & /*value, active, _color_map*/
      41 && nl(
        e,
        "background-color",
        /*class_or_confidence*/
        t[47] === null || /*active*/
        t[5] && /*active*/
        t[5] !== /*class_or_confidence*/
        t[47] ? "" : (
          /*_color_map*/
          t[3][
            /*class_or_confidence*/
            t[47]
          ].primary
        )
      );
    },
    d(f) {
      f && A(e), o = !1, Be(s);
    }
  };
}
function it(t) {
  let e, l, n, o;
  function s(a) {
    t[26](a);
  }
  let i = {
    labelToEdit: (
      /*labelToEdit*/
      t[6]
    ),
    category: (
      /*class_or_confidence*/
      t[47]
    ),
    active: (
      /*active*/
      t[5]
    ),
    _color_map: (
      /*_color_map*/
      t[3]
    ),
    indexOfLabel: (
      /*i*/
      t[49]
    ),
    text: (
      /*token*/
      t[46]
    ),
    handleValueChange: (
      /*handleValueChange*/
      t[9]
    )
  };
  return (
    /*value*/
    t[0] !== void 0 && (i.value = /*value*/
    t[0]), l = new Rt({ props: i }), Ut.push(() => Yt(l, "value", s)), {
      c() {
        e = Ye(` 
									`), Xt(l.$$.fragment);
      },
      m(a, f) {
        B(a, e, f), Kt(l, a, f), o = !0;
      },
      p(a, f) {
        const r = {};
        f[0] & /*labelToEdit*/
        64 && (r.labelToEdit = /*labelToEdit*/
        a[6]), f[0] & /*value*/
        1 && (r.category = /*class_or_confidence*/
        a[47]), f[0] & /*active*/
        32 && (r.active = /*active*/
        a[5]), f[0] & /*_color_map*/
        8 && (r._color_map = /*_color_map*/
        a[3]), f[0] & /*value*/
        1 && (r.text = /*token*/
        a[46]), !n && f[0] & /*value*/
        1 && (n = !0, r.value = /*value*/
        a[0], Dt(() => n = !1)), l.$set(r);
      },
      i(a) {
        o || (z(l.$$.fragment, a), o = !0);
      },
      o(a) {
        R(l.$$.fragment, a), o = !1;
      },
      d(a) {
        a && A(e), Gt(l, a);
      }
    }
  );
}
function ot(t) {
  let e, l, n;
  function o() {
    return (
      /*click_handler_3*/
      t[31](
        /*i*/
        t[49]
      )
    );
  }
  function s(...i) {
    return (
      /*keydown_handler_3*/
      t[32](
        /*i*/
        t[49],
        ...i
      )
    );
  }
  return {
    c() {
      e = O("span"), e.textContent = "×", E(e, "class", "label-clear-button svelte-u7mykt"), E(e, "role", "button"), E(e, "aria-roledescription", "Remove label from text"), E(e, "tabindex", "0");
    },
    m(i, a) {
      B(i, e, a), l || (n = [
        T(e, "click", o),
        T(e, "keydown", s)
      ], l = !0);
    },
    p(i, a) {
      t = i;
    },
    d(i) {
      i && A(e), l = !1, Be(n);
    }
  };
}
function st(t) {
  let e;
  return {
    c() {
      e = O("br");
    },
    m(l, n) {
      B(l, e, n);
    },
    d(l) {
      l && A(e);
    }
  };
}
function ft(t) {
  let e = (
    /*line*/
    t[50].trim() !== ""
  ), l, n = (
    /*j*/
    t[52] < il(
      /*token*/
      t[46]
    ).length - 1
  ), o, s, i = e && tt(t), a = n && st();
  return {
    c() {
      i && i.c(), l = ae(), a && a.c(), o = Sl();
    },
    m(f, r) {
      i && i.m(f, r), B(f, l, r), a && a.m(f, r), B(f, o, r), s = !0;
    },
    p(f, r) {
      r[0] & /*value*/
      1 && (e = /*line*/
      f[50].trim() !== ""), e ? i ? (i.p(f, r), r[0] & /*value*/
      1 && z(i, 1)) : (i = tt(f), i.c(), z(i, 1), i.m(l.parentNode, l)) : i && (Ne(), R(i, 1, 1, () => {
        i = null;
      }), Ee()), r[0] & /*value*/
      1 && (n = /*j*/
      f[52] < il(
        /*token*/
        f[46]
      ).length - 1), n ? a || (a = st(), a.c(), a.m(o.parentNode, o)) : a && (a.d(1), a = null);
    },
    i(f) {
      s || (z(i), s = !0);
    },
    o(f) {
      R(i), s = !1;
    },
    d(f) {
      f && (A(l), A(o)), i && i.d(f), a && a.d(f);
    }
  };
}
function at(t) {
  let e, l, n = ve(il(
    /*token*/
    t[46]
  )), o = [];
  for (let i = 0; i < n.length; i += 1)
    o[i] = ft(Gl(t, n, i));
  const s = (i) => R(o[i], 1, 1, () => {
    o[i] = null;
  });
  return {
    c() {
      for (let i = 0; i < o.length; i += 1)
        o[i].c();
      e = Sl();
    },
    m(i, a) {
      for (let f = 0; f < o.length; f += 1)
        o[f] && o[f].m(i, a);
      B(i, e, a), l = !0;
    },
    p(i, a) {
      if (a[0] & /*value, removeHighlightedText, active, selectable, _color_map, handleSelect, labelToEdit, handleKeydownSelection, activeElementIndex, handleValueChange, show_legend*/
      13183) {
        n = ve(il(
          /*token*/
          i[46]
        ));
        let f;
        for (f = 0; f < n.length; f += 1) {
          const r = Gl(i, n, f);
          o[f] ? (o[f].p(r, a), z(o[f], 1)) : (o[f] = ft(r), o[f].c(), z(o[f], 1), o[f].m(e.parentNode, e));
        }
        for (Ne(), f = n.length; f < o.length; f += 1)
          s(f);
        Ee();
      }
    },
    i(i) {
      if (!l) {
        for (let a = 0; a < n.length; a += 1)
          z(o[a]);
        l = !0;
      }
    },
    o(i) {
      o = o.filter(Boolean);
      for (let a = 0; a < o.length; a += 1)
        R(o[a]);
      l = !1;
    },
    d(i) {
      i && A(e), al(o, i);
    }
  };
}
function Wn(t) {
  let e, l, n, o;
  const s = [Qn, Jn], i = [];
  function a(f, r) {
    return (
      /*mode*/
      f[7] === "categories" ? 0 : 1
    );
  }
  return l = a(t), n = i[l] = s[l](t), {
    c() {
      e = O("div"), n.c(), E(e, "class", "container svelte-u7mykt");
    },
    m(f, r) {
      B(f, e, r), i[l].m(e, null), o = !0;
    },
    p(f, r) {
      let _ = l;
      l = a(f), l === _ ? i[l].p(f, r) : (Ne(), R(i[_], 1, 1, () => {
        i[_] = null;
      }), Ee(), n = i[l], n ? n.p(f, r) : (n = i[l] = s[l](f), n.c()), z(n, 1), n.m(e, null));
    },
    i(f) {
      o || (z(n), o = !0);
    },
    o(f) {
      R(n), o = !1;
    },
    d(f) {
      f && A(e), i[l].d();
    }
  };
}
function Qe(t) {
  let e, l = t[0], n = 1;
  for (; n < t.length; ) {
    const o = t[n], s = t[n + 1];
    if (n += 2, (o === "optionalAccess" || o === "optionalCall") && l == null)
      return;
    o === "access" || o === "optionalAccess" ? (e = l, l = s(l)) : (o === "call" || o === "optionalCall") && (l = s((...i) => l.call(e, ...i)), e = void 0);
  }
  return l;
}
function il(t) {
  return t.split(`
`);
}
function $n(t, e, l) {
  const n = typeof document < "u";
  let { value: o = [] } = e, { show_legend: s = !1 } = e, { color_map: i = {} } = e, { selectable: a = !1 } = e, { default_label: f } = e, r = -1, _, d = {}, p = "", b, c = -1;
  Kn(() => {
    const m = () => {
      b = window.getSelection(), w(), window.removeEventListener("mouseup", m);
    };
    window.addEventListener("mousedown", () => {
      window.addEventListener("mouseup", m);
    });
  });
  async function h(m, V) {
    if (Qe([b, "optionalAccess", (X) => X.toString, "call", (X) => X()]) && r !== -1 && o[r].token.toString().includes(b.toString())) {
      const X = Symbol(), Oe = o[r].token, [wn, vn, yn] = [
        Oe.substring(0, m),
        Oe.substring(m, V),
        Oe.substring(V)
      ];
      let Je = [
        ...o.slice(0, r),
        { token: wn, class_or_confidence: null },
        {
          token: vn,
          class_or_confidence: u === "scores" ? 1 : f,
          flag: X
        },
        {
          token: yn,
          // add a temp flag to the new highlighted text element
          class_or_confidence: null
        },
        ...o.slice(r + 1)
      ];
      l(6, c = Je.findIndex(({ flag: G }) => G === X)), Je = Je.filter((G) => G.token.trim() !== ""), l(0, o = Je.map(({ flag: G, ...Cn }) => Cn)), y(), Qe([
        document,
        "access",
        (G) => G.getElementById,
        "call",
        (G) => G(`label-input-${c}`),
        "optionalAccess",
        (G) => G.focus,
        "call",
        (G) => G()
      ]);
    }
  }
  const v = Gn();
  function L(m) {
    !o || m < 0 || m >= o.length || (l(0, o[m].class_or_confidence = null, o), l(0, o = Ht(o, "equal")), y(), Qe([
      window,
      "access",
      (V) => V.getSelection,
      "call",
      (V) => V(),
      "optionalAccess",
      (V) => V.empty,
      "call",
      (V) => V()
    ]));
  }
  function y() {
    v("change", o), l(6, c = -1), s && (l(14, i = {}), l(3, d = {}));
  }
  let u;
  function g(m) {
    l(5, p = m);
  }
  function N() {
    l(5, p = "");
  }
  async function k(m) {
    b = window.getSelection(), m.key === "Enter" && w();
  }
  function w() {
    if (b && Qe([
      b,
      "optionalAccess",
      (m) => m.toString,
      "call",
      (m) => m(),
      "access",
      (m) => m.trim,
      "call",
      (m) => m()
    ]) !== "") {
      const m = b.getRangeAt(0).startOffset, V = b.getRangeAt(0).endOffset;
      h(m, V);
    }
  }
  function de(m, V, X) {
    v("select", {
      index: m,
      value: [V, X]
    });
  }
  const re = (m) => g(m), me = (m) => g(m), be = () => N(), Ue = () => N(), _e = (m) => k(m), ye = (m) => l(4, r = m), ne = (m) => l(4, r = m), Xe = (m) => l(6, c = m), cl = (m) => l(6, c = m), Ge = (m) => l(6, c = m);
  function Ke(m) {
    o = m, l(0, o);
  }
  const je = (m, V, X) => {
    m !== null && de(V, X, m);
  }, ul = (m, V, X, Oe) => {
    m !== null ? (l(6, c = V), de(V, X, m)) : k(Oe);
  }, dl = (m) => l(4, r = m), C = (m) => l(4, r = m), cn = (m) => L(m), un = (m, V) => {
    V.key === "Enter" && L(m);
  };
  function dn(m) {
    o = m, l(0, o);
  }
  const mn = (m) => l(4, r = m), bn = (m) => l(4, r = m), hn = (m) => l(6, c = m), gn = (m, V) => {
    V.key === "Enter" && l(6, c = m);
  }, pn = (m) => L(m), kn = (m, V) => {
    V.key === "Enter" && L(m);
  };
  return t.$$set = (m) => {
    "value" in m && l(0, o = m.value), "show_legend" in m && l(1, s = m.show_legend), "color_map" in m && l(14, i = m.color_map), "selectable" in m && l(2, a = m.selectable), "default_label" in m && l(15, f = m.default_label);
  }, t.$$.update = () => {
    if (t.$$.dirty[0] & /*color_map, value, _color_map*/
    16393) {
      if (i || l(14, i = {}), o.length > 0) {
        for (let m of o)
          if (m.class_or_confidence !== null)
            if (typeof m.class_or_confidence == "string") {
              if (l(7, u = "categories"), !(m.class_or_confidence in i)) {
                let V = At(Object.keys(i).length);
                l(14, i[m.class_or_confidence] = V, i);
              }
            } else
              l(7, u = "scores");
      }
      Bt(i, d, n, _);
    }
  }, [
    o,
    s,
    a,
    d,
    r,
    p,
    c,
    u,
    L,
    y,
    g,
    N,
    k,
    de,
    i,
    f,
    re,
    me,
    be,
    Ue,
    _e,
    ye,
    ne,
    Xe,
    cl,
    Ge,
    Ke,
    je,
    ul,
    dl,
    C,
    cn,
    un,
    dn,
    mn,
    bn,
    hn,
    gn,
    pn,
    kn
  ];
}
class xn extends Yn {
  constructor(e) {
    super(), Un(
      this,
      e,
      $n,
      Wn,
      Xn,
      {
        value: 0,
        show_legend: 1,
        color_map: 14,
        selectable: 2,
        default_label: 15
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: ei,
  assign: li,
  create_slot: ti,
  detach: ni,
  element: ii,
  get_all_dirty_from_scope: oi,
  get_slot_changes: si,
  get_spread_update: fi,
  init: ai,
  insert: ri,
  safe_not_equal: _i,
  set_dynamic_element_data: rt,
  set_style: Y,
  toggle_class: ie,
  transition_in: Jt,
  transition_out: Qt,
  update_slot_base: ci
} = window.__gradio__svelte__internal;
function ui(t) {
  let e, l, n;
  const o = (
    /*#slots*/
    t[18].default
  ), s = ti(
    o,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let i = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: l = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-nl1om8"
    }
  ], a = {};
  for (let f = 0; f < i.length; f += 1)
    a = li(a, i[f]);
  return {
    c() {
      e = ii(
        /*tag*/
        t[14]
      ), s && s.c(), rt(
        /*tag*/
        t[14]
      )(e, a), ie(
        e,
        "hidden",
        /*visible*/
        t[10] === !1
      ), ie(
        e,
        "padded",
        /*padding*/
        t[6]
      ), ie(
        e,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), ie(
        e,
        "border_contrast",
        /*border_mode*/
        t[5] === "contrast"
      ), ie(e, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), Y(
        e,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), Y(e, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), Y(
        e,
        "border-style",
        /*variant*/
        t[4]
      ), Y(
        e,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), Y(
        e,
        "flex-grow",
        /*scale*/
        t[12]
      ), Y(e, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), Y(e, "border-width", "var(--block-border-width)");
    },
    m(f, r) {
      ri(f, e, r), s && s.m(e, null), n = !0;
    },
    p(f, r) {
      s && s.p && (!n || r & /*$$scope*/
      131072) && ci(
        s,
        o,
        f,
        /*$$scope*/
        f[17],
        n ? si(
          o,
          /*$$scope*/
          f[17],
          r,
          null
        ) : oi(
          /*$$scope*/
          f[17]
        ),
        null
      ), rt(
        /*tag*/
        f[14]
      )(e, a = fi(i, [
        (!n || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!n || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!n || r & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-nl1om8")) && { class: l }
      ])), ie(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), ie(
        e,
        "padded",
        /*padding*/
        f[6]
      ), ie(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), ie(
        e,
        "border_contrast",
        /*border_mode*/
        f[5] === "contrast"
      ), ie(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), r & /*height*/
      1 && Y(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), r & /*width*/
      2 && Y(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), r & /*variant*/
      16 && Y(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), r & /*allow_overflow*/
      2048 && Y(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && Y(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), r & /*min_width*/
      8192 && Y(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      n || (Jt(s, f), n = !0);
    },
    o(f) {
      Qt(s, f), n = !1;
    },
    d(f) {
      f && ni(e), s && s.d(f);
    }
  };
}
function di(t) {
  let e, l = (
    /*tag*/
    t[14] && ui(t)
  );
  return {
    c() {
      l && l.c();
    },
    m(n, o) {
      l && l.m(n, o), e = !0;
    },
    p(n, [o]) {
      /*tag*/
      n[14] && l.p(n, o);
    },
    i(n) {
      e || (Jt(l, n), e = !0);
    },
    o(n) {
      Qt(l, n), e = !1;
    },
    d(n) {
      l && l.d(n);
    }
  };
}
function mi(t, e, l) {
  let { $$slots: n = {}, $$scope: o } = e, { height: s = void 0 } = e, { width: i = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: f = [] } = e, { variant: r = "solid" } = e, { border_mode: _ = "base" } = e, { padding: d = !0 } = e, { type: p = "normal" } = e, { test_id: b = void 0 } = e, { explicit_call: c = !1 } = e, { container: h = !0 } = e, { visible: v = !0 } = e, { allow_overflow: L = !0 } = e, { scale: y = null } = e, { min_width: u = 0 } = e, g = p === "fieldset" ? "fieldset" : "div";
  const N = (k) => {
    if (k !== void 0) {
      if (typeof k == "number")
        return k + "px";
      if (typeof k == "string")
        return k;
    }
  };
  return t.$$set = (k) => {
    "height" in k && l(0, s = k.height), "width" in k && l(1, i = k.width), "elem_id" in k && l(2, a = k.elem_id), "elem_classes" in k && l(3, f = k.elem_classes), "variant" in k && l(4, r = k.variant), "border_mode" in k && l(5, _ = k.border_mode), "padding" in k && l(6, d = k.padding), "type" in k && l(16, p = k.type), "test_id" in k && l(7, b = k.test_id), "explicit_call" in k && l(8, c = k.explicit_call), "container" in k && l(9, h = k.container), "visible" in k && l(10, v = k.visible), "allow_overflow" in k && l(11, L = k.allow_overflow), "scale" in k && l(12, y = k.scale), "min_width" in k && l(13, u = k.min_width), "$$scope" in k && l(17, o = k.$$scope);
  }, [
    s,
    i,
    a,
    f,
    r,
    _,
    d,
    b,
    c,
    h,
    v,
    L,
    y,
    u,
    g,
    N,
    p,
    o,
    n
  ];
}
class Wt extends ei {
  constructor(e) {
    super(), ai(this, e, mi, di, _i, {
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
const {
  SvelteComponent: bi,
  append: ml,
  attr: We,
  create_component: hi,
  destroy_component: gi,
  detach: pi,
  element: _t,
  init: ki,
  insert: wi,
  mount_component: vi,
  safe_not_equal: yi,
  set_data: Ci,
  space: Si,
  text: qi,
  toggle_class: ge,
  transition_in: Li,
  transition_out: Ei
} = window.__gradio__svelte__internal;
function Ni(t) {
  let e, l, n, o, s, i;
  return n = new /*Icon*/
  t[1]({}), {
    c() {
      e = _t("label"), l = _t("span"), hi(n.$$.fragment), o = Si(), s = qi(
        /*label*/
        t[0]
      ), We(l, "class", "svelte-9gxdi0"), We(e, "for", ""), We(e, "data-testid", "block-label"), We(e, "class", "svelte-9gxdi0"), ge(e, "hide", !/*show_label*/
      t[2]), ge(e, "sr-only", !/*show_label*/
      t[2]), ge(
        e,
        "float",
        /*float*/
        t[4]
      ), ge(
        e,
        "hide-label",
        /*disable*/
        t[3]
      );
    },
    m(a, f) {
      wi(a, e, f), ml(e, l), vi(n, l, null), ml(e, o), ml(e, s), i = !0;
    },
    p(a, [f]) {
      (!i || f & /*label*/
      1) && Ci(
        s,
        /*label*/
        a[0]
      ), (!i || f & /*show_label*/
      4) && ge(e, "hide", !/*show_label*/
      a[2]), (!i || f & /*show_label*/
      4) && ge(e, "sr-only", !/*show_label*/
      a[2]), (!i || f & /*float*/
      16) && ge(
        e,
        "float",
        /*float*/
        a[4]
      ), (!i || f & /*disable*/
      8) && ge(
        e,
        "hide-label",
        /*disable*/
        a[3]
      );
    },
    i(a) {
      i || (Li(n.$$.fragment, a), i = !0);
    },
    o(a) {
      Ei(n.$$.fragment, a), i = !1;
    },
    d(a) {
      a && pi(e), gi(n);
    }
  };
}
function ji(t, e, l) {
  let { label: n = null } = e, { Icon: o } = e, { show_label: s = !0 } = e, { disable: i = !1 } = e, { float: a = !0 } = e;
  return t.$$set = (f) => {
    "label" in f && l(0, n = f.label), "Icon" in f && l(1, o = f.Icon), "show_label" in f && l(2, s = f.show_label), "disable" in f && l(3, i = f.disable), "float" in f && l(4, a = f.float);
  }, [n, o, s, i, a];
}
class $t extends bi {
  constructor(e) {
    super(), ki(this, e, ji, Ni, yi, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: Vi,
  append: Mi,
  attr: bl,
  binding_callbacks: Fi,
  create_slot: Ti,
  detach: Ii,
  element: ct,
  get_all_dirty_from_scope: zi,
  get_slot_changes: Ai,
  init: Bi,
  insert: Hi,
  safe_not_equal: Oi,
  toggle_class: pe,
  transition_in: Zi,
  transition_out: Pi,
  update_slot_base: Ri
} = window.__gradio__svelte__internal;
function Di(t) {
  let e, l, n;
  const o = (
    /*#slots*/
    t[5].default
  ), s = Ti(
    o,
    t,
    /*$$scope*/
    t[4],
    null
  );
  return {
    c() {
      e = ct("div"), l = ct("div"), s && s.c(), bl(l, "class", "icon svelte-3w3rth"), bl(e, "class", "empty svelte-3w3rth"), bl(e, "aria-label", "Empty value"), pe(
        e,
        "small",
        /*size*/
        t[0] === "small"
      ), pe(
        e,
        "large",
        /*size*/
        t[0] === "large"
      ), pe(
        e,
        "unpadded_box",
        /*unpadded_box*/
        t[1]
      ), pe(
        e,
        "small_parent",
        /*parent_height*/
        t[3]
      );
    },
    m(i, a) {
      Hi(i, e, a), Mi(e, l), s && s.m(l, null), t[6](e), n = !0;
    },
    p(i, [a]) {
      s && s.p && (!n || a & /*$$scope*/
      16) && Ri(
        s,
        o,
        i,
        /*$$scope*/
        i[4],
        n ? Ai(
          o,
          /*$$scope*/
          i[4],
          a,
          null
        ) : zi(
          /*$$scope*/
          i[4]
        ),
        null
      ), (!n || a & /*size*/
      1) && pe(
        e,
        "small",
        /*size*/
        i[0] === "small"
      ), (!n || a & /*size*/
      1) && pe(
        e,
        "large",
        /*size*/
        i[0] === "large"
      ), (!n || a & /*unpadded_box*/
      2) && pe(
        e,
        "unpadded_box",
        /*unpadded_box*/
        i[1]
      ), (!n || a & /*parent_height*/
      8) && pe(
        e,
        "small_parent",
        /*parent_height*/
        i[3]
      );
    },
    i(i) {
      n || (Zi(s, i), n = !0);
    },
    o(i) {
      Pi(s, i), n = !1;
    },
    d(i) {
      i && Ii(e), s && s.d(i), t[6](null);
    }
  };
}
function Yi(t) {
  let e, l = t[0], n = 1;
  for (; n < t.length; ) {
    const o = t[n], s = t[n + 1];
    if (n += 2, (o === "optionalAccess" || o === "optionalCall") && l == null)
      return;
    o === "access" || o === "optionalAccess" ? (e = l, l = s(l)) : (o === "call" || o === "optionalCall") && (l = s((...i) => l.call(e, ...i)), e = void 0);
  }
  return l;
}
function Ui(t, e, l) {
  let n, { $$slots: o = {}, $$scope: s } = e, { size: i = "small" } = e, { unpadded_box: a = !1 } = e, f;
  function r(d) {
    if (!d)
      return !1;
    const { height: p } = d.getBoundingClientRect(), { height: b } = Yi([
      d,
      "access",
      (c) => c.parentElement,
      "optionalAccess",
      (c) => c.getBoundingClientRect,
      "call",
      (c) => c()
    ]) || { height: p };
    return p > b + 2;
  }
  function _(d) {
    Fi[d ? "unshift" : "push"](() => {
      f = d, l(2, f);
    });
  }
  return t.$$set = (d) => {
    "size" in d && l(0, i = d.size), "unpadded_box" in d && l(1, a = d.unpadded_box), "$$scope" in d && l(4, s = d.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*el*/
    4 && l(3, n = r(f));
  }, [i, a, f, n, s, o, _];
}
class xt extends Vi {
  constructor(e) {
    super(), Bi(this, e, Ui, Di, Oi, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: Xi,
  append: ut,
  attr: U,
  detach: Gi,
  init: Ki,
  insert: Ji,
  noop: hl,
  safe_not_equal: Qi,
  svg_element: gl
} = window.__gradio__svelte__internal;
function Wi(t) {
  let e, l, n;
  return {
    c() {
      e = gl("svg"), l = gl("path"), n = gl("path"), U(l, "fill", "currentColor"), U(l, "d", "M12 15H5a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h5V5a1 1 0 0 0-1-1H3V2h6a3 3 0 0 1 3 3zM5 9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h5V9zm15 14v2a1 1 0 0 0 1 1h5v-4h-5a1 1 0 0 0-1 1z"), U(n, "fill", "currentColor"), U(n, "d", "M2 30h28V2Zm26-2h-7a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h5v-2a1 1 0 0 0-1-1h-6v-2h6a3 3 0 0 1 3 3Z"), U(e, "xmlns", "http://www.w3.org/2000/svg"), U(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), U(e, "aria-hidden", "true"), U(e, "role", "img"), U(e, "class", "iconify iconify--carbon"), U(e, "width", "100%"), U(e, "height", "100%"), U(e, "preserveAspectRatio", "xMidYMid meet"), U(e, "viewBox", "0 0 32 32");
    },
    m(o, s) {
      Ji(o, e, s), ut(e, l), ut(e, n);
    },
    p: hl,
    i: hl,
    o: hl,
    d(o) {
      o && Gi(e);
    }
  };
}
class _l extends Xi {
  constructor(e) {
    super(), Ki(this, e, null, Wi, Qi, {});
  }
}
function Fe(t) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], l = 0;
  for (; t > 1e3 && l < e.length - 1; )
    t /= 1e3, l++;
  let n = e[l];
  return (Number.isInteger(t) ? t : t.toFixed(1)) + n;
}
function el() {
}
function $i(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
const en = typeof window < "u";
let dt = en ? () => window.performance.now() : () => Date.now(), ln = en ? (t) => requestAnimationFrame(t) : el;
const Te = /* @__PURE__ */ new Set();
function tn(t) {
  Te.forEach((e) => {
    e.c(t) || (Te.delete(e), e.f());
  }), Te.size !== 0 && ln(tn);
}
function xi(t) {
  let e;
  return Te.size === 0 && ln(tn), {
    promise: new Promise((l) => {
      Te.add(e = { c: t, f: l });
    }),
    abort() {
      Te.delete(e);
    }
  };
}
const Ve = [];
function eo(t, e = el) {
  let l;
  const n = /* @__PURE__ */ new Set();
  function o(a) {
    if ($i(t, a) && (t = a, l)) {
      const f = !Ve.length;
      for (const r of n)
        r[1](), Ve.push(r, t);
      if (f) {
        for (let r = 0; r < Ve.length; r += 2)
          Ve[r][0](Ve[r + 1]);
        Ve.length = 0;
      }
    }
  }
  function s(a) {
    o(a(t));
  }
  function i(a, f = el) {
    const r = [a, f];
    return n.add(r), n.size === 1 && (l = e(o, s) || el), a(t), () => {
      n.delete(r), n.size === 0 && l && (l(), l = null);
    };
  }
  return { set: o, update: s, subscribe: i };
}
function mt(t) {
  return Object.prototype.toString.call(t) === "[object Date]";
}
function kl(t, e, l, n) {
  if (typeof l == "number" || mt(l)) {
    const o = n - l, s = (l - e) / (t.dt || 1 / 60), i = t.opts.stiffness * o, a = t.opts.damping * s, f = (i - a) * t.inv_mass, r = (s + f) * t.dt;
    return Math.abs(r) < t.opts.precision && Math.abs(o) < t.opts.precision ? n : (t.settled = !1, mt(l) ? new Date(l.getTime() + r) : l + r);
  } else {
    if (Array.isArray(l))
      return l.map(
        (o, s) => kl(t, e[s], l[s], n[s])
      );
    if (typeof l == "object") {
      const o = {};
      for (const s in l)
        o[s] = kl(t, e[s], l[s], n[s]);
      return o;
    } else
      throw new Error(`Cannot spring ${typeof l} values`);
  }
}
function bt(t, e = {}) {
  const l = eo(t), { stiffness: n = 0.15, damping: o = 0.8, precision: s = 0.01 } = e;
  let i, a, f, r = t, _ = t, d = 1, p = 0, b = !1;
  function c(v, L = {}) {
    _ = v;
    const y = f = {};
    return t == null || L.hard || h.stiffness >= 1 && h.damping >= 1 ? (b = !0, i = dt(), r = v, l.set(t = _), Promise.resolve()) : (L.soft && (p = 1 / ((L.soft === !0 ? 0.5 : +L.soft) * 60), d = 0), a || (i = dt(), b = !1, a = xi((u) => {
      if (b)
        return b = !1, a = null, !1;
      d = Math.min(d + p, 1);
      const g = {
        inv_mass: d,
        opts: h,
        settled: !0,
        dt: (u - i) * 60 / 1e3
      }, N = kl(g, r, t, _);
      return i = u, r = t, l.set(t = N), g.settled && (a = null), !g.settled;
    })), new Promise((u) => {
      a.promise.then(() => {
        y === f && u();
      });
    }));
  }
  const h = {
    set: c,
    update: (v, L) => c(v(_, t), L),
    subscribe: l.subscribe,
    stiffness: n,
    damping: o,
    precision: s
  };
  return h;
}
const {
  SvelteComponent: lo,
  append: le,
  attr: j,
  component_subscribe: ht,
  detach: to,
  element: no,
  init: io,
  insert: oo,
  noop: gt,
  safe_not_equal: so,
  set_style: $e,
  svg_element: te,
  toggle_class: pt
} = window.__gradio__svelte__internal, { onMount: fo } = window.__gradio__svelte__internal;
function ao(t) {
  let e, l, n, o, s, i, a, f, r, _, d, p;
  return {
    c() {
      e = no("div"), l = te("svg"), n = te("g"), o = te("path"), s = te("path"), i = te("path"), a = te("path"), f = te("g"), r = te("path"), _ = te("path"), d = te("path"), p = te("path"), j(o, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), j(o, "fill", "#FF7C00"), j(o, "fill-opacity", "0.4"), j(o, "class", "svelte-43sxxs"), j(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), j(s, "fill", "#FF7C00"), j(s, "class", "svelte-43sxxs"), j(i, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), j(i, "fill", "#FF7C00"), j(i, "fill-opacity", "0.4"), j(i, "class", "svelte-43sxxs"), j(a, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), j(a, "fill", "#FF7C00"), j(a, "class", "svelte-43sxxs"), $e(n, "transform", "translate(" + /*$top*/
      t[1][0] + "px, " + /*$top*/
      t[1][1] + "px)"), j(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), j(r, "fill", "#FF7C00"), j(r, "fill-opacity", "0.4"), j(r, "class", "svelte-43sxxs"), j(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), j(_, "fill", "#FF7C00"), j(_, "class", "svelte-43sxxs"), j(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), j(d, "fill", "#FF7C00"), j(d, "fill-opacity", "0.4"), j(d, "class", "svelte-43sxxs"), j(p, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), j(p, "fill", "#FF7C00"), j(p, "class", "svelte-43sxxs"), $e(f, "transform", "translate(" + /*$bottom*/
      t[2][0] + "px, " + /*$bottom*/
      t[2][1] + "px)"), j(l, "viewBox", "-1200 -1200 3000 3000"), j(l, "fill", "none"), j(l, "xmlns", "http://www.w3.org/2000/svg"), j(l, "class", "svelte-43sxxs"), j(e, "class", "svelte-43sxxs"), pt(
        e,
        "margin",
        /*margin*/
        t[0]
      );
    },
    m(b, c) {
      oo(b, e, c), le(e, l), le(l, n), le(n, o), le(n, s), le(n, i), le(n, a), le(l, f), le(f, r), le(f, _), le(f, d), le(f, p);
    },
    p(b, [c]) {
      c & /*$top*/
      2 && $e(n, "transform", "translate(" + /*$top*/
      b[1][0] + "px, " + /*$top*/
      b[1][1] + "px)"), c & /*$bottom*/
      4 && $e(f, "transform", "translate(" + /*$bottom*/
      b[2][0] + "px, " + /*$bottom*/
      b[2][1] + "px)"), c & /*margin*/
      1 && pt(
        e,
        "margin",
        /*margin*/
        b[0]
      );
    },
    i: gt,
    o: gt,
    d(b) {
      b && to(e);
    }
  };
}
function ro(t, e, l) {
  let n, o, { margin: s = !0 } = e;
  const i = bt([0, 0]);
  ht(t, i, (p) => l(1, n = p));
  const a = bt([0, 0]);
  ht(t, a, (p) => l(2, o = p));
  let f;
  async function r() {
    await Promise.all([i.set([125, 140]), a.set([-125, -140])]), await Promise.all([i.set([-125, 140]), a.set([125, -140])]), await Promise.all([i.set([-125, 0]), a.set([125, -0])]), await Promise.all([i.set([125, 0]), a.set([-125, 0])]);
  }
  async function _() {
    await r(), f || _();
  }
  async function d() {
    await Promise.all([i.set([125, 0]), a.set([-125, 0])]), _();
  }
  return fo(() => (d(), () => f = !0)), t.$$set = (p) => {
    "margin" in p && l(0, s = p.margin);
  }, [s, n, o, i, a];
}
class _o extends lo {
  constructor(e) {
    super(), io(this, e, ro, ao, so, { margin: 0 });
  }
}
const {
  SvelteComponent: co,
  append: Se,
  attr: se,
  binding_callbacks: kt,
  check_outros: nn,
  create_component: uo,
  create_slot: mo,
  destroy_component: bo,
  destroy_each: on,
  detach: S,
  element: ce,
  empty: He,
  ensure_array_like: ol,
  get_all_dirty_from_scope: ho,
  get_slot_changes: go,
  group_outros: sn,
  init: po,
  insert: q,
  mount_component: ko,
  noop: wl,
  safe_not_equal: wo,
  set_data: W,
  set_style: ke,
  space: fe,
  text: F,
  toggle_class: J,
  transition_in: Ie,
  transition_out: ze,
  update_slot_base: vo
} = window.__gradio__svelte__internal, { tick: yo } = window.__gradio__svelte__internal, { onDestroy: Co } = window.__gradio__svelte__internal, So = (t) => ({}), wt = (t) => ({});
function vt(t, e, l) {
  const n = t.slice();
  return n[38] = e[l], n[40] = l, n;
}
function yt(t, e, l) {
  const n = t.slice();
  return n[38] = e[l], n;
}
function qo(t) {
  let e, l = (
    /*i18n*/
    t[1]("common.error") + ""
  ), n, o, s;
  const i = (
    /*#slots*/
    t[29].error
  ), a = mo(
    i,
    t,
    /*$$scope*/
    t[28],
    wt
  );
  return {
    c() {
      e = ce("span"), n = F(l), o = fe(), a && a.c(), se(e, "class", "error svelte-1yserjw");
    },
    m(f, r) {
      q(f, e, r), Se(e, n), q(f, o, r), a && a.m(f, r), s = !0;
    },
    p(f, r) {
      (!s || r[0] & /*i18n*/
      2) && l !== (l = /*i18n*/
      f[1]("common.error") + "") && W(n, l), a && a.p && (!s || r[0] & /*$$scope*/
      268435456) && vo(
        a,
        i,
        f,
        /*$$scope*/
        f[28],
        s ? go(
          i,
          /*$$scope*/
          f[28],
          r,
          So
        ) : ho(
          /*$$scope*/
          f[28]
        ),
        wt
      );
    },
    i(f) {
      s || (Ie(a, f), s = !0);
    },
    o(f) {
      ze(a, f), s = !1;
    },
    d(f) {
      f && (S(e), S(o)), a && a.d(f);
    }
  };
}
function Lo(t) {
  let e, l, n, o, s, i, a, f, r, _ = (
    /*variant*/
    t[8] === "default" && /*show_eta_bar*/
    t[18] && /*show_progress*/
    t[6] === "full" && Ct(t)
  );
  function d(u, g) {
    if (
      /*progress*/
      u[7]
    )
      return jo;
    if (
      /*queue_position*/
      u[2] !== null && /*queue_size*/
      u[3] !== void 0 && /*queue_position*/
      u[2] >= 0
    )
      return No;
    if (
      /*queue_position*/
      u[2] === 0
    )
      return Eo;
  }
  let p = d(t), b = p && p(t), c = (
    /*timer*/
    t[5] && Lt(t)
  );
  const h = [To, Fo], v = [];
  function L(u, g) {
    return (
      /*last_progress_level*/
      u[15] != null ? 0 : (
        /*show_progress*/
        u[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = L(t)) && (i = v[s] = h[s](t));
  let y = !/*timer*/
  t[5] && Tt(t);
  return {
    c() {
      _ && _.c(), e = fe(), l = ce("div"), b && b.c(), n = fe(), c && c.c(), o = fe(), i && i.c(), a = fe(), y && y.c(), f = He(), se(l, "class", "progress-text svelte-1yserjw"), J(
        l,
        "meta-text-center",
        /*variant*/
        t[8] === "center"
      ), J(
        l,
        "meta-text",
        /*variant*/
        t[8] === "default"
      );
    },
    m(u, g) {
      _ && _.m(u, g), q(u, e, g), q(u, l, g), b && b.m(l, null), Se(l, n), c && c.m(l, null), q(u, o, g), ~s && v[s].m(u, g), q(u, a, g), y && y.m(u, g), q(u, f, g), r = !0;
    },
    p(u, g) {
      /*variant*/
      u[8] === "default" && /*show_eta_bar*/
      u[18] && /*show_progress*/
      u[6] === "full" ? _ ? _.p(u, g) : (_ = Ct(u), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), p === (p = d(u)) && b ? b.p(u, g) : (b && b.d(1), b = p && p(u), b && (b.c(), b.m(l, n))), /*timer*/
      u[5] ? c ? c.p(u, g) : (c = Lt(u), c.c(), c.m(l, null)) : c && (c.d(1), c = null), (!r || g[0] & /*variant*/
      256) && J(
        l,
        "meta-text-center",
        /*variant*/
        u[8] === "center"
      ), (!r || g[0] & /*variant*/
      256) && J(
        l,
        "meta-text",
        /*variant*/
        u[8] === "default"
      );
      let N = s;
      s = L(u), s === N ? ~s && v[s].p(u, g) : (i && (sn(), ze(v[N], 1, 1, () => {
        v[N] = null;
      }), nn()), ~s ? (i = v[s], i ? i.p(u, g) : (i = v[s] = h[s](u), i.c()), Ie(i, 1), i.m(a.parentNode, a)) : i = null), /*timer*/
      u[5] ? y && (y.d(1), y = null) : y ? y.p(u, g) : (y = Tt(u), y.c(), y.m(f.parentNode, f));
    },
    i(u) {
      r || (Ie(i), r = !0);
    },
    o(u) {
      ze(i), r = !1;
    },
    d(u) {
      u && (S(e), S(l), S(o), S(a), S(f)), _ && _.d(u), b && b.d(), c && c.d(), ~s && v[s].d(u), y && y.d(u);
    }
  };
}
function Ct(t) {
  let e, l = `translateX(${/*eta_level*/
  (t[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ce("div"), se(e, "class", "eta-bar svelte-1yserjw"), ke(e, "transform", l);
    },
    m(n, o) {
      q(n, e, o);
    },
    p(n, o) {
      o[0] & /*eta_level*/
      131072 && l !== (l = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && ke(e, "transform", l);
    },
    d(n) {
      n && S(e);
    }
  };
}
function Eo(t) {
  let e;
  return {
    c() {
      e = F("processing |");
    },
    m(l, n) {
      q(l, e, n);
    },
    p: wl,
    d(l) {
      l && S(e);
    }
  };
}
function No(t) {
  let e, l = (
    /*queue_position*/
    t[2] + 1 + ""
  ), n, o, s, i;
  return {
    c() {
      e = F("queue: "), n = F(l), o = F("/"), s = F(
        /*queue_size*/
        t[3]
      ), i = F(" |");
    },
    m(a, f) {
      q(a, e, f), q(a, n, f), q(a, o, f), q(a, s, f), q(a, i, f);
    },
    p(a, f) {
      f[0] & /*queue_position*/
      4 && l !== (l = /*queue_position*/
      a[2] + 1 + "") && W(n, l), f[0] & /*queue_size*/
      8 && W(
        s,
        /*queue_size*/
        a[3]
      );
    },
    d(a) {
      a && (S(e), S(n), S(o), S(s), S(i));
    }
  };
}
function jo(t) {
  let e, l = ol(
    /*progress*/
    t[7]
  ), n = [];
  for (let o = 0; o < l.length; o += 1)
    n[o] = qt(yt(t, l, o));
  return {
    c() {
      for (let o = 0; o < n.length; o += 1)
        n[o].c();
      e = He();
    },
    m(o, s) {
      for (let i = 0; i < n.length; i += 1)
        n[i] && n[i].m(o, s);
      q(o, e, s);
    },
    p(o, s) {
      if (s[0] & /*progress*/
      128) {
        l = ol(
          /*progress*/
          o[7]
        );
        let i;
        for (i = 0; i < l.length; i += 1) {
          const a = yt(o, l, i);
          n[i] ? n[i].p(a, s) : (n[i] = qt(a), n[i].c(), n[i].m(e.parentNode, e));
        }
        for (; i < n.length; i += 1)
          n[i].d(1);
        n.length = l.length;
      }
    },
    d(o) {
      o && S(e), on(n, o);
    }
  };
}
function St(t) {
  let e, l = (
    /*p*/
    t[38].unit + ""
  ), n, o, s = " ", i;
  function a(_, d) {
    return (
      /*p*/
      _[38].length != null ? Mo : Vo
    );
  }
  let f = a(t), r = f(t);
  return {
    c() {
      r.c(), e = fe(), n = F(l), o = F(" | "), i = F(s);
    },
    m(_, d) {
      r.m(_, d), q(_, e, d), q(_, n, d), q(_, o, d), q(_, i, d);
    },
    p(_, d) {
      f === (f = a(_)) && r ? r.p(_, d) : (r.d(1), r = f(_), r && (r.c(), r.m(e.parentNode, e))), d[0] & /*progress*/
      128 && l !== (l = /*p*/
      _[38].unit + "") && W(n, l);
    },
    d(_) {
      _ && (S(e), S(n), S(o), S(i)), r.d(_);
    }
  };
}
function Vo(t) {
  let e = Fe(
    /*p*/
    t[38].index || 0
  ) + "", l;
  return {
    c() {
      l = F(e);
    },
    m(n, o) {
      q(n, l, o);
    },
    p(n, o) {
      o[0] & /*progress*/
      128 && e !== (e = Fe(
        /*p*/
        n[38].index || 0
      ) + "") && W(l, e);
    },
    d(n) {
      n && S(l);
    }
  };
}
function Mo(t) {
  let e = Fe(
    /*p*/
    t[38].index || 0
  ) + "", l, n, o = Fe(
    /*p*/
    t[38].length
  ) + "", s;
  return {
    c() {
      l = F(e), n = F("/"), s = F(o);
    },
    m(i, a) {
      q(i, l, a), q(i, n, a), q(i, s, a);
    },
    p(i, a) {
      a[0] & /*progress*/
      128 && e !== (e = Fe(
        /*p*/
        i[38].index || 0
      ) + "") && W(l, e), a[0] & /*progress*/
      128 && o !== (o = Fe(
        /*p*/
        i[38].length
      ) + "") && W(s, o);
    },
    d(i) {
      i && (S(l), S(n), S(s));
    }
  };
}
function qt(t) {
  let e, l = (
    /*p*/
    t[38].index != null && St(t)
  );
  return {
    c() {
      l && l.c(), e = He();
    },
    m(n, o) {
      l && l.m(n, o), q(n, e, o);
    },
    p(n, o) {
      /*p*/
      n[38].index != null ? l ? l.p(n, o) : (l = St(n), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(n) {
      n && S(e), l && l.d(n);
    }
  };
}
function Lt(t) {
  let e, l = (
    /*eta*/
    t[0] ? `/${/*formatted_eta*/
    t[19]}` : ""
  ), n, o;
  return {
    c() {
      e = F(
        /*formatted_timer*/
        t[20]
      ), n = F(l), o = F("s");
    },
    m(s, i) {
      q(s, e, i), q(s, n, i), q(s, o, i);
    },
    p(s, i) {
      i[0] & /*formatted_timer*/
      1048576 && W(
        e,
        /*formatted_timer*/
        s[20]
      ), i[0] & /*eta, formatted_eta*/
      524289 && l !== (l = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && W(n, l);
    },
    d(s) {
      s && (S(e), S(n), S(o));
    }
  };
}
function Fo(t) {
  let e, l;
  return e = new _o({
    props: { margin: (
      /*variant*/
      t[8] === "default"
    ) }
  }), {
    c() {
      uo(e.$$.fragment);
    },
    m(n, o) {
      ko(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o[0] & /*variant*/
      256 && (s.margin = /*variant*/
      n[8] === "default"), e.$set(s);
    },
    i(n) {
      l || (Ie(e.$$.fragment, n), l = !0);
    },
    o(n) {
      ze(e.$$.fragment, n), l = !1;
    },
    d(n) {
      bo(e, n);
    }
  };
}
function To(t) {
  let e, l, n, o, s, i = `${/*last_progress_level*/
  t[15] * 100}%`, a = (
    /*progress*/
    t[7] != null && Et(t)
  );
  return {
    c() {
      e = ce("div"), l = ce("div"), a && a.c(), n = fe(), o = ce("div"), s = ce("div"), se(l, "class", "progress-level-inner svelte-1yserjw"), se(s, "class", "progress-bar svelte-1yserjw"), ke(s, "width", i), se(o, "class", "progress-bar-wrap svelte-1yserjw"), se(e, "class", "progress-level svelte-1yserjw");
    },
    m(f, r) {
      q(f, e, r), Se(e, l), a && a.m(l, null), Se(e, n), Se(e, o), Se(o, s), t[30](s);
    },
    p(f, r) {
      /*progress*/
      f[7] != null ? a ? a.p(f, r) : (a = Et(f), a.c(), a.m(l, null)) : a && (a.d(1), a = null), r[0] & /*last_progress_level*/
      32768 && i !== (i = `${/*last_progress_level*/
      f[15] * 100}%`) && ke(s, "width", i);
    },
    i: wl,
    o: wl,
    d(f) {
      f && S(e), a && a.d(), t[30](null);
    }
  };
}
function Et(t) {
  let e, l = ol(
    /*progress*/
    t[7]
  ), n = [];
  for (let o = 0; o < l.length; o += 1)
    n[o] = Ft(vt(t, l, o));
  return {
    c() {
      for (let o = 0; o < n.length; o += 1)
        n[o].c();
      e = He();
    },
    m(o, s) {
      for (let i = 0; i < n.length; i += 1)
        n[i] && n[i].m(o, s);
      q(o, e, s);
    },
    p(o, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        l = ol(
          /*progress*/
          o[7]
        );
        let i;
        for (i = 0; i < l.length; i += 1) {
          const a = vt(o, l, i);
          n[i] ? n[i].p(a, s) : (n[i] = Ft(a), n[i].c(), n[i].m(e.parentNode, e));
        }
        for (; i < n.length; i += 1)
          n[i].d(1);
        n.length = l.length;
      }
    },
    d(o) {
      o && S(e), on(n, o);
    }
  };
}
function Nt(t) {
  let e, l, n, o, s = (
    /*i*/
    t[40] !== 0 && Io()
  ), i = (
    /*p*/
    t[38].desc != null && jt(t)
  ), a = (
    /*p*/
    t[38].desc != null && /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[40]
    ] != null && Vt()
  ), f = (
    /*progress_level*/
    t[14] != null && Mt(t)
  );
  return {
    c() {
      s && s.c(), e = fe(), i && i.c(), l = fe(), a && a.c(), n = fe(), f && f.c(), o = He();
    },
    m(r, _) {
      s && s.m(r, _), q(r, e, _), i && i.m(r, _), q(r, l, _), a && a.m(r, _), q(r, n, _), f && f.m(r, _), q(r, o, _);
    },
    p(r, _) {
      /*p*/
      r[38].desc != null ? i ? i.p(r, _) : (i = jt(r), i.c(), i.m(l.parentNode, l)) : i && (i.d(1), i = null), /*p*/
      r[38].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[40]
      ] != null ? a || (a = Vt(), a.c(), a.m(n.parentNode, n)) : a && (a.d(1), a = null), /*progress_level*/
      r[14] != null ? f ? f.p(r, _) : (f = Mt(r), f.c(), f.m(o.parentNode, o)) : f && (f.d(1), f = null);
    },
    d(r) {
      r && (S(e), S(l), S(n), S(o)), s && s.d(r), i && i.d(r), a && a.d(r), f && f.d(r);
    }
  };
}
function Io(t) {
  let e;
  return {
    c() {
      e = F(" /");
    },
    m(l, n) {
      q(l, e, n);
    },
    d(l) {
      l && S(e);
    }
  };
}
function jt(t) {
  let e = (
    /*p*/
    t[38].desc + ""
  ), l;
  return {
    c() {
      l = F(e);
    },
    m(n, o) {
      q(n, l, o);
    },
    p(n, o) {
      o[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[38].desc + "") && W(l, e);
    },
    d(n) {
      n && S(l);
    }
  };
}
function Vt(t) {
  let e;
  return {
    c() {
      e = F("-");
    },
    m(l, n) {
      q(l, e, n);
    },
    d(l) {
      l && S(e);
    }
  };
}
function Mt(t) {
  let e = (100 * /*progress_level*/
  (t[14][
    /*i*/
    t[40]
  ] || 0)).toFixed(1) + "", l, n;
  return {
    c() {
      l = F(e), n = F("%");
    },
    m(o, s) {
      q(o, l, s), q(o, n, s);
    },
    p(o, s) {
      s[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (o[14][
        /*i*/
        o[40]
      ] || 0)).toFixed(1) + "") && W(l, e);
    },
    d(o) {
      o && (S(l), S(n));
    }
  };
}
function Ft(t) {
  let e, l = (
    /*p*/
    (t[38].desc != null || /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[40]
    ] != null) && Nt(t)
  );
  return {
    c() {
      l && l.c(), e = He();
    },
    m(n, o) {
      l && l.m(n, o), q(n, e, o);
    },
    p(n, o) {
      /*p*/
      n[38].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[40]
      ] != null ? l ? l.p(n, o) : (l = Nt(n), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(n) {
      n && S(e), l && l.d(n);
    }
  };
}
function Tt(t) {
  let e, l;
  return {
    c() {
      e = ce("p"), l = F(
        /*loading_text*/
        t[9]
      ), se(e, "class", "loading svelte-1yserjw");
    },
    m(n, o) {
      q(n, e, o), Se(e, l);
    },
    p(n, o) {
      o[0] & /*loading_text*/
      512 && W(
        l,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && S(e);
    }
  };
}
function zo(t) {
  let e, l, n, o, s;
  const i = [Lo, qo], a = [];
  function f(r, _) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(l = f(t)) && (n = a[l] = i[l](t)), {
    c() {
      e = ce("div"), n && n.c(), se(e, "class", o = "wrap " + /*variant*/
      t[8] + " " + /*show_progress*/
      t[6] + " svelte-1yserjw"), J(e, "hide", !/*status*/
      t[4] || /*status*/
      t[4] === "complete" || /*show_progress*/
      t[6] === "hidden"), J(
        e,
        "translucent",
        /*variant*/
        t[8] === "center" && /*status*/
        (t[4] === "pending" || /*status*/
        t[4] === "error") || /*translucent*/
        t[11] || /*show_progress*/
        t[6] === "minimal"
      ), J(
        e,
        "generating",
        /*status*/
        t[4] === "generating"
      ), J(
        e,
        "border",
        /*border*/
        t[12]
      ), ke(
        e,
        "position",
        /*absolute*/
        t[10] ? "absolute" : "static"
      ), ke(
        e,
        "padding",
        /*absolute*/
        t[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, _) {
      q(r, e, _), ~l && a[l].m(e, null), t[31](e), s = !0;
    },
    p(r, _) {
      let d = l;
      l = f(r), l === d ? ~l && a[l].p(r, _) : (n && (sn(), ze(a[d], 1, 1, () => {
        a[d] = null;
      }), nn()), ~l ? (n = a[l], n ? n.p(r, _) : (n = a[l] = i[l](r), n.c()), Ie(n, 1), n.m(e, null)) : n = null), (!s || _[0] & /*variant, show_progress*/
      320 && o !== (o = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1yserjw")) && se(e, "class", o), (!s || _[0] & /*variant, show_progress, status, show_progress*/
      336) && J(e, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!s || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && J(
        e,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!s || _[0] & /*variant, show_progress, status*/
      336) && J(
        e,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!s || _[0] & /*variant, show_progress, border*/
      4416) && J(
        e,
        "border",
        /*border*/
        r[12]
      ), _[0] & /*absolute*/
      1024 && ke(
        e,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && ke(
        e,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      s || (Ie(n), s = !0);
    },
    o(r) {
      ze(n), s = !1;
    },
    d(r) {
      r && S(e), ~l && a[l].d(), t[31](null);
    }
  };
}
let xe = [], pl = !1;
async function Ao(t, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (xe.push(t), !pl)
      pl = !0;
    else
      return;
    await yo(), requestAnimationFrame(() => {
      let l = [0, 0];
      for (let n = 0; n < xe.length; n++) {
        const s = xe[n].getBoundingClientRect();
        (n === 0 || s.top + window.scrollY <= l[0]) && (l[0] = s.top + window.scrollY, l[1] = n);
      }
      window.scrollTo({ top: l[0] - 20, behavior: "smooth" }), pl = !1, xe = [];
    });
  }
}
function Bo(t, e, l) {
  let n, { $$slots: o = {}, $$scope: s } = e, { i18n: i } = e, { eta: a = null } = e, { queue_position: f } = e, { queue_size: r } = e, { status: _ } = e, { scroll_to_output: d = !1 } = e, { timer: p = !0 } = e, { show_progress: b = "full" } = e, { message: c = null } = e, { progress: h = null } = e, { variant: v = "default" } = e, { loading_text: L = "Loading..." } = e, { absolute: y = !0 } = e, { translucent: u = !1 } = e, { border: g = !1 } = e, { autoscroll: N } = e, k, w = !1, de = 0, re = 0, me = null, be = null, Ue = 0, _e = null, ye, ne = null, Xe = !0;
  const cl = () => {
    l(0, a = l(26, me = l(19, je = null))), l(24, de = performance.now()), l(25, re = 0), w = !0, Ge();
  };
  function Ge() {
    requestAnimationFrame(() => {
      l(25, re = (performance.now() - de) / 1e3), w && Ge();
    });
  }
  function Ke() {
    l(25, re = 0), l(0, a = l(26, me = l(19, je = null))), w && (w = !1);
  }
  Co(() => {
    w && Ke();
  });
  let je = null;
  function ul(C) {
    kt[C ? "unshift" : "push"](() => {
      ne = C, l(16, ne), l(7, h), l(14, _e), l(15, ye);
    });
  }
  function dl(C) {
    kt[C ? "unshift" : "push"](() => {
      k = C, l(13, k);
    });
  }
  return t.$$set = (C) => {
    "i18n" in C && l(1, i = C.i18n), "eta" in C && l(0, a = C.eta), "queue_position" in C && l(2, f = C.queue_position), "queue_size" in C && l(3, r = C.queue_size), "status" in C && l(4, _ = C.status), "scroll_to_output" in C && l(21, d = C.scroll_to_output), "timer" in C && l(5, p = C.timer), "show_progress" in C && l(6, b = C.show_progress), "message" in C && l(22, c = C.message), "progress" in C && l(7, h = C.progress), "variant" in C && l(8, v = C.variant), "loading_text" in C && l(9, L = C.loading_text), "absolute" in C && l(10, y = C.absolute), "translucent" in C && l(11, u = C.translucent), "border" in C && l(12, g = C.border), "autoscroll" in C && l(23, N = C.autoscroll), "$$scope" in C && l(28, s = C.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (a === null && l(0, a = me), a != null && me !== a && (l(27, be = (performance.now() - de) / 1e3 + a), l(19, je = be.toFixed(1)), l(26, me = a))), t.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && l(17, Ue = be === null || be <= 0 || !re ? null : Math.min(re / be, 1)), t.$$.dirty[0] & /*progress*/
    128 && h != null && l(18, Xe = !1), t.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (h != null ? l(14, _e = h.map((C) => {
      if (C.index != null && C.length != null)
        return C.index / C.length;
      if (C.progress != null)
        return C.progress;
    })) : l(14, _e = null), _e ? (l(15, ye = _e[_e.length - 1]), ne && (ye === 0 ? l(16, ne.style.transition = "0", ne) : l(16, ne.style.transition = "150ms", ne))) : l(15, ye = void 0)), t.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? cl() : Ke()), t.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && k && d && (_ === "pending" || _ === "complete") && Ao(k, N), t.$$.dirty[0] & /*status, message*/
    4194320, t.$$.dirty[0] & /*timer_diff*/
    33554432 && l(20, n = re.toFixed(1));
  }, [
    a,
    i,
    f,
    r,
    _,
    p,
    b,
    h,
    v,
    L,
    y,
    u,
    g,
    k,
    _e,
    ye,
    ne,
    Ue,
    Xe,
    je,
    n,
    d,
    c,
    N,
    de,
    re,
    me,
    be,
    s,
    o,
    ul,
    dl
  ];
}
class fn extends co {
  constructor(e) {
    super(), po(
      this,
      e,
      Bo,
      zo,
      wo,
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
  SvelteComponent: Ho,
  add_flush_callback: Oo,
  assign: an,
  bind: Zo,
  binding_callbacks: Po,
  check_outros: Re,
  create_component: $,
  destroy_component: x,
  detach: qe,
  empty: ql,
  get_spread_object: rn,
  get_spread_update: _n,
  group_outros: De,
  init: Ro,
  insert: Le,
  mount_component: ee,
  safe_not_equal: Do,
  space: sl,
  transition_in: M,
  transition_out: I
} = window.__gradio__svelte__internal;
function Yo(t) {
  let e, l;
  return e = new Wt({
    props: {
      variant: (
        /*interactive*/
        t[12] ? "dashed" : "solid"
      ),
      test_id: "highlighted-text",
      visible: (
        /*visible*/
        t[5]
      ),
      elem_id: (
        /*elem_id*/
        t[3]
      ),
      elem_classes: (
        /*elem_classes*/
        t[4]
      ),
      padding: !1,
      container: (
        /*container*/
        t[8]
      ),
      scale: (
        /*scale*/
        t[9]
      ),
      min_width: (
        /*min_width*/
        t[10]
      ),
      $$slots: { default: [Jo] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o & /*interactive*/
      4096 && (s.variant = /*interactive*/
      n[12] ? "dashed" : "solid"), o & /*visible*/
      32 && (s.visible = /*visible*/
      n[5]), o & /*elem_id*/
      8 && (s.elem_id = /*elem_id*/
      n[3]), o & /*elem_classes*/
      16 && (s.elem_classes = /*elem_classes*/
      n[4]), o & /*container*/
      256 && (s.container = /*container*/
      n[8]), o & /*scale*/
      512 && (s.scale = /*scale*/
      n[9]), o & /*min_width*/
      1024 && (s.min_width = /*min_width*/
      n[10]), o & /*$$scope, _selectable, show_legend, color_map, default_label, value, gradio, label, container, loading_status*/
      1075655 && (s.$$scope = { dirty: o, ctx: n }), e.$set(s);
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function Uo(t) {
  let e, l;
  return e = new Wt({
    props: {
      variant: "solid",
      test_id: "highlighted-text",
      visible: (
        /*visible*/
        t[5]
      ),
      elem_id: (
        /*elem_id*/
        t[3]
      ),
      elem_classes: (
        /*elem_classes*/
        t[4]
      ),
      padding: !1,
      container: (
        /*container*/
        t[8]
      ),
      scale: (
        /*scale*/
        t[9]
      ),
      min_width: (
        /*min_width*/
        t[10]
      ),
      $$slots: { default: [xo] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o & /*visible*/
      32 && (s.visible = /*visible*/
      n[5]), o & /*elem_id*/
      8 && (s.elem_id = /*elem_id*/
      n[3]), o & /*elem_classes*/
      16 && (s.elem_classes = /*elem_classes*/
      n[4]), o & /*container*/
      256 && (s.container = /*container*/
      n[8]), o & /*scale*/
      512 && (s.scale = /*scale*/
      n[9]), o & /*min_width*/
      1024 && (s.min_width = /*min_width*/
      n[10]), o & /*$$scope, _selectable, value, show_legend, color_map, gradio, label, container, loading_status*/
      1067463 && (s.$$scope = { dirty: o, ctx: n }), e.$set(s);
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function It(t) {
  let e, l;
  return e = new $t({
    props: {
      Icon: _l,
      label: (
        /*label*/
        t[7]
      ),
      float: !1,
      disable: (
        /*container*/
        t[8] === !1
      )
    }
  }), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o & /*label*/
      128 && (s.label = /*label*/
      n[7]), o & /*container*/
      256 && (s.disable = /*container*/
      n[8] === !1), e.$set(s);
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function Xo(t) {
  let e, l;
  return e = new xt({
    props: {
      $$slots: { default: [Ko] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o & /*$$scope*/
      1048576 && (s.$$scope = { dirty: o, ctx: n }), e.$set(s);
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function Go(t) {
  let e, l, n;
  function o(i) {
    t[18](i);
  }
  let s = {
    selectable: (
      /*_selectable*/
      t[11]
    ),
    show_legend: (
      /*show_legend*/
      t[6]
    ),
    color_map: (
      /*color_map*/
      t[1]
    ),
    default_label: (
      /*default_label*/
      t[13]
    )
  };
  return (
    /*value*/
    t[0] !== void 0 && (s.value = /*value*/
    t[0]), e = new xn({ props: s }), Po.push(() => Zo(e, "value", o)), e.$on(
      "change",
      /*change_handler*/
      t[19]
    ), {
      c() {
        $(e.$$.fragment);
      },
      m(i, a) {
        ee(e, i, a), n = !0;
      },
      p(i, a) {
        const f = {};
        a & /*_selectable*/
        2048 && (f.selectable = /*_selectable*/
        i[11]), a & /*show_legend*/
        64 && (f.show_legend = /*show_legend*/
        i[6]), a & /*color_map*/
        2 && (f.color_map = /*color_map*/
        i[1]), a & /*default_label*/
        8192 && (f.default_label = /*default_label*/
        i[13]), !l && a & /*value*/
        1 && (l = !0, f.value = /*value*/
        i[0], Oo(() => l = !1)), e.$set(f);
      },
      i(i) {
        n || (M(e.$$.fragment, i), n = !0);
      },
      o(i) {
        I(e.$$.fragment, i), n = !1;
      },
      d(i) {
        x(e, i);
      }
    }
  );
}
function Ko(t) {
  let e, l;
  return e = new _l({}), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function Jo(t) {
  let e, l, n, o, s, i, a;
  const f = [
    { autoscroll: (
      /*gradio*/
      t[2].autoscroll
    ) },
    /*loading_status*/
    t[14],
    { i18n: (
      /*gradio*/
      t[2].i18n
    ) }
  ];
  let r = {};
  for (let c = 0; c < f.length; c += 1)
    r = an(r, f[c]);
  e = new fn({ props: r });
  let _ = (
    /*label*/
    t[7] && It(t)
  );
  const d = [Go, Xo], p = [];
  function b(c, h) {
    return (
      /*value*/
      c[0] ? 0 : 1
    );
  }
  return o = b(t), s = p[o] = d[o](t), {
    c() {
      $(e.$$.fragment), l = sl(), _ && _.c(), n = sl(), s.c(), i = ql();
    },
    m(c, h) {
      ee(e, c, h), Le(c, l, h), _ && _.m(c, h), Le(c, n, h), p[o].m(c, h), Le(c, i, h), a = !0;
    },
    p(c, h) {
      const v = h & /*gradio, loading_status*/
      16388 ? _n(f, [
        h & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          c[2].autoscroll
        ) },
        h & /*loading_status*/
        16384 && rn(
          /*loading_status*/
          c[14]
        ),
        h & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          c[2].i18n
        ) }
      ]) : {};
      e.$set(v), /*label*/
      c[7] ? _ ? (_.p(c, h), h & /*label*/
      128 && M(_, 1)) : (_ = It(c), _.c(), M(_, 1), _.m(n.parentNode, n)) : _ && (De(), I(_, 1, 1, () => {
        _ = null;
      }), Re());
      let L = o;
      o = b(c), o === L ? p[o].p(c, h) : (De(), I(p[L], 1, 1, () => {
        p[L] = null;
      }), Re(), s = p[o], s ? s.p(c, h) : (s = p[o] = d[o](c), s.c()), M(s, 1), s.m(i.parentNode, i));
    },
    i(c) {
      a || (M(e.$$.fragment, c), M(_), M(s), a = !0);
    },
    o(c) {
      I(e.$$.fragment, c), I(_), I(s), a = !1;
    },
    d(c) {
      c && (qe(l), qe(n), qe(i)), x(e, c), _ && _.d(c), p[o].d(c);
    }
  };
}
function zt(t) {
  let e, l;
  return e = new $t({
    props: {
      Icon: _l,
      label: (
        /*label*/
        t[7]
      ),
      float: !1,
      disable: (
        /*container*/
        t[8] === !1
      )
    }
  }), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o & /*label*/
      128 && (s.label = /*label*/
      n[7]), o & /*container*/
      256 && (s.disable = /*container*/
      n[8] === !1), e.$set(s);
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function Qo(t) {
  let e, l;
  return e = new xt({
    props: {
      $$slots: { default: [$o] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o & /*$$scope*/
      1048576 && (s.$$scope = { dirty: o, ctx: n }), e.$set(s);
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function Wo(t) {
  let e, l;
  return e = new In({
    props: {
      selectable: (
        /*_selectable*/
        t[11]
      ),
      value: (
        /*value*/
        t[0]
      ),
      show_legend: (
        /*show_legend*/
        t[6]
      ),
      color_map: (
        /*color_map*/
        t[1]
      )
    }
  }), e.$on(
    "select",
    /*select_handler*/
    t[17]
  ), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    p(n, o) {
      const s = {};
      o & /*_selectable*/
      2048 && (s.selectable = /*_selectable*/
      n[11]), o & /*value*/
      1 && (s.value = /*value*/
      n[0]), o & /*show_legend*/
      64 && (s.show_legend = /*show_legend*/
      n[6]), o & /*color_map*/
      2 && (s.color_map = /*color_map*/
      n[1]), e.$set(s);
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function $o(t) {
  let e, l;
  return e = new _l({}), {
    c() {
      $(e.$$.fragment);
    },
    m(n, o) {
      ee(e, n, o), l = !0;
    },
    i(n) {
      l || (M(e.$$.fragment, n), l = !0);
    },
    o(n) {
      I(e.$$.fragment, n), l = !1;
    },
    d(n) {
      x(e, n);
    }
  };
}
function xo(t) {
  let e, l, n, o, s, i, a;
  const f = [
    { autoscroll: (
      /*gradio*/
      t[2].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      t[2].i18n
    ) },
    /*loading_status*/
    t[14]
  ];
  let r = {};
  for (let c = 0; c < f.length; c += 1)
    r = an(r, f[c]);
  e = new fn({ props: r });
  let _ = (
    /*label*/
    t[7] && zt(t)
  );
  const d = [Wo, Qo], p = [];
  function b(c, h) {
    return (
      /*value*/
      c[0] ? 0 : 1
    );
  }
  return o = b(t), s = p[o] = d[o](t), {
    c() {
      $(e.$$.fragment), l = sl(), _ && _.c(), n = sl(), s.c(), i = ql();
    },
    m(c, h) {
      ee(e, c, h), Le(c, l, h), _ && _.m(c, h), Le(c, n, h), p[o].m(c, h), Le(c, i, h), a = !0;
    },
    p(c, h) {
      const v = h & /*gradio, loading_status*/
      16388 ? _n(f, [
        h & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          c[2].autoscroll
        ) },
        h & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          c[2].i18n
        ) },
        h & /*loading_status*/
        16384 && rn(
          /*loading_status*/
          c[14]
        )
      ]) : {};
      e.$set(v), /*label*/
      c[7] ? _ ? (_.p(c, h), h & /*label*/
      128 && M(_, 1)) : (_ = zt(c), _.c(), M(_, 1), _.m(n.parentNode, n)) : _ && (De(), I(_, 1, 1, () => {
        _ = null;
      }), Re());
      let L = o;
      o = b(c), o === L ? p[o].p(c, h) : (De(), I(p[L], 1, 1, () => {
        p[L] = null;
      }), Re(), s = p[o], s ? s.p(c, h) : (s = p[o] = d[o](c), s.c()), M(s, 1), s.m(i.parentNode, i));
    },
    i(c) {
      a || (M(e.$$.fragment, c), M(_), M(s), a = !0);
    },
    o(c) {
      I(e.$$.fragment, c), I(_), I(s), a = !1;
    },
    d(c) {
      c && (qe(l), qe(n), qe(i)), x(e, c), _ && _.d(c), p[o].d(c);
    }
  };
}
function es(t) {
  let e, l, n, o;
  const s = [Uo, Yo], i = [];
  function a(f, r) {
    return (
      /*interactive*/
      f[12] ? 1 : 0
    );
  }
  return e = a(t), l = i[e] = s[e](t), {
    c() {
      l.c(), n = ql();
    },
    m(f, r) {
      i[e].m(f, r), Le(f, n, r), o = !0;
    },
    p(f, [r]) {
      let _ = e;
      e = a(f), e === _ ? i[e].p(f, r) : (De(), I(i[_], 1, 1, () => {
        i[_] = null;
      }), Re(), l = i[e], l ? l.p(f, r) : (l = i[e] = s[e](f), l.c()), M(l, 1), l.m(n.parentNode, n));
    },
    i(f) {
      o || (M(l), o = !0);
    },
    o(f) {
      I(l), o = !1;
    },
    d(f) {
      f && qe(n), i[e].d(f);
    }
  };
}
function ls(t, e, l) {
  let { gradio: n } = e, { elem_id: o = "" } = e, { elem_classes: s = [] } = e, { visible: i = !0 } = e, { value: a } = e, f, { show_legend: r } = e, { color_map: _ = {} } = e, { label: d = n.i18n("highlighted_text.highlighted_text") } = e, { container: p = !0 } = e, { scale: b = null } = e, { min_width: c = void 0 } = e, { _selectable: h = !1 } = e, { combine_adjacent: v = !1 } = e, { interactive: L } = e, { default_label: y = "label" } = e, { loading_status: u } = e;
  const g = ({ detail: w }) => n.dispatch("select", w);
  function N(w) {
    a = w, l(0, a), l(15, v);
  }
  const k = () => n.dispatch("change");
  return t.$$set = (w) => {
    "gradio" in w && l(2, n = w.gradio), "elem_id" in w && l(3, o = w.elem_id), "elem_classes" in w && l(4, s = w.elem_classes), "visible" in w && l(5, i = w.visible), "value" in w && l(0, a = w.value), "show_legend" in w && l(6, r = w.show_legend), "color_map" in w && l(1, _ = w.color_map), "label" in w && l(7, d = w.label), "container" in w && l(8, p = w.container), "scale" in w && l(9, b = w.scale), "min_width" in w && l(10, c = w.min_width), "_selectable" in w && l(11, h = w._selectable), "combine_adjacent" in w && l(15, v = w.combine_adjacent), "interactive" in w && l(12, L = w.interactive), "default_label" in w && l(13, y = w.default_label), "loading_status" in w && l(14, u = w.loading_status);
  }, t.$$.update = () => {
    t.$$.dirty & /*color_map*/
    2 && !_ && Object.keys(_).length && l(1, _), t.$$.dirty & /*value, combine_adjacent*/
    32769 && a && v && l(0, a = Ht(a, "equal")), t.$$.dirty & /*value, old_value, gradio*/
    65541 && a !== f && (l(16, f = a), n.dispatch("change"));
  }, [
    a,
    _,
    n,
    o,
    s,
    i,
    r,
    d,
    p,
    b,
    c,
    h,
    L,
    y,
    u,
    v,
    f,
    g,
    N,
    k
  ];
}
class ts extends Ho {
  constructor(e) {
    super(), Ro(this, e, ls, es, Do, {
      gradio: 2,
      elem_id: 3,
      elem_classes: 4,
      visible: 5,
      value: 0,
      show_legend: 6,
      color_map: 1,
      label: 7,
      container: 8,
      scale: 9,
      min_width: 10,
      _selectable: 11,
      combine_adjacent: 15,
      interactive: 12,
      default_label: 13,
      loading_status: 14
    });
  }
}
export {
  xn as BaseInteractiveHighlightedText,
  In as BaseStaticHighlightedText,
  ts as default
};
