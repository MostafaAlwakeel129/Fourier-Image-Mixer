(function () {
    // Tuning knobs
    const CONTRAST_SENS = 0.005;   // horizontal sensitivity
    const BRIGHT_SENS = 0.003;     // vertical sensitivity (scaled by window width)
    const SAMPLE_TARGET = 5000;    // sampling for robust min/max
    const P_LO = 0.02, P_HI = 0.98;

    const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

    function sampleZ(z) {
        // z is typically 2D array (rows)
        if (!Array.isArray(z) || z.length === 0) return [];
        const rows = z.length;
        const cols = Array.isArray(z[0]) ? z[0].length : 0;
        if (!cols) return [];

        const total = rows * cols;
        const stride = Math.max(1, Math.floor(Math.sqrt(total / SAMPLE_TARGET)));

        const out = [];
        for (let r = 0; r < rows; r += stride) {
            const row = z[r];
            if (!Array.isArray(row)) continue;
            for (let c = 0; c < cols; c += stride) {
                const v = row[c];
                if (Number.isFinite(v)) out.push(v);
            }
        }
        return out;
    }

    function percentile(sorted, p) {
        if (!sorted.length) return 0;
        const idx = (sorted.length - 1) * p;
        const lo = Math.floor(idx);
        const hi = Math.ceil(idx);
        if (lo === hi) return sorted[lo];
        const t = idx - lo;
        return sorted[lo] * (1 - t) + sorted[hi] * t;
    }

    function initState(gd) {
        // gd is the Plotly graph div (class js-plotly-plot)
        if (gd._bcState) return gd._bcState;

        const trace = gd.data && gd.data[0];
        const z = trace && trace.z;
        const s = sampleZ(z);
        s.sort((a, b) => a - b);

        // robust defaults from percentiles (prevents a few hot pixels from ruining contrast)
        let baseMin = percentile(s, P_LO);
        let baseMax = percentile(s, P_HI);
        if (!(baseMax > baseMin)) { baseMin = 0; baseMax = 1; }

        const baseWidth = baseMax - baseMin;
        const state = {
            dragging: false,
            lastX: null,
            lastY: null,

            baseMin,
            baseMax,
            baseCenter: (baseMin + baseMax) / 2,
            baseWidth,

            center: (baseMin + baseMax) / 2,
            width: baseWidth,

            minWidth: baseWidth / 2000,      // don’t let it collapse to 0
            maxWidth: baseWidth * 50         // don’t let it explode forever
        };

        gd._bcState = state;
        return state;
    }

    function applyWindow(gd) {
        const st = gd._bcState;
        const half = st.width / 2;
        const zmin = st.center - half;
        const zmax = st.center + half;

        // Update only mapping (not the data) => instant
        Plotly.restyle(gd, { zmin: [zmin], zmax: [zmax] }, [0]);
    }

    function resetWindow(gd) {
        const st = initState(gd);
        st.center = st.baseCenter;
        st.width = st.baseWidth;
        applyWindow(gd);
    }

    function attachToGraphDiv(gd) {
        if (!gd || gd.dataset.bcAttached === "1") return;
        gd.dataset.bcAttached = "1";

        // Make pointer events reliable (touch + pen too)
        gd.style.touchAction = "none";
        gd.style.cursor = "grab";

        gd.addEventListener("pointerdown", (e) => {
            const st = initState(gd);
            st.dragging = true;
            st.lastX = e.clientX;
            st.lastY = e.clientY;
            gd.setPointerCapture?.(e.pointerId);
            gd.style.cursor = "grabbing";
        });

        gd.addEventListener("pointermove", (e) => {
            const st = initState(gd);
            if (!st.dragging) return;

            const dx = e.clientX - st.lastX;
            const dy = e.clientY - st.lastY;
            st.lastX = e.clientX;
            st.lastY = e.clientY;

            // Horizontal => contrast (window width), exponential feels nice
            const factor = Math.exp(dx * CONTRAST_SENS);
            st.width = clamp(st.width * factor, st.minWidth, st.maxWidth);

            // Vertical => brightness (window center), scale by width so it feels consistent
            st.center += (-dy) * (st.width * BRIGHT_SENS);

            applyWindow(gd);
        });

        const stopDrag = () => {
            const st = initState(gd);
            st.dragging = false;
            gd.style.cursor = "grab";
        };

        gd.addEventListener("pointerup", stopDrag);
        gd.addEventListener("pointercancel", stopDrag);
        gd.addEventListener("pointerleave", stopDrag);

        // Double click to reset window/level
        gd.addEventListener("dblclick", (e) => {
            e.preventDefault();
            resetWindow(gd);
        });
    }

    function scanAndAttach() {
        // We attached stable ids: raw-graph-1..4, so look for them
        for (let i = 1; i <= 4; i++) {
            const outer = document.getElementById(`raw-graph-${i}`);
            if (!outer) continue;

            // Plotly graph div inside dcc.Graph
            const gd = outer.querySelector(".js-plotly-plot");
            if (gd) attachToGraphDiv(gd);
        }
    }

    // Attach now + whenever Dash re-renders graphs
    document.addEventListener("DOMContentLoaded", scanAndAttach);
    new MutationObserver(scanAndAttach).observe(document.body, { childList: true, subtree: true });
})();