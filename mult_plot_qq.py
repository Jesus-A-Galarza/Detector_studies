import os
import logging
from plot_resolution_qq import compute_res  # this assumes you have compute_res() defined in plot_resolution.py

# Setup logger
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("plot_batch")
logger.setLevel(logging.INFO)

# Define the samples and corresponding analysis output files
samples = {
    "resolution_CLD_1.0T_Zuu_ecm91p2": "output/CLD_1.0T_Zuu_ecm91p2.root",
    "resolution_CLD_2.0T_Zuu_ecm91p2": "output/CLD_2.0T_Zuu_ecm91p2.root",
    "resolution_CLD_3.0T_Zuu_ecm91p2": "output/CLD_3.0T_Zuu_ecm91p2.root",
    "resolution_IDEA_1.0T_Zuu_ecm91p2": "output/IDEA_1.0T_Zuu_ecm91p2.root",
    "resolution_IDEA_2.0T_Zuu_ecm91p2": "output/IDEA_2.0T_Zuu_ecm91p2.root",
    "resolution_IDEA_3.0T_Zuu_ecm91p2": "output/IDEA_3.0T_Zuu_ecm91p2.root"
}

# Output directory for plots
plot_dir = "plots_pt"
os.makedirs(plot_dir, exist_ok=True)

# Histogram name that compute_res expects
hist_name = "qq_res"

def main():
    logger.info("📊 Starting resolution plots for all samples")

    for label, input_file in samples.items():
        output_plot = f"{plot_dir}/resolution_{label}"
        logger.info(f"📈 Plotting resolution for {label}")
        compute_res(input_file, hist_name, output_plot)

    logger.info("✅ All resolution plots generated.")

if __name__ == "__main__":
    main()
