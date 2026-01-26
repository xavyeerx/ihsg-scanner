# ============================================
# IHSG STOCKS LIST - FULL COMPREHENSIVE
# ============================================
# Format: Yahoo Finance ticker with .JK suffix

IHSG_STOCKS = [
    # === USER REQUESTED (PRIORITY) ===
    "BUMI.JK", "DEWA.JK", "ANTM.JK", "BBCA.JK", "BBRI.JK",
    "BMRI.JK", "BRMS.JK", "INET.JK", "PTRO.JK", "ADRO.JK",
    "RAJA.JK", "ARCI.JK", "SUPA.JK", "BUVA.JK", "BULL.JK",
    "GOTO.JK", "MINA.JK", "MBMA.JK", "ASII.JK", "TLKM.JK",
    "AMMN.JK", "MDKA.JK", "BRPT.JK", "INCO.JK", "DSSA.JK",
    "TINS.JK", "BKSL.JK", "BBNI.JK", "UNTR.JK", "WIFI.JK",
    "CDIA.JK", "NCKL.JK", "IMPC.JK", "ENRG.JK", "RATU.JK",
    "ADMR.JK", "PANI.JK", "CUAN.JK", "EMAS.JK", "INDY.JK",
    "GTSI.JK", "HRTA.JK", "BIPI.JK", "KIJA.JK", "RMKE.JK",
    "HUMI.JK", "MEDC.JK", "CBDK.JK", "NICL.JK", "COIN.JK",
    "OASA.JK", "EMTK.JK", "EXCL.JK", "BREN.JK", "JPFA.JK",
    "TOBA.JK", "PNLF.JK", "INKP.JK", "VKTR.JK", "PSAB.JK",
    "PADI.JK", "TCPI.JK", "AADI.JK", "PWON.JK", "PGAS.JK",
    "RLCO.JK", "BBYB.JK", "CPRO.JK", "HRUM.JK", "TRIN.JK",
    "UNVR.JK", "INDF.JK", "LEAD.JK", "TRUE.JK", "ITMA.JK",
    "PSKT.JK", "SMDR.JK", "KLBF.JK", "ICBP.JK", "SSIA.JK",
    "BBKP.JK", "PGEO.JK", "KETR.JK", "BRIS.JK", "SINI.JK",
    "AMRT.JK", "IRSX.JK", "LPKR.JK", "TPIA.JK", "PADA.JK",
    "NRCA.JK", "SCMA.JK", "COAL.JK", "ZATA.JK", "IATA.JK",
    "DKFT.JK", "BNBR.JK", "SOCI.JK", "ISAT.JK", "ELTY.JK",
    "REAL.JK", "PTBA.JK", "PBSA.JK", "PIPA.JK", "PPRE.JK",
    "KPIG.JK", "SMIL.JK", "CPIN.JK", "PJHB.JK", "ESSA.JK",
    "HMSP.JK", "BBTN.JK", "SRTG.JK", "TEBE.JK", "FILM.JK",
    "TOWR.JK", "DOOH.JK", "DATA.JK", "AKRA.JK", "CTRA.JK",
    "DSNG.JK", "SMGR.JK", "MBSS.JK", "MORA.JK", "MHKI.JK",
    "FUTR.JK", "INPC.JK", "ITMG.JK", "MAPI.JK", "GOLF.JK",
    "SGER.JK", "ASLI.JK", "ASHA.JK", "AHAP.JK", "CBRE.JK",
    "CYBR.JK", "JARR.JK", "MLPL.JK", "PTPP.JK", "SMRA.JK",
    "GGRM.JK", "BWPT.JK", "MYOR.JK", "MTEL.JK", "ELIT.JK",
    "JSMR.JK", "CMNT.JK", "ARKO.JK", "BUKA.JK", "VICI.JK",
    "TBIG.JK", "ELSA.JK", "FOLK.JK", "MEJA.JK", "WIRG.JK",
    "MAHA.JK", "BELL.JK", "MSIN.JK", "NETV.JK", "TAPG.JK",
    "INDO.JK", "ASRI.JK", "TOSK.JK", "KLAS.JK", "DAAZ.JK",
    "KEEN.JK", "NINE.JK", "PNBN.JK", "OPMS.JK", "BBRM.JK",
    "MARK.JK", "FIRE.JK", "UNIQ.JK", "AYAM.JK", "STRK.JK",
    "FAST.JK", "PACK.JK", "BMTR.JK", "TMAS.JK", "BACA.JK",
    "ERAA.JK", "BSDE.JK", "COCO.JK", "DMAS.JK", "TRON.JK",
    "SLIS.JK", "PYFA.JK", "TKIM.JK", "KDTN.JK", "ARTO.JK",
    "SOLA.JK", "KRAS.JK", "SGRO.JK", "MAPA.JK", "APEX.JK",
    "NSSS.JK", "DSFI.JK", "KOCI.JK", "BSBK.JK", "GIAA.JK",
    "GMFI.JK", "SMGA.JK", "INTP.JK", "UANG.JK", "HOPE.JK",
    "WIIM.JK", "SMKM.JK", "ASSA.JK", "IKAN.JK",

    "BGTG.JK", "BOAT.JK", "FPNI.JK", "HATM.JK", "JGLE.JK",
    "RMKO.JK", "HDIT.JK", "DEWI.JK", "KOKA.JK", "WOWS.JK",
    "ATLA.JK", "ACES.JK", "MNCN.JK", "MSKY.JK", "BEEF.JK",
    "IMJS.JK", "BFIN.JK", "UDNG.JK", "CMRY.JK", "ERAL.JK",
    "MMIX.JK", "JAST.JK"
]

def get_all_stocks():
    """Return list of all IHSG stocks (Unique)"""
    return sorted(list(set(IHSG_STOCKS)))

def get_stock_count():
    """Return total number of stocks"""
    return len(get_all_stocks())
