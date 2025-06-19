import os
import logging
from analysis_resolution import analysis  # This assumes your script is named analysis_resolution.py

# Setup logger
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("batch_runner")
logger.setLevel(logging.INFO)

# Define your samples
samples = {
    "CLD_1.0T_Zmumu_ecm240": "samples/CLD_1.0T_Zmumu_ecm240.root",
    "CLD_3.0T_Zmumu_ecm240": "samples/CLD_3.0T_Zmumu_ecm240.root",
    "CLD_2.0T_Zmumu_ecm240": "samples/CLD_2.0T_Zmumu_ecm240.root",
    "IDEA_1.0T_Zmumu_ecm240": "samples/IDEA_1.0T_Zmumu_ecm240.root",
    "IDEA_2.0T_Zmumu_ecm240": "samples/IDEA_2.0T_Zmumu_ecm240.root",
    "IDEA_3.0T_Zmumu_ecm240": "samples/IDEA_3.0T_Zmumu_ecm240.root"

}

# Output folder
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def main():
    logger.info("🔁 Starting analysis for all detector configurations...")

    for label, input_path in samples.items():
        output_file = f"{output_dir}/{label}_p_pt.root"
        logger.info(f"🚀 Running analysis on {label}")
        analysis([input_path], output_file)
        logger.info(f"✅ Saved to {output_file}")

    logger.info("🎉 All samples processed.")

if __name__ == "__main__":
    main()
