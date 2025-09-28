
from transformers import pipeline

def get_pipe():
	return pipeline("text-classification", model="Dc-4nderson/tone-classifier")
