from fastapi import FastAPI
from modules.sentiment_analysis.sentiment_analysis import router as sentiment_analysis_router
from modules.trend_detector.trend_detector import router as trend_detector_router
from modules.data_toolkit.nse.nse_indices import router as nse_indices_router
from modules.data_toolkit.nse.nse_equities import router as nse_eq_router
from modules.data_toolkit.screener.screener_equities import router as screener_eq_router

app = FastAPI()

app.include_router(sentiment_analysis_router)
app.include_router(trend_detector_router)
app.include_router(nse_indices_router)
app.include_router(nse_eq_router)
app.include_router(screener_eq_router)