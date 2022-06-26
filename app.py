from flask import Flask
from flask import request
from schemas import Imports_schema, Get_schema, Stats_schema, ErrorSchema
from sqlalchemy import and_
from utils import *
from models import *
from collections import defaultdict
from dateutil import parser
from dateutil.relativedelta import *
from marshmallow.exceptions import ValidationError
from sqlalchemy import func
import  json


"""
function, that changes path for all element children after rebase
"""
def rebase_children(db, rebased_id, new_path, upd_time):
    to_rebase = db.session.query(Product).filter(Product.path.contains(rebased_id + '.'))
    for i in to_rebase:
        i.path = new_path + i.path.split('.' + rebased_id)[1]
        upd_entry = Update(id=i.id, name=i.name, parentId=i.parentId, type=i.type,
                           price=i.price, date=upd_time, path=new_path + i.path.split('.' + rebased_id)[1])
        upd_entry.rebased = True
        db.session.add(upd_entry)
    db.session.flush()


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mynameismike99@localhost/products'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ml:ya_project@db:5432/products'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
import_schema = Imports_schema()
db.create_all(app=app)
#test function
@app.route('/')
def hello_world():
    return json.dumps(hello='world')
@app.route('/imports', methods=['POST'])
def products_import():
    try:
        import_dic = import_schema.load(request.json)
    except ValidationError as e:
        return ErrorSchema().dump({'error': 400, 'message': str(e.messages)}), 400
    update_time = import_dic['updateDate']
    import_dic = import_dic['items']
    add_order = []
    ids = {}
    p_ids = set()
    id_p_id = {}
#   creates parent-child dictionary and checks for duplocates
    for product in import_dic:
        ids[product['id']] = product
        p_ids.add(product['parentId'])
        if not product['id'] in id_p_id.keys():
            id_p_id[product['id']] = product['parentId']
        else:
            return ErrorSchema().dump({'error': 400, 'message': 'Two elements with the same id'}), 400
    trees = id_p_id.keys() & p_ids #elements, which have parent_id in the same import
#    determines order to add elements, so when element is added, its parent is already in database
    while (trees) != set():
        trees_c = trees.copy()
        for i in trees_c:
            if not id_p_id[i] in trees:
                add_order.append(i)
                trees.remove(i)
    add_last = list(id_p_id.keys() - p_ids)
    add_order.extend(add_last)
    ids_to_update_time = set() # to update parent categories time
#    adds/updates elements to database
    for i in add_order:
        product = ids[i]
        path = ''
        if product['parentId'] != None:
            parent = db.session.query(Product).get(product['parentId'])
            if parent != None:
                ids_to_update_time.update(parent.path.split('.'))
                path = parent.path + '.' + product['id']
            else:
                return ErrorSchema().dump({'error': 400, 'message': 'No parent id in database'}), 400
        else:
            path = product['id']
        p_entry = Product(id=product['id'], name=product['name'], parentId=product['parentId'], type=product['type'],
                          price=product['price'], date=update_time, path=path)
        to_update = db.session.query(Product).get(product['id'])
        if to_update != None and to_update.type.value == product['type']:
            p_entry.isupdated = True
            if to_update.parentId != product['parentId']:
                rebase_children(db, product['id'], path, update_time)
            db.session.merge(p_entry)
        elif to_update != None and to_update.type != product['type']:
            return ErrorSchema().dump({'error': 400, 'message': 'Can\'t change item type on update'}), 400
        else:
            db.session.add(p_entry)
        upd_entry = Update(id=product['id'], name=product['name'], parentId=product['parentId'], type=product['type'],
                           price=product['price'], date=update_time, path=path)
        db.session.add(upd_entry)

    ids_to_update_time = list(ids_to_update_time - (id_p_id.keys() & p_ids))
    db.session.commit()
    db.session.query(Product).filter(Product.id.in_(ids_to_update_time)).update({Product.date: update_time})
    db.session.commit()
    return 'ok', 200


@app.route('/delete/<string:item_id>', methods=['DELETE'])
def products_delete(item_id):
    if not (is_uuid(item_id)):
        return ErrorSchema().dump({'error': 400, 'message': 'Wrong input'}), 400
    to_delete = db.session.query(Product).filter_by(id=item_id)
    if to_delete.first() == None:
        return ErrorSchema().dump({'error': 404, 'message': 'Item not found'}), 404
    to_delete.delete()
    db.session.commit()
    return 'ok', 200


@app.route('/nodes/<string:item_id>')
def get_product(item_id):
    if not (is_uuid(item_id)):
        return ErrorSchema().dump({'error': 400, 'message': 'Wrong input'}), 400
#   gets all children by looking for element id in path string, order by path, so elements are ordered by tree levels
    to_get = db.session.query(Product).filter(Product.path.contains(item_id)).order_by(Product.path.desc()).all()
    if to_get == []:
        return ErrorSchema().dump({'error': 404, 'message': 'Item not found'}), 404
    to_get = {str(i.id): row_to_dict(i) for i in to_get}
    add_order = list(to_get.keys())
    cat_prices = defaultdict(list)
# builds tree dict for node
    for i in add_order[0:-1]:
        parent = str(to_get[i]['parentId'])
        if 'children' in to_get[parent].keys():
            to_get[parent]['children'].append(to_get[i])
        else:
            to_get[parent]['children'] = [to_get[i]]
        if to_get[i]['type'] == 'CATEGORY' and 'children' in to_get[i].keys():
            to_get[i]['price'] = sum(cat_prices[i]) // len(cat_prices[i])
            cat_prices[parent].extend(cat_prices[i])
        elif to_get[i]['type'] == 'OFFER':
            cat_prices[parent].append(to_get[i]['price'])
        else:
            to_get[i]['price'] = None
        to_get.pop(i)

    if to_get[item_id]['type'] == 'CATEGORY' and 'children' in to_get[item_id].keys():
        to_get[item_id]['price'] = sum(cat_prices[item_id]) // len(cat_prices[item_id])
    schema = Get_schema()
    return schema.dump(to_get[item_id], ), 200


@app.route('/sales', methods=['GET'])
def sales():
    args = request.args
    if not ('date' in args.keys() and is_datetime(args['date'])):
        return ErrorSchema().dump({'error': 400, 'message': 'Wrong input'}), 400
    date = parser.isoparse(args['date'])
    day_before = date + relativedelta(days=-1)
    q = db.session.query(Product).filter(
        and_(Product.date.between(day_before, date), Product.type == 'OFFER', Product.isupdated == True))
    items = []
    for i in q:
        items.append(row_to_dict(i))
    return Stats_schema().dump({'items': items}), 200


@app.route('/node/<string:item_id>/statistic', methods=['GET'])
def stats(item_id):
    args = request.args
    if not (is_uuid(item_id) and 'dateStart' in args.keys() and 'dateEnd' in args.keys() and is_datetime(
            args['dateStart']) and is_datetime(args['dateEnd'])):
        return ErrorSchema().dump({'error': 400, 'message': 'Wrong input'}), 400
    dateStart = parser.isoparse(args['dateStart'])
    dateEnd = parser.isoparse(args['dateEnd'])
    id_updates = db.session.query(Update.id).filter(
        Update.id == item_id).first()
    if id_updates == None:
        return ErrorSchema().dump(
            {'error': 404, 'message': 'Updates for this element during the period not found'}), 404
    q = db.session.query(Update).filter(
        and_(Update.id == item_id, Update.date.between(dateStart, dateEnd), Update.rebased == False))
    el_type = q.first()
    if el_type != None:
        el_type = el_type.type
    items = []
#   gets item history list
    if el_type == 'OFFER':
        for i in q:
            items.append(row_to_dict(i))
    else:
#   for category objets calculates mean of their children
        for i in q:
            offers = db.session.query(Update.id).filter(
                and_(Update.path.contains(item_id + '.'), Update.date <= i.date, Update.type == 'OFFER')).all()
            offer_ids = [r[0] for r in offers]
            m_price = db.session.query(Update.id, func.max(Update.date), Update.price, Update.path).filter(
                Update.id.in_(offer_ids)).group_by(Update.id,
                                                   Update.price, Update.path).subquery()
            mean = db.session.query(func.avg(m_price.c.price)).filter(Update.path.contains(item_id + '.')).all()
            if not mean[0][0] is None:
                i.price = int(mean[0][0])
            items.append(row_to_dict(i))
    return Stats_schema().dump({'items': items}), 200


if __name__ == '__main__':
    app.run()
