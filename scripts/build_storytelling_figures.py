"""Export numbered PNG/SVG figures from reconciled handoff evidence."""

from __future__ import annotations

import hashlib
import json
import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache/matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from build_storytelling_evidence import OUTPUT, build

FIGURES = ROOT / "deliverables/report/figures"
INK, TEAL, RED, AMBER, GRAY = "#253746", "#087F8C", "#BC3F32", "#AF761D", "#667582"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK,
                     "ytick.color": INK, "axes.titleweight": "bold", "svg.fonttype": "none"})


def vi(value: float, digits: int = 0) -> str:
    return f"{value:,.{digits}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def canvas(title: str, subtitle: str):
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.4))
    fig.subplots_adjust(left=.12, right=.97, top=.69, bottom=.20, wspace=.45)
    fig.text(.055, .965, textwrap.fill(title, width=83), fontsize=17, weight="bold", va="top")
    fig.text(.055, .80, subtitle, fontsize=10, color=GRAY)
    return fig, axes


def save(fig, stem: str) -> None:
    for ext in ["png", "svg"]:
        path = FIGURES / f"{stem}.{ext}"
        fig.savefig(path, dpi=240, facecolor="white", bbox_inches="tight", pad_inches=.22)
        if ext == "svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n",
                            encoding="utf-8", newline="\n")
    plt.close(fig)


def main() -> None:
    evidence = build()
    if json.loads(OUTPUT.read_text(encoding="utf-8")) != evidence:
        raise ValueError("Rebuild/review storytelling evidence before exporting figures.")
    FIGURES.mkdir(parents=True, exist_ok=True)
    modes = evidence["shipping_modes"]
    labels = [r["shipping_mode"] for r in modes]
    colors = [RED, AMBER, GRAY, TEAL]
    fig, (a, b) = canvas("Tỷ lệ trễ và đóng góp vào tổng số đơn trễ",
                         "DataCo: 62.897 đơn không hủy; 36.048 đơn trễ.")
    a.barh(labels, [r["late_rate"] * 100 for r in modes], color=colors, height=.62)
    a.invert_yaxis()
    a.set_xlim(0, 128)
    a.set_xticks([0, 25, 50, 75, 100])
    a.set_xlabel("Tỷ lệ trễ trong từng phương thức (%)")
    a.set_title("First Class có tỷ lệ trễ cao nhất", loc="left", fontsize=12, pad=16)
    for i, row in enumerate(modes):
        a.text(row["late_rate"] * 100 + 2, i, vi(row["late_rate"] * 100, 2) + "%", va="center", fontsize=10)
    b.barh(labels, [r["late_count"] for r in modes], color=colors, height=.62)
    b.invert_yaxis()
    b.set_xlim(0, 21300)
    b.set_xticks([0, 5000, 10000, 15000, 20000])
    b.xaxis.set_major_formatter(FuncFormatter(lambda x, _: vi(x)))
    b.set_xlabel("Số đơn trễ (tỷ trọng trong tổng số đơn trễ)")
    b.set_title("Standard Class có nhiều đơn trễ nhất", loc="left", fontsize=12, pad=16)
    for i, row in enumerate(modes):
        b.text(row["late_count"] + 350, i, f"{vi(row['late_count'])}\n({vi(row['share_of_all_late_orders'] * 100, 1)}%)", va="center", fontsize=9)
    save(fig, "story_01_priority")

    model = evidence["forecast"]
    fig, (a, b) = canvas("Cảnh báo: độ chính xác và mức bỏ sót",
                         "13.071 đơn test; baseline theo phương thức; ngưỡng P_Late ≥ 0,50.")
    groups = [
        (a, model["true_alerts"], model["false_alerts"], AMBER, "Cảnh báo đúng", "Cảnh báo sai",
         f"Precision: {vi(model['precision'] * 100, 2)}%", "4.560 đơn được cảnh báo"),
        (b, model["true_alerts"], model["missed_late"], RED, "Phát hiện được", "Bỏ sót",
         f"Recall: {vi(model['recall'] * 100, 2)}%", "7.524 đơn trễ thực tế"),
    ]
    for ax, yes, no, color, yes_label, no_label, title, denominator in groups:
        ax.barh([0], [yes], height=.5, color=TEAL, label=f"{yes_label}: {vi(yes)}")
        ax.barh([0], [no], left=[yes], height=.5, color=color, label=f"{no_label}: {vi(no)}")
        ax.set_xlim(0, 8000)
        ax.set_ylim(-.7, .7)
        ax.set_yticks([])
        ax.set_xticks([0, 2000, 4000, 6000, 8000])
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: vi(x)))
        ax.set_xlabel(denominator)
        ax.set_title(title, loc="left", pad=16)
        ax.legend(loc="upper left", frameon=False, fontsize=10)
    save(fig, "story_02_alerts")

    policy = evidence["bounded_promise"]
    fig, (a, b) = canvas("Cam kết dài hơn và tỷ lệ vượt hẹn",
                         "13.071 đơn test; kịch bản +1 ngày cho dịch vụ khác Same Day; giữ Same Day = 0 ngày.")
    rate_values = [policy["current_exceedance_rate"] * 100, policy["proposed_exceedance_rate"] * 100]
    a.bar(["Cam kết cũ", "Kịch bản +1 ngày"], rate_values, color=[RED, TEAL], width=.55)
    a.set_ylim(0, 75)
    a.set_ylabel("Tỷ lệ vượt hẹn tính lại (%)")
    a.set_title(f"Giảm {vi(policy['reduction_percentage_points'], 2)} điểm phần trăm", loc="left", fontsize=12, pad=16)
    for i, value in enumerate(rate_values):
        a.text(i, value + 2, vi(value, 2) + "%", ha="center", fontsize=12, weight="bold")
    import csv
    with (ROOT / "workstreams/prescriptive/results/promise_summary.csv").open(encoding="utf-8-sig", newline="") as stream:
        current = next(r for r in csv.DictReader(stream) if r["policy"] == "current" and r["partition"] == "test")
    old = float(current["mean_current_days"])
    day_values = [old, old + policy["added_mean_promise_days"]]
    b.bar(["Cam kết cũ", "Kịch bản +1 ngày"], day_values, color=[GRAY, TEAL], width=.55)
    b.set_ylim(0, 5.3)
    b.set_ylabel("Số ngày cam kết trung bình")
    b.set_title(f"Cam kết dài hơn trung bình {vi(policy['added_mean_promise_days'], 2)} ngày", loc="left", fontsize=12, pad=16)
    for i, value in enumerate(day_values):
        b.text(i, value + .13, vi(value, 2), ha="center", fontsize=12, weight="bold")
    fig.text(.565, .135, f"Thời gian thực tế giữ nguyên: {vi(policy['unchanged_mean_actual_days'], 2)} ngày.", fontsize=10, color=GRAY)
    save(fig, "story_03_promise_tradeoff")

    route = evidence["routing_c101"]
    fig, (a, b) = canvas("Tuyến C101: so sánh hai phương án khả thi",
                         "Solomon C101: 100 khách; sức chở Q = 200; giới hạn K = 25 xe.")
    labels = ["Nearest feasible\n(đối chứng)", "OR-Tools"]
    for ax, values, ylim, title, ylabel, digits in [
        (a, [route["nearest_vehicles"], route["ortools_vehicles"]], 27, "Số xe: 21 → 10", "Xe trong lời giải khả thi", 0),
        (b, [route["nearest_distance_units"], route["ortools_distance_units"]], 2400,
         f"Quãng đường giảm {vi(route['distance_reduction_pct'], 2)}%", "Quãng đường (đơn vị tọa độ benchmark)", 2),
    ]:
        ax.bar(labels, values, color=[GRAY, TEAL], width=.55)
        ax.set_ylim(0, ylim)
        ax.set_title(title, loc="left", fontsize=12, pad=16)
        ax.set_ylabel(ylabel)
        for i, value in enumerate(values):
            ax.text(i, value + ylim * .025, vi(value, digits), ha="center", fontsize=12, weight="bold")
    save(fig, "story_04_routing")
    paths = sorted(FIGURES.glob("story_0*.*"))
    manifest = {"evidence_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                "matplotlib_version": matplotlib.__version__,
                "outputs": {str(p.relative_to(ROOT)).replace("\\", "/"): {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
                            for p in paths}}
    (ROOT / "reports/storytelling/figure_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Exported {len(paths)} PNG/SVG figure files from verified evidence.")


if __name__ == "__main__":
    main()
