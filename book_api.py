import json

from odoo import http
from odoo.http import request

class BookApi(http.Controller):

    @http.route("/api/book", methods=["POST"], type="http", auth="none", csrf=False)
    def post_book(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "message": "name is require"
            }, status=400)
        try:
            res = request.env['library.book'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "book has been created successfully",
                    "name": res.name,
                },status=201)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)


    @http.route("/api/book/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_book_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['library.book'].sudo().create(vals)
        if res:
            # return list of dictionary
            return [{
                "message": "book has been created successfully"
            }]

    @http.route('/v1/book/<int:book_id>', methods=['PUT'], type='http', auth='none', csrf=False)
    def update_book(self, book_id):
       try:
            book_id = request.env['library.book'].sudo().search([('id', '=', book_id)])
            if not book_id:
                return request.make_json_response({
                    "message": "id doen't exist"
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            book_id.write(vals)
            return request.make_json_response({
                "message": "book has been update successfully",
                "id" : book_id.id,
                "name": book_id.name,
            }, status=201)
       except Exception as error:
           return request.make_json_response({
               "message": "error"
           }, status=400)


    @http.route('/v1/book/<int:book_id>',methods=['GET'], type='http', auth='none', csrf=False)
    def get_book(self, book_id):
        try:
            book_id = request.env['library.book'].sudo().search([('id', '=', book_id)])
            if not book_id:
                return request.make_json_response({
                    "message": "There is no book with this id"
                }, status=400)
            return request.make_json_response({
                "id": book_id.id,
                "name": book_id.name,
            }, status=201)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)



