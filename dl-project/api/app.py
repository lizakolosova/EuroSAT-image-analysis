
from flask import Flask
from flask_cors import CORS

from config import Config
from utils.logger import setup_logger
from models.model_loader import ModelLoader
from preprocessing.image_processor import ImagePreprocessor
from predictor import PredictionEngine
from routes import api_bp, init_routes
from error_handlers import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, origins=config_class.CORS_ORIGINS)

    logger = setup_logger('eurosat-api', log_file='logs/api.log')

    try:
        logger.info("Initializing application components...")

        model_loader = ModelLoader(
            model_path=config_class.MODEL_PATH,
            device=config_class.DEVICE,
            num_classes=config_class.NUM_CLASSES,
            logger=logger
        )
        model = model_loader.load_model(architecture='resnet50')

        preprocessor = ImagePreprocessor(image_size=224)

        prediction_engine = PredictionEngine(
            model=model,
            device=config_class.DEVICE,
            class_names=config_class.CLASS_NAMES,
            logger=logger
        )

        init_routes(config_class, preprocessor, prediction_engine, logger)
        app.register_blueprint(api_bp)

        register_error_handlers(app, logger)

        logger.info("Application initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise

    return app

if __name__ == '__main__':
    app = create_app()

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
