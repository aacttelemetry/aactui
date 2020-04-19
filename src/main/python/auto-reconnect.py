 async def listen_forever(self):
        while True:
        # outer loop restarted every time the connection fails
            try:
                async with websockets.connect(self.url) as ws:
                    while True:
                    # listener loop
                        try:
                            reply = await asyncio.wait_for(ws.recv(), timeout=***)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=self.ping_timeout)
                                logger.debug('Ping OK, keeping connection alive...')
                                continue
                            except:
                                await asyncio.sleep(self.sleep_time)
                                break  # inner loop
                        # do stuff with reply object
            except socket.gaierror:
                # log something
                continue
            except ConnectionRefusedError:
                # log something else
                continue