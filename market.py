import json
class Stock:
    def __init__(self, name):
        self.name = name
        self.own = 0
        self.sell = 0
        self.buy = 0

class MarkingPositionMonitor:
    def __init__(self):
        self.stock_dict = {}
        self.order_dict = {}

    def on_event(self, message):
        input = json.loads(message)
        if input["type"] == "NEW":
            target = input["symbol"]
            self.order_dict[input["order_id"]] = input
            if target not in self.stock_dict:
                self.stock_dict[target] = Stock(target)
            if input["side"] == "BUY":
                self.stock_dict[target].buy += int(input["quantity"])
            if input["side"] == "SELL":
                self.stock_dict[target].sell += int(input["quantity"])
            return self.stock_dict[target].own - self.stock_dict[target].sell

        if input["type"] == "ORDER_ACK":
            order_detail = self.order_dict[input["order_id"]]
            target = order_detail["symbol"]
            return self.stock_dict[target].own - self.stock_dict[target].sell

        if input["type"] == "ORDER_REJECT":
            order_detail = self.order_dict[input["order_id"]]
            target = order_detail["symbol"]
            if order_detail["type"] == "NEW":
                if order_detail["side"] == "BUY":
                    self.stock_dict[target].buy -= int(order_detail["quantity"])
                if order_detail["side"] == "SELL":
                    self.stock_dict[target].sell -= int(order_detail["quantity"])
            return self.stock_dict[target].own - self.stock_dict[target].sell

        if input["type"] == "CANCEL":
            order_id = input["order_id"]
            order_detail = self.order_dict[order_id]
            target = order_detail["symbol"]
            if order_detail["type"] == "NEW":
                return self.stock_dict[target].own - self.stock_dict[target].sell

        if input["type"] == "CANCEL_ACK":
            order_detail = self.order_dict[input["order_id"]]
            target = order_detail["symbol"]
            if order_detail["type"] == "NEW":
                if order_detail["side"] == "BUY":
                    self.stock_dict[target].buy -= int(order_detail["quantity"])
                if order_detail["side"] == "SELL":
                    self.stock_dict[target].sell -= int(order_detail["quantity"])
                return self.stock_dict[target].own - self.stock_dict[target].sell

        if input["type"] == "CANCEL_REJECT":
            order_detail = self.order_dict[input["order_id"]]
            target = order_detail["symbol"]
            if order_detail["type"] == "NEW":
                return self.stock_dict[target].own - self.stock_dict[target].sell

        if input["type"] == "FILL":
            order_detail = self.order_dict[input["order_id"]]
            target = order_detail["symbol"]
            if order_detail["type"] == "NEW":
                if "filled_quantity" not in order_detail:
                    order_detail["filled_quantity"] = 0
                if order_detail["side"] == "BUY":
                    self.stock_dict[target].own -= order_detail["filled_quantity"]
                    order_detail["filled_quantity"] = input["filled_quantity"]
                    self.stock_dict[target].own += order_detail["filled_quantity"]
                if order_detail["side"] == "SELL":
                    order_detail["filled_quantity"] = input["filled_quantity"]
                return self.stock_dict[target].own - self.stock_dict[target].sell
        return 0 

def assertEqual(a, b):
    if a != b:
        print("False! ", a, b)
    else:
        print(a)

if __name__ == '__main__':
    print("###### test 1 ########")
    M = MarkingPositionMonitor()
    str = json.dumps({"type": "NEW", "symbol": "IMIMP", "order_id": 1, "side": "SELL", "quantity": 800, "time": "2017-03-15T10:15:10.975187"})
    # print(M.on_event(str))  #800 1
    assertEqual(M.on_event(str), -800) # 1

    str = json.dumps({"type": "ORDER_REJECT", "order_id": 1, "reason": "SYMBOL_UNKNOWN", "time": "2017-03-15T10:15:10.975332"})
    # print(M.on_event(str)) #0 2
    assertEqual(M.on_event(str), 0) # 2

    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 2, "side": "BUY", "quantity": 2000, "time": "2017-03-15T10:15:10.975492"})
    # print(M.on_event(str)) #0 3
    assertEqual(M.on_event(str), 0) # 3

    str = json.dumps({"type": "ORDER_ACK", "order_id": 2, "time": "2017-03-15T10:15:10.975606"})
    # print(M.on_event(str)) #0 4
    assertEqual(M.on_event(str), 0)  # 4

    str = json.dumps({"type": "FILL", "order_id": 2, "filled_quantity": 2000, "remaining_quantity": 0, "time": "2017-03-15T10:15:10.975717"})
    #print(M.on_event(str)) #2000 5
    assertEqual(M.on_event(str), 2000)  # 5

    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 3, "side": "SELL", "quantity": 700, "time": "2017-03-15T10:15:10.975860"})
    #print(M.on_event(str)) #1300 6
    assertEqual(M.on_event(str), 1300)  # 6

    str = json.dumps({"type": "ORDER_ACK", "order_id": 3, "time": "2017-03-15T10:15:10.975966"})
    #print(M.on_event(str)) #1300  7
    assertEqual(M.on_event(str), 1300)  # 7

    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 4, "side": "SELL", "quantity": 1500, "time": "2017-03-15T10:15:10.976067"})
    #print(M.on_event(str)) #-200  8
    assertEqual(M.on_event(str), -200)  # 8

    str = json.dumps({"type": "ORDER_ACK", "order_id": 4, "time": "2017-03-15T10:15:10.976170"})
    #print(M.on_event(str)) #-200  9
    assertEqual(M.on_event(str), -200)  # 9

    str = json.dumps({"type": "CANCEL", "order_id": 3, "time": "2017-03-15T10:15:10.976431"})
    #print(M.on_event(str)) #-200  10
    assertEqual(M.on_event(str), -200)  # 10

    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 5, "side": "SELL", "quantity": 900, "time": "2017-03-15T10:15:10.976536"})
    #print(M.on_event(str)) #-1100  11
    assertEqual(M.on_event(str), -1100)  # 11

    str = json.dumps({"type": "CANCEL_ACK", "order_id": 3, "time": "2017-03-15T10:15:10.976653"})
    #print(M.on_event(str)) #-400 12
    assertEqual(M.on_event(str), -400)  # 12

    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 6, "side": "SELL", "quantity": 800, "time": "2017-03-15T10:15:10.976778"})
    #print(M.on_event(str)) #-1200 13
    assertEqual(M.on_event(str), -1200)  # 13

    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 7, "side": "BUY", "quantity": 1700, "time": "2017-03-15T10:15:10.976893"})
    #print(M.on_event(str)) #-1200 14
    assertEqual(M.on_event(str), -1200)  # 14

    str = json.dumps({"type": "ORDER_ACK", "order_id": 5, "time": "2017-03-15T10:15:10.977002"})
    #print(M.on_event(str)) #-1200 15
    assertEqual(M.on_event(str), -1200)  # 15

    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 8, "side": "SELL", "quantity": 1300, "time": "2017-03-15T10:15:10.977103"})
    #print(M.on_event(str)) #-2500 16
    assertEqual(M.on_event(str), -2500)  # 16

    str = json.dumps({"type": "ORDER_ACK", "order_id": 6, "time": "2017-03-15T10:15:10.977206"})
    #print(M.on_event(str)) #-2500 17
    assertEqual(M.on_event(str), -2500)  # 17

    str = json.dumps({"type": "CANCEL", "order_id": 7, "time": "2017-03-15T10:15:10.977295"})
    #print(M.on_event(str)) #-2500 18
    assertEqual(M.on_event(str), -2500)  # 18

    str = json.dumps({"type": "ORDER_REJECT", "order_id": 7, "reason": "FIRM_RISK_LIMIT_EXCEEDED", "time": "2017-03-15T10:15:10.977395"})
    #print(M.on_event(str)) #-2500 19
    assertEqual(M.on_event(str), -2500)  # 19

    str = json.dumps({"type": "CANCEL", "order_id": 6, "time": "2017-03-15T10:15:10.977515"})
    #print(M.on_event(str)) #-2500 20
    assertEqual(M.on_event(str), -2500)  # 20

    str = json.dumps({"type": "ORDER_REJECT", "order_id": 8, "reason": "FIRM_RISK_LIMIT_EXCEEDED", "time": "2017-03-15T10:15:10.977665"})
    #print(M.on_event(str)) #-1200 21
    assertEqual(M.on_event(str), -1200)  # 21

    # my additional cases
    str = json.dumps({"type": "NEW", "symbol": "SPY", "order_id": 9, "side": "BUY", "quantity": 1000, "time": "2017-03-15T11:15:10.977103"})
    assertEqual(M.on_event(str), -1200)  # 22

    str = json.dumps({"type": "ORDER_ACK", "order_id": 9, "time": "2017-03-15T11:15:10.977206"})
    assertEqual(M.on_event(str), -1200)  # 23

    str = json.dumps({"type": "FILL", "order_id": 9, "filled_quantity": 200, "remaining_quantity": 700,
                      "time": "2017-03-15T11:15:10.975717"})
    assertEqual(M.on_event(str), -1000)  # 24

    str = json.dumps({"type": "FILL", "order_id": 9, "filled_quantity": 1000, "remaining_quantity": 0,
                      "time": "2017-03-15T11:15:10.975717"})
    assertEqual(M.on_event(str), -200)  # 25
    M2 = MarkingPositionMonitor()
