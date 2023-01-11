import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date


start_date = date.fromisoformat("2015-01-03")


ticker1 = yf.Ticker('AA   ACGL   ACHC   ACM   ADC   ADM   AEE   AEM   AEP   AER   AFL   AIG   AKAM   ALV   AMD   AMZN   AOS   APH   APO   APTV   ARES   AXS   AZN   AZTA   BAH   BALL   BBY   BC   BERY   BF-B   BG   BHP   BKI   BLDR   BMO   BMY   BNS   BPOP   BRKR   BRO   BWXT   BX   BXP   BYD   CAH   CALX   CBRE   CCEP   CCK   CF   CGNX   CHD   CHRW   CIEN   CIVI   CL   CMA   CMC   CMS   CNC   CNQ   COF   COUP   CP   CPB   CPRI   CPRT   CRUS   CSGP   CTSH   CVS   D   DAR   DD   DHI   DINO   DIS   DOX   DVA   DVN   ED   EHC   EIX   ELF   EMN   EMR   ENTG   ENV   EQR   ES   EW   EWBC   EXAS   EXPE   FAF   FBIN   FIS   FIVN   FMX   FND   FTV   FWONK   GDDY   GE   GGG   GILD   GIS   GMED   GOOG   GOOGL   GRMN   GWRE   HALO   HAS   HDB   HIG   HOLX   HQY   HSIC   HXL   IART   IBKR   INCY   IR   IRDM   ITCI   JBL   JCI   JD   K   KMX   KNX   L   LAMR   LBRDK   LEN   LITE   LKQ   LNT   LNW   LOGI   LPX   LSCC   LSI   LVS   LW   LYB   LYV   MAS   MAXR   MCHP   MDLZ   MDT   MET   MGA   MKC   MKSI   MMP   MS   MTDR   MTZ   MU   NDAQ   NEE   NEM   NTAP   NTES   NTR   NTRS   NVCR   NVS   O   OC   OKE   OKTA   OLLI   OLN   OMC   ON   ORCL   OXY   PCAR   PDCE   PEG   PFG   PFGC   PLNT   PNW   PRU   PVH   PYPL   QDEL   QRVO   QSR   RBA   RCL   REG   REXR   RHI   RIO   RPM   RTX   RY   SCCO   SCHW   SCI   SE   SEE   SEIC   SF   SHEL   SLB   SO   SONY   SPLK   SQ   SQM   SSNC   STT   STX   SWK   SWKS   SYY   TAP   TD   TECH   TER   THC   THO   TJX   TKR   TOL   TRGP   TRMB   TRU   TSM   TSN   TTE   TWLO   TXRH   TXT   VOYA   WAL   WEC   WELL   WIX   WMS   WOLF   WPC   WRB   WYNN   XEL   YUMC   ZION')

dataframe1 = ticker1.history(
    start=start_date, interval="1d", rounding=True, auto_adjust=True).Close
