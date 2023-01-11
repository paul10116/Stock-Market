import yfinance as yf
from datetime import date
import pandas as pd
from plotly import tools
import plotly.graph_objs as go
import sys

start_date = date.fromisoformat("2015-01-03")


def pair(longs, shorts):

    longArray = longs.split()
    shortArray = shorts.split()

    for buy_ticker in longArray:

        ticker1 = yf.Ticker(buy_ticker)

        for sell_ticker in shortArray:
            ticker2 = yf.Ticker(sell_ticker)

            if buy_ticker != sell_ticker:
                dataframe1 = ticker1.history(
                    start=start_date, interval="1d", rounding=True, auto_adjust=True).Close
                dataframe2 = ticker2.history(
                    start=start_date, interval="1d", rounding=True, auto_adjust=True).Close

                corr_matrix = pd.concat(
                    [dataframe1, dataframe2], axis=1).corr().round(2)
                corr_check = corr_matrix.iloc[0, 1]
                print(f"{buy_ticker}/{sell_ticker} corr={corr_check}")

                if corr_check > 0.4 or corr_check < -0.4:
                    data = pd.DataFrame({
                        'ratio': (dataframe1/dataframe2).round(3),
                        'spread': (dataframe1-dataframe2).round(2)
                    })

                    if data.ratio[-1] > 0.4 and data.ratio[-1] < 2:
                        data['ratioMA200'] = data['ratio'].rolling(
                            200).mean().round(3)
                        data['spreadMA200'] = data['spread'].rolling(
                            200).mean().round(2)

                        if data.ratio[-1] > data.ratioMA200[-1] and data.spread[-1] > data.spreadMA200[-1]:

                            data["spreadMA60"] = data.spread.rolling(
                                60).mean().round(2)
                            data["spreadMA20"] = data.spread.rolling(
                                20).mean().round(2)

                            if data.spreadMA60[-1] > data.spread[-1] and data.spreadMA20[-1] < data.spread[-1]:

                                sub_trace1 = go.Scatter(
                                    y=dataframe1, mode='lines', name=buy_ticker)
                                sub_trace2 = go.Scatter(
                                    y=dataframe2, mode='lines', name=sell_ticker)
                                sub_trace3 = go.Scatter(
                                    y=data.ratio, mode='lines', name='Ratio')
                                sub_trace4 = go.Scatter(
                                    y=data.ratioMA200, mode='lines', name='Ratio MA 200')
                                sub_trace5 = go.Scatter(
                                    y=data.spread, mode='lines', name='Spread')
                                sub_trace6 = go.Scatter(
                                    y=data.spreadMA200, mode='lines', name='Spread MA 200')
                                sub_trace7 = go.Scatter(
                                    y=data.spreadMA60, mode='lines', name='Spread MA 60')
                                sub_trace8 = go.Scatter(
                                    y=data.spreadMA20, mode='lines', name='Spread MA 20')

                                sub_fig = tools.make_subplots(rows=2, cols=2, subplot_titles=[
                                    buy_ticker, 'Ratio', sell_ticker, "Spread"], shared_xaxes=True, x_title=f"Correlation: {corr_check}")
                                sub_fig.append_trace(sub_trace1, 1, 1)
                                sub_fig.append_trace(sub_trace2, 2, 1)
                                sub_fig.append_trace(sub_trace3, 1, 2)
                                sub_fig.append_trace(sub_trace4, 1, 2)
                                sub_fig.append_trace(sub_trace5, 2, 2)
                                sub_fig.append_trace(sub_trace6, 2, 2)
                                sub_fig.append_trace(sub_trace7, 2, 2)
                                sub_fig.append_trace(sub_trace8, 2, 2)

                                sub_fig.show()


pair("VTRS   VZ   W   WBA   WBD   WDC   WES   WFC   WMB   WTRG   WU   WWW   WY   X   XPRO   XRAY   XRX   YELP   Z   ZG   ZWS",
     "ABR   ACAD   ACIW   ACRE   ADEA   ADTN   AEO   AES   AGNC   ALSN   AM   AMH   AMKR   APA   APAM   APLE   APPS   AR   ARCC   ARI   ARLP   ARMK   ARWR   ASB   ATEC   ATEN   ATI   AVNT   AVT   BAC   BBWI   BCRX   BEN   BGS   BHVN   BK   BKR   BKU   BPMC   BSX   BTU   BWA   BXMT   C   CAG   CARG   CDMO   CDNA   CFG   CG   CGNX   CHGG   CLF   CMCSA   CNP   CNX   COOP   CORT   CPE   CPRX   CRK   CSCO   CSX   CTLT   CTRA   CUZ   CVBF   CVI   CXW   CYTK   CZR   DAL   DAN   DEI   DELL   DENN   DISH   DK   DNLI   DNOW   DVAX   EBAY   EFC   ENLC   EPD   EQT   ESTE   ET   EVH   EVRI   EXAS   EXC   EXEL   EXTR   F   FAST   FBP   FCX   FE   FGEN   FHI   FITB   FNB   FNF   FOLD   FORM   FTAI   FTNT   FULT   GDOT   GEL   GEN   GEO   GLW   GM   GNTX   GOGO   GPS   GT   GTN   HA   HAIN   HAL   HBAN   HIW   HLF   HLIT   HPE   HPQ   HR   HRL   HST   HTGC   HWM   IAC   INSM   INTC   INVA   INVH   IONS   IP   IPG   IRWD   ISEE   IVZ   JNPR   JWN   KAR   KDP   KEY   KHC   KIM   KKR   KMI   KR   KRC   KRG   KSS   KTOS   KURA   KW   LEG   LPSN   LSXMA   LSXMK   LUV   LXP   LXU   M   MAC   MAT   MDC   MDRX   MDU   MFA   MGM   MGNI   MLKN   MO   MODG   MOS   MPLX   MPW   MRC   MRO   MRTX   MRVL   MTCH   MTG   MUR   MWA   MXL   MYGN   NCR   NEOG   NI   NLY   NOV   NTLA   NTRA   NUVA   NVAX   NWL   NXGN   NYT   OI   OII   OMI   ONB   OPCH   PAA   PARA   PARR   PCG   PEAK   PEB   PENN   PHM   PLAB   PLUG   PMT   PPL   PRMW   PTCT   PTEN   RAMP   RARE   RCKT   RCM   RDN   RF   RLJ   ROIC   ROL   RPD   RVNC   SBH   SBRA   SFM   SFNC   SGRY   SITC   SKT   SLCA   SLM   SM   SMPL   SMTC   SNDX   SPWR   SSRM   SSYS   STAG   STWD   SYF   SYNH   T   TDOC   TDS   TFC   TGNA   TGTX   TNDM   TPX   TREX   TRIP   TROX   TTD   TTMI   TVTX   TWNK   TWO   UAA   UAL   UDR   UE   UMPQ   UNFI   UNM   USB   USFD   VCYT   VFC   VGR   VIAV   VICI   VLY   VRE   VRNS   VTR   VTRS   VZ   W   WBA   WBD   WDC   WES   WFC   WMB   WTRG   WU   WWW   WY   X   XPRO   XRAY   XRX   YELP   Z   ZG   ZWS")

data_10_50 = "ABR   ACAD   ACIW   ACRE   ADEA   ADTN   AEO   AES   AGNC   ALSN   AM   AMH   AMKR   APA   APAM   APLE   APPS   AR   ARCC   ARI   ARLP   ARMK   ARWR   ASB   ATEC   ATEN   ATI   AVNT   AVT   BAC   BBWI   BCRX   BEN   BGS   BHVN   BK   BKR   BKU   BPMC   BSX   BTU   BWA   BXMT   C   CAG   CARG   CDMO   CDNA   CFG   CG   CGNX   CHGG   CLF   CMCSA   CNP   CNX   COOP   CORT   CPE   CPRX   CRK   CSCO   CSX   CTLT   CTRA   CUZ   CVBF   CVI   CXW   CYTK   CZR   DAL   DAN   DEI   DELL   DENN   DISH   DK   DNLI   DNOW   DVAX   EBAY   EFC   ENLC   EPD   EQT   ESTE   ET   EVH   EVRI   EXAS   EXC   EXEL   EXTR   F   FAST   FBP   FCX   FE   FGEN   FHI   FITB   FNB   FNF   FOLD   FORM   FTAI   FTNT   FULT   GDOT   GEL   GEN   GEO   GLW   GM   GNTX   GOGO   GPS   GT   GTN   HA   HAIN   HAL   HBAN   HIW   HLF   HLIT   HPE   HPQ   HR   HRL   HST   HTGC   HWM   IAC   INSM   INTC   INVA   INVH   IONS   IP   IPG   IRWD   ISEE   IVZ   JNPR   JWN   KAR   KDP   KEY   KHC   KIM   KKR   KMI   KR   KRC   KRG   KSS   KTOS   KURA   KW   LEG   LPSN   LSXMA   LSXMK   LUV   LXP   LXU   M   MAC   MAT   MDC   MDRX   MDU   MFA   MGM   MGNI   MLKN   MO   MODG   MOS   MPLX   MPW   MRC   MRO   MRTX   MRVL   MTCH   MTG   MUR   MWA   MXL   MYGN   NCR   NEOG   NI   NLY   NOV   NTLA   NTRA   NUVA   NVAX   NWL   NXGN   NYT   OI   OII   OMI   ONB   OPCH   PAA   PARA   PARR   PCG   PEAK   PEB   PENN   PHM   PLAB   PLUG   PMT   PPL   PRMW   PTCT   PTEN   RAMP   RARE   RCKT   RCM   RDN   RF   RLJ   ROIC   ROL   RPD   RVNC   SBH   SBRA   SFM   SFNC   SGRY   SITC   SKT   SLCA   SLM   SM   SMPL   SMTC   SNDX   SPWR   SSRM   SSYS   STAG   STWD   SYF   SYNH   T   TDOC   TDS   TFC   TGNA   TGTX   TNDM   TPX   TREX   TRIP   TROX   TTD   TTMI   TVTX   TWNK   TWO   UAA   UAL   UDR   UE   UMPQ   UNFI   UNM   USB   USFD   VCYT   VFC   VGR   VIAV   VICI   VLY   VRE   VRNS   VTR   VTRS   VZ   W   WBA   WBD   WDC   WES   WFC   WMB   WTRG   WU   WWW   WY   X   XPRO   XRAY   XRX   YELP   Z   ZG   ZWS"
