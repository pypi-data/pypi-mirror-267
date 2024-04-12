# TIQS API Client

Official Python client for [Tiqs Hummingbird API](https://docs.tiqs.in/documentation/).

## Installation

You can install the package using:
```
python3 -m pip install pytiqs
```

## API Usage

```python
import logging
import sys
from pytiqs import Tiqs, constants


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s')

tiqs = Tiqs(app_id="<APP_ID>")

# login and generate the request token from the URL obtained from tiqs.login_url()

tiqs.generate_session(request_token="<REQUEST_TOKEN>", api_secret="<API_SECRET>")

try:
    order_no = tiqs.place_order(
        exchange=constants.Exchange.NFO,
        token="46338",
        qty=15,
        disclosed_qty=0,
        product=constants.ProductType.NRML,
        symbol="BANKNIFTY2441048900CE",
        transaction_type=constants.TransactionType.BUY,
        order_type=constants.OrderType.MARKET,
        variety=constants.Variety.REGULAR,
        price=0,
        validity=constants.Retention.DAY,
        tags=None,
        amo=False,
        trigger_price=None
    )
    logging.info("order id: {}".format(order_no))
except Exception as e:
    logging.error("error in order placement: {}".format(e))
    
# all orders
tiqs.get_user_orders()

```

