import os
import logging
from plot_resolution import compute_res  # assumes compute_res is defined in plot_resolution.py

# Setup logger
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("plot_batch")
logger.setLevel(logging.INFO)

# Define the samples and corresponding analysis output files
samples = {
    "CLD_0.5T_Zmumu_ecm240": "output/CLD_0.5T_Zmumu_ecm240_p_pt.root",
    "CLD_1.0T_Zmumu_ecm240": "output/CLD_1.0T_Zmumu_ecm240_p_pt.root",
    "CLD_1.5T_Zmumu_ecm240": "output/CLD_1.5T_Zmumu_ecm240_p_pt.root",
    "CLD_2.0T_Zmumu_ecm240": "output/CLD_2.0T_Zmumu_ecm240_p_pt.root",
    "CLD_2.5T_Zmumu_ecm240": "output/CLD_2.5T_Zmumu_ecm240_p_pt.root",
    "CLD_3.0T_Zmumu_ecm240": "output/CLD_3.0T_Zmumu_ecm240_p_pt.root",
    "IDEA_0.5T_Zmumu_ecm240": "output/IDEA_0.5T_Zmumu_ecm240_p_pt.root",
    "IDEA_1.0T_Zmumu_ecm240": "output/IDEA_1.0T_Zmumu_ecm240_p_pt.root",
    "IDEA_1.5T_Zmumu_ecm240": "output/IDEA_1.5T_Zmumu_ecm240_p_pt.root",
    "IDEA_2.0T_Zmumu_ecm240": "output/IDEA_2.0T_Zmumu_ecm240_p_pt.root",
    "IDEA_2.5T_Zmumu_ecm240": "output/IDEA_2.5T_Zmumu_ecm240_p_pt.root",
    "IDEA_3.0T_Zmumu_ecm240": "output/IDEA_3.0T_Zmumu_ecm240_p_pt.root"
}

# Output directory for plots
plot_dir = "plots_pt"
os.makedirs(plot_dir, exist_ok=True)

def main():
    logger.info("📊 Starting resolution plots for all samples")

    for label, input_file in samples.items():
        logger.info(f"📈 Processing {label}")

        # Plot total momentum resolution
        hist_name_p = "muons_res_p"
        output_plot_p = os.path.join(plot_dir, f"resolution_{label}_p")
        logger.info(f"    ➤ Plotting total momentum resolution (p)")
        compute_res(input_file, hist_name_p, output_plot_p)

        # Plot transverse momentum resolution
        hist_name_pt = "muons_res_pt"
        output_plot_pt = os.path.join(plot_dir, f"resolution_{label}_pt")
        logger.info(f"    ➤ Plotting transverse momentum resolution (pt)")
        compute_res(input_file, hist_name_pt, output_plot_pt)

    logger.info("✅ All resolution plots generated.")

if __name__ == "__main__":
    main()
