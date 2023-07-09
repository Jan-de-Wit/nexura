(allowedBrowsers = ["IEWin7", "Edge", "Chrome", "Safari", "Firefox"]),
  (function () {
    var e,
      t,
      o,
      r,
      n = {
        frameRate: 150,
        animationTime: 400,
        stepSize: 100,
        pulseAlgorithm: !0,
        pulseScale: 4,
        pulseNormalize: 1,
        accelerationDelta: 50,
        accelerationMax: 3,
        keyboardSupport: !0,
        arrowScroll: 50,
      },
      l = n,
      a = !1,
      i = { x: 0, y: 0 },
      s = !1,
      c = document.documentElement,
      u = [],
      d = /^Mac/.test(navigator.platform),
      f = {
        left: 37,
        up: 38,
        right: 39,
        down: 40,
        spacebar: 32,
        pageup: 33,
        pagedown: 34,
        end: 35,
        home: 36,
      },
      h = { 37: 1, 38: 1, 39: 1, 40: 1 };
    function $() {
      var r, n, i, u, d, f;
      !s &&
        document.body &&
        ((s = !0),
        (r = document.body),
        (n = document.documentElement),
        (f = window.innerHeight),
        (i = r.scrollHeight),
        (c = 0 <= document.compatMode.indexOf("CSS") ? n : r),
        (e = r),
        l.keyboardSupport && M("keydown", b),
        top != self
          ? (a = !0)
          : Q &&
            f < i &&
            (r.offsetHeight <= f || n.offsetHeight <= f) &&
            (((u = document.createElement("div")).style.cssText =
              "position:absolute; z-index:-10000; top:0; left:0; right:0; height:" +
              c.scrollHeight +
              "px"),
            document.body.appendChild(u),
            (o = function () {
              d =
                d ||
                setTimeout(function () {
                  (u.style.height = "0"),
                    (u.style.height = c.scrollHeight + "px"),
                    (d = null);
                }, 500);
            }),
            setTimeout(o, 10),
            M("resize", o),
            (t = new R(o)).observe(r, {
              attributes: !0,
              childList: !0,
              characterData: !1,
            }),
            c.offsetHeight <= f &&
              (((f = document.createElement("div")).style.clear = "both"),
              r.appendChild(f))));
    }
    var p = [],
      m = !1,
      _ = Date.now();
    function v(e, t, o) {
      var r, n, a, s, c, u, d;
      (r = 0 < (r = t) ? 1 : -1),
        (n = 0 < (n = o) ? 1 : -1),
        (i.x === r && i.y === n) || ((i.x = r), (i.y = n), (p = []), (_ = 0)),
        1 != l.accelerationMax &&
          ((n = Date.now() - _) < l.accelerationDelta &&
            1 < (a = (1 + 50 / n) / 2) &&
            ((t *= a = Math.min(a, l.accelerationMax)), (o *= a)),
          (_ = Date.now())),
        p.push({
          x: t,
          y: o,
          lastX: t < 0 ? 0.99 : -0.99,
          lastY: o < 0 ? 0.99 : -0.99,
          start: Date.now(),
        }),
        m ||
          ((s = e === (a = q()) || e === document.body),
          null == e.$scrollBehavior &&
            (null == D[(d = S((u = e)))] &&
              ((u = getComputedStyle(u, "")["scroll-behavior"]),
              (D[d] = "smooth" == u)),
            D[d]) &&
            ((e.$scrollBehavior = e.style.scrollBehavior),
            (e.style.scrollBehavior = "auto")),
          (c = function (r) {
            for (var n = Date.now(), a = 0, i = 0, u = 0; u < p.length; u++) {
              var d,
                f = p[u],
                h = n - f.start,
                $ = h >= l.animationTime,
                _ = $ ? 1 : h / l.animationTime;
              l.pulseAlgorithm &&
                (_ =
                  1 <= (d = _)
                    ? 1
                    : d <= 0
                    ? 0
                    : (1 == l.pulseNormalize && (l.pulseNormalize /= F(1)),
                      F(d))),
                (h = (f.x * _ - f.lastX) >> 0),
                (_ = (f.y * _ - f.lastY) >> 0),
                (a += h),
                (i += _),
                (f.lastX += h),
                (f.lastY += _),
                $ && (p.splice(u, 1), u--);
            }
            s
              ? window.scrollBy(a, i)
              : (a && (e.scrollLeft += a), i && (e.scrollTop += i)),
              (p = t || o ? p : []).length
                ? A(c, e, 1e3 / l.frameRate + 1)
                : ((m = !1),
                  null != e.$scrollBehavior &&
                    ((e.style.scrollBehavior = e.$scrollBehavior),
                    (e.$scrollBehavior = null)));
          }),
          A(c, e, 0),
          (m = !0));
    }
    function y(t) {
      s || $();
      var o = t.target;
      if (
        t.defaultPrevented ||
        t.ctrlKey ||
        X(e, "embed") ||
        (X(o, "embed") && /\.pdf/i.test(o.src)) ||
        X(e, "object") ||
        o.shadowRoot
      )
        return !0;
      var n = -t.wheelDeltaX || t.deltaX || 0,
        i = -t.wheelDeltaY || t.deltaY || 0;
      return (
        d &&
          (t.wheelDeltaX &&
            N(t.wheelDeltaX, 120) &&
            (n = -((t.wheelDeltaX / Math.abs(t.wheelDeltaX)) * 120)),
          t.wheelDeltaY &&
            N(t.wheelDeltaY, 120) &&
            (i = -((t.wheelDeltaY / Math.abs(t.wheelDeltaY)) * 120))),
        n || i || (i = -t.wheelDelta || 0),
        1 === t.deltaMode && ((n *= 40), (i *= 40)),
        (o = C(o))
          ? !!(function (e) {
              if (e) {
                u.length || (u = [e, e, e]),
                  (e = Math.abs(e)),
                  u.push(e),
                  u.shift(),
                  clearTimeout(r),
                  (r = setTimeout(function () {
                    try {
                      localStorage.SS_deltaBuffer = u.join(",");
                    } catch (e) {}
                  }, 1e3));
                var t = 120 < e && K(e),
                  t = !K(120) && !K(100) && !t;
                return e < 50 || t;
              }
            })(i) ||
            (1.2 < Math.abs(n) && (n *= l.stepSize / 120),
            1.2 < Math.abs(i) && (i *= l.stepSize / 120),
            v(o, n, i),
            t.preventDefault(),
            void O())
          : !a ||
            !V ||
            (Object.defineProperty(t, "target", { value: window.frameElement }),
            parent.wheel(t))
      );
    }
    function b(t) {
      var o = t.target,
        r =
          t.ctrlKey ||
          t.altKey ||
          t.metaKey ||
          (t.shiftKey && t.keyCode !== f.spacebar);
      document.body.contains(e) || (e = document.activeElement);
      var n = /^(button|submit|radio|checkbox|file|color|image)$/i;
      if (
        t.defaultPrevented ||
        /^(textarea|select|embed|object)$/i.test(o.nodeName) ||
        (X(o, "input") && !n.test(o.type)) ||
        X(e, "video") ||
        (function (e) {
          var t = e.target,
            o = !1;
          if (-1 != document.URL.indexOf("www.youtube.com/watch"))
            do
              if (
                (o =
                  t.classList && t.classList.contains("html5-video-controls"))
              )
                break;
            while ((t = t.parentNode));
          return o;
        })(t) ||
        o.isContentEditable ||
        r ||
        ((X(o, "button") || (X(o, "input") && n.test(o.type))) &&
          t.keyCode === f.spacebar) ||
        (X(o, "input") && "radio" == o.type && h[t.keyCode])
      )
        return !0;
      var i = 0,
        s = 0,
        c = C(e);
      if (!c) return !a || !V || parent.keydown(t);
      var u = c.clientHeight;
      switch ((c == document.body && (u = window.innerHeight), t.keyCode)) {
        case f.up:
          s = -l.arrowScroll;
          break;
        case f.down:
          s = l.arrowScroll;
          break;
        case f.spacebar:
          s = -(t.shiftKey ? 1 : -1) * u * 0.9;
          break;
        case f.pageup:
          s = -(0.9 * u);
          break;
        case f.pagedown:
          s = 0.9 * u;
          break;
        case f.home:
          s = -(c =
            c == document.body && document.scrollingElement
              ? document.scrollingElement
              : c).scrollTop;
          break;
        case f.end:
          var d = c.scrollHeight - c.scrollTop - u,
            s = 0 < d ? 10 + d : 0;
          break;
        case f.left:
          i = -l.arrowScroll;
          break;
        case f.right:
          i = l.arrowScroll;
          break;
        default:
          return !0;
      }
      v(c, i, s), t.preventDefault(), O();
    }
    function w(t) {
      e = t.target;
    }
    var g,
      x,
      S =
        ((g = 0),
        function (e) {
          return e.uniqueID || (e.uniqueID = g++);
        }),
      E = {},
      k = {},
      D = {};
    function O() {
      clearTimeout(x),
        (x = setInterval(function () {
          E = k = D = {};
        }, 1e3));
    }
    function B(e, t, o) {
      for (var r = o ? E : k, n = e.length; n--; ) r[S(e[n])] = t;
      return t;
    }
    function C(e) {
      var t = [],
        o = document.body,
        r = c.scrollHeight;
      do {
        var n = k[S(e)];
        if (n) return B(t, n);
        if ((t.push(e), r === e.scrollHeight)) {
          if (((n = (T(c) && T(o)) || z(c)), (a && H(c)) || (!a && n)))
            return B(t, q());
        } else if (H(e) && z(e)) return B(t, e);
      } while ((e = e.parentElement));
    }
    function H(e) {
      return e.clientHeight + 10 < e.scrollHeight;
    }
    function T(e) {
      return (
        "hidden" !== getComputedStyle(e, "").getPropertyValue("overflow-y")
      );
    }
    function z(e) {
      return (
        "scroll" ===
          (e = getComputedStyle(e, "").getPropertyValue("overflow-y")) ||
        "auto" === e
      );
    }
    function M(e, t, o) {
      window.addEventListener(e, t, o || !1);
    }
    function L(e, t, o) {
      window.removeEventListener(e, t, o || !1);
    }
    function X(e, t) {
      return e && (e.nodeName || "").toLowerCase() === t.toLowerCase();
    }
    if (window.localStorage && localStorage.SS_deltaBuffer)
      try {
        u = localStorage.SS_deltaBuffer.split(",");
      } catch (Y) {}
    function N(e, t) {
      return Math.floor(e / t) == e / t;
    }
    function K(e) {
      return N(u[0], e) && N(u[1], e) && N(u[2], e);
    }
    var P,
      A =
        window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        function (e, t, o) {
          window.setTimeout(e, o || 1e3 / 60);
        },
      R =
        window.MutationObserver ||
        window.WebKitMutationObserver ||
        window.MozMutationObserver,
      q =
        ((P = document.scrollingElement),
        function () {
          var e, t;
          return (
            P ||
              (((e = document.createElement("div")).style.cssText =
                "height:10000px;width:1px;"),
              document.body.appendChild(e),
              (t = document.body.scrollTop),
              document.documentElement.scrollTop,
              window.scrollBy(0, 3),
              (P =
                document.body.scrollTop != t
                  ? document.body
                  : document.documentElement),
              window.scrollBy(0, -3),
              document.body.removeChild(e)),
            P
          );
        });
    function F(e) {
      var t;
      return (
        ((e *= l.pulseScale) < 1
          ? e - (1 - Math.exp(-e))
          : (--e, (t = Math.exp(-1)) + (1 - Math.exp(-e)) * (1 - t))) *
        l.pulseNormalize
      );
    }
    var j = window.navigator.userAgent,
      I = /Edge/.test(j),
      V = /chrome/i.test(j) && !I,
      W = /safari/i.test(j) && !I,
      U = /firefox/i.test(j),
      G = /mobile/i.test(j),
      J = /Windows NT 6.1/i.test(j) && /rv:11/i.test(j),
      Q = W && (/Version\/8/i.test(j) || /Version\/9/i.test(j)),
      Z = G
        ? ~allowedBrowsers.indexOf("Mobile")
        : I
        ? ~allowedBrowsers.indexOf("Edge")
        : V
        ? ~allowedBrowsers.indexOf("Chrome")
        : W
        ? ~allowedBrowsers.indexOf("Safari")
        : U
        ? ~allowedBrowsers.indexOf("Firefox")
        : J
        ? ~allowedBrowsers.indexOf("IEWin7")
        : ~allowedBrowsers.indexOf("other"),
      ee = !1;
    try {
      window.addEventListener(
        "test",
        null,
        Object.defineProperty({}, "passive", {
          get: function () {
            ee = !0;
          },
        })
      );
    } catch (et) {}
    var j = !!ee && { passive: !1 },
      eo = "onwheel" in document.createElement("div") ? "wheel" : "mousewheel";
    function er(e) {
      for (var t in e) n.hasOwnProperty(t) && (l[t] = e[t]);
    }
    eo && Z && (M(eo, y, j), M("mousedown", w), M("load", $)),
      (er.destroy = function () {
        t && t.disconnect(),
          L(eo, y),
          L("mousedown", w),
          L("keydown", b),
          L("resize", o),
          L("load", $);
      }),
      window.SmoothScrollOptions && er(window.SmoothScrollOptions),
      "function" == typeof define && define.amd
        ? define(function () {
            return er;
          })
        : "object" == typeof exports
        ? (module.exports = er)
        : (window.SmoothScroll = er);
  })();
