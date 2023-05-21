from flask import Flask
import json

from recommendations import Recommender

recommender = Recommender(primary_column='description')


app = Flask(__name__)

@app.route("/get_query_results/<top_n>/<query>")
def query_results(query, top_n):

    print("\n Query Received : {}".format(query))
    query_split = query.split('_')

    if len(query_split) == 1:
        final_query = query_split[0]
        print("Main Query : {}".format(final_query))
    else:


        feature_dict = eval('_'.join(query_split[1:]))
        print('Feature dict : {}'.format(feature_dict))

        # main_query = query_split[0]
        if  query_split[0] == '':
            main_query = feature_dict['query']
        else :
            main_query = query_split[0]

        print("Main Query : {}".format(main_query))
        sub_query = ''
        if feature_dict['query'] == 'shirt':
            sub_query += feature_dict['sleeve'] +  ' ' + 'sleeve' +  ' ' + feature_dict['Neckline'] + ' ' +  'neckline' +  ' ' + feature_dict['Cloth_Material']
        elif feature_dict['query'] == 'shoes':
            sub_query += feature_dict['Footwear_Type'] +  ' ' + feature_dict['ShoeMaterial']
        elif feature_dict['query'] == 'bra':
            sub_query += ''
        elif feature_dict['query'] == 'earing':
            sub_query += feature_dict['Jewellery_Material'] +  ' ' + feature_dict['Jewellery_Ocassion']
        elif feature_dict['query'] == 'pant':
            sub_query += feature_dict['Waist'] +  ' ' + 'waist' +  ' ' + feature_dict['Bottom_Wear_Length'] +  ' ' +  'length' + ' ' + feature_dict['cloth_material']

        final_query = main_query + ' ' + sub_query + ' ' + main_query 

    print("final_query : {}".format(final_query))
    recommendation_indices, recommendation_asins = recommender.return_most_similar(query=final_query, top_n=top_n)
    # print(recommendations)
    return [str(i) for i in recommendation_asins]

@app.route("/similar_products/<asin>")
def similarity_results(asin):
    recommendation_indices = recommender.get_image_based_similar_items(product_asin=asin)
    # print(recommendations)
    return [str(i) for i in recommendation_indices]


@app.route("/")
def home():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5743)