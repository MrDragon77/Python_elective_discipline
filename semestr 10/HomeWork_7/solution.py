import numpy as np
import cv2
import time
from scipy.ndimage import sobel, gaussian_filter
from sklearn.metrics import mean_squared_error, r2_score


def make_image(size=256, n_cells=15, cell_radius=10, noise_std=8, seed=0):
    rng = np.random.default_rng(seed)
    img = np.full((size, size), 220, dtype=np.float32)
    centers = []
    attempts = 0
    while len(centers) < n_cells and attempts < 5000:
        r = rng.integers(cell_radius, size - cell_radius)
        c = rng.integers(cell_radius, size - cell_radius)
        if all(np.hypot(r - cr, c - cc) > cell_radius * 2.2 for cr, cc in centers):
            centers.append((r, c))
            rr, cc = np.ogrid[:size, :size]
            mask = (rr - r) ** 2 + (cc - c) ** 2 <= cell_radius ** 2
            img[mask] = rng.integers(30, 80)
        attempts += 1
    img += rng.normal(0, noise_std, img.shape).astype(np.float32)
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8), centers


def sobel_gradients(img, sigma=2.0):
    smooth = gaussian_filter(img.astype(np.float32), sigma=sigma)
    gy = sobel(smooth, axis=0)
    gx = sobel(smooth, axis=1)
    return gx, gy


def find_convergence(gx, gy, start_r, start_c, lr=0.5, n_iter=150):
    H, W = gx.shape
    r, c = float(start_r), float(start_c)
    for _ in range(n_iter):
        ri = int(np.clip(r, 0, H - 1))
        ci = int(np.clip(c, 0, W - 1))
        gr, gc = gy[ri, ci], gx[ri, ci]
        mag = np.hypot(gr, gc) + 1e-8
        r -= lr * gr / mag
        c -= lr * gc / mag
        r = float(np.clip(r, 0, H - 1))
        c = float(np.clip(c, 0, W - 1))
    return int(round(r)), int(round(c))


def merge_clusters(points, eps):
    clusters = []
    for p in points:
        merged = False
        for cl in clusters:
            cr, cc = cl['center']
            if np.hypot(p[0] - cr, p[1] - cc) < eps:
                cl['members'].append(p)
                n = len(cl['members'])
                cl['center'] = (
                    sum(m[0] for m in cl['members']) / n,
                    sum(m[1] for m in cl['members']) / n,
                )
                merged = True
                break
        if not merged:
            clusters.append({'center': (float(p[0]), float(p[1])), 'members': [p]})
    return clusters


def detect_cells(img, gx, gy, N=20, W_block=80, H_block=80, R=8,
                 lr=0.5, n_iter=150, eps_cluster=14, seed=1):
    rng = np.random.default_rng(seed)
    H, W = img.shape
    conv_pts = []
    for _ in range(N):
        r0 = rng.integers(0, max(H - H_block, 1))
        c0 = rng.integers(0, max(W - W_block, 1))
        for _ in range(R):
            sr = rng.integers(r0, min(r0 + H_block, H))
            sc = rng.integers(c0, min(c0 + W_block, W))
            cr, cc = find_convergence(gx, gy, sr, sc, lr=lr, n_iter=n_iter)
            if img[cr, cc] < 130:
                conv_pts.append((cr, cc))
    clusters = merge_clusters(conv_pts, eps=eps_cluster)
    return clusters, conv_pts


def _draw_histogram(values, title, color_bgr, width=300, height=200):
    canvas = np.full((height, width, 3), 240, dtype=np.uint8)
    if not values:
        return canvas
    arr = np.array(values)
    counts, edges = np.histogram(arr, bins=10)
    bar_w = width // 10
    max_c = max(counts) if max(counts) > 0 else 1
    for i, cnt in enumerate(counts):
        bar_h = int(cnt / max_c * (height - 30))
        x1 = i * bar_w + 2
        x2 = (i + 1) * bar_w - 2
        y1 = height - 20 - bar_h
        y2 = height - 20
        cv2.rectangle(canvas, (x1, y1), (x2, y2), color_bgr, -1)
    cv2.putText(canvas, title, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    return canvas


def show_results(img, true_centers, clusters, conv_pts):
    bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    panel1 = bgr.copy()
    for r, c in true_centers:
        cv2.circle(panel1, (c, r), 12, (0, 255, 0), 2)
    cv2.putText(panel1, 'True centers', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    panel2 = bgr.copy()
    for r, c in conv_pts:
        cv2.circle(panel2, (c, r), 2, (0, 0, 255), -1)
    cv2.putText(panel2, 'Convergence pts', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    panel3 = bgr.copy()
    for cl in clusters:
        r, c = cl['center']
        cv2.circle(panel3, (int(c), int(r)), 12, (255, 255, 0), 2)
    cv2.putText(panel3, f'Detected: {len(clusters)}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    combined = np.hstack([panel1, panel2, panel3])
    cv2.imwrite('segmentation_result.png', combined)
    print('segmentation_result.png saved')


def analyze_cells(img, clusters, cell_radius=12):
    H, W = img.shape
    stats = []
    for cl in clusters:
        r, c = cl['center']
        ri, ci = int(round(r)), int(round(c))
        rr, cc = np.ogrid[:H, :W]
        mask = (rr - ri) ** 2 + (cc - ci) ** 2 <= cell_radius ** 2
        region = img[mask]
        stats.append({
            'mean_intensity': float(region.mean()),
            'std_intensity':  float(region.std()),
            'min_intensity':  float(region.min()),
            'area':           int(mask.sum()),
            'members':        len(cl['members']),
        })

    if not stats:
        print('No cells detected.')
        return stats

    means   = [s['mean_intensity'] for s in stats]
    stds    = [s['std_intensity']  for s in stats]
    areas   = [s['area']           for s in stats]
    members = [s['members']        for s in stats]

    print(f'\nEDA: {len(stats)} cells')
    print(f'mean intensity: {np.mean(means):.1f} +/- {np.std(means):.1f}')
    print(f'mean area:      {np.mean(areas):.1f}')
    print(f'mean conv pts:  {np.mean(members):.1f}')

    h1 = _draw_histogram(means,   'Mean intensity',  (200, 100, 50))
    h2 = _draw_histogram(stds,    'Std intensity',   (50, 100, 200))
    h3 = _draw_histogram(areas,   'Cell area',       (50, 180, 80))
    h4 = _draw_histogram(members, 'Conv pts count',  (180, 50, 180))

    top = np.hstack([h1, h2])
    bot = np.hstack([h3, h4])
    eda_img = np.vstack([top, bot])
    cv2.imwrite('eda_result.png', eda_img)
    print('eda_result.png saved')
    return stats


def measure_quality(size=256, cell_counts=(5, 8, 10, 12, 15, 18, 20),
                    seeds=(0, 1, 2, 3, 4, 5, 6)):
    true_counts, pred_counts = [], []
    for n, seed in zip(cell_counts, seeds):
        img, _ = make_image(size=size, n_cells=n, seed=seed)
        gx, gy = sobel_gradients(img)
        clusters, _ = detect_cells(img, gx, gy, N=25, R=10, seed=seed)
        true_counts.append(n)
        pred_counts.append(len(clusters))
        print(f'true={n:2d}  pred={len(clusters):2d}')

    mse = mean_squared_error(true_counts, pred_counts)
    r2  = r2_score(true_counts, pred_counts)
    print(f'\nMSE={mse:.2f}  R2={r2:.3f}')

    # scatter plot via cv2
    W, H = 400, 350
    canvas = np.full((H, W, 3), 255, dtype=np.uint8)
    mn, mx = min(true_counts), max(true_counts)
    def to_px(v): return int((v - mn) / (mx - mn + 1e-8) * (W - 60) + 30)
    def to_py(v): return int(H - 30 - (v - mn) / (mx - mn + 1e-8) * (H - 60))

    # ideal line
    cv2.line(canvas, (to_px(mn), to_py(mn)), (to_px(mx), to_py(mx)), (0, 0, 200), 1)
    for t, p in zip(true_counts, pred_counts):
        cv2.circle(canvas, (to_px(t), to_py(p)), 5, (200, 80, 0), -1)
    cv2.putText(canvas, f'MSE={mse:.2f} R2={r2:.3f}', (30, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(canvas, 'True count', (W // 2 - 30, H - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    cv2.imwrite('quality_metric.png', canvas)
    print('quality_metric.png saved')
    return mse, r2


def _eval_params(N, W_block, H_block, R, img, true_count, seed=42):
    t0 = time.perf_counter()
    gx, gy = sobel_gradients(img)
    clusters, _ = detect_cells(img, gx, gy, N=N, W_block=W_block, H_block=H_block, R=R, seed=seed)
    elapsed = time.perf_counter() - t0
    pred = len(clusters)
    accuracy = max(0.0, 1.0 - abs(pred - true_count) / max(true_count, 1))
    return accuracy, elapsed


def optimize_params(img, true_count, mu1=0.7, mu2=0.3, sigma_t=2.0,
                    n_iter=12, step=1.5,
                    N0=5, W0=30, H0=30, R0=2):
    """
    Optimize N, W_block, H_block, R by maximizing:
        f = mu1 * F / max_F + mu2 * gauss(T) / gauss(0)
    where F = accuracy, T = processing time.
    Gradient estimated numerically with finite differences.
    """
    max_F = 1.0

    def gauss(t):
        return np.exp(-0.5 * (t / sigma_t) ** 2)

    def objective(N, W, H, R):
        N, W, H, R = max(1, int(round(N))), max(10, int(round(W))), \
                     max(10, int(round(H))), max(1, int(round(R)))
        F, T = _eval_params(N, W, H, R, img, true_count)
        return mu1 * F / max_F + mu2 * gauss(T) / gauss(0)

    params = np.array([float(N0), float(W0), float(H0), float(R0)])
    deltas = np.array([3.0, 15.0, 15.0, 2.0])

    print(f'\nOptimizing params (mu1={mu1}, mu2={mu2}):')
    print(f'  start: N={N0} W={W0} H={H0} R={R0}')
    for it in range(n_iter):
        f0 = objective(*params)
        grad = np.zeros(4)
        for i in range(4):
            p_plus = params.copy()
            p_plus[i] += deltas[i]
            grad[i] = (objective(*p_plus) - f0) / deltas[i]
        norm = np.linalg.norm(grad) + 1e-8
        params += step * grad / norm
        params = np.clip(params, [1, 10, 10, 1], [60, 200, 200, 20])
        N, W, H, R = (max(1, int(round(p))) for p in params)
        print(f'  iter {it+1:2d}: f={f0:.4f}  N={N} W={W} H={H} R={R}')

    N, W, H, R = (max(1, int(round(p))) for p in params)
    F_opt, T_opt = _eval_params(N, W, H, R, img, true_count)
    print(f'Optimal: N={N} W={W} H={H} R={R}  accuracy={F_opt:.3f}  time={T_opt:.3f}s')
    return N, W, H, R


if __name__ == '__main__':
    print('Generating image...')
    img, true_centers = make_image(size=256, n_cells=15, seed=42)
    print(f'Image shape: {img.shape}, true cells: {len(true_centers)}')

    print('Computing gradients...')
    gx, gy = sobel_gradients(img)

    print('Detecting cells...')
    clusters, conv_pts = detect_cells(img, gx, gy, N=25, W_block=80, H_block=80, R=10)
    print(f'Detected: {len(clusters)} cells (true: {len(true_centers)})')

    show_results(img, true_centers, clusters, conv_pts)
    analyze_cells(img, clusters)

    print('\nQuality metrics:')
    measure_quality()

    print('\nParameter optimization (Task 2):')
    optimize_params(img, len(true_centers))
