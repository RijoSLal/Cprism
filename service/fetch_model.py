import mlflow
from mlflow.client import MlflowClient
from dotenv import load_dotenv
import logging 
import os
import log_config
import yaml

log_config.config_setup()
logger = logging.getLogger(__name__)

load_dotenv()


class Fetch_model():
    def __init__(self,user_id: str):
        mlflow.set_tracking_uri(user_id)
        self.client = MlflowClient()
        """
        Initializes the client API to Mlflow to download model from artifact
        """

    def channel_model(self,model_artifact: str, version: str, model_file: str) -> str:
        """
        Args:
            model_artifact(str): artifact name in the registry
            version(str): version of registered model 
            model_file(str): model file with .pt extension
        Return:
            str: downloaded model's path 
        """

        model_version = self.client.get_model_version(name=model_artifact, version=version)
        artifact_uri = model_version.source

        try:
           downloaded_path = mlflow.artifacts.download_artifacts(artifact_uri=artifact_uri)
           model_path = os.path.join(downloaded_path, model_file)
           logger.info(f"Model retrieval successful {model_path}")
           return model_path
        
        except Exception as e:
            logger.exception(f"Failed to download the model from registry: {e}")


#for future updations

class Params:
    """
    This class handles all configurations applied on this API

    """
    def __init__(self,yaml_file: str):
        self.yaml_file = yaml_file

    
    def yaml_file_parameters(self) -> dict:
        """
        Returns:
            dict: returns inference_params in yaml file
        """
        try:
            with open("config.yaml","r") as file:
                params = yaml.safe_load(file)
                logger.info("Parameters are loaded successfully")
                return params
            
        except FileNotFoundError:
            logger.error("File not found!")
            return None 
        except Exception as e:
            logger.exception(f"Error occured in extracting parameters: {e}")