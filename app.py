from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Contoh data sepatu
shoes = {
    "1": {"name": "Shoe 1", "price": 100000},
    "2": {"name": "Shoe 2", "price": 200000},
    "3": {"name": "Shoe 3", "price": 300000}
}

# Contoh data review
reviews = {
    "1": [{"review_id": "1", "text": "Good shoe!", "rating": 5}],
    "2": [{"review_id": "2", "text": "Comfortable", "rating": 4}]
}

class ShoeList(Resource):
    def get(self):
        return jsonify(shoes)

class ShoeDetail(Resource):
    def get(self, shoe_id):
        shoe = shoes.get(shoe_id)
        if shoe:
            return jsonify(shoe)
        return {"message": "Shoe not found"}, 404

class AddShoe(Resource):
    def post(self):
        new_id = str(len(shoes) + 1)
        data = request.get_json()
        shoes[new_id] = data
        return {"message": "Shoe added", "shoe": shoes[new_id]}, 201

class UpdateShoe(Resource):
    def put(self, shoe_id):
        if shoe_id in shoes:
            data = request.get_json()
            shoes[shoe_id].update(data)
            return {"message": "Shoe updated", "shoe": shoes[shoe_id]}
        return {"message": "Shoe not found"}, 404

class DeleteShoe(Resource):
    def delete(self, shoe_id):
        if shoe_id in shoes:
            deleted_shoe = shoes.pop(shoe_id)
            return {"message": "Shoe deleted", "shoe": deleted_shoe}
        return {"message": "Shoe not found"}, 404

class ShoeReview(Resource):
    def get(self, shoe_id):
        if shoe_id in reviews:
            return jsonify(reviews[shoe_id])
        return {"message": "No reviews found for this shoe"}, 404

    def post(self, shoe_id):
        if shoe_id in shoes:
            review_id = str(len(reviews.get(shoe_id, [])) + 1)
            data = request.get_json()
            new_review = {"review_id": review_id, "text": data.get("text"), "rating": data.get("rating")}
            reviews.setdefault(shoe_id, []).append(new_review)
            return {"message": "Review added", "review": new_review}, 201
        return {"message": "Shoe not found"}, 404

    def delete(self, shoe_id, review_id):
        if shoe_id in reviews:
            shoe_reviews = reviews[shoe_id]
            for review in shoe_reviews:
                if review["review_id"] == review_id:
                    shoe_reviews.remove(review)
                    return {"message": "Review deleted", "review": review}
            return {"message": "Review not found"}, 404
        return {"message": "No reviews found for this shoe"}, 404

# Menambahkan endpoint ke API
api.add_resource(ShoeList, '/shoes')
api.add_resource(ShoeDetail, '/shoes/<string:shoe_id>')
api.add_resource(AddShoe, '/shoes/add')
api.add_resource(UpdateShoe, '/shoes/update/<string:shoe_id>')
api.add_resource(DeleteShoe, '/shoes/delete/<string:shoe_id>')
api.add_resource(ShoeReview, '/shoes/<string:shoe_id>/reviews', '/shoes/<string:shoe_id>/reviews/<string:review_id>')

if __name__ == '__main__':
    app.run(debug=True)
