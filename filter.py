from flask import request, Response, jsonify, make_response
from flask_restx import Resource, Api, Namespace
import json
from pandas.io.json import json_normalize
from sql import SQL,SQLRequest
from util import Util

FILTER = Namespace('products/filter')


@FILTER.route('')
class Filter(Resource):
    def get(self):
        connection = SQL()
        util = Util()
        erorr_msg = {}
        data = SQLRequest()
        try:
            cvs = request.args.get('cvs')
            event = request.args.get('event')
            offset = request.args.get('offset')
            limit = request.args.get('limit')
            order = request.args.get('order-by')

            if cvs is None:
                erorr_msg['message'] = 'cvs is empty'
            else : 
                data.add('cvs',cvs)

            if event is None:
                erorr_msg['message'] = 'event is empty'
            else : 
                data.add('event',event)
                
            if offset is not None:
                if not offset.isdecimal():
                    erorr_msg['message'] = f'offset must be a integer : {offset}'
                else:
                     data.set_offset(offset)
            
            if limit is not None:
                if not limit.isdecimal():
                    erorr_msg['message'] = f'limit must be a integer : {limit}'
                else:
                     data.set_limit(limit)

            if order is not None:
                if order != 'asc' and order != 'desc':
                    erorr_msg['message'] = f'order must be asc or desc : {order}'
                else:
                     data.set_order_by(order)
            
            if len(erorr_msg) == 0:
                res = connection.processDB(data)
                #return res
                return jsonify(util.make_response_json(res))
            else:
                return make_response( jsonify(erorr_msg),400)

        except Exception as e:
            print(f"error {e}")
            raise e



