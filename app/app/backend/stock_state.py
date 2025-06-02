import reflex as rx
import asyncio
import os
OUTPUT_LEN = 7

class StockInfor(rx.State):
    ticker: str = ""
    predict_result: dict = {}
    crawl_result: dict = {}
    is_loading: bool = False
    
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
    
    @rx.event(background=True)
    async def handle_submit(self):
        import httpx 

        async with self:
            self.is_loading = True
        
        try:
            # Update state within context manager
            async with self:
                # Make the HTTP requests
                async with httpx.AsyncClient() as client:
                    api_url = os.getenv("API_URL", "http://0.0.0.0:8000")
                    crawl_response = await client.get(f"{api_url}/crawl/{self.ticker}")
                    await asyncio.sleep(2)
                    predict_response = await client.post(f"{api_url}/predict/{self.ticker}")
                if predict_response.status_code == 200:
                    self.predict_result = predict_response.json()
                if crawl_response.status_code == 200:
                    self.crawl_result = crawl_response.json()

        except Exception as e:
            print(f"Error in handle_submit: {str(e)}")
        finally:
            # Ensure loading state is always reset
            async with self:
                self.is_loading = False


