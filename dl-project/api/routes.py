
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import traceback

api_bp = Blueprint('api', __name__, url_prefix='/api')

config = None
preprocessor = None
prediction_engine = None
logger = None

def init_routes(app_config, img_preprocessor, pred_engine, app_logger):
    global config, preprocessor, prediction_engine, logger
    config = app_config
    preprocessor = img_preprocessor
    prediction_engine = pred_engine
    logger = app_logger

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': prediction_engine is not None,
        'device': config.DEVICE
    })

@api_bp.route('/classes', methods=['GET'])
def get_classes():
    return jsonify({
        'classes': [
            {'id': i, 'name': name}
            for i, name in enumerate(config.CLASS_NAMES)
        ]
    })

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        if prediction_engine is None:
            logger.error("Prediction engine not initialized")
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please check server logs.'
            }), 500

        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Empty filename'
            }), 400

        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if file_ext not in config.ALLOWED_EXTENSIONS:
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(config.ALLOWED_EXTENSIONS)}'
            }), 400

        image_bytes = file.read()
        if len(image_bytes) > config.MAX_IMAGE_SIZE:
            return jsonify({
                'success': False,
                'error': f'Image too large. Maximum size: {config.MAX_IMAGE_SIZE / (1024 *1024)}MB'
            }), 400

        try:
            image_tensor, original_image = preprocessor.preprocess(image_bytes)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

        result = prediction_engine.predict(image_tensor)

        result['image_info'] = {
            'filename': filename,
            'size': len(image_bytes),
            'dimensions': f"{original_image.width}x{original_image.height}"
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again.'
        }), 500
