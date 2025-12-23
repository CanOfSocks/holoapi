from flask import Flask, request, jsonify, render_template_string
from flask_caching import Cache
import blake3
import os
import logging
from dotenv import load_dotenv

from docs_page import html_template
import markdown

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60 * 60  # 1 hour
# Config and initialization (adjust your actual config here)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 1800  # seconds

# MySQL connection via SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("connection_string")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cache = Cache(app)

# Assuming you have already created db and models (Channel, Format, Thumbnail, Video, VideoFormat)
from models import db, Channel, Format, Thumbnail, Video, VideoFormat  # import your models
from sqlalchemy import inspect, asc, desc
from sqlalchemy.orm import joinedload

db.init_app(app)

def make_cache_key():
    key = request.full_path.encode('utf-8')
    return blake3.blake3(key).hexdigest()

def get_paginated_response(query, page, per_page):
    total_items = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    items_data = [item.as_dict() for item in items]

    return {
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'total_pages': (total_items + per_page - 1) // per_page,
        'items': items_data
    }

def get_page_and_per_page():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        if page < 1 or per_page < 1:
            raise ValueError()
    except ValueError:
        return None, None, jsonify({'error': 'Invalid pagination parameters'}), 400
    per_page = min(per_page, 100)
    return page, per_page, None, None

def apply_filters_and_sorting(model, query, request_args):
    mapper = inspect(model)
    valid_columns = {c.key: getattr(model, c.key) for c in mapper.attrs}

    # Operator mapping
    operators = {
        '__eq': lambda col, val: col == val,
        '__neq': lambda col, val: col != val,
        '__lt': lambda col, val: col < val,
        '__lte': lambda col, val: col <= val,
        '__gt': lambda col, val: col > val,
        '__gte': lambda col, val: col >= val,
        '__like': lambda col, val: col.like(f"%{val}%")
    }

    # Apply filters
    for key, value in request_args.items():
        if key in ['page', 'per_page', 'sort_by', 'sort_order']:
            continue

        for op_suffix in operators.keys():
            if key.endswith(op_suffix):
                col_name = key[:-len(op_suffix)]
                operator_func = operators[op_suffix]
                break
        else:
            col_name = key
            operator_func = operators['__eq']

        if col_name in valid_columns:
            column = valid_columns[col_name]
            try:
                python_type = column.property.columns[0].type.python_type
                if python_type == bool:
                    if value.lower() in ['true', '1', 'yes']:
                        cast_value = True
                    elif value.lower() in ['false', '0', 'no']:
                        cast_value = False
                    else:
                        cast_value = bool(value)
                else:
                    cast_value = python_type(value)
            except (AttributeError, ValueError, TypeError):
                cast_value = value

            query = query.filter(operator_func(column, cast_value))

    # Apply sorting
    sort_by = request_args.get('sort_by', 'last_updated')
    sort_order = request_args.get('sort_order', 'desc').lower()

    if sort_by in valid_columns:
        column = valid_columns[sort_by]
        query = query.order_by(asc(column) if sort_order == 'asc' else desc(column))

    return query


from flask import send_from_directory
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
@cache.cached(key_prefix=make_cache_key)
def show_markdown():
    md_file_path = os.path.join('static', 'api_documentation.md')
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite', 'tables'])

    return render_template_string(html_template, content=html_content)

@app.route('/api/channel', methods=['GET'])
@cache.cached(key_prefix=make_cache_key)
def get_channels():
    page, per_page, error_response, status = get_page_and_per_page()
    if error_response:
        return error_response, status
    try:
        query = Channel.query
        query = apply_filters_and_sorting(Channel, query, request.args)
        data = get_paginated_response(query, page, per_page)
        return jsonify(data)
    except Exception as e:
        logging.exception("Error retrieving channel info:")
        return jsonify({'error': "An unexpected error occurred"}), 500

@app.route('/api/format', methods=['GET'])
@cache.cached(key_prefix=make_cache_key)
def get_formats():
    page, per_page, error_response, status = get_page_and_per_page()
    if error_response:
        return error_response, status
    try:
        query = Format.query
        query = apply_filters_and_sorting(Format, query, request.args)
        data = get_paginated_response(query, page, per_page)
        return jsonify(data)
    except Exception as e:
        logging.exception("Error retrieving format info:")
        return jsonify({'error': "An unexpected error occurred"}), 500


@app.route('/api/thumbnail', methods=['GET'])
@cache.cached(key_prefix=make_cache_key)
def get_thumbnails():
    page, per_page, error_response, status = get_page_and_per_page()
    if error_response:
        return error_response, status
    try:
        query = Thumbnail.query
        query = apply_filters_and_sorting(Thumbnail, query, request.args)
        data = get_paginated_response(query, page, per_page)
        return jsonify(data)
    except Exception as e:
        logging.exception("Error retrieving thumbnail info:")
        return jsonify({'error': "An unexpected error occurred"}), 500


@app.route('/api/video', methods=['GET'])
@cache.cached(key_prefix=make_cache_key)
def get_videos():
    page, per_page, error_response, status = get_page_and_per_page()
    if error_response:
        return error_response, status

    try:
        query = Video.query
        query = apply_filters_and_sorting(Video, query, request.args)

        data = get_paginated_response(query, page, per_page)
        return jsonify(data)

    except Exception as e:
        logging.exception("Error retrieving video info:")
        return jsonify({'error': "An unexpected error occurred"}), 500


@app.route('/api/video_format/<string:video_id>', methods=['GET'])
@cache.cached(key_prefix=make_cache_key)
def get_video_formats(video_id):
    page, per_page, error_response, status = get_page_and_per_page()
    if error_response:
        return error_response, status

    try:
        query = (
            VideoFormat.query
            .filter_by(video_id=video_id)
            .options(joinedload(VideoFormat.format_rel))
        )
        query = apply_filters_and_sorting(VideoFormat, query, request.args)
        data = get_paginated_response(query, page, per_page)
        return jsonify(data)

    except Exception as e:
        logging.exception("Error retrieving video format info:")
        return jsonify({'error': "An unexpected error occurred"}), 500


if __name__ == '__main__':
    app.run(port=8000)
