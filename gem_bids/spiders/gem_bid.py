"""- Bid No: (also based on some condition) b_bid_number_parent - Ra No: (this could be bid or ra depending on a
condition) b_bid_number - Items: if (bidData.b_category_name[0].length > 30) { htmlDta += bidData.b_category_name[
0].substr(0, 30) } else { htmlDta += (bidData.bbt_title) ? bidData.b_category_name[0] + ' (' + bidData.bbt_title +
')' : bidData.b_category_name[0]; }

- Quantity: b_total_quantity
- Department: ba_official_details_deptName
- Start date (parsed datetime object): final_start_date_sort
- End date(parsed datetime object): final_end_date_sort
- Document checksum from bid document (instead just store document link)
 href='showbidDocument/' + bidData.b_id_parent
"""

import json
import scrapy

payload = {
    "param": {
        "searchBid": "",
        "searchType": "fullText"
    },
    "filter": {
        "bidStatusType": "ongoing_bids",
        "byType": "all",
        "highBidValue": "",
        "byEndDate": {
            "from": "",
            "to": ""
        },
        "sort": "Bid-End-Date-Oldest"
    },
}

clean_d = []


class BidSpider(scrapy.Spider):
    name = 'bid_spider'
    start_urls = ['https://bidplus.gem.gov.in/all-bids']

    def parse(self, response):
        data = {"payload": payload,
                "csrf_bd_gem_nk":
                    response.headers.getlist('Set-Cookie')[0].decode("utf-8").split('; ')[0].split("=")[
                        1]}
        return scrapy.FormRequest(
            url="https://bidplus.gem.gov.in/all-bids-data", formdata=data, callback=self.parse_load_bid,
            cb_kwargs={"page_num": 2}
        )

    def parse_load_bid(self, response, page_num):
        res = json.loads(response.body)
        for doc in res['response']['response']['docs']:
            item = ""
            if len(doc['b_category_name'][0]) > 30:
                truncated_category_name = doc['b_category_name'][0][:30]
                item += truncated_category_name
            else:
                boq_title = doc.get('bbt_title', '')
                category_name = doc['b_category_name'][0]

                if boq_title:
                    item += f'{category_name} ({boq_title})'
                else:
                    item += category_name

            clean_d.append({
                # prob with
                # 'Bid_No': doc.get('b_bid_number_parent', '')[0],
                # is that if the key is not found it returns ''[0] which is 'N'
                'Bid_No': doc.get('b_bid_number_parent', ''),
                'Ra_No': doc.get('b_bid_number', ''),
                'Items': item,
                'Quantity': doc.get('b_total_quantity', ''),
                'Department': doc.get('ba_official_details_deptName', ''),
                'Start_date': doc.get('final_start_date_sort', ''),
                'End_date': doc.get('final_end_date_sort', ''),
                'doclink': doc.get('b_id_parent', '')
            })

        if page_num <= 3:  # math.ceil(res.get('response','').get('response', '').get('numFound', '')/10):
            data = {"payload": {"page": page_num, **payload},
                    "csrf_bd_gem_nk":
                        response.headers.getlist('Set-Cookie')[0].decode("utf-8").split('; ')[0].split("=")[
                            1]}
            scrapy.FormRequest(
                url="https://bidplus.gem.gov.in/all-bids-data", formdata=data, callback=self.parse_load_bid,
                cb_kwargs={"page_num": page_num + 1}, dont_filter=True
            )

        return clean_d
