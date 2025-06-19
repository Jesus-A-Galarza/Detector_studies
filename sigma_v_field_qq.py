import ROOT
import os
import logging
import matplotlib.pyplot as plt

# Create output folder
os.makedirs("plots", exist_ok=True)

# Setup logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("sigma_plot")
logger.setLevel(logging.INFO)

# Sample structure: (filename base, B field, detector label)
samples = [
    ("CLD_1.0T_Zuu_ecm91p2_qq", 1.0, "CLD"),
    ("CLD_2.0T_Zuu_ecm91p2_qq", 2.0, "CLD"),
    ("CLD_3.0T_Zuu_ecm91p2", 3.0, "CLD"),
    ("IDEA_1.0T_Zuu_ecm91p2", 1.0, "IDEA"),
    ("IDEA_1.5T_Zuu_ecm91p2", 1.5, "IDEA"),
    ("IDEA_2.0T_Zuu_ecm91p2", 2.0, "IDEA"),
    ("IDEA_2.5T_Zuu_ecm91p2", 2.5, "IDEA"),
    ("IDEA_3.0T_Zuu_ecm91p2", 3.0, "IDEA")
]

input_dir = "output"

# Separate data by detector
fields_CLD, sigmas_CLD = [], []
fields_IDEA, sigmas_IDEA = [], []

for name, B, label in samples:
    file_path = f"{input_dir}/{name}.root"
    f = ROOT.TFile(file_path)

    h_p = f.Get("qq_res")
    if h_p:
        fit_p = h_p.Fit("gaus", "SQRN")
        if fit_p.Status() == 0:
            sigma_p = fit_p.Parameter(2)
            if label == "CLD":
                fields_CLD.append(B)
                sigmas_CLD.append(sigma_p)
            else:
                fields_IDEA.append(B)
                sigmas_IDEA.append(sigma_p)
        else:
            logger.warning(f"Fit failed for p in {name}")
    else:
        logger.warning(f"qq_res not found in {file_path}")

# --- Plot ---
plt.figure(figsize=(7, 5))

# Sorted for connected line plot
fields_CLD, sigmas_CLD = zip(*sorted(zip(fields_CLD, sigmas_CLD)))
fields_IDEA, sigmas_IDEA = zip(*sorted(zip(fields_IDEA, sigmas_IDEA)))

plt.plot(fields_CLD, sigmas_CLD, 'o-', label="CLD")
plt.plot(fields_IDEA, sigmas_IDEA, 's-', label="IDEA")

plt.xlabel("Magnetic Field (T)")
plt.ylabel("Momentum Resolution σ (Gaus width)")
plt.title("Muon Momentum Resolution vs Magnetic Field")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig("plots/sigma_vs_field_qq.png")
plt.savefig("plots/sigma_vs_field_qq.pdf")
plt.show()
