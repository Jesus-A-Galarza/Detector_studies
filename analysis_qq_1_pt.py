import sys, os, glob, math
import ROOT
import logging

logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("fcclogger")
logger.setLevel(logging.INFO)

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

ROOT.EnableImplicitMT() # use all cores

# Load FCCAnalyses
ROOT.gSystem.Load("libFCCAnalyses")
fcc_loaded = ROOT.dummyLoader()
ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")
ROOT.gInterpreter.Declare('#include "functions.h"')

ROOT.gInterpreter.Declare("""
#include <vector>
#include <cmath>
#include "ROOT/RVec.hxx"

ROOT::VecOps::RVec<float> get_inv_pt(ROOT::VecOps::RVec<float> pt_vec) {
    ROOT::VecOps::RVec<float> inv_pt;
    for (auto pt : pt_vec) {
        if (pt > 0)
            inv_pt.push_back(1.0f / pt);
        else
            inv_pt.push_back(0.0f);
    }
    return inv_pt;
}

ROOT::VecOps::RVec<float> inv_pt_res(ROOT::VecOps::RVec<float> reco, ROOT::VecOps::RVec<float> gen) {
    ROOT::VecOps::RVec<float> res;
    for (size_t i = 0; i < std::min(reco.size(), gen.size()); ++i) {
        res.push_back(reco[i] - gen[i]);
    }
    return res;
}
""")

bins_p = (125, 0, 125)
bins_res = (10000, -0.1, 0.1)

def analysis(input_files, output_file):
    df = ROOT.RDataFrame("events", input_files)

    df = df.Alias("MCRecoAssociations0", "_MCRecoAssociations_rec.index")
    df = df.Alias("MCRecoAssociations1", "_MCRecoAssociations_sim.index")

    # select charged reco/gen particles
    df = df.Define("reco_q", "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
    df = df.Define("gen_q", "FCCAnalyses::MCParticle::get_charge(Particle)")
    df = df.Define("reco_q_sel", "reco_q != 0")
    df = df.Define("gen_q_sel", "gen_q != 0")
    df = df.Define("reco_charged", "ReconstructedParticles[reco_q_sel]")
    df = df.Define("gen_charged", "Particle[gen_q_sel]")
    df = df.Define("reco_charged_p", "FCCAnalyses::ReconstructedParticle::get_p(reco_charged)")
    df = df.Define("reco_charged_n", "FCCAnalyses::ReconstructedParticle::get_n(reco_charged)")
    df = df.Define("gen_charged_p", "FCCAnalyses::MCParticle::get_p(gen_charged)")
    df = df.Define("gen_charged_n", "FCCAnalyses::MCParticle::get_n(gen_charged)")

    # hadronic resolution = sum of energy of all particles
    df = df.Define("reco_e", "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df = df.Define("reco_e_tot", "Sum(reco_e)")
    df = df.Define("mc_final", "FCCAnalyses::MCParticle::sel_genStatus(1)(Particle)")
    df = df.Define("mc_e", "FCCAnalyses::MCParticle::get_e(mc_final)")
    df = df.Define("mc_e_tot", "Sum(mc_e)")
    df = df.Define("qq_res", "1.0/reco_e_tot - 1.0/mc_e_tot")

    # 1/pT of reco and gen charged particles
    df = df.Define("reco_charged_pt", "FCCAnalyses::ReconstructedParticle::get_pt(reco_charged)")
    df = df.Define("gen_charged_pt", "FCCAnalyses::MCParticle::get_pt(gen_charged)")

    df = df.Define("reco_charged_inv_pt", "get_inv_pt(reco_charged_pt)")
    df = df.Define("gen_charged_inv_pt", "get_inv_pt(gen_charged_pt)")

    # resolution 
    df = df.Define("inv_pt_resolution", "inv_pt_res(reco_charged_inv_pt, gen_charged_inv_pt)")

    inv_pt_hist = df.Histo1D(("inv_pt", "1/pT of reco charged particles", 500, 0.02, 0.06), "reco_charged_inv_pt")
    inv_pt_res_hist = df.Histo1D(("inv_pt_res", "1/pT resolution (reco - gen)", 1000, -0.01, 0.01), "inv_pt_resolution")
    qq_res = df.Histo1D(("qq_res", "", *bins_res), "qq_res")
    reco_e_tot = df.Histo1D(("reco_e_tot", "", *bins_p), "reco_e_tot")

    # Save output
    fout = ROOT.TFile(output_file, "RECREATE")
    inv_pt_hist.Write()
    inv_pt_res_hist.Write()
    qq_res.Write()
    reco_e_tot.Write()
    fout.Close()


if __name__ == "__main__":
    input_files, output_file = ["samples/IDEA_2.5T_Zuu_ecm91p2.root"], "output/IDEA_2.5T_Zuu_ecm91p2_1_pt.root"
    logger.info("Start analysis")
    analysis(input_files, output_file)
    logger.info(f"Done! Output saved to {output_file}")
