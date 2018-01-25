import tornado.ioloop
import tornado.web
import tornado.httpserver
import os

import MovingAverageCrossoverTrader as mva


class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	self.render("template.html", mva_days="", cash="", text="", btc_checked="", eth_checked="")

    def post(self):
        mva_days_input = int(self.get_argument('mva_days'))
        cash_input = int(self.get_argument('cash'))
        currency = self.get_argument('currency')
        btc_checked = ""
        eth_checked = ""
        filename = ""
        if (currency == "BTC"):
            btc_checked = "checked"
            eth_checked = ""
            filename = "prices/5-minute/bitcoin.txt"
        elif (currency == "ETH"):
            filename = "prices/5-minute/ethereum.txt"
            eth_checked = "checked"
            btc_checked = ""
        trader = mva.MovingAverageCrossoverTrader(currency, mva_days_input, True, cash_input, filename)
        trader.trade()
        results = trader.results()
        self.render("template.html", mva_days=mva_days_input, cash=cash_input, text=results, btc_checked=btc_checked, eth_checked=eth_checked)

class Server(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            # Add more paths here
        ]
        settings = {
        "debug": True,
        "template_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        "static_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    application = Server()
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    #app = make_app()
    #app.listen(8888)
    #tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
	main()