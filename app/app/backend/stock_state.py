import reflex as rx
OUTPUT_LEN = 7

class StockInfor(rx.State):
    ticker: str = ""
    predict_result: dict = {}
    crawl_result: dict = {}
    
    @rx.var
    def line_data(self) -> list[dict]:
        """Get the line chart data from the prediction result.
        
        Returns:
            list[dict]: List of data points for the line chart
        """
        if not self.predict_result or not isinstance(self.predict_result, dict):
            return []
            
        prices = self.predict_result.get("predicted_price", [])
        timestamps = self.predict_result.get("timestamp", [])
            
        return [
            {
                "predicted_price": prices[i],
                "timestamp": timestamps[i] # Ensure timestamp is string
            }
            for i in range(OUTPUT_LEN)
        ]
    

    @rx.var
    def table_data(self) -> list[list]:
        if not self.crawl_result or not isinstance(self.crawl_result, dict):
            return []
            
        raw_data = self.crawl_result.get("raw_data", [])
        date = raw_data["Date"]
        close = raw_data["Close"]
        open = raw_data["Open"]
        high = raw_data["High"]
        low = raw_data["Low"]
        volume = raw_data["Volume"]

        return [[date[-i], round(close[-i],2), round(open[-i],2), round(high[-i],2), round(low[-i],2), volume[-i]] for i in range(1, OUTPUT_LEN+1)]
            
        
    def set_ticker(self, value: str):
        self.ticker = value.upper()  # Convert to uppercase for consistency

    async def handle_submit(self):
        import httpx 
        async with httpx.AsyncClient() as client:
            # predict_response = await client.post(f"http://backend:8000/predict/{self.ticker}")
            # crawl_response = await client.get(f"http://backend:8000/crawl/{self.ticker}")
            predict_response = await client.post(f"http://localhost:8000/predict/{self.ticker}")
            crawl_response = await client.get(f"http://localhost:8000/crawl/{self.ticker}")
            if predict_response.status_code == 200:
                self.predict_result = predict_response.json()
            if crawl_response.status_code == 200:
                self.crawl_result = crawl_response.json()


