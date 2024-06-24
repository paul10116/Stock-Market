sectorsTickers = 'SPY XLF XLV XLP XLC XLE XLY XLRE XLK XLU XLB XLI'

over_2_B = ''' A   AA   AAL   AAON   AAP   AAPL   ABBV   ABM   ABNB   ABR   ABT   ACAD   ACGL   ACHC   ACI   ACIW   ACM   ACN   ACVA   ADBE   ADC   ADI   ADM   ADMA   ADNT   ADP   ADSK   ADT   AEE   AEG   AEM   AEO   AEP
AER   AES   AESI   AFL   AFRM   AGCO   AGI   AGIO   AGL   AGNC   AGR   AI   AIG   AIRC   AJG   AKAM   AL   ALAB   ALB   ALC   ALGM   ALGN   ALIT   ALK   ALKS   ALL   ALLE   ALLY   ALNY   ALSN   ALTM   ALV
AM   AMAT   AMBP   AMCR   AMD   AME   AMGN   AMH   AMKR   AMRX   AMT   AMX   AMZN   ANET   ANF   AON   AOS   APA   APD   APG   APH   APLE   APLS   APO   APP   APTV   AQN   AR   ARCC   ARE   ARES   ARHS   ARM
ARMK   AROC   ARWR   AS   ASAN   ASB   ASML   ASO   ASPN   ASX   ATI   ATMU   ATO   AU   AVB   AVDX   AVGO   AVT   AVTR   AWK   AX   AXNX   AXON   AXP   AXS   AXTA   AY   AZEK   AZN   AZTA   BA   BABA   BAC
BAH   BALL   BAM   BAX   BBAR   BBIO   BBVA   BBWI   BBY   BC   BCS   BDX   BE   BEAM   BECN   BEKE   BEN   BEP   BEPC   BERY   BG   BGC   BHC   BHP   BHVN   BIDU   BIIB   BILI   BILL   BIPC   BJ   BK
BKR   BKU   BL   BLDR   BLK   BMO   BMRN   BMY   BN   BNL   BNS   BNTX   BOX   BP   BPMC   BRBR   BRFS   BRKR   BRO   BROS   BRX   BRZE   BSBR   BSX   BSY   BTE   BTI   BTU   BUD   BUR   BURL   BVN
BWA   BWXT   BX   BXMT   BXP   BXSL   BYD   BZ   C   CADE   CAE   CAG   CAH   CALX   CARG   CARR   CART   CAT   CAVA   CB   CBOE   CBRE   CC   CCCS   CCEP   CCI   CCJ   CCK   CCL   CDE   CDNS   CDP   CDW   CE
CEG   CELH   CERE   CERT   CF   CFG   CFLT   CG   CGNX   CHD   CHK   CHKP   CHRW   CHTR   CHWY   CHX   CI   CIEN   CINF   CIVI   CL   CLBT   CLDX   CLF   CLS   CLSK   CLVT   CLX   CM   CMA   CMC   CMCSA   CME
CMI   CMS   CNC   CNH   CNI   CNK   CNM   CNO   CNP   CNQ   CNX   COF   COHR   COIN   COLB   COLD   COO   COP   COR   CORT   COST   COTY   CP   CPB   CPNG   CPRI   CPRT   CPT   CRBG   CRC   CRDO   CRH   CRK
CRL   CRM   CRNX   CROX   CRSP   CRWD   CSCO   CSGP   CSTM   CSX   CTLT   CTRA   CTRE   CTSH   CTVA   CUBE   CUZ   CVBF   CVE   CVI   CVNA   CVS   CVX   CWAN   CWEN   CWK   CX   CXM   CYTK   CZR   DAL
DAR   DASH   DAY   DB   DBRG   DBX   DCI   DD   DDOG   DE   DEI   DELL   DEO   DFS   DG   DGX   DHI   DHR   DINO   DIS   DKNG   DKS   DLO   DLR   DLTR   DNB   DNLI   DOC   DOCN   DOCS   DOCU   DOV   DOW   DOX
DRI   DRS   DT   DTE   DTM   DUK   DV   DVA   DVN   DXC   DXCM   DYN   EA   EBAY   EBC   EC   ECL   ED   EDR   EDU   EFX   EGO   EHC   EIX   EL   ELAN   ELF   ELS   ELV   EMN   EMR   ENB   ENLC   ENOV   ENPH
ENR   ENTG   ENV   ENVX   EOG   EPAM   EPD   EPR   EPRT   EQC   EQH   EQIX   EQNR   EQR   EQT   ERIC   ERJ   ES   ESI   ESNT   ESTC   ET   ETN   ETR   ETRN   ETSY   EVH   EVRG   EW   EWBC   EXAS   EXC   EXEL
EXLS   EXPD   EXPE   EXR   F   FAF   FANG   FAST   FBIN   FBP   FCX   FDX   FE   FERG   FHB   FHI   FHN   FI   FIBK   FIS   FITB   FIVE   FIVN   FL   FLEX   FLNC   FLO   FLR   FLS   FLUT   FMC   FMX   FNB
FND   FNF   FNV   FOLD   FORM   FOUR   FOX   FOXA   FR   FROG   FRSH   FRT   FSK   FSLR   FTAI   FTDR   FTI   FTNT   FTRE   FTS   FTV   FULT   FUTU   FWONK   FYBR   G   GBCI   GBDC   GD   GDDY   GDRX   GE
GEHC   GEN   GERN   GEV   GFI   GFL   GFS   GGAL   GGB   GGG   GH   GIL   GILD   GIS   GL   GLBE   GLNG   GLPI   GLW   GM   GME   GMED   GNRC   GNTX   GNW   GO   GOGL   GOLD   GOOG   GOOGL   GPC   GPK   GPN
GPS   GRAB   GRMN   GS   GSK   GT   GTES   GTLB   GWRE   GXO   HAE   HAL   HALO   HAS   HASI   HAYW   HBAN   HBM   HCA   HCC   HCP   HD   HDB   HES   HESM   HGV   HIG   HIMS   HIW   HL   HLN   HLT   HMC   HMY
HOG   HOLX   HOMB   HON   HOOD   HP   HPE   HPQ   HQY   HR   HRB   HRL   HSBC   HSIC   HST   HSY   HTGC   HTHT   HUM   HUN   HWM   HXL   IAC   IART   IBKR   IBM   IBN   IBRX   ICE   ICL   ICLR   IDYA   IEP
IFF   IGT   ILMN   IMVT   INCY   INFA   INFY   ING   INSM   INTA   INTC   INTR   INTU   INVH   IONS   IOT   IOVA   IP   IPG   IQ   IQV   IR   IRDM   IRM   IRT   ISRG   ITCI   ITUB   ITW   IVZ   J   JAMF   JAZZ
JBHT   JBL   JCI   JD   JEF   JHG   JNJ   JNPR   JOBY   JPM   JWN   JXN   K   KBH   KBR   KD   KDP   KEY   KEYS   KGC   KHC   KIM   KKR   KLAC   KMB   KMI   KMX   KNX   KO   KOS   KR   KRC   KRG   KSS   KT
KTB   KTOS   KVUE   KVYO   KYMR   L   LAUR   LAZ   LBRDK   LBRT   LBTYA   LBTYK   LDOS   LEA   LEGN   LEN   LEVI   LFST   LH   LHX   LI   LIN   LITE   LIVN   LKQ   LLY   LMT   LNC   LNG   LNT   LNTH   LNW
LOAR   LOW   LPX   LRCX   LSCC   LSPD   LSXMA   LSXMK   LTH   LULU   LUV   LVS   LW   LXP   LYB   LYFT   LYV   M   MA   MAA   MAC   MAR   MARA   MAS   MAT   MBLY   MC   MCD   MCHP   MCK   MCO   MCW   MDB   MDLZ
MDT   MDU   MET   META   MFC   MFG   MGA   MGM   MGY   MHK   MIR   MKC   MKSI   MLCO   MLI   MMC   MMM   MMYT   MNSO   MNST   MO   MOD   MODG   MOS   MP   MPC   MPLX   MPW   MQ   MRK   MRNA   MRO   MRUS   MRVL
MS   MSCI   MSFT   MSI   MT   MTB   MTCH   MTDR   MTG   MTSI   MTZ   MU   MUFG   MUR   MWA   MYGN   NABL   NATL   NBIX   NCLH   NCNO   NDAQ   NE   NEE   NEM   NEOG   NEP   NET   NEXT   NFE   NFLX   NI   NICE
NIO   NKE   NLY   NMIH   NMR   NNN   NOC   NOG   NOK   NOMD   NOV   NOW   NRG   NSA   NSC   NTAP   NTES   NTLA   NTNX   NTR   NTRA   NTRS   NU   NUE   NVAX   NVCR   NVDA   NVEI   NVO   NVS   NVST   NVT   NWG
NWL   NWS   NWSA   NXE   NXPI   NXT   NYCB   NYT   O   OBDC   OC   ODFL   OGE   OGN   OHI   OII   OKE   OKTA   OLLI   OLN   OMC   OMF   ON   ONB   ONON   OPCH   OR   ORAN   ORCL   ORI   OSCR   OTEX   OTIS   OUT
OVV   OWL   OXY   OZK   PAA   PAAS   PAGP   PAGS   PANW   PARA   PATH   PAYC   PAYO   PAYX   PB   PBA   PBF   PBR   PCAR   PCG   PCOR   PCVX   PD   PDCO   PDD   PECO   PEG   PENN   PEP   PFE   PFG   PFGC   PG
PGNY   PGR   PH   PHG   PHM   PII   PINS   PK   PKG   PLD   PLNT   PLTK   PLTR   PM   PNC   PNM   PNR   PNW   PODD   POR   PPBI   PPG   PPL   PR   PRGO   PRIM   PRKS   PRMW   PRU   PRVA   PSA   PSEC   PSTG
PSX   PTC   PTCT   PTEN   PUK   PVH   PWR   PWSC   PYCR   PYPL   QCOM   QDEL   QFIN   QGEN   QRVO   QS   QSR   QTWO   RARE   RBA   RBLX   RCI   RCL   RCM   RDN   RDNT   REG   RELX   RELY   REXR   REYN   REZI
RF   RGEN   RHI   RIG   RIO   RIOT   RITM   RIVN   RJF   RKLB   RKT   RMBS   RMD   RNA   RNG   RNW   ROIV   ROK   ROKU   ROL   ROP   ROST   RPD   RPM   RPRX   RSG   RTO   RTX   RUN   RVMD   RVTY   RXO   RXRX
RY   RYAAY   RYAN   RYTM   S    SAN   SAP   SATS   SBAC   SBLK   SBRA   SBS   SBSW   SBUX   SCCO   SCHW   SCI   SDRL   SE   SEDG   SEE   SEIC   SEM   SF   SFM   SG   SGRY   SHC   SHEL   SHO   SHOO   SHOP   SHW
SITC   SIX   SJM   SKT   SKX   SLB   SLF   SLG   SLGN   SLM   SM   SMAR   SMCI   SMFG   SMMT   SMPL   SN   SNAP   SNDR   SNN   SNOW   SNPS   SNV   SNX   SNY   SO   SOFI   SOLV   SONY   SPG   SPGI   SPNT   SPOT
SPR   SQ   SQM   SQSP   SRCL   SRE   SRPT   SSL   SSNC   ST   STAG   STE   STLA   STLD   STM   STNE   STR   STT   STWD   STX   STZ   SU   SUI   SUM   SUN   SUZ   SWK   SWKS   SWN   SWTX   SYF   SYK   SYY   T
TAC   TAL   TAP   TCOM   TD   TDC   TDS   TEAM   TECH   TECK   TEF   TEL   TENB   TER   TEVA   TEX   TFC   TGNA   TGT   TGTX   THC   TJX   TKO   TME   TMHC   TMO   TMUS   TNDM   TNL   TOL   TOST   TPG   TPH
TPR   TPX   TREX   TRGP   TRIP   TRMB   TRMD   TRN   TRNO   TROW   TROX   TRP   TRU   TRV   TS   TSCO   TSLA   TSM   TSN   TT   TTC   TTD   TTE   TTWO   TU   TW   TWLO   TWST   TXG   TXN   TXRH   TXT   U   UA
UAA   UAL   UBER   UBS   UCBI   UDR   UE   UEC   UGI   UGP   UHS   UL   UMC   UNH   UNM   UNP   UPS   URBN   URI   USB   USFD   V   VAL   VALE   VECO   VEEV   VERX   VFC   VICI   VIK   VIPS   VIRT   VIST   VIV
VKTX   VLO   VLTO   VLY   VMC   VNO   VNOM   VNT   VOD   VOYA   VRN   VRNS   VRNT   VRRM   VRSK   VRSN   VRT   VRTX   VSH   VST   VTR   VTRS   VVV   VZ   VZIO   W   WAB   WAL   WBA   WBD   WBS   WCN   WDAY
WDC   WDS   WEC   WELL   WEN   WERN   WES   WFC   WFRD   WH   WHD   WHR   WIT   WIX   WM   WMB   WMG   WMT   WOLF   WPC   WPM   WRB   WRK   WSC   WSM   WTRG   WU   WY   WYNN   X   XEL   XOM   XP   XPEV   XPO
XPRO   XRAY   XYL   YELP   YETI   YMM   YPF   YUM   YUMC   Z   ZBH   ZETA   ZG   ZGN   ZI   ZIM   ZION   ZM   ZS   ZTO   ZTS   ZWS '''