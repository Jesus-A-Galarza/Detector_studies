import sys, os, glob, math
import ROOT
import logging

logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("fcclogger")
logger.setLevel(logging.INFO)

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

ROOT.EnableImplicitMT()

ROOT.gSystem.Load("libFCCAnalyses")
fcc_loaded = ROOT.dummyLoader()
ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")
ROOT.gInterpreter.Declare('#include "functions.h"')

# Declare inverse momentum resolution function
ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<float> leptonResolutionInvP(
    const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& reco_muons,
    const ROOT::VecOps::RVec<int>& reco_match_idx,
    const ROOT::VecOps::RVec<int>& mc_match_idx,
    const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& allReco,
    const ROOT::VecOps::RVec<edm4hep::MCParticleData>& allMC,
    int pdg
) {
    ROOT::VecOps::RVec<float> resolution;
    std::map<int, int> match_map;
    for (size_t i = 0; i < reco_match_idx.size(); ++i) {
        match_map[reco_match_idx[i]] = mc_match_idx[i];
    }

    for (const auto& reco : reco_muons) {
        int reco_idx = -1;
        for (size_t i = 0; i < allReco.size(); ++i) {
            if (
                allReco[i].momentum.x == reco.momentum.x &&
                allReco[i].momentum.y == reco.momentum.y &&
                allReco[i].momentum.z == reco.momentum.z
            ) {
                reco_idx = i;
                break;
            }
        }

        if (reco_idx < 0 || match_map.find(reco_idx) == match_map.end()) {
            resolution.push_back(-998.);
            continue;
        }

        int mc_idx = match_map[reco_idx];
        if (mc_idx < 0 || mc_idx >= (int)allMC.size()) {
            resolution.push_back(-998.);
            continue;
        }

        const auto& mc = allMC[mc_idx];
        float reco_p = std::sqrt(reco.momentum.x * reco.momentum.x + reco.momentum.y * reco.momentum.y + reco.momentum.z * reco.momentum.z);
        float mc_p   = std::sqrt(mc.momentum.x * mc.momentum.x + mc.momentum.y * mc.momentum.y + mc.momentum.z * mc.momentum.z);

        if (mc_p < 1e-3 || reco_p < 1e-3) {
            resolution.push_back(-998.);
            continue;
        }

        resolution.push_back(1.0f / reco_p - 1.0f / mc_p);
    }

    return resolution;
}
""")

bins_p = (250, 0, 250)
bins_pt = (250, 0, 250)
bins_res = (10000, -0.05, 0.05)


def analysis(input_files, output_file):
    df = ROOT.RDataFrame("events", input_files)

    df = df.Alias("MCRecoAssociations0", "_MCRecoAssociations_rec.index")
    df = df.Alias("MCRecoAssociations1", "_MCRecoAssociations_sim.index")
    df = df.Alias("Muons", "Muon_objIdx.index")

    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muons, ReconstructedParticles)")

    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
    df = df.Define("muons_pt", "FCCAnalyses::ReconstructedParticle::get_pt(muons_all)")
    muons_p = df.Histo1D(("muons_p", "", *bins_p), "muons_p")
    muons_pt = df.Histo1D(("muons_pt", "", *bins_pt), "muons_pt")

    df = df.Define("muons_res_invp", "leptonResolutionInvP(muons_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, 0)")
    df = df.Filter("All(muons_res_invp > -998)", "Filter invalid invp resolutions")
    df = df.Filter("All(abs(muons_res_invp) < 0.1)", "Filter extreme invp resolution values")
    muons_res_invp = df.Histo1D(("muons_res_invp", "", 10000, -0.01, 0.01), "muons_res_invp")

    fout = ROOT.TFile(output_file, "RECREATE")
    muons_p.Write()
    muons_pt.Write()
    muons_res_invp.Write()
    fout.Close()


if __name__ == "__main__":
    input_files, output_file = ["samples/CLD_1T_Zmumu_ecm240.root"], "output/CLD_1T_Zmumu_ecm240_invp_res.root"
    logger.info(f"Start analysis")
    analysis(input_files, output_file)
    logger.info(f"Done! Output saved to {output_file}")
