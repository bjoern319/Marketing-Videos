/* KNIGGE Katana remix: kinetic type and brand layer (Red Hat Display, KNIGGE red #CA2C35, slate #444F4F). */
(function () {
  const U = RRC.util;
  const FONT = '"RHD", sans-serif';
  let LOGO = null;
  RRC.hook("ready", async () => {
    LOGO = await U.img("comp/assets/logo.png", true);
  });
  const c01 = (v) => Math.max(0, Math.min(1, v));
  const eo3 = (t) => 1 - Math.pow(1 - c01(t), 3);
  const ei2 = (t) => Math.pow(c01(t), 2);
  const ei3 = (t) => Math.pow(c01(t), 3);
  const ob = (t) => {
    t = c01(t);
    const c1 = 1.70158, c3 = c1 + 1;
    return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
  };
  const fnt = (w, size, it) => `${it ? "italic " : ""}${w} ${size}px ${FONT}`;

  function glowText(x, txt, cx, cy, size, o) {
    x.save();
    x.globalAlpha = o.alpha ?? 1;
    x.translate(cx, cy);
    const sc = o.scale ?? 1;
    x.scale(sc, sc);
    x.font = fnt(o.w ?? 800, size, o.it);
    x.textAlign = o.align || "center";
    x.textBaseline = "middle";
    x.letterSpacing = (o.track ?? 0) + "px";
    if (o.blur) x.filter = `blur(${U.px(o.blur)}px)`;
    if (o.glow) {
      x.shadowColor = o.glow;
      x.shadowBlur = U.px(o.glowBlur ?? 30);
    }
    x.fillStyle = o.fill || "#ffffff";
    x.fillText(txt, 0, 0);
    if (o.glow) {
      x.shadowBlur = U.px((o.glowBlur ?? 30) * 0.35);
      x.fillText(txt, 0, 0);
    }
    x.restore();
  }

  // Title written into the sky, then flown through by the FPV approach (ref F10-F59).
  RRC.register("LAYERS", "skytitle", {
    phase: "over",
    order: 60,
    draw(S, p, x) {
      const lt = S.lt, W = S.W, H = S.H, size = p.size ?? 104;
      const w0 = p.w0 ?? 0.12, w1 = p.w1 ?? 0.55, f0 = p.f0 ?? 1.05, f1 = p.f1 ?? 1.5;
      if (lt < w0) return;
      let sc = 1 + 0.1 * c01((lt - w0) / (f0 - w0)), cy = (p.y ?? 0.13) * H, alpha = 1, blur = 0;
      if (lt > f0) {
        const u = ei3((lt - f0) / (f1 - f0));
        sc *= 1 + 5.5 * u;
        cy -= u * 0.5 * H;
        alpha = 1 - c01(((lt - f0) / (f1 - f0)) * 1.15);
        blur = 14 * u;
      }
      if (alpha <= 0.01) return;
      x.save();
      x.font = fnt(p.w ?? 800, size, p.it);
      x.letterSpacing = (p.track ?? 0) + "px";
      const tw = x.measureText(p.text).width * sc;
      x.restore();
      const rev = eo3((lt - w0) / (w1 - w0));
      x.save();
      x.beginPath();
      x.rect(W / 2 - tw / 2 - 60, 0, (tw + 120) * rev, H);
      x.clip();
      glowText(x, p.text, W / 2, cy, size, { w: p.w ?? 800, it: p.it, glow: "rgba(255,236,210,0.9)", glowBlur: 28, alpha, scale: sc, blur, track: p.track });
      x.restore();
    },
  });

  // A word anchored in the empty room; the camera flies through it into a white smear (ref F81-F109).
  RRC.register("LAYERS", "flyword", {
    phase: "over",
    order: 61,
    draw(S, p, x) {
      const lt = S.lt, d = S.dur, W = S.W, H = S.H;
      const a0 = p.a0 ?? 0.08, f0 = p.f0 ?? d - 0.24;
      if (lt < a0) return;
      const s0 = p.s0 ?? 0.55, s1 = p.s1 ?? 1.0;
      let sc = s0 + (s1 - s0) * c01((lt - a0) / (f0 - a0)), alpha = eo3((lt - a0) / 0.12), blur = 0;
      if (lt > f0) {
        const u = ei3((lt - f0) / (d - f0));
        sc *= 1 + 9 * u;
        alpha *= 1 - u;
        blur = 18 * u;
      }
      glowText(x, p.text, W / 2, (p.y ?? 0.5) * H, p.size ?? 150, { w: p.w ?? 900, glow: "rgba(205,228,255,0.95)", glowBlur: 34, alpha, scale: sc, blur, track: p.track ?? -2 });
      if (lt > f0) {
        x.save();
        x.globalAlpha = 0.85 * ei2((lt - f0) / (d - f0));
        x.fillStyle = "#ffffff";
        x.fillRect(0, 0, W, H);
        x.restore();
      }
    },
  });

  // Room label that pops in once the room is alive (ref 'FAMILY ROOM' F128-F172).
  RRC.register("LAYERS", "label", {
    phase: "over",
    order: 62,
    draw(S, p, x) {
      const lt = S.lt, d = S.dur, W = S.W, H = S.H, a0 = p.a0 ?? 0.4;
      if (lt < a0) return;
      const pop = ob((lt - a0) / 0.24);
      const alpha = c01((lt - a0) / 0.1) * (1 - c01((lt - (d - 0.12)) / 0.12));
      const drift = ((p.drift ?? -36) * (lt - a0)) / (d - a0);
      glowText(x, p.text, W * (p.x ?? 0.5) + drift, H * (p.y ?? 0.33), p.size ?? 150, { w: p.w ?? 800, it: p.it ?? true, glow: "rgba(255,186,110,0.95)", glowBlur: 34, alpha, scale: 0.6 + 0.4 * pop, track: p.track ?? 1 });
    },
  });

  // Season word over the locked-off facade.
  RRC.register("LAYERS", "season", {
    phase: "over",
    order: 63,
    draw(S, p, x) {
      const lt = S.lt, d = S.dur, W = S.W, H = S.H;
      const k = eo3((lt - 0.04) / 0.2);
      const alpha = k * (1 - c01((lt - (d - 0.08)) / 0.08));
      if (alpha <= 0) return;
      // dark pill behind the word so it reads on bright spring and sunset skies
      const size = p.size ?? 62, cy = H * (p.y ?? 0.135) + (1 - k) * 26;
      x.save();
      x.font = fnt(800, size);
      x.letterSpacing = (p.track ?? 14) + "px";
      const tw = x.measureText(p.text).width;
      x.globalAlpha = alpha;
      x.fillStyle = "rgba(24,28,32,0.42)";
      x.beginPath();
      x.roundRect(W / 2 - tw / 2 - 34, cy - size * 0.78, tw + 68 - (p.track ?? 14), size * 1.56, size * 0.78);
      x.fill();
      x.restore();
      glowText(x, p.text, W / 2, cy, size, { w: 800, glow: "rgba(0,0,0,0.5)", glowBlur: 14, alpha, track: p.track ?? 14 });
    },
  });

  // Warm light of the party inside the front door while the camera pulls back out (ref F897-F914).
  RRC.register("LAYERS", "doorglow", {
    phase: "post",
    order: 40,
    draw(S, p, x) {
      const M = S.M;
      if (!M || !p.box) return;
      const [x0, y0, x1, y1] = p.box;
      const map = (u, v) => [M[0] * u + M[2] * v + M[4], M[1] * u + M[3] * v + M[5]];
      const a = map(x0, y0), b = map(x1, y1);
      const u = c01(S.lt / S.dur);
      const alpha = 1 - eo3(u * 1.15);
      if (alpha <= 0) return;
      x.save();
      x.globalAlpha = alpha;
      x.shadowColor = "rgba(255,210,140,1)";
      x.shadowBlur = U.px(50 + 90 * (1 - u));
      x.fillStyle = "rgba(255,238,205,1)";
      x.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]);
      x.restore();
    },
  });

  // Brand end card: white panel, KNIGGE logo (unchanged), headline, CTA, URL. Text stays inside 168-1330 px.
  RRC.register("LAYERS", "endcard", {
    phase: "post",
    order: 90,
    draw(S, p, x) {
      const t = S.t, W = S.W, H = S.H, T0 = p.t0 ?? 17.38, top = p.top ?? 820, L = p.left ?? 72;
      const k = eo3((t - T0) / 0.45);
      if (k <= 0) return;
      const y0 = H - (H - top) * k;
      x.save();
      const g = x.createLinearGradient(0, y0 - 160, 0, y0);
      g.addColorStop(0, "rgba(20,24,28,0)");
      g.addColorStop(1, "rgba(20,24,28,0.3)");
      x.fillStyle = g;
      x.fillRect(0, y0 - 160, W, 160);
      x.fillStyle = "#ffffff";
      const r = 46;
      x.beginPath();
      x.moveTo(0, y0 + r);
      x.arcTo(0, y0, r, y0, r);
      x.lineTo(W - r, y0);
      x.arcTo(W, y0, W, y0 + r, r);
      x.lineTo(W, H);
      x.lineTo(0, H);
      x.closePath();
      x.fill();
      x.restore();
      const dy = y0 - top;
      const item = (ta, fn) => {
        const u = (t - ta) / 0.32;
        if (u > 0) fn(eo3(u), ob(u));
      };
      item(p.tl ?? 17.6, (e) => {
        if (!LOGO) return;
        const h = p.logo_h ?? 80, w = (h * LOGO.width) / LOGO.height;
        x.save();
        x.globalAlpha = e;
        x.drawImage(LOGO, L, top + 60 + dy + (1 - e) * 30, w, h);
        x.restore();
      });
      item(p.t1 ?? 17.79, (e) => {
        x.save();
        x.globalAlpha = e;
        x.font = fnt(800, 58);
        x.fillStyle = "#444F4F";
        x.textBaseline = "alphabetic";
        x.fillText(p.l1, L - (1 - e) * 40, top + 220 + dy);
        x.restore();
      });
      item(p.t2 ?? 18.207, (e, o) => {
        x.save();
        x.globalAlpha = e;
        const sc = 0.7 + 0.3 * o;
        x.translate(L, top + 340 + dy);
        x.scale(sc, sc);
        x.font = fnt(900, 132);
        x.letterSpacing = "-3px";
        x.fillStyle = "#CA2C35";
        x.textBaseline = "alphabetic";
        x.fillText(p.l2, 0, 0);
        x.restore();
      });
      item(p.t3 ?? 18.62, (e, o) => {
        x.save();
        x.globalAlpha = e;
        x.font = fnt(800, 38);
        const cw = x.measureText(p.cta).width + 64, ch = 76, cy = top + 370 + dy;
        const sc = 0.8 + 0.2 * o;
        x.translate(L, cy + ch / 2);
        x.scale(sc, sc);
        x.translate(0, -ch / 2);
        x.fillStyle = "#CA2C35";
        x.beginPath();
        x.roundRect(0, 0, cw, ch, 20);
        x.fill();
        x.fillStyle = "#ffffff";
        x.textBaseline = "middle";
        x.fillText(p.cta, 32, ch / 2 + 2);
        x.restore();
      });
      item(p.t4 ?? 18.83, (e) => {
        x.save();
        x.globalAlpha = e;
        x.font = fnt(700, 40);
        x.fillStyle = "#444F4F";
        x.textBaseline = "alphabetic";
        x.fillText(p.url, L, top + 498 + dy);
        x.restore();
      });
    },
  });
})();
